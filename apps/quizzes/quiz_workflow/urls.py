from django.urls import path

from .views import QuizResultCSVExportView, QuizWorkflow

urlpatterns = [
    path('', QuizWorkflow.as_view(), name='quiz_workflow'),
    path('/export_data', QuizResultCSVExportView.as_view(), name='quiz_result_export_data'),
]
