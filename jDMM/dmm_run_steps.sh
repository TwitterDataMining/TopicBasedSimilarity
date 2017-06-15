#!/usr/bin/env bash

# following input are needed by user_topic_lis.py and make_topic_vector.py

# File contains username, preprocesssed tweets
USERNAME_FILE="data/24Legacy1000_s_username.csv"

# This is result of topic modelling from jLDADMM xxx.topicAssignments
TOPIC_ASSIGNMENT="data/model.topicAssignments"

# Name of the output file for user topic
USER_TOPIC_DICT="data/24Legacy1000_user_topic.p"

# Name of the output file for  topic vector
TOPIC_VECTOR="data/24Legacy1000_topic_vector.p"

# Name of the log file
LOG_FILE="data/logfile.log"



python user_topic_list.py $TOPIC_ASSIGNMENT $USERNAME_FILE $USER_TOPIC_DICT $LOG_FILE
python make_topic_vector.py $USER_TOPIC_DICT $TOPIC_VECTOR $LOG_FILE


