__author__ = 'igorpetrovski'

from sklearn.feature_extraction.text import  TfidfVectorizer
from basic_classification import BasicClassificator
import Utility
from sklearn.naive_bayes import MultinomialNB
import time
import random

class NaiveBayes(BasicClassificator):

    def __init__(self, categories):
        BasicClassificator.__init__(self, categories)
        self.vocabulary = Utility.load_vocabulary(num_words=100000)
        self.vectorizer = TfidfVectorizer(vocabulary=self.vocabulary, stop_words=Utility.stop_words)



    def train(self, input, output,vectorized=False):

        X, y = input, output

        if not vectorized:
            print 'Vectorized the training set'
            X, y = self.transform_to_vector_space(input, output)

        begin = time.time()
        self.model = MultinomialNB()
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

def cross_validation(nf=10):

    tuples = []
    for line in open(Utility.path_dataset):

        category, text = line.decode('utf-8').strip().split('\t')
        tuples.append((category, text))

    random.shuffle(tuples)


    num_folds=nf
    N = len(tuples)
    total_score = 0
    total_time = 0

    for i in xrange(num_folds):

        X, y = [], []

        X_train, y_train = [], []
        X_test, y_test = [], []


        begin = i * N/num_folds
        end = (i+1) * N/num_folds

        ind = 0
        for tuple in tuples:
            category, text = tuple[0], tuple[1]
            X.append(text)
            y.append(category)

            if begin <= ind and ind < end:
               X_test.append(text)
               y_test.append(category)
            else:
                X_train.append(text)
                y_train.append(category)

            ind += 1


        print 'Read the dataset'
        naive_bayes = NaiveBayes(y)

        begin = time.time()
        naive_bayes.train(X_train, y_train, vectorized=False)
        end = time.time()

        print '%d: %d seconds' % (i,end - begin)
        total_time += (end-begin)

        score = naive_bayes.test_score(X_test, y_test)
        score_perc = score * 100

        print '%d: Score: %.2f\n' % (i, score_perc)

        total_score += score_perc


    avg_score = total_score*1.0/num_folds
    avg_time = (total_time*1.0)/num_folds
    print 'Average score: %.2f' % avg_score
    print 'Average training time: %.2f' % avg_time

cross_validation(nf=10)

"""

X, y = [], []

X_train, y_train = [], []
X_test, y_test = [], []


counter = 0

tuples = []
for line in open(Utility.path_dataset):

    category, text = line.decode('utf-8').strip().split('\t')
    tuples.append((category, text))

random.shuffle(tuples)


#num_tuples = 50000

#tuples = tuples[:num_tuples]

for tuple in tuples:
    category, text = tuple[0], tuple[1]
    X.append(text)
    y.append(category)

    if random.random() <= 0.2:
       X_test.append(text)
       y_test.append(category)
    else:
        X_train.append(text)
        y_train.append(category)


print 'Read the dataset'
naive_bayes = NaiveBayes(y)


naive_bayes.train(X_train, y_train, vectorized=False)
score = naive_bayes.test_score(X_test, y_test)
print 'score: %.2f' % score
#score = svm.test_score(X_test, y_test, vectorized=False)


#print 'The score is: %.2f' % score

predictions = naive_bayes.predict(X_test)

num_correct = 0

for i in xrange(len(predictions)):
    if predictions[i] == naive_bayes.cat_to_ind[y_test[i]]:
        num_correct += 1




print 'Num correct: %d out of %d' % (num_correct, len(predictions))
print 'Percentage correct: %.2f' % (100.0*num_correct/len(predictions))

#print digits_set.info
"""

