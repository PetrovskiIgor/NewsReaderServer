
from google.appengine.ext import ndb

class Cluster(ndb.Model):
    category = ndb.StringProperty()
    listNews = ndb.PickleProperty()

    @classmethod
    def query_cluster(cls, ancestor_key):
        return cls.query().filter(ancestor = ancestor_key).fetch()