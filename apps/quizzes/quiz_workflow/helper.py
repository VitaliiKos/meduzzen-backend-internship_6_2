import os

from django.core.cache import cache
from django.db.models import QuerySet
from django.http import HttpResponse
from rest_framework.generics import get_object_or_404

from apps.companies.models import CompanyModel
from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.schemas import VoteData
from core.enums.file_format_enum import FileFormatEnum
from core.utils.file_helper import FileExportHelper, FileExportResponseHelper


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


def create_file_name(params_dict, user) -> str:
    if 'company' in params_dict:
        company = get_object_or_404(CompanyModel, pk=params_dict['company'])
        return f'company_{company.name}_quiz_result'

    elif 'quiz' in params_dict:
        return f"quiz_{params_dict['quiz']}_result_{user.last_name}"


def create_export_data(quiz_votes_list: QuerySet[QuizResultModel], serializer, file_format: str) -> str:
    exporter = FileExportHelper(quiz_votes_list, serializer)

    if file_format == FileFormatEnum.CSV.value:
        return exporter.to_csv()
    elif file_format == FileFormatEnum.JSON.value:
        return exporter.to_json()
    else:
        raise ValueError("Invalid export format")


def create_export_response(filename: str, content: str, file_format: str) -> HttpResponse:
    response_helper = FileExportResponseHelper(filename, content, file_format)

    if file_format == FileFormatEnum.CSV.value:
        return response_helper.get_csv_response()
    elif file_format == FileFormatEnum.JSON.value:
        return response_helper.get_json_response()
    else:
        raise ValueError("Invalid export format")
