from django_filters import rest_framework as filters

from apps.quizzes.quiz_workflow.models import QuizResultModel


class QuizResultFilter(filters.FilterSet):
    quiz = filters.NumberFilter(field_name='quiz__id', lookup_expr='exact')
    company = filters.NumberFilter(field_name='company__id', lookup_expr='exact')
    user = filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = QuizResultModel
        fields = ['quiz', 'user', 'company']
