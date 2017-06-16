"""
Takes topic vectors and pair_file to calculate similarity between the pairs of users in the pair file
input :
    topic vector file : the pickled file - a dictionary of topic vector c
    user pair file : csv containing pairs to calculate similarity ; followinf format in each line:
                    userid1 , userid2
    name_of result folder

output:
    write similarity between pairs in result folder ( pickled dict)
    created histogram  for similarity distribution
    writes mean similarity in log file

"""
import argparse
import pickle
import logging
import datetime
from gensim import matutils
import os

import math
import numpy as np
from matplotlib import pyplot as plt
import scipy.stats
# Input arguments
PROGRAM_DESCRIPTION = "Read tweets from collection"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('topic_vector', type=str, help='path to topic vector pickle file')
parser.add_argument('pair_file', type=str, help='filepath for pairs')
parser.add_argument('sim', type=str, help='simi directory')
args = vars(parser.parse_args())


def main():
    user_dict_file = args['topic_vector']
    pair_file = args['pair_file']
    sim_dir= args['sim']

    pair_file_name = os.path.basename(pair_file).split('.')[0]
    dir_name = user_dict_file.rpartition('/')[0]
    result_dir = dir_name + "/" + sim_dir

    try:
        os.stat(result_dir)
    except:
        os.mkdir(result_dir)



    print(user_dict_file)
    user_dict = pickle.load(open(user_dict_file, 'rb'))
    print(user_dict)

    log_file = result_dir + "/"+ pair_file_name + "_similarity_logs"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, filemode='w', format='%(asctime)s %(message)s')
    logging.debug("begin similarity measure : {0}  for {1}".format(datetime.date.today(), pair_file_name))
    calculate_similarities(user_dict, pair_file, result_dir)


def calculate_similarities(user_dict, pair_file, result_dir):
    result_dict_dir = result_dir + "/simdict"
    try:
        os.stat(result_dict_dir)
    except:
        os.mkdir(result_dict_dir)

    pair_file_name = os.path.basename(pair_file).split('.')[0]
    total_cosine = 0
    total_pearson = 0
    count_sims = 0
    count_sims2 = 0
    count_all = 0
    keys = user_dict.keys()
    sim_dict = {}
    sim_dict2 = {}
    count_sims_p = 0

    with open(pair_file, 'r') as f:
        for line in f:
            count_all += 1
            user1, user2 = line.strip().split(',')

            user1 = user1.strip()
            user2 = user2.strip()
            if user1 in keys and user2 in keys:

                topic1 = dict(user_dict[user1])
                topic2 = dict(user_dict[user2])
                keys_inner = list(topic1.viewkeys() | topic2.viewkeys())  # get all common keys

                sim = matutils.cossim(topic1, topic2)
                total_cosine += sim
                try:
                    sim2 = scipy.stats.pearsonr(
                        [topic1.get(x, 0) for x in keys_inner],
                        [topic2.get(x, 0) for x in keys_inner])
                    if not math.isnan(sim2[0]):
                        total_pearson += sim2[0] # take only the mean ignore stad dev
                        count_sims_p += 1
                except:
                    pass
                count_sims += 1

                sim_dict[(user1,user2)] = sim
                sim_dict2[(user1, user2)] = sim2

    logging.debug("Cosine Similarity=======>")
    logging.debug("total of similarities : {}".format(total_cosine))
    logging.debug("count of similarity available : {}".format(count_sims))
    logging.debug("out of total user pairs : {}".format(count_all))
    logging.debug("=================================================")
    logging.debug("Average Similarity : {}".format(total_cosine/count_sims))
    logging.debug("=================================================")

    logging.debug("Pearson Similarity=======>")
    logging.debug("total of similarities : {}".format(total_pearson))
    logging.debug("count of similarity available : {}".format(count_sims_p))
    logging.debug("out of total user pairs : {}".format(count_all))
    logging.debug("=================================================")
    logging.debug("Average Similarity : {}".format(total_pearson/count_sims_p))
    logging.debug("=================================================")

    sim_dict_name1 = result_dict_dir +"/similarity_dict_cosine" + pair_file_name + ".p"
    sim_dict_name2 = result_dict_dir + "/similarity_dict_pearson_" + pair_file_name + ".p"
    with open(sim_dict_name1, 'wb') as f:
        pickle.dump(sim_dict, f)
    with open(sim_dict_name2, 'wb') as f:
        pickle.dump(sim_dict2, f)

    similarity_list_cosine = plot_results(sim_dict, sim_dict_name1, False)
    similarity_list_pearson = plot_results(sim_dict2, sim_dict_name2, True)

    logging.debug("Cosine Similarity Discriptive=======>")
    logging.debug(scipy.stats.describe(similarity_list_cosine))
    logging.debug("Cosine Similarity Discriptive=======>")
    logging.debug(scipy.stats.describe(similarity_list_pearson))






def plot_results(similarity_dict, sim_dict_name, tuple=True):
    values = []
    print(similarity_dict.values())
    for value in similarity_dict.values():
        if tuple:
            if not np.isnan(value[0]):
                values.append(value[0])
            else:
                continue
        else:
            if value is not None:
                values.append(value)
            else:
                "found one"
    new_values = sorted(values)

    #print(new_values)

    title = sim_dict_name.rpartition('/')[2]
    axes = plt.gca()
    axes.set_ylim([0, 500])
    plt.hist(new_values)
    plt.title(title)

    plt.ylabel('Frequency')
    plt.xlabel('similarity')
    plt.savefig(sim_dict_name.rpartition('.')[0] + ".png")
    #plt.show()
    plt.clf()
    return new_values





if __name__ == "__main__":
    main()