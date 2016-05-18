# encoding=utf-8

from cPickle import Unpickler
import math

import Utility
from machinelearning import naivebayes_classification


def testNaiveBayes():
    counter = 0

    fileToRead = open(naivebayes_classification.str_dict_word_in_cat)
    dict_words = Unpickler(fileToRead).load()
    fileToRead.close()

    fileToRead = open(naivebayes_classification.str_dict_cat_count)
    dict_cat_count = Unpickler(fileToRead).load()
    fileToRead.close()

    fileToRead = open(naivebayes_classification.str_dict_priors)
    dict_priors = Unpickler(fileToRead).load()
    fileToRead.close()



    numErrors = 0
    for line in open(Utility.path_dataset):

        parts = line.decode('utf-8').strip().split('\t')
        category = parts[0]
        text = parts[1]
        words = Utility.getWords(text)

        nb_category = get_NB_category(words, dict_words, dict_cat_count, dict_priors)

        if nb_category != category:
            #print 'correct category: %s my category: %s' % (category, nb_category)
            numErrors += 1

        counter += 1



    print 'accuracy: %f' % (100*(1 - numErrors*1.0/counter))

def get_NB_category(words, dict_words, dict_cats, dict_priors):

    maxCat = ''
    maxProb = 0

    flag_firstTime = True

    for cat in dict_cats:
        prob = compute_NB_prob(words, dict_words, dict_cats, cat,dict_priors)


        if flag_firstTime:
            flag_firstTime = False
            maxProb = prob
            continue

        #print 'prob: %f\n' % prob

        if prob > maxProb:
            maxProb = prob
            maxCat = cat


    return maxCat

def compute_NB_prob(words, dict_words, dict_cats, cat, priors):

    total_prob = 1
    den = dict_cats[cat]

    den += len(dict_words[cat])

    for word in words:

        nom = dict_words[cat].get(word, 0) + 1

        toAdd = (1.0*nom)/den

        total_prob +=math.log10(toAdd)

    total_prob += math.log10(priors[cat])

    return total_prob


#testNaiveBayes()