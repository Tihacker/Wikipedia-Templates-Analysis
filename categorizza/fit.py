#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampagrafici.py [<template>] [options]

Options:
  -h --help           Show this screen.
  -v                  Verbose.
  --esempio
  --esempio2
  --esempio3

"""

import csv, re, pdb, ast, time, os, math

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile


def do(inputtemplate, verbose):

    #NORMALIZZAZIONE

    if(arguments['--esempio'] or arguments['--esempio2'] or arguments['--esempio3']):

        coord = csv.reader(open("it/graphs/total/Bio.csv", "r"))

    else:

        coord = csv.reader(open(inputtemplate, "r"))

    xdiff = 0

    ymax = 0

    ymin = -1

    x = []

    y = []

    for c in coord:

        date = int(c[0])

        value = int(c[1])

        if xdiff == 0:

            xdiff = date

        if ymin == -1:

            ymin = value

        if value > ymax:

            ymax = value

        if value < ymin:

            ymin = value

        x.append(date - xdiff)

        y.append(value)

    xdiff = date - xdiff

    ydiff = ymax - ymin

    normx = []

    normy = []

    n = 0

    if xdiff != 0 and ydiff != 0:

        while (n < len(x)):

            partial = 0

            percent = x[n] / xdiff

            normx.append(percent)

            partial = y[n] - ymin

            normy.append(partial / ydiff)

            n = n + 1

    else:

        return 1

    #ESEMPIO2

    number = 0

    halfnormx = []

    limit = 0

    while number < len(normx)/4:

        halfnormx.append(normx[number])

        limit = normx[number]

        number = number + 1

    number = 0

    halfnormy = []

    while number < len(normx)/4:

        halfnormy.append(normy[number])

        number = number + 1

    if(arguments['--esempio3']):

        normx = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

        normy = [0.5, 0.6, 0.5, 0.6, 0.5, 0.6, 0.5, 0.6, 0.5, 0.6, 0.5]

    #PRE

    np.seterr(all="warn")

    l = np.linspace(0, 1, len(normx))

    r2 = {}

    #PIATTA

    z = np.polyfit(normx, normy, 0)

    piatta = np.poly1d(z)

    i = 0

    media = np.sum(normy)/len(normy)

    ssreg = np.sum((piatta(normx)-media)**2)

    sstot = np.sum((normy - media)**2)

    print(sstot)

    r2["piatta"] = ssreg / sstot

    #LINEARE

    if(arguments['--esempio']):

        z = np.polyfit(halfnormx, halfnormy, 1)

    else:

        z = np.polyfit(normx, normy, 1)

    lineare = np.poly1d(z)

    i = 0

    media = np.sum(normy)/len(normy)

    ssreg = np.sum((lineare(normx)-media)**2)

    sstot = np.sum((normy - media)**2)

    r2["lineare"] = ssreg / sstot

    #POLINOMIALE

    if(arguments['--esempio']):

        z = np.polyfit(halfnormx, halfnormy, 2)

    else:

        z = np.polyfit(normx, normy, 2)

    polinomiale = np.poly1d(z)

    i = 0

    media = np.sum(normy)/len(normy)

    ssreg = np.sum((polinomiale(normx)-media)**2)

    sstot = np.sum((normy - media)**2)

    r2["polinomiale"] = ssreg / sstot

    #ESPONENZIALE

    normyexp = []

    for n in normy:

        if n == 0:

            normyexp.append(0)

        else:

            normyexp.append(np.log(n))

    z = np.polyfit(normx, normyexp, 1)

    esponenziale = np.poly1d(z)

    i = 0

    media = np.sum(normyexp)/len(normyexp)

    ssreg = np.sum((esponenziale(normx)-media)**2)

    sstot = np.sum((normyexp - media)**2)

    if (sstot != 0):

        r2["esponenziale"] = ssreg / sstot

    else:

        r2["esponenziale"] = 0

    #SQUARE

    normysquare = []

    for n in normy:

        normysquare.append(n**2)

    z = np.polyfit(normx, normysquare, 1)

    radice = np.poly1d(z)

    i = 0

    media = np.sum(normysquare)/len(normysquare)

    ssreg = np.sum((radice(normx)-media)**2)

    sstot = np.sum((normysquare - media)**2)

    r2["radice"] = ssreg / sstot

    #LOG

    normylog = []

    for n in normy:

        normylog.append(np.exp(n))

    z = np.polyfit(normx, normylog, 1)

    log = np.poly1d(z)

    i = 0

    media = np.sum(normylog)/len(normylog)

    ssreg = np.sum((log(normx)-media)**2)

    sstot = np.sum((normylog - media)**2)

    r2["log"] = ssreg / sstot

    #CALCOLOMIGLIORE

    best = max(r2, key=r2.get)

    if r2[best] == r2["polinomiale"]:

        if ((r2["polinomiale"] - r2["lineare"])/r2["lineare"] < 0.1):

            best = "lineare"

    if r2[best] == r2["lineare"]:

        if ((r2["lineare"] - r2["piatta"])/r2["piatta"] < 0.1):

            best = "piatta"

    if r2[best] <= 0.5:

        best = "none"

    if (verbose):

        #STAMPAGRAFICI
        
        fig = plot.figure()

        ax = fig.add_subplot(111)

        ax.grid(which='major', alpha=0.5)

        plot.xlabel('X')

        plot.ylabel("Y")

        if (arguments['--esempio']):

            l = np.linspace(-1, 2, len(normx))

            ax.set_xlim([0,1])
    
            ax.set_ylim([0,1.5])

            ax.axvline(limit, linestyle='--', label = "Limite fit")

            plot.plot(normx, normy, 'ro', label = "Punti")

            plot.plot(l, lineare(l), linewidth=2, label="Lineare")

            plot.plot(l, polinomiale(l), linewidth=2, label="Polinomiale")

        if (arguments['--esempio2']):

            plot.xlabel('X')

            plot.ylabel("Y")

            plot.plot(l, normy)

            plot.plot(l, normylog, linewidth=1, label="Log")

        else:

            ax.set_xlim([0,1])
    
            ax.set_ylim([0,1])

            plot.plot(normx, normy, linewidth=2, label="Curva")

            plot.plot(l, piatta(l), linewidth=1, label="Piatta")

            plot.plot(l, lineare(l), linewidth=1, label="Lineare")
            
            plot.plot(l, polinomiale(l), linewidth=1, label="Polinomiale")

            plot.plot(l, np.exp(esponenziale(l)), linewidth=1, label="Esponenziale")

            plot.plot(l, np.sqrt(radice(l)), linewidth=1, label="Radice")

            plot.plot(l, np.log(log(l)), linewidth=1, label="Log")

        plot.legend(bbox_to_anchor=(0.35, 1))

        print("PIATTA: " + str(r2["piatta"]))

        print("LINEARE: " + str(r2["lineare"]))

        print("POLI: " + str(r2["polinomiale"]))

        print("ESPONENZIALE: " + str(r2["esponenziale"]))

        print("SQUARE: " + str(r2["radice"]))

        print("LOG: " + str(r2["log"]))

        print("Migliore: " + best)

        plot.show()

    return best


if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = arguments['<template>']

    result = do(i, arguments['-v'])

    print(result)