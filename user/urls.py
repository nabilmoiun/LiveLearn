from django.urls import path, include

from rest_framework import routers

from .views import (
    UserViewSetAdmin
)

router = routers.DefaultRouter()
router.register("users", UserViewSetAdmin, basename="users")

urlpatterns = [
    path("", include(router.urls))
]
