from django.contrib import admin
from django.urls import path, include
from habitrackapp import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView

router = DefaultRouter()

router.register("templates",
                views.TemplateViewSet,
                basename="template")

router.register("users",
                views.UserViewSet,
                basename="user")

router.register("subscriptions",
                views.SubscriptionViewSet,
                basename="subscription")

# router.register("register",
#                 views.RegisterView,
#                 basename="register")

urlpatterns = [
    path("", include(router.urls)),

    path('csrf/', views.get_csrf, name='api-csrf'),
    path('login/', views.login_view, name='api-login'),
    path('logout/', views.logout_view, name='api-logout'),
    path('session/', views.SessionView.as_view(), name='api-session'),  # new
    path('whoami/', views.WhoAmIView.as_view(), name='api-whoami'),  # new

]
