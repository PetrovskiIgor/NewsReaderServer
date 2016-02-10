#encoding=utf-8

from google.appengine.ext import ndb
import math
import json
import unicodedata
class NewsPostClient(ndb.Model):

    url = ndb.StringProperty()
    host_page = ndb.StringProperty()
    title = ndb.StringProperty()
    numWords = ndb.IntegerProperty()


    def serialize(self):
        return {
            "url":          self.url,
            "host_page":    self.host_page,
            "title":        self.title
        }


