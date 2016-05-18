#encoding=utf-8


# Description:
# This file contains utility functions, dictionaries which are used through out the application


import math
from cPickle import Pickler
from model.Source import Source


#???!!!! DALI E MOZHNO DA IMA PROBLEMI ZA PRAZNO MESTO KAJ 7 semestar ???!!!!
training_file_path='/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'
vocabulary_file_path=''


def isInStopWords(word):
    return word in stop_words


# source boundaries
# i have noticed that specific links put constant tokens at the beginning/end of a document
# so i have decided to ignore(delete) them

paragraph_boundaries = {
                'http://vecer.mk/rss.xml':[0,-3],
                'http://www.crnobelo.com/?format=feed&type=rss': [0,-2],
                'http://novatv.mk/rss.xml?tip=2'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=5'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=7'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=23'   :[2,-2],
                'http://alsat.mk/RssFeed'           :[0,-1],
                'http://www.vest.mk/rssGenerator/'  :[0,-7],
                'http://alsat.mk/RssFeed'           :[1,-3],
                'http://www.mkd.mk/feed':[0,-4],
                'http://www.sport.com.mk/rssgenerator/rss.aspx': [1]
                }


#set of stopwords which will be ignored when processing a text
stop_words = set(['сте', 'ве', 'ви', 'вие', 'вас', 'но', 'го', 'а', 'е', 'на', 'во', 'и', 'ни', 'ние', 'или',
'та', 'ма', 'ти', 'се', 'за', 'од', 'да', 'со', 'ќе', 'дека', 'што', 'не', 'ги', 'ја', 'јас',
'тие', 'тоа', 'таа', 'тој', 'мк', 'отсто', 'гр', 'мл', 'тв', 'ул', 'врз', 'сите', 'иако', 'друг', 'друга',
'при', 'цел', 'меѓу', 'околу', 'нив', 'кои', 'кога', 'поради', 'има', 'без', 'биле', 'она', 'кое', 'кај',
'овој', 'него', 'некои', 'оваа', 'веќе', 'оние', 'уште', 'може', 'меѓутоа',
'the', 'of', 'in', 'and', 'is', 'a', 'to', 'are', 'for', 'that', 'all', 'an', 'i', 'on',
'fg', '3p', 'ft', 'reb', 'pos', 'pts', 'min', 'eff', 'bs', 'pf', 'am', 'pm', '3rd', '4th', '5th', '6th', 'nbsp'
                 'kurir', 'црнобело', 'kanal5'])


# sources where we collection data from

sources = [
            Source(0, 'http://vecer.mk', ['http://vecer.mk/rss.xml']),
            Source(1,'http://www.crnobelo.com',['http://www.crnobelo.com/?format=feed&type=rss']),
            Source(2,'http://sitel.mk',['http://sitel.mk/rss.xml']),
            Source(3,'http://kurir.mk',['http://kurir.mk/feed/']),
            Source(4,'http://republika.mk',['http://republika.mk/?feed=rss2']),
            Source(5,'http://plusinfo.mk',['http://plusinfo.mk/rss/biznis','http://plusinfo.mk/rss/skopje', 'http://plusinfo.mk/rss/kultura',
                               'http://plusinfo.mk/rss/zdravje', 'http://plusinfo.mk/rss/svet', 'http://plusinfo.mk/rss/scena']),
            Source(6,'http://www.vest.mk',['http://www.vest.mk/rssGenerator/']),
            Source(7,'http://alsat.mk',['http://alsat.mk/RssFeed']),
            Source(8,'http://www.mkd.mk/feed',[ 'http://www.mkd.mk/feed']),
            Source(9,'http://www.sport.com.mk',['http://www.sport.com.mk/rssgenerator/rss.aspx']),
            Source(10,'http://www.dnevnik.mk',['http://www.dnevnik.mk/rssGenerator/']),
            Source(11, 'http://interesno.com.mk' , ['http://interesno.com.mk/index.php?format=feed&type=rss' ])
          ]



str_idf_dict = 'dict_idf'
path_dataset = '/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'

#function that for a given text (string) returns a list of words contained in that text

def getWords(line):

    """
    the basic function that parses a line
    :param line: line that needs to be parsed
    :return: list of words
    """
    line = line.lower()
    out = []
    word = []

    for c in line:
        if c.isalpha():
            word.append(c)
            continue
        else:
            if word:
                newWord = ''.join(word)

                if not newWord in stop_words:
                    if len(newWord) > 6:
                        newWord = newWord[0:6]

                    out.append(newWord)
            word = []

    if word:
        newWord =   ''.join(word)

        if not newWord in stop_words:
            if len(newWord) > 6:
                newWord = newWord[0:6]

            out.append(newWord)

    return out




def calculate_idf_dictionary(file_path):

    """
    function for calculating the idf dictionary
    only one execution needed
    :param file_path: the file where we build the dictionary from
    :return: we return the built dictionary
    """

    #idf for a word: log (number of total documents / number of documents that word appears in )

    num_documents = 0

    idf_dict = {}
    for line in open(file_path):
        parts = line.decode('utf-8').strip().split('\t')

        category = parts[0] #unimportant for now..
        text     = parts[1]


        words = set(getWords(text))


        for word in words:
            idf_dict[word] = 1 + idf_dict.get(word, 0)

        num_documents += 1

        if num_documents % 10000 == 0:
            print 'processed %d number of documents' % num_documents

    for word in idf_dict:
        idf_dict[word] = math.log(num_documents / (idf_dict[word] * 1.0))


    print 'number of words: ', len(idf_dict)
    print 'number of documents: ', num_documents

    fileToWrite = open(str_idf_dict, 'w')
    Pickler(fileToWrite).dump(idf_dict)
    fileToWrite.close()

    return idf_dict


#calculate_idf_dictionary(path_dataset)




