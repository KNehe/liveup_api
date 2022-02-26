from rest_framework import permissions

from main.roles import DOCTOR, RECEPTIONIST

class IsReceptionist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == RECEPTIONIST

class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == DOCTOR
