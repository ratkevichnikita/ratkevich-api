from gigachain import GigaChain
from gigachat import GigaChat
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Загрузите переменные окружения
load_dotenv()

class Assistant:
    def __init__(self):
        self.chain = GigaChain(
            authorization=os.getenv("AUTHORIZATION_KEY"),
            client_id=os.getenv("CLIENT_ID"),
            scope=os.getenv("SCOPE")
        )
        self.chat = GigaChat()
        self.docsearch = None  # Инициализируем позже

    def load_documents(self, texts):
        """
        Загружает тексты в векторное хранилище.
        """
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_text(texts)
        embeddings = OpenAIEmbeddings()
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
        response = self.chain.process(context=context, question=question)
        return response