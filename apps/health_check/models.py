from django.db import models


class TimeStampedModel(models.Model):
    """An abstract base model for adding timestamp fields.

    This model includes `created_at` and `updated_at` fields for tracking the creation and
    last modification timestamps.
    """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
