"""Scrapes news sites, adds info to database"""
import newspaper
from newspaper import Article, fulltext, news_pool
import requests
import os
import django
import sys
from source_info import *

# # include this file location on the path 
sys.path.append(os.getcwd())   
# # explain where the settings are - these include where the db is 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bestnews.settings')
django.setup() 

from bestnews_site.models import Article

newspaper_sections = ['criminal_justice','business','education',
                      'environment','investigations', 'metro','national',
                      'opinion', 'politics', 'world']


# def build_newspapers():

    # def build_local():

    #     for newspaper_source in list_news_obj:
            # print('*' * 50)
            # print(f'\nName: {newspaper_source.name}')
            # local = newspaper_source.make_local_url()
            # print(f'Local url {local}')
            # newspaper_build = newspaper.build(local)
            # for article in newspaper_build.articles:
            #     url_to_check = article.url
            #     # print(f'Article url: {url_to_check}')
            #     publication = newspaper_source.name
            #     url_check = filter_junk_results(url_to_check, publication, 'local')
            #     if url_check:
            #         try:
            #             article.download()
            #             article.parse()

            #             title = article.title
            #             url = article.url
            #             publication = newspaper_source.name
            #             city = newspaper_source.place
            #             section = 'local'
            #             authors = article.authors
            #             date = article.publish_date
            #             body = article.text
            #             summary = article.summary
            #             image = article.top_image
            #             try:
            #                 a = Article(title=title, url=url, publication=publication,
            #                 city=city, section=section, authors=authors, date=date, body=body,
            #                 summary=summary, image=image)
            #                 a.save()
            #                 print(f'created new article: {a.title}')
            #             except django.db.utils.IntegrityError as e:
            #                 print('Duplicate entry, not added.', e)
            #             except Exception as e:
            #                 print(e)  
            #             # print (f'Title: {title}, url: {url}, publication: {publication}, city: {city}\nsection: {section}, authors: {authors}')
            #             # print(f'body text 100 char: {body[100:]}\nsummary:{summary}\n\n')
            #         except Exception as e:
            #             print(e)

def build_section(section):
    for newspaper_source in list_news_obj:
        print('*' * 50)
        print(f'\nName: {newspaper_source.name}')
        if section in newspaper_source.paths:
            newspaper_stack = []
            print(f'{newspaper_source.name} has {section} section')
            section_url = newspaper_source.make_path(section)
            print(f'{section} url {section_url}')
            newspaper_build = newspaper.build(section_url)
            newspaper_stack.append(newspaper_build)
            news_pool.set(newspaper_stack, threads_per_source=2) # (3*2) = 6 threads total
            news_pool.join()
            for downloaded_paper in newspaper_stack:
                articles = downloaded_paper.articles
                for article in articles:    
                    print(article.url)
                    print(article.title)
                    url_check = filter_junk_results(article.url, newspaper_source.name, section)
            # for article in newspaper_build.articles:
            #     url_to_check = article.url
            #     print(f'Article url: {url_to_check}')
                    #url_check = filter_junk_results(url_to_check, publication, section)
                    #if url_check:
                        # try:
                        #     article.download()
                        #     article.parse()

                        #     title = article.title
                        #     url = article.url
                        #     publication = newspaper_source.name
                        #     city = newspaper_source.place
                        #     section = 'local'
                        #     authors = article.authors
                        #     date = article.publish_date
                        #     body = article.text
                        #     summary = article.summary
                        #     image = article.top_image
                        #     try:
                        #         a = Article(title=title, url=url, publication=publication,
                        #         city=city, section=section, authors=authors, date=date, body=body,
                        #         summary=summary, image=image)
                        #         a.save()
                        #         print(f'created new article: {a.title}')
                        #     except django.db.utils.IntegrityError as e:
                        #         print('Duplicate entry, not added.', e)
                        #     except Exception as e:
                        #         print(e)  
                            # print (f'Title: {title}, url: {url}, publication: {publication}, city: {city}\nsection: {section}, authors: {authors}')
                            # print(f'body text 100 char: {body[100:]}\nsummary:{summary}\n\n')
                        # except Exception as e:
                        #     print(e)


"""This function checks the urls against known bad responses, returns boolean value"""
def filter_junk_results(url, publication, section):

    # general bad results
    # the responses from some publications are less straight forward and require more attention
    if publication == 'Atlanta Journal Constitution':
        exception_check = url[:5]
        atlanta_last_characters = ['blog/']

        if exception_check == 'blog/': # atlanta journal constitution returns blog results
            print('\natlanta exception check occurred')
            print(f'offending url: {url}')
            return False

    if publication == 'St. Louis Post Dispatch': # st louis post dispatch returns links to sections along with articles
        if len(url) <= 60:
            print('\nst louis under 60 char')
            return False
        
        if url[25:] != 'https://www.stltoday.com/':
            print(f'\nstl not correct beginning\nurl:{url}')
            return False

        stlouis_add_check = url[25:28]
        print(f'st louis checks, add:\n{stlouis_add_check}')
        if stlouis_add_check == 'ads':
            print(f'failed add check,\n{url}')
            return False

    if publication == 'Chicago Tribune':
        chicago_html_check = url[:4]
        if chicago_html_check != 'html':
            print('chicago html check failed')
            return False

        chicago_obit_check = url[36:46]
        if chicago_obit_check == 'obituaries':
            print(f'chicago obit')
            return False

    # good results includes publication name, first and last places for string slicing for comparison, and results we want
    good_results = {
        'The Birmingham News': {'first': 19, 'last': 23, 'local': ['news', 'life'],
             'opinion': ['opin'], 'politics': ['poli']},
        'The Denver Post': {'first': 12, 'last': 29, 'local': ['denverpost.com/20']},
        'Atlanta Journal Constitution': {'first': 12, 'last': 25, 'local': ['ajc.com/news/'],
           'investigations': ['ajc.com/news/investigation'], 'national': ['ajc.com/news/nation-world/'],},
        'Chicago Tribune': {'first': 12, 'last': 35, 'local': ['chicagotribune.com/midw', 'chicagotribune.com/news', 'chicagotribune.com/subu'],
            'criminal_justice': [], 'business': [], 'environment': [], 'investigations': [],
            'national': ['chicagotribune.com/nati'], 'politics': []},
        'Boston Herald': {'first': 12, 'last': 31, 'local': ['bostonherald.com/20'],
            'criminal_justice': [], 'business': [], 'education': [], 'environment': [], 'investigations': [],
            'national': [], 'opinion': [], 'politics': [], 'world': []},
        'Detroit Free Press': {'first': 12, 'last': 37, 'local': ['reep.com/story/news/local', 'freep.com/story/news/loca'],
            'criminal_justice': [], 'business': [], 'education': [], 'environment': [], 'investigations': [],
            'national': [], 'opinion': [], 'politics': [], 'world': []},
        'St. Louis Post Dispatch': {'first': 8, 'last': 35, 'local': ['stltoday.com/news/local'],
            'criminal_justice': [], 'business': [], 'education': [], 'environment': [], 'investigations': [],
            'national': [], 'opinion': [], 'politics': [], 'world': []},
        'Milwaukee Journal Sentinal': {'first': 24, 'last': 40, 'local': ['story/news/local', 'story/communitie'],
            'criminal_justice': [], 'business': ['story/money/'], 'education': [], 'environment': [], 'investigations': [],
            'national': [], 'opinion': [], 'politics': [], 'world': []}
    }
    # The Denver Post urls are very unhelpful for sorting by section
    if publication == 'The Denver Post':
        section = 'local'

    if section == 'opinion':

    if section == 'politics':

    if section == 'national':
        good_results['Atlanta Journal Constitution']['last'] = 38
    if section == 'world':
    if section == 'environment':
    if section == 'education':
    if section == 'investigations':
        good_results['Atlanta Journal Constitution']['last'] = 38

    if section == 'criminal_justice':
    if section == 'business':
        good_results['Milwaukee Journal Sentinal']['last'] = 36

    if section == 'metro':

    if section in good_results[publication]:

        first = good_results[publication]['first']
        print(f'first {first}')
        last = good_results[publication]['last']
        print(f'last {last}')
        truncated_url = url[first:last]
        print(f'truncated url {truncated_url}')
        li_good_result = good_results[publication][section]
        print(f'li_good_result {li_good_result}')


        # finally we can check results and possibly return true
        if truncated_url in li_good_result:
            print('#$%&' * 30)
            print('\nSUCCESS\ntruncated url matched li_good_result item')
            return True
        
if __name__ == "__main__":
    # build_newspapers()
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


