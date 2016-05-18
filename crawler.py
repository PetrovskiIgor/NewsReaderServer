#encoding=utf-8
import  logging
from urllib2 import urlopen
from cPickle import Unpickler

from bs4 import BeautifulSoup
from model.NewsPost import NewsPost
import Utility
from google.appengine.ext import ndb


# rss-feeds:

# 1.    http://vecer.mk/rss.xml
# 2.    http://puls24.mk/rss-feed
# 3.    http://www.crnobelo.com/?format=feed&type=rss
# 4.    http://sitel.mk/rss.xml
# 5.    http://www.telegraf.mk/telegrafrss
# 6.    http://www.femina.mk/rss
# 7.    http://kurir.mk/feed/
# 8.    http://press24.mk/taxonomy/term/3/feed
# 9.    http://press24.mk/taxonomy/term/7/feed
# 10.   http://novatv.mk/rss
# 11.
# 12.
# 13.
# 14.
# 15.
# 16.
# 17.
# 18.
# 19.
# 20.





sources_config = {#'http://kurir.mk/feed/': [-1],
                  #'http://press24.mk/taxonomy/term/7/feed': [-1],
                  #'http://press24.mk/taxonomy/term/3/feed': [-1],
                  #'http://novatv.mk/rss': [0],
                  #'http://puls24.mk/rss-feed': [0,0],
                  #'http://vecer.mk/rss.xml': [-1],
                  #'http://www.telegraf.mk/telegrafrss': [-1,-1]
                  }

#some sources have a fixed set of content non-related tokens at the beginning/end of each title
#example: (КУРИР: Политичката криза во Македонија ќе биде надмината)
# ^ here we would like to delete the first token that appears in the sentence

def filterTitles(words, source):
    """
    :param words: words in the title that are going to be filtered, if needed
    :param source: the source id of the title
    :return: the filtered words to be returned
    """
    if source not in sources_config:
        return words

    for index in sources_config[source]:
        del words[index]

    return words




def getNewsPosts(source_object, web_page_url, dict_IDF):

    """
    The main function which crawls a particular link and returns news posts as object that have been extracted from that link.
    Needs revising and (possibly) modifying the process of text extraction.

    :param sourceObject: the source object that wraps multiple web_page_urls (we need it for creating the news post object)
    :param web_page_url: the web page url where we extract the information from
    :param dictIDF:     the idf dictionary that we need to calculate tf_idf for a document
    :return: list of news posts and a feedback (for logging)
    """

    #feedback variable for logging
    feedback = ''

    try:
        #opening the url and reading the content
        c = urlopen(web_page_url)
        content = c.read()
        soup = BeautifulSoup(content)

        logging.debug('getNewsPosts: failed on reading web_page_url')


        logging.debug('instantiated beautiful soup')

        #the list of object that we are going to return
        newsPosts = []

        for item in soup.findAll('item'):

            #in each item we have a link to the news that we would like to process

            try:
                #title of the news
                title   = item.find('title').string
                #link to the news
                link_url = item.find('link').string

                feedback += 'title: %s\n' % title
                feedback += 'link_url: %s\n' % link_url

                same_news_posts = NewsPost.query(NewsPost.url == link_url).fetch()


                #we must not process the same news twice
                if same_news_posts is not None and len(same_news_posts) > 0:
                    feedback += 'There is/are already news post/s with this link. Continuing..\n'
                    feedback += '------------------------------\n'
                    continue


                img_url = None

                #we try to fetch the photo url directly from the rss feed, if not possible we will try later again
                if (item.description is not None) and (item.description.string is not None):
                    img_obj = BeautifulSoup(item.description.string).find('img')

                    if img_obj is not None:
                        img_url = img_obj['src']
                elif item.description is not None:
                    img_obj = item.description.find('img')

                    if img_obj is not None:
                        img_url =  img_obj['src']


                #here we get the content of the news
                link_content = urlopen(link_url).read()
                innerSoup = BeautifulSoup(link_content)


                title_words = Utility.getWords(title)
                title_words = filterTitles(title_words, web_page_url)

                total_words = title_words

                # add title twice, because we consider those words in the title twice as important as the other words
                total_words.extend(total_words)


                #which paragraphs to take into consideration
                start = 0
                end = len(innerSoup.findAll('p'))

                if web_page_url in Utility.paragraph_boundaries:
                    start =  Utility.paragraph_boundaries[web_page_url][0]
                    if len(Utility.paragraph_boundaries[web_page_url]) > 1:
                        end = Utility.paragraph_boundaries[web_page_url][1]


                for p in innerSoup.findAll('p')[start:end]:
                    words = Utility.getWords(p.text)

                    if words is not None and len(words) > 0:
                        total_words.extend(words)


                num_words = len(total_words)


                dict_news = {}
                for word in total_words:
                    dict_news[word] = 1 + dict_news.get(word, 0)




                #we are trying to get the image from the news
                if img_url is None:
                    imgs = innerSoup.findAll('img')

                    img_url = ''
                    if imgs is not None and len(imgs) > 0:
                        img_url = imgs[0]['src']

                #deal with the pictures with relative path to the web
                if (img_url is not None) and (len(img_url) > 0):
                    if img_url.find(source_object.url) != 0:
                        img_url = source_object.url + '/' + img_url


                feedback += 'img_url: %s\n' % img_url


                newsPost = NewsPost(parent=ndb.Key('NewsPost', link_url or "*notitle*"), url = link_url, host_page = web_page_url,
                                    title = title, dictWords = dict_news, numWords = num_words, words = total_words ,
                                    source_id = source_object.id, source_url = source_object.url,
                                    img_url = img_url)

                newsPost.calculate_tf_idf(dict_IDF)
                newsPost.put()
                newsPosts.append(newsPost)

                feedback += '------------------------------\n'
            except Exception as inst:
                feedback += 'Inner Exception type: %s\n' % str(type(inst))
                feedback += 'Inner Exception message: %s\n' % inst.message


        return newsPosts, feedback
    except Exception as inst:

        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception message: %s\n' % inst.message

        #if there is an exception, we return and empty list of news posts
        return [], feedback



def crawl_me_some_news(start=0, end=len(Utility.sources)):

    ### !!!
    ### TREBA DA SE WRAP-IRA ZA SEKOJ LINK DA SE PROBA POVEKJE PATI (MIN 2) DOKOLKU IMA EXCEPTION
    ### !!!

    """
    Crawls some pages and stores them in a database using the function getNewsPosts()
    :param start starting index of the sources of rss feed to crawl:
    :param end   ending index of the sources of rss feed to crawl:
    :return returns a string containing the logs.. are the news posts are stored in the getNewsPosts function:
    """

    logging.debug('start: %d end: %d' % (start, end))

    file_to_read = open('dict_idf')
    dictIDF = Unpickler(file_to_read).load()
    file_to_read.close()

    str = ''
    #newsPosts = []

    num_news_posts = 0
    for sourceObject in Utility.sources[start:end]:

        for source in sourceObject.links:
            newsList, feedback = getNewsPosts(sourceObject, source, dictIDF)
            num_crawled_news = len(newsList)

            if newsList is None or len(newsList) == 0:
                #try again
                str += 'Trying again for source link: %s\n' % source
                newList, feedback = getNewsPosts(sourceObject, source, dictIDF)

            #newsPosts.extend(newList)

            str += feedback
            num_news_posts += len(newsList)



    str += 'number of posts: %d\n' % num_news_posts

    return str


def take_all_news_posts():

    """
    :return returns every news post there is:
    """

    return NewsPost.query().fetch()


















