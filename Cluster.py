
from google.appengine.ext import ndb

class Cluster(ndb.Model):
    category = ndb.StringProperty()
    listNews = ndb.PickleProperty()