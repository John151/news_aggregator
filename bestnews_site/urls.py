from django.urls import path
from . import views

urlpatterns = [
    #landing page, local news aggregate
    path('', views.home_page, name='home_page'),
    path('national/', views.national, name='national'),
    path('world/', views.world, name='world'),
    path('metro/', views.metro, name='metro'),
    path('investigations/', views.investigations, name='investigations'),
    path('business/', views.business, name='business'),
    path('politics/', views.politics, name='politics'),
    path('opinion/', views.opinion, name='opinion'),

]

