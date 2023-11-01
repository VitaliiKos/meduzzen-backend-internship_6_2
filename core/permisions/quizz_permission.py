from rest_framework import permissions

from apps.companies.models import CompanyModel
from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.models import QuizModel
from apps.quizzes.questions.models import QuestionModel


class QuizPermission(permissions.BasePermission):
    """Custom permission class for quiz access control.

    Allows 'owner' and 'admin' roles to access quizzes and quiz lists.
    Safe methods (GET, HEAD, OPTIONS) are always allowed.
    """

    def has_object_permission(self, request, view, obj):
        print(obj.__dict__)
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

