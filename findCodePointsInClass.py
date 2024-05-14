#!/usr/bin/env python3
#
# findCodePointsInClass.py: Display all Unicode chars in (any or no) category.
# 2022-10-04: Written by Steven J. DeRose.
#
import sys
import unicodedata

#import logging
#lg = logging.getLogger("findUnassignedCodePoints.py")

__metadata__ = {
    "title"        : "findUnassignedCodePoints",
    "description"  : "Display all Unicode chars in (any or no) category.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.9",
    "created"      : "2022-10-04",
    "modified"     : "2023-11-23",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Name=
    """ +__metadata__["title"] + ": " + __metadata__["description"] + """


=Description=

[superceded by showUnicodeCharsInClass.py]

==Usage==

    findCodePointsInClass.py [options] [files]

Scan for characters that are in some one- or two-letter Unicode category.
By default, searches for category "Cn", "Unassigned".

Note: The following characters do not come back as unicodedata.category
"Unassigned", but seem to have "meta" names, and are kind of weird/special:

    0080;<control>;Cc;0;BN;;;;;N;;;;;
    0081;<control>;Cc;0;BN;;;;;N;;;;;
    0084;<control>;Cc;0;BN;;;;;N;;;;;
    0099;<control>;Cc;0;BN;;;;;N;;;;;
    3400;<CJK Ideograph Extension A, First>;Lo;0;L;;;;;N;;;;;
    4DB5;<CJK Ideograph Extension A, Last>;Lo;0;L;;;;;N;;;;;
    4E00;<CJK Ideograph, First>;Lo;0;L;;;;;N;;;;;
    9FCC;<CJK Ideograph, Last>;Lo;0;L;;;;;N;;;;;
    AC00;<Hangul Syllable, First>;Lo;0;L;;;;;N;;;;;
    D7A3;<Hangul Syllable, Last>;Lo;0;L;;;;;N;;;;;
    D800;<Non Private Use High Surrogate, First>;Cs;0;L;;;;;N;;;;;
    DB7F;<Non Private Use High Surrogate, Last>;Cs;0;L;;;;;N;;;;;
    DB80;<Private Use High Surrogate, First>;Cs;0;L;;;;;N;;;;;
    DBFF;<Private Use High Surrogate, Last>;Cs;0;L;;;;;N;;;;;
    DC00;<Low Surrogate, First>;Cs;0;L;;;;;N;;;;;
    DFFF;<Low Surrogate, Last>;Cs;0;L;;;;;N;;;;;
    E000;<Private Use, First>;Co;0;L;;;;;N;;;;;
    F8FF;<Private Use, Last>;Co;0;L;;;;;N;;;;;

The Private Use areas can also be considered an edge-case of "defined":
    U+00E000–U+00F8FF
    U+0F0000–U+0FFFFD
    U+100000–U+10FFFD


=See also=

`showUnicodeCharsInClass.py` is a much better version.


=Known bugs and Limitations=


=To do=


=History=

* 2022-10-04: Written by Steven J. DeRose.


=Rights=

Copyright 2022-10-04 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/] for more information.

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse
    def anyInt(x:str) -> int:
        try:
            return int(x, 0)
        except ValueError as e:
            return e

    def processOptions() -> argparse.Namespace:
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--category", type=str, default="Cn",
            help="Unicode category to search for.")
        parser.add_argument(
            "--group", action="store_true",
            help="Report ranges, not just individual characters.")
        parser.add_argument(
            "--join", action="store_true",
            help="Do not put each char/range on a separate line.")
        parser.add_argument(
            "--literal", action="store_true",
            help="Also show the character as a literal.")
        parser.add_argument(
            "--max", type=anyInt, default=0xFFFF,
            help="Last character to check.")
        parser.add_argument(
            "--min", type=anyInt, default=0x0000,
            help="First character to check.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Add more messages (repeatable).")
        parser.add_argument(
            "--version", action="version", version=__version__,
            help="Display version information, then exit.")

        args0 = parser.parse_args()
        #if (lg and args0.verbose):
            #logging.basicConfig(level=logging.INFO - args0.verbose)

        return(args0)

    def printSingleton(cp:int) -> None:
        if (args.literal):
            print("\\u%04x  '%s'" % (cp, chr(cp)), end=ender)
        else:
            print("\\u%04x" % (cp), end=ender)

    def printRange(cp1:int, cp2) -> None:
        if (args.literal):
            print("\\u%04x-\\u%04x  '%s'-'%s'" %
                (cp1, cp2, chr(cp1), chr(cp2)), end=ender)
        else:
            print("\\u%04x-\\u%04x" % (cp1, cp2), end=ender)


    ###########################################################################
    #
    args = processOptions()
    if (len(args.category) < 1 or len(args.category) > 2 or
        not args.category.istitle()):
        sys.stderr.write("--category must be one or two letters.")
        sys.exit()

    ender = "\n"
    if args.join: ender = ""

    lastU = 0x0000
    nFound = 0
    for i in range(args.min, args.max+1):
        ucat = unicodedata.category(chr(i))
        if (ucat.startswith(args.category)):
            nFound += 1
            if (not args.group): printSingleton(i)
        else:
            if (args.group and lastU < i-1):
                if (lastU+1 == i-1): printSingleton(i)
                else: printRange(lastU+1, i-1)
            lastU = i

    if (args.group and lastU < i-1):
        printRange(lastU+1, i-1)

    print("")
    print("*** Total code points in category '%s': %d." % (args.category, nFound))
