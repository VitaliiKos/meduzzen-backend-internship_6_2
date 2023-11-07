from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.tests.base_test import BaseTestCase
from core.enums.quiz_result_enum import QuizResultEnum

UserModel = get_user_model()


class QuizWorkflowTest(BaseTestCase):
    def setUp(self):
        super().setUp()

        self._authentication(self.member)

    def test_all_correct_answers(self):
        """Test when all answers are correct in the quiz workflow."""
        query_params = {"quiz_id": self.quiz.id}
        url = reverse('quiz_workflow')
        data = {
            str(self.question1.id): [self.answer1_1.id],
            str(self.question2.id): [self.answer2_1.id]
        }
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]),
                                    data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_question'], 2)
        self.assertEqual(response.data['total_answer'], 2)
        self.assertEqual(float(response.data['score']), float(100))
        self.assertEqual(response.data['status'], QuizResultEnum.COMPLETED.value)

    def test_one_correct_answer(self):
        """Test when one answer is correct in the quiz workflow."""
        query_params = {"quiz_id": self.quiz.id}
        url = reverse('quiz_workflow')
        data = {
            str(self.question1.id): [self.answer1_1.id],
            str(self.question2.id): [self.answer2_2.id]
        }
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]),
                                    data=data, format='json')
        user_system_rating = QuizResultModel.get_system_rating(self.member.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_question'], 2)
        self.assertEqual(response.data['total_answer'], 1)
        self.assertEqual(float(response.data['score']), float(50))
        self.assertEqual(response.data['status'], QuizResultEnum.COMPLETED.value)
        self.assertEqual(float(user_system_rating), float(50))

    def test_answer_for_one_question(self):
        """Test when an answer is provided for only one question in the quiz workflow."""
        query_params = {"quiz_id": self.quiz.id}
        url = reverse('quiz_workflow')
        data = {
            str(self.question1.id): [self.answer1_1.id],
        }
        response = self.client.post(url + '?' + '&'.join([f"{key}={value}" for key, value in query_params.items()]),
                                    data=data, format='json')
        user_system_rating = QuizResultModel.get_system_rating(self.member.id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_question'], 1)
        self.assertEqual(response.data['total_answer'], 1)
        self.assertEqual(float(response.data['score']), float(100))
        self.assertEqual(response.data['status'], QuizResultEnum.STARTED.value)
        self.assertEqual(float(user_system_rating), float(100))
