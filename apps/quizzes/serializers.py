from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.quizzes.helper import validate_correct_answers, validate_min_items
from apps.quizzes.models import AnswerModel, QuestionModel, QuizModel


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = AnswerModel
        fields = ('id', 'answer_text', 'is_correct')


class QuestionSerializer(ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuestionModel
        fields = ('id', 'question_text', 'answers')

    @transaction.atomic
    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        validate_min_items(answers_data, {'detail': 'Each question must have at least two answer options'})
        validate_correct_answers(answers_data)

        question = QuestionModel.objects.create(**validated_data)
        answer_objects = [AnswerModel(question=question, **answer) for answer in answers_data]

        AnswerModel.objects.bulk_create(answer_objects)

        return question


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
