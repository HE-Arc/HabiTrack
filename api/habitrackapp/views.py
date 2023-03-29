from django.contrib.auth.models import User
from .serializers import UserSerializer, TemplateSerializer
from rest_framework import generics
from .models import Template
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Template
from rest_framework.decorators import action
from django.utils.decorators import method_decorator


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

# ExempleViewSet(viewsets.ModelViewSet):
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [IsAuthenticated]f


# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# Create your views here.

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


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    # No actions needed for the moment


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    @action(detail=True, methods=['post'])
    def get_subscriptions(self):
        user = self.request.user
        if user.is_authenticated:
            return JsonResponse({
                'success': True,
                # View can fetch each template's data
                'subscriptions': [template.id for template in user.subscriptions.all()]
            })
        else:
            return JsonResponse({'error': 'User not logged in'})

    @action(detail=True, methods=['post'])
    def get_subscribers(self, request, template_id):
        template = get_object_or_404(Template, id=template_id)
        return JsonResponse({
            'success': True,
            # View can fetch each user's data
            'subscribers': [user.id for user in template.subscribers.all()]
        })


# Authentication

class LoginView(APIView):
    def post(self, request):
        if (request.user.is_authenticated):
            # Redirect home
            redirect('home')
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


class AuthUserView(generics.RetrieveAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return request.user.id


class CurrentUserView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({
                'success': 'User logged in',
                'user': user
            })
        else:
            return Response({'error': 'User not logged in'})
