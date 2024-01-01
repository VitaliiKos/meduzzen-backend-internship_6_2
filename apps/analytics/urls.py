from django.urls import path

from .views import (
    AnalyticsView,
    CompanyMembersAnalyticsView,
    CompanyQuizzesAnalyticsView,
    QuizzesAnalyticsView,
    UserRatingView,
    UsersAverageView,
)

urlpatterns = [
    path('', AnalyticsView.as_view(), name='analytics'),
    path('/quizzes', QuizzesAnalyticsView.as_view(), name='quizzes_analytics'),
    path('/users', UserRatingView.as_view(), name='user_rating'),
    path('/users/list_of_average', UsersAverageView.as_view(), name='user_list_of_average'),
    path('/company/<int:pk>', CompanyQuizzesAnalyticsView.as_view(), name='company_quizzes_analytics'),
    path('/company/<int:pk>/members', CompanyMembersAnalyticsView.as_view(), name='company_members_analytics'),

]
