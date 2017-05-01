import nltk, ast, string, sys
from bs4 import BeautifulSoup
from urllib import request
# import urllib2
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist


def filter_stopwords(text):
    all_stopwords = stopwords.words('english')
    content_without_sw = [w for w in text if w.lower() not in all_stopwords]
    return content_without_sw

def get_urls(filePath):
    f = open(filePath)
    urls = f.readlines()
    
    dated_links = list()

    for date_line in urls:
        line = date_line.split("\t")
        sentence = nltk.sent_tokenize(line[1])
        date = nltk.sent_tokenize(line[0])
        dated_links +=[("type",date,sentence)]
    return dated_links  
  
  
filein =  r"test_link.txt"
fileout = r"test_link_out.txt"
out = open(fileout,"w+")

dated_links = get_urls(filein)

source_words = list()

for (type,date,link) in dated_links:
    try:
       # if __name__ == '__main__':
        
        # Getting content from the websites
        url = link[0]
        html = request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, "html.parser")
        script = soup.find_all("script", type="application/ld+json")
        content = ast.literal_eval(script[0].get_text().strip())['articleBody']
        
        # tokenize the string object
        tokens = word_tokenize(content)
        
        # filter out punctuation
        punctuations = list(string.punctuation)
        tokens = [word.lower() for word in tokens if word not in punctuations]
        
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
         print("Error:", sys.exc_info()[0])
         print(inst)
   
# build frequency distribution
fdist = FreqDist(source_words)
print(fdist)

out.close()  