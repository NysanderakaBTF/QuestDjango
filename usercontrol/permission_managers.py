from rest_framework import permissions


class GroupPermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.is_public or request.user.id in obj.group_members or request.user.is_staff
        return request.user.is_staff or request.user == obj.group_owner


class UserPermissionManager(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return (not request.user.is_authenticated) or request.user.is_staff
        if request.method in ['DELETE', 'PUT', 'PATCH']:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print(request)
        if request.user.id == obj.id or request.user.is_staff:
            return True
        return False
