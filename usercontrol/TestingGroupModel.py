from django.db import models

from testcreater.models import Test


class TestingGroup(models.Model):
    name = models.CharField(max_length=150, blank=False)
    description = models.TextField(blank=True)
    group_owner = models.ForeignKey('TestSubject', on_delete=models.CASCADE)
    group_members = models.ManyToManyField('TestSubject', blank=True, related_name="member_groups")
    group_tests = models.ManyToManyField(Test, blank=True, related_name="in_groups")
    is_public = models.BooleanField(default=True)
