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

    # Lists of marker styles and line styles
    markers = 10 * ['o','^','x']
    lines = 10 * ['-','--','-.']

    infile = sys.argv[1]

    resframe = pd.read_csv(infile)

    print "Summary of all results found:"
    print resframe
    labels = map(int, resframe['Writers'].unique())
    labels.sort()

    fig, ax = plt.subplots()

    sns.pointplot(x='Writers', y='Write Bandwidth (MiB/s)',
      data=resframe, hue='Scheme', scale=0.75, markers=markers,
      linestyles=lines)
    ax.set_ylim(ymin=0)

    plt.ylabel('Max. Write Bandwidth / MiB/s')
    plt.xlabel('Writers')
    plt.legend()
    plt.savefig('max_bandwidth_stats.png')
    plt.clf()

    sys.exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])
