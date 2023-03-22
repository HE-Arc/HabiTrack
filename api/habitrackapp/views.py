from django.contrib.auth.models import User
from .serializers import UserSerializer, TemplateSerializer
from rest_framework import generics
from .models import Template
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Template

# Annotations
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView

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


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    # No actions needed for the moment


class SubscriptionViewSet(viewsets.ModelViewSet):
    # TODO Once login is implemented, add user to the template
    # user = request.user
    # template.subscriptions.add(user)
    # For now we add the user with id 1
    #! IMPORTANT None can be replaced by User.objects.get(id=1) but only once migrations are done!
    user = None
    queryset = Template.objects.filter(subscribers=user)
    serializer_class = TemplateSerializer


# Authentication
class SessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'isAuthenticated': True})
        else:
            return Response({'isAuthenticated': False})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'success': 'Login Successful'})

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

    def get_object(self):
        return self.request.user

# Subscription logic

# TODO Uncomment when login is implemented
# @login_required


@csrf_exempt
def subscribe_to_template(request, template_id):
    template = get_object_or_404(Template, id=template_id)
    # TODO Once login is implemented, add user to the template
    # user = request.user
    # template.subscriptions.add(user)
    # For now we add the user with id 1
    template.subscribers.add(User.objects.get(id=1))
    return JsonResponse({'success': True})
