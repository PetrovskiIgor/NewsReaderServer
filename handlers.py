from flask import Flask
from flask import Request
from flask import  Response




import crawler
import classification
import clustering
app = Flask(__name__)
# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.
import  naivebayes_classification
import  test_classifications
from cPickle import Unpickler
from Cluster import Cluster

from flask import request
from NewsPostClient import  NewsPostClient

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/crawl_me_some_pages')
def crawl():
    res = crawler.crawlThem()

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

            str += '^^^ CLUSTER CATEGORY: %s\n' % maxCat

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











