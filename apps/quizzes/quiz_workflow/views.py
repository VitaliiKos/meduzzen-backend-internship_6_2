from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.quizzes.models import QuizModel
from apps.quizzes.quiz_workflow.helper import (
    create_export_data,
    create_export_response,
    create_file_name,
    filter_by_company,
    filter_by_quiz,
)
from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.serializers import QuizResultSerializer


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
    permission_classes = [IsAuthenticated]

    def get_serializer(self, queryset, many=True):
        return self.serializer_class(queryset, many=many, )

    def get_queryset(self):
        params_dict = self.request.query_params.dict()
        if 'company_id' in params_dict:
            return filter_by_company(params_dict, authenticated_user=self.request.user)

        elif 'quiz_id' in params_dict:
            return filter_by_quiz(params_dict, authenticated_user=self.request.user)

        raise APIException({'detail': 'Bad request'})

    def list(self, request, *args, **kwargs):
        params_dict = self.request.query_params.dict()
        export_format = params_dict.get('file_format', None)

        filename = create_file_name(params_dict=params_dict, user=self.request.user)

        export_data = create_export_data(quiz_votes_list=self.get_queryset(), serializer=QuizResultSerializer,
                                         file_format=export_format)
        response = create_export_response(filename=filename, content=export_data, file_format=export_format)
        return response
