import os
import django
import sys
import datetime

# # include this file location on the path 
sys.path.append(os.getcwd())   
# # explain where the settings are - these include where the db is 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestnews.settings')
django.setup() 

from bestnews_site.models import Article


def delete_outdated_articles():
    Article.objects.filter(date=datetime.datetime.now() - datetime.timedelta(days=2)).delete()



if __name__ == "__main__":
    delete_outdated_articles()