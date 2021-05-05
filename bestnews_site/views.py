from django.shortcuts import render

def home_page(request):
    return render(request, 'home.html')

def national(request):
    national_news = Articles.objects.get(section='national')
    return render(request, 'national.html')