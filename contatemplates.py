#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create the .csv file listing all redirects.

Usage:
  redirect.py [options]

Options:
  --download LIST     Download and execute for every dump on the list.
  -f PATH             Manually set the dump's location PATH. [default: dump.bz2]
  -h --help           Show this screen.
  -o OUT              Choose a name for the output. [default: numbertemplate.csv]

"""

from docopt import docopt

from mw.xml_dump import Iterator

import csv, re, pdb, bz2, time, urllib.request, sys, os


def do(dump, name):

    out = csv.writer(open(name, "w"))

    firstrow = ["template", "timestamp"]

    out.writerow(firstrow)

    for page in dump:

        if page.namespace == 10:

            page_title = page.title

            page_title = page_title.split(':', 1)[-1]

            #ELIMINO (?)

            if ":" in page_title:

                continue

            #ELIMINO SOTTOTEMPLATE

            if "/" in page_title:

                continue

            #ELIMINO SOFTREDIRECT

            if page_title == "Softredirect":

                continue

            for revision in page:

                timestamp = revision.timestamp

                out.writerow([page_title, timestamp])

                break


def dlProgress(count, blockSize, totalSize):

      percent = int(count*blockSize*100/totalSize)

      sys.stdout.write("\r%d%%" % percent)

      sys.stdout.flush()


if __name__ == "__main__":

    arguments = docopt(__doc__)

    template_dict = {}

    if (arguments['--download']):

        l = open(arguments['--download']).read().splitlines()

        for line in l:

            n = 0

            x = True

            while (x):

                name = "tmpdump" + str(n) + ".bz2"

                if (os.path.isfile(name)):

                    n = n + 1

                else:

                    x = False

            print("Downloading " + line + "...")
            
            urllib.request.urlretrieve(line, name, reporthook=dlProgress)

            print("\nAnalizing " + line + "...")

            dump = Iterator.from_file(bz2.open(name, "r"))

            do(dump, line.split("/")[-1] + ".csv")

            os.remove(name)

    else:

        dump = Iterator.from_file(bz2.open(arguments["-f"], "r"))

        do(dump, arguments['-o'])