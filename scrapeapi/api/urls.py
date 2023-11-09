from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'projects', views.ProjectViewSet, basename='project')
router.register(r'scrapers', views.ScraperViewSet, basename='scraper')
router.register(r'elements', views.ElementViewSet, basename='element')

urlpatterns = [
    path('', include(router.urls)),
    path('scrapers/<int:scraper_id>/json/', views.ScraperResult.as_view())
]
