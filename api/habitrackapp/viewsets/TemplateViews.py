# Django
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import action

# Custom models
from ..models import Template

# Serializers
from ..serializers import SimpleTemplateSerializer, TemplateSerializer


class TemplateViewSet(viewsets.ModelViewSet):
    """
    This file defines the TemplateViewSet class which contains several actions for managing templates.

    Functions:

        create(self, request, *args, **kwargs)
            Creates a new template object with the data provided in the request and associates it with the user who made the request.

        get_queryset(self)
            Returns a queryset of all templates ordered by name.

        destroy(self, request, *args, **kwargs)
            Deletes the template object associated with a specific template ID if the user making the request is the creator of the template.

        put(self, request, *args, **kwargs)
            Updates the template object associated with a specific template ID with the data provided in the request if the user making the request is the creator of the template.

        count_by_user(self, request, username)
            Returns the number of templates associated with a given username.

        get_by_user(self, request, username)
            Returns a list of all templates associated with a given username.
    """

    queryset = Template.objects.all()
    serializer_class = TemplateSerializer

    #####################################################################
    # CRUD

    def create(self, request, *args, **kwargs):
        """
        Is called when a POST request is made to the TemplateViewSet. It creates a new template object with the data provided in the request and associates it with the user who made the request.
        """
        data = request.data
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

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
        """
        Is called when a GET request is made to the TemplateViewSet. Returns a queryset of all templates ordered by name.
        """
        templates = Template.objects.all().order_by('name')
        return templates

    def destroy(self, request, *args, **kwargs):
        """
        Is called when a DELETE request is made to the TemplateViewSet with a specific template ID. It deletes the template object associated with that ID if the user making the request is the creator of the template.
        """
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

        try:
            template = self.get_object()
            if user.id != template.creator.id:
                return JsonResponse({'errors': 'You are not the creator of this template.'}, status=401)

            template.delete()
        except Template.DoesNotExist:
            return JsonResponse({'errors': 'Template does not exist.'}, status=404)

        return JsonResponse({'success': 'Successfully deleted template.'})

    def put(self, request, *args, **kwargs):
        """
        Is called when a PUT request is made to the TemplateViewSet with a specific template ID. It updates the template object associated with that ID with the data provided in the request if the user making the request is the creator of the template.
        """
        data = request.data
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

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

    #####################################################################
    # Tools

    @ action(detail=False, methods=['get'], url_path=r"count/(?P<username>[\w.@+-]+)")
    def count_by_user(self, request, username):
        """
        Is called when a GET request is made to `/templates/count/<username>` with a specific username in the URL path. It returns the number of templates associated with the user with that username.
        """
        user = get_object_or_404(User, username=username)
        count = self.get_queryset().filter(creator=user).count()
        return JsonResponse({'success': True,
                             'count': count})

    @ action(detail=False, methods=['get'], url_path=r"user/(?P<username>[\w.@+-]+)")
    def get_created_templates(self, request, username):
        """
        Is called when a GET request is made to `/templates/user/<username>` with a specific username in the URL path. It returns a list of all templates associated with the user with that username.
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'errors': 'User not found'}, status=404)

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not ' + username + '.'}, status=401)

        templates = Template.objects.filter(creator=user)
        created_data = []
        for template in templates:
            template_data = SimpleTemplateSerializer(
                template).data
            created_data.append(template_data)

        return JsonResponse({
            'success': True,
            'templates': created_data,
        })
