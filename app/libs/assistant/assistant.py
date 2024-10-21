import json
import time

from fastapi import HTTPException
from openai import OpenAI

from app.core.config import settings
from app.core.logger import logger
from app.schemas import Question, Answers


class Assistant:
    _assistant_id: str
    _api_key: str

    def __init__(self):
        logger.info("Initializing OpenAI Assistant")
        self._assistant_id = settings.OPENAI_ASSISTANT_ID
        self._api_key = settings.OPENAI_API_KEY

    async def question(self, question_data: Question) -> Answers:

        logger.info(f"Asking question", data=question_data)
        client = OpenAI(api_key=self._api_key)

        prompt = _transform_question(question_data)

        try:
            logger.info("Creating thread and message")
            # Create thread and message in one step
            thread = client.beta.threads.create_and_run(
                assistant_id=self._assistant_id,
                thread={
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            logger.info("Waiting for completion")
            # Wait for completion with timeout
            start_time = time.time()
            while True:
                if time.time() - start_time > 10:  # 10 seconds timeout
                    logger.error("Assistant response took too long")
                    raise TimeoutError("Assistant response took too long")

                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.thread_id,
                    run_id=thread.id
                )
                if run.status == 'completed':
                    break
                time.sleep(0.5)

            # Get the last (assistant) message
            messages = client.beta.threads.messages.list(thread_id=thread.thread_id)
            answer_str = messages.data[0].content[0].text.value

            # Parse the JSON string
            answer_dict = json.loads(answer_str)

            # Create an instance of Answers
            answers = Answers(**answer_dict)

            return answers



        except Exception as e:
            logger.error(f"Failed to ask question: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))



def _transform_question(question_data: Question):

    # Constructing the formatted question
    formatted_question = f"Type {question_data.type}. Question {question_data.title}"

    # Extracting options and creating the formatted answers
    answers = []
    for option in question_data.options:
        answers.append(f"{option.text}")

    # Joining the answers in the required format
    formatted_answers = ", ".join(answers)

    # Returning the final result
    return f"{formatted_question} Answers {formatted_answers}"