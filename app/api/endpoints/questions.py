from fastapi import APIRouter, Depends, Request

from app.core.rate_limiter import user_key_rate_limit
from app.core.security import verify_api_key, verify_admin_key
from app.db.questions import select_question, save_question, delete_expired_questions
from app.libs.assistant import Assistant
from app.schemas import Question

router = APIRouter()

assistant = Assistant()

@router.post("/question")
@user_key_rate_limit(calls=25, period=60)
async def gpt_request(
    request: Request,
    question_data: Question,
    api_key: str = Depends(verify_api_key),
    # user_key: str = Depends(verify_user_key) # Verify user key in user_key_rate_limit
):

    answer = await select_question(question_data.test_url, question_data.title)

    if answer['type_text'] != 'No matching question found':

        return {
            "info": "cached",
            "answers": {
              "type": answer['type_text'],
              "text": answer['answers_text']
            }
        }

    answers = await assistant.question(question_data)

    await save_question(question_data.test_url, question_data.title, answers)

    return {
        "info": "new",
        "answers": answers
    }

@router.delete("/question")
async def delete_question(
    _: str = Depends(verify_admin_key),
):
    await delete_expired_questions()
    return {"status": "success"}