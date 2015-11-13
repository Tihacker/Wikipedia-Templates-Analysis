#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampacategorie.py [options]

Options:
  -f FILE             Set the input. [default: categorie.csv]
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os, math

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = csv.reader(open(arguments['-f'], "r"))

    count = {}

    for line in i:

        try:

            count[line[1]] = count[line[1]] + 1

        except KeyError:

            count[line[1]] = 1

    val = []

    keys = []

    for k in sorted(count.items()):

        if k[0] != "non classificabile":

            keys.append(k[0])

            val.append(k[1])

    X = np.arange(len(keys))

    plot.bar(X, val, color = [ "red", "blue", "yellow", "green", "purple", "cyan"],  align = "center", width = 0.5)

    plot.xticks(X, keys)

    ax = plot.subplot(111)

    plot.ylabel('Number of templates')

    ax.grid(which='major', alpha=0.5)

    plot.savefig("categorie.png",bbox_inches='tight')