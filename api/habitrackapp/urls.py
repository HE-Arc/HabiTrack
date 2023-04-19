# ViewSets
from .viewsets.TemplateViews import TemplateViewSet
from .viewsets.SubscriptionViews import SubscriptionViewSet

# User Tools
from .views import UserViewSet
from .views import SessionView, WhoAmIView
from .views import MyProfileView

# Authentication Tools
from .viewsets.AuthenticationViews import get_csrf, register_view, login_view, logout_view, change_password_view

# Other
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("templates",
                TemplateViewSet,
                basename="template")

router.register("users",
                UserViewSet,
                basename="user")

router.register("subscriptions",
                SubscriptionViewSet,
                basename="subscription")

urlpatterns = [
    path("", include(router.urls)),

    # Practical views for the frontend
    path('csrf/', get_csrf, name='api-csrf'),
    path('register/', register_view, name='api-register'),
    path('login/', login_view, name='api-login'),
    path('logout/', logout_view, name='api-logout'),
    path('session/', SessionView.as_view(), name='api-session'),
    path('whoami/', WhoAmIView.as_view(), name='api-whoami'),

    # User profile views
    path('my-profile/', MyProfileView.as_view(), name='api-my-profile'),
    path('change-password/', change_password_view,
         name='api-change-password'),
]
