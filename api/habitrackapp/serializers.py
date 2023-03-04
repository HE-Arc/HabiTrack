from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template

# User Serializer


class UserSerializer(serializers.HyperlinkedModelSerializer):
    templates = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="template-detail",
        read_only=True)

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "templates"
        ]


# Template Serializer


class TemplateSerializer(serializers.HyperlinkedModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    creator = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="user-detail",
        queryset=User.objects.all(),
        allow_null=True,
        read_only=False,
        source="creator.id"  # This calls the field in the model
    )

    class Meta:
        model = Template
        fields = [
            "url",
            "id",
            "users",
            "name",
            "description",
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "creator"
        ]
