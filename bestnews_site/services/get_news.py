"""Scrapes news sites, adds info to database"""
import newspaper
from newspaper import Article, fulltext
from bs4 import BeautifulSoup
import requests
import os
import django
import sys
from source_info import *

# # include this file location on the path 
# sys.path.append(os.getcwd())   
# # explain where the settings are - these include where the db is 
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestnews.settings')
# django.setup() 

# from bestnews_site.models import news_articles

def build_newspapers():

    for newspaper_source in list_news_obj:
        print(newspaper_source.name)
        local = newspaper_source.make_local_url()
        newspaper_build = newspaper.build(local)
        for article in newspaper_build.articles:
            url_to_check = article.url
            pubication = newspaper_source.name
            url_check = filter_junk_results(url_to_check, publication, 'local')
            if url_check:

                article.download()
                article.parse()

                title = article.title
                url = article.url
                pubication = newspaper_source.name
                city = newspaper_source.place
                section = ''
                authors = article.authors
                date = ''
                body = article.text
                image = article.top_image


def filter_junk_results(url, publication, section):
    



    # for section in newspaper.paths:
    #     print(section)
    #     section_url = newspaper.make_path(section)
    #     print(section_url)

    # class Article(models.Model):
    # title = models.CharField(blank=False, unique=True)
    # url = models.CharField(max_length=100, blank=False, unique=True)
    # publication = models.CharField(max_length=100, blank=False)
    # section = models.CharField(max_length=25, blank=False)
    # authors = models.CharField(max_length=50, blank=False)
    # date = models.DateField(blank=False)
    # body = models.CharField(blank=False)
    # image = models.ImageField(upload_to='article_images/', blank=True, null=True)