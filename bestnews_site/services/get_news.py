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
# os.environ.setd`efault('DJANGO_SETTINGS_MODULE', 'bestnews.settings')
# django.setup() 

# from bestnews_site.models import news_articles

def build_newspapers():

    for newspaper_source in list_news_obj:
        print('*' * 50)
        print(f'\nName: {newspaper_source.name}')
        local = newspaper_source.make_local_url()
        print(f'Local url {local}')
        newspaper_build = newspaper.build(local)
        for article in newspaper_build.articles:
            url_to_check = article.url
            print(f'Article url: {url_to_check}')
            publication = newspaper_source.name
            url_check = filter_junk_results(url_to_check, publication, 'local')
            if url_check:

                article.download()
                article.parse()

                title = article.title
                url = article.url
                pubication = newspaper_source.name
                city = newspaper_source.place
                section = 'local'
                authors = article.authors
                date = article.publish_date
                body = article.text
                summary = article.summary
                image = article.top_image
                print (f'Title: {title}, url: {url}, publication: {publication}, city: {city}\nsection: {section}, authors: {authors}')
                print(f'body text 100 char: {body[100:]}\nsummary:{summary}\n\n')

"""This function checks the urls against known bad responses, returns boolean value"""
def filter_junk_results(url, publication, section):

    # good results includes publication name, first and last places for string slicing for comparison, and results we want
    good_results = {
        'The Birmingham News': {'first': 19, 'last': 23, 'good_result': ['news', 'life']},
        'The Denver Post': {'first': 12, 'last': 29, 'good_result': ['denverpost.com/20']},
        'Atlanta Journal Constitution': {'first': 12, 'last': 25, 'good_result': ['ajc.com/news/']},
        'Chicago Tribune': {'first': 12, 'last': 35, 'good_result': ['chicagotribune.com/midw', 'chicagotribune.com/news', 'chicagotribune.com/subu']},
        'Boston Herald': {'first': 12, 'last': 31, 'good_result': ['bostonherald.com/20']},
        'Detroit Free Press': {'first': 12, 'last': 37, 'good_result': ['reep.com/story/news/local', 'freep.com/story/news/loca']},
        'St. Louis Post Dispatch': {'first': 12, 'last': 35, 'good_result': ['stltoday.com/news/local']},
        'Milwaukee Journal Sentinal': {'first': 24, 'last': 40, 'good_result': ['story/news/local', 'story/communitie']}
    }

    first = good_results[publication]['first']
    print(f'first {first}')
    last = good_results[publication]['last']
    print(f'last {last}')
    truncated_url = url[first:last]
    print(f'truncated url {truncated_url}')
    li_good_result = good_results[publication]['good_result']
    print(f'li_good_result {li_good_result}')


    # the responses from some publications are less straight forward and require more attention
    if publication == 'Atlanta Journal Constitution':
        exception_check = url[:5]
        atlanta_last_characters = ['blog/']

        if exception_check == 'blog/': # atlanta journal constitution returns blog results
            print('atlanta exception check occurred')
            print(f'offending url: {url}')
            return False

    if publication == 'St. Louis Post Dispatch': # st louis post dispatch returns links to sections along with articles
        if len(url) <= 60:
            print('st louis under 60 char')
            return False
        
        if url[25:] != 'https://www.stltoday.com/':
            print(f'stl not correct beginning\nurl:{url}')
            return False

        stlouis_add_check = url[25:28]
        print(f'st louis checks, add:\n{stlouis_add_check}')
        if stlouis_add_check == 'ads':
            print(f'failed add check,\n{url}')
            return False

    if publication == 'Chicago Tribune':
        chicago_html_check = url[:4]
        if chicago_html_check != 'html':
            return False

        chicago_obit_check = url[36:46]
        if chicago_obit_check == 'obituaries':
            print(f'chicago obit')
            return False


    # finally we can check results and possibly return true
    if truncated_url in li_good_result:
        print('truncated url matched li_good_result item')
        return True
        

build_newspapers()
    # url matches, and notes for sources that have issues
    # The Birmingham News
    # al.com/news/
    # al.com/life/
    # al.com/business/

    # San Francisco Chronicle
    # issue

    # The Denver Post
    # denverpost.com/20

    # Atlanta Journal Constitution
    # ajc.com/news/
    # and not
    # https://www.ajc.com/news/commuting-blog/

    # Chicago Tribune
    # chicagotribune.com/midwest/
    # chicagotribune.com/news/

    # Boston Herald
    # bostonherald.com/20

    # Detroit Free Press *not 12* normal slice will be slightly different
    # https://cm.f reep.com/story/news/local 12-25
    # freep.com/story/news/loca 12-25

    # Star Tribune
    # issue - returns 1 link, e.g. https://www.startribune.com/local/start-from/1619712935/

    # St. Louis Post Dispatch
    # stltoday.com/news/local

    # The Philadelphia Inquirer
    # issue - returns nothing

    # The Houston Chronicle
    # issue - only returns top level urls, links to secions and blogs

    # Milwaukee Journal Sentinal
    # jsonline.com/ story/news/local
    # jsonline.com/ story/communitie 

    # for section in newspaper.paths:
    #     print(section)
    #     section_url = newspaper.make_path(section)
    #     print(section_url)

    # here for reference
    # class Article(models.Model):
    # title = models.CharField(blank=False, unique=True)
    # url = models.CharField(max_length=100, blank=False, unique=True)
    # publication = models.CharField(max_length=100, blank=False)
    # section = models.CharField(max_length=25, blank=False)
    # authors = models.CharField(max_length=50, blank=False)
    # date = models.DateField(blank=False)
    # body = models.CharField(blank=False)
    # image = models.ImageField(upload_to='article_images/', blank=True, null=True)