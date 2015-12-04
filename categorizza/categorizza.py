#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampagrafici.py [options]

Options:
  -d DIR              Directory to categorize.
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os, math

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile

import fit


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = []

    if arguments['-d']:

        for f in os.listdir(arguments['-d']):
            
            if f.endswith(".csv"):
                
                i.append(f)

    out = csv.writer(open("categorie.csv", "w"))

    for name in i:

        inputfile = open(arguments['-d'] + name, "r")

        rows = sum(1 for row in inputfile)

        result = fit.do(arguments['-d'] + name, False)

        if result != 1:

            out.writerow([name, result, rows])