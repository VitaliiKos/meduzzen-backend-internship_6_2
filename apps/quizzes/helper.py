from rest_framework.exceptions import ValidationError

from apps.quizzes.answers.models import AnswerModel
from apps.quizzes.questions.models import QuestionModel


def validate_min_items(items, error_message):
    if len(items) < 2:
        raise ValidationError({'detail': error_message})


def validate_correct_answers(answers):
    correct_count = sum(1 for answer in answers if answer.get('is_correct'))
    if not correct_count:
        raise ValidationError({'detail': 'Each question must have at least one correct answer.'})


# def create_answer(questions, answers):
#     answers_list = []
#     for i, question in enumerate(questions):
#         for answer in answers[i]:
#             answer['question'] = question
#             answers_list.append(answer)
#     answer_objects = [AnswerModel(**answer) for answer in answers_list]
#     AnswerModel.objects.bulk_create(answer_objects)


# def create_questions(quiz, questions):
#     question_objects = []
#     answer_data_objects = []
#
#     for question_data in questions:
#         answers_data = question_data.pop('answers')
#         validate_min_items(answers_data, {'detail': 'Each question must have at least two answer options'})
#         validate_correct_answers(answers_data)
#         answer_data_objects.append(answers_data)
#
#         question_data['quiz'] = quiz
#         question_objects.append(QuestionModel(**question_data))
#     questions_bulk = QuestionModel.objects.bulk_create(question_objects)
#     create_answer(questions_bulk, answer_data_objects)

    # return questions_bulk


def answer_update_permission(request, instance):
    if not request.data.get('is_correct') and instance.is_correct:
        correct_answers_count = instance.answers.filter(is_correct=True).count()
        if correct_answers_count <= 1:
            raise ValidationError({"detail": "Each question must have at least one correct answer"})


def question_destroy_permission(question):
    if question.quiz.questions.count() <= 2:
        raise ValidationError({"detail": "There must be at least two questions."})


def answer_destroy_permission(answer):
    answers_count = answer.question.answers.count()
    correct_answers_count = answer.question.answers.filter(is_correct=True).count()

    if answers_count <= 2 or answer.is_correct and correct_answers_count < 2:
        raise ValidationError({"detail": "Each question must have at least two answer options and one correct answer"})
