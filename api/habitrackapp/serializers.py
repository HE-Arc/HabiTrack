from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template
from django.contrib.auth.password_validation import validate_password


###########################################################################
# Serializers
# They define the API representation.
# They are also responsible for validating the data that is deserialized.


#############################################################
#                      User Serializer                      #
#############################################################


class SimpleUserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
        ]


class UserSerializer(serializers.HyperlinkedModelSerializer):

    # Creations

    # SerializerMethodField is a read-only field that get its
    # representation from calling a method on the parent serializer class.
    # The method called will be of the form "get_{field_name}", and should take a single
    # argument, which is the object being serialized.
    created_templates = serializers.SerializerMethodField()

    # This function is used to get the templates of the user
    def get_created_templates(self, obj):
        created_templates = Template.objects.filter(creator=obj)
        serializer = TemplateSerializer(
            created_templates, many=True, context=self.context)
        return serializer.data

    # TODO : fix this

    class Meta:
        model = User
        fields = SimpleUserSerializer.Meta.fields + [
            "created_templates"
        ]


#############################################################
#                      Register Serializer                  #
#############################################################

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        if self.is_valid():
            user = User.objects.create_user(
                validated_data['username'], validated_data['password'])
            return user
        else:
            return serializers.ValidationError(self.errors)

#############################################################
#                    Subscribe Serializer                    #
#############################################################


# class SubscriberSerializer(serializers.HyperlinkedModelSerializer):

#############################################################
#                    Template Serializer                    #
#############################################################


class TemplateSerializer(serializers.HyperlinkedModelSerializer):

    subscribers = UserSerializer(
        many=True,
        read_only=True
    )

    creator = SimpleUserSerializer(
        read_only=True
    )

    class Meta:
        model = Template
        fields = [
            "url",
            "id",
            "name",
            "subscribers",
            "description",
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "creator"
        ]
