import os

from django.core.cache import cache

from apps.quizzes.quiz_workflow.schemas import VoteData


def save_quiz_vote_to_redis(user_id: int, company_id: int, quiz_id: int, question_id: int, user_answer,
                            is_correct: bool) -> None:
    """Stores the result of a vote in Redis cache."""
    key = f"user:{user_id}:company:{company_id}:quiz_id:{quiz_id}:question_id:{question_id}"
    expiration_time = os.environ.get('EXPIRATION_TIME')

    vote_data = VoteData(
        user_id=user_id,
        company_id=company_id,
        quiz_id=quiz_id,
        question_id=question_id,
        user_answer=user_answer,
        is_correct=is_correct
    )
    cache.set(key, vote_data.dict(), int(expiration_time))


def get_quiz_vote_from_redis(user_id: int, quiz_id: int, company_id: int, question_id: int) -> VoteData:
    """Retrieves the result of a vote from Redis."""
    key = f"user:{user_id}:company:{company_id}:quiz_id:{quiz_id}:question_id:{question_id}"

    quiz_vote_data = cache.get(key)
    return quiz_vote_data
