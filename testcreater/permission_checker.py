from rest_framework import permissions

class TestPermissionsChecker(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            if obj.owner == request.user.id or obj.is_public or (request.user.testinggroup_set in  obj.in_groups.all()):
                return True
