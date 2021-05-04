"""defines news source properties, each needs name, city/state, homepage url and 
path to local news url. additional paths saved in dictionary as needed"""

class News_Source:
    def __init__(self, name, place, homepage_url, local_news_path):
        self.name = name
        self.place = place
        self.homepage_url = homepage_url
        self.local_news = local_news_path
        self.paths = {}

    def make_local_url(self):
        return str(self.homepage_url + self.local_news)
        #do I need str()? -- check

    def add_path(self, subtopic, path):    
        self.paths[subtopic] = path

    def make_path(self, subtopic):
        return str(self.homepage_url + self.paths[subtopic])

    def soup_url(self, url):
        pass
    # todo beautiful soup this 