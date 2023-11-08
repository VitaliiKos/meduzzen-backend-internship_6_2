from django.core.cache import cache


def save_quiz_vote_to_redis(user_id: int, company_id: int, quiz_id: int, question_id: int, user_answer,
                            is_correct: bool):
    """Stores the result of a vote in Redis cache."""
    key = f"user:{user_id}:company:{company_id}:quiz_id:{quiz_id}:question_id:{question_id}"
    expiration_time = 48 * 60 * 60
    vote_data = {
        'user_id': user_id,
        'company_id': company_id,
        'quiz_id': quiz_id,
        'question_id': question_id,
        'user_answer': user_answer,
        'is_correct': is_correct,
    }
    cache.set(key, vote_data, expiration_time)


def get_quiz_vote_from_redis(user_id: int, quiz_id: int, company_id: int, question_id: int):
    """Retrieves the result of a vote from Redis."""
    key = f"user:{user_id}:company:{company_id}:quiz_id:{quiz_id}:question_id:{question_id}"

    quiz_vote_data = cache.get(key)
    return quiz_vote_data
