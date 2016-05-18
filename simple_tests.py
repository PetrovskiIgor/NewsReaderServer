__author__ = 'igorpetrovski'


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


print test_substring('igorr', 'igo')







