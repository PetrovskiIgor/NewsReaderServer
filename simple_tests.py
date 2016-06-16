#encoding=utf-8
__author__ = 'igorpetrovski'


class BaseClass:

    def __init__(self,a):
        print 'BaseClass sucessful..'
        self.a = a

class DerivedClass(BaseClass):

    def __init__(self,a=5):
        BaseClass.__init__(self, a)

        print 'DerivedClass successful..'



from machinelearning import naivebayes_classification
#here we can try some offline tests

def extending_array(arr):

    for elem in arr:
        print elem,

    print

    arr.extend(arr)

    for elem in arr:
        print elem,

    print


def test_substring(main_string, subtext):


    return main_string.find(subtext)



def printType(iterable):

    if isinstance(iterable,list):
        print 'IT IS LIST!!!'
    else:
        if isinstance(iterable,dict):
            print 'It is dict!'
        else:
            print 'It is not list. It is not dict. It is a: '
            print type(iterable)







