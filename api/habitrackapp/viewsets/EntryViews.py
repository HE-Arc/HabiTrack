# Django
import datetime
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

# Rest Framework
from rest_framework import viewsets
from rest_framework.decorators import action

# Custom models
from ..models import Template, Entry

# Serializers
from ..serializers import EntrySerializer


class EntryViewSet(viewsets.ModelViewSet):
    """
    This file defines the EntryViewSet class which contains several actions for managing entries.

    Functions:

        create(self, request, *args, **kwargs)
            Creates a new entry object with the data provided in the request and associates it with the user who made the request.

        get_queryset(self)
            Returns a queryset of all entries ordered by date.

        destroy(self, request, *args, **kwargs)
            Deletes the entry object associated with a specific entry ID if the user making the request is the creator of the entry.

        put(self, request, *args, **kwargs)
            Updates the entry object associated with a specific entry ID with the data provided in the request if the user making the request is the creator of the entry.

        count_by_user(self, request, username)
            Returns the number of entries associated with a given username.

        get_by_user(self, request, username)
            Returns a list of all entries associated with a given username only if the user making the request is the creator of the entry.
    """

    queryset = Entry.objects.all()
    serializer_class = EntrySerializer

    #####################################################################
    # CRUD

    def create(self, request, *args, **kwargs):
        """
        Is called when a POST request is made to the EntryViewSet. It creates a new entry object with the data provided in the request and associates it with the user who made the request.
        """
        data = request.data
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        entryData = data.get('entry')

        template = get_object_or_404(Template, id=entryData.get('template_id'))
        selected_option = entryData.get('selected_option')

        # Check wether selcted_option is between 0 and 3
        if selected_option < 0 or selected_option > 3:
            return JsonResponse({'errors': 'Selected option is not valid. Given '
                                 + selected_option + ' but expected 0, 1, 2 or 3.'
                                 }, status=400)

        entry = Entry.objects.create(
            user=user,
            template=template,
            selected_option=selected_option)

        if entry is None:
            return JsonResponse({'errors': 'Something went terribly wrong.'}, status=500)
        else:
            return JsonResponse({'success': 'Successfully created entry.'})

    def get_queryset(self):
        """
        Is called when a GET request is made to the EntryViewSet. It returns a queryset of all entries ordered by date.
        """
        return super().get_queryset().order_by('created_at')

    def destroy(self, request, *args, **kwargs):
        """
        Is called when a DELETE request is made to the EntryViewSet. It deletes the entry object associated with a specific entry ID if the user making the request is the creator of the entry.
        """
        user = request.user

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        try:
            entry = Entry.objects.get(pk=kwargs.get('pk'))
            if user.id != entry.user.id:
                return JsonResponse({'errors': 'You\'re not the creator of this entry.'}, status=400)

            entry.delete()
        except Entry.DoesNotExist:
            return JsonResponse({'errors': 'Entry does not exist.'}, status=400)

        return JsonResponse({'success': 'Successfully deleted entry.'})

    def put(self, request, *args, **kwargs):
        """
        Is called when a PUT request is made to the EntryViewSet. It updates the entry object associated with a specific entry ID with the data provided in the request if the user making the request is the creator of the entry.
        """
        user = request.user
        data = request.data

        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=400)

        entryData = data.get('entry')

        try:
            entry = Entry.objects.get(id=entryData.get('id'))
            if user.id != entry.user.id:
                return JsonResponse({'errors': 'You\'re not the creator of this entry.'}, status=400)

            entry.selected_option = entryData.get('selected_option')
            entry.updated = True

            entry.save()
        except Entry.DoesNotExist:
            return JsonResponse({'errors': 'Entry does not exist.'}, status=400)

        return JsonResponse({'success': 'Successfully updated entry.'})

    #####################################################################
    # Tools

    @ action(detail=False, methods=['get'], url_path=r"count/(?P<username>[\w.@+-]+)")
    def count_by_user(self, request, username):
        """
        Is called when a GET request is made to the EntryViewSet with the url path `/entries/count/<username>`. It returns the number of entries associated with a given username.
        """
        user = get_object_or_404(User, username=username)
        count = Entry.objects.filter(user=user).count()
        return JsonResponse({'count': count})

    @ action(detail=False, methods=['get'], url_path=r"user/(?P<username>[\w.@+-]+)")
    def get_by_user(self, request, username):
        """
        Is called when a GET request is made to the EntryViewSet with the url path `/entries/user/<username>`. It returns a list of all entries associated with a given username only if the user making the request is the creator of the entry.
        """
        user = get_object_or_404(User, username=username)
        if request.user.id != user.id:
            return JsonResponse({'errors': 'You\'re not ' + username + '.'}, status=401)

        entries = Entry.objects.filter(user=user)
        serializer = EntrySerializer(entries, many=True)
        return JsonResponse({'entries': serializer.data})

    @ action(detail=False, methods=['get'], url_path=r"template/(?P<template_id>[\w.@+-]+)")
    def get_by_template(self, request, template_id):
        """
        Is called when a GET request is made to the EntryViewSet with the url path `/entries/template/<template_id>`. It returns a list of all entries associated with a given template ID.
        """
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

        template = get_object_or_404(Template, pk=template_id)
        if template.subscribers.filter(id=user.id).exists():
            return JsonResponse({'errors': 'You\'re not subscribed to this template.'}, status=401)

        entries = Entry.objects.filter(template=template_id, user=user)
        serializer = EntrySerializer(entries, many=True)
        return JsonResponse({
            'success': 'Successfully retrieved entries.',
            'entries': serializer.data})

    @ action(detail=False, methods=['get'], url_path=r"template/(?P<template_id>[0-9]+)/today")
    def get_todays_entry_from_template(self, request, template_id):
        """
        Is called when a GET request is made to the EntryViewSet with the url path `/entries/template/<template_id>/today`. It returns the entry object associated with a given template ID and the current date.
        """
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

        template = get_object_or_404(Template, pk=template_id)
        if template.subscribers.filter(id=user.id).exists():
            return JsonResponse({'errors': 'You\'re not subscribed to this template.'}, status=401)

        entries = Entry.objects.filter(
            template=template_id, user=user)
        for entry in entries:
            if entry.created_at.date() == datetime.date.today():
                serializer = EntrySerializer(entry)
                return JsonResponse({
                    'success': 'Successfully retrieved entry.',
                    'entry': serializer.data})
        return JsonResponse({
            'success': 'No Entry found for today.',
            'entry': None})
