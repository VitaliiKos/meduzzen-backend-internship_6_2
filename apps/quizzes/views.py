from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.models import CompanyModel
from apps.quizzes.models import AnswerModel, QuestionModel, QuizModel
from apps.quizzes.serializers import AnswerSerializer, QuestionSerializer, QuizSerializer
from core.permisions.quizz_permission import QuizPermission


class QuizView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, QuizPermission)

    def get_queryset(self):
        params_dict = self.request.query_params.dict()
        if 'company_id' in params_dict:
            return QuizModel.objects.get_quiz_by_company_id(params_dict['company_id'])
        elif self.kwargs.get('pk'):
            return QuizModel.objects.filter(id=self.kwargs.get('pk'))
        raise APIException({'detail': 'Bad request'})

    def get(self, request, *args, **kwargs):

        if 'pk' in self.kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)

    def perform_create(self, serializer):
        company_id = self.request.query_params.get('company_id')
        company = get_object_or_404(CompanyModel, pk=company_id)
        self.check_object_permissions(self.request, company)
        user = self.request.user
        serializer.save(user=user, company=company)

    def update(self, request, *args, **kwargs):
        quiz = self.get_object()
        serializer = self.get_serializer(quiz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


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
        if question.quiz.questions.count() <= 2:
            return Response({"detail": "There must be at least two questions."}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(question)
        return Response(status=status.HTTP_204_NO_CONTENT)


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

        if not request.data.get('is_correct') and answer.is_correct:
            correct_answers_count = answer.question.answers.filter(is_correct=True).count()
            if correct_answers_count <= 1:
                return Response({"detail": "Each question must have at least one correct answer"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(answer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        answer = self.get_object()
        answers_count = answer.question.answers.count()
        correct_answers_count = answer.question.answers.filter(is_correct=True).count()

        if answers_count <= 2 or answer.is_correct and correct_answers_count < 2:
            return Response({"detail": "Each question must have at least two answer options and one correct answer"},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_destroy(answer)
        return Response(status=status.HTTP_204_NO_CONTENT)
