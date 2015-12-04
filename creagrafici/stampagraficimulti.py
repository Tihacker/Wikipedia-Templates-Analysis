#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampagraficimulti.py [<template>]... [options]

Options:
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile


init = datetime.date(2001, 1, 1)


def creategraphs(inputtemplate):

    fig = plot.figure()

    ax = fig.add_subplot(111)

    years    = mdates.YearLocator()
    months   = mdates.MonthLocator()
    yearsFmt = mdates.DateFormatter('%Y')
    monthsFmt = mdates.DateFormatter('%m')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)
    #ax.xaxis.set_minor_formatter(monthsFmt)

    #second_axes = plot.twinx()
    #second_axes.set_yticks([int(y[-1])])

    ax.grid(which='minor', alpha=0.2)

    ax.grid(which='major', alpha=0.5)

    plot.xlabel('Time')

    plot.ylabel('Template Occurrences')

    if not os.path.exists("png"):

        os.makedirs("png")

    title = input("Inserire il titolo: ")

    for single in inputtemplate:

        coord = csv.reader(open(single, "r"))

        value = 0

        x = []

        y = []

        directory = single.rsplit("/", 1)[0]

        filename = single.split("/")[-1]

        filename = filename.replace(".csv", "")

        for c in coord:

            date = init + datetime.timedelta(days=int(c[0]))

            x.append(date)

            y.append(c[1])

        label = input("Inserire il label per " + single + ": ")

        color = input("Inserire il colore per " + single + ": ")

        plot.plot(x, y, color=color, label=label)

        plot.suptitle(title, fontsize = 20)

    legend = ax.legend(loc='upper center', shadow=True)

    plot.savefig("png/" + filename + ".png")

    plot.close()

if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = []

    graphs = arguments['<template>']

    for g in graphs:

        i.append(g)

    creategraphs(i)