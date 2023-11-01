from django.db import transaction


@transaction.atomic
def update_employee(employee, new_status, invitation, role=None):
    """Update the employee's role and the invitation status."""
    employee.role = role
    invitation.status = new_status
    employee.save()
    invitation.save()
    return invitation
