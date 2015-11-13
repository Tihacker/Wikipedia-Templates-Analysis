#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampacategorie.py [options]

Options:
  -d DIR              Set the input graphs csv directory.
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

import stampagraficisingle


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = csv.reader(open(arguments['-f'], "r"))

    count = {}

    for line in i:

        if int(line[2]) > 100:

            stampagraficisingle.categorygraph(arguments['-d'] + line[0], line[1])