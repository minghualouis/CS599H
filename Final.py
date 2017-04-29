#!/etc/env python
"""
This is the Final project of CS599H 
Authors: Minghua Liu, Olaoluwa Komolafe and Emily Hardy
"""

import nltk
from bs4 import BeautifulSoup
from urllib import request, error
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize
from nltk.corpus import stopwords
import ast
import string
from nltk.probability import FreqDist
import requests

def filter_stopwords(text):
    all_stopwords = stopwords.words('english')
    content_without_sw = [w for w in text if w.lower() not in all_stopwords]
    return content_without_sw

def handle_nytimes_content(url):
    q = requests.get(url)
    soup = BeautifulSoup(q.text, "html.parser")
    p_set = soup.find_all("p", class_= "story-body-text story-content")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content
    
    
def handle_slate_content(url):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find_all("script", type="application/ld+json")
    content = ast.literal_eval(script[0].get_text().strip())['articleBody']
    return content

def handle_huffingtonpost_content(url):
    req = requests.Request('GET', url, headers={'Accept-Encoding': 'gzip, deflate, sdch'})
    r = req.prepare()
#     print(req.prepare())
    s = requests.Session()
    q = s.send(r)
    soup = BeautifulSoup(q.text, "html.parser")
    p_set = soup.find_all("div", class_= "content-list-component bn-content-list-text text")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content
    
def handle_breitbart_content(url):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("p")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content

def handle_washingtonpost_content(url):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("article")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content

def handle_foxnews_content(url):
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("div", class_="article-text")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content

if __name__ == '__main__':

    # Getting content from the websites
    #url = "http://www.slate.com/articles/health_and_science/science/2016/11/standing_rock_shows_why_environmentalists_should_move_beyond_cost_benefit.html"
    #url = "https://www.nytimes.com/2017/02/07/us/army-approves-construction-of-dakota-access-pipeline.html"
    #url = "http://www.huffingtonpost.com/entry/rex-tillerson-keystone-pipeline_us_58c21ebae4b0ed71826b8e1a"
    #url = "http://www.huffingtonpost.com/entry/defiant-as-ever-water-protectors-vow-to-continue-the-fight-against-the-dakota-black-snake-pipeline_us_588a738de4b0303c0752b963?utm_hp_ref=dakota-access-pipeline"
    #url = "http://www.huffingtonpost.com/entry/obama-dakota-access-pipeline-halt_us_5844882be4b0c68e04817323"
    #url = "http://www.breitbart.com/news/us-shutting-down-dakota-access-oil-pipeline-protest-camp/"
    #url = "https://www.washingtonpost.com/news/monkey-cage/wp/2016/09/20/this-is-why-environmentalists-are-targeting-energy-pipelines-like-the-north-dakota-project/?utm_term=.9c78e4ca29af"
    url = "http://www.foxnews.com/us/2017/03/07/judge-wont-stop-construction-dakota-access-pipeline.html"
    
    if url.startswith("https://www.nytimes.com"):
        content = handle_nytimes_content(url)
    elif url.startswith("http://www.slate.com"):
        content = handle_slate_content(url)
    elif url.startswith("http://www.huffingtonpost.com"):
        content = handle_huffingtonpost_content(url)
    elif url.startswith("http://www.breitbart.com"):
        content = handle_breitbart_content(url)
    elif url.startswith("https://www.washingtonpost.com"):
        content = handle_washingtonpost_content(url)
    elif url.startswith("http://www.foxnews.com"):
        content = handle_foxnews_content(url)
    # Confirm the content, for debug
#     print("This is the content: {0}".format(content))

    # tokenize the string object
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(content)
#     tokens = word_tokenize(content) # use above tokenization cause it will better handle the punctuations
    
    # filter out punctuation
#     print(string.punctuation)
#     punctuations = list(string.punctuation)
#     punctuations.append("”")
#     punctuations.append("“")
#     tokens = [word for word in tokens if word not in punctuations]
    
    # creating NLTK text object
    text = nltk.Text(tokens)
    
    # filter out stopwords
    text_without_sw = filter_stopwords(text)
    
    # stemming with Porter stemmer
    porter = nltk.PorterStemmer()
    text_after_stemming = [porter.stem(t) for t in text_without_sw]
    
    # build frequency distribution
    fdist = FreqDist(text_after_stemming)
    fdist.tabulate()
    print(fdist)
    
    
    
    
    