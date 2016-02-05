#encoding=utf-8

import math
from cPickle import Pickler

def isInStopWords(word):
    return word in stopWords




stopWords = set(['сте', 'ве', 'ви', 'вие', 'вас', 'но', 'го', 'а', 'е', 'на', 'во', 'и', 'ни', 'ние', 'или',
'та', 'ма', 'ти', 'се', 'за', 'од', 'да', 'со', 'ќе', 'дека', 'што', 'не', 'ги', 'ја', 'јас',
'тие', 'тоа', 'таа', 'тој', 'мк', 'отсто', 'гр', 'мл', 'тв', 'ул', 'врз', 'сите', 'иако', 'друг', 'друга',
'при', 'цел', 'меѓу', 'околу', 'нив', 'кои', 'кога', 'поради', 'има', 'без', 'биле', 'она', 'кое', 'кај',
'овој', 'него', 'некои', 'оваа', 'веќе', 'оние', 'уште', 'може', 'меѓутоа',
'the', 'of', 'in', 'and', 'is', 'a', 'to', 'are', 'for', 'that', 'all', 'an', 'i', 'on',
'fg', '3p', 'ft', 'reb', 'pos', 'pts', 'min', 'eff', 'bs', 'pf', 'am', 'pm', '3rd', '4th', '5th', '6th', 'nbsp'
                 'kurir', 'црнобело', 'kanal5'])



str_idf_dict = 'dict_idf'
path_dataset = '/Users/igorpetrovski/Desktop/7 semestar/NLP/dataset-hw.txt'

def getWords(line):
  line = line.lower()
  out = []
  word = []

  for c in line:
    if c.isalpha():
      word.append(c)
      continue
    else:
      if word:
        newWord =  ''.join(word).lower()

        if not isInStopWords(newWord):

            if len(newWord) > 6:
                newWord = newWord[0:6]
            out.append(newWord)
      word = []
  if word:
        newWord =   ''.join(word).lower()

        if not isInStopWords(newWord):
            if len(newWord) > 6:
                newWord = newWord[0:6]

            out.append(newWord)
  return out


def calculate_idf_dictionary(fileName):

    numDocuments = 0

    dictWords = {}
    for line in open(fileName):
        parts = line.decode('utf-8').strip().split('\t')

        category = parts[0] #unimportant for now..
        text = parts[1]

        words = set(getWords(text))


        for word in words:
            dictWords[word] = 1 + dictWords.get(word, 0)

        numDocuments += 1

        if numDocuments % 1000 == 0:
            print 'processed %d number of documents' % numDocuments

    for word in dictWords:
        dictWords[word] = math.log(numDocuments / (dictWords[word] * 1.0))


    print 'number of words: ', len(dictWords)
    print 'number of documents: ', numDocuments

    fileToWrite = open(str_idf_dict, 'w')
    Pickler(fileToWrite).dump(dictWords)
    fileToWrite.close()


#calculate_idf_dictionary(path_dataset)




