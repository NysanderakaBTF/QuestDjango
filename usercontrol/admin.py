from django.contrib import admin

from .models import TestSubject
from .TestingGroupModel import TestingGroup


@admin.register(TestSubject)
class TestSubjectAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'school', 'is_active')
    list_editable = ('is_active',)


@admin.register(TestingGroup)
class TestingGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_owner', 'is_public')
    list_editable = ('is_public',)