__author__ = 'Petre'

from math import sqrt
import heapq

from google.appengine.ext import ndb

# ======================================================================================================================


class bicluster:

    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        #left child cluster (in the hierarchical clustering)
        self.left = left
        #right child cluster (in the hierarchical clustering)
        self.right = right
        #the vector of words
        self.vec = vec
        self.id = id
        self.distance = distance
        self.posts = []



# ======================================================================================================================


# utility class for the heap

class cluster_distances:
    def __init__(self,id1,id2,distance):
        self.id1=id1;
        self.id2=id2;
        self.distance=distance;


    def __cmp__(self, other):
        return cmp(self.distance,other.distance)



# ======================================================================================================================


def dotproduct(v1, v2):
    sum = 0
    for word in v1:
        if word in v2:
            sum += v1[word] * v2[word]

    return sum


# ======================================================================================================================

#computing the length of the vector

def module(v1):
    sum = 0
    for word in v1:
        sum += v1[word] * v1[word]

    return sqrt(sum)


# ======================================================================================================================

#computing similarity between two vectors

def simfunc(v1, v2, id1, id2, moduls):

    den = moduls[id1] * moduls[id2]

    if den == 0:
        return 0

    return dotproduct(v1, v2) / den


# ======================================================================================================================

#computing distance between two vectors

def distance(v1, v2, id1, id2, moduls):
    return 1-(simfunc(v1,v2,id1,id2,moduls))


# ======================================================================================================================


def printSet(set):
    for k in set:
        print k


# ======================================================================================================================


def mergevectors(vec1, vec2):
    newVec = {}
    l1 = len(vec1)
    l2 = len(vec2)

    im = l1 + l2

    for zbor, weight in vec1.items():
        if zbor in vec2:
            newVec[zbor] = (l1 * weight + l2 * vec2[zbor]) / im
        else:
            newVec[zbor] = (l1 * weight) / im

    for zbor, weight in vec2.items():
        if zbor not in vec1:
            newVec[zbor] = (l2 * weight) / im

    return newVec



# ======================================================================================================================


# gets list of news_posts and returns list of clusters where each cluster contains set of news_posts (posts)
def cluster_news(news_post):

    innerfeedback = ''
    try:
        currentclustid = -1
        sims = []

        # Clusters are initially just the posts
        clust = []
        i=0;
        inArr = set()

        innerfeedback += 'Assigning one cluster to one newspost..\n'
        for post in news_post:
            c = bicluster(vec=post.dict_tf_idf,id=i)
            c.posts.append(post)
            clust.append(c)

            inArr.add(i)
            i += 1

        innerfeedback += 'Completed the job ^^\n'



        #preprocessing step of calculating the moduls(lengths)  of vectors in the clusters
        moduls = {}

        innerfeedback += 'Preprocessing the modules of the vectors\n'
        numClusters = 0
        for c in clust:
            moduls[c.id] = module(c.vec)
            numClusters += 1

        innerfeedback += 'Completed the job ^^\n'


        innerfeedback += 'Calculating the distances between the clusters\n'
        #calculating between clusters distances
        for i in range(numClusters):
            #print i
            for j in range(i + 1, numClusters):
                value = distance(clust[i].vec, clust[j].vec, clust[i].id, clust[j].id, moduls)
                heapq.heappush(sims, cluster_distances(clust[i].id,clust[j].id,value))

        innerfeedback += 'Completed the job^^\n'


        # creating idVsCluster index map
        idVsCluster = {}
        for i in range(numClusters):
            idVsCluster[clust[i].id]=clust[i];

        print len(sims)

        while len(clust) > 1:
            # print len(clust)
            mostSim = heapq.heappop(sims);
            lowestpair = [mostSim.id1,mostSim.id2];

            if (lowestpair[0] not in inArr or lowestpair[1] not in inArr):
                continue

            print mostSim.distance, mostSim.id1, mostSim.id2

            # calculate the average of the two clusters
            # bidejki imame max heap i prevrteni ni se slichnostite
            if mostSim.distance > 0.6:
                break


            first = idVsCluster[lowestpair[0]]
            second = idVsCluster[lowestpair[1]]

            #creating new cluster
            mergevec = mergevectors(first.vec, second.vec)
            newcluster = bicluster(mergevec, left=first,right=second, distance=mostSim, id=currentclustid)

            #decrementing the id of cluster
            currentclustid -= 1

            #titles for new cluster
            posts = []
            for n in first.posts:
                posts.append(n)

            for n in second.posts:
                posts.append(n)

            newcluster.posts = posts

            #caluculate the module of new cluster
            moduls[newcluster.id] = module(mergevec)

            #deletering clusters that has been merged
            clust.remove(first)
            inArr.remove(first.id)
            clust.remove(second)
            inArr.remove(second.id)

            #adding new cluster in list of clusters
            clust.append(newcluster)
            #adding new cluster in map index
            idVsCluster[newcluster.id]=newcluster;
            #adding the id in list of ids
            inArr.add(newcluster.id)

            #calculating the distance between new cluster and other clusters
            for i in range(len(clust)):
                tekClust = clust[i];
                if (tekClust.id!=newcluster.id):
                    value = distance(tekClust.vec, newcluster.vec, tekClust.id, newcluster.id, moduls)
                    heapq.heappush(sims, cluster_distances(tekClust.id,newcluster.id,value))
    except Exception as inst:
        innerfeedback += 'ClusteringException type: %s\n' % (type(inst))
        innerfeedback += 'ClusteringException: %s\n' % inst.message

    return clust, innerfeedback

