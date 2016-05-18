# encoding=utf-8
__author__ = 'igorpetrovski'




from cPickle import Unpickler



# gets the weigths and a news post and returns estimated category for the news post
def classify_news_post(weights, news_post):
    dict_tf_idf = news_post.dict_tf_idf

    resCat = {}
    for cat in weights:
        res = 0
        for w in dict_tf_idf:
            if w in weights[cat]:
                res+=dict_tf_idf[w]*weights[cat][w]
        resCat[cat] = res


    toRet = "MAKEDONIJA"
    maxValue = resCat["MAKEDONIJA"]

    for k,v in resCat.items():
        if v>maxValue:
            toRet = k
            maxValue = v


    return toRet



#=======================================================================================================================


# gets list of news posts and return dictionary where the key is specific category and the value is list from news
# posts in that category
def classify_posts(posts):
    dicToRet = {}

    print "loading weights"
    toRead = open("estimated_weights.txt",'rb')
    weights = Unpickler(toRead).load()
    toRead.close()

    for post in posts:
        estimated_cat = classify_news_post(weights,post)
        if estimated_cat not in dicToRet:
            dicToRet[estimated_cat]=[]
        dicToRet[estimated_cat].append(post)


    return dicToRet

