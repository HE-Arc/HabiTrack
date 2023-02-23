from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
        ]
        

class TemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Template
        fields = [
            "url",
            "id",
            "name",
            "description",
            "option_1",
            "option_2", 
            "option_3", 
            "option_4",
        ]

