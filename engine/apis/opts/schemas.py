from pydantic import BaseModel, Field
from typing import List

class ConversationResponse(BaseModel):
    answer: str = Field(
        description="Answer from the AI", default=""
    )

class ConversationCreate(BaseModel):
    question: str = Field(
        description="Request to the AI", default=""
    )
    conversation_id: str = Field(
        description="Unique identifier for the conversation. Use the same value to retain history", default="1234"
    )