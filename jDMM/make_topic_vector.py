"""
STEP-2
read the list of username, topic
return a dict username: topic vector

"""
import argparse
import pickle
import pandas as pd
import logging

# Input arguments
PROGRAM_DESCRIPTION = "Read the topic asignment file from jLDADMM algorithm and creates the topic vectors"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('filename', type=str, help='user_topic_pickle')
parser.add_argument('topicdict', type=str, help='user_topic_pickle')
parser.add_argument('logfile', type=str, help='user_topic_pickle')
args = vars(parser.parse_args())


def main():
    print("some")

    user_topic_list = args['filename']
    topic_result = args['topicdict']
    log_file = args['logfile']
    topic_count = 20

    list_user = pickle.load(open(user_topic_list, 'rb'))

    # create log file
    # log_file = user_topic_list.rpartition('/')[0] + "log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug("make topic vector for {0} ".format(user_topic_list))
    # print(list_user)
    df = pd.DataFrame(list_user)
    #print(df[:5])
    grouped_df = df.groupby(['userid'])

    dict = {}
    count = 0
    for key, item in grouped_df:
        count += 1
        #print ("key: " + key)
        gf = item.groupby('topic').size()
        topics = [str(x) for x in range(0, topic_count)]
        #print(topics)
        # topics = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10','11', '12',
        #           '13', '14', '15', '16', '17', '18','19']
        topic_Dict = gf.to_dict()
        topic_vec = []
        total = 0
        for one_topic in topics:
            if one_topic  in topic_Dict:
                topic_vec.append(topic_Dict[one_topic])
                total += topic_Dict[one_topic]
            else:
                topic_vec.append(0)
        #print(topic_vec)
        discarded_count = 0
        if total == 0:
            discarded_count += 1
            #print("user: ", key , " discarded")
            continue;
        if count % 1000 == 0:
            logging.info("users donr : {} ".format(count))
        finallist = [float(x)/float(total) for x in topic_vec]

        # change list to dict
        list_dict = {}
        for idx, val in enumerate(finallist):
            if val > 0:
                list_dict[idx] = val

        dict[key] = list_dict
        #logging.debug("discarded {}".format(discarded_count))
        pickle.dump( dict, open(topic_result, 'w'))







if __name__ == '__main__':
    main()