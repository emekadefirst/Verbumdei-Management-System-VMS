from .models import CustomUser
from rest_framework.permissions import BasePermission


class IsHeadTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == CustomUser.ROLE.HEAD_TEACHER and
            request.user.has_perm('customuser.view_student_reports')
        )

class IsParent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == CustomUser.ROLE.PARENT and
            request.user.has_perm('customuser.manage_student')
        )

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == CustomUser.ROLE.TEACHER and
            request.user.has_perm('customuser.manage_staff')
        )

class IsAccountant(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role == CustomUser.ROLE.ACCOUNTANT and
            request.user.has_perm('customuser.manage_inventories')
        )


class IsManager(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.ROLE.MANAGER
            and request.user.has_perm("customuser.manage_inventory")
        )
