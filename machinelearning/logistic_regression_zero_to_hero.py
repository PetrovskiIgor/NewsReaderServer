__author__ = 'igorpetrovski'

import math
import random
from sklearn import datasets
import numpy as np

class LogisticRegression:

    def __init__(self, num_features, alpha=0.1, num_classes=2):
        """
        :param num_features: the number of input neurons
        :param alpha: the learning rate (how much should it be??)
        :param num_classes: how many classes there are in the logistic regression
        :return:
        """

        self.alpha = alpha
        self.num_features = num_features
        self.num_classes = num_classes
        self.weights = []
        self.num_samples = 0

        for _ in xrange(num_features):
            #append a random weight on the range (-1,1)
            weight = random.random() - random.randint(0,2)
            self.weights.append(weight)


    def train(self, inputs, outputs, num_iterations=300):
        """
        The training function which i use to train the model which will later classify the inputs.

        Time Complexity:
        O(num_iterations * num_features * num_samples)

        :param inputs: training examples where each element is a vector of length self.num_features
        :param outputs: outputs for the training examples where the i-th output is the class for the i-th input
        """

        if len(inputs) != len(outputs):
            raise ValueError('train(): The length of the inputs is different from the length of outputs')

        self.num_samples = len(inputs)

        for it in xrange(num_iterations):

            if it % 10 == 0:
                print 'Iteration: %d' % it

            updated_weights = []

            for j in xrange(self.num_features):
               new_weight = self.weights[j] - self.alpha * self.derivative_loss(inputs, outputs, j)
               updated_weights.append(new_weight)

            self.weights = list(updated_weights)

    def loss(self, inputs, outputs):
        """
        Calculates the loss by the formula for logistic regression

        :param inputs: the samples over which we calculate the loss
        :param outputs: outputs[i] gives us the correct output for inputs[i]
        :return: returns the loss as a real number
        """

        num_samples = len(inputs)

        if num_samples == 0:
            print 'No training samples..'
            return

        loss = 0.0

        for ind in xrange(num_samples):
            loss_one = -outputs[ind]*math.log(self.h(inputs[ind])) - (1 - outputs[ind])*math.log(1 - self.h(inputs[ind]))

            if loss_one < 0.0:
                print 'ATTENTION!!! LOSS IS NEGATIVE!!! loss one: %.2f' % loss_one

            loss += loss_one

        loss /= (1.0 * num_samples)

        return loss

    def derivative_loss(self, inputs, outputs, j):
        """
        The derivate of the loss function, relative to the j-th feature
        :param inputs: the inputs which the derivate loss is calculated on
        :param outputs: the correct outputs
        :param j: the current feature j
        :return: the derivate loss for feature j
        """
        res = 0.0
        m = len(inputs)
        for ind in xrange(m):
            one_loss = (self.h(inputs[ind]) - outputs[ind]) * inputs[ind][j]
            res += one_loss

        res/= (1.0 * m)

        return res


    def h(self, input_vector):
        """
        :param input_vector: the X input vector
        :return: the result from the logistic regression
        """

        if len(input_vector) != self.num_features:
            raise ValueError('The length of the input vector is different that the number of features!')

        sum = 0.0

        for ind in xrange(self.num_features):
            sum += input_vector[ind] * self.weights[ind]


        output = self.sigmoid(sum)

        if(output < 0.0 or output > 1.0):
            print 'Output is not in the range [0.0, 1.0] !!!'
        return output

    def sigmoid(self, x):
        """
        g(x)
        for a given value as input returns the sigmoid/logistic function performed on that value as output
        :param x: x in the g(x)
        :return: g(x)
        """

        if x < -30:
            return 0.0
        if x > 30:
            return 1.0

        return 1.0/(1.0 + np.exp(-x))

    def classify(self, input_vector):
        """
        for a given vector as an input, returns the class (0 or 1)
        :param input_vector: the input features
        :return: the output class (0 or 1)
        """


        output = self.h(input_vector)



        if output >= 0.5:
            return 1

        return 0


def TestLogisticRegression():
    X, y = datasets.make_hastie_10_2(n_samples=1000,random_state=None)

    # da se testira dali X[i][0] pochnuva so 1 (za bias unit-ot)

    for i in xrange(len(y)):
        if y[i] == -1:
            y[i] = 0

    for _ in y:
        if _ != 0 and _ != 1:
            print 'Attention: %d' % _

    for i in xrange(len(X)):
        X[i] = [1] + X[i]

    num_features = len(X[0])

    model = LogisticRegression(num_features=num_features, alpha=0.001)

    model.train(X, y, 2000)


    testing_part = 20

    test_set_loss = model.loss(X[:-testing_part], y[:-testing_part])

    test_x, test_y = X[-testing_part:], y[-testing_part:]

    num_correct  = 0
    total = len(test_x)

    counter = [0, 0]
    for ind in xrange(len(test_x)):
        inp = test_x[ind]
        out = test_y[ind]

        answer = model.classify(inp)

        if answer == out:
            num_correct += 1

        counter[answer] += 1


    print 'Num correct: %d out of %d. Precision: %f' % (num_correct, total, num_correct*1.0/total)
    print 'Num ones: %d Num zeros: %d' % (counter[1], counter[0])
    print 'loss: %f' % test_set_loss


    print 'On training: '


    for ind in xrange(len(X[:-testing_part])):
        inp = X[ind]
        out = y[ind]

        answer = model.classify(inp)

        if answer == out:
            num_correct += 1

    total = len(X) - testing_part

    print 'Num correct: %d out of %d. Precision: %f' % (num_correct, total, num_correct*1.0/total)

    training_set_loss = model.loss(X[:-testing_part], y[:-testing_part])

    print 'Loss: %f' % training_set_loss



TestLogisticRegression()





