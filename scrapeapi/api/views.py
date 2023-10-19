from rest_framework import viewsets, status
from rest_framework.views import APIView
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
        queryset = Scraper.objects.filter(project__user=self.request.user)
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
        queryset = Element.objects.filter(scraper__project__user = self.request.user)
        if 'scraper' in self.request.data:
            queryset = queryset.filter(scraper=self.request.data['scraper'])
        return queryset

    def create(self, request, *args, **kwargs):
        if request.data.get('scraper'):
            scraper = Scraper.objects.get(pk=request.data.get('scraper'))
            if scraper.project:
                if scraper.project.user == request.user:
                    return super().create(request, *args, **kwargs)
        response = {'element': 'Incorrect parameters passed.'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post']

class ScraperResult(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, scraper_id):
        scraper = Scraper.objects.get(pk=scraper_id)
        if scraper.project.user == request.user:
            response = scraper.output_json
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = {
                'message': 'Scraper not found.'
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)