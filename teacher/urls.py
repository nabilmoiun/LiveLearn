from django.urls import path, include

from rest_framework import routers

from .views import (
    BatchViewSet,
    ProfileViewSet,
    AcademicViewSet,
    ProfessionalExperienceViewSet,
)

router = routers.DefaultRouter()

router.register("academics", AcademicViewSet, basename="academics")
router.register("batches", BatchViewSet, basename="teacher-batches")
router.register("profile", ProfileViewSet, basename="teacher-profile")
router.register("experiences", ProfessionalExperienceViewSet, basename="experiences")


urlpatterns = [
    path("", include(router.urls))
]
