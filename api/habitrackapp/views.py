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
    serializer_class = TemplateSerializer

    # No actions needed for the moment


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # No actions needed for the moment

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
