from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import BaseSerializer

from testcreater.models import *
from usercontrol.serializers import TestingGroupSerializer
from usercontrol.TestingGroupModel import TestingGroup


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
        fields = ('text_ques', 'img_ques', 'is_sel_quest', 'test', 'score', 'position_in_test', 'answer_var_n')

    def create(self, validated_data):
        self.is_valid(raise_exception=True)
        if 'img_ques' not in validated_data.keys():
            validated_data.setdefault('img_ques', None)
        # print(self.validated_data)
        if not 'answers' in self.initial_data.keys():
            raise ValidationError(f"Question {validated_data['text_ques']} must contain at least 1 answer")
        question = Question.objects.create(text_ques=validated_data['text_ques'],
                                           img_ques=validated_data['img_ques'],
                                           test_id=self.initial_data['test'],
                                           answer_var_n=validated_data['answer_var_n'],
                                           position_in_test=validated_data['position_in_test'],
                                           score=validated_data['score'],
                                           is_sel_quest=validated_data['is_sel_quest'])
        for j in self.initial_data['answers']:
            new_data = j
            new_data.setdefault('question', question.pk)
            ans = QuestionAnswerSerializer(data=new_data)
            # ans.fields['question'] = question.pk
            ans.is_valid(raise_exception=True)
            ans.save()
        return question


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# TODO:change to serializer for list
class TestSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(Question.objects.all(), many=True)
    categories = CategorySerializer(Category.objects.all(), many=True)
    in_groups = TestingGroupSerializer(TestingGroup.objects.all(), many=True)

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
        fields = '__all__'
