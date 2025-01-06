from pydantic import BaseModel, Field
from typing import List

class ConversationResponse(BaseModel):
    answer: str

class ConversationCreate(BaseModel):
    question: str