from django.urls import path

from .views import QuizWorkflow

urlpatterns = [
    path('', QuizWorkflow.as_view(), name='quiz_workflow'),
]
