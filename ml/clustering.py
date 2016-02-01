__author__ = 'Petre'

from math import sqrt
import heapq



# ======================================================================================================================


class bicluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        self.left = left
        self.right = right
        self.vec = vec
        self.id = id
        self.distance = distance
        self.posts = set()



# ======================================================================================================================



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
    for zbor in v1:
        if zbor in v2:
            sum += v1[zbor] * v2[zbor]

    return sum


# ======================================================================================================================


def module(v1):
    sum = 0
    for zbor, weight in v1.items():
        sum += weight * weight

    return sqrt(sum)


# ======================================================================================================================


def simfunc(v1, v2, id1, id2, moduls):
    return (dotproduct(v1, v2) / (moduls[id1] * moduls[id2]))


# ======================================================================================================================


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


# gets list of news_posts and return list of clusters where each cluster contains set of news_posts (posts)
def cluster_news(news_post):
    print len(news_post)

    currentclustid = -1
    sims = []

    # Clusters are initially just the posts
    clust = []
    i=0;
    inArr = set()
    for post in news_post:
        c = bicluster(vec=post.dict_tf_idf,id=i)
        c.posts.add(post)
        clust.append(c)

        inArr.add(i)
        i+=1



    #preprocessing step of calculating the moduls of clusters
    moduls = {}
    for c in clust:
        moduls[c.id] = module(c.vec)


    #calculating between clusters distances
    for i in range(len(clust)):
        #print i
        for j in range(i + 1, len(clust)):
            value = distance(clust[i].vec, clust[j].vec, clust[i].id, clust[j].id, moduls)
            heapq.heappush(sims, cluster_distances(clust[i].id,clust[j].id,value))


    # creating idVsCluster index map
    idVsCluster = {}
    for i in range(len(clust)):
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
        posts = set()
        for n in first.posts:
            posts.add(n)

        for n in second.posts:
            posts.add(n)

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

    return clust

