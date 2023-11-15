import csv
import io
import json
from decimal import Decimal

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse

from apps.quizzes.quiz_workflow.models import QuizResultModel


class FileExportHelper:
    def __init__(self, quiz_votes_list: QuerySet[QuizResultModel], serializer):
        self.quiz_votes_list = quiz_votes_list
        self.serializer = serializer
        self.header = serializer.Meta.fields

    def to_csv(self) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, delimiter=';', fieldnames=self.header, quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in self.quiz_votes_list.values(*self.header):
            writer.writerow(row)
        content = output.getvalue()
        output.close()
        return content

    def to_json(self) -> str:
        data_list = [row for row in self.quiz_votes_list.values(*self.header)]
        return json.dumps(data_list, indent=4, cls=DecimalEncoder)


class FileExportResponseHelper:
    def __init__(self, filename: str, content: str, file_format: str):
        self.filename = filename
        self.content = content
        self.file_format = file_format

    def get_csv_response(self) -> HttpResponse:
        response = HttpResponse(content=self.content, content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={self.filename}.csv'
        return response

    def get_json_response(self) -> JsonResponse:
        response = JsonResponse(json.loads(self.content), safe=False, json_dumps_params={'indent': 2})
        response['Content-Disposition'] = f'attachment; filename={self.filename}.json'
        return response


class DecimalEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)
