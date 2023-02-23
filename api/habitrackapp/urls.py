from django.contrib import admin
from django.urls import path, include
from habitrackapp import views
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register("templates",
                views.TemplateViewSet,
                basename="template")


urlpatterns = [
    # TODO Remove
    path("users/", views.UserList.as_view(), name="user-list"),
    path(
        "users/<int:pk>/",
        views.UserDetail.as_view(),
        name="user-detail",
    ),
    path("", include(router.urls))
]
