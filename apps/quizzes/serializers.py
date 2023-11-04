from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.helper import validate_min_items, validate_correct_answers
from apps.quizzes.models import QuizModel
from apps.quizzes.questions.models import QuestionModel
from apps.quizzes.questions.serlalizers import QuestionSerializer


class QuizSerializer(ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = QuizModel
        fields = ('id', 'title', 'description', 'frequency', 'questions')
        ordering = ('-created_at',)

    @transaction.atomic
    def create(self, validated_data):
        questions = validated_data.pop('questions')
        validate_min_items(questions, {'detail': 'There must be at least two questions'})

        quiz = QuizModel.objects.create(**validated_data)
        self.create_questions(quiz, questions)

        return quiz

    def create_questions(self, quiz, questions):
        question_objects = []
        answer_data_objects = []

        for question_data in questions:
            answers_data = question_data.pop('answers')
            validate_min_items(answers_data, {'detail': 'Each question must have at least two answer options'})
            validate_correct_answers(answers_data)
            answer_data_objects.append(answers_data)

            question_data['quiz'] = quiz
            question_objects.append(QuestionModel(**question_data))
        questions_bulk = QuestionModel.objects.bulk_create(question_objects)
        self.create_answer(questions_bulk, answer_data_objects)

        return questions_bulk

    def create_answer(self, questions, answers):
        answers_list = []
        for i, question in enumerate(questions):
            for answer in answers[i]:
                answer['question'] = question
                answers_list.append(answer)
        answer_objects = [AnswerModel(**answer) for answer in answers_list]
        AnswerModel.objects.bulk_create(answer_objects)
