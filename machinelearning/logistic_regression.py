#encoding=utf-8
__author__ = 'igorpetrovski'

import time
import numpy as np
import matplotlib.pyplot as plt
import random
import Utility

from sklearn.feature_extraction.text import TfidfVectorizer


from sklearn import linear_model
from sklearn import datasets

def classify(points, weights):

    if len(points) != len(weights):
        raise ValueError('The length of the points and the length of the weights are not the same! length points: %d length weights: %d' % (len(points, len(weights))))


    sum = 0.0
    for i in xrange(len(points)):
        sum += points[i] * weights[i]


    return sigmoid(sum)

def sigmoid(val):
    pass


def statistics_classes(file_name):

    begin = time.time()
    classes = {}
    total = 0
    for line in open(file_name):
        parts = line.strip().split('\t')
        classes[parts[0]] = 1 + classes.get(parts[0], 0)
        total += 1


    tuples = sorted([(c, classes[c]) for c in classes], key=lambda x: -x[1])

    for tuple in tuples:
        print '%s\t%.2f' % (tuple[0], tuple[1] * 100.0 / total)

    print 'TOTAL: %d' % total

    print 'Done for %d seconds' % (time.time() - begin)


def info_for_dataset(dataset):


    i = 0
    for dim in dataset:
        i += 1
        print 'Iteration: %d\t Name: %s' % (i, dim)
        print dataset[dim]

    print 'Dimension of iris: %d' % len(dataset)


def plot_iris():
    print(__doc__)


    # Code source: Gaël Varoquaux
    # Modified for documentation by Jaques Grobler
    # License: BSD 3 clause



    # import some data to play with
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # we only take the first two features.
    Y = iris.target

    h = .02  # step size in the mesh

    logreg = linear_model.LogisticRegression(C=1e5)

    # we create an instance of Neighbours Classifier and fit the data.
    logreg.fit(X, Y)

    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, m_max]x[y_min, y_max].
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    Z = logreg.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1, figsize=(4, 3))
    plt.pcolormesh(xx, yy, Z, cmap=plt.cm.Paired)

    # Plot also the training points
    plt.scatter(X[:, 0], X[:, 1], c=Y, edgecolors='k', cmap=plt.cm.Paired)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')

    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.xticks(())
    plt.yticks(())

    plt.show()


def logistic_regression_classification(data_set, print_logs=True):
    data_set = datasets.load_digits()

    inputs = data_set.data
    outputs = data_set.target

    num_samples = len(inputs)
    X_train = []#np.array([])#inputs[:0.9*num_samples]
    Y_train = []#np.array([])#outputs[:0.9*num_samples]

    X_test = []#np.array([])#inputs[0.9*num_samples:]
    Y_test = []#np.array([])#outputs[0.9*num_samples:]

    for i in xrange(num_samples):
        if random.random() < 0.1:
            #add it to test set
            X_test.append(inputs[i])
            Y_test.append(outputs[i])

        else:
            #add it to training set
            X_train.append(inputs[i])
            Y_train.append(outputs[i])

    if print_logs:
        print 'Training size: %d %d' % (len(X_train), len(Y_train))
        print 'Test size: %d %d' % (len(X_test), len(Y_test))

    begin = time.time()
    logistic = linear_model.LogisticRegression()

    if print_logs:
        print 'max iterations: %d' % logistic.max_iter
        print 'Loaded logistic regression model for %d seconds' % (time.time() - begin)
    begin = time.time()
    logistic.fit(X_train, Y_train)

    if print_logs:
        print 'Training ended for %d seconds' % (time.time() - begin)
    score = logistic.score(X_test, Y_test)

    if print_logs:
        print 'The score is: %f' % score

    return score

"""
list_datasets = [datasets.load_mlcomp('20news-18828', 'train'),datasets.load_digits(), datasets.load_iris(), datasets.load_boston(), datasets.load_breast_cancer(), datasets.load_diabetes()]


total_scores = 0
for dataset in list_datasets:
    score = logistic_regression_classification(dataset,print_logs=False)
    print 'Score:\t%f' % (score)
    total_scores += score

print 'Average score: %f' % (total_scores/(1.0 * len(list_datasets)))
#logistic_regression_classification(datasets.())
"""

#text_dataset = datasets.load_mlcomp('20news-18828', 'train')

def tf_idf_vectorization():
    t_total = time.time()
    t0 = time.time()
    cat_to_ind = {}
    ind_to_cat = []

    curr_cat_ind = 0

    X_train = []
    Y_train = []

    X_test = []
    Y_test = []

    for line in open(Utility.training_file_path):
        parts = line.decode(encoding='utf-8').strip().split('\t')
        category = parts[0]
        text = parts[1]

        if category not in cat_to_ind:
            cat_to_ind[category] = curr_cat_ind
            ind_to_cat.append(category)
            curr_cat_ind += 1

        item = [text, cat_to_ind[category]]
        if random.random() < 0.0:
            #for testing
            X_test.append(item[0])
            Y_test.append(item[1])
        else:
            #for training
            X_train.append(item[0])
            Y_train.append(item[1])

    print 'Read the dataset for %d seconds' % (time.time() - t0)



    vectorizer = TfidfVectorizer(encoding='utf-8', lowercase=True,stop_words=Utility.stop_words)

    t0 = time.time()
    X_train = vectorizer.fit_transform(X_train)


    X_train_2 = []
    Y_train_2 = []
    i = 0
    for item in X_train:
        if random.random() < 0.1:
            X_test.append(X_train[i])
            Y_test.append(Y_train[i])
        else:
            X_train_2.append(X_train[i])
            Y_train_2.append(Y_train[i])
        i+= 1

    print 'Vectorized the train and test set for %d seconds' % (time.time()-t0)


    classifier = linear_model.LogisticRegression()

    t0 = time.time()
    classifier.fit(X_train_2, Y_train_2)

    print 'Trained the model for %d seconds' % (time.time() - t0)

    t0 = time.time()
    score = classifier.score(X_test, Y_test)

    print 'Calculated score for %d seconds' % (time.time() - t0)

    print 'Score: %.2f' % score
    """
    """
    print 'Total time in seconds: %d' % (time.time() - t_total)









tf_idf_vectorization()
