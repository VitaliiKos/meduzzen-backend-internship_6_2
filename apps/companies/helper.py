from typing import Optional

from apps.companies.employee.models import EmployeeModel


def get_user_role_in_company(user_id: int, company_id: int) -> Optional[str]:
    """Get the role of a user in a company.

    This function checks if a user has a specific role (e.g., 'Owner') in a company.

    Returns
    -------
        The user's role as a Owner value, or None if the user doesn't exist.
    """
    try:
        member = EmployeeModel.objects.get(user=user_id, company=company_id)
        return member.role
    except EmployeeModel.DoesNotExist:
        return None
