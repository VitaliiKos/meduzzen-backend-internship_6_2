from model_bakery import baker
from rest_framework.test import APITestCase, override_settings

from apps.companies.employee.models import EmployeeModel
from apps.companies.models import CompanyModel
from apps.quizzes.models import AnswerModel, QuestionModel, QuizModel
from apps.users.models import UserModel
from core.enums.user_enum import UserEnum


@override_settings(CACHES={"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"}})
class BaseTestCase(APITestCase):
    """Base test case for common setup and utility functions."""

    def setUp(self):
        """Set up common data for test cases."""
        self.owner = baker.make(UserModel)
        self.company = baker.make(CompanyModel)
        self.member = baker.make(UserModel)
        self.quiz = baker.make(QuizModel, company=self.company, user=self.owner)

        # Create two questions for the quiz
        self.question1 = baker.make(QuestionModel, quiz=self.quiz, question_text="Question 1 text")
        self.question2 = baker.make(QuestionModel, quiz=self.quiz, question_text="Question 2 text")

        # Create two answer options for each question
        self.answer1_1 = baker.make(AnswerModel, question=self.question1, answer_text="Answer 1 for Question 1",
                                    is_correct=True)
        self.answer1_2 = baker.make(AnswerModel, question=self.question1, answer_text="Answer 2 for Question 1")

        self.answer2_1 = baker.make(AnswerModel, question=self.question2, answer_text="Answer 1 for Question 2",
                                    is_correct=True)
        self.answer2_2 = baker.make(AnswerModel, question=self.question2, answer_text="Answer 2 for Question 2")

        baker.make(EmployeeModel, user=self.owner, company=self.company, role=UserEnum.OWNER.value)
        baker.make(EmployeeModel, user=self.member, company=self.company, role=UserEnum.MEMBER.value)

    def _authentication(self, user):
        """Set the authentication credentials using the provided token."""
        self.client.force_authenticate(user=user)
