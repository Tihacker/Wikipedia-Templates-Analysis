#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create the .csv file listing all redirects.

Usage:
  redirect.py [options]

Options:
  --download LIST     Download and execute for every dump on the list.
  -f PATH             Manually set the dump's location PATH. [default: dump.bz2]
  -h --help           Show this screen.
  -o OUT              Choose a name for the output. [default: redirect.csv]

"""

from docopt import docopt

from mw.xml_dump import Iterator

import csv, re, pdb, bz2, time, urllib.request, sys, os


def normalize(template):

    if ("template:" in template):

        template = template.rsplit(":")[-1]

    template = template.split("|")[0]

    template = template.replace("\"", "")

    template = template.replace("\n", " ")

    template = template.replace("\t", "")

    template = template.replace("  ", " ")

    template = template.replace("\"", "")

    template = template.replace("_", " ")

    while (template[:1] == " "):

        template = template[1:]

    while (template[-1:] == " "):

        template = template[:-1]

    try:

        template = template[0].upper() + template[1:]

    except IndexError:

        template = template.capitalize()

    return template

if __name__ == "__main__":

    arguments = docopt(__doc__)

