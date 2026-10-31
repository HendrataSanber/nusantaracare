
from pydantic import BaseModel

class QuestionInput(BaseModel):
    text: str

class AnswerResponse(BaseModel):
    answer: str
    confidence_label: str
    reason_code: str
