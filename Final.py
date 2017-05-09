
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


def get_urls(filePath):
    f = open(filePath)
    urls = f.readlines()
    
    dated_links = list()

    for date_line in urls:
        line = date_line.split("\t")
        sentence = nltk.sent_tokenize(line[1])
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
            # Confirm the content, for debug
            #     print("This is the content: {0}".format(content))
            
            # tokenize the string object
            tokenizer = RegexpTokenizer(r'\w+')
            tokens = tokenizer.tokenize(content)
            
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
            
            #add words to combined list of words for source
            source_words += text_after_stemming
            
            print("success:"+ link[0])
        except Exception as inst:
            out.write(link[0] + "\n")
            print("Error:"+ link[0])
            print(inst)
       
    # build frequency distribution
    fdist = FreqDist(source_words)
    list_for_wc = fdist.most_common(100)
#     print(list_for_wc)
    new_fdist = FreqDist(dict(list_for_wc))
#     print(new_fdist.most_common(10))

    out.close()  
    
    #list_for_cloud = [(k,v) for (k,v) in fdist.items() if v > 1]  # use most_common() instead
#     print(list_for_cloud)
    # use WordCloud lib(need to install with pip)
    # https://amueller.github.io/word_cloud/
    # https://github.com/amueller/word_cloud/
    wc = WordCloud()
#     wc.generate_from_frequencies(new_fdist)
#     plt.imshow(wc, interpolation='bilinear')
#     plt.axis("off")
    wc = WordCloud(max_font_size=40).generate_from_frequencies(new_fdist)
    plt.figure()
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    print("End...")
    