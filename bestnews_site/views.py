from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Article

# once I get these figured out I'll only need 2, confused atm
def home_page(request):
    section = 'local'
    local_news = Article.objects.filter(section=section).order_by('?')
    paginator = Paginator(local_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def national(request):
    section = 'national'
    news = Article.objects.filter(section=section).order_by('?')
    paginator = Paginator(news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def world(request):
    world_news = Article.objects.filter(section='world').order_by('?')
    section = 'world'
    paginator = Paginator(world_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def business(request):
    business_news = Article.objects.filter(section='business').order_by('?')
    section = 'business'
    paginator = Paginator(business_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def metro(request):
    metro_news = Article.objects.filter(section='metro').order_by('?')
    section = 'metro'
    paginator = Paginator(metro_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def investigations(request):
    investigations_news = Article.objects.filter(section='investigations').order_by('?')
    section = 'investigations'
    paginator = Paginator(investigations_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def politics(request):
    politics_news = Article.objects.filter(section='politics').order_by('?')
    section = 'politics'
    paginator = Paginator(politics_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})

def opinion(request):
    opinion_news = Article.objects.filter(section='opinion').order_by('?')
    section = 'opinion'
    paginator = Paginator(opinion_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'section.html', {'page_obj': page_obj, 'section': section})