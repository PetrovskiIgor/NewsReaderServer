__author__ = 'igorpetrovski'
__email__ = 'igor.tetovo@gmail.com'

from sklearn.feature_extraction.text import  TfidfVectorizer
from basic_classification import BasicClassificator
import Utility
from sklearn.linear_model import LogisticRegression
import time
import random


class LogReg(BasicClassificator):

    def __init__(self, categories):
        BasicClassificator.__init__(self, categories)
        self.vocabulary = Utility.load_vocabulary(num_words=100000)
        self.vectorizer = TfidfVectorizer(vocabulary=self.vocabulary)

   

    def train(self, input, output,vectorized=False):

        X, y = input, output
        begin = time.time()
        if not vectorized:
            print 'Vectorized the training set'
            X, y = self.transform_to_vector_space(input, output)


        self.model = LogisticRegression()
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
logistic_regression = LogReg(y)


logistic_regression.train(X_train, y_train, vectorized=False)

#score = svm.test_score(X_test, y_test, vectorized=False)


#print 'The score is: %.2f' % score

score = logistic_regression.test_score(X_test, y_test)

print 'Score: %.2f' % score

"""
num_correct = 0

for i in xrange(len(predictions)):
    if predictions[i] == knn.cat_to_ind[y_test[i]]:
        num_correct += 1




print 'Num correct: %d out of %d' % (num_correct, len(predictions))
print 'Percentage correct: %.2f' % (100.0*num_correct/len(predictions))
"""

#print digits_set.info

