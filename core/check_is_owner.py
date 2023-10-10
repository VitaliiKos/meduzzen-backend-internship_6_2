from apps.companies.models import EmployeeModel


def get_user_role_in_company(user_id: int, company_id: int) -> bool:
    """Get the role of a user in a company.

    This function checks if a user has a specific role (e.g., 'Owner') in a company.

    Returns
    -------
        bool: True if the user has the specified role in the company, False otherwise.
    """
    try:
        member = EmployeeModel.objects.get(user=user_id, company=company_id)
        if member.role == 'Owner':
            return True
    except Exception:
        return False
