from django.contrib import admin
from django.urls import path, include
from habitrackapp import views
from rest_framework.routers import DefaultRouter

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

urlpatterns = [
    path("", include(router.urls)),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('current_user/', views.CurrentUserView.as_view(), name='current_user'),
]
