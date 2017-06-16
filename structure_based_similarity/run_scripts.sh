#!/usr/bin/env bash
WRITE_COLLECTION="Interactions"
USER_FILE="data/unique_users.csv"
READ_COLLECTION="old_tweets"

DIR="data/pair_files"

cd " path to folder "
python prepare_interactions.py $WRITE_COLLECTION $USER_FILE $READ_COLLECTION
python interactions_stats.py $WRITE_COLLECTION $DIR
