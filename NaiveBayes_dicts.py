__author__ = 'igorpetrovski'
from google.appengine.ext import ndb
class Dicts(ndb.Model):

    dict_words = ndb.PickleProperty()
    dict_cats = ndb.PickleProperty()
    dict_priors = ndb.PickleProperty()
