from django.contrib.auth.models import User
from .serializers import ComplexUserSerializer, ComplexTemplateSerializer
from rest_framework import generics
from .models import Template
from rest_framework import viewsets
# from django.shortcuts import render
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status

# Create your views here.

# TODO Remove, help for the understanding of CaffeinItemViewSet
# @api_view(["GET", "POST"])
# def template_list(request):
#     if request.method == "GET":
#         templates = Template.objetcs.all()
#         serializer = TemplateSerializer(templates, many=True)
#         return Response(serializer.data)
#     elif request.method == "POST":
#         serializer = TemplateSerializer(templates)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    # We need the complex serializer here
    serializer_class = ComplexTemplateSerializer

    # No actions needed for the moment


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    # We need the complex serializer here
    serializer_class = ComplexUserSerializer

    # No actions needed for the moment
