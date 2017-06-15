import argparse
import logging
import datetime
from gensim import corpora, models
import pyLDAvis.gensim


# Input arguments
PROGRAM_DESCRIPTION = "Run LDA"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('collection_name_prefix', type=str, help='prefix of the files')
parser.add_argument('directory', type=str, help='Directory of tv show')
parser.add_argument('topics', type=str, help='Number of topics')
parser.add_argument('passes', type=str, help='Number of passes')
args = vars(parser.parse_args())


def main():
    collection_name = args['collection_name_prefix']
    dir = args['directory']
    topics = args['topics']
    passes = args['passes']


    filename =  dir + "/" + collection_name +"_text.csv"

    lda_result_file = dir + "/" + collection_name +  "lda_results.csv"
    log_file = dir + '/' + collection_name + "lda_log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug("reading users fof topic modelling: {0} for hashtags : {1}".format(datetime.date.today(), collection_name))


    dict_file = filename + ".dict"
    corpus_file = filename + "_corpus.mm"

    dictionary = corpora.Dictionary.load(dict_file)
    corpus = corpora.MmCorpus(corpus_file)

    lda, corpus, dictionary= runLDA(lda_result_file, dictionary, corpus, topics, passes)
    lda.save(dir + '/lda.gensim')
    file_html = dir + "/" + collection_name + "_visualize.html"
    followers_data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.display(followers_data)
    pyLDAvis.save_html(followers_data, file_html)

def runLDA(lda_result_file, dictionary, corpus, topics=20, passes=20):
    rf = open(lda_result_file, 'w')
    rf.write("Dictionary size is %d\n" % len(dictionary))
    rf.write("corpus size is %d\n" % len(corpus))
    rf.write("topics : {}\n".format(str(topics)))
    rf.write("passes : {}\n".format(str(passes)))
    rf.write("------------------------------------\n")

    # train the lda model
    lda = models.LdaModel(corpus, id2word=dictionary,
                          num_topics=int(topics),
                          passes=int(passes))


    # write the topics to file
    lda.show_topics()
    topics_matrix = lda.show_topics(formatted=False, num_words=20, num_topics=topics)
    count = 0
    for topic in topics_matrix:
        print topic[1]
        rf.write("Topic %d :" % count)
        rf.write(" ".join([x for x, _ in topic[1]]).encode("utf-8"))
        rf.write("\n")
        count += 1
    rf.write("-----------------------------------\n")
    rf.close()
    return lda, corpus, dictionary

if __name__ == "__main__":
    main()