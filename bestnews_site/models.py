from django.db import models
from django.core.files.storage import default_storage


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    url = models.CharField(max_length=100, blank=False, unique=True)
    publication = models.CharField(max_length=100, blank=False)
    city = models.CharField(max_length=30, blank=False)
    section = models.CharField(max_length=25, blank=False)
    date = models.DateField(max_length=25, blank=False)
    body = models.TextField()
    image = models.ImageField(upload_to='article_images/', blank=True, null=True)