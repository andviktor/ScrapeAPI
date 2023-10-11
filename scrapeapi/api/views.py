from rest_framework import viewsets
from .models import Project, Scraper, Element
from .serializers import ProjectSerializer, ScraperSerializer, ElementSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ScraperViewSet(viewsets.ModelViewSet):
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
