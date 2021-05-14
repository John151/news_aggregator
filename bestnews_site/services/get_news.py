"""Scrapes news sites, adds info to database"""
import newspaper
from newspaper import Article, fulltext, news_pool
import os
import django
from django.utils.timezone import localdate
import sys
from source_info import *

# # include this file location on the path 
sys.path.append(os.getcwd())   
# # explain where the settings are - these include where the db is 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestnews.settings')
django.setup() 

from bestnews_site.models import Article

newspaper_sections = ['criminal_justice','business','education',
                      'environment','investigations', 'local' 'metro', 'national',
                      'opinion', 'politics', 'world']


"""uses newspaper3k library to build newspaper objects
   data like article url, title, is pulled from the objects and put into the database
   this function also invokes a results and reassignment checker
"""

def build_section(section):

    for newspaper_source in list_news_obj:
        print(f'\nName: {newspaper_source.name}')

        if section in newspaper_source.paths:
            newspaper_stack = []
            section_url = newspaper_source.make_path(section)
            newspaper_build = newspaper.build(section_url)
            newspaper_stack.append(newspaper_build)
            news_pool.set(newspaper_stack, threads_per_source=2) # (3*2) = 6 threads total
            news_pool.join()

            for downloaded_paper in newspaper_stack:
                articles = downloaded_paper.articles

                for article in articles:    
                    # print(article.url)
                    # print(article.title)
                    section = filter_junk_results(article.url, newspaper_source.name, section)

                    if section:
                        try:
                            article.download()
                            article.parse()

                            title = article.title
                            url = article.url
                            publication = newspaper_source.name
                            city = newspaper_source.place
                            section = section
                            if article.authors:
                                authors = article.authors[0]
                            else:
                                authors = ''
                            body = article.text
                            summary = article.summary
                            image = article.top_image
                            try:
                                a = Article(title=title, url=url, publication=publication,
                                city=city, section=section, authors=authors, date=date, body=body,
                                summary=summary, image=image)
                                a.save()
                                print(f'created new article: {a.title}')
                            except django.db.utils.IntegrityError as e:
                                print('Duplicate entry, not added.', e)
                            except Exception as e:
                                print(e)  
                            print (f'Title: {title}, url: {url}, publication: {publication}, city: {city}\nsection: {section}, authors: {authors}')
                        except Exception as e:
                            print(e)


"""This function checks the urls against known bad responses, 
    it also makes sure the section is correct based off of its url
    if it is a good result the section is reassigned and returned
    otherwise return is False
"""
def filter_junk_results(url, publication, section):

    # general bad results
    # the responses from some publications are less straight forward and require more attention
    if publication == 'Atlanta Journal Constitution':
        if len(url) <= 45:
            return False

        exception_check = url[:5]
        atlanta_last_characters = ['blog/']

        if exception_check == 'blog/': # atlanta journal constitution returns blog results
            return False

    if publication == 'St. Louis Post Dispatch': # st louis post dispatch returns links to sections along with articles
        if len(url) <= 60:
            return False
        
        if url[25:] != 'https://www.stltoday.com/':
            return False

        stlouis_add_check = url[25:28]
        if stlouis_add_check == 'ads':
            return False

    if publication == 'Chicago Tribune':
        chicago_html_check = url[:4]
        if chicago_html_check != 'html':
            return False

        chicago_obit_check = url[36:46]
        if chicago_obit_check == 'obituaries':
            return False

    # good results includes publication name, first and last places for string slicing for comparison, and results we want
    # url section matches key, value is section to be returned
    good_results = {
        'The Birmingham News': {'first': 19, 'last': 23, 'news': 'local', 'life': 'local',
             'opin': 'opinion', 'poli': 'politics'},
        'The Denver Post': {'first': 12, 'last': 29, 'denverpost.com/20': 'local'},
        'Atlanta Journal Constitution': {'first': 12, 'last': 38, 'ajc.com/news/atlanta-news/': 'local',
           'ajc.com/news/georgia-news/': 'local', 'ajc.com/news/investigation': 'investigations',
            'ajc.com/news/atlanta-news/': 'metro', 'ajc.com/news/nation-world/': 'national'},
        'Chicago Tribune': {'first': 31, 'last': 35, 'midw': 'local', 'news': 'local', 'subu': 'local',
            'crim': 'criminal_justice', 'busi': 'business', 'envi': 'environment', 'inve': 'investigations',
            'nati': 'national', 'poli': 'politics'},
        'Boston Herald': {'first': 12, 'last': 31, 'bostonherald.com/20': 'local'},
        'Detroit Free Press': {'first': 28, 'last': 33, 'local': 'local', 'money': 'business',
         'inves': 'investigations', 'ws/in': 'investigations', 'opini': 'opinion', 'polit': 'politics'},
        'St. Louis Post Dispatch': {'first': 12, 'last': 35, 'stltoday.com/news/local': 'local',
            'stltoday.com/business/l': 'business', 'stltoday.com/opinion/ed': 'opinion',
             'stltoday.com/opinion/co': 'opinion'},
        'Milwaukee Journal Sentinal': {'first': 24, 'last': 40, 'alternate_last': 36, 'story/news/local': 'local', 'story/communitie': 'local',
            'story/money/': 'business'}
    }
    # TODO Detroid free press sometimes has different url pattern, make sure you're getting all relevant results

    # Here some edge cases are sorted out, we may need to adjust more parameters
    # The Denver Post urls are very unhelpful for sorting by section, so is Boston Herald aparently
    if publication == 'The Denver Post' or publication == 'Boston Herald':
        section = 'local'

    if section == 'business':
        good_results['Milwaukee Journal Sentinal']['last'] = 36

    first = good_results[publication]['first']
    print(f'first {first}')
    last = good_results[publication]['last']
    print(f'last {last}')
    truncated_url = url[first:last]
    print(f'truncated url {truncated_url}')
    if 'alternate_last' in good_results[publication]:
        alternate_last = good_results[publication]['alternate_last']
        alternate_truncated_url = url[first:alternate_last]
            
        if alternate_truncated_url in good_results[publication]:
            print('  MATCH ON ALTERNATE')
            section = good_results[publication][alternate_truncated_url]
            return section

    # finally we can check results and possibly return true
    if truncated_url in good_results[publication]:
        print('  MATCH  ')
        section = good_results[publication][truncated_url]
        print(section)
        return section
    

    else:
        print('  NOT A MATCH  ')
        return False
        
if __name__ == "__main__":
    for section in newspaper_sections:
        build_section(section)

    # San Francisco Chronicle
    # issue

    # The Denver Post
    # always this url path:
    # denverpost.com/20

    # Atlanta Journal Constitution
    # ajc.com/news/
    # and not
    # https://www.ajc.com/news/commuting-blog/

    # Boston Herald
    # bostonherald.com/20

    # Star Tribune
    # issue - returns 1 link, e.g. https://www.startribune.com/local/start-from/1619712935/

    # The Philadelphia Inquirer
    # issue - returns nothing

    # The Houston Chronicle
    # issue - only returns top level urls, links to secions and blogs


