__author__ = 'igorpetrovski'

import random
import Utility


def create_num_samples(data_path,  file_path_dest, num_samples=10000):
    print 'at beginning..'

    sentences = []
    set_added = set()

    counter = 0

    print 'begin'
    for line in open(data_path):

        line = line.decode('utf-8').strip()
        sentences.append(line)

        counter += 1

    print 'read the set'


    final_set = []

    for i in xrange(num_samples):

        if i % 500: print 'iteration %d' % i
        while True:
            m = random.randint(0, counter)

            if m not in set_added:
                final_set.append(sentences[m])
                set_added.add(m)
                break


    print 'Done!'


    file_to_write = open(file_path_dest, 'w')

    for sent in final_set:
        file_to_write.write((sent + '\n').encode('utf-8'))

    file_to_write.close()



input_file = '/Users/igorpetrovski/Desktop/za_salka.txt'

counter = 0
for x in open(input_file):
    if counter % 500:
        print x

    counter += 1