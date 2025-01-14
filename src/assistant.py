from langchain_gigachat import GigaChat
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_gigachat.embeddings import GigaChatEmbeddings
import os
from dotenv import load_dotenv

# Загрузите переменные окружения
load_dotenv()

class Assistant:
    def __init__(self):
        self.chat = GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),
            scope=os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS"),
            verify_ssl_certs=False  # Отключение проверки сертификатов (для тестирования)
        )
        self.docsearch = None  # Инициализируем позже

    def load_documents(self, texts):
        """
        Загружает тексты в векторное хранилище.
        """
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(texts)
        embeddings = GigaChatEmbeddings(credentials=os.getenv("GIGACHAT_CREDENTIALS"))
        self.docsearch = FAISS.from_texts(texts, embeddings)

    def ask(self, question):
        """
        Задает вопрос ассистенту.
        """
        if not self.docsearch:
            raise ValueError("Документы не загружены!")

        # Найдем релевантные фрагменты
        docs = self.docsearch.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])

        # Зададим вопрос
        response = self.chat.invoke(f"Контекст: {context}\n\nВопрос: {question}")
        return response.content