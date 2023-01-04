from dataclasses import fields

from rest_framework import serializers
from models import ModeratorUser, RegularUser


class ModeratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeratorUser
        fields = '__all__'


class RegularUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegularUser
        fields = '__all__'
