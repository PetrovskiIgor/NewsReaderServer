__author__ = 'igorpetrovski'
__email__ = 'igor.tetovo@gmail.com'


from pybrain.datasets import ClassificationDataSet
from sklearn.feature_extraction.text import TfidfVectorizer
import Utility
import random
import numpy as np
import time
import sklearn

print 'Version: ', sklearn.__version__



begin = time.time()
idf_dict = Utility.get_idf_dictionary()
print 'Loaded for %d seconds.' % (time.time() - begin)

print len(idf_dict)



"""
X, y = [], []

X_train, y_train = [], []
X_test, y_test = [], []


counter = 0

tuples = []
categories = set()
for line in open(Utility.path_dataset):

    category, text = line.decode('utf-8').strip().split('\t')
    tuples.append((category, text))
    categories.add(category)

    counter += 1

    if counter > 100: break

categories = list(categories)
cat_to_ind= {}
ind = 0
for c in categories:
    cat_to_ind[c] = ind
    ind += 1

random.shuffle(tuples)


#num_tuples = 100000

#tuples = tuples[:num_tuples]

for tuple in tuples:
    category, text = tuple[0], tuple[1]
    X.append(text)
    y.append(category)

    if random.random() <= 0.35:
       X_test.append(text)
       y_test.append(category)
    else:
        X_train.append(text)
        y_train.append(category)

print 'Read the dataset'

vectorizer = TfidfVectorizer(vocabulary=Utility.load_vocabulary(num_words=100000),stop_words=Utility.stop_words)



X = vectorizer.fit_transform(X)





print X.shape[0]
print y[0]
"""


