#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Eliminate every template used only in one page.

Usage:
  post-processing.py [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output.csv]
  -h --help           Show this screen.
  -o OUT              Set Output File's name OUT. [default: output-post.csv]
  -p                  Create the list of templates used only in one page.
  -r                  Create the list of templates used only in one revision.
  --redirect RED      Create also the output considering redirects. Specify .csv file's location.

"""

import csv, re, pdb, ast

from docopt import docopt


if __name__ == "__main__":

    arguments = docopt(__doc__)

    dump = csv.reader(open(arguments['-f'], "r"))
    
    next(dump)

    if (arguments['-p']):

        elimp = open("eliminated-page.txt", "w")

    if (arguments['-r']):

        elimr = open("eliminated-revision.txt", "w")

    eliminati = set()

    count = {}

    countpage = {}

    templatespage = set()

    old = -1

    print("Counting templates...")

    for listt in dump:

        if old != listt[1]:

            for temp in templatespage:

                try:

                    countpage[temp] = countpage[temp] + 1

                except KeyError:

                    countpage[temp] = 1

            templatespage = set()

        templates = ast.literal_eval(listt[4])

        for template in templates:

            if template not in templatespage:

                templatespage.add(template)

            try:

                count[template] = count[template] + 1

            except KeyError:

                count[template] = 1

        old = listt[1]

    for tmp in count:

        if(count[tmp]==1):

            if tmp not in eliminati:

                eliminati.add(tmp)

                if (arguments['-r']):

                    elimr.write(str(tmp) + "\n")

    for tmp in countpage:

        if(countpage[tmp]==1):

            if tmp not in eliminati:

                eliminati.add(tmp)

                if (arguments['-p']):

                    elimp.write(str(tmp) + "\n")

    dump = csv.reader(open(arguments['-f'], "r"))

    next(dump)

    print("Creating .csv files...")

    out = csv.writer(open(arguments['-o'], "w"))

    firstrow = ["page_id", "page_title", "rev_id", "timestamp", "dictionary"]

    out.writerow(firstrow)

    if (arguments['--redirect']):

        out2 = csv.writer(open(arguments['-o'][:-4] + "-redirect.csv", "w"))

        out2.writerow(firstrow)

        redirects = csv.reader(open(arguments['--redirect'], "r"))

        next(redirects)

        dictred = {}

        for t in redirects:

                    i = 0

                    subsubdict = {}

                    try:

                        subdict = dictred[t[0]]

                    except KeyError:

                        subdict = {}

                    subsubdict['red'] = t[1]

                    subsubdict['revid'] = t[2]

                    subdict[t[3]] = subsubdict

                    dictred[t[0]] = subdict

    for listt in dump:

        templates = ast.literal_eval(listt[4])

        newtemplates = templates.copy()

        newtemplates2 = templates.copy()

        for template in templates:

            if template in eliminati:

                del newtemplates[template]

                del newtemplates2[template]

                continue

            if (arguments['--redirect']):

                new = ""

                if template in dictred:

                    subdict = dictred[template]

                    for d in sorted(subdict.keys()):

                        if listt[3] > d:

                            d = subdict[d]

                            new = d['red']

                if (new != ""):

                    try:

                        newtemplates2[new] = newtemplates2[new] + newtemplates2.pop(template)

                    except KeyError:

                        newtemplates2[new] = newtemplates2.pop(template)

        out.writerow([listt[0], listt[1], listt[2], listt[3], newtemplates])

        if (arguments['--redirect']):

            out2.writerow([listt[0], listt[1], listt[2], listt[3], newtemplates2])