from rest_framework import viewsets
from .models import Project, Scraper
from .serializers import ProjectSerializer, ScraperSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ScraperViewSet(viewsets.ModelViewSet):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer
