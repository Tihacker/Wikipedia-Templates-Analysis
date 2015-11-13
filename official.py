#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Create the .csv file counting every template usage for revision.

Usage:
  official.py [options]

Options:
  -f PATH             Manually set the dump's location. [default: dump.bz2]
  -h --help           Show this screen.
  -i                  Initiate Template Table.
  -l LANG             Set wikipedia language (it, en, es...). [default: en]
  --list LIST         Execute every dump on the list, instead of a single dump. Give a .txt file as input.
  -o OUT              Set Output File's name (if not specified uses the dump's name). Doesn't work for lists.
  -v                  Show percent of the process (may take a while to initiate).

"""

from docopt import docopt

from mw.api import Session

from mw.xml_dump import Iterator

import csv, re, pdb, bz2


def executeoutput(inputbz2, output):

    dump = Iterator.from_file(bz2.open(inputbz2, "r"))

    out = csv.writer(open(output, "w"))

    firstrow = ["page_id", "page_title", "rev_id", "timestamp", "dictionary"]

    out.writerow(firstrow)

    t = 0

    reg = re.compile("(?={{(.*?)(?:\||{{|}}))", re.DOTALL)

    for page in dump:

        if page.namespace == 0:

            if arguments["-v"] == True:

                t += 1

                print(str.format("\r[{0:.2f}%]", t*100/pages_number), end="", flush=True)

            page_id = page.id

            page_title = page.title

            for revision in page:

                rev_id = revision.id

                timestamp = revision.timestamp

                wikitext = revision.text

                output_dict = {}
                
                templates = reg.findall(wikitext)

                for template in templates:

                    template = template.replace("\n", " ")

                    template = template.replace("\t", "")

                    template = template.replace("  ", " ")

                    template = template.replace("\"", "")

                    template = template.replace("_", " ")

                    if (template[:len(template_namespace)].lower() == template_namespace.lower()) or (template[:9].lower() == "template:"):

                        template = template.rsplit(":")[-1]

                    while (template[:1] == " "):

                        template = template[1:]

                    while (template[-1:] == " "):

                        template = template[:-1]

                    if template[:1] == "#":

                        continue

                    if template[:1] == "{":

                        continue

                    #ELIMINO PARSER FUNCTIONS

                    if ":" in template:

                        continue

                    #ELIMINO SOTTO-TEMPLATE

                    if "/" in template:

                        continue

                    #ELIMINO MAGIC WORDS

                    if template in wordlist:

                        continue

                    try:

                        template = template[0].upper() + template[1:]

                    except IndexError:

                        template = template.capitalize()

                    try:

                        output_dict[template] = output_dict[template] + 1

                    except KeyError:

                        output_dict[template] = 1

                out.writerow([page_id, page_title, rev_id, timestamp, output_dict])

    out.close()

    print("\r" + output + " DONE.\n")



if __name__ == "__main__":

    arguments = docopt(__doc__)

    print("Wikipedia language set: " + arguments["-l"])

    template_dict = {}

    print("Finding local namespace...", end=" ", flush=True)
        
    session = Session("https://" + arguments["-l"] + ".wikipedia.org/w/api.php", user_agent='Default')

    #CERCO IL NOME LOCALE DEL NAMESPACE TEMPLATE

    namespaces = session.site_info.query(properties={"namespaces"})

    for ids in namespaces['namespaces']:

        for attribute, value in namespaces['namespaces'][ids].items():

            if attribute == "canonical" and value == "Template":

                template_namespace = namespaces['namespaces'][ids].get("*")

    print("LOCAL NAMESPACE: " + template_namespace)

    if arguments["-i"] == True:

        dump = Iterator.from_file(bz2.open(arguments["-f"], "r"))

        #STAMPO L'ELENCO DEI TEMPLATE

        out = csv.writer(open("templatetable.csv", "w"))

        for page in dump:

            if page.namespace == 10:

                out.writerow([page.title.rsplit(":")[-1]])

        r = ""

        while (r != "Y"):

            r = input ("Templatetable inizializated. Continue? (Y/N).")

            if (r == "N"):

                exit()

    if arguments["-v"] == True:

        dump = Iterator.from_file(bz2.open(arguments["-f"], "r"))
        
        print("Calculating pages number...", end=" ", flush=True)

        pages_number = 0

        for page in dump:

            if page.namespace == 0:

                pages_number += 1

        print("PAGES NUMBER: " + str(pages_number))

    wordlist = set([line.strip() for line in open("magicwords.csv", 'r')])

    if arguments['--list']:

        l = open(arguments['--list'], "r")

        lines = l.read().splitlines()

        for line in lines:

            executeoutput(line, line + ".csv")

    else:

        if arguments['-o']:

            o = arguments['-o']

        else:

            o = arguments['-f']

        o = o + ".csv"

        executeoutput(arguments['-f'], o)