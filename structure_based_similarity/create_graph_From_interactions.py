"""
utility script to create histograms
Takes the interactions stats and creates the frequency graphs for visualization.
"""
import pandas as pd
import glob
import matplotlib.pyplot as plt
import os

# log file
LOG_FILE = "interaction_stats.log"

# path to folder that containes interaction statistics as csv : output of "interactions_stats.py"
DEST_DIR="data/24Legacy/2000Social"

def main():
    # get data file names
    files = glob.glob(DEST_DIR + "/*.csv")
    for each_file in files:
        df = pd.read_csv(open(each_file, 'r'))
        plot_histogram(df, each_file)


def plot_histogram(df, each_file):
    direc = each_file.rpartition("/")[0]
    folder = each_file.rpartition("/")[2].rpartition('.')[0]
    dest = direc + '/' + folder
    try:
        os.stat(dest)
    except:
        os.mkdir(dest)

    for column in df:
        filename = dest + '/' + column + ".png"
        S =  df[column]

        S[~((S - S.mean()).abs() > 1 * S.std())]
        histogram = S.hist(bins=50)
        histogram.set_xlabel(column)
        histogram.set_ylabel("frequency")
        histogram.set_title(folder)
        fig = histogram.get_figure()
        fig.savefig(filename)
        fig.clf()


if __name__ == "__main__":
    main()