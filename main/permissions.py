from rest_framework import permissions

from main.choices import DOCTOR, NURSE,\
    RECEPTIONIST, STUDENT_CLINICIAN


class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RECEPTIONIST


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == DOCTOR


class IsNurse(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == NURSE


class IsStudent_Clinician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == STUDENT_CLINICIAN
