#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Analize every template.

Usage:
  distribuzioni.py [options]

Options:
  -i                  Create the creation date histogram.
  -d DIR              Manually set the directory to analize. [default: ./]
  -h --help           Show this screen.
  -l                  Create the lastvalue histogram.
  -m                  Create the maxvalue histogram.

"""

import csv, pdb, ast, os, math, datetime

from docopt import docopt

import matplotlib.pyplot as plot

import matplotlib.dates as mdates

import numpy as np

init = datetime.date(2001, 1, 1)

def add_month(sourcedate):

    month = sourcedate.month + 1

    year = sourcedate.year

    day = sourcedate.day

    if month == 13:

        year = year + 1

        month = 1

    return datetime.date(year,month,day)


if __name__ == "__main__":

    arguments = docopt(__doc__)    

    maxvalue = []

    initvalue = []

    lastvalue = []

    for f in os.listdir(arguments['-d']):
        
        if f.endswith(".csv"):

            dump = csv.reader(open(arguments['-d'] + f, "r"))

            name = f.replace(".csv", "")

            first = True

            maxv = 0

            for c in dump:

                date = int(c[0])

                value = int(c[1])

                if first:

                    date = init + datetime.timedelta(days=int(c[0]))

                    initvalue.append(date)

                    first = False

                if value > maxv:

                    maxv = value

            maxvalue.append(maxv)

            lastvalue.append(value)

    limit = datetime.date(2001, 1, 1)

    dates = {}

    if (arguments['-i']):

        while limit <= datetime.date.today():

            month = len([x for x in initvalue if x<=limit])

            initvalue = [x for x in initvalue if not x<=limit]

            if month > 0:

                dates[limit] = month

            limit = add_month(limit)

        x = []

        y = []

        for d in sorted(dates):

            x.append(d)

            y.append(dates[d])

        ax = plot.subplot(111)

        years    = mdates.YearLocator()
        months   = mdates.MonthLocator()

        yearsFmt = mdates.DateFormatter('%Y')
        monthsFmt = mdates.DateFormatter('%m')

        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(months)

        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plot.xlabel('Time')
        plot.ylabel('Number of templates created')
        
        ax.bar(x, y, width=2)
        
        ax.xaxis_date()

        plot.savefig("initvalue.png",bbox_inches='tight')

        plot.clf()

    if (arguments['-m']):

        ax = plot.subplot(111)

        ax.grid(which='major', alpha=0.5)

        ax.set_xscale('log')

        plot.xlabel('Max Value')

        plot.ylabel('Number of templates')

        limit = math.ceil(np.log10(max(maxvalue)))

        plot.hist(maxvalue, log = True, bins=np.logspace(0.0, limit, 20))

        plot.savefig("maxvalue.png",bbox_inches='tight')

        plot.clf()

    if (arguments['-l']):

        ax = plot.subplot(111)

        ax.grid(which='major', alpha=0.5)

        ax.set_xscale('log')

        plot.xlabel('Last value')

        plot.ylabel('Number of templates')

        limit = math.ceil(np.log10(max(lastvalue)))

        plot.hist(lastvalue, log = True, bins=np.logspace(0.0, limit, 20))

        plot.savefig("lastvalue.png",bbox_inches='tight')

    plot.close()