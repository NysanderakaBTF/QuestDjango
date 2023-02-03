import rest_framework.exceptions
from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import viewsets, views, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.generics import mixins, GenericAPIView
from rest_framework.reverse import reverse

from testcreater.permission_checker import TestPermissionsChecker
from testcreater.serializers import *
from usercontrol.TestingGroupModel import TestingGroup
from usercontrol.permission_managers import GroupPermissionManager


class IsTestOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class TestListAPIView(views.APIView):
    def get(self, request):
        if request.user.id:
            available_tests = Test.objects.filter(
                Q(is_public=True) | Q(in_groups__group_members__in=[request.user.id])).values_list('id', 'title',
                                                                                                   'owner')
        else:
            available_tests = Test.objects.filter(Q(is_public=True)).values_list('id', 'title', 'owner')
        # available_tests1 = available_tests | [i.group_tests.all().values_list('id', 'title', 'owner') for
        # i in request.user.testinggroup_set.all()]
        #  return Response(TestSerializer(instance=available_tests).data)
        return Response(available_tests.values())


class TestAPIView(views.APIView):
    permission_classes = (TestPermissionsChecker,)

    def get(self, request, pk=None):
        # в сериализаторе нет in groups
        if not pk:
            test = Test.objects.filter(Q(is_public=True) | Q(in_groups__group_members__in=[request.user.id]) | Q(
                owner_id=request.user.id)).only('title', 'info', 'is_public', 'categories', 'owner').distinct()
            return Response(TestListSerializer(instance=test, many=True).data)
        test = get_object_or_404(Test, pk=pk)
        return Response(TestSerializer(instance=test).data)

    def post(self, request):

        # TODO: избавиться от создания объекта сразу, сделать сначала объект или словарь, а затем его сериалираьтором
        # создать
        # поебать, переадресацию на фронте сделать, с сообщением об ошибке, переадресация на Retrive (get + pk)
        print(request.data)

        #  if any(((request.user.is_staff is False) or request.user.id != group.group_owner.pk) for group in request.data['in_groups']):

        test = Test.objects.create(title=request.data['title'],
                                   is_public=request.data['is_public'],
                                   info=request.data['info'],
                                   owner_id=request.user.id,
                                   duration=request.data['duration'],
                                   is_positional=request.data['is_positional'],
                                   n_quest=request.data['n_quest']
                                   )
        if 'categories' in request.data.keys():
            for i in request.data['categories']:
                try:
                    cat = Category.objects.get(title__iexact=i['title'])
                except:
                    cat = Category.objects.create(title=i['title'])
                # cat.category_tests.add(test)
                test.categories.add(cat)
        # cat.save()
        if 'questions' in request.data.keys():
            for i in request.data['questions']:
                if not 'answers' in i.keys():
                    raise ValidationError(f"Question {i['text_ques']} must contain at least 1 answer")
                i.setdefault('test', test.pk)
                new_ques = CreateQuestionSerializer(data=i)
                new_ques.is_valid(raise_exception=True)
                new_ques.save()
        if 'in_groups' in request.data.keys():
            for i in request.data['in_groups']:
                print(i)
                group = get_object_or_404(TestingGroup, pk=i)
                if not (request.user.is_staff or request.user.id == group.group_owner.pk):
                    raise rest_framework.exceptions.PermissionDenied(
                        {"detail": f"You can't add a test to {group.name}, because you're not an owner",
                         'test': TestSerializer(instance=test).data})
                else:
                    group.group_tests.add(test)
                    group.save()
        test.save()
        # make redirect in front-end. After error - use Put method
        return Response(TestSerializer(test).data)

    def delete(self, request, pk):
        # print(request)
        if not pk:
            return Response({"error": "DELETE is not allowed"})

        try:
            test_obj = Test.objects.get(pk=pk)
        except:
            return Response({"error": "404 Test not found"}, status=404)

        try:
            test_obj.delete()
        except:
            return Response({"error": "Deletion error"})
        return Response(TestSerializer(Test.objects.filter(owner_id=request.user.id), many=True).data)


class TestUpdateAPIView(views.APIView):
    permission_classes = (GroupPermissionManager, TestPermissionsChecker)

    def patch(self, request, pk):
        if not pk:
            return Response({"error": "PATCH is not allowed"}, status=400)
        test_obj = get_object_or_404(Test, pk=pk)
        if 'in_groups' in request.data.keys():
            test_obj.in_groups.clear()
            for i in request.data['in_groups']:
                group = get_object_or_404(TestingGroup, pk=i)
                self.check_object_permissions(request, group)
                test_obj.in_groups.add(group)

        serialized_test = TestUpdateSerializer(data=request.data, instance=test_obj, partial=True)
        serialized_test.is_valid(raise_exception=True)
        test_obj.save()
        # serialized_test = TestSerializer(data=request.data, instance=test_obj, partial=True)
        #
        # serialized_test.is_valid(raise_exception=True)
        serialized_test.save()
        return Response({"test": serialized_test.data})


class MyTestListAPIView(ListAPIView):
    serializer_class = TestSerializer
    permission_classes = (TestPermissionsChecker,)

    def get_queryset(self):
        return Test.objects.filter(owner_id=self.request.user.id)


# !!!!!!!!!!!!!!!!!!!!


class CreateQuestionAPIView(CreateAPIView):
    serializer_class = CreateQuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (TestPermissionsChecker, GroupPermissionManager)

    def create(self, request, pk):
        data = request.data
        data.setdefault('test', pk)
        serializer = CreateQuestionSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class QuestionAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsTestOwner,)

    # TODO:короче, обновлять вопросы не через тест, а через апи ворпосов.!!!

    def retrieve(self, request, test_pk=None, pk=None):
        if test_pk and pk:
            return Response({"question": QuestionSerializer(Question.objects.get(pk=pk)).data})
        if not pk:
            return Response({"question": QuestionSerializer(Question.objects.all()).data})

    def destroy(self, request, test_pk, pk):
        if not pk:
            return Response({"error": "DELETE is not allowed"})

        try:
            quest = Question.objects.get(pk=pk)
        except:
            return Response({"error": "404 question not found"}, status=404)

        try:
            quest.delete()
        except:
            return Response({"error": "Deletion error"})
        return Response(QuestionSerializer(Question.objects.filter(test_id=test_pk), many=True).data)


class QuestionAnswerAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()
    permission_classes = (IsTestOwner,)

    def create(self, request, test_pk, quest_pk):
        data = request.data
        data.setdefault('question', quest_pk)
        serializer = QuestionAnswerSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(QuestionSerializer(Question.objects.get(id=quest_pk)).data)


class CategoryApiView(views.APIView):

    def get(self, request, pk=None):
        if not pk:
            cats = Category.objects.all()
            return Response(CategorySerializer(instance=cats, many=True).data)
        cat = get_object_or_404(Category, id=request.data['pk'])
        return Response({"category": cat, "tests": CategoryANDTestSerializer(instance=cat, many=True).data})
        # return Response({"category": cat})

    def post(self, request):
        newcat = CategorySerializer(data=request.data)
        newcat.is_valid(raise_exception=True)
        newcat.save()
        return Response(CategorySerializer(instance=newcat).data)

    def put(self, request, pk):
        cat = get_object_or_404(Category, pk)
        upd_cat = CategorySerializer(data=request.data, instance=cat)
        upd_cat.is_valid(raise_exception=True)
        upd_cat.save()
        return Response(CategoryANDTestSerializer(instance=upd_cat).data)

    def delete(self, request, pk):
        if not pk:
            return Response({"error": "DELETE is not allowed"})

        try:
            cat = Category.objects.get(pk=pk)
        except:
            return Response({"error": "404 Caegory not found"}, status=404)

        try:
            cat.delete()
        except:
            return Response({"error": "Deletion error"})
        return Response(CategorySerializer(Category.objects.all(), many=True).data)


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
