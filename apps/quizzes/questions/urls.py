from django.urls import include, path

from .views import QuizQuestionView

urlpatterns = [
    path('', QuizQuestionView.as_view(), name='create_question'),
    path('/<int:pk>', QuizQuestionView.as_view(), name='question_detail'),
    path('/<int:pk>/answer', include('apps.quizzes.answers.urls')),
]
