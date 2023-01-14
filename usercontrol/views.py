import rest_framework.viewsets
from django.db.models import Q
from django.shortcuts import render
from requests import request
from rest_framework import permissions
from rest_framework.generics import *
from rest_framework.response import Response

from testcreater.models import Test
from testcreater.views import IsTestOwner
from .permission_managers import GroupPermissionManager, UserPermissionManager
from .serializers import *


class UserListAPIView(ListAPIView):
    queryset = TestSubject.objects.all()
    serializer_class = TestSubjectSerializer

class CreateUserAPIView(CreateAPIView):
    serializer_class = TestSubjectSerializer
    queryset = TestSubject.objects.all()

    def post(self, request, *args, **kwargs):
        if 'is_superuser' in request.data.keys():
            if request.data['is_superuser']:
                raise ValidationError("Can't create superuser")
        if 'is_staff' in request.data.keys():
            if request.data['is_staff']:
                raise ValidationError("Can't create moderator")
        request.data['is_active'] = 'True'

        return self.create(request, *args, **kwargs)


class UpdateUserAPIView(UpdateAPIView):
    queryset = TestSubject.objects.all()
    serializer_class = TestSubjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class RetriveUserAPIView(RetrieveAPIView):
    queryset = TestSubject.objects.all()
    serializer_class = TestSubjectSerializer


class DeleteUserAPIView(DestroyAPIView):
    queryset = TestSubject.objects.all()
    serializer_class = TestSubjectSerializer(partial=True)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, UserPermissionManager)


# class CreateGroupAPIView(CreateAPIView):
#     queryset = TestingGroup.objects.all()
#     serializer_class = TestingGroupSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         print(request, *args, **kwargs)
#         request.data['group_owner'] = request.user
#         return super().post(self, request, *args, **kwargs)

class CreateGroupAPIView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data

        data.setdefault('group_owner', request.user.id)
        data['group_members'].append(request.user.id)
        # creatable_gr = TestingGroup(*data)

        new_goup = TestingGroupSerializer(data=data)
        new_goup.is_valid(raise_exception=True)
        new_goup.save()
        return Response(new_goup.data)


class UpdateDeleteGroupAPIView(DestroyAPIView, UpdateAPIView):
    queryset = TestingGroup.objects.all()
    serializer_class = TestingGroupSerializer
    permission_classes = (GroupPermissionManager,)

    def patch(self, request, *args, **kwargs):
        upd_instance = get_object_or_404(TestingGroup,pk=kwargs['pk'])
        if 'group_tests' in request.data.keys():
            for i in request.data['group_tests']:
                test = get_object_or_404(Test, pk=i)
                if not(test.is_public or test.owner == request.user.id or request.user.is_staff) :
                    raise ValidationError(f"Can't get access to '{test.title}' test")

        serializer = TestingGroupSerializer(instance=upd_instance, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)


class ListGroupAPIView(ListAPIView):
    serializer_class = TestingGroupSerializer

    def get_queryset(self):
        return TestingGroup.objects.filter(Q(is_public=True) | Q(group_members__in=[self.request.user.id]))


class RetriveGroupAPIView(RetrieveAPIView):
    queryset = TestingGroup.objects.all()
    serializer_class = TestingGroupSerializer
