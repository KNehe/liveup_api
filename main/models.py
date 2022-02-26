from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from main.roles import RECEPTIONIST, ROLES

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLES, default=RECEPTIONIST)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self) -> str:
        return self.username


class Patient(models.Model):
    patient_number = models.CharField(max_length=10, blank=True)
    next_of_kin = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    date_of_birth = models.DateField(
                                     validators=[MaxValueValidator(timezone.now().date())])
    age = models.IntegerField(blank=True)
    contacts = models.CharField(max_length=20)
    patient_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='patient_created_by')
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='patient_updated_by')

    def __str__(self) -> str:
        return self.patient_name

    def calculate_age(self):
        today = timezone.now()
        born = self.date_of_birth
        self.age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))

    def generate_patient_number(self):
        self.patient_number = f'P-{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calculate_age()
        self.generate_patient_number()
        


class Prescription(models.Model):
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='patient_prescribed')
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    description = models.TextField(max_length=400)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='presciption_created_by')
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='presciption_updated_by')
    
    def __str__(self) -> str:
        return f'Prescribed by {self.created_by} for {self.patient}'


class Ward(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL, null=True,
                                   related_name='ward_created_by')
    updated_at = models.DateTimeField(null=True, blank=True,)
    updated_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='updated_created_by')


class Admission(models.Model):
    ward = models.ForeignKey(Ward,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='ward_admitted')
    patient = models.ForeignKey(Patient,
                                on_delete=models.CASCADE,
                                related_name='patient_admitted')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True,
                                   related_name='admission_created_by')
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User,
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True,
                                   related_name='admission_updated_by')
