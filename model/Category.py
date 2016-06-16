
from google.appengine.ext import ndb

#source class that describes the Source where we extract the news from

class Category(ndb.Model):

    def __init__(self, id, name, title):

        self.id = id
        self.name = name
        self.title = title


    def serialize(self):
        return {
            'id':   self.id,
            'name':  self.name,
            'title': self.title,

        }
