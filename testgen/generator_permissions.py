from rest_framework import permissions

from testcreater.models import Test
from testgen.models import GeneratedTest


class ViewSolveTestPermisson(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj:GeneratedTest):
        test = Test.objects.get(pk = obj.test_id)
        if request.user.is_staff:
            return True
        if test.is_public or any(t_group in request.user.member_groups for t_group in test.in_groups.all()):
            if request.methpd == 'POST':
                return True
            if obj.user_id == request.user.id and test.allowed_attempts>obj.attempt:
                return True
        return False

