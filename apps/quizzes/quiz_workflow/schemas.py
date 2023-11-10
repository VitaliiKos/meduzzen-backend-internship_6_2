from pydantic import BaseModel


class VoteData(BaseModel):
    user_id: int
    company_id: int
    quiz_id: int
    question_id: int
    user_answer: list[str]
    is_correct: bool
