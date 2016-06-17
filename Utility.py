#encoding=utf-8


# Description:
# This file contains utility functions, dictionaries which are used through out the application


import math
import time
from cPickle import Pickler
from cPickle import Unpickler
from model.Source import Source
from model.Category import  Category


training_file_path='/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'
categories_file_path='/Users/igorpetrovski/Desktop/NewsReaderServer/categories.txt'



def isInStopWords(word):
    return word in stop_words


# source boundaries
# i have noticed that specific links put constant tokens at the beginning/end of a document
# so i have decided to ignore(delete) them




#set of stopwords which will be ignored when processing a text
stop_words = set(['сте', 'ве', 'ви', 'вие', 'вас', 'но', 'го', 'а', 'е', 'на', 'во', 'и', 'ни', 'ние', 'или',
'та', 'ма', 'ти', 'се', 'за', 'од', 'да', 'со', 'ќе', 'дека', 'што', 'не', 'ги', 'ја', 'јас',
'тие', 'тоа', 'таа', 'тој', 'мк', 'отсто', 'гр', 'мл', 'тв', 'ул', 'врз', 'сите', 'иако', 'друг', 'друга',
'при', 'цел', 'меѓу', 'околу', 'нив', 'кои', 'кога', 'поради', 'има', 'без', 'биле', 'она', 'кое', 'кај',
'овој', 'него', 'некои', 'оваа', 'веќе', 'оние', 'уште', 'може', 'меѓутоа',
'the', 'of', 'in', 'and', 'is', 'a', 'to', 'are', 'for', 'that', 'all', 'an', 'i', 'on',
'fg', '3p', 'ft', 'reb', 'pos', 'pts', 'min', 'eff', 'bs', 'pf', 'am', 'pm', '3rd', '4th', '5th', '6th', 'nbsp'
                 'kurir', 'црнобело', 'kanal5'])



#categories

categories = [
                Category(0,'MAKEDONIJA', 'Македонија', 'http://img.freeflagicons.com/thumb/round_icon/macedonia/macedonia_640.png'),
                Category(1,'SVET', 'Свет', 'http://www.fordesigner.com/imguploads/Image/cjbc/zcool/png20080526/1211766291.png'),
                Category(2,'EKONOMIJA', 'Економија', 'http://static1.squarespace.com/static/54bebe07e4b0dc5217eebd19/t/5512f5a2e4b008b87901036f/1427146265321/icon-graph.png'),
                Category(3,'SCENA', 'Сцена'),
                Category(4,'ZIVOT', 'Живот'),
                Category(5,'KULTURA', 'Култура'),
                Category(6,'ZDRAVJE', 'Здравје', 'http://www.surelineproductions.com/uploads/2/2/9/5/22952802/4826818.png'),
                Category(7,'TEHNOLOGIJA', 'Технологија', 'http://www.fancyicons.com/free-icons/101/dragon-ball/png/256/dragonball3_256.png'),
                Category(8,'FUDBAL', 'Фудбал', 'http://www.freeiconspng.com/uploads/soccer-ball-ico-9.png'),
                Category(9,'KOSARKA', 'Кошарка'),
                Category(10,'RAKOMET', 'Ракомет'),
                Category(11,'TENIS', 'Тенис')

]

# sources where we collection data from

sources = [
            Source(0, 'http://vecer.mk', ['http://vecer.mk/rss.xml']),#opoziconen
            Source(1,'http://www.crnobelo.com',['http://www.crnobelo.com/?format=feed&type=rss']),
            Source(2,'http://sitel.mk',['http://sitel.mk/rss.xml']),#opoziconen
            Source(3,'http://kurir.mk',['http://kurir.mk/feed/']),#opoziconen
            Source(4,'http://republika.mk',['http://republika.mk/?feed=rss2']),#opoziconen
            #Source(5,'http://plusinfo.mk',['http://plusinfo.mk/rss/biznis','http://plusinfo.mk/rss/skopje', 'http://plusinfo.mk/rss/kultura',
              #                 'http://plusinfo.mk/rss/zdravje', 'http://plusinfo.mk/rss/svet', 'http://plusinfo.mk/rss/scena']),
            Source(6,'http://www.vest.mk',['http://www.vest.mk/rssGenerator/']),#opoziconen
            Source(7,'http://alsat.mk',['http://alsat.mk/RssFeed']),
            Source(8,'http://www.mkd.mk/',[ 'http://www.mkd.mk/feed']),
            Source(9,'http://www.sport.com.mk',['http://www.sport.com.mk/rssgenerator/rss.aspx']),
            Source(10,'http://www.dnevnik.mk',['http://www.dnevnik.mk/rssGenerator/']),#opoziconen
            Source(11, 'http://interesno.com.mk' , ['http://interesno.com.mk/index.php?format=feed&type=rss' ]),
            Source(12, 'http://www.fakulteti.mk/',['http://www.fakulteti.mk/rss/rss.ashx']),
            Source(13, 'http://novatv.mk/', ['http://novatv.mk/feed']), # ne se load-a feedot
            Source(14, 'http://kajgana.com/', ['http://kajgana.com/rss.xml']),
            Source(15, 'http://derbi.mk/', ['http://derbi.mk/feed/']),
            Source(16, 'http://www.libertas.mk/', ['http://www.libertas.mk/feed/']),
            Source(17, 'http://mkd-news.com/', ['http://mkd-news.com/feed/']),
            Source(18, 'http://www.brif.mk/', ['http://www.brif.mk/feed/']),
            Source(19, 'http://off.net.mk/', ['http://feeds.feedburner.com/offnetmk']),
            Source(20, 'http://it.mk/', ['http://it.mk/feed/']),
            Source(21, 'http://www.smartportal.mk/',['http://www.smartportal.mk/feed/']),
            Source(22, 'http://popularno.mk/',['http://www.popularno.mk/feed/']),
            Source(23, 'http://www.femina.mk/',['http://www.femina.mk/rss']),
            Source(24, 'http://doktori.mk/',['http://feeds.feedburner.com/doktorimk']),
            Source(25, 'http://tocka.com.mk/',['http://tocka.com.mk/rss.php']),
            Source(26, 'http://koli.com.mk/',['http://koli.com.mk/rss.ashx']),
            Source(27, 'http://a1on.mk/wordpress/',['http://a1on.mk/wordpress/feed']),
            Source(28, 'http://reporter.mk/',['http://reporter.mk/feed/']),
            Source(29, 'http://lokalno.mk/',['http://lokalno.mk/feed/']),
            Source(30, 'http://automedia.mk/',['http://automedia.mk/?feed=rss2']),
            Source(31, 'http://netpress.com.mk/',['http://netpress.com.mk/feed/']),#opoziconen
            Source(32, 'http://evesti.mk/', ['http://feeds.feedburner.com/evesti']),
            Source(33, 'http://www.novamakedonija.com.mk/', ['http://www.novamakedonija.com.mk/rssAll.asp']),
            Source(34, 'http://makfax.com.mk/', ['http://makfax.com.mk/_feeds/rss2/news']),
            Source(35, 'http://ekonomski.mk/', ['http://ekonomski.mk/feed/']),
            Source(36, 'http://www.spektra.com.mk/', ['http://www.spektra.com.mk/rss']),
            Source(37, 'http://bi.mk/', ['http://bi.mk/feed/']),
            Source(38, 'http://faktor.mk/', ['http://faktor.mk/feed/']),
            Source(39, 'http://aktuelno24.mk/', ['http://feeds.feedburner.com/aktuelno24/ywvm']), #losho lista sliki,
            Source(40, 'http://pozitiv.mk/', ['http://pozitiv.mk/feed/']),
            Source(41, 'http://www.idividi.com.mk/', ['http://www.idividi.com.mk/rss.aspx']),
            Source(42, 'http://zase.mk/', ['http://zase.mk/feed/']), #ne raboti feedot koga vlecam od localhost

            # ----------- PROVERKA -----------------
            #vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

            Source(43, 'http://www.avtomagazin.com.mk/', ['http://www.avtomagazin.com.mk/avto-magazin.rss']), #PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(44, 'http://meta.mk/', ['http://meta.mk/feed/']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(45, 'http://slobodna.mk/', ['http://slobodna.mk/feed/']), #PROVERENO TEKSTOT SE ZEMA DOBRO (NEKOGAS LISTA I META DATA)
            Source(47, 'http://www.utrinski.mk/', ['http://www.utrinski.mk/rssgenerator/rss.aspx']), # PROVERENO, TEKSTOT SE ZEMA DOBRO (samo naslovot se povtoruva duplo)
            Source(48, 'http://kapital.mk/', ['http://kapital.mk/feed/']), # LOSH FEED
            Source(49, 'http://www.akademik.mk/', ['http://www.akademik.mk/feed/']),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(50, 'http://mk.rbth.com/', ['http://mk.rbth.com/xml/index.xml'], 'Руска реч'),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(51, 'http://telma.com.mk/', ['http://telma.com.mk/rss.xml'], 'Телма'), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(52, 'http://kanal77.mk/', ['http://kanal77.mk/feed/']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(53, 'http://24vesti.mk/', ['http://24vesti.mk/rss.xml']), # PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(54, 'http://marketing365.mk/', ['http://marketing365.mk/feed/']),# PROVERENO, TEKSTOT SE ZEMA DOBRO
            Source(55, 'http://maxim.mk/', ['http://maxim.mk/rss.xml']), # PROVERENO, TEKSTOT SE ZEMA DOBRO

            # PROVERENO, RAZLICNI TAGOVI. pr: entry mesto item itn
            # ako ima povekje vakvi slucaevi togas da se razmisli kako da se opfati ovoj slucaj (povtorno e mozhno so dictionaries)
            Source(56, 'http://prizma.birn.eu.com/', ['http://mix.chimpfeedr.com/5ee9b-Prizma'], 'Призма')
          ]



#the dictionary that tells us which paragraphs we need to ignore for a given source
fetch_text_specifications = {
                'http://vecer.mk/rss.xml':[0,-3],
                'http://www.crnobelo.com/?format=feed&type=rss': [0,-2],
                'http://novatv.mk/rss.xml?tip=2'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=5'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=7'    :[2,-2],
                'http://novatv.mk/rss.xml?tip=23'   :[2,-2],
                'http://www.vest.mk/rssGenerator/'  :[0,-7],
                'http://alsat.mk/RssFeed'           :[1,-3],
                'http://www.mkd.mk/feed':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'main-wrapper',
                                            'nested_tag_type':'div', 'nested_attribute_type':'class', 'nested_attribute_value':'field-body',

                                             },

                'http://www.sport.com.mk/rssgenerator/rss.aspx': [1],
                'http://reporter.mk/feed/':[3,-10],
                'http://tocka.com.mk/rss.php':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'sodrzina_vest'},
                'http://www.femina.mk/rss':[0,-7],
                'http://feeds.feedburner.com/offnetmk':{'tag_type':'div', 'attribute_type':'class',
                                                        'attribute_value':['sodrzhina-full', 'voved']},
                'http://lokalno.mk/feed/': [0,-9],
                'http://it.mk/feed/':[2,-28],
                'http://netpress.com.mk/feed/': [0,-1],
                'http://feeds.feedburner.com/doktorimk':[1,-1],
                'http://feeds.feedburner.com/evesti': [0,-10],
                'http://makfax.com.mk/_feeds/rss2/news':[2,-5],
                'http://ekonomski.mk/feed/':[0,-4],
                'http://www.spektra.com.mk/rss':[0,-12],
                'http://bi.mk/feed/':[0,-23], #da se proveruva za update!!!,
                'http://faktor.mk/feed/': [0,-20],
                'http://pozitiv.mk/feed/': [0,-2],
                'http://www.motika.com.mk/feed/': [4],
                'http://www.idividi.com.mk/rss.aspx':[0,-13],
                'http://kurir.mk/feed/': [0,-5],
                'http://www.avtomagazin.com.mk/avto-magazin.rss':[0,-23],
                'http://slobodna.mk/feed/':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'entry clearfix'},
                'http://meta.mk/feed/':[1,-14],

                'http://maxim.mk/rss.xml':[0,-6],
                'http://marketing365.mk/feed/':[0,-21],
                'http://www.utrinski.mk/rssgenerator/rss.aspx': [3,-6],
                'http://telma.com.mk/rss.xml':[0,-1],
                'http://kanal77.mk/feed/':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'entry', 'nested_tag_type':'p',
                                           'nested_attribute_type':'class', 'nested_attribute_value': None},
                'http://www.akademik.mk/feed/':[0,-1],
                'http://mk.rbth.com/xml/index.xml':[0,-2],
                'http://www.avtomagazin.com.mk/avto-magazin.rss':{'tag_type':'section', 'attribute_type':'class', 'attribute_value':'link-arrow'},
                'http://24vesti.mk/rss.xml':{'tag_type':'div', 'attribute_type':'class', 'attribute_value':'main-content',
                                            'nested_tag_type':'div', 'nested_attribute_type':'class', 'nested_attribute_value':'content',
                                             'limit':1},
                'http://republika.mk/?feed=rss2':{'tag_type':'div', 'attribute_type':'id', 'attribute_value':'article_text'}
                }


str_idf_dict = 'dict_idf'
path_dataset = '/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'

#function that for a given text (string) returns a list of words contained in that text

def getWords(line, to_lower=True):

    """
    the basic function that parses a line
    :param line: line that needs to be parsed
    :return: list of words
    """
    if to_lower:
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


def get_idf_dictionary():

    file_to_read = open(str_idf_dict, 'r')
    idf_dict = Unpickler(file_to_read).load()
    file_to_read.close()

    return idf_dict



def calculate_idf_dictionary(file_path):

    """
    function for calculating the idf dictionary
    only one execution needed
    :param file_path: the file where we build the dictionary from
    :return: we return the built dictionary
    """

    #idf for a word: log (number of total documents / number of documents that word appears in )
    begin = time.time()
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

    print 'Done for: %d seconds.' % (time.time()-begin)
    fileToWrite = open(str_idf_dict, 'w')
    Pickler(fileToWrite).dump(idf_dict)
    fileToWrite.close()

    return idf_dict


def create_files_for_categories(file_path_input, file_path_store):
    """
    function for storing the categories in file
    the i-th line will contain the ith-category
    from this file we will be able to create the dictionary category -> id_category and reversed dictionary id_category -> category
    :param file_path_input: the file where we read the categories from
    :param file_path_store:  where we need to store the categories
    :return: nothing
    """

    categories = []
    for line in open(file_path_input):
        category = line.decode(encoding='utf-8').strip().split('\t')[0]
        categories.append(category)

    categories = set(categories)



    file_to_write = open(file_path_store, 'w')
    for category in categories:
        file_to_write.write(('%s\n' % category).encode('utf-8'))

    file_to_write.close()

def load_categories():
    """
    Loading the categories that we need for text categorization
    :return: returns cat_to_ind and ind_to_cat dictionaries
    """
    cat_to_ind = {}
    ind_to_cat = []

    ind_line = 0
    for line in open(categories_file_path):
        category = line.decode(encoding='utf-8').strip()
        cat_to_ind[category] = ind_line
        ind_to_cat.append(line)
        ind_line += 1


    return cat_to_ind, ind_to_cat

def load_vocabulary(num_words=50000):
    print 'loading vocabulary..'
    vocabulary = {}
    ind = 0
    for line in open('vocabulary%d.txt' % num_words):
        line = line.decode('utf-8').strip()

        if line:
            vocabulary[line] = ind
            ind += 1
    print 'vocabulary size: %d' % len(vocabulary)
    return vocabulary




def create_vocabulary(file_path_source, file_path_dest,num_words=50000):
    """
    creates a vocabulary of most common words
    :param file_path_source: source where we should read the sentnces from
    :param file_path_dest:  where should we store the list
    :param num_words: how many words to take into considerations after sorting
    :return: the list of 'num_words' most common words
    """
    word_count = {}
    t0 = time.time()
    for line in open(file_path_source):
        text = line.decode(encoding='utf-8').strip().split('\t')[1]
        words = getWords(text)

        for w in words:
            word_count[w] = 1 + word_count.get(w, 0)


    print 'Processed the source for %d seconds.' % (time.time() - t0)

    list_words = sorted([(w, word_count[w]) for w in word_count], key=lambda x: -x[1])

    num_words = min(len(list_words), num_words)

    list_words = list_words[:num_words]

    t0 = time.time()
    file_to_write = open('%s%d.txt' % (file_path_dest, num_words), 'w')
    for word in list_words:
        file_to_write.write((word[0] + '\n').encode('utf-8'))
    file_to_write.close()

    print 'Wrote the words in a file for %d seconds' % (time.time() - t0)

    return list_words





def transform_single_text_tf_idf(text_input):


        words = getWords(text_input, to_lower=True)

        word_count = {}

        for w in words:
            word_count[w] = 1 + word_count.get(w, 0)

        dict_tf_idf = {}

        idf = get_idf_dictionary()


        # we pass the words that we got when instantiating the object one by one
        for word in word_count:

            # we calculate the term frequency for each word
            tf = (word_count[word] * 1.0)


            # we read the inverse document frequency if it exists

            val_idf = idf.get(word, None)
            if val_idf is not None:
                if tf > 0:
                    tf = 1 + math.log10(tf)
                else:
                    tf = 0

                dict_tf_idf[word] = val_idf*tf
            else:
                dict_tf_idf[word] = 0


        return dict_tf_idf


def category_count(source_file, write_to_file=False):

    dict = {}
    for line in open(source_file):

        cat = line.strip().split('\t')[0]

        dict[cat] = 1 + dict.get(cat,0)


    categories = sorted([(category, dict[category]) for category in dict],key=lambda x: -x[1])


    if not write_to_file: return


    file_to_write = open('categories_count', 'w')

    for tuple in categories:
        file_to_write.write('%s\t%d\n' % (tuple[0], tuple[1]))


    file_to_write.close()


#category_count(source_file=path_dataset, write_to_file=True)