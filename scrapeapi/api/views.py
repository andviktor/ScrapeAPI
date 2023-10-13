from django.db.models import Exists
from django.http.request import QueryDict
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny
from .models import User, Project, Scraper, Element
from .serializers import UserSerializer, ProjectSerializer, ScraperSerializer, ElementSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
    
class ScraperViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ScraperSerializer

    def get_queryset(self):
        queryset = Scraper.objects.filter(project__in=Project.objects.filter(user=self.request.user))
        if 'project' in self.request.data:
            queryset = queryset.filter(project=self.request.data['project'])
        return queryset

    def create(self, request, *args, **kwargs):
        if request.data.get('project'):
            project = Project.objects.get(pk=request.data.get('project'))
            if project:
                if project.user == request.user:
                    return super().create(request, *args, **kwargs)
        response = {'scraper': 'Incorrect parameters passed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                

class ElementViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication, )
    serializer_class = ElementSerializer
    
    def get_queryset(self):
        queryset = Element.objects.filter(scraper__in=Scraper.objects.filter(project__in=Project.objects.filter(user=self.request.user)))
        if 'scraper' in self.request.data:
            queryset = queryset.filter(scraper=self.request.data['scraper'])
        return queryset

    def create(self, request, *args, **kwargs):
        scraper = Scraper.objects.get(pk=request.data.get('scraper'))
        project = Project.objects.get(pk=scraper.project.id)
        if project.user == request.user:
            return super().create(request, *args, **kwargs)
        else:
            response = {'scraper': 'Scraper not found.'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']
