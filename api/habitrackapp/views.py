from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Template
from rest_framework.decorators import action
from django.utils.decorators import method_decorator


import json
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

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

    @action(detail=False, methods=['delete'], url_path=r"(?P<user_id>\d+)")
    def delete(self, request, pk=None, user_id=None):
        user = get_object_or_404(User, id=user_id)
        if user.is_authenticated:
            user.delete()
            return Response({'success': True})
        else:
            return Response({'success': False}, status=401)

    @ action(detail=False, methods=['delete'], url_path=r"(?P<username>\w+)")
    def delete_by_username(self, request, pk=None, username=None):
        user = get_object_or_404(User, username=username)
        if user.is_authenticated:
            user.delete()
            return Response({'success': True})
        else:
            return Response({'success': False}, status=401)


#####################################################################
# Authentication tools

class SessionView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @ staticmethod
    def get(request, format=None):
        return JsonResponse({'isAuthenticated': True})


class WhoAmIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @ staticmethod
    def get(request, format=None):
        if request.user.is_authenticated:
            return JsonResponse({'username': request.user.username})
        else:
            return JsonResponse({'username': None})


@ ensure_csrf_cookie
def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response


@ require_POST
def register_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'errors': 'Please provide username and password.'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'errors': 'Username already exists.'}, status=409)

    user = User.objects.create_user(username=username, password=password)

    if user is None:
        return JsonResponse({'errors': 'Something went terribly wrong.'}, status=500)

    login(request, user)
    return JsonResponse({'success': 'Successfully registered.'})


@ require_POST
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return JsonResponse({'errors': 'Please provide username and password.'}, status=400)

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse({'errors': 'Invalid credentials.'}, status=401)

    login(request, user)
    return JsonResponse({'success': 'Successfully logged in.'})


@ require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

    logout(request)
    return JsonResponse({'success': 'Successfully logged out.'})


@ require_POST
def change_password_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new')
    confirm_password = data.get('confirm')

    if not username or not password or not new_password or not confirm_password:
        return Response({'error': 'Please enter a new password'}, status=400)

    user = authenticate(request=request, username=username, password=password)
    if user is None:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)

    if new_password != confirm_password:
        return JsonResponse({'error': 'New password and confirm password must match'}, status=400)

    user.set_password(new_password)
    user.save()

    login(request, user)

    return JsonResponse({'success': 'Password changed successfully'})

#####################################################################
# User space


class MyProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @ staticmethod
    def get(request, format=None):
        user = request.user
        return JsonResponse(SimpleUserSerializer(user).data)


#####################################################################
# Model views

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    #####################################################################
    # CRUD

    def create(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        templateData = data.get('template')
        # get template object as Template
        template = Template.objects.create(
            name=templateData.get('name'),
            description=templateData.get('description'),
            option_1=templateData.get('option_1'),
            option_2=templateData.get('option_2'),
            option_3=templateData.get('option_3'),
            option_4=templateData.get('option_4'),
            creator=user)

        if template is None:
            return JsonResponse({'errors': 'Something went terribly wrong.'}, status=500)
        else:
            return JsonResponse({'success': 'Successfully created template.'})

    def get_queryset(self):
        return super().get_queryset().order_by('name')

    def destroy(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        try:
            template = self.get_object()
            if user.id != template.creator.id:
                return JsonResponse({'errors': 'You are not the creator of this template.'}, status=401)

            template.delete()
        except Template.DoesNotExist:
            return JsonResponse({'errors': 'Template does not exist.'}, status=404)

        return JsonResponse({'success': 'Successfully deleted template.'})

    def put(self, request, *args, **kwargs):
        data = request.data
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        templateData = data.get('template')

        try:
            template = Template.objects.get(id=templateData.get('id'))
            if user.id != template.creator.id:
                return JsonResponse({'errors': 'You are not the creator of this template.'}, status=400)

            template.name = templateData.get('name', template.name)
            template.description = templateData.get(
                'description', template.description)
            template.option_1 = templateData.get('option_1', template.option_1)
            template.option_2 = templateData.get('option_2', template.option_2)
            template.option_3 = templateData.get('option_3', template.option_3)
            template.option_4 = templateData.get('option_4', template.option_4)

            template.save()
        except Template.DoesNotExist:
            return JsonResponse({'errors': 'Template does not exist.'}, status=400)

        return JsonResponse({'success': 'Successfully updated template.'})

    @ action(detail=False, methods=['get'], url_path=r"count/(?P<username>[\w.@+-]+)")
    def count_by_user(self, request, username):
        user = get_object_or_404(User, username=username)
        count = self.get_queryset().filter(creator=user).count()
        return JsonResponse({'success': True,
                             'count': count})

    @ action(detail=False, methods=['get'], url_path=r"user/(?P<username>[\w.@+-]+)")
    def get_by_user(self, request, username):
        user = get_object_or_404(User, username=username)
        templates = self.get_queryset().filter(creator=user)
        return JsonResponse({'success': True,
                             'templates': TemplateSerializer(templates, many=True).data})


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @ action(detail=False, methods=['get'], url_path=r"user/(?P<username>[\w.@+-]+)")
    def get_subscriptions(self, request, username=None):
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
        user = get_object_or_404(User, username=username)
        count = self.get_queryset().filter(user=user).count()
        return Response({'success': True,
                         'count': count})

    # Is a username subscribed to a template?
    @ action(detail=False, methods=['get'], url_path=r"(?P<username>[\w.@+-]+)/subscribed/(?P<template_id>[\w.@+-]+)")
    def is_subscribed(self, request, username, template_id):
        user = get_object_or_404(User, username=username)
        template = get_object_or_404(Template, id=template_id)
        subscription = Subscription.objects.filter(
            user=user, template=template)
        return JsonResponse({'success': True,
                             'subscribed': subscription.exists()})

    # Subscribe a username to a template
    @ action(detail=False, methods=['post'], url_path=r"subscribe/(?P<username>[\w.@+-]+)/(?P<template_id>[\w.@+-]+)")
    def subscribe(self, request, username, template_id):
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
