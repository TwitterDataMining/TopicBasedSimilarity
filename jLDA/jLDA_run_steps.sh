#!/usr/bin/env bash

USERNAME_FILE="/data/24Legacy1000_username.csv"
THETA_FILE="data/model.theta"
TOPIC_VECTOR="data/24Legacy1000_topic_vectors.p"

cd "path to the script file"
python create_topic_vectors_jLDA.py $THETA_FILE $USERNAME_FILE $TOPIC_VECTOR



