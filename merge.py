#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Merge .csv files.

Usage:
  merge.py [<file>...] [options]

Options:
  -d DIR              Merge every .csv file in a directory.
  -h --help           Show this screen.
  -l LIST             Merge by a .txt list.
  -o OUT              Choose a name for the output. [default: merged-output.csv]

"""

import csv, pdb, ast, os

from docopt import docopt


if __name__ == "__main__":

    arguments = docopt(__doc__)

    out = csv.writer(open(arguments['-o'],"w"))

    firstrow = ["page_id", "page_title", "rev_id", "timestamp", "dictionary"]

    out.writerow(firstrow)

    try:

        if arguments['-d']:

            i = os.listdir(arguments['-d'])

            d = arguments['-d']

        if arguments['-l']:

            i = [line.strip() for line in open(arguments['-l'], 'r')]

            d = ""

        else:

            i = arguments['<file>']

            d = ""

        for file in i:

            if (d + file == arguments['-o']):

                continue

            if file.endswith(".csv"):

                print("Merging: " + file + "...")

                f = csv.reader(open(d + file))

                next(f)
                
                for line in f:
                
                    out.writerow(line)

    except Exception as e:

        print("Error: " + str(e))