
from fastapi import FastAPI
from app.schemas import QuestionInput, AnswerResponse
from app.services.agent import ask_agent

app = FastAPI(
    title="NusantaraCare AI Assistant",
    description="Asisten GenAI berbasis RAG",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message": "NusantaraCare AI Assistant is running"}

@app.post("/ask", response_model=AnswerResponse)
def ask(question: QuestionInput):
    result = ask_agent(question.text)
    return result
