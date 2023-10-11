from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, ScraperViewSet, ElementViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('scrapers', ScraperViewSet)
router.register('elements', ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
