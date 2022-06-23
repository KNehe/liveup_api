from django.utils import timezone
from .models import Referral, Patient, Prescription, Admission


def generate_receptionist_stats(request):
    today = timezone.now().date()

    referrals = Referral.objects.all().count()
    referrals_by_user = Referral.objects.filter(created_by=request.user).count()
    referrals_today_by_user = Referral.objects.filter(
        created_by=request.user, created_at__date=today
    ).count()

    patients = Patient.objects.all().count()
    patients_by_user = Patient.objects.filter(created_by=request.user).count()
    patients_today_by_user = Patient.objects.filter(
        created_by=request.user, created_at__date=today
    ).count()

    stats = {
        "referrals": referrals,
        "referrals_by_user": referrals_by_user,
        "referrals_today_by_user": referrals_today_by_user,
        "patients": patients,
        "patients_by_user": patients_by_user,
        "patients_today_by_user": patients_today_by_user,
    }
    return stats


def generate_clinician_stats(request):
    today = timezone.now().date()

    referrals = Referral.objects.all().count()
    referrals_to_user = Referral.objects.filter(doctor=request.user).count()
    referrals_today_to_user = Referral.objects.filter(
        doctor=request.user, created_at__date=today
    ).count()

    admissions = Admission.objects.all().count()
    admissions_by_user = Admission.objects.filter(created_by=request.user).count()
    admissions_today_by_user = Admission.objects.filter(
        created_by=request.user, created_at__date=today
    ).count()

    prescriptions = Prescription.objects.all().count()
    prescriptions_by_user = Prescription.objects.filter(created_by=request.user).count()
    prescriptions_today_by_user = Prescription.objects.filter(
        created_by=request.user, created_at__date=today
    ).count()

    stats = {
        "referrals": referrals,
        "referrals_to_user": referrals_to_user,
        "referrals_today_to_user": referrals_today_to_user,
        "admissions": admissions,
        "admissions_by_user": admissions_by_user,
        "admissions_today_by_user": admissions_today_by_user,
        "prescriptions": prescriptions,
        "prescriptions_by_user": prescriptions_by_user,
        "prescriptions_today_by_user": prescriptions_today_by_user,
    }
    return stats
