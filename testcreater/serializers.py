from rest_framework import serializers
from testcreater.models import *


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(QuestionAnswer.objects.all(), many=True)

    class Meta:
        model = Question
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(Question.objects.all(), many=True)
    categories = CategorySerializer(Category.objects.all(), many=True)

    class Meta:
        model = Test
        fields = '__all__'


class CategoryANDTestSerializer(serializers.ModelSerializer):
    tests = TestSerializer(Test.objects.all(), many=True)

    class Meta:
        model = Category
        fields = '__all__'
