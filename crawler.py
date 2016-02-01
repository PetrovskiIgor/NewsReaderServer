#encoding=utf-8
import  logging
from bs4 import BeautifulSoup
from urllib2 import urlopen
from NewsPost import NewsPost
import Utility
from cPickle import Unpickler
from cPickle import Pickler
from google.appengine.ext import ndb

# rss-feeds:

# http://vecer.mk/rss.xml
# http://puls24.mk/rss-feed
# http://www.crnobelo.com/?format=feed&type=rss
# http://sitel.mk/rss.xml
# http://www.telegraf.mk/telegrafrss


sources = ['http://vecer.mk/rss.xml', 'http://puls24.mk/rss-feed', 'http://www.crnobelo.com/?format=feed&type=rss',
           'http://sitel.mk/rss.xml', 'http://www.telegraf.mk/telegrafrss']







def getNewsPosts(web_page_url):

    c = urlopen(web_page_url)
    content = c.read()
    soup = BeautifulSoup(content)
    logging.debug('instantiated beautiful soup')
    newsPosts = []

    for item in soup.findAll('item'):


        linkUrl = item.find('link').string
        print 'processing ', linkUrl



        linkContent = urlopen(linkUrl).read()

        innerSoup = BeautifulSoup(linkContent)

        title = innerSoup.find('title').text

        logging.debug('item title %s' % title)

        totalWords = Utility.getWords(' '.join([title, title]))

        dictNews = {}


        for p in innerSoup.findAll('p'):
            words = Utility.getWords(p.text)

            if words != None and len(words) > 0:
                totalWords.extend(words)


        numWords = len(totalWords)
        for word in totalWords:
            dictNews[word] = 1 + dictNews.get(word, 0)

        # dictNews, title, link, host_page

        newsPost = NewsPost(parent=ndb.Key('NewsPost', web_page_url or "*notitle*"), url = linkUrl,host_page = web_page_url,
                            title = title, dictWords = dictNews, numWords = numWords)

        newsPosts.append(newsPost)




    return newsPosts


def crawlThem():

    newsPosts = getNewsPosts(sources[0])

    fileToRead = open('dict_idf')
    dictIDF = Unpickler(fileToRead).load()
    fileToRead.close()


    for np in newsPosts:
        np.calculate_tf_idf(dictIDF)
        np.put()

    #fileToWrite = open('listNewsPosts', 'w')
    #Pickler(fileToWrite).dump(newsPosts)
    #fileToWrite.close()


# da se prochita od datastore..

def takeNewsPosts():

   # ancestor_key = ndb.Key('NewsPost','*notitle*')


    return NewsPost.query()










