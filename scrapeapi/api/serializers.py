from rest_framework import serializers
from .models import Project, Scraper

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'user')

class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        fields = ('id', 'project', 'title', 'description', 'output_json', 'exec_datetime', 'headers')
