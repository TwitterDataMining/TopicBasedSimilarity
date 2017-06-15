import argparse
import os
import logging
import datetime
import itertools
from gensim import corpora, models


# Input arguments
PROGRAM_DESCRIPTION = "Read TV show tweets and analyse"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('prefix', type=str, help='Prefix of input files')
parser.add_argument('directory', type=str, help='Directory tv show')
parser.add_argument('output', type=str, help='Directory tv show')
args = vars(parser.parse_args())

def main():
    collection_name = args['prefix']
    dir_name = args['directory']
    output_dir = args['output']
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    filename = dir_name + "/" + collection_name +"_text.csv"
    output_file= output_dir + "/" + collection_name +"_text.csv"


    log_file = output_dir + '/' + collection_name + "lda_log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug("reading users fof topic modelling: {0} for hashtags : {1}".format(datetime.date.today(), collection_name))

    doc_gen = read_file_into_generator(filename)
    create_corpus(doc_gen, filename, output_file)


def create_corpus(doc_gen, filename, output_file):
    documents1, documents2 = itertools.tee(doc_gen)  # clone the generator
    # create a Gensim dictionary from documents
    dictionary = corpora.Dictionary(documents1)
    logging.debug("dictionary length {0}".format(len(dictionary)))
    # filter extremes
    dictionary.filter_extremes(no_below=1, no_above=0.5)
    logging.debug("dictionary length after extreme removal {0}".format(len(dictionary)))
    dictionary.save(output_file + '.dict')

    # convert the dictionary to a corpus
    corpus = [dictionary.doc2bow(doc) for doc in documents2]
    corpora.MmCorpus.serialize(output_file + '_corpus.mm', corpus)
    logging.debug("corpus written !!")

def read_file_into_generator(filename):
    print("reading {}".format(filename))
    with open(filename, 'r') as r:
        count = 0
        for line in r:
            count += 1
            if count % 1000 == 0:
                logging.debug("users done {0}".format(count))
            yield line.split()


if __name__ =="__main__":
    main()