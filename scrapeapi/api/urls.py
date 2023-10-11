from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ProjectViewSet, ScraperViewSet, ElementViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('projects', ProjectViewSet)
router.register('scrapers', ScraperViewSet)
router.register('elements', ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
