from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import Admission, Patient, Prescription, Referral, User, Ward
from .forms import CustomUserChangeFrom, CustomUserCreationFrom


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationFrom
    form = CustomUserChangeFrom
    model = User
    list_display = [
        "username",
        "email",
        "role",
        "is_staff",
    ]
    fieldsets = (
        (
            "Personal Info",
            {
                "fields": (
                    "username",
                    "email",
                    "password",
                    "phone_number",
                    "first_name",
                    "last_name",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "role",
                    "is_staff",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "phone_number",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Ward)
admin.site.register(Admission)
admin.site.register(Referral)
