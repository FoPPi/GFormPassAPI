from typing import List

from pydantic import BaseModel


class Option(BaseModel):
    text: str
    id: str

class Question(BaseModel):
    test_url: str
    title: str
    type: str
    options: List[Option]