#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Eliminate every template used only in one page.

Usage:
  post-processing.py [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output-nocomment.csv]
  -h --help           Show this screen.
  -o PATH             Set Output File's name OUT. [default: outputwithredirects.csv]
  -r PATH             Set the redirects .csv file location. [default: redirects.csv]

"""

import csv, re, pdb, ast

from docopt import docopt


if __name__ == "__main__":

    arguments = docopt(__doc__)

    dump = csv.reader(open(arguments['-f'], "r"))

    next(dump)

    redirects = csv.reader(open(arguments['-r'], "r"))

    next(redirects)

    redirectsset = set()

    redirectsdict = {}

    print("Reading redirects...")

    for line in redirects:

        try:

            tmp = redirectsdict[line[0]]

        except KeyError:

            tmp = {}

        if line[3] not in tmp:

            tmp[line[3]] = line[1]

        redirectsdict[line[0]] = tmp

    print("Creating output...")

    out = csv.writer(open(arguments['-o'], "w"))

    firstrow = ["page_id", "page_title", "rev_id", "timestamp", "dictionary"]

    out.writerow(firstrow)

    for listt in dump:

        templates = ast.literal_eval(listt[4])

        newtemplates = templates.copy()

        for template in templates:

            new = template

            if template in redirectsdict:

                redirects = redirectsdict[template]

                sort = sorted(redirects)

                for s in sort:

                    if s < listt[3]:

                        new = redirects[s]

                if (new != template):

                    try:

                        newtemplates[new] = newtemplates[new] + newtemplates.pop(template)

                    except KeyError:

                        newtemplates[new] = newtemplates.pop(template)

        out.writerow([listt[0], listt[1], listt[2], listt[3], newtemplates])