from unittest.util import _MAX_LENGTH
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Template


###########################################################################
# Serializers
# They define the API representation.
# They are also responsible for validating the data that is deserialized.


#############################################################
#                      User Serializer                      #
#############################################################


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

    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "created_templates"
        ]


#############################################################
#                    Template Serializer                    #
#############################################################


class TemplateSerializer(serializers.HyperlinkedModelSerializer):
    creator = serializers.HyperlinkedRelatedField(
        many=False,
        view_name="user-detail",
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
        default=serializers.CurrentUserDefault()
    )

    # SerializerMethodField is a read-only field that get its
    # representation from calling a method on the parent serializer class.
    # The method called will be of the form "get_{field_name}", and should take a single
    # argument, which is the object being serialized.
    creator_username = serializers.SerializerMethodField()

    # This function is used to get the username of the creator
    def get_creator_username(self, obj):
        creator = obj.creator
        if creator is not None:
            return creator.username
        return None

    # Subscriber names
    subscriber_usernames = serializers.SerializerMethodField()

    def get_subscriber_usernames(self, obj):
        subscribers = obj.subscribers
        subscriber_usernames = []
        for subscriber in subscribers.all():
            if subscriber is not None:
                subscriber_usernames.append(subscriber.username)
            else:
                subscriber_usernames.append(None)
        return subscriber_usernames

    class Meta:
        model = Template
        fields = [
            "url",
            "id",
            "subscribers",
            "subscriber_usernames",
            "name",
            "description",
            "option_1",
            "option_2",
            "option_3",
            "option_4",
            "creator",
            "creator_username"
        ]
