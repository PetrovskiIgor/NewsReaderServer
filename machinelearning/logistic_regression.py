#encoding=utf-8
__author__ = 'igorpetrovski'
__email__  = 'igor.tetovo@gmail.com'
__faculty__= 'Faculty of Computer Science and Engineering in Skopje, Macedonia'

import time
import random
import Utility

from sklearn.feature_extraction.text import TfidfVectorizer


from sklearn import linear_model
from cPickle import Pickler
from cPickle import Unpickler



model_file_path = 'logreg.pkl'
vectorizer_file_path= 'logreg_vectorizer.pkl'





def create_model(model_file_name, vectorizer_file_name, training_percentage=0.93, max_iter=300, print_logs=False):
    """
    creating the model for logistic regression and storing it for later use
    :param model_file_name: the name of the file where the model will be stored
    :param vectorizer_file_name: the name of file where the vectorizer will be stored
    :param training_percentage: how much of the training set should we use
    :param max_iter: the maximum number of iterations for training
    :param print_logs: whether we should print the logs (such as time needed for training) or not
    :return: returns the model and the vectorizer
    """



    begin = time.time()
    t0 = time.time()

    #for a given category we return it's id
    cat_to_ind = {}
    #for a given id we return the category associated with that id
    ind_to_cat = []

    curr_cat_ind = 0

    X_train = []
    Y_train = []

    cat_to_ind, ind_to_cat = Utility.load_categories()

    for line in open(Utility.training_file_path):
        parts = line.decode(encoding='utf-8').strip().split('\t')
        category = parts[0]
        text = parts[1]

        item = [text, cat_to_ind[category]]

        if random.random() < training_percentage:
            X_train.append(item[0])
            Y_train.append(item[1])

    if print_logs:
        print 'Read the dataset for %d seconds' % (time.time() - t0)
    t0 = time.time()

    vectorizer = TfidfVectorizer(encoding='utf-8', lowercase=True, stop_words=Utility.stop_words)
    X_train = vectorizer.fit_transform(X_train)

    if print_logs:
        print 'Vectorized the train and test set for %d seconds' % (time.time()-t0)


    classifier = linear_model.LogisticRegression(max_iter=max_iter)
    classifier.predi

    t0 = time.time()
    classifier.fit(X_train, Y_train)
    if print_logs:
        print 'Trained the model for %d seconds' % (time.time() - t0)

    t0 = time.time()

    file_to_write = open(model_file_name, 'w')
    Pickler(file_to_write).dump(classifier)
    file_to_write.close()

    file_to_write = open(vectorizer_file_name, 'w')
    Pickler(file_to_write).dump(vectorizer)
    file_to_write.close()

    if print_logs:
        print 'Dumped the items for %d seconds.' % (time.time() - t0)

    if print_logs:
        print 'Total time: %d seconds' % (time.time() - begin)

    return classifier, vectorizer

def get_persisted_model(model_path=model_file_path):
    """
    getter for geting the model that was previously persisted
    :param model_path: the file path where the model is persisted
    :return: returns the model for classifying
    """
    t0 = time.time()

    file_to_read = open(model_path)
    classifier = Unpickler(file_to_read).load()
    file_to_read.close()

    print 'Loaded model for %d seconds ' % (time.time() - t0)
    return classifier



def get_persisted_vectorizer(vectorizer_path=vectorizer_file_path):
    """
    geter for getting the vectorizer that was previously persisted
    :param vectorizer_path: where the vectorizer is located
    :return: vectorizer
    """
    t0 = time.time()
    file_to_read = open(vectorizer_path)
    vectorizer = Unpickler(file_to_read).load()
    file_to_read.close()
    print 'Loaded vectorizer for %d seconds' % (time.time() - t0)
    return vectorizer

def score_classifier(classifier, X_test, Y_test):

    score = classifier.score(X_test, Y_test)
    print 'Classifier score: %f' % score


def get_me_some_test_samples(file_path, prob_to_take=1.0):
    """
    :param file_path: the path for the file where we load the data from
    :param prob_to_take: the probability to take ceratin news as a test sample
    :return: returns X_test and Y_test
                X_test is a list of lists, where each list in the list represents a list of feautres
                Y_test represents the class id for each list of features in X_test
    """

    cat_to_ind, ind_to_cat = Utility.load_categories()

    vectorizer = get_persisted_vectorizer(vectorizer_file_path)

    X_test = []
    Y_test = []


    for line in open(file_path):
        parts = line.decode(encoding='utf-8').strip().split('\t')
        category = parts[0]
        text = parts[1]

        if random.random() < prob_to_take:
            X_test.append(text)
            Y_test.append(cat_to_ind[category])


    X_test = vectorizer.transform(X_test)
    return X_test, Y_test





#create_model(model_file_name=model_file_path, vectorizer_file_name=vectorizer_file_path, print_logs=True)

#X_test, Y_test = get_me_some_test_samples(Utility.training_file_path, prob_to_take=0.1)
#model = get_persisted_model(model_file_path)
#score_classifier(model, X_test, Y_test)

"""
texts = []
for line in open('/Users/igorpetrovski/Desktop/test_tekstovi.txt'):
    print line
    print '----------------'
    texts.append(line)

vectorizer = get_persisted_vectorizer(vectorizer_file_path)
X_test = vectorizer.transform(texts)

model = get_persisted_model(model_file_path)

predictions = model.predict(X_test)


_, ind_to_cat = Utility.load_categories()

for i in xrange(0, len(texts)):
    print texts[i]
    print ind_to_cat[predictions[i]]

    print '---------------'
"""

