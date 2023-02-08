import rest_framework.exceptions
from django.contrib.auth.models import PermissionsMixin
from django.utils.dateparse import parse_duration
from django.db.models import Q, QuerySet
from django.http import HttpResponseRedirect
from rest_framework import viewsets, views, permissions
from rest_framework.exceptions import *
from rest_framework.generics import get_object_or_404, ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.generics import mixins, GenericAPIView
from rest_framework.reverse import reverse

from testcreater.permissions import TestPermissionsChecker, AddTestToGroupPermission
from testcreater.serializers import *
from usercontrol.permissions import GroupPermissionManager


class IsTestOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated


class TestListAPIView(views.APIView):
    def get(self, request):
        if request.user.id:
            available_tests = Test.objects.filter(
                Q(is_public=True) | Q(in_groups__group_members__in=[request.user.id]) | Q(
                    owner_id=request.user.id)).only('title', 'info', 'is_public', 'categories', 'owner').distinct()
        else:
            available_tests = Test.objects.filter(is_public=True).values_list('id', 'title', 'owner')
        return Response(TestSerializer(instance=available_tests, many=True).data)


class TestCreateAPIView(views.APIView):
    permission_classes = (TestPermissionsChecker,)

    def post(self, request):
        #
        # # TODO: избавиться от создания объекта сразу, сделать сначала объект или словарь, а затем его сериалираьтором
        # # создать
        # # поебать, переадресацию на фронте сделать, с сообщением об ошибке, переадресация на Retrive (get + pk)
        # # print(request.data)
        # # Test update should be perfomed as creation of certain questions and addition of them to test
        #
        # test = Test.objects.create(title=request.data['title'],
        #                            is_public=request.data['is_public'],
        #                            info=request.data['info'],
        #                            owner_id=request.user.id,
        #                            duration=parse_duration(request.data['duration']),
        #                            is_positional=request.data['is_positional'],
        #                            n_quest=request.data['n_quest']
        #                            )
        # if 'categories' in request.data.keys():
        #     for i in request.data['categories']:
        #         try:
        #             cat = Category.objects.get(title__iexact=i['title'])
        #         except:
        #             cat = Category.objects.create(title=i['title'])
        #         test.categories.add(cat)
        #
        # questions_data = []
        # if 'questions' in request.data.keys():
        #     for i in request.data['questions']:
        #         if not 'answers' in i.keys():
        #             raise ValidationError(f"Question {i['text_ques']} must contain at least 1 answer")
        #         i.setdefault('test_id', test.pk)
        #         # idk how to make it bulk
        #         new_quesions = CreateQuestionSerializer(data=i)
        #         new_quesions.is_valid(raise_exception=True)
        #         # new_quesions.save()
        #         questions_data.append(Question(**i))
        #     Question.objects.bulk_create(questions_data)
        #
        # if 'in_groups' in request.data.keys():
        #     for i in request.data['in_groups']:
        #         group = get_object_or_404(TestingGroup, pk=i)
        #         if not (request.user.is_staff or request.user.id == group.group_owner.pk):
        #             raise rest_framework.exceptions.PermissionDenied(
        #                 {"detail": f"You can't add a test to {group.name}, because you're not an owner",
        #                  'test': TestSerializer(instance=test).data})
        #         self.check_object_permissions(self.request, group)
        #         group.group_tests.add(test)
        #         group.save()
        #
        # test.save()
        # # make redirect in front-end. After error - use Put method
        # serializer = CreateTestSerializer(data=request.data)
        serializer = CreateTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TestAPIView(views.APIView):
    permission_classes = (TestPermissionsChecker,)

    def get(self, request, pk=None):
        # в сериализаторе нет in groups
        test = get_object_or_404(Test, pk=pk)
        return Response(TestSerializer(instance=test).data)

    def delete(self, request, pk):

        test_obj = get_object_or_404(Test, id=pk)
        try:
            test_obj.delete()
        except:
            raise APIException("Can't delete object", code=500)
        # Возвращаю что осталось, норм же?
        return Response(TestSerializer(Test.objects.filter(owner_id=request.user.id), many=True).data)


class TestUpdateAPIView(views.APIView):
    permission_classes = (GroupPermissionManager, TestPermissionsChecker)

    def put(self, request, pk):
        test_obj = get_object_or_404(Test, pk=pk)
        if 'in_groups' in request.data.keys():
            test_obj.in_groups.clear()
            for i in request.data['in_groups']:
                group = get_object_or_404(TestingGroup, pk=i)
                self.check_object_permissions(request, group)
                test_obj.in_groups.add(group)

        serialized_test = TestUpdateSerializer(data=request.data, instance=test_obj, partial=True)
        serialized_test.is_valid(raise_exception=True)
        serialized_test.save()
        return Response(serialized_test.data)


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


class QuesionListAPIView(ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (TestPermissionsChecker,)
    queryset = Question.objects.all()
    # def get_queryset(self):
    #     return Question.objects.filter(test_id=self.request.data['test_'])



class QuestionAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = (IsTestOwner,)

    def retrieve(self, request, test_pk, pk):
        return Response(QuestionSerializer(Question.objects.get(id=pk)))

    def destroy(self, request, test_pk, pk):

        quest = get_object_or_404(Question, id=pk)

        try:
            quest.delete()
        except:
            raise APIException("Can't delete object", code=500)

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
        return Response(serializer.data)


class CategoryApiView(views.APIView):

    def get(self, request, pk):
        cat = get_object_or_404(Category, id=pk)
        return Response(CategoryANDTestSerializer(instance=cat).data)

    def post(self, request):
        newcat = CategorySerializer(data=request.data)
        newcat.is_valid(raise_exception=True)
        newcat.save()
        return Response(newcat.data)

    def put(self, request, pk):
        cat = get_object_or_404(Category, pk)
        upd_cat = CategorySerializer(data=request.data, instance=cat)
        upd_cat.is_valid(raise_exception=True)
        upd_cat.save()
        return Response(upd_cat.data)

    def delete(self, request, pk):
        cat = get_object_or_404(Category, id=pk)
        try:
            cat.delete()
        except:
            return APIException("Can't delete category", code=500)
        return Response(CategorySerializer(Category.objects.all(), many=True).data)


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
