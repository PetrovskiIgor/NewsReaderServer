
from google.appengine.ext import ndb
import handlers
class Cluster(ndb.Model):
    category = ndb.StringProperty()
    listNews = ndb.PickleProperty()
    vec = ndb.PickleProperty()


    def serialize(self):
        return {
            "category": self.category,
            'listNews': [news.serialize() for news in self.listNews]
        }