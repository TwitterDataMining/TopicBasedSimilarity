"""
Trains word2vector from the corpus file
input :
    1. corpus file : containing preprocessed tweets as documents,
        the format of the file needs to be:
        username, preprocess tweet text
    2. log file name : to store the logging information.

output : trained word to vector model
"""
import gensim, logging
import datetime


# Input arguments
PROGRAM_DESCRIPTION = "Create word vectors"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('document_file', type=str, help='file containing preprocessed tweets')
parser.add_argument('log_file', type=str, help='log file for writting logs')
args = vars(parser.parse_args())

def main():
    filename = args['document_file']
    log_file = args['log_file']
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug("creating word2vec for {} : {}".format(filename ,datetime.date.today()))
    parts = filename.rpartition('/')
    outputfile = parts[2].rpartition('.')[0]
    outputfolder = parts[0]
    sentences = Sentences(filename)
    model = gensim.models.Word2Vec(sentences, workers=4, min_count=1)
    model.save(outputfolder + "/" + outputfile + "_word2vec.model")


class Sentences:
    """

    """
    def __init__(self, filename):
        self.f = open(filename, 'r')

    def __iter__(self, loc=-1):
        for line in self.f:
            parts = line.split(',')
            yield parts[loc].strip().split(' ')




if __name__ == "__main__":
    main()