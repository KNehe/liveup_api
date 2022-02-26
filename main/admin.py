from django.contrib import admin

from main.models import Admission, Patient, Prescription, User, Ward

admin.site.register(User)
admin.site.register(Patient)
admin.site.register(Prescription)
admin.site.register(Ward)
admin.site.register(Admission)
