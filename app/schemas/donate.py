from pydantic import BaseModel


class Donate(BaseModel):
    pubId: str
    message: str
    amount: str
    currency: str