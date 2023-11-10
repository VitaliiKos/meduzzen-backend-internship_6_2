from django.db import transaction
from rest_framework.serializers import ModelSerializer

from apps.quizzes.models import AnswerModel, QuestionModel
from apps.quizzes.quiz_workflow.helper import save_quiz_vote_to_redis
from apps.quizzes.quiz_workflow.models import QuizResultModel
from core.enums.quiz_result_enum import QuizResultEnum


class QuizResultSerializer(ModelSerializer):
    class Meta:
        model = QuizResultModel
        fields = '__all__'
        read_only_fields = ('score', 'user', 'company', 'quiz')

    @transaction.atomic
    def create(self, validated_data):
        user_vote = self.initial_data
        quiz = validated_data.pop('quiz')
        user = validated_data.pop('user')
        company = validated_data.pop('company')
        questions = QuestionModel.objects.all().filter(quiz=quiz.id)

        quiz_result = QuizResultModel.objects.filter(user=user, company=company, quiz=quiz).order_by(
            '-updated_at').first()

        last_quiz_result_in_company = QuizResultModel.objects.filter(user=user, company=company).order_by(
            '-created_at').first()

        total_questions = last_quiz_result_in_company.total_question if last_quiz_result_in_company else 0
        total_correct_answers = last_quiz_result_in_company.total_answer if last_quiz_result_in_company else 0

        if quiz_result and quiz_result.status == QuizResultEnum.STARTED.value:
            previous_attempt = quiz_result.attempt
        else:
            previous_attempt = {}

        missing_items = {key: value for key, value in user_vote.items() if key not in previous_attempt}

        for question in questions:
            correct_answers = set(
                AnswerModel.objects.filter(question=question, is_correct=True).values_list('id', flat=True))
            question_id = str(question.id)

            if question_id in missing_items:
                total_questions += 1
                user_selected_answers = set(missing_items[question_id])
                if correct_answers == user_selected_answers:
                    total_correct_answers += 1

        if not quiz_result or quiz_result.status != QuizResultEnum.STARTED.value:
            quiz_result = QuizResultModel.objects.create(
                user=user,
                company=company,
                quiz=quiz,
            )
        quiz_result.total_question = total_questions
        quiz_result.total_answer = total_correct_answers

        quiz_result.attempt.update(missing_items)
        quiz_result.status = QuizResultEnum.STARTED.value if len(
            quiz_result.attempt) < len(questions) else QuizResultEnum.COMPLETED.value
        quiz_result.score = quiz_result.total_answer / total_questions * 100 if total_questions > 0 else 0.0
        quiz_result.save()

        for user_question_id, user_answer_options in quiz_result.attempt.items():
            correct_answer_ids = list(
                AnswerModel.objects.filter(question=user_question_id, is_correct=True).values_list('id', flat=True))

            save_quiz_vote_to_redis(user_id=user.id, company_id=company.id, quiz_id=quiz.id,
                                    question_id=user_question_id, user_answer=user_answer_options,
                                    is_correct=user_answer_options == correct_answer_ids)

        return quiz_result
