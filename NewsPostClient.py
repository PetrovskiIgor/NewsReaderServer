#encoding=utf-8

from google.appengine.ext import ndb
import math

class NewsPostClient(ndb.Model):

    url = ndb.StringProperty()
    host_page = ndb.StringProperty()
    title = ndb.StringProperty()
    numWords = ndb.IntegerProperty()


