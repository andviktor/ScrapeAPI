from rest_framework import serializers
from .models import Project, Scraper, Element

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'user')

class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        fields = ('id', 'project', 'title', 'description', 'output_json', 'exec_datetime', 'headers')

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'scraper', 'title', 'xpath', 'regex_sub', 'regex_search', 'concat_result')
