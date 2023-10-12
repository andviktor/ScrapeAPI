from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, ProjectViewSet, ScraperViewSet, ElementViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'scrapers', ScraperViewSet, basename='scraper')
router.register(r'elements', ElementViewSet, basename='element')

urlpatterns = [
    path('', include(router.urls)),
]
