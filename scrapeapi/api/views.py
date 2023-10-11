from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from .models import Project, Scraper, Element
from .serializers import ProjectSerializer, ScraperSerializer, ElementSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ScraperViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    queryset = Scraper.objects.all()
    serializer_class = ScraperSerializer

class ElementViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
