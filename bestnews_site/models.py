from django.db import models
from django.core.files.storage import default_storage
import datetime


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    url = models.CharField(max_length=100, blank=False, unique=True)
    publication = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=30, blank=False)
    section = models.CharField(max_length=25, blank=False)
    authors = models.CharField(max_length=50, blank=False)
    date = models.DateTimeField(auto_now_add=True, blank=False)
    body = models.TextField()
    image = models.CharField(max_length=100, blank=True, null=True)