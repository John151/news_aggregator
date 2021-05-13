from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Article


def home_page(request):
    local_news = Article.objects.filter(section='local').order_by('?')
    section = 'local'
    paginator = Paginator(local_news, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj, 'section': section})

def national(request):
    national_news = Article.objects.filter(section='national')
    return render(request, 'national.html', {'news': national_news})