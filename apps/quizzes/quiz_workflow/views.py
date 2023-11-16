from rest_framework.generics import ListAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.quizzes.models import QuizModel
from apps.quizzes.quiz_workflow.filters import QuizResultFilter
from apps.quizzes.quiz_workflow.helper import (
    create_export_data,
    create_export_response,
    create_file_name,
)
from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.serializers import QuizResultSerializer
from core.permisions.quizz_permission import ExportQuizResultPermission


class QuizWorkflow(ListCreateAPIView):
    queryset = QuizResultModel.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        quiz_id = self.request.query_params.get('quiz_id')
        quiz = get_object_or_404(QuizModel, pk=quiz_id)
        serializer.save(user=self.request.user, company=quiz.company, quiz=quiz)


class QuizResultCSVExportView(ListAPIView):
    serializer_class = QuizResultSerializer
    permission_classes = [IsAuthenticated, ExportQuizResultPermission]
    filterset_class = QuizResultFilter

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(queryset, many=many, )

    def get_queryset(self):
        queryset = QuizResultModel.objects.all()
        params_dict = self.request.query_params.dict()
        if 'quiz' in params_dict:
            return queryset.filter(user=self.request.user.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        params_dict = self.request.query_params.dict()
        export_format = params_dict.get('file_format', None)

        filename = create_file_name(params_dict=params_dict, user=self.request.user)

        export_data = create_export_data(quiz_votes_list=queryset, serializer=QuizResultSerializer,
                                         file_format=export_format)
        response = create_export_response(filename=filename, content=export_data, file_format=export_format)
        return response
