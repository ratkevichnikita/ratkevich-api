import os
import sys
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat
from langchain_gigachat.embeddings.gigachat import GigaChatEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
import pdfplumber
import base64

# Функция для извлечения текста из PDF
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Формирование авторизационных данных
client_id = "7b68f9d6-895f-448f-842a-b492f20f796b"  # Замените на ваш Client ID
client_secret = "N2I2OGY5ZDYtODk1Zi00NDhmLTg0MmEtYjQ5MmYyMGY3OTZiOjM3NTZjZDViLWVmY2YtNDFjZS1iZGJlLWZkMjE3OWI0ZTA3Mg=="  # Замените на ваш Client Secret
credentials = f"{client_id}:{client_secret}"
encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

# Инициализация GigaChat
giga = GigaChat(
    credentials=client_secret,  # Используем авторизационные данные
    verify_ssl_certs=False,
)

# Инициализация GigaChatEmbeddings для создания эмбеддингов
embeddings = GigaChatEmbeddings(
    credentials=client_secret,  # Используем авторизационные данные
    verify_ssl_certs=False,
)

# Пути к PDF-файлам
pdf_files = [
    os.path.join("data", "doctors", "azarovskaya_galina.pdf"),
    os.path.join("data", "company", "company.pdf")
]

# Проверка наличия файлов
for pdf_file in pdf_files:
    if not os.path.exists(pdf_file):
        print(f"Файл не найден: {pdf_file}")
    else:
        print(f"Файл найден: {pdf_file}")

# Загрузка и обработка PDF-файлов
documents = []
for pdf_file in pdf_files:
    if os.path.exists(pdf_file):
        try:
            loader = PyPDFLoader(pdf_file)
            loaded_docs = loader.load()
            print(f"Загружен документ: {pdf_file}")
            print(f"Количество страниц: {len(loaded_docs)}")
            print(f"Пример текста: {loaded_docs[0].page_content[:200]}...")  # Первые 200 символов первой страницы
            documents.extend(loaded_docs)
        except Exception as e:
            print(f"Ошибка при загрузке файла {pdf_file}: {e}")
    else:
        print(f"Файл {pdf_file} пропущен, так как он не найден.")

# Разделение текста на фрагменты
if documents:
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    splits = text_splitter.split_documents(documents)
    print(f"Текст разбит на {len(splits)} фрагментов.")
else:
    print("Нет документов для обработки.")
    exit()

# Создание базы данных эмбеддингов
try:
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
    )
    print("База данных эмбеддингов успешно создана.")
except Exception as e:
    print(f"Ошибка при создании базы данных эмбеддингов: {e}")
    exit()

# Создание цепочки RetrievalQA
qa_chain = RetrievalQA.from_chain_type(
    llm=giga,
    retriever=vectorstore.as_retriever(),
)

import sys

# Основной цикл диалога
while True:
    try:
        # Чтение ввода с обработкой ошибок кодировки
        user_input = input("Пользователь: ").encode('utf-8', errors='ignore').decode('utf-8')
    except Exception as e:
        print(f"Ошибка при чтении ввода: {e}")
        continue

    if user_input.lower() in ["пока", "exit", "quit"]:
        break

    # Получаем ответ от модели с использованием RAG
    try:
        response = qa_chain.invoke({"query": user_input})
        print("GigaChat: ", response["result"])
    except Exception as e:
        print(f"Ошибка при генерации ответа: {e}")