#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create template graphs png of multiple graphs.

Usage:
  stampagrafici.py [<tipologia>]... [options]

Options:
  -h --help           Show this screen.

"""

import csv, re, pdb, ast, time, os, math

from docopt import docopt

import datetime

import matplotlib.pyplot as plot

import numpy as np

import matplotlib.dates as mdates

import tarfile


def creategraphs(tipologia):

    fig = plot.figure()

    ax = fig.add_subplot(111)

    ax.grid(which='minor', alpha=0.2)

    ax.grid(which='major', alpha=0.5)

    ax.set_xlim([0,1])
    
    ax.set_ylim([0,1])

    points = np.linspace(0, 1, 100)

    if tipologia == "logaritmica" or tipologia == "polinomiale" or  tipologia == "esponenziale":

        ax.set_xlim([0,10])
    
        ax.set_ylim([0,10])

        points = np.linspace(0, 10, 100)

    x = []

    y1 = []

    y2 = []

    for p in points:

        if tipologia == "piatta":

            x.append(p)

            y1.append(0.2)

            label1 = "a = 0.2"

            y2.append(0.8)

            label2 = "a = 0.8"

            title = "Y = a"

        if tipologia == "lineare":

            x.append(p)

            y1.append((0.5*p) + 0.2)

            label1 = "a = 0.5, b = 0.2"

            y2.append((-0.8*p) + 0.6)

            label2 = "a = -0.8, b = 0.6"

            title = "Y = aX + b"

        if tipologia == "polinomiale":

            x.append(p)

            y1.append(1 * (p**2) + 0*p + 0)

            label1 = "a = 1, b = 0, c = 0"

            y2.append(0.5 * (p**2) + 0.5*p + 0)

            label2 = "a = 0.5, b = 0.5, c = 0"

            title = "Y = aX^2 + bX + c"

        if tipologia == "esponenziale":

            x.append(p)

            y1.append(math.exp(1 * p) - 1)

            label1 = "a = 1, b = -1"

            y2.append(math.exp(0.5 * p) - 1)

            label2 = "a = 0.5, b = -1"

            title = "Y = e^aX + b"

        if tipologia == "radicale":

            x.append(p)

            y1.append(math.sqrt(1 * p) + 0)

            label1 = "a = 1, b = 0"

            y2.append(math.sqrt(0.5 * p) + 0)

            label2 = "a = 0.5, b = 0"

            title = "Y = sqrt(aX) + b"

        if tipologia == "logaritmica":

            if p == 0:

                continue

            x.append(p)

            y1.append(math.log(1 * p) + 0)

            label1 = "a = 1, b = 0"

            y2.append(math.log(5 * p) + 0)

            label2 = "a = 5, b = 0"

            title = "Y = log(aX) + b"

    plot.plot(x, y1, label = label1)

    plot.plot(x, y2, label = label2)

    plot.legend()

    plot.suptitle(title, fontsize = 20)

    plot.savefig(tipologia + ".png",bbox_inches='tight')

    plot.close()

if __name__ == "__main__":
            
    arguments = docopt(__doc__)

    i = []

    tipologia = arguments['<tipologia>']

    for t in tipologia:

        creategraphs(t)