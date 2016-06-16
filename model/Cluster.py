
#model class that represents the cluster that is being sent to the user

from google.appengine.ext import ndb


class Cluster(ndb.Model):
    #the category where this cluster belongs
    category = ndb.StringProperty()
    #the list of news that form the cluster
    listNews = ndb.PickleProperty()
    #vector of words that represents this cluster
    vec = ndb.PickleProperty()




    def serialize(self):
        return {
            "category": self.category,
            "listNews": [news.serialize() for news in self.listNews],
        }