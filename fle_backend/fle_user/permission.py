from rest_framework.permissions import BasePermission


class IsSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user,'.............admin..........')
        return user.is_authenticated and user.is_superuser


class IsUser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user,'......user........')
        return user.is_authenticated