#encoding=utf-8

from google.appengine.ext import ndb
import math
from model import Source


# heavy weight class for representing a news-post
# we send a light-weighted version (described in NewsPostClient) to the user because the user doesn't need all the dictionaries contained here

class NewsPost(ndb.Model):
    #the url that contains the news
    url = ndb.StringProperty()
    #the host page where this news post
    host_page = ndb.StringProperty()
    #the title of the news
    title = ndb.StringProperty()
    #dictionary that for a given word returns the number of times that it appeared in the document
    dictWords = ndb.PickleProperty()
    #dictionary which is computed using the calculate_tf_idf() function
    dict_tf_idf = ndb.PickleProperty()
    #integer that represents how many words there are in the document
    numWords = ndb.IntegerProperty()
    #ordered array that represents the tokenized version of the document
    words = ndb.PickleProperty()

    #the id of the source object
    source_id = ndb.IntegerProperty()
    #the url of the source object (same as host_page) <-- maybe we need to reconsider the design for this
    source_url = ndb.StringProperty()

    #the url to the image associated with the news post
    img_url = ndb.StringProperty()

    #def __init__(self, host_page, url, title, dictWords, numWords):
    #    self.host_page = host_page
    #    self.url = url
    #    self.title = title
    #    self.dictWords = dictWords
    #    self.numWords = numWords
    #    self.dict_tf_idf = {}


    def calculate_tf_idf(self, dict_IDF):
        """
        function for calculating and storing the final version of a document

        :param dict_IDF: the idf dictionary which is precomputed
        :return: returns nothing
        """

        if self.dict_tf_idf is None:
            self.dict_tf_idf = {}

        # we pass the words that we got when instantiating the object one by one
        for word in self.dictWords:

            # we calculate the term frequency for each word
            tf = (self.dictWords[word] * 1.0)


            # we read the inverse document frequency if it exists

            val_idf = dict_IDF.get(word, None)
            if val_idf is not None:
                if tf > 0:
                    tf = 1 + math.log10(tf)
                else:
                    tf = 0

                tf_idf = val_idf * tf
                self.dict_tf_idf[word] = tf_idf
            else:
                self.dict_tf_idf[word] = 0


    @classmethod
    def query_newspost(cls, ancestor_key):
        """
        Method that is bundled with the Google's App Engine Datastore API
        :param ancestor_key: the key associated with this news post
        :return: returns array of objects that match the ancestor_key
        """
        return cls.query().filter(ancestor = ancestor_key)


