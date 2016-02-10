#encoding=utf-8
import re
import json

from flask import Flask
from flask import  Response

import crawler
import classification
import clustering

app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
import  naivebayes_classification
import  test_classifications
from model.Cluster import Cluster

from flask import request
from model.NewsPostClient import  NewsPostClient
from IDFModel import IDFModel
from flask import redirect
from google.appengine.api import taskqueue

import Utility


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'No te procupas, compadre!'


@app.route('/crawl_me_some_pages')
def crawl():

    start = request.args.get('start')
    end = request.args.get('end')

    if start is None:
        start = 0



    if end is None:
        end = 1000

    start = int(start)
    end = int(end)

    res = crawler.crawlThem(start, end)

    return Response(res, mimetype='text/plain')

@app.route('/get_me_some_links')
def getLinks():


    newsPosts = crawler.takeNewsPosts()
    str = ''
    for np in newsPosts:
        str += np.title + '\n';

        pairs = sorted([(word, np.dict_tf_idf[word]) for word in np.dict_tf_idf], key=lambda x:-x[1])

        for pair in pairs[0:10]:
            str += '%s %f\n' % (pair[0], pair[1])

        str += '\n'

    return Response(str, mimetype='text/plain')


@app.route('/get_clusters')
def getClusters():
    feedback = ''
    str = ''
    try:
        newsPosts = crawler.takeNewsPosts()


        # utility dicts for majority voting with nb

        fileToRead = open(naivebayes_classification.str_dict_word_in_cat)
        dict_words = Unpickler(fileToRead).load()
        fileToRead.close()

        fileToRead = open(naivebayes_classification.str_dict_cat_count)
        dict_cats = Unpickler(fileToRead).load()
        fileToRead.close()

        fileToRead = open(naivebayes_classification.str_dict_priors)
        dict_priors = Unpickler(fileToRead).load()
        fileToRead.close()

        feedback += 'took the newsposts \n'



        #return Response('%d' % counter, mimetype='text/plain')
        clusters, innerfeedback = clustering.cluster_news(newsPosts)

        feedback += '%s\n' % innerfeedback

        feedback += 'done the clustering\n'
        i = 0
        for c in clusters:
            newsInCluster = c.posts


            str += 'cluster %d\n' % i

            #implementing the majority voting

            votes_cat = {}

            for np in newsInCluster:
                str += ' \t %s\n' % np.title
                category = test_classifications.get_NB_category(np.words,dict_words, dict_cats, dict_priors)
                votes_cat[category] = 1 + votes_cat.get(category, 0)

            maxVotes = 0
            maxCat = ''

            for cat in votes_cat:
                if votes_cat[cat] > maxVotes:
                    maxVotes = votes_cat[cat]
                    maxCat = cat

            str += '^^^ CLUSTER CATEGORY: %s with maxVotes: %d\n' % (maxCat, maxVotes)

            listNews = []
            for np in  c.posts:
                newNews = NewsPostClient(url = np.url, host_page = np.host_page, title = np.title, numWords = np.numWords)
                listNews.append(newNews)

            newCluster = Cluster(category = maxCat, listNews = listNews)
            newCluster.put()
            
            str += '\n'

            i += 1

        str += feedback
    except Exception as inst:
        feedback += 'Exception type: %s\n' % (type(inst))
        feedback += 'Exception: %s\n' % (inst.message)

    str += feedback
    return Response(str, mimetype='text/plain')

@app.route('/get_categories')
def getCategories():

    newsPosts = crawler.takeNewsPosts()

    categories = classification.classify_posts(newsPosts)
    #str = ''
    #for cat in categories:
    #    str += '%s\n' % cat
    #
    #    for newsPost in categories[cat]:
    #       str += '\t%s\n' % newsPost.title
    #
    #    str += '\n'

    str = '%d\n' % len(categories)

    for cat in categories:
        str += '%s %d\n' % (cat, len(categories[cat]))


    for cat in categories:
        str += '%s\n' % cat

        for np in categories[cat]:
            str += '\t%s\n' % np.title

        str += '\n'

    return Response(str, mimetype='text/plain')


@app.route('/getNewsPosts')
def getNewsPosts():

    newsPosts = crawler.takeNewsPosts()

    str = ''
    i = 0
    for np in newsPosts:
        str += '%d: %s\n' % (i , np.title)
        i += 1


    return Response(str, mimetype='text/plain')



@app.route('/get_classification_naivebayes')
def getCategoriesNB():

    response = ''
    feedback = ''
    try:
        newsPosts = crawler.takeNewsPosts()


        fileToRead = open(naivebayes_classification.str_dict_word_in_cat)
        dict_words = Unpickler(fileToRead).load()
        fileToRead.close()

        fileToRead = open(naivebayes_classification.str_dict_cat_count)
        dict_cats = Unpickler(fileToRead).load()
        fileToRead.close()

        fileToRead = open(naivebayes_classification.str_dict_priors)
        dict_priors = Unpickler(fileToRead).load()
        fileToRead.close()


        dict_results = {}

        for np in newsPosts:
            #words, dict_words, dict_cats, dict_priors
            category = test_classifications.get_NB_category(np.words, dict_words, dict_cats, dict_priors)

            dict_results.setdefault(category, [])
            dict_results[category].append(np)

        response += 'number of documents: %d\n' % (len(newsPosts))
        for cat in dict_results:
            response += '%s\t\t%d\n' % (cat, len(dict_results.get(cat, [])))

        for cat in dict_results:
            response += '%s\n' % cat
            for np in dict_results[cat]:
                response += '\t%s\n' % np.title
            response += '\n'


    except Exception as inst:
        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception: %s\n' % inst.message

    response += feedback
    return Response(response, mimetype='text/plain')


@app.route('/get_clusters_with_cat')
def  getClustersWithCat():
    feedback = ''
    str = ''
    try:
        category = request.args.get('category')

        str += 'got parameter category: %s\n' % category
        clusters = Cluster.query(Cluster.category == category).fetch()
        str += 'fetched the clusters'
        str = ''
        i = 1
        for c in clusters:
            str += 'cluster %d:\n' % i
            str += 'category: %s\n' % c.category


            for np in c.listNews:
                str += '\t%s\n' % np.title


            str += '\n'


            i+= 1

    except Exception as inst:
            feedback += 'Exception type: %s\n' % type(inst)
            feedback += 'Exception: %s\n' % inst.message

    str += feedback

    return Response(str, mimetype='text/plain')


@app.route('/insert_dict_idf_to_task')
def insertDICTIDF_task():
    str = ''
    feedback = ''
    try:
        logging.debug('Trying to load the dictionary for idf..')
        fileToRead = open('dict_idf')
        dictIDF = Unpickler(fileToRead).load()
        fileToRead.close()

        logging.debug('Loaded the dictionary for idf!')

        logging.debug('Inserting words')
        counter = 0
        for word in dictIDF:
            key = ndb.Key('IDFModel', word)

            newPair = IDFModel(parent = key, word = word, value = dictIDF[word])
            newPair.put()

            counter += 1

            if counter % 1000:
                logging.debug('Inserted %d words' % counter)



        logging.debug('Wuhu! Inserted all the words.')
        str += 'Inserted %d words for IDF\n' % counter
    except Exception as inst:
        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception message: %s\n' % inst.message

        logging.debug(feedback)

    str += feedback
    return Response(str, mimetype='text/plain')


@app.route('/insert_dict_idf')
def insertDictIDF():
    taskqueue.add(url='/insert_dict_idf_to_task')
    return redirect("/", code=302)


@app.route('/get_idf_value')
def getIDFValue():

    str = ''
    word = request.args.get('zbor')

    rows = IDFModel.query(IDFModel.word == word).fetch()

    if rows is not None and len(rows) > 0:
        str += 'IDF value for word %s is %f\n' % (word, rows[0].value)
    else:
        str += 'No IDF Value for word %s\n' % word

    return Response(str, mimetype='text/plain')


@app.route('/get_my_clusters')
def getMYClusters():
    category = request.args.get('category')

    clusters = Cluster.query(Cluster.category == category).fetch()

    obj = {'listClusters' : [c.serialize() for c in clusters]}

    result = json.dumps(obj, ensure_ascii=True)

    return Response(result, mimetype='text/plain')


@app.route('/get_my_news')
def getMYNews():
    category = request.args.get('category')
    news = NewsPost.query().fetch()
    clusters = Cluster.query(Cluster.category == category).fetch()

    newNews = []

    for n in news:
        newObject = NewsPostClient(url = n.url,host_page = n.host_page,title = n.title)
        newNews.append(newObject)


    #result = str(byteify(newNews[0].serialize()))

    result = ''


    return Response(result, mimetype='application/javascript')


def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input


@app.route('/get_clusters_server')
def getClustersServer():

    category = request.args.get('category')

    clusters = Cluster.query(Cluster.category == category).fetch()
    str = ''
    if clusters is None:
        str = 'None clusters :/'
    else:
        i = 1
        for c in clusters:
            str += 'Cluster %d\n' % i

            for np in c.listNews:
                str += '\t%s\n' % np.title

            i += 1


    return Response(str, mimetype='text/plain')



@app.route('/get_news_from_source')
def getNewsFromSource():
    source = request.args.get('source')
    s = ''
    newsPosts = NewsPost.query(NewsPost.host_page == source).fetch()

    for np in newsPosts:
        s+= '%s\n' % np.title


    return Response(s, mimetype='text/plain')

import  logging
from bs4 import BeautifulSoup
from urllib2 import urlopen
from model.NewsPost import NewsPost
from cPickle import Unpickler
from google.appengine.ext import ndb


@app.route('/crawl_content')
def crawlContent():
    web_page_url = request.args.get('source')
    str = ''
    feedback = ''
    try:
        str += 'Trying to open the url..'
        c = urlopen(web_page_url)
        content = c.read()
        soup = BeautifulSoup(content)

        str += 'Opened the url!'
        logging.debug('getNewsPosts: failed on reading web_page_url')


        logging.debug('instantiated beautiful soup')
        newsPosts = []
        feedback += 'in it\n'
        for item in soup.findAll('item'):

            try:
                title   = item.find('title').string

                str += 'title: %s\n' % title

                content = item.find('content:encoded')

                if content is not None:
                    str += 'content:\n'

                    for p in content.findAll('p'):
                        str += '%s\n' % p.text
                else:
                    str += 'No content. Fuck you\n'




            except Exception as inst:
                feedback += 'Inner Exception type: %s\n' % str(type(inst))
                feedback += 'Inner Exception message: %s\n' % inst.message


    except Exception as inst:

        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception message: %s\n' % inst.message



    str += feedback

    return Response(str, mimetype='text/plain')



p_boundaries = {'http://vecer.mk/rss.xml':[0,-3],
                'http://www.crnobelo.com/?format=feed&type=rss': [0,-2],
                'http://novatv.mk/rss.xml?tip=2':[2,-2],
                'http://novatv.mk/rss.xml?tip=5':[2,-2],
                'http://novatv.mk/rss.xml?tip=7':[2,-2],
                'http://novatv.mk/rss.xml?tip=23':[2,-2]}

@app.route('/check_words')
def checkWords():


    web_page_url = request.args.get('source')

    str = ''
    feedback = ''
    try:
        c = urlopen(web_page_url)
        content = c.read()
        soup = BeautifulSoup(content)

        feedback += 'in it\n'
        counter = 0
        for item in soup.findAll('item'):

            try:
                title  = item.find('title').string

                str += 'TITLE: %s\n' % title
                str += 'CONTENT:\n'

                content = item.find('content')

                #if content is not None:
                #    str += 'IMA GOTOV BRALE\n'
                #    str += '%s\n' % content.text

                #else:
                linkUrl = item.find('link').string
                linkContent = urlopen(linkUrl).read()
                innerSoup = BeautifulSoup(linkContent)

                feedback += 'setting start and end..\n'
                start = 0
                end = len(innerSoup.findAll('p'))
                feedback += 'Set start & end!\n'

                if web_page_url in crawler.p_boundaries:
                    start =  crawler.p_boundaries[web_page_url][0]

                    if len(crawler.p_boundaries[web_page_url]) > 1:
                        end = crawler.p_boundaries[web_page_url][1]

                for p in innerSoup.findAll('p')[start:end]:
                    str +='%s\n' % p.text

                str += '\n'
            except Exception as inst:
                feedback += 'Inner Exception type: %s\n' % str(type(inst))
                feedback += 'Inner Exception message: %s\n' % inst.message

            counter += 1
            if counter > 4: break

    except Exception as inst:

        feedback += 'Exception type: %s\n' % type(inst)
        feedback += 'Exception message: %s\n' % inst.message


    str += feedback

    return Response(str, mimetype='text/plain')


def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True



@app.route('/prepare_for_clustering')
def prepareClustering():
    logging.debug('preparing for refreshing..')
    ndb.delete_multi(Cluster.query().fetch(keys_only=True))

    getClusters()
    logging.debug('refreshed!')

    return ''


@app.route('/get_sources')
def getSources():

    sources = [source.serialize() for source in Utility.sources]


    return Response(str(sources), mimetype='application/javascript')
