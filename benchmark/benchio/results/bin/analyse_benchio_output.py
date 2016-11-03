#!/usr/bin/env python
#
# Analyse benchio output files
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
    resdir = sys.argv[1]
    usesize = int(sys.argv[2])

    files = get_filelist(resdir, "benchio_")

    # Loop over files getting data
    resframe_proto = []
    for file in files:
       infile = open(file, 'r')
       resdict = {}
       for line in infile:
          if re.search('MPI-IO', line):
             break
          elif re.search('Starting job', line):
             tokens = line.split()
             resdict['JobID'] = tokens[2]
          elif re.search('Running', line):
             tokens = line.split()
             resdict['Writers'] = int(tokens[2])
          elif re.search('Array', line):
             tokens = line.split()
             x = int(tokens[4])
             y = int(tokens[6])
             z = int(tokens[8])
             resdict['LocalSize'] = (x, y, z)
          elif re.search('Global', line):
             tokens = line.split()
             x = int(tokens[4])
             y = int(tokens[6])
             z = int(tokens[8])
             resdict['GlobalSize'] = (x, y, z)
          elif re.search('Total', line):
             tokens = line.split()
             resdict['TotData'] = float(tokens[5])
       infile.close()
       infile = open(file, 'r')
       timedict = resdict.copy()
       for line in infile:
          if re.search('HDF5', line):
             break
          elif re.search('Writing to', line):
             tokens = line.split()
             if re.match('striped', tokens[2]):
                timedict['Striping'] = -1
             elif re.match('defstriped', tokens[2]):
                timedict['Striping'] = 4
          elif re.match(' time', line):
             tokens = line.split()
             timedict['Write'] = float(tokens[6])
             timedict['File'] = os.path.abspath(file)
             timedict['Count'] = 1
             resframe_proto.append(timedict)
             curstriping = timedict['Striping']  
             timedict = resdict.copy()
             timedict['Striping'] = curstriping
             
       infile.close()

    resframe = pd.DataFrame(resframe_proto)
    print 'Number of valid results files read = ', len(resframe.index)

    resframe = resframe[resframe.LocalSize == (usesize, usesize, usesize) ]

    print "Summary of all results found:"
    print resframe
    labels = map(int, resframe['Writers'].unique())
    labels.sort()

    # Get copy of dataframe with only numeric values
    resframe_num = resframe.drop(['File', 'GlobalSize', 'TotData'], 1)

    # What stats are we computing on which columns
    groupf = {'Write':['min','median','max','mean'], 'Count':'sum'}
   
    # Compute the maximum read and write bandwidths from the data
    stats = resframe_num.sort('Writers').groupby(['Writers', 'Striping', 'LocalSize']).agg(groupf)
    print "Useful statistics:"
    print stats
    print stats.to_csv(float_format='%.3f')


    fig, ax = plt.subplots()

    sns.stripplot(x='Writers', y='Write', data=resframe, jitter=True, hue='Striping')

    ax.set_ylim(ymin=0)

    plt.ylabel('Bandwidth / MiB/s')
    plt.xlabel('Writers')
    plt.legend()
    plt.savefig(resdir + '_stats.png')
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
