from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Template
from rest_framework.decorators import action
from django.utils.decorators import method_decorator

# Models
from .models import Template, Subscription

# Serializers
from .serializers import SimpleUserSerializer, UserSerializer
from .serializers import SimpleTemplateSerializer, TemplateSerializer
from .serializers import SubscriptionSerializer


# Annotations
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import redirect


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(login_required)
    @action(detail=True, methods=['post'], url_path=r"subscribe/(?P<template_id>\d+)")
    def subscribe(self, request, pk=None, template_id=None):
        template = get_object_or_404(Template, id=template_id)
        template.subscribers.add(User.objects.get(id=pk))
        return Response({'success': True})

    @method_decorator(login_required)
    @action(detail=True, methods=['post'], url_path=r"unsubscribe/(?P<template_id>\d+)")
    def unsubscribe(self, request, pk=None, template_id=None):
        template = get_object_or_404(Template, id=template_id)
        template.subscribers.remove(User.objects.get(id=pk))
        return Response({'success': True})

    @action(detail=False, methods=['get'], url_path=r"current")
    def current(self, request):
        user = request.user
        if user.is_authenticated:
            serializer = SimpleUserSerializer(user)
            return Response({
                'success': 'User logged in',
                'user': serializer.data
            })
        else:
            return Response({'error': 'User not logged in'})


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    # No actions needed for the moment


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    # TODO Check wether this is needed and correct
    @action(detail=False, methods=['get'], url_path=r"user/(?P<user_id>\d+)")
    def get_subscriptions(self, request, user_id=None):
        try:
            user = User.objects.get(id=user_id)
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

    # # TODO Check wether this is needed and correct
    # @action(detail=True, methods=['post'])
    # def get_subscribers(self, request, template_id):
    #     template = get_object_or_404(Template, id=template_id)
    #     return JsonResponse({
    #         'success': True,
    #         # View can fetch each user's data
    #         'subscribers': [user.id for user in template.subscribers.all()]
    #     })

    # Check wether a user is subscribed to a template
    # @action(detail=True, methods=['get'], url_path=r"subscribed/(?P<template_id>\d+)")
    # def subscribed(self, request, pk=None, template_id=None):
    #     user = User.objects.get(id=pk)
    #     template = get_object_or_404(Template, id=template_id)
    #     return Response({
    #         'success': True,
    #         'subscribed': user in template.subscribers.all()
    #     })

    # Authentication


class LoginView(APIView):
    def post(self, request):
        if (request.user.is_authenticated):
            return Response({'error': 'User already logged in'})
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(
            request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_authenticated:
                return Response({'success': 'Login Successful'})
            else:
                return Response({'error': 'User not authenticated'})
        return Response({'error': 'Wrong Credentials'})


class LogoutView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'User not logged in'})

        logout(request)
        return Response({'success': 'Logout Successful'})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
