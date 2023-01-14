from dataclasses import fields
from pyexpat import model

from rest_framework import serializers

from usercontrol.TestingGroupModel import TestingGroup
from usercontrol.models import TestSubject


class TestingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestingGroup
        fields = ('id', 'name', 'description', 'group_owner', 'group_members', 'group_tests', 'is_public')


class TestSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestSubject
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = TestSubject(**validated_data)
        user.set_password(password)
        user.save()
        return user
