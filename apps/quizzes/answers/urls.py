from django.urls import path

from .views import QuizAnswerView

urlpatterns = [
    path('', QuizAnswerView.as_view(), name='answer_create'),
    path('/<int:pk>', QuizAnswerView.as_view(), name='answer_detail'),
]
