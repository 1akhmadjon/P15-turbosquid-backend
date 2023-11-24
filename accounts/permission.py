from rest_framework import permissions

from accounts.models import UserRole


class AdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.get(user=request.user).role
            return user_role.name == 'admin'
        except UserRole.DoesNotExist:
            return False