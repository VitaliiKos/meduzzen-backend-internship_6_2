from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from apps.companies.models import CompanyModel
from apps.quizzes.models import AnswerModel, QuestionModel, QuizModel


class QuizPermission(permissions.BasePermission):
    """Custom permission class for quiz access control.

    Allows 'owner' and 'admin' roles to access quizzes and quiz lists.
    Safe methods (GET, HEAD, OPTIONS) are always allowed.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, CompanyModel):
            return obj.is_owner(request.user.id) or obj.is_admin(request.user.id)
        if isinstance(obj, QuizModel):
            return obj.company.is_owner(request.user.id) or obj.company.is_admin(request.user.id)
        elif isinstance(obj, QuestionModel):
            return obj.quiz.company.is_owner(request.user.id) or obj.quiz.company.is_admin(request.user.id)
        elif isinstance(obj, AnswerModel):
            return obj.question.quiz.company.is_owner(request.user.id) or obj.question.quiz.company.is_admin(
                request.user.id)


class ExportQuizResultPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        params_dict = request.query_params.dict()
        if 'company' in params_dict:
            company = get_object_or_404(CompanyModel, pk=params_dict.get('company'))
            if 'user' in params_dict and not company.has_member(params_dict.get('user')):
                return False
            return company.is_owner(request.user.id) or company.is_admin(request.user.id)
        return True
