"""
Reads the interactions from collection in Mongodb and pair files from a folder
and outputs the interaction statistics between the pairs

input :
    folder_name     :    which contains csv files with pairs of users for whom the interaction
                        statistics need to be calculated
    collection_name :   This collection in database stores interaction counts for every user
                        Following example shows the format of one document in the collection
                        {
                            "id" : 2783728
                            "interactions" : {
                                "347882" : 3
                                "377828" : 5
                            }
                            "hashtags" : [ "somehashtag1", "somehashtag2"]
                            "retweets" : {
                                "347882" : 3
                                "377828" : 5
                            }
                            "replies" :{
                                "347882" : 3
                                "377828" : 5
                            }
                            "quotes" :{
                                "347882" : 3
                                "377828" : 5
                            }
                            "mentions" : {
                                "347882" : 3
                                "377828" : 5
                            }
                        }
   output : write the interactions between the pairs in csv,
            which can be reloaded as pandas df
            columns include : hashtags_jac, interactions, interactions_jac, mentions,
                              mentions_jac, quotes,quotes_jac, replies, replies_jac ,
                              retweets,retweets_jac

            for each pair file in folder one output file is writen with suffix "_stats"


"""
from pymongo import MongoClient
import os
import logging
import pandas as pd
import glob


LOG_FILE = "interaction_stats.log"


# Input arguments
PROGRAM_DESCRIPTION = " Create interaction similarity for pairs"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('coll', type=str, help='collection of interactions')
parser.add_argument('pair_dir', type=str, help='directory which contains csv files with pairs of users')
args = vars(parser.parse_args())

def main():
    COLL = args['coll']
    DEST_DIR = args['pair_dir']

    db = get_mongo_connection()
    coll = db[COLL]

    try:
        os.stat(DEST_DIR)
    except:
        os.mkdir(DEST_DIR)
    logging.basicConfig(filename=DEST_DIR + "/" + LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')
    pair_files = get_files_from_folder(DEST_DIR)
    for file in pair_files:
        df = make_stats(file, coll, DEST_DIR)


def get_files_from_folder(folder):
    # get data file names
    filenames = glob.glob(folder + "/*.csv")
    print(filenames)
    return filenames


def make_stats(pair_file, coll, dest):
    dest = dest + "/inter"
    try:
        os.stat(dest)
    except:
        os.mkdir(dest)
    l = []
    newfile = dest + "/" + pair_file.rpartition('.')[0].rpartition('/')[2] + '_stats.csv'
    count = 0
    with open(pair_file, 'r') as f:
        for line in f:
            user1, user2 = line.strip().split(',')
            query1 = {'id': (int)(user1.strip())}
            query2 = {'id': (int)(user2.strip())}
            test1= coll.find_one(query1)
            test2 =coll.find_one(query2)
            d = calculate_stats(test1, test2)
            l.append(d)
            count += 1
            if count % 100 == 0:
                logging.info("done {}".format(count))

    df = pd.DataFrame(l)
    logging.info(newfile)
    logging.info(df.describe())
    df.to_csv(newfile)
    return df



def calculate_stats(user1, user2):
    stats = {}
    stats['hashtags_jac'] = jaccard(user1['hashtags'], user2['hashtags'])
    stats['retweets_jac'] = jaccard(user1['retweets'].keys(), user2['retweets'].keys());
    stats['replies_jac'] = jaccard(user1['replies'].keys(), user2['replies'].keys());
    stats['interactions_jac'] = jaccard(user1['interactions'].keys(), user2['interactions'].keys());
    stats['quotes_jac'] = jaccard(user1['quotes'].keys(), user2['quotes'].keys());
    stats['mentions_jac'] = jaccard(user1['mentions'].keys(), user2['mentions'].keys());
    stats['retweets'] = get_count(user1['retweets'], user1['id'], user2['retweets'], user2['id']);
    stats['interactions'] = get_count(user1['interactions'], user1['id'], user2['interactions'], user2['id']);
    stats['replies'] = get_count(user1['replies'], user1['id'], user2['replies'], user2['id']);
    stats['quotes'] = get_count(user1['quotes'], user1['id'], user2['quotes'], user2['id']);
    stats['mentions'] = get_count(user1['mentions'], user1['id'], user2['mentions'], user2['id']);
    return stats


def get_count(user1, uid1,  user2, uid2):
    cnt1 = 0
    cnt2 = 0
    suid1 = str(uid1)
    suid2 = str(uid2)
    if suid1 in user2:
        cnt1 = user2[suid1]
    if  suid2 in user1:
        cnt2 = user1[suid2]
    return cnt1+cnt2





def jaccard(a,b):
    union = list(set(a+b))
    intersection = list(set(a) - (set(a)-set(b)))
    if len(union) == 0:
        return 0
    jaccard_coeff = float(len(intersection))/len(union)
    return jaccard_coeff

def get_mongo_connection(host="localhost", port=27017, db_name="stream_store"):
    return MongoClient(host=host, port=port)[db_name]

if __name__ == "__main__":
    main()