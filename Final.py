
#!/etc/env python
"""
This is the Final project of CS599H 
Authors: Minghua Liu, Olaoluwa Komolafe and Emily Hardy
"""

import nltk, ast, string, sys,requests
from bs4 import BeautifulSoup
from urllib import request, error
from nltk.tokenize import RegexpTokenizer
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import wordcloud
import matplotlib.pyplot as plt


def filter_stopwords(text):
    """
    This function filters out the stop words
    
    :return: a list of words
    :rtype: a list of words without stop words
    :raise: currently no exception for simplicity
    """
    all_stopwords = stopwords.words('english')
    content_without_sw = [w for w in text if w.lower() not in all_stopwords]
    return content_without_sw

def handle_nytimes_content(url):
    """
    This function handles requests to NY Times
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
    q = requests.get(url)
    soup = BeautifulSoup(q.text, "html.parser")
    p_set = soup.find_all("p", class_= "story-body-text story-content")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content
    
    
def handle_slate_content(url):
    """
    This function handles requests to slate.com
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find_all("script", type="application/ld+json")
    content = ast.literal_eval(script[0].get_text().strip())['articleBody']
    return content

def handle_huffingtonpost_content(url):
    """
    This function handles requests to huffington post
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
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
    """
    This function handles requests to breitbart.com
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("p")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content

def handle_washingtonpost_content(url):
    """
    This function handles requests to washington post
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("article")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content

def handle_foxnews_content(url):
    """
    This function handles requests to fox news
    
    :param a string of url
    :type string
    :return: content of the html
    :rtype: string 
    :raise: currently no exception for simplicity
    """
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, "html.parser")
    p_set = soup.find_all("div", class_="article-text")
    content = ''
    for element in p_set:
        content += element.get_text().strip()
    return content


def get_urls(filePath):
    """
    This function read links from the file
    
    :param path of the file
    :type string
    :return: all links read from the file
    :rtype: list 
    :raise: IndexError if file is not tab delimited
    """
    f = open(filePath)
    urls = f.readlines()
    
    dated_links = list()

    for date_line in urls:
        line = date_line.split("\t")
        sentence = ""
        try:
            sentence = nltk.sent_tokenize(line[1])
        except IndexError:
            print("error:{}".format( sentence))
        date = nltk.sent_tokenize(line[0])
        dated_links +=[(date,sentence)]
    return dated_links  
  
if __name__ == '__main__':
    filein =  r"link_input.txt"
    fileout = r"link_error_out.txt"
    out = open(fileout,"w+")
    
    #get links from file
    dated_links = get_urls(filein)
    
    source_words = list()
    
    for (date,link) in dated_links:
        try:        
            # Getting content from the websites
            url = link[0]
                    
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
            
            # tokenize the string object
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(content)
 
            text = nltk.Text(tokens)
            
            # filter out stopwords
            text_without_sw = filter_stopwords(text)
            
            # stemming with Porter stemmer
            porter = nltk.PorterStemmer()
            text_after_stemming = [porter.stem(t) for t in text_without_sw]
            
            #add words to combined list of words for source
            source_words += text_after_stemming
            
            print("success:"+ link[0])
        except Exception as inst:
            out.write(link[0] + "\n")
            print("Error:"+ link[0])
            print(inst)
       
    #close error file
    out.close()  
    
    # build frequency distribution
    fdist = FreqDist(source_words)
    list_for_wc = fdist.most_common(100)

    new_fdist = FreqDist(dict(list_for_wc))

    wc = WordCloud()

    wc = WordCloud(max_font_size=40).generate_from_frequencies(new_fdist)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    print("End...")
    