from django.urls import include, path

from .views import QuizView

urlpatterns = [
    path('', QuizView.as_view(), name='quiz_list'),
    path('/<int:pk>', QuizView.as_view(), name='quiz_detail'),
    path('/<int:pk>/question', include('apps.quizzes.questions.urls'))
]
