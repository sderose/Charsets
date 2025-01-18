#!/usr/bin/env python3
#
# findBadChars.py
# 2023-07-25: Written by Steven J. DeRose.
#
import sys
import os
import codecs
import unicodedata
from typing import List
import logging

lg = logging.getLogger("findBadChars.py")

__metadata__ = {
    "title"        : "findBadChars",
    "description"  : "Scan for non-Unicode or suspicious characters.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.11",
    "created"      : "2023-07-25",
    "modified"     : "2024-06-24",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Name=
findBadChars: Scan for non-Unicode or suspicious characters.


=Description=

Reports the number and optional positions of "bad" Unicode characters
in the input. Specifically:

* C0 and C1 control characters other than CR, LF, TAB, and space
* Private Use characters
* Unassigned characters

Options --latin, --greek, and --hebrew
cause the script to consider all characters bad except those for
the orthographies whose options are set. However, ASCII is always considered
ok, mainly to allow for markup and for \\t\\r\\n.

--typography allows the Punctuation and Space categories, and is meant
to facilitate checking Latinate texts that use nice quotes, dashes,
spaces, etc. However, it allows all spaces and punctuation, so it is
probably more forgiving than it ought to be.

--bit is shorthand to set all 4 of these options, because I use them a lot.

For each input line that contains bad characters, the line number,
number of bad characters found, and the line itself are shown.
With --details, each individual bad character is also shown, with
the column, hex code point, and literal character.

The --normal [type] option (still experimental)
lets you check for characters not in a
particular Unicode normal form (see below). However, --details does not
apply to these cases; they are merely reported by line, and not counted.
Also, false positives may occur with form NFKC because it may not be strictly
idempotent (the check here is done by normalizing each line and then comparing
to the original).


==Usage==

    findBadChars.py [options] [files]


=See also=

My ''countChars'' -- give total counts for all characters, and total
by Unicode plane, block, and category. Can also be set to recognize
character escapes using conventions Python, XML, URLs, etc.

My `badMappings.py` -- tries to help analyze character set corruption.


=Known bugs and Limitations=

Does not support reporting counts of particular bad characters.
For that use my `countChars`.


=To do=

Option to check if characters for specific languages are in the right
markup constructs (xml:lang="XX" or similar).

Option to rule out all but certain quote types? Perhaps better separately.

Colorize the bad chars?

Consider some others categories to allow with --typography or other option?
* Dingbats
* Combining characters
* fractions, copyright, trademark, pilcrow, pound
* medial s
* Common math like therefore, multiply, degree, inf, plusmn, deg
* superscripts/subscripts
* Narrower typgography set? nbsp, lsquo rsquo ldquo rdquo mdash shy deg ndash
dag ddag bull hellip copy reg trade.
* ES? iexcl iquest ntilde [aeiou]acute uuml ordm ordf
* LAtin1?


=History=

* 2023-07-25: Written by Steven J. DeRose.
* 2024-06-24ff: Add --latin, --normal, etc.


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
        if (sys.stdin.isatty() and not args.quiet): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            lg.info("Cannot open '%s':\n    %s", path, e)
            return 0

    recnum = 0
    for rec in fh.readlines():
        recnum += 1
        isNormalForm = isInNF(rec)
        theBaddies = getBadCharList(rec)
        if (not theBaddies and isNormalForm): continue
        print("Record #%5d (%2d bad): %s" %
            (recnum, len(theBaddies), rec), end="")
        if (args.details and theBaddies):
            for tb in theBaddies:
                print("    Offset %3d: U+%05x ('%s') %s" %
                    (tb[0], ord(tb[1]), tb[1],
                    unicodedata.name(tb[1], "Unknown") if args.details else ""))
    if  (fh != sys.stdin): fh.close()
    return recnum

def isInNF(s:str) -> bool:
    """If --normal is set, check that the record is in the chosen Unicode
    normal form, and return True if not.
    This assumes all the normalizers are idempotent, which may not be
    quite true for form NFKC.
    """
    if (not args.normal): return True
    nfString = unicodedata.normalize(args.normal, s)
    return nfString == s

def getBadCharList(s:str) -> List:
    """Scan a str for bad characters as defined by the options in use,
    and return a list of (offset, char) pairs. If the list is empty,
    all the characters are ok.
    """
    badList = []
    for _col, c in enumerate(s):
        n = ord(c)
        isBad = False
        if (isControl(n) and c not in "\r\n\t "): isBad = True
        elif (isPrivateUse(n)): isBad = True
        elif (n > 255 and isUnassigned(n)): isBad = True
        elif (args.latin or args.greek or args.hebrew): isBad = not isForLanguage(n)
        if (isBad): badList.append( ( _col, c ) )
    return badList

def isControl(n:int) -> bool:
    if (n <= 0x1F): return True
    if (0x7F <= n <= 0x9F): return True  # Yup, \x7F is a control (DELETE)
    return False

def isPrivateUse(n:int) -> bool:
    if (0xE000 <= n <= 0xF8FF): return True
    if (0x000F0000 <= n <= 0x000FFFFD): return True
    if (0x00100000 <= n <= 0x0010FFFD): return True
    return False

def isUnassigned(n:int) -> bool:
    try:
        _name = unicodedata.name(chr(n))
        return False
    except ValueError:
        return True

def isForLanguage(n:int) -> bool:
    """Unlike the prior methods, this checks for good characters (that is,
    ones in the language(s) chosen, or ascii which is always allowed; and
    any leftovers are considered bad.
    """
    c = chr(n)
    if (c.isascii()): return True
    found = False
    category = unicodedata.category(c)
    uname = unicodedata.name(c, "Unknown")
    if (args.latin and "LATIN" in uname): found = True
    elif (args.greek and "GREEK" in uname): found = True
    elif (args.hebrew and "HEBREW" in uname): found = True
    elif (args.typography and
        (category[0] in "PZ" or c in "\xAD")):
        found = True
    return found


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
            "--bib", action="store_true",
            help="Shorthand for --latin --greek --hebrew --typography.")
        parser.add_argument(
            "--color",  # Don't default. See below.
            help="Colorize the output.")
        parser.add_argument(
            "--details", action="store_true",
            help="For all instances, show code point, column, and char.")
        parser.add_argument(
            "--greek", action="store_true",
            help="Allow Greek characters.")
        parser.add_argument(
            "--hebrew", action="store_true",
            help="Allow Hebrew characters.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--latin", action="store_true",
            help="Allow Latin characters")
        parser.add_argument(
            "--names", action="store_true",
            help="With --details, also show full character names.")
        parser.add_argument(
            "--normal", type=str, metavar="S",
            choices=[ "NFKC", "NFKD", "NFC", "NFD" ],
            help="Report lines with characters not in the specified Unicode NF.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--recursive", action="store_true",
            help="Descend into subdirectories.")
        parser.add_argument(
            "--typography", action="store_true",
            help="Allow all Unicode space and punctuation charcters.")
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

        if (args0.bib):
            args0.latin = args0.greek = args0.hebrew = args0.typography = True

        return(args0)

    args = processOptions()

    if (len(args.files) == 0):
        lg.warning("findBadChars.py: No files specified....")
        doOneFile(None)
    else:
        for path0 in args.files:
            doOneFile(path0)
