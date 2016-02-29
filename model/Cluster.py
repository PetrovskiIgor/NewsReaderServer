
#model class that represents the cluster that is being sent to the user

from google.appengine.ext import ndb
import handlers
class Cluster(ndb.Model):
    category = ndb.StringProperty() #the category where this cluster belongs
    listNews = ndb.PickleProperty() #the list of news that form the cluster
    vec = ndb.PickleProperty()      #vector of words that represents this cluster




    def serialize(self):
        return {
            "category": self.category,
            "listNews": [news.serialize() for news in self.listNews],
        }