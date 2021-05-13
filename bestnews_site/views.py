from django.shortcuts import render
from django.db import models
from .models import Article


def home_page(request):
    local_news = Article.objects.filter(section='local')
    return render(request, 'home.html', {'news': local_news})

def national(request):
    national_news = Article.objects.filter(section='national')
    return render(request, 'national.html', {'news': national_news})