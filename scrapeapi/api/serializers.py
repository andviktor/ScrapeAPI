from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import User, Project, Scraper, Element

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'user')

class ScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scraper
        fields = ('id', 'project', 'title', 'description', 'source_urls', 'source_scraper', 'source_scraper_urls_element', 'output_json', 'exec_datetime', 'headers', 'in_favorites')

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ('id', 'scraper', 'title', 'xpath', 'regex_sub_pattern', 'regex_sub_repl', 'regex_search', 'concat_result')
        extra_kwargs = {
            "regex_sub_pattern": {"trim_whitespace": False},
            "regex_sub_repl": {"trim_whitespace": False},
            "concat_result": {"trim_whitespace": False},
            }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
