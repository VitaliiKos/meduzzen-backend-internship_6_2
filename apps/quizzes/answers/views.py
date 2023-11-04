from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.answers.serializers import AnswerSerializer
from apps.quizzes.helper import answer_update_permission, answer_destroy_permission
from apps.quizzes.questions.models import QuestionModel
from core.permisions.quizz_permission import QuizPermission


class QuizAnswerView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = AnswerModel.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated, QuizPermission)

    def perform_create(self, serializer):
        question_id = self.request.query_params.get('question_id')
        question = get_object_or_404(QuestionModel, id=question_id)
        self.check_object_permissions(self.request, question)
        serializer.save(question=question)

    def update(self, request, *args, **kwargs):
        answer = self.get_object()
        answer_update_permission(request, answer)
        serializer = self.get_serializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        answer = self.get_object()
        answer_destroy_permission(answer)

        self.perform_destroy(answer)
        return Response(status=status.HTTP_204_NO_CONTENT)
