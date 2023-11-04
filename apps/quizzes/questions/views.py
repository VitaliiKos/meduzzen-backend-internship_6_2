from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.quizzes.helper import question_destroy_permission
from apps.quizzes.models import QuizModel
from apps.quizzes.questions.models import QuestionModel
from apps.quizzes.questions.serlalizers import QuestionSerializer
from core.permisions.quizz_permission import QuizPermission


class QuizQuestionView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated, QuizPermission)

    def perform_create(self, serializer):
        quiz_id = self.request.query_params.get('quiz_id')
        quiz = get_object_or_404(QuizModel, pk=quiz_id)
        self.check_object_permissions(self.request, quiz)

        serializer.save(quiz=quiz)

    def destroy(self, request, *args, **kwargs):
        question = self.get_object()
        question_destroy_permission(question)

        self.perform_destroy(question)
        return Response(status=status.HTTP_204_NO_CONTENT)
