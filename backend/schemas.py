from pydantic import BaseModel


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
    sources: list


class IngestResponse(BaseModel):
    message: str
    chunks_created: int