# encoding=utf-8
__author__ = 'Petre'


# !!!! PETRE'S CLASSIFICATION !!!!

import anydbm
import cPickle
from math import log10
from math import sqrt
from cPickle import Pickler
from cPickle import Unpickler
from random import random
from math import exp
import time
import Utility


#=======================================================================================================================
# This part is for building the classifcatior and it has to be called on local machine


path = '/Users/igorpetrovski/Desktop/NEURAL_WEIGHTS'



# ======================================================================================================================


def extract(line):
    out = []
    word = []

    for c in line:
        if c.isalpha():
            word.append(c)
            continue
        else:
            if word:
                ww = "".join(word)
                ww=ww.lower()
                if ww not in Utility.stopWords:
                    out.append(ww)
            word = []
    if word:
        ww = "".join(word)
        ww=ww.lower()
        if ww not in Utility.stopWords:
            out.append(ww)

    return out


# ======================================================================================================================



def getWordCounts():
    docFile = open(path+"/data.txt")
    wCounts = {}
    print "presmetuvame frekfencija na zborovi"
    i=0
    for line in docFile:

        if i%10000==0: print i
        i+=1

        line = line.decode("utf-8")
        line = line.strip()
        if line:
            cat,doc = line.split("\t")
            words = extract(doc)
            for w in words:
                if w not in wCounts: wCounts[w]=0
                wCounts[w]=wCounts[w]+1

    docFile.close()
    lessThanFive = set()
    for w,c in wCounts.items():
        if c<=5:
            lessThanFive.add(w)

    toWrite = open(path+"/lessFrequentWords.txt",'w')
    Pickler(toWrite).dump(lessThanFive)
    toWrite.close()


# ======================================================================================================================


def filterDocuments():
    docFile = open(path+"/data.txt")
    toWrite = open(path+"/filteredData.txt", 'w')

    lessThanFive = Unpickler(open(path+"/lessFrequentWords.txt")).load()

    i=0
    for line in docFile:
        if i%10000==0: print i
        i+=1

        line = line.decode("utf-8")
        line = line.strip()
        if line:
            cat,doc = line.split("\t")
            words = extract(doc)
            filtered = []
            for w in words:
                if w not in lessThanFive:
                    filtered.append(w.encode("utf-8"))

            toWrite.write(cat.encode("utf-8")+"\t"+(" ".join(filtered)))
            toWrite.write("\n")


    docFile.close()
    toWrite.close()


# ======================================================================================================================


def create_anydbm():
    docID = 0
    print "creating anydbm"
    f = anydbm.open(path + '/dataset.anydbm', 'c')
    docCat = anydbm.open(path+"/docIDvsCategory.anydbm",'c')

    for line in open(path + '/filteredData.txt'):

        if (docID%10000==0): print docID

        line = line.strip().split('\t')
        if (len(line)<2) :
            #print "ne treba da se sluchi"
            continue
        f[str(docID)] = line[1]
        docCat[str(docID)]=line[0]
        docID += 1
    f.close()
    docCat.close()


# ======================================================================================================================


def calculate_tf():
    N = 272700
    f = anydbm.open(path + '/dataset.anydbm')
    tf = anydbm.open(path+"/TFs.anydbm",'c')

    print "calculating tf"
    for i in range(N):
        if (i%10000==0): print i
        frequences = {}
        doc = f[str(i)]
        doc = doc.decode('utf-8')
        words = doc.split(" ")
        for w in words:
            if w not in frequences: frequences[w]=1
            else: frequences[w]=frequences[w]+1

        for key in frequences:
            frequences[key]=1+log10(frequences[key])

        tf[str(i)]=cPickle.dumps(frequences,2)

    f.close()
    tf.close()


# ======================================================================================================================


def calculate_idf():
    N = 272700
    dfs = {}
    print "calculating idf"
    f = anydbm.open(path + '/dataset.anydbm','c')

    for i in range(N):

        if i%10000==0: print i


        doc = f[str(i)]
        doc = doc.decode('utf-8')
        words = doc.split(" ")
        words = list(set(words))
        for w in words:
            if w not in dfs:
                dfs[w]=0
            dfs[w]=dfs[w]+1

    f.close()

    idf = {}
    i=0
    for w in dfs:
        idf[w]=log10(float(N)/float(dfs[w]))
        if i%5000==0: print "calculating ",i
        i+=1

    idf_f = anydbm.open(path+"/idfs.anydbm",'c')
    for w,c in idf.items():
        idf_f[str(w.encode("utf-8"))]=str(c)
    idf_f.close()


# ======================================================================================================================


def calculate_tf_idf():
    N = 272700
    print "calucalting tf-idf"
    tf = anydbm.open(path+"/TFs.anydbm",'c')
    idf = anydbm.open(path+"/idfs.anydbm",'c')

    idf_dic = {}
    for w in idf:
        idf_dic[w.decode("utf-8")]=float(idf[w])

    print len(idf_dic)
    tf_idf = anydbm.open(path+"/TF_IDF.anydbm",'c')
    for i in range(N):

        if (i%5000==0):
            print i
        i+=1

        tf_dic = cPickle.loads(tf[str(i)])

        res = {}
        vec_module=0
        for w,sc in tf_dic.items():
            res[w]=sc*idf_dic[w]
            vec_module+=sc**2

        vec_module=sqrt(float(vec_module))
        for w,sc in res.items():
            res[w]=float(sc)/float(vec_module)

        tf_idf[str(i)]=cPickle.dumps(res,2)


# ======================================================================================================================


def toExponent(resCat):
    toRet = {}
    for cat,r in resCat.items():
        if r<-30:
            toRet[cat]=0
        elif r>30:
            toRet[cat]=100000000000000
        else:
            toRet[cat]=exp(r)


    return toRet


# ======================================================================================================================


def sumExp(expVals):
    res = 0
    for cat,r in expVals.items():
        res+=r
    return res


# ======================================================================================================================

# function for building the classificator
def estimate_weights():
    N = 272000
    tf_idf = anydbm.open(path+"/TF_IDF.anydbm")

    docCat = anydbm.open(path+"/docIDvsCategory.anydbm")


    docIdvsCat = {}
    categories = set()

    print " reading id vs cat"
    for i in range(N):
        docIdvsCat[i]=docCat[str(i)]
        categories.add(docIdvsCat[i])
        if i==N: break
        i+=1


    print " reading id vs doc"
    idvsdoc = {}
    for i in range(1,N):
        if random()<=0.2:
            idvsdoc[i-1]=cPickle.loads(tf_idf[str(i)])
        if i==N: break
        if i%10000 ==0 : print i
        i+=1

    print "len of idvsdoc",str(len(idvsdoc))

    print " creating set of words"
    words = set()
    for id,doc in idvsdoc.items():
        for w in doc:
            words.add(w)

    print " creatirng weights matrix"
    weights = {}
    for cat in categories:
        weights[cat]={}
        for w in words:
            weights[cat][w]=random()


    maxIter = 400
    eta = 15


    for t in range(maxIter):
        grad_t = {}
        for cat in categories:
            grad_t[cat]={}
            for w in words:
                grad_t[cat][w]=0

        numErrors = 0
        for i in idvsdoc:
            doc = idvsdoc[i]
            cat = docIdvsCat[i]

            resCat = {}
            for c in categories:
                res = 0
                for w in doc:
                    res+=doc[w]*weights[c][w]
                resCat[c]=res


            exp_vals = toExponent(resCat)
            sumOfExp = sumExp(exp_vals)
            lik = exp_vals[cat]/sumOfExp

            toMul = 1-lik

            for w in doc:
                grad_t[cat][w]+=doc[w]*toMul


            for c in categories:
                if c!=cat:
                    if (exp_vals[c]/sumOfExp) > lik:
                        #print c,str(exp_vals[c]/sumOfExp),"   ",cat,str(lik)
                        numErrors+=1
                        break

        # za moj uvid
        print "iter : "+str(t)+" numErrors : "+str(numErrors)

        for cat,words in weights.items():
            for w in words:
                weights[cat][w]=weights[cat][w]+((1/float(len(idvsdoc)))*eta*grad_t[cat][w])


    toWrite = open(path+"/estimated_weights.txt",'wb')
    Pickler(toWrite).dump(weights)
    toWrite.close()


#=======================================================================================================================

# function for evaluating the classificator
def evaluate_weights():
    N = 272000

    print "loading weights"
    weights = Unpickler(open(path+"/estimated_weights.txt",'rb')).load()


    docCat = anydbm.open(path+"/docIDvsCategory.anydbm")
    docIdvsCat = {}
    categories = set()
    print " reading id vs cat"
    for i in range(N):
        docIdvsCat[i]=docCat[str(i)]
        categories.add(docIdvsCat[i])
        if i==N: break
        i+=1


    tf_idf = anydbm.open(path+"/TF_IDF.anydbm")
    print " reading id vs doc"
    idvsdoc = {}
    for i in range(1,N):
        if random()<=0.1:
            idvsdoc[i-1]=cPickle.loads(tf_idf[str(i)])
        if i==N: break
        if i%10000 ==0 : print i
        i+=1


    print "starting"
    start = time.clock()
    numErrors = 0
    for i in idvsdoc:
        doc = idvsdoc[i]
        cat = docIdvsCat[i]

        resCat = {}
        for c in categories:
            res = 0
            for w in doc:
                if w in weights[c]:
                    res+=doc[w]*weights[c][w]
            resCat[c]=res

        exp_vals = toExponent(resCat)
        sumOfExp = sumExp(exp_vals)
        lik = exp_vals[cat]/sumOfExp

        for c in categories:
            if c!=cat:
                if (exp_vals[c]/sumOfExp) > lik:
                    numErrors+=1
                    break


    print str(numErrors), str(len(idvsdoc)), str(float(numErrors)/float(len(idvsdoc)))

    end = time.clock()
    print "time : ",str(end-start)

# the functions have to be called in this order
#getWordCounts()

#filterDocumtens()

#create_anydbm()

#calculate_tf()

#calculate_idf()


#calculate_tf_idf()


#estimate_weights()


#evaluate_weights()














#=======================================================================================================================
# This part is for news classification




# gets the weigths and a news post and returns estimated category for the news post
def classify_news_post(weights, news_post):
    dict_tf_idf = news_post.dict_tf_idf

    resCat = {}
    for c in weights:
        res = 0
        for w in dict_tf_idf:
            if w in weights[c]:
                res+=dict_tf_idf[w]*weights[c][w]
        resCat[c] = res


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

