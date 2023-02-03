from rest_framework import serializers
from testcreater import serializers as t_serializer
from testcreater.models import Test
from .models import *


class TestsListSerializer(serializers.ModelSerializer):
    test = t_serializer.TestSerializer(Test.objects.all(), many=True)
    class Meta:
        model = GeneratedTest
        fields = ('test', 'allowed_attempts', 'result', 'id')


class GeneratedTestserialize(serializers.ModelSerializer):
    class Meta:
        model = GeneratedTest
        fields = '__all__'


class GeneratedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedQuestion
        fields = '__all__'


class GeneratedQuestionSerializerNonAbstract(serializers.ModelSerializer):
    class Meta:
        model = GeneratedQuestionNonAbstract
        fields = '__all__'

