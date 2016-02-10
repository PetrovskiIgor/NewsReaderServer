
from google.appengine.ext import ndb

class Source(ndb.Model):

    def __init__(self, id, url, links):

        self.id = id
        self.url = url
        self.links = links


    def serialize(self):
        return {
            'id':   self.id,
            'url':  self.url,

        }
