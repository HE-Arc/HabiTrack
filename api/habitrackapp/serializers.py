from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template, Subscription, Entry
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
        fields = ['id', 'username']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    SerializerMethodField is a read-only field that get its representation from calling a method on the parent serializer class. The method called will be of the form "get_{field_name}", and should take a single argument, which is the object being serialized.
    """
    created_templates = serializers.SerializerMethodField()

    # This function is used to get the templates of the user
    def get_created_templates(self, obj):
        created_templates = Template.objects.filter(creator=obj)
        serializer = TemplateSerializer(
            created_templates, many=True, context=self.context)
        return serializer.data

    class Meta:
        model = User
        fields = SimpleUserSerializer.Meta.fields + [
            "created_templates"
        ]


#############################################################
#                    Template Serializer                    #
#############################################################

class SimpleTemplateSerializer(serializers.HyperlinkedModelSerializer):

    creator = SimpleUserSerializer(
        read_only=True
    )

    class Meta:
        model = Template
        fields = ['id', 'name', 'description', 'option_1',
                  'option_2', 'option_3', 'option_4', 'creator']


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

#############################################################
#                    Subscribe Serializer                   #
#############################################################


class SubscriptionSerializer(serializers.ModelSerializer):
    template = serializers.PrimaryKeyRelatedField(
        queryset=Template.objects.all())

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'template', 'created_at')


#############################################################
#                      Entry Serializer                     #
#############################################################

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('id', 'user', 'template', 'created_at', 'selected_option')
