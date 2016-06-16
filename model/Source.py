
from google.appengine.ext import ndb

#source class that describes the Source where we extract the news from

class Source(ndb.Model):

    def __init__(self, id, url, links, name=None):

        self.id = id
        self.url = url
        self.links = links

        if name is not None:
            self.name = name


    def serialize(self):
        return {
            'id':   self.id,
            'url':  self.url,

        }
