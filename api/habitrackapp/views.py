# Django
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
# Authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Serializers
from .serializers import SimpleUserSerializer, UserSerializer


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

    @ staticmethod
    def get(request, format=None):
        if request.user.is_authenticated:
            return JsonResponse({
                'success': True,
                'username': request.user.username})
        else:
            return JsonResponse({
                'success': True,  # also true even if the user is not authenticated
                'username': None})


#####################################################################
# User space


class MyProfileView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @ staticmethod
    def get(request, format=None):
        user = request.user
        return JsonResponse(SimpleUserSerializer(user).data)
