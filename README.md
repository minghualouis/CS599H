# Introduction

Our goal is to create a tool that can be used to pull create word clouds of most used words from various news sites to be used for sentiment analysis. For this, we use the Natural Language Toolkit provided by the Python programming language.

The process of analyzing the word use of a news source is broken into the following steps

1. We are provided a list of internet links for articles written about the DAPL protests in a tab delimited text file with the date posted and link.
2. We read the links into a Python List; with each element being a tuple of posted date and link
3. For each element in the link, we read the web page source code. Depending on the source (i.e. NYT, Breitbart, Slate, etc…) we have a different method of pulling and parsing the article language
4. The parsed language  is then tokenized into the word stems which are then saved into a master stem list for the current source
5. With this list of words, we create a frequency distribution that counts the use of word stems across articles for the source.
6. With this list of word stems and counts we create a word cloud visualization
 
The goal of this tool is to give Humanities professionals the ability to pass ANY list of URLS (for supported news sources) and to get back a frequency distribution of the words used and a word cloud that can be used for analysis



# Installation

The tool requires the installation of python library wordcloud, NLTK, matplotlib and bs4. For wordcloud, you can either install by downloading the source code from https://github.com/amueller/word_cloud or install through pip. Detailed installation guide can be found with above link from wordcloud github page.


# Limitation

When developing the tool, we encountered 403 error that occurred when using some links from most of the provided URLs. While working on the solutions, we figured how to solve the error by using requests object. The solution works for most of the URLs except some links from washington post. Currently only 16/112 URLs cannot be processed with the tool. It seems some links from washington post are being very "persistent" thus won't be correctly handled via the current solution and can be optimized in the future work.
