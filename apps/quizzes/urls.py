from django.urls import path

from .views import QuizAnswerView, QuizQuestionView, QuizView

urlpatterns = [
    path('', QuizView.as_view(), name='quiz_list'),
    path('/<int:pk>', QuizView.as_view(), name='quiz_detail'),

    path('/question', QuizQuestionView.as_view(), name='create_question'),
    path('/question/<int:pk>', QuizQuestionView.as_view(), name='question_detail'),

    path('/answer', QuizAnswerView.as_view(), name='answer_create'),
    path('/answer/<int:pk>', QuizAnswerView.as_view(), name='answer_detail'),

]
