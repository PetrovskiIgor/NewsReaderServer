#encoding=utf-8

from google.appengine.ext import ndb

class NewsPost(ndb.Model):

    url = ndb.StringProperty()
    host_page = ndb.StringProperty()
    title = ndb.StringProperty()
    dictWords = ndb.PickleProperty()
    dict_tf_idf = ndb.PickleProperty()
    numWords = ndb.IntegerProperty()

    #def __init__(self, host_page, url, title, dictWords, numWords):
    #    self.host_page = host_page
    #    self.url = url
    #    self.title = title
    #    self.dictWords = dictWords
    #    self.numWords = numWords
    #    self.dict_tf_idf = {}


    # function for calculating and storing the final version of a document
    def calculate_tf_idf(self, dictIDF):

        if self.dict_tf_idf is None:
            self.dict_tf_idf = {}

        # we pass through all the words
        for word in self.dictWords:

            # we calculate the term frequency for each word
            tf = (self.dictWords[word] * 1.0) / (self.numWords)


            # we read the inverse document frequency if it exists

            val_idf = dictIDF.get(word, None)
            if val_idf is not None:
                tf_idf = val_idf * tf
                self.dict_tf_idf[word] = tf_idf


    @classmethod
    def query_newspost(cls, ancestor_key):
        return cls.query(ancestor=ancestor_key)


