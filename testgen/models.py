from django import forms
from djongo import models


class GeneratedQuestion(models.Model):
    user_score = models.IntegerField(blank=True)
    question_id = models.IntegerField()
    answers = models.JSONField(blank=True)
    given_answer = models.JSONField(blank=True)

    class Meta:
        abstract = True


class GeneratedQuestionNonAbstract(models.Model):
    user_score = models.IntegerField(blank=True)
    question_id = models.IntegerField()
    answers = models.JSONField(default=list())
    given_answer = models.JSONField(blank=True)


class GeneratedQuestionForm(forms.ModelForm):
    class Meta:
        model = GeneratedQuestion
        fields = '__all__'


class GeneratedTest(models.Model):
    user_id = models.IntegerField(blank=True, db_index=True)
    test_id = models.IntegerField(db_index=True)
    _id = models.UUIDField()
    questions = models.ArrayField(model_container=GeneratedQuestion,
                                  model_form_class=GeneratedQuestionForm)
    result = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)