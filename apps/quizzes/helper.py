from rest_framework.exceptions import ValidationError


def validate_min_items(items, error_message):
    if len(items) < 2:
        raise ValidationError({'detail': error_message})


def validate_correct_answers(answers):
    correct_count = sum(1 for answer in answers if answer.get('is_correct'))
    if not correct_count:
        raise ValidationError({'detail': 'Each question must have at least one correct answer.'})

