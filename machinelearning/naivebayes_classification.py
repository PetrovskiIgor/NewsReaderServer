# encoding=utf-8

import Utility
from cPickle import Pickler
from cPickle import Unpickler



# P(text  | class) = P(w1|class) * P(w2 | class) * ... P(wN | class)
# P(w_i | class) = (number of times w_i appears in class)/ (number of words in class)




str_dict_cat_count = 'dict_cat_count'
str_dict_word_in_cat = 'dict_word_in_cat'
str_dict_probs = 'dict_probs'
str_dict_priors = 'dict_priors'

def buildDicts(file_name, save_dicts=False):
    """

    :param file_name:   the file that contains the pairs (category, sentence) where we build the dictionary from
    :param save_dicts:  variable indicating whether to save the dictionaries in files or just just to return them
    :return: returns    dict_cat_count, dict_word_in_cat,
    """
    counter = 0
    # priors (priors[cat] <- how many documents are in category cat)
    priors = {}
    # for a given category as a key, this returns how many words there are as a value
    dict_cat_count = {}
    # for a given category and a word as keys (dict_word_in_cat[category][word]),
    # we get how many times that word has appeared in that category
    dict_word_in_cat = {}


    for line in open(file_name):

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

    if save_dicts:
        print 'Saving the dicts..'
        fileToWrite = open(str_dict_cat_count, 'w')
        Pickler(fileToWrite).dump(dict_cat_count)
        fileToWrite.close()


        fileToWrite = open(str_dict_word_in_cat, 'w')
        Pickler(fileToWrite).dump(dict_word_in_cat)
        fileToWrite.close()

        fileToWrite = open(str_dict_priors, 'w')
        Pickler(fileToWrite).dump(priors)
        fileToWrite.close()
        print 'Saved the dicts!'

    return dict_cat_count, dict_word_in_cat, priors



def computeProbabilities(dict_cat=None, dict_words=None, save_dict_probs=True):
    """
    Computes and returns the dictionary for P(word | category)
    :param dict_cat:        dictionary of priors where dict_cat[cat] is the number of documents classified in category CAT
    :param dict_words:      dict_words[cat][word] - gives us how many times the word 'word' appeared in category 'cat'
    :param save_dict_probs: whether to save the dict as file or not
    :return: returns a dictonary where dict_probs[cat][word] gives us the probability P(word | cat) = P(word, cat) / P(cat)
    """

    if dict_cat is None:
        fileToRead = open(str_dict_cat_count)
        dict_cat = Unpickler(fileToRead).load()
        fileToRead.close()

    if dict_words is None:
        fileToRead = open(str_dict_word_in_cat)
        dict_words = Unpickler(fileToRead).load()
        fileToRead.close()

    dict_probs = {}

    for cat in dict_words:
        dict_probs[cat] = {}
        for word in dict_words[cat]:
            dict_probs[cat][word] = (dict_words[cat][word] * 1.0) / dict_cat[cat]

    if save_dict_probs:
        fileToWrite = open(str_dict_probs, 'w')
        Pickler(fileToWrite).dump(dict_probs)
        fileToWrite.close()

    return dict_probs


#buildDicts(path)
