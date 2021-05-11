import sys
sys.path.append(".")
from news_source import News_Source


list_news_obj = []

# collections of news sites urls, each should have a local and at least one other
# others will be in their own pages by category
# Ideally there will be at least one for each state, for now 2 per region will suffice

# Alabama
burmingham_news = News_Source('The Birmingham News', 'Birmingham, AL', 'https://www.al.com/', 'news')
burmingham_news.add_path('politics', 'politics')
burmingham_news.add_path('opinion', 'opinion')
list_news_obj.append(burmingham_news)

# Alaska
# Arizona
# Arkansas
# California
# sf_chronicle = News_Source('San Francisco Chronicle', 'San Francisco, CA', 'https://www.sfchronicle.com/', 'local')
# sf_chronicle.add_path('business', 'business')
# sf_chronicle.add_path('politics', 'politics')
# sf_chronicle.add_path('investigations', 'investigations')
# sf_chronicle.add_path('opinion', 'opinion')
# list_news_obj.append(sf_chronicle)

# Colorado
denver_post = News_Source('The Denver Post', 'Denver, CO', 'https://www.denverpost.com/', 'news')
denver_post.add_path('national', 'news/national')
denver_post.add_path('world', 'news/world')
denver_post.add_path('environment', 'news/environment')
denver_post.add_path('education', 'news/education')
list_news_obj.append(denver_post)

# Connecticut
# Delaware
# Florida
# Georgia
atlanta_journal = News_Source('Atlanta Journal Constitution', 'Atlanta, GA', 'https://www.ajc.com/', 'news/atlanta-news')
atlanta_journal.add_path('national', 'news/nation-world')
atlanta_journal.add_path('investigations', 'news/investigations')
list_news_obj.append(atlanta_journal)

# Hawaii
# Idaho
# Illinois
chicago_tribune = News_Source('Chicago Tribune', 'Chicago, IL', 'https://www.chicagotribune.com/', 'midwest')
chicago_tribune.add_path('environment', 'news/environment')
chicago_tribune.add_path('investigations', 'investigations')
chicago_tribune.add_path('politics', 'politics')
chicago_tribune.add_path('criminal_justice', 'criminal-justice')
chicago_tribune.add_path('national', 'nation-world')
chicago_tribune.add_path('business', 'business')
list_news_obj.append(chicago_tribune)

# Indiana
# Iowa
# Kansas
# Kentucky
# Louisiana
# Maine
# Maryland
# Massachusetts
boston_herald = News_Source('Boston Herald', 'Boston, MA','https://www.bostonherald.com/', 'news/massachusetts-news')
boston_herald.add_path('national', 'news/national-news')
boston_herald.add_path('world', 'news/world-news')
list_news_obj.append(boston_herald)

# Michigan
detroit_free = News_Source('Detroit Free Press', 'Detroit, MI', 'https://www.freep.com/', 'news/michigan')
detroit_free.add_path('metro', 'news/detroit')
detroit_free.add_path('politics', 'news/politics')
detroit_free.add_path('investigations', 'news/investigations')
detroit_free.add_path('business', 'business')
detroit_free.add_path('opinion', 'opinion')
list_news_obj.append(detroit_free)

# Minnesota - issue with results returned
# star_tribune = News_Source('Star Tribune', 'Minneapolis, MN', 'https://www.startribune.com/', 'local')
# star_tribune.add_path('business', 'business')
# star_tribune.add_path('opinion', 'opinion')
# star_tribune.add_path('national', 'nation')
# star_tribune.add_path('world', 'world')
# star_tribune.add_path('science', 'science')
# list_news_obj.append(star_tribune)

# Mississippi
# Missouri
stl_post = News_Source('St. Louis Post Dispatch', 'St. Louis, MO', 'https://www.stltoday.com/', 'news/local/metro')
stl_post.add_path('politics', 'news/local/govt-and-politics')
stl_post.add_path('metro', 'news/local/metro')
stl_post.add_path('opinion', 'opinion')
stl_post.add_path('business', 'business/national-and-international')
list_news_obj.append(stl_post)

# Montana
# Nebraska
# Nevada
# New Hampshire
# New Jersey
# New Mexico
# New York
# North Carolina
# North Dakota
# Ohio
# Oklahoma
# Oregon
# Pennsylvania - inquirer returns nothing
# philadelphia_inq = News_Source('The Philadelphia Inquirer', 'Philadelphia, PA', 'https://www.inquirer.com/', 'news/pennsylvania')
# philadelphia_inq.add_path('politics', 'politics')
# philadelphia_inq.add_path('national', 'news/nation-world')
# philadelphia_inq.add_path('economy', 'economy')
# philadelphia_inq.add_path('opinion', 'opinion')
# list_news_obj.append(philadelphia_inq)

# Rhode Island
# South Carolina
# South Dakota
# Tennessee
# Texas
# houston_chron = News_Source('The Houston Chronicle', 'Houston, TX', 'https://www.chron.com/', 'news/houston-texas')
# houston_chron.add_path('national', 'news/nation-world/nation')
# houston_chron.add_path('world', 'news/nation-world/world')
# list_news_obj.append(houston_chron)

# Utah
# Vermont
# Virginia
# Washington
# West Virginia
# Wisconsin
milwaukee_journal = News_Source('Milwaukee Journal Sentinal', 'Milwaukee, WI', 'https://www.jsonline.com/', 'news/state')
milwaukee_journal.add_path('business', 'business')
list_news_obj.append(milwaukee_journal)

# Wyoming

# Student papers, intrest specific publications like environmentalist, feminist, progressive, etc