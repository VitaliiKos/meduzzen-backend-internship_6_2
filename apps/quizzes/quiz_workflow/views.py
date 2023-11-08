from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from apps.quizzes.models import QuizModel
from apps.quizzes.quiz_workflow.models import QuizResultModel
from apps.quizzes.quiz_workflow.serializers import QuizResultSerializer


class QuizWorkflow(ListCreateAPIView):
    queryset = QuizResultModel.objects.all()
    serializer_class = QuizResultSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        quiz_id = self.request.query_params.get('quiz_id')
        quiz = get_object_or_404(QuizModel, pk=quiz_id)
        serializer.save(user=self.request.user, company=quiz.company, quiz=quiz)
