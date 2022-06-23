from rest_framework import permissions

from main.choices import DOCTOR, NURSE, RECEPTIONIST, STUDENT_CLINICIAN


class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, RECEPTIONIST)


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, DOCTOR)


class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, NURSE)


class IsStudent_Clinician(permissions.BasePermission):
    def has_permission(self, request, view):
        return perform_check(request, STUDENT_CLINICIAN)


def perform_check(request, role):
    if not request.user.is_authenticated:
        return False
    return request.user.role == role
