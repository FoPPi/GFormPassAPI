from fastapi import HTTPException

from app.core.logger import logger
from app.db.base import db
from app.schemas import Answers


async def save_question(test_url: str, question: str, answers: Answers) -> bool:
    logger.info(f"Saving question: {question} to database",
                data={'test_url': test_url, 'question': question, 'answers': answers})
    try:
        logger.info("Checking if question already exists")
        condition = f"test_url = '{test_url}' AND question = '{question}'"
        selected = await db.select_data('questions', '*', condition)

        if len(selected) > 0:
            logger.warning(f"Question already exists: {question}",
                         data={'test_url': test_url, 'question': question, 'answers': answers})
            return False

        answers_array = db.to_pg_array(answers.text)

        # Insert question
        query = f"INSERT INTO questions (test_url, type, question, answers) VALUES ('{test_url}', '{answers.type}', '{question}', '{answers_array}');"
        await db.execute_transaction(query)
        logger.info(f"Question saved to database: {question}", data={'test_url': test_url, 'question': question, 'answers': answers})
        # await _db.insert_data('questions', {
        #     'test_url': test_url,
        #     'question': question,
        #     'answers': answers_array
        # })
        return True
    except Exception as e:
        logger.error(f"Failed to save question. Error: {e}", data={'test_url': test_url, 'question': question, 'answers': answers})
        return False

async def select_question(test_url: str, question: str):
    logger.info(f"Selecting question: {question}", data={'test_url': test_url, 'question': question})
    query = f"select_and_update_question('{test_url}', '{question}') as result"

    result = await db.select_data(query)

    if not result:
        return None

    return result[0]

async def delete_expired_questions():
    try:
        logger.info("Deleting expired questions")
        await db.execute_transaction('CALL delete_expired_questions()')

        return True
    except Exception as e:
        logger.error(f"Failed to delete expired questions. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))