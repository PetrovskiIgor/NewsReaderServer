__author__ = 'igorpetrovski'

import numpy as np


class LogisticRegression:

    def softmax(self, W, b, x):
        """
        N - number of features
        M - number of classes
        :param W:  MxN matrix where the i-th row represents the weights associated with the i-th class
        :param b: the bias units for each class Mx1 vector
        :param x: the input vector with dimension N
        :return: returns a vector with probabilities that x belongs to each class. the vector has shape: (M,1) - M rows 1 column
        """
        #we get the values b1x1 + b2x2 + ... +bnxn for each of the M classes
        vec = np.dot(x, W.T)
        #add the biases b0 for each of the classes
        vec = np.add(vec, b)

        #we bring the values to an exponent
        exp_vec = np.exp(vec)

        sum_of_exps = np.sum(exp_vec, axis=1)

        res = exp_vec.T /sum_of_exps

        return res

    def predict(self, x):
        """

        :param x: the input vector that needs to be classified
        :return: the output vector with dimensions Mx1 that gives as the class probabilities
        """

        y = self.softmax(self.W, self.b, x)
        return y

    def label(self, y):
        """
        for a given class y returns the name of that class
        :param y: the index of the class
        :return: the name of the class
        """

        return self.labels[y]

    def classify(self, x):

        predictions = self.predict(x)

        max = 0.0
        max_ind = -1
        i=0
        for elem in predictions:
            if elem[0] > max:
                max = elem[0]
                max_ind = i

            i += 1

        return self.label(max_ind)




arr = np.array([[1],[4],[3],[2],[1]])

print arr.max(axis=1)
