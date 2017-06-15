"""
input : 1. word vectors file
            format:  word followed by vector separated by space only :
                word vector
            eg:
            man 0.31553 0.53765 0.10177 0.032553 0.003798 0.015364 -0.20344 0.33294 -0.20886 0.10061 0.30976 0.50015
            women 0.1911 0.24668 -0.060752 -0.43623 0.019302 0.59972 0.13444 0.012801 -0.54052 0.27387 -1.182 -0.27677
        2. Input data to be filter
            one document per line - words separated by space

output :
        one document per line - words separated by space and words not in the vecto removed

Use : when pretrained word2vec is used

"""
import logging

def main():
    filename = "../data_gathering/24Legacy1000/24Legacy1000_text.csv"
    #vector_file = "../data/glove_vector/glove.twitter.27B.200d.txt"
    vector_file = "data/24Legacy1000/24Legacy1000_username_word2vec.model.txt"
    log_file = filename.rpartition('.')[0] + "_remove_uncommon.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    make_clean_file(filename, vector_file)


def make_vector_words_set(filename):
    vector = set()
    with open(filename) as open_file:
        for each_line in open_file:
            vector.add(each_line.split(' ')[0])
    return vector


def clean_sentences(sentence, vector):
    common_words = []
    not_found = 0
    word_count = 0
    removed_words = set()
    for each_word in sentence.strip().split(' '):
        word_count += 1
        if each_word in vector:

            common_words.append(each_word)
        else:
            removed_words.add(each_word)
            not_found += 1
    print "found: {}, notfound : {}".format(word_count, not_found)
    return " ".join(common_words), word_count, not_found, " ".join(removed_words)



def make_clean_file(filename, vector_file):
    vectors = make_vector_words_set(vector_file)
    total_not_found = 0
    total_words = 1
    with open(filename, 'r') as read_file, open(filename + "_clean_trained1.txt", 'w') as write_file, open(filename + "_discarded1.txt", 'w') as dis_file:
        for each_Sentence in read_file:
            clean_sentence, words, n_words, removed = clean_sentences(each_Sentence, vectors)
            total_not_found += n_words
            total_words += words
            write_file.write(clean_sentence + '\n')
            dis_file.write(removed + '\n')
    logging.info("words: {}, notfound : {} ({} %)".format(total_words, total_not_found,
                                                          float(total_not_found)/total_words*100))


if __name__ == "__main__":
    main()


