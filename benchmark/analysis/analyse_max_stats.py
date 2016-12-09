#!/usr/bin/env python
#
# Read a max IO data CSV file and produce a plot
#

# System modules for grabbing data
import sys
import os.path
import re
from glob import glob
import seaborn as sns

# Modules for analysing and visualising data
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
matplotlib.rcParams.update({'font.size': 9})
matplotlib.rcParams.update({'figure.autolayout': True})

def main(argv):
    infile = sys.argv[1]

    resframe = pd.read_csv(infile)

    print "Summary of all results found:"
    print resframe
    labels = map(int, resframe['Writers'].unique())
    labels.sort()

    fig, ax = plt.subplots()

    sns.pointplot(x='Writers', y='Max. Write Bandwidth (MiB/s)', data=resframe, hue='Scheme', scale=0.5)
    # sns.stripplot(x='Writers', y='Write', data=resframe, hue='Striping', jitter=True)
    ax.set_ylim(ymin=0)

    plt.ylabel('Bandwidth / MiB/s')
    plt.xlabel('Writers')
    plt.legend()
    plt.savefig('max_bandwidth_stats.png')
    plt.clf()

    sys.exit(0)

def get_filelist(dir, stem):
    """
    Get list of date files in the specified directory
    """

    files = []
    if os.path.exists(dir):
        files = glob(os.path.join(dir, stem + '*' ))
        files.sort()
    else:
        sys.stderr.write("Directory does not exist: {1}".format(dir))
        sys.exit(1)

    return files

if __name__ == "__main__":
    main(sys.argv[1:])
