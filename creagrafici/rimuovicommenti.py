#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Usage:
  rimuovicommenti.py [options]

Options:
  -f PATH             Manually set the .csv file location. [default: output.csv]
  -h --help           Show this screen.
  -o OUT              Set Output File's name OUT. [default: output-nocomment.csv]

"""

import csv, re, pdb, ast

from docopt import docopt


if __name__ == "__main__":

    arguments = docopt(__doc__)

    dump = csv.reader(open(arguments['-f'], "r"))

    next(dump)

    out = csv.writer(open(arguments['-o'], "w"))

    firstrow = ["page_id", "page_title", "rev_id", "timestamp", "dictionary"]

    out.writerow(firstrow)

    for listt in dump:

        templates = ast.literal_eval(listt[4])

        newtemplates = templates.copy()

        for template in templates:

            new = template.split("<!", 1)[0]

            while (new[-1:] == " "):

                        new = new[:-1]

            new = new.replace("<includeonly>", "")

            if (new != template):

                try:

                    newtemplates[new] = newtemplates[new] + newtemplates.pop(template)

                except KeyError:

                    newtemplates[new] = newtemplates.pop(template)

        out.writerow([listt[0], listt[1], listt[2], listt[3], newtemplates])