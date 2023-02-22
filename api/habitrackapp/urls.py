from django.contrib import admin
from django.urls import path
from habitrackapp import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="user-list"),
    path(
        "users/<int:pk>/",
        views.UserDetail.as_view(),
        name="user-detail",
    ),
]
