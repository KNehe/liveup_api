from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def validate_dob(value):
    if value > timezone.now().date():
        raise ValidationError(
            _(f"Date should be less than or equal to {timezone.now().date()}")
        )
