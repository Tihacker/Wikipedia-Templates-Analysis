#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create the lists of template's counts by usage.

Usage:
  statistiche.py [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output-post.csv]
  -h --help           Show this screen.
  -t                  Create the total usages list.
  -u                  Create the unic usages list.

"""

import csv, pdb, ast

from docopt import docopt

from collections import Counter


if __name__ == "__main__":

    arguments = docopt(__doc__)

    dump = csv.reader(open(arguments['-f'], "r"))
    
    next(dump)

    count = {}

    countunic = {}

    old = 0

    oldpage = -1

    numeropagine = 0

    for listt in dump:

        if (oldpage == -1):

            oldpage = listt[0]

        if (oldpage != listt[0]):

            templates = ast.literal_eval(oldlist)

            for template in templates:

                try:

                    countunic[template] = countunic[template] + 1

                except KeyError:

                    countunic[template] = 1

                try:

                    count[template] = count[template] + templates[template]

                except KeyError:

                    count[template] = templates[template]

            numeropagine = numeropagine + 1

            oldpage = listt[0]

        oldlist = listt[4]

    templates = ast.literal_eval(oldlist)

    for template in templates:

        try:

            countunic[template] = countunic[template] + 1

        except KeyError:

            countunic[template] = 1

        try:

            count[template] = count[template] + templates[template]

        except KeyError:

            count[template] = templates[template]
            
    numeropagine = numeropagine + 1

    if (arguments['-u']):

        top = csv.writer(open("topunic.csv", "w"))

        c = Counter(countunic)

        for template, value in c.most_common():

            top.writerow([str(template), str(value)])

    if (arguments['-t']):

        top = csv.writer(open("toptotal.csv", "w"))

        c = Counter(count)

        for template, value in c.most_common():

            top.writerow([str(template), str(value)])

    print("Numero pagine: " + str(numeropagine))