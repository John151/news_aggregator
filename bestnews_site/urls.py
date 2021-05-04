from django.urls import path
from . import views

urlpatterns = [
    #landing page, local news aggregate
    path('', views.home_page, name='home_page')
]