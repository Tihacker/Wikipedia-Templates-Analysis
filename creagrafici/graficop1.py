#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs.

Usage:
  graficop1.py [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output-post.csv]
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates


init = datetime.date(2001, 1, 1)


def allgraph():

    dump = csv.reader(open(arguments['-f'], "r"))
    
    next(dump)

    alldict = csv.writer(open("alldict.csv", "w"))

    pagedict = {}

    oldpage = -1

    print("Creating templates dictionary...")

    for listt in dump:

        if oldpage != listt[1] and oldpage != -1:

            alldict.writerow([oldpage, pagedict])

            pagedict = {}

        anno = listt[3][:4]

        mese = listt[3][4:6]

        giorno = listt[3][6:8]

        data = datetime.date(int(anno), int(mese), int(giorno))

        minus = data - init

        minus = minus.days

        pagedict[minus] = ast.literal_eval(listt[4])

        oldpage = listt[1]

    alldict.writerow([oldpage, pagedict])


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    allgraph()