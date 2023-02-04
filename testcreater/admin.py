from django.contrib import admin
from .models import *


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text_ques', 'test', 'img_ques')


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('text_ans', 'img_ans', 'is_correct', 'question')
    list_editable = ('is_correct',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'info')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)

@admin.register(TestingGroup)
class TestingGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_owner', 'is_public')
    list_editable = ('is_public',)