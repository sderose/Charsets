#!/usr/bin/env python3
#
# findBadChars.py
# 2023-07-25: Written by Steven J. DeRose.
#
import sys
import os
import codecs

import logging
lg = logging.getLogger("findBadChars.py")

def info0(msg:str) -> None:
    if (args.verbose >= 0): lg.info(msg)
def info1(msg:str) -> None:
    if (args.verbose >= 1): lg.info(msg)
def info2(msg:str) -> None:
    if (args.verbose >= 2): lg.info(msg)
def fatal(msg:str) -> None:
    lg.critical(msg); sys.exit()

__metadata__ = {
    "title"        : "findBadChars.py",
    "description"  : "Scan for non-Unicode or suspicious characters.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.9",
    "created"      : "2023-07-25",
    "modified"     : "2023-11-23",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Name=
    """ +__metadata__["title"] + ": " + __metadata__["description"] + """


=Description=

==Usage==

    findBadChars.py [options] [files]


=See also=

''countChars''


=Known bugs and Limitations=


=To do=

Doesn't yet report undefined characters.


=History=

* 2023-07-25: Written by Steven J. DeRose.


=Rights=

Copyright 2023-07-25 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/] for more information.

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
#
def doOneFile(path:str) -> int:
    """Read and deal with one individual file.
    """
    if (not path):
        if (sys.stdin.isatty()): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            info0("Cannot open '%s':\n    %s" % (path, e))
            return 0

    recnum = 0
    for rec in fh.readlines():
        recnum += 1
        if (countBadChars(rec)):
            print("Record #%5d: %s" % (recnum, rec))
    if  (fh != sys.stdin): fh.close()
    return recnum

def countBadChars(s:str) -> int:
    nbad = 0
    for _col, c in enumerate(s):
        n = ord(c)
        if (isControl(n) and c not in "\r\n\t "): nbad += 1
        elif (isPrivateUse(n)): nbad += 1
        elif (isUnassigned(n)): nbad += 1
    return nbad

def isControl(n:int) -> bool:
    if (n <= 0x1F): return True
    if (0x7F <= n <= 0x9F): return True  # Yup, \x7F is a control (DELETE)
    return False

def isPrivateUse(n:int) -> bool:
    if (0xE000 <= n <= 0xF8FF): return True
    if (0x000F0000 <= n <= 0x000FFFFD): return True
    if (0x00100000 <= n <= 0x0010FFFD): return True
    return False

def isUnassigned(_n:int) -> bool:
    return False  # TODO Finish


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse
    def anyInt(x:str) -> int:
        return int(x, 0)

    def processOptions() -> argparse.Namespace:
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--color",  # Don't default. See below.
            help="Colorize the output.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--recursive", action="store_true",
            help="Descend into subdirectories.")
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

        if (args0.color is None):
            args0.color = ("CLI_COLOR" in os.environ and sys.stderr.isatty())
        #lg.setColors(args0.color)
        return(args0)

    ###########################################################################
    #
    args = processOptions()

    if (len(args.files) == 0):
        lg.warning("findBadChars.py: No files specified....")
        doOneFile(None)
    else:
        for path0 in args.files:
            doOneFile(path0)
