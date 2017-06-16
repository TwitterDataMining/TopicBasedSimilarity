"""
inserts interactions for a user in the database if not already present.
input :
    unique usernames file,
    Mongodb collection that stores the old tweets of the user
    Mongodb collection to write the interactions
output : inserts interactions (created from old tweets tweets) into interactions collections
"""
from interactions import Interactions
from pymongo import MongoClient
import logging


QUERY = "user_id" # for old db design compatability
LOG_FILE = "interactions.log"


# Input arguments
PROGRAM_DESCRIPTION = " Write interactions of users to database"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('write_collection', type=str, help='collection to write interactions')
parser.add_argument('user_file', type=str, help='file that contains the user ids')
parser.add_argument('read_collections', type=str, help='collections of historic tweets')
args = vars(parser.parse_args())

def main():
    WRITE_COLLECTION = args['write_collection']
    USER_FILE = args['user_file']
    READ_COLLECTION = args['read_collections']


    # get the list of users
    users = get_unique_users_fromfile(USER_FILE)
    logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG, format='%(asctime)s %(message)s')

    # get mongodb collections
    db = get_mongo_connection()
    read_collection = db[READ_COLLECTION]
    write_collection = db[WRITE_COLLECTION]

    # create instance if Interactions (which contains actual processing utility)
    inter = Interactions(read_collection, QUERY)

    # process the users and write interactions to db
    process(inter, users, write_collection)


def process(inter, users, write_collection):
    """
    responsible for counting the interactions from the old tweets of every user
    and inserting those interactions into the write collections

    :param inter: instance of Interactions class
    :param users: list of unique users
    :param write_collection: collection where interactions need to be written
    :return:
    """
    count = 0
    found = 0
    for user in users:
        cur = write_collection.find({"id": user})
        if cur.count() == 0:
            user_obj = inter.get_interactions_for_user(user)
            dict = user_obj.toJson()
            write_collection.insert(dict)
        else:
            found += 1
        if count % 100 == 0:
            logging.info(" done {0} found = {1}".format(count, found))
        count += 1


def get_unique_users_fromfile(filename):
    """
    takes the csv files containing unique users and returns the
    list of user id's as list of int
    :param filename:
    :return: list of user ids
    """
    with open(filename, 'rb') as f:
        users = map(int, f.readlines())
    return users


def get_mongo_connection(host="localhost", port=27017, db_name="stream_store"):
    return MongoClient(host=host, port=port)[db_name]

if __name__ == "__main__":
    main()