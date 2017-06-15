from pymongo import  MongoClient
import argparse
from gensim import corpora, matutils, models
import csv
import pickle


# Input arguments
PROGRAM_DESCRIPTION = "Create topic vectors"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('prefix', type=str, help='name of collection eg ThisIsUs_o')
parser.add_argument('directory', type=str, help='path to gensim lda output')
parser.add_argument('data_input_dir', type=str, help='path to preprocesses raw data')
args = vars(parser.parse_args())


def main():
    collection_name = args['prefix']
    dir_name = args['directory']
    input_dir = args['data_input_dir']

    dir = dir_name
    filename = input_dir + "/" + collection_name + "_username.csv"
    dict_name = dir + "/" + collection_name + "_text.csv.dict"
    lda_file = dir +  "/lda.gensim"

    print("lda " , lda_file)

    user_data = read_file(filename)
    dict = corpora.Dictionary.load(dict_name)
    lda = models.LdaModel.load(lda_file)

    topic_dict = {}
    topic_file = dir + "/" + collection_name + "_topic_vectors.csv"
    topic_pickle = dir + "/" + collection_name + "_topic_vectors.p"
    count = 0;
    with open(topic_file, 'w') as f:
        fieldnames = ['user', 'topic']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for user, vec in user_data:
            count += 1
            entry = {}
            entry['user'] = user
            words = vec.split()
            vec_bow = dict.doc2bow(words)
            topics = lda[vec_bow]
            topic_dict[user] = topics
            entry['topic'] = topics
            writer.writerow(entry)
            if count % 1000 == 0:
                print ("done : {}".format(count))

    with open(topic_pickle, 'w') as f:
        pickle.dump(topic_dict, f)


def read_file(filename):
    with open(filename, 'r') as f:
        for each_line in f:
            yield each_line.split(',')

if __name__ == "__main__":
    main()