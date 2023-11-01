from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.answers.serializers import AnswerSerializer
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
        correct_answer_count = AnswerModel.objects.filter(question=question.id, is_correct=True).count()

        if self.request.data.get('is_correct') and correct_answer_count:
            raise serializers.ValidationError({'detail': 'Each question must have exactly one correct answer'})
        serializer.save(question=question)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if self.request.data.get('is_correct'):
            return Response({"detail": "Each question must have exactly one correct answer"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        answers_count = AnswerModel.objects.filter(question=instance.question).count()

        if answers_count <= 2 or instance.is_correct:
            return Response({"detail": "Each question must have at least two answer options and one correct answer"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
