from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template

# Simple User Serializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
        ]


# Simple Template Serializer


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

# Adding more fields to the UserSerializer


class ComplexUserSerializer(UserSerializer):
    templates = serializers.HyperlinkedRelatedField(
        many=True, view_name="template-detail",
        read_only=True)

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + [
            "templates",
        ]


# Adding more fields to the TemplateSerializer


class ComplexTemplateSerializer(TemplateSerializer):
    user_object = UserSerializer(source="user", read_only=True)
    template_object = TemplateSerializer(source="template", read_only=True)

    class Meta:
        model = Template
        fields = TemplateSerializer.Meta.fields + [
            "user_object",
            "template_object",
        ]
