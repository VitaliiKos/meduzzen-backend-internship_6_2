import csv
import io
import json
import os
from decimal import Decimal

from django.core.cache import cache
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from rest_framework.exceptions import APIException, PermissionDenied
from rest_framework.generics import get_object_or_404

from apps.companies.models import CompanyModel
from apps.quizzes.models import QuizModel
from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.schemas import VoteData
from core.enums.file_format_enum import FileFormatEnum


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
    if 'company_id' in params_dict:
        company = get_object_or_404(CompanyModel, pk=params_dict['company_id'])
        if company.is_owner(user) or company.is_admin(user):
            return f'company_{company.name}_quiz_result'
        else:
            raise PermissionDenied("You don't have permission to access this resource.")

    elif 'quiz_id' in params_dict:
        return f"quiz_{params_dict['quiz_id']}_result_{user.last_name}"


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def create_export_data(quiz_votes_list, serializer, file_format):
    header = serializer.Meta.fields

    if file_format == FileFormatEnum.CSV.value:
        output = io.StringIO()
        writer = csv.DictWriter(output, delimiter=';', fieldnames=header, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in quiz_votes_list.values(*header):
            writer.writerow(row)

        content = output.getvalue()
        output.close()
        return content

    elif file_format == FileFormatEnum.JSON.value:
        data_list = [row for row in quiz_votes_list.values(*header)]
        return json.dumps(data_list, indent=4, cls=DecimalEncoder)

    else:
        raise ValueError("Invalid export format")


def create_export_response(filename: str, content: str, file_format: str) -> HttpResponse:
    if file_format == FileFormatEnum.CSV.value:
        response = HttpResponse(content=content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={filename}.csv'
    elif file_format == FileFormatEnum.JSON.value:
        response = JsonResponse(json.loads(content), safe=False, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename={filename}.json'
    else:
        raise ValueError("Invalid export format")

    return response


def filter_by_company(params_dict, authenticated_user):
    company = get_object_or_404(CompanyModel, pk=params_dict['company_id'])

    if not company.is_owner(authenticated_user) and not company.is_admin(authenticated_user):
        raise PermissionDenied("You don't have permission to access this resource.")

    user_id = params_dict.get('user_id', None)

    filter_conditions = Q(company=company)

    if user_id:
        if not company.has_member(user=user_id):
            raise APIException({"detail": "User isn't a member of your company."})
        filter_conditions &= Q(user=user_id)
    return QuizResultModel.objects.filter(filter_conditions)


def filter_by_quiz(params_dict, authenticated_user) -> list[QuizResultModel]:
    quiz = get_object_or_404(QuizModel, pk=params_dict['quiz_id'])
    return QuizResultModel.objects.filter(quiz=quiz, user=authenticated_user)
