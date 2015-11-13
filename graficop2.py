#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs.

Usage:
  graficop2.py [options]

Options:

  -h --help           Show this screen.
  -u                  Print unics.

"""

import csv, re, pdb, ast, time, os, sys

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates


init = datetime.date(2001, 1, 1)


def allgraph(unic):

    csv.field_size_limit(sys.maxsize)

    alldict = csv.reader(open("alldict.csv", "r"))

    alltemplates = {}

    print("Creating output dictionary...")

    for line in alldict:

        page = line[0]

        pagedict = ast.literal_eval(line[1])

        sort = sorted(pagedict)

        oldcount = {}

        for s in sort:

            new = 0

            for tmp in pagedict[s]:

                if unic:

                    new = 1

                else:

                    d = pagedict[s]

                    new = d[tmp]

                try:

                    old = oldcount[tmp]

                except KeyError:

                    old = 0

                add = new - old

                if (add != 0):

                    try:

                        singletemplate = alltemplates[tmp]

                    except KeyError:

                        singletemplate = {}

                    try:

                        singletemplate[s] = singletemplate[s] + add

                    except KeyError:

                        singletemplate[s] = add

                    alltemplates[tmp] = singletemplate

                oldcount[tmp] = new

            for o in oldcount:

                if o not in pagedict[s] and oldcount[o] != 0:

                    singletemplate = alltemplates[o]

                    try:

                        singletemplate[s] = singletemplate[s] - oldcount[o]

                    except KeyError:

                        singletemplate[s] = - oldcount[o]

                    oldcount[o] = 0

                    alltemplates[o] = singletemplate

    print("Creating .csv files...")

    if not os.path.exists("grafici"):

        os.makedirs("grafici")

    if unic:

        if not os.path.exists("grafici/unic"):

            os.makedirs("grafici/unic")

    else:

        if not os.path.exists("grafici/total"):

            os.makedirs("grafici/total")

    alldict = {}

    for singletemplate in alltemplates:

        name = singletemplate

        if len(name) > 130:

            continue

        singletemplate = alltemplates[singletemplate]

        if unic:

            out = csv.writer(open("grafici/unic/" + name + ".csv", "w"))

        else:

            out = csv.writer(open("grafici/total/" + name + ".csv", "w"))

        sort = sorted(singletemplate)

        value = 0

        x = []

        y = []

        for s in sort:

            value = value + singletemplate[s]

            x.append(s)

            y.append(value)

        l = len(x)

        n = 0

        while n < l:

            out.writerow([x[n], y[n]])

            n = n + 1


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    allgraph(arguments['-u'])