from django.db.models import QuerySet


class QuizManager(QuerySet):
    def get_quiz_by_company_id(self, id):
        return self.filter(company_id=id)
