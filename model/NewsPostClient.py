#encoding=utf-8

from google.appengine.ext import ndb
from model import Source

class NewsPostClient(ndb.Model):

    url = ndb.StringProperty()
    host_page = ndb.StringProperty()
    title = ndb.StringProperty()
    numWords = ndb.IntegerProperty()

    source_id = ndb.IntegerProperty()
    source_url = ndb.StringProperty()

    img_url = ndb.StringProperty()


    def serialize(self):
        return {
            "url":          self.url,
            "host_page":    self.host_page,
            "title":        self.title,
            "source_id":    self.source_id,
            "source_url":   self.source_url,
            "img_url":      self.img_url,
        }


