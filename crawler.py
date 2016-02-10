#encoding=utf-8
import  logging
from urllib2 import urlopen
from cPickle import Unpickler

from bs4 import BeautifulSoup
from model.NewsPost import NewsPost
import Utility
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


sources = ['http://vecer.mk/rss.xml',                           #0
           'http://www.crnobelo.com/?format=feed&type=rss',     #1
           'http://sitel.mk/rss.xml',                           #2,
           'http://kurir.mk/feed/',                             #3
           'http://republika.mk/?feed=rss2',                    #4
           'http://plusinfo.mk/rss/biznis',                     #5
           'http://plusinfo.mk/rss/skopje',                     #6
           'http://plusinfo.mk/rss/kultura',                    #7
           'http://plusinfo.mk/rss/biznis',                     #8
           'http://plusinfo.mk/rss/zdravje',                    #9
           'http://plusinfo.mk/rss/svet',                       #10
           'http://plusinfo.mk/rss/scena',                      #11
          # 'http://novatv.mk/rss.xml?tip=2',                    #12
          # 'http://novatv.mk/rss.xml?tip=5',                    #13
          # 'http://novatv.mk/rss.xml?tip=7',                    #14
         #  'http://novatv.mk/rss.xml?tip=23',                   #15
           'http://www.vest.mk/rssGenerator/',                  #16
           'http://alsat.mk/RssFeed',                           #17
           'http://www.mkd.mk/feed',                            #18
           'http://www.sport.com.mk/rssgenerator/rss.aspx',     #19
           'http://www.dnevnik.mk/rssGenerator/',               #20
           'http://interesno.com.mk/index.php?format=feed&type=rss' ] #21

p_boundaries = {'http://vecer.mk/rss.xml':[0,-3],
                'http://www.crnobelo.com/?format=feed&type=rss': [0,-2],
                'http://novatv.mk/rss.xml?tip=2'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=5'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=7'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=23'   :[2,-2],
                'http://alsat.mk/RssFeed'           :[0,-1],
                'http://www.vest.mk/rssGenerator/'  :[0,-7],
                'http://alsat.mk/RssFeed'           :[1,-3],
                'http://www.mkd.mk/feed':[0,-4],
                'http://www.sport.com.mk/rssgenerator/rss.aspx': [1]}


sources_config = {#'http://kurir.mk/feed/': [-1],
                  #'http://press24.mk/taxonomy/term/7/feed': [-1],
                  #'http://press24.mk/taxonomy/term/3/feed': [-1],
                  #'http://novatv.mk/rss': [0],
                  #'http://puls24.mk/rss-feed': [0,0],
                  #'http://vecer.mk/rss.xml': [-1],
                  #'http://www.telegraf.mk/telegrafrss': [-1,-1]
                  }
def filterTitles(words, source):

    if source not in sources_config:
        return words

    for index in sources_config[source]:
        del words[index]

    return words


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
                title   = item.find('title').string
                linkUrl = item.find('link').string
                print 'processing ', linkUrl

                linkContent = urlopen(linkUrl).read()

                innerSoup = BeautifulSoup(linkContent)
                feedback += 'trying to read the title ..\n'

                feedback += 'read the title!\n'
                #logging.debug('item title %s' % title)



                titleWords = Utility.getWords(title)

                titleWords = filterTitles(titleWords, web_page_url)

                newTitle = ' '.join(titleWords)

                # add title twice
                totalWords = titleWords
                totalWords.extend(titleWords)
                dictNews = {}

                start = 0
                end = len(innerSoup.findAll('p'))

                if web_page_url in p_boundaries:
                    start =  p_boundaries[web_page_url][0]
                    if len(p_boundaries[web_page_url]) > 1:
                        end = p_boundaries[web_page_url][1]

                for p in innerSoup.findAll('p')[start:end]:
                    words = Utility.getWords(p.text)

                    if words != None and len(words) > 0:
                        totalWords.extend(words)

                numWords = len(totalWords)
                feedback += 'numWords: %d\n' % numWords
                for word in totalWords:
                    dictNews[word] = 1 + dictNews.get(word, 0)

                # OBAVEZNO DA SE OPFATI SLUCAJOT KADE SE ZEMAAT VO PREDVID DUPLIKATI !!!

                howMuch = NewsPost.query(NewsPost.url == linkUrl).fetch()

                if howMuch is None:
                    feedback += 'howMuch is none\n'
                else:
                    feedback += 'howMuch is NOT none\n'


                if howMuch is not None and len(howMuch) > 0:
                    continue

                feedback += 'item title %s\n' % title
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

        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception message: %s\n' % inst.message

        return [], feedback


def crawlThem(start, end):

    end = min(end, len(sources))

    logging.debug('start: %d end: %d' % (start, end))

    fileToRead = open('dict_idf')
    dictIDF = Unpickler(fileToRead).load()
    fileToRead.close()

    str = ''
    newsPosts = []

    for source in sources[start:end]:
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


















