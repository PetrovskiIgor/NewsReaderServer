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
# http://www.femina.mk/rss
# http://kurir.mk/feed/
# http://press24.mk/taxonomy/term/3/feed
# http://press24.mk/taxonomy/term/7/feed
# http://novatv.mk/rss


sources = ['http://vecer.mk/rss.xml', 'http://puls24.mk/rss-feed', 'http://www.crnobelo.com/?format=feed&type=rss',
           'http://sitel.mk/rss.xml', 'http://www.telegraf.mk/telegrafrss', 'http://www.femina.mk/rss',
           'http://kurir.mk/feed/', 'http://novatv.mk/rss', 'http://press24.mk/taxonomy/term/3/feed',
           'http://press24.mk/taxonomy/term/7/feed']





def getNewsPosts(web_page_url, dictIDF):

    feedback = ''
    try:
        c = urlopen(web_page_url)
        content = c.read()
        soup = BeautifulSoup(content)

        logging.debug('getNewsPosts: failed on reading web_page_url')


        logging.debug('instantiated beautiful soup')
        newsPosts = []
        feedback += 'in it\n'
        for item in soup.findAll('item'):

            try:
                linkUrl = item.find('link').string
                print 'processing ', linkUrl

                linkContent = urlopen(linkUrl).read()

                innerSoup = BeautifulSoup(linkContent)

                title = innerSoup.find('title').text

                logging.debug('item title %s' % title)

                feedback += 'item title %s\n' % title

                totalWords = [] #Utility.getWords(' '.join([title, title]))

                dictNews = {}


                for p in innerSoup.findAll('p'):
                    words = Utility.getWords(p.text)

                    if words != None and len(words) > 0:
                        totalWords.extend(words)

                numWords = len(totalWords)
                feedback += 'numWords: %d\n' % numWords
                for word in totalWords:
                    dictNews[word] = 1 + dictNews.get(word, 0)

                # OBAVEZNO DA SE OPFATI SLUCAJOT KADE SE ZEMAAT VO PREDVID DUPLIKATI !!!

                #feedback += 'getting the key.. \n'
                #prevent from adding duplicates
                #myKey = ndb.Key('NewsPost', linkUrl)

               # howMuch = NewsPost.query(myKey)

                #if howMuch is None:
                #    feedback += 'howMuch is none\n'
                #else:
                #    feedback += 'howMuch is NOT none\n'


                #if howMuch is not None and len(howMuch) > 0:
                #    continue


                 # dictNews, title, link, host_page
                newsPost = NewsPost(parent=ndb.Key('NewsPost', linkUrl or "*notitle*"), url = linkUrl,host_page = web_page_url,
                                    title = title, dictWords = dictNews, numWords = numWords, words = totalWords)
                newsPost.calculate_tf_idf(dictIDF)
                newsPost.put()
                newsPosts.append(newsPost)
            except Exception as inst:
                feedback += 'Inner Exception type: %s\n' % str(type(inst))
                feedback += 'Inner Exception message: %s\n' % inst.message


        return newsPosts, feedback
    except Exception as inst:

        feedback += 'Exception type: %s\n' % str(type(inst))
        feedback += 'Exception message: %s\n' % inst.message

        return [], feedback


def crawlThem():

    fileToRead = open('dict_idf')
    dictIDF = Unpickler(fileToRead).load()
    fileToRead.close()

    str = ''
    newsPosts = []

    for source in sources[0:1]:
        newList, feedback = getNewsPosts(source, dictIDF)
        newsPosts.extend(newList)
        str += feedback


    str += 'number of posts: %d\n' % len(newsPosts)




    for np in newsPosts:
        np.calculate_tf_idf(dictIDF)
        #np.put()

    #fileToWrite = open('listNewsPosts', 'w')
    #Pickler(fileToWrite).dump(newsPosts)
    #fileToWrite.close()

    return str


# da se prochita od datastore..

def takeNewsPosts():

   # ancestor_key = ndb.Key('NewsPost','*notitle*')


    return NewsPost.query().fetch()













