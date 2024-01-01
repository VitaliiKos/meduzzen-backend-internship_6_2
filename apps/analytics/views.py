from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.analytics.helper import (
    get_attempt_results_for_users,
    get_average_scores_by_quiz_and_company_over_time,
    get_average_scores_by_quizzes_for_user,
    get_quizzes_with_last_completions,
    members_last_attempt,
)
from apps.companies.models import CompanyModel
from apps.quizzes.quiz_workflow.models import QuizResultModel
from core.permisions.company_permission import IsCompanyOwnerOrAdmin


class UserRatingView(ListAPIView):
    queryset = QuizResultModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        params_dict = self.request.query_params.dict()
        user_id = params_dict['user_id'] if 'user_id' in params_dict else self.request.user.id
        if 'company_id' in params_dict:
            company = get_object_or_404(CompanyModel, pk=params_dict['company_id'])
            if not company.has_member(user=self.request.user):
                return Response({'detail': "You are not a company employee "})
            user_company_avg = QuizResultModel.get_company_rating(user=self.request.user, company=company.id)
            response = {'company_rating': user_company_avg}
        else:
            user_system_avg = QuizResultModel.get_system_rating(user=user_id)
            response = {'system_rating': user_system_avg}

        return Response(response, status=status.HTTP_200_OK)


class CompanyQuizzesAnalyticsView(ListAPIView):
    """List of quizzes and the time if it’s last completions.(2)"""
    queryset = CompanyModel.objects.all()
    permission_classes = (IsAuthenticated, IsCompanyOwnerOrAdmin)

    def list(self, request, *args, **kwargs):
        company = self.get_object()
        quizzes_list_with_last_completions = get_quizzes_with_last_completions(company_id=company.id)
        response = {'quizzes_list_with_last_completions': quizzes_list_with_last_completions}
        return Response(response, status=status.HTTP_200_OK)


class QuizzesAnalyticsView(ListAPIView):
    """List of average scores for each of the quiz from all companies with dynamics over time.(3)"""
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        list_of_average_for_all_quizzes_in_all_companies = get_average_scores_by_quiz_and_company_over_time()

        response = {
            'list_of_average_for_all_quizzes_in_all_companies': list_of_average_for_all_quizzes_in_all_companies}
        return Response(response, status=status.HTTP_200_OK)


class UsersAverageView(ListAPIView):
    """List of average scores of all users with dynamics over time.(4)"""
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        list_of_attempt_results_for_users = get_attempt_results_for_users()

        response = {'list_of_attempt_results_for_users': list_of_attempt_results_for_users}
        return Response(response, status=status.HTTP_200_OK)


class AnalyticsView(ListAPIView):
    """List of average scores for all quizzes of the selected user with dynamics over time.(5)"""
    queryset = QuizResultModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        user_average_scores_for_quizzes = get_average_scores_by_quizzes_for_user(user_id=self.request.user.id)
        return Response({'user_average_scores_for_quizzes': user_average_scores_for_quizzes}, status=status.HTTP_200_OK)


class CompanyMembersAnalyticsView(ListAPIView):
    """List of users of the company and their time of last completions.(6)"""
    queryset = CompanyModel.objects.all()
    permission_classes = (IsCompanyOwnerOrAdmin,)

    def list(self, request, *args, **kwargs):
        company = self.get_object()
        members_last_quiz_completion_times = members_last_attempt(company=company)
        response = {'members_last_quiz_completion_times': members_last_quiz_completion_times}
        return Response(response, status=status.HTTP_200_OK)
