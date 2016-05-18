# encoding=utf-8

import Utility
from cPickle import Pickler
from cPickle import Unpickler
# P(text  | class) = P(w1|class) * P(w2 | class) * ... P(wN | class)

# P(w_i | class) = (number of times w_i appears in class)/ (number of words in class)

# za dadena kategorija, dava kolku vkupno zborovi ima
dict_cat_count = {} # gives us how many words a class has
dict_word_in_cat = {} # gives us how many times each word appears in a category dict[category][word]

path = '/Users/igorpetrovski/Desktop/NEURAL_WEIGHTS/data.txt'

str_dict_cat_count = 'dict_cat_count'
str_dict_word_in_cat = 'dict_word_in_cat'
str_dict_probs = 'dict_probs'
str_dict_priors = 'dict_priors'
def buildDicts(fileName):

    counter = 0
    # priors[cat] - dava KOLKU dokumenti se klasificirani so kategorija cat
    priors = {}


    for line in open(fileName):
        parts = line.decode('utf-8').strip().split('\t')
        category = parts[0]
        text = parts[1]

        priors[category] = 1 + priors.get(category, 0)

        words = Utility.getWords(text)

        dict_cat_count[category] = len(words) + dict_cat_count.get(category, 0)

        dict_word_in_cat.setdefault(category, {})

        for w in words:
            dict_word_in_cat[category][w] = 1 + dict_word_in_cat[category].get(w, 0)


        counter += 1

        if counter % 10000 == 0:
            print 'processed %d news' % counter


    for cat in priors:
        priors[cat] = (priors[cat] * 1.0) / counter
        print 'Category %s num words: %d' % (cat, dict_cat_count[cat])


    print 'num unique words: %d' % (len(dict_word_in_cat))

    return dict_cat_count, dict_word_in_cat, priors
    #fileToWrite = open(str_dict_cat_count, 'w')
    #Pickler(fileToWrite).dump(dict_cat_count)
    #fileToWrite.close()


    #fileToWrite = open(str_dict_word_in_cat, 'w')
    #Pickler(fileToWrite).dump(dict_word_in_cat)
    #fileToWrite.close()

    #fileToWrite = open(str_dict_priors, 'w')
    #Pickler(fileToWrite).dump(priors)
    #fileToWrite.close()


def computeProbabilities():
    fileToRead = open(str_dict_cat_count)
    dictCat = Unpickler(fileToRead).load()
    fileToRead.close()


    fileToRead = open(str_dict_word_in_cat)
    dictWords = Unpickler(fileToRead).load()
    fileToRead.close()

    dict_probs = {}


    for cat in dictWords:
        dict_probs[cat] = {}
        for word in dictWords[cat]:
            dict_probs[cat][word] = (dictWords[cat][word] * 1.0) / dictCat[cat]

    fileToWrite = open(str_dict_probs, 'w')
    Pickler(fileToWrite).dump(dict_probs)
    fileToWrite.close()


#buildDicts(path)
