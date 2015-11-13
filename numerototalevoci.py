#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs.

Usage:
  grafico.py [<template>]... [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output-post.csv]
  -r PATH             Specify redirects file location. [default: redirects.csv]
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates


init = datetime.date(2001, 1, 1)


def graph():

    dump = csv.reader(open(arguments['-f'], "r"))
    
    next(dump)

    redirects = csv.reader(open(arguments['-r'], "r"))
    
    next(redirects)

    dates = {}

    oldpage = -1

    for listt in dump:

        if oldpage != listt[0] or oldpage == -1:

            anno = listt[3][:4]

            mese = listt[3][4:6]

            giorno = listt[3][6:8]

            data = datetime.date(int(anno), int(mese), int(giorno))

            minus = data - init

            minus = minus.days

            dates[minus] = 1

        oldpage = listt[0]

    deleted = set()

    for listt in redirects:

        print(listt[0])

        if (listt[0] not in deleted):

            anno = listt[3][:4]

            mese = listt[3][4:6]

            giorno = listt[3][6:8]

            data = datetime.date(int(anno), int(mese), int(giorno))

            minus = data - init

            minus = minus.days

            deleted.add(listt[0])

            dates[minus] = -1

        else:

            if (listt[0] == listt[1]):

                anno = listt[3][:4]

                mese = listt[3][4:6]

                giorno = listt[3][6:8]

                data = datetime.date(int(anno), int(mese), int(giorno))

                minus = data - init

                minus = minus.days

                deleted.remove(listt[0])

                dates[minus] = 1

    value = 0

    out = csv.writer(open("allpagesgraph.csv", "w"))

    x = []

    y = []

    old = -1

    for date in sorted(dates):

        value = value + dates[date]

        if old != date:

            out.writerow([date, value])

        old = date


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    graph()