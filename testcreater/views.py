from django.contrib.auth.models import PermissionsMixin
from django.db.models import Q
from rest_framework import viewsets, views, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404, ListAPIView
from rest_framework.response import Response
from rest_framework.generics import mixins, GenericAPIView

from testcreater.permission_checker import TestPermissionsChecker
from testcreater.serializers import *
from usercontrol.TestingGroupModel import TestingGroup


class IsTestOwner(permissions.BasePermission):
    def has_permission(self, request, view, obj):
        print(request, view, obj)
        return request.user == obj.owner


class TestListAPIView(views.APIView):
    def get(self, request, *args, **kwargs):
        if request.user.id:
            available_tests = Test.objects.filter(
                Q(is_public=True) | Q(in_groups__group_members__in=[request.user.id])).values_list('id', 'title', 'owner')
        else:
            available_tests = Test.objects.filter(Q(is_public=True)).values_list('id', 'title', 'owner')
        # available_tests1 = available_tests | [i.group_tests.all().values_list('id', 'title', 'owner') for
        # i in request.user.testinggroup_set.all()]
        #  return Response(TestSerializer(instance=available_tests).data)
        return Response(available_tests.values())


class TestAPIView(views.APIView):
    permission_classes = (TestPermissionsChecker,)

    def get(self, request, pk=None):
        if not pk:
            test = Test.objects.all().only('title', 'info', 'is_public', 'categories', 'owner')
            # add values_list('id', 'title', 'owner') for prod or mongo
            return Response(TestSerializer(instance=test).data)
        test = get_object_or_404(Test, pk=pk)
        return Response(TestSerializer(instance=test).data)

    def post(self, request):


        #TODO: избавиться от создания объекта сразу, сделать сначала объект или словарь, а затем его сериалираьтором
        #создать
        print(request.data)

        test = Test.objects.create(title=request.data['title'],
                                   is_public=request.data['is_public'],
                                   info=request.data['info'],
                                   owner_id=request.user.id,
                                   )
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
                question = Question.objects.create(text_ques=i['text_ques'],
                                                   img_ques=i['img_ques'],
                                                   test_id=test.pk)
                for j in i['answers']:
                    new_data = j
                    new_data.setdefault('question', question.pk)
                    ans = QuestionAnswerSerializer(data=new_data)
                    # ans.fields['question'] = question.pk
                    ans.is_valid(raise_exception=True)
                    ans.save()
        else:
            raise ValidationError("You must provide at least 1 question for test")
        if 'in_groups' in request.data.keys():
            for i in request.data['in_groups']:
                print(i)
                group = TestingGroup.objects.get(pk=i)
                if request.user.is_staff == False or request.user.id != group.group_owner.pk:
                    raise ValidationError(f"You can't add a test to {group.name}, because you're not an owner")
                else:
                    group.group_tests.add(test)
                    group.save()
        test.save()
        return Response(TestSerializer(test).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "PUT is not allowe"})

        try:
            test_obj = Test.objects.get(pk=pk)
        except:
            return Response({"error": "404 Test not found"})

        serialized_test = TestSerializer(data=request.data, instance=test_obj)
        serialized_test.is_valid(raise_exception=True)
        serialized_test.save()
        return Response({"test": serialized_test.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "PUT is not allowe"})

        try:
            test_obj = Test.objects.get(pk=pk)
        except:
            return Response({"error": "404 Test not found"})

        try:
            test_obj.delete()
        except:
            return Response({"error": "Deletion error"})


class QuestionAPIView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      GenericAPIView
                      ):
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('quest_pk', None)
        test_pk = kwargs.get('test_pk', None)

        if test_pk and pk:
            return Response({"question": QuestionSerializer(Question.objects.get(pk=pk)).data})
        if not pk:
            return Response({"question": QuestionSerializer(Question.objects.all()).data})


class QuestionAnswerAPIView(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()
    permission_classes = (IsTestOwner,)


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


class CategoryListAPIView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
