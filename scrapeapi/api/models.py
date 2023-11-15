from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self) -> str:
        return self.title

class Scraper(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300, blank=True)
    output_json = models.JSONField(null=True, blank=True)
    exec_datetime = models.DateTimeField(null=True, blank=True)
    headers = models.TextField(blank=True)
    source_urls = models.TextField(blank=True)
    source_json_url_field = models.CharField(max_length=100, blank=True)
    in_favorites = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title

class Element(models.Model):
    scraper = models.ForeignKey(Scraper, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    xpath = models.TextField()
    regex_sub_pattern = models.TextField(blank=True)
    regex_sub_repl = models.TextField(blank=True)
    regex_search = models.TextField(blank=True)
    concat_result = models.CharField(max_length=10, blank=True)

    def __str__(self) -> str:
        return self.title
