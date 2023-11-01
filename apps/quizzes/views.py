from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.companies.models import CompanyModel
from apps.quizzes.models import QuizModel
from apps.quizzes.serializers import QuizSerializer
from core.permisions.quizz_permission import QuizPermission


class QuizView(ListCreateAPIView, RetrieveUpdateDestroyAPIView):
    queryset = QuizModel.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticated, QuizPermission)

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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
