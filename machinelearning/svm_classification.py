__author__ = 'igorpetrovski'

import time
import random

from sklearn.svm import SVC
from sklearn.feature_extraction.text import  TfidfVectorizer
import Utility
from basic_classification import BasicClassificator

class SVM(BasicClassificator):

    def __init__(self,categories, vocabulary=None):

        BasicClassificator.__init__(self, categories)

        if vocabulary is None:
            print 'Loading vocabulary..'
            self.vocabulary = Utility.load_vocabulary(num_words=100000)
        else:
            self.vocabulary = vocabulary

        self.vectorizer = TfidfVectorizer(vocabulary=self.vocabulary, stop_words=Utility.stop_words)

        print 'Vocabulary size: %d' % len(self.vocabulary)

    def transform_to_vector_space(self, inputs, outputs):

        X = []
        y = []


        X = self.vectorizer.fit_transform(inputs)

        for output in outputs:
            y.append(self.cat_to_ind[output])


        return X, y

    def train(self, input, output,vectorized=False):

        X, y = input, output

        if not vectorized:
            print 'Vectorized the training set'
            X, y = self.transform_to_vector_space(input, output)

        begin = time.time()
        self.model = SVC(gamma=0.001)
        print 'Created the model for training'
        self.model.fit(X, y)


        print 'Training Ended for %d seconds.' % (time.time() - begin)


    def test_score(self, input, output, vectorized=False):

        X, y = input, output

        if not vectorized:
            print 'Vectorized the test set'
            X, y = self.transform_to_vector_space(input, output)

        score = self.model.score(X, y)

        return score

    def predict(self, input, vectorized = False):

        X = input

        if not vectorized:
            X, _ = self.transform_to_vector_space(input, [])

        predictions = self.model.predict(X)

        return predictions


X, y = [], []

X_train, y_train = [], []
X_test, y_test = [], []


counter = 0

tuples = []
for line in open(Utility.path_dataset):

    category, text = line.decode('utf-8').strip().split('\t')
    tuples.append((category, text))

random.shuffle(tuples)


num_tuples = 50000

tuples = tuples[:num_tuples]

for tuple in tuples:
    category, text = tuple[0], tuple[1]
    X.append(text)
    y.append(category)

    if random.random() <= 0.1:
       X_test.append(text)
       y_test.append(category)
    else:
        X_train.append(text)
        y_train.append(category)


print 'Read the dataset'
svm = SVM(y)


svm.train(X_train, y_train, vectorized=False)

#score = svm.test_score(X_test, y_test, vectorized=False)


#print 'The score is: %.2f' % score

predictions = svm.predict(X_test)

num_correct = 0

for i in xrange(len(predictions)):
    if predictions[i] == svm.cat_to_ind[y_test[i]]:
        num_correct += 1




print 'Num correct: %d out of %d' % (num_correct, len(predictions))
print 'Percentage correct: %.2f' % (100.0*num_correct/len(predictions))

#print digits_set.info
