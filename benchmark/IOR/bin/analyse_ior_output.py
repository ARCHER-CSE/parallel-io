#!/usr/bin/env python
#
# Analyse IOR output files
#

# System modules for grabbing data
import sys
import os.path
import re
from glob import glob

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
    files = get_filelist(resdir, "ior_res")

    # Loop over files getting data
    resframe_proto = []
    for file in files:
       infile = open(file, 'r')
       resdict = {}
       for line in infile:
          if re.match('Summary of', line):
             break
          elif re.search('JobID', line):
             tokens = line.split()
             resdict['JobID'] = tokens[2]
          elif re.search('Striping', line):
             tokens = line.split()
             resdict['Striping'] = int(tokens[2])
          elif re.search('xfersize', line):
             tokens = line.split()
             xfer = int(tokens[2])
             resdict['Xfer'] = xfer
          elif re.search('blocksize', line):
             tokens = line.split()
             block = int(tokens[2])
             resdict['Block'] = block
          elif re.search('clients', line):
             tokens = line.split()
             clients = int(tokens[2])
             resdict['Clients'] = clients
          elif re.search('api', line):
             tokens = line.split()
             api = tokens[2].strip()
             resdict['API'] = api
          elif re.search('Began', line):
             tokens = line.split(':', 1)
             date = tokens[1].strip()
             resdict['Date'] = date
          elif re.match('write', line):
             tokens = line.split()
             writebw = float(tokens[1])
             resdict['Write'] = writebw
          elif re.match('read', line):
             tokens = line.split()
             readbw = float(tokens[1])
             resdict['Read'] = readbw
       infile.close()
       # Save this set of values to the array of dicts (if non-empty)
       if resdict:
          resdict['File'] = os.path.abspath(file)
          resdict['Count'] = 1
          resframe_proto.append(resdict)

    resframe = pd.DataFrame(resframe_proto)
    print 'Number of valid results files read = ', len(resframe.index)

    print "Summary of all results found:"
    print resframe

    # Get copy of dataframe with only numeric values
    resframe_num = resframe.drop(['File','Date','API', 'JobID'], 1)

    # What stats are we computing on which columns
    groupf = {'Write':['min','max'], 'Read':['min','max'], 'Count':'sum'}
   
    # Compute the maximum read and write bandwidths from the data
    stats = resframe_num.groupby(['Clients', 'Block', 'Xfer', 'Striping']).agg(groupf)
    print "Useful statistics:"
    print stats

    # stats.to_csv(resdir + '_stats.csv', quotechar='"')

    # fig, ax = plt.subplots()
    # stats.plot()
    # plt.savefig(resdir + '_stats.png')
    # plt.clf()

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
