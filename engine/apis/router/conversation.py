from ...common.logger import log
from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from ..opts.database import engine
from ..opts.schemas import ConversationResponse, ConversationCreate
from ..api import BaseEngineChatApi
# from ..opts.crud import create_room, get_all_rooms
from typing import List


router = APIRouter()

@router.post("/", response_model=ConversationResponse)
async def make_prompt(question: ConversationCreate):
    log.info(f"Received request to invoke question: {question.question}")
    return BaseEngineChatApi.subsclasses[0]().make_user_prompt(question.question)
