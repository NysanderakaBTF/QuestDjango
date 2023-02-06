from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import BaseSerializer

from testcreater.models import *

class TestingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingGroup
        fields = ('id', 'name', 'description', 'group_owner', 'group_members', 'group_tests', 'is_public')

class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class AnswerVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ('text_ans', 'img_ans', 'question', 'id')


class QuestionSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(QuestionAnswer.objects.all(), many=True)

    class Meta:
        model = Question
        fields = '__all__'


class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('text_ques', 'img_ques', 'is_sel_quest', 'test_id', 'score', 'position_in_test', 'answer_var_n')

    def create(self, validated_data):
        self.is_valid(raise_exception=True)
        if 'img_ques' not in validated_data.keys():
            validated_data.setdefault('img_ques', None)

        if not 'answers' in self.initial_data.keys():
            raise ValidationError(f"Question {validated_data['text_ques']} must contain at least 1 answer")

        data = validated_data
        data.setdefault('test_id', self.initial_data['test'])
        data.setdefault('test', self.initial_data['test'])

        question = Question.objects.create(**data)
        answers = []
        for j in self.initial_data['answers']:
            new_data = j
            new_data.setdefault('question_id', question.pk)
            answers.append(QuestionAnswer(**new_data))
            # ans = QuestionAnswerSerializer(data=new_data)
            # ans.is_valid(raise_exception=True)
            # answers.append(ans)

        # answers_serializer = QuestionAnswerSerializer(data=answers, many=True)
        # answers_serializer.is_valid(raise_exception=True)
        # answers_serializer.save()
        QuestionAnswer.objects.bulk_create(answers)
        # QuestionAnswer.objects.bulk_create(answers)

        return question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


# TODO:change to serializer for list
class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(Question.objects.all(), many=True)
    categories = CategorySerializer(Category.objects.all(), many=True)
    in_groups = TestingGroupSerializer(TestingGroup.objects.all(), many=True)

    class Meta:
        model = Test
        fields = '__all__'


class CreateTestSerializer(serializers.ModelSerializer):
    questions = CreateQuestionSerializer(many=True)
    categories = CategorySerializer(many=True)
    in_groups = TestingGroupSerializer(many=True)
    class Meta:
        model = Test
        fields = '__all__'

class TestUpdateSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(Category.objects.all(), many=True)
    questions = CreateQuestionSerializer(Question.objects.all(), many=True)

    class Meta:
        model = Test
        fields = ('id', 'categories', 'title', 'info', 'is_public', 'owner', 'n_quest', 'is_positional')

    # def update(self, instance: Test, validated_data):
    #     self.is_valid(raise_exception=True)
    #
    #     for key, val in validated_data.items():
    #         if key == 'questions':
    #             # print(instance.questions.all().values())
    #             for i in self.initial_data['questions']:
    #                 i.setdefault('test', instance.pk)
    #                 # print(i)
    #
    #                 try:
    #                     question_ = instance.questions.get(text_ques__iexact=i['text_ques'])
    #                     print(question_, '1!!!!!')
    #                     question_ser = QuestionSerializer(instance=question_, data=i, partial=True)
    #                     question_ser.is_valid(raise_exception=True)
    #                     question_ser.update()
    #                 except:
    #                     new_ques = CreateQuestionSerializer(data=i)
    #                     new_ques.is_valid(raise_exception=True)
    #                     new_ques.save()
    #
    #
    #     return instance


class TestListSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(Category.objects.all(), many=True)
    in_groups = TestingGroupSerializer(TestingGroup.objects.all(), many=True)

    class Meta:
        model = Test
        fields = ('pk', 'title', 'owner', 'in_groups', 'categories')


class CategoryANDTestSerializer(serializers.ModelSerializer):
    tests = TestSerializer(Test.objects.all(), many=True)

    class Meta:
        model = Category
        fields = ('id', 'title', 'tests')



