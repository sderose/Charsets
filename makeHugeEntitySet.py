#!/usr/bin/env python3
#
# makeHugeEntitySet.py: Generate named entities broadly.
# 2024-07-16: Written by Steven J. DeRose.
#
import sys
import re
import logging

import unicodedata
from collections import defaultdict

lg = logging.getLogger("makeHugeEntitySet")

__metadata__ = {
    "title"        : "makeHugeEntitySet",
    "description"  : "Generate named entities broadly.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.9",
    "created"      : "2024-07-16",
    "modified"     : "2024-07-16",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Name=

makeHugeEntitySet: Generate named entities broadly.

[unfinished]


=Description=

Go through Unicode and generate entity names for a wide range of
characters.

For now, focused on letters, with this construction:
    * 2-letter language (or orthography?) code
    * .
    * the token after "LETTER" in the Unicode name
    * For lower, title, and upper case, use it.
    * a dot-separated token for each "WITH" item
    * _ and In/Med/Fin/Iso

==Usage==

    makeHugeEntitySet.py [options] [files]


=Notes


=Known bugs and Limitations=


=To do=


=History=

* 2024-07-16: Written by Steven J. DeRose.


=Rights=

Copyright 2024-07-16 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/] for more information.

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""

width = { "FULLWIDTH", "HALFWIDTH" }

# https://en.wikipedia.org/wiki/ISO_15924
# cf utData
# These should really use orthgraphic system codes, not language codes.
#
lang = {
    "ARABIC":                           "ar", #ara
    "ARMENIAN":                         "hy",# arm
    "BALINESE":                         "ban",
    "BAMUM":                            "",
    "BATAK":                            "",
    "BENGALI":                          "bn", #ben
    "BOPOMOFO":                         "",
    "BUGINESE":                         "bug",
    "BUHID":                            "",
    "CHAM":                             "cmc",
    "CHEROKEE":                         "chr",
    "COPTIC":                           "cop",
    "CYRILLIC":                         "",
    "DEVANAGARI":                       "",
    "GEORGIAN":                         "ka", #kat
    "GLAGOLITIC":                       "",
    "GREEK":                            "el", #ell
    "GUJARATI":                         "gu", #guj
    "GURMUKHI":                         "",
    "HANGUL":                           "",
    "HANUNOO":                          "",
    "HEBREW":                           "he", #heb
    "HIRAGANA":                         "",
    "JAVANESE":                         "jv", #jav
    "KANNADA":                          "kn", #kan
    "KATAKANA":                         "",
    "KAYAH LI":                         "",
    "KHMER":                            "km", #khm
    "LAO":                              "lo", #lao
    "LATIN":                            "la", #lat
    "LEPCHA":                           "",
    "LIMBU":                            "",
    "LISU":                             "",
    "MALAYALAM":                        "ml", #mal
    "MANDAIC":                          "",
    "MEETEI MAYEK":                     "",
    "MONGOLIAN":                        "",
    "MYANMAR":                          "",
    "NEW TAI LUE":                      "",
    "NKO":                              "nqo",
    "OGHAM":                            "",
    "OL CHIKI":                         "",
    "ORIYA":                            "",
    "PHAGS-PA":                         "",
    "REJANG":                           "",
    "RUNIC":                            "",
    "SAMARITAN":                        "sam",
    "SAURASHTRA":                       "",
    "SINHALA":                          "si", #sin
    "SUNDANESE":                        "su", #sun
    "SYLOTI NAGRI":                     "",
    "SYRIAC":                           "syr",
    "TAGALOG":                          "tl", #tgl
    "TAGBANWA":                         "",
    "TAI LE":                           "",
    "TAI THAM":                         "",
    "TAI VIET":                         "",
    "TAMIL":                            "ta", #tam
    "TELUGU":                           "te", #tel
    "THAANA":                           "",
    "TIBETAN":                          "bo", #bod
    "TIFINAGH":                         "",
}

caseTurn = {
    "CAPITAL", "SMALL", "SMALL CAPITAL", "SMALL TURNED", "SMALL REVERSED", "SMALL TOP HALF",
    "SIDEWAYS", "SIDEWAYS TURNED", "SHORT", "EPIGRAPHIC", "SUBSCRIPT SMALL", "MODIFIER",
    "SUBJOINED SUPERFIXED",
}

form = {
    "FINAL FORM", "INITIAL FORM", "ISOLATED FORM", "MEDIAL FORM",
}

prefix = {
    "WIDE", "TURNED", "STRETCHED", "STRAIGHT", "SQUAT REVERSED",
    "ARCHAIC", "BARRED", "BLACKLETTER",
    "CLOSED", "OPENED", "REVERSED", "CROSSED", "DOTLESS", "DOUBLE",
}

suffix = {
    "DIGRAPH", "ABOVE", "REVERSED",
}
"""
    FINAL w/o "FORM"

    TONE ....

    SYLLABLE

    Math ...
"""

def countParts():
    catL = noLETTER = 0
    priors = defaultdict(int)
    letters = defaultdict(int)
    withs = defaultdict(int)
    forms = defaultdict(int)

    for i in range(65535):
        try:
            c = chr(i)
            cat = unicodedata.category(c)
            if (not cat.startswith("L")): continue
            nam = unicodedata.name(c)
        except KeyError:
            continue
        catL += 1
        if ("LETTER" not in nam):
            noLETTER += 1
            continue

        ### FORM
        mat = re.search(r" (\w+) FORM\b", nam)
        if (mat):
            forms[mat.group(1)] += 1
            nam = re.sub(r" (\w+) FORM\b", "", nam)

        ### WITH
        mat = re.search(r" WITH (.*)$", nam)
        if (mat):
            withs[mat.group(1)] += 1
            nam = re.sub(r" WITH .*$", "", nam)

        mat = re.match(r"^(.*) LETTER (.*?)$", nam)
        if (not mat):
            lg.error("Huh? %s", nam)
            continue
        priors[mat.group(1)] += 1
        letters[mat.group(2)] += 1

    showDict(priors, "Priors")
    showDict(letters, "Letters")
    showDict(withs, "Withs")
    showDict(forms, "Forms")

def showDict(d, hed:str):
    print("\n\n####### %s (%d)" % (hed, len(d)))
    for k in sorted(d.keys()):
        print("    %6d  %s " % (d[k], k))


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse

    def processOptions() -> argparse.Namespace:
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--ignoreCase", "-i", action="store_true",
            help="Disregard case distinctions.")
        parser.add_argument(
            "--oencoding", type=str, metavar="E", default="utf-8",
            help="Use this character coding for output. Default: iencoding.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--unicode", action="store_const", dest="iencoding",
            const="utf8", help="Assume utf-8 for input files.")
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Add more messages (repeatable).")
        parser.add_argument(
            "--version", action="version", version=__version__,
            help="Display version information, then exit.")

        parser.add_argument(
            "files", type=str, nargs=argparse.REMAINDER,
            help="Path(s) to input file(s)")

        args0 = parser.parse_args()
        if (lg and args0.verbose):
            logging.basicConfig(level=logging.INFO - args0.verbose)

        return(args0)


    ###########################################################################
    #
    args = processOptions()
    if (args.iencoding and not args.oencoding):
        args.oencoding = args.iencoding
    if (args.oencoding):
        # https://stackoverflow.com/questions/4374455/
        # sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stdout.reconfigure(encoding="utf-8")

    countParts()
