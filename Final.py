import nltk
from bs4 import BeautifulSoup
from urllib import request
# import urllib2
from nltk import word_tokenize
from nltk.corpus import stopwords
import ast
import string

def filter_stopwords(text):
    all_stopwords = stopwords.words('english')
    content_without_sw = [w for w in text if w.lower() not in all_stopwords]
    return content_without_sw


if __name__ == '__main__':

    # Getting content from the websites
    url = "http://www.slate.com/articles/health_and_science/science/2016/11/standing_rock_shows_why_environmentalists_should_move_beyond_cost_benefit.html"
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find_all("script", type="application/ld+json")
    content = ast.literal_eval(script[0].get_text().strip())['articleBody']
    
    # tokenize the string object
    tokens = word_tokenize(content)
    
    # filter out punctuation
    punctuations = list(string.punctuation)
    tokens = [word for word in tokens if word not in punctuations]
    
    # creating NLTK text object
    text = nltk.Text(tokens)
    
    # filter out stopwords
    text_without_sw = filter_stopwords(text)
    
    # stemming with Porter stemmer
    porter = nltk.PorterStemmer()
    text_after_stemming = [porter.stem(t) for t in text_without_sw]
    unique_text_after_stemming = list(set(text_after_stemming))
    print(unique_text_after_stemming)
    
    
    
    
    
    
    
    