# Django
from django.contrib.auth.models import User

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

# Other
import json

"""
This module contains four views that handle user authentication in a Django application.

Functions:
    get_csrf(request)
        Sets the CSRF cookie and returns a JSON response with a success message.

    register_view(request)
        Registers a new user with the provided username and password.

    login_view(request)
        Logs in a user with the provided username and password.

    logout_view(request)
        Logs out the current user.

    change_password_view(request)
        Changes the current user's password to the provided new password.
"""


@ csrf_exempt
def get_csrf(request):
    """
    View function that sets the CSRF cookie and returns a response with a success message. This is called early in the page load process to ensure that the CSRF cookie is set before any AJAX requests are made.

    Parameters:
    ----------
    request: HttpRequest
        The HTTP request object.
    """
    response = JsonResponse({
        'success': 'CSRF cookie set.',
        'csrfToken': get_token(request)
    })
    return response


@ require_POST
def register_view(request):
    """
    View function that handles user registration. Expects a POST request with a JSON payload
    containing a "username" and "password" field. If the username is already taken, returns
    a response with a 409 status code. If the user is successfully created and logged in, returns
    a response with a success message.

    Parameters:
    ----------
    request: HttpRequest
        The HTTP request object.
    """
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
    """
    View function that handles user login. Expects a POST request with a JSON payload containing
    a "username" and "password" field. If the credentials are invalid, returns a response with
    a 401 status code. If the user is successfully authenticated and logged in, returns a
    response with a success message.

    Parameters:
    ----------
    request: HttpRequest
        The HTTP request object.
    """
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
    """
    View function that handles user logout. If the user is not authenticated, returns a response
    with a 400 status code. If the user is successfully logged out, returns a response with
    a success message.

    Parameters:
    ----------
    request: HttpRequest
        The HTTP request object.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'errors': 'You\'re not logged in.'}, status=401)

    logout(request)
    return JsonResponse({'success': 'Successfully logged out.'})


@require_POST
def change_password_view(request):
    """
    View function that handles changing the user's password. Expects a POST request with a JSON
    payload containing a "username", "password", "new", and "confirm" field. If any of the fields
    are missing, returns a response with a 400 status code. If the credentials are invalid or
    the new password and confirm password do not match, returns a response with a 401 or 400
    status code, respectively. If the password is successfully changed and the user is logged in,
    returns a response with a success message.

    Parameters:
    ----------
    request: HttpRequest
        The HTTP request object.
    """
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    new_password = data.get('new')
    confirm_password = data.get('confirm')

    if not username or not password or not new_password or not confirm_password:
        return JsonResponse({'errors': 'Please enter a new password'}, status=400)

    user = authenticate(request=request, username=username, password=password)
    if user is None:
        return JsonResponse({'errors': 'Invalid credentials'}, status=401)

    if new_password != confirm_password:
        return JsonResponse({'errors': 'New password and confirm password must match'}, status=400)

    user.set_password(new_password)
    user.save()

    login(request, user)

    return JsonResponse({'success': 'Password changed successfully'})
