import rest_framework.generics
from django.shortcuts import render, redirect
from rest_framework import viewsets, views
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.generics import mixins, GenericAPIView

from testcreater.models import *
from testcreater.serializers import *


class TestListAPIView(rest_framework.generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class TestAPIView(views.APIView):
    def get(self, request, pk=None):
        if not pk:
            test = Test.objects.all()
            return Response(test)
        test = get_object_or_404(Test, pk=pk)

        questions = [ {QuestionSerializer(instance=q).data:[QuestionAnswerSerializer(instance=a).data]}
                      for q in test.question_set.all()
                        for a in q.questionanswer_set.all()]
        return Response({"test":TestSerializer(instance=test).data, "questions":questions})

    def post(self, request):
        post_new = TestSerializer(data=request.data)
        post_new.is_valid(raise_exception=True)
        post_new.save()
        return Response({"test": post_new.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "PUT is not allowe"})

        try:
            test_obj = Test.objects.get(pk=pk)
        except:
            return Response({"error": "404 Test not found"})

        serialized_test = TestSerializer(data=request.data, instance= test_obj)
        serialized_test.is_valid(raise_exception=True)
        serialized_test.save()
        return Response({"test":serialized_test.data})

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
            return Response({"error":"Deletion error"})



class QuestionAPIView(mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.CreateModelMixin,
                      GenericAPIView
                      ):
    serializer_class = QuestionSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        q = Question.objects.get(pk=1)
        test_id = kwargs.get('test_id', None)
        if not pk:
            return Response({"question":QuestionSerializer(Question.objects.all()).data})







