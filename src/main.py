from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from assistant import Assistant
from utils import extract_text_from_folder
import os

app = FastAPI()

# Извлечение текста из PDF-файлов
doctors_text = extract_text_from_folder("data/doctors")
company_text = extract_text_from_folder("data/company")
sales_text = extract_text_from_folder("data/sales")

combined_text = doctors_text + company_text + sales_text

# Инициализация ассистента
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