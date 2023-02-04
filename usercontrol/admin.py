from django.contrib import admin

from .models import TestSubject


@admin.register(TestSubject)
class TestSubjectAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'school', 'is_active')
    list_editable = ('is_active',)