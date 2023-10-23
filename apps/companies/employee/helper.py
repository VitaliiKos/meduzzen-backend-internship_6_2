from apps.companies.employee.models import EmployeeModel
from core.enums.user_enum import UserEnum


def get_company_employees(company):
    return EmployeeModel.objects.filter(company=company, role__in=[UserEnum.OWNER, UserEnum.MEMBER])
