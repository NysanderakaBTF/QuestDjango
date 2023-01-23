from django.db import models

from usercontrol.models import TestSubject


class QuestionAnswer(models.Model):
    text_ans = models.CharField(verbose_name='Answers', max_length=255)
    explanation = models.TextField(blank=True)
    img_ans = models.ImageField(upload_to='img/%Y/%m/d/ans', blank=True, verbose_name='image', null=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.text_ans + str(self.is_correct)


class Question(models.Model):
    text_ques = models.TextField(verbose_name='Question')
    img_ques = models.ImageField(upload_to='img/%Y/%m/d/ques', blank=True, verbose_name='Image', null=True)
    is_sel_quest = models.BooleanField(default=True)
    test = models.ForeignKey('Test', on_delete=models.CASCADE, related_name='questions')

    score = models.SmallIntegerField(default=1)
    position_in_test = models.IntegerField(default=-1)
    answer_var_n = models.SmallIntegerField(default=1)

    def __str__(self):
        return self.text_ques


class Category(models.Model):
    title = models.CharField(max_length=70, blank=False, unique=True)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    info = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    categories = models.ManyToManyField(Category, blank=True, db_index=True, related_name='category_tests')
    owner = models.ForeignKey(TestSubject, on_delete=models.SET_NULL, null=True)

    n_quest = models.IntegerField()
    is_positional = models.BooleanField(default=False)
    duration = models.DurationField(default="01:00:00")

    def __str__(self):
        return self.title


