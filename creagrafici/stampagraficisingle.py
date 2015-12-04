#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of single graphs.

Usage:
  stampagraficisingle.py [<template>]... [options]

Options:
  -a DIR              Print the entire DIR directory.
  -h --help           Show this screen.
  -l LIST             Create graphs from a list.
  -r                  Remove old graphs.

"""

import csv, re, pdb, ast, time, os

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile


init = datetime.date(2001, 1, 1)


def singlegraph(inputtemplate):

    coord = csv.reader(open(inputtemplate, "r"))

    directory = inputtemplate.rsplit("/", 1)[0]

    filename = inputtemplate.split("/")[-1]

    filename = filename.replace(".csv", "")

    value = 0

    x = []

    y = []

    for c in coord:

        date = init + datetime.timedelta(days=int(c[0]))

        x.append(date)

        y.append(c[1])

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

    plot.ylabel(filename + " Occurrences")

    plot.plot(x, y)

    if not os.path.exists("png"):

        os.makedirs("png")

    print("Creating " + inputtemplate + ".png...")

    plot.savefig("png/" + filename + ".png")

    plot.close()


def categorygraph(inputtemplate, category):

    coord = csv.reader(open(inputtemplate, "r"))

    directory = inputtemplate.rsplit("/", 1)[0]

    filename = inputtemplate.split("/")[-1]

    filename = filename.replace(".csv", "")

    value = 0

    x = []

    y = []

    for c in coord:

        date = init + datetime.timedelta(days=int(c[0]))

        x.append(date)

        y.append(c[1])

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

    plot.ylabel(filename + " Occurrences")

    plot.plot(x, y)

    if not os.path.exists("png"):

        os.makedirs("png")

    if not os.path.exists("png/" + category):

        os.makedirs("png/" + category)

    print("Creating " + inputtemplate + ".png...")

    plot.savefig("png/" + category + "/" + filename + ".png")

    plot.close()


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = []

    if arguments['-r']:

        print("Removing old .png...")

        if os.path.exists("png"):

            for f in os.listdir("png/"):
                
                if f.endswith(".png"):

                    os.remove("png/" + f)

    if arguments['-l']:

        r = open(arguments['-l'])

        l = r.read().splitlines()

        for line in l:

            i.append(line)

    if arguments['-a']:

        for f in os.listdir(arguments['-a']):
            
            if f.endswith(".csv"):
                
                i.append(f)

    else:

        graphs = arguments['<template>']

        for g in graphs:

            i.append(g)

    for graph in i:

        singlegraph(graph)