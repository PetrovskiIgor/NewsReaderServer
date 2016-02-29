#encoding=utf-8


# Description:
# This file contains utility functions, dictionaries which are used through out the application

import math
from cPickle import Pickler
from model.Source import Source




def isInStopWords(word):
    return word in stopWords


#set of stopwords which will be ignored when processing a text
stopWords = set(['сте', 'ве', 'ви', 'вие', 'вас', 'но', 'го', 'а', 'е', 'на', 'во', 'и', 'ни', 'ние', 'или',
'та', 'ма', 'ти', 'се', 'за', 'од', 'да', 'со', 'ќе', 'дека', 'што', 'не', 'ги', 'ја', 'јас',
'тие', 'тоа', 'таа', 'тој', 'мк', 'отсто', 'гр', 'мл', 'тв', 'ул', 'врз', 'сите', 'иако', 'друг', 'друга',
'при', 'цел', 'меѓу', 'околу', 'нив', 'кои', 'кога', 'поради', 'има', 'без', 'биле', 'она', 'кое', 'кај',
'овој', 'него', 'некои', 'оваа', 'веќе', 'оние', 'уште', 'може', 'меѓутоа',
'the', 'of', 'in', 'and', 'is', 'a', 'to', 'are', 'for', 'that', 'all', 'an', 'i', 'on',
'fg', '3p', 'ft', 'reb', 'pos', 'pts', 'min', 'eff', 'bs', 'pf', 'am', 'pm', '3rd', '4th', '5th', '6th', 'nbsp'
                 'kurir', 'црнобело', 'kanal5'])


# sources where we collection data from

sources = [ Source(0, 'http://vecer.mk', ['http://vecer.mk/rss.xml']),
            Source(1,'http://www.crnobelo.com',['http://www.crnobelo.com/?format=feed&type=rss']),
            Source(2,'http://sitel.mk',['http://sitel.mk/rss.xml']),
            Source(3,'http://kurir.mk',['http://kurir.mk/feed/']),
            Source(4,'http://republika.mk',['http://republika.mk/?feed=rss2'])
            #Source(5,'http://plusinfo.mk',['http://plusinfo.mk/rss/biznis','http://plusinfo.mk/rss/skopje', 'http://plusinfo.mk/rss/kultura',
            #                   'http://plusinfo.mk/rss/zdravje', 'http://plusinfo.mk/rss/svet', 'http://plusinfo.mk/rss/scena']),
            #Source(6,'http://www.vest.mk',['http://www.vest.mk/rssGenerator/']),
            #Source(7,'http://alsat.mk',['http://alsat.mk/RssFeed']),
            #Source(8,'http://www.mkd.mk/feed',[ 'http://www.mkd.mk/feed']),
            #Source(9,'http://www.sport.com.mk',['http://www.sport.com.mk/rssgenerator/rss.aspx']),
            #Source(10,'http://www.dnevnik.mk',['http://www.dnevnik.mk/rssGenerator/']),
            #Source(11, 'http://interesno.com.mk' , ['http://interesno.com.mk/index.php?format=feed&type=rss' ])
          ]



str_idf_dict = 'dict_idf'
path_dataset = '/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'

#function that for a given text (string) returns a list of words contained in that text

def getWords(line):
  line = line.lower()
  out = []
  word = []

  for c in line:
    if c.isalpha():
      word.append(c)
      continue
    else:
      if word:
        newWord =  ''.join(word).lower()

        if not isInStopWords(newWord):

            if len(newWord) > 6:
                newWord = newWord[0:6]
            out.append(newWord)
      word = []
  if word:
        newWord =   ''.join(word).lower()

        if not isInStopWords(newWord):
            if len(newWord) > 6:
                newWord = newWord[0:6]

            out.append(newWord)

  return out


# function for calculating the idf dictionary
# only one execution needed

def calculate_idf_dictionary(fileName):

    numDocuments = 0

    dictWords = {}
    for line in open(fileName):
        parts = line.decode('utf-8').strip().split('\t')

        category = parts[0] #unimportant for now..
        text = parts[1]

        words = set(getWords(text))


        for word in words:
            dictWords[word] = 1 + dictWords.get(word, 0)

        numDocuments += 1

        if numDocuments % 1000 == 0:
            print 'processed %d number of documents' % numDocuments

    for word in dictWords:
        dictWords[word] = math.log(numDocuments / (dictWords[word] * 1.0))


    print 'number of words: ', len(dictWords)
    print 'number of documents: ', numDocuments

    fileToWrite = open(str_idf_dict, 'w')
    Pickler(fileToWrite).dump(dictWords)
    fileToWrite.close()


#calculate_idf_dictionary(path_dataset)




