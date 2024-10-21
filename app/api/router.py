from fastapi import APIRouter

from app.api.endpoints import questions, users

api_router = APIRouter()
api_router.include_router(questions.router, tags=["questions"])
api_router.include_router(users.router, tags=["users"])