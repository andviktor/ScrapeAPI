from django.urls import path, include
from rest_framework import routers
from .views import ProjectViewSet, ScraperViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('scrapers', ScraperViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
