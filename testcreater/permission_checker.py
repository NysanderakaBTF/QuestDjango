from rest_framework import permissions


class TestPermissionsChecker(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if obj.owner == request.user.id or obj.is_public or (request.user.testinggroup_set in obj.in_groups.all()):
                return True
        if request.method in ['DELETE', 'PATCH', 'PUT']:
            return obj.group_owner == request.user or request.user.is_staff
