# Django
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Custom models
from ..models import Subscription
from ..models import Template

# Serializers
from ..serializers import SubscriptionSerializer
from ..serializers import SimpleTemplateSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    """
    This file defines the SubscriptionViewSet class which contains several actions for managing user subscriptions to templates.

    Functions:

        get_subscriptions(self, request, username)
            Returns a list of template data that a given user is subscribed to.

        count_by_user(self, request, username)
            Returns the number of subscriptions a given user has.

        is_subscribed(self, request, username, template_id)
            Determines if a given user is subscribed to a given template.

        subscribe(self, request, username, template_id)
            Subscribes a given user to a given template.

        unsubscribe(self, request, username, template_id)
            Unsubscribes a given user from a given template.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @ action(detail=False, methods=['get'], url_path=r"user/(?P<username>[\w.@+-]+)")
    def get_subscriptions(self, request, username=None):
        """
        Returns a list of template data that a given user is subscribed to.

        Args:
        - request: the request object
        - username: the username of the user to get the subscriptions for

        Returns:
        - A JSON response containing a list of template data that the given user is subscribed to.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'})

        if not user.is_authenticated:
            return JsonResponse({'error': 'User not logged in'})

        subscriptions = Subscription.objects.filter(user=user)
        subscription_data = []
        for subscription in subscriptions:
            template_data = SimpleTemplateSerializer(
                subscription.template).data
            subscription_data.append(template_data)

        return JsonResponse({
            'success': True,
            'subscriptions': subscription_data,
        })

    @ action(detail=False, methods=['get'], url_path=r"count/(?P<username>[\w.@+-]+)")
    def count_by_user(self, request, username):
        """
        Returns the number of subscriptions a given user has.

        Args:
        - request: the request object
        - username: the username of the user to get the count for

        Returns:
        - A JSON response containing the count of subscriptions the given user has.
        """
        user = get_object_or_404(User, username=username)
        count = self.get_queryset().filter(user=user).count()
        return Response({'success': True,
                         'count': count})

    # Is a username subscribed to a template?
    @ action(detail=False, methods=['get'], url_path=r"(?P<username>[\w.@+-]+)/subscribed/(?P<template_id>[\w.@+-]+)")
    def is_subscribed(self, request, username, template_id):
        """
        Determines if a given user is subscribed to a given template.

        Args:
        - request: the request object
        - username: the username of the user to check subscription for
        - template_id: the id of the template to check subscription for

        Returns:
        - A JSON response indicating if the given user is subscribed to the given template.
        """
        user = get_object_or_404(User, username=username)
        template = get_object_or_404(Template, id=template_id)
        subscription = Subscription.objects.filter(
            user=user, template=template)
        return JsonResponse({'success': True,
                             'subscribed': subscription.exists()})

    # Subscribe a username to a template
    @ action(detail=False, methods=['post'], url_path=r"subscribe/(?P<username>[\w.@+-]+)/(?P<template_id>[\w.@+-]+)")
    def subscribe(self, request, username, template_id):
        """
        Subscribes a given user to a given template.

        Args:
        - request: the request object
        - username: the username of the user to subscribe
        - template_id: the id of the template to subscribe to

        Returns:
        - A JSON response indicating if the given user was successfully subscribed to the given template.
        """
        user = get_object_or_404(User, username=username)
        # check if user is authed
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not logged in'})

        template = get_object_or_404(Template, id=template_id)
        subscription_exists = Subscription.objects.filter(
            user=user, template=template).exists()
        if subscription_exists:
            return JsonResponse({'error': 'Subscription already exists'})

        subscription = Subscription.objects.create(
            user=user, template=template)
        return JsonResponse({'success': "Successfully subscribed to template."})

    @ action(detail=False, methods=['post'], url_path=r"unsubscribe/(?P<username>[\w.@+-]+)/(?P<template_id>[\w.@+-]+)")
    def unsubscribe(self, request, username, template_id):
        """
        Unsubscribes a given user from a given template.

        Args:
        - request: the request object
        - username: the username of the user to unsubscribe
        - template_id: the id of the template to unsubscribe from

        Returns:
        - A JSON response indicating if the given user was successfully unsubscribed from the given template.
        """
        user = get_object_or_404(User, username=username)
        # check if user is authed
        if not user.is_authenticated:
            return JsonResponse({'error': 'User not logged in'})

        template = get_object_or_404(Template, id=template_id)
        subscription = Subscription.objects.filter(
            user=user, template=template)
        if not subscription.exists():
            return JsonResponse({'error': 'Subscription does not exist'})

        subscription.delete()
        return JsonResponse({'success': "Successfully unsubscribed from template."})
