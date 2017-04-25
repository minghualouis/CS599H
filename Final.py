import nltk
from bs4 import BeautifulSoup
from urllib import request
# import urllib2
from nltk import word_tokenize
import json
import ast

if __name__ == '__main__':

    url = "http://www.slate.com/articles/health_and_science/science/2016/11/standing_rock_shows_why_environmentalists_should_move_beyond_cost_benefit.html"
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find_all("script", type="application/ld+json")
    content = ast.literal_eval(script[0].get_text().strip())['articleBody']
    