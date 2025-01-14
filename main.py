from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:3000", "https://localhost:3000"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Все настроено! Проверка автодеплоя"}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.assistant import Assistant
from src.utils import extract_text_from_folder
import os

app = FastAPI()

doctors_text = extract_text_from_folder("data/doctors")
company_text = extract_text_from_folder("data/company")
sales_text = extract_text_from_folder("data/sales")

combined_text = doctors_text + company_text + sales_text

assistant = Assistant()
assistant.load_documents(combined_text)

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        answer = assistant.ask(request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
import uvicorn
uvicorn.run(app, host="0.0.0.0", port=3000)