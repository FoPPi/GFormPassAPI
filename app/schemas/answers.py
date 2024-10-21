from typing import List

from pydantic import BaseModel


class Answers(BaseModel):
    type: str
    text: List[str]