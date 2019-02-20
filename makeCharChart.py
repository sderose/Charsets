#!/usr/bin/env python
#
# makeCharChart: Written 2013-04-24 by Steven J. DeRose.
#
# ~2014-06-17: Written. Copyright by Steven J. DeRose.
# 2014-10-28: Renamed from showASCIIChart. Support Unicode, HTML, options.
#
# Creative Commons Attribution-Share-alike 3.0 unported license.
# See http://creativecommons.org/licenses/by-sa/3.0/.
#
# To do:
#
from __future__ import print_function
import sys, argparse
import re
#import string
import codecs
import unicodedata

#from sjdUtils import sjdUtils
from alogging import ALogger
from MarkupHelpFormatter import MarkupHelpFormatter

lg = ALogger(1)
__version__ = "2014-10-28"


###############################################################################
#
def processOptions():
    "Parse command-line options and arguments."
    parser = argparse.ArgumentParser(
        description="""
Display a chart of the characters in a given range of (Unicode) code points.
The characters are written assumsing a given encoding (I<--oencoding>).

The chart can be written in your choice of character encoding,
and in I<text> or I<html>.

=head1 Related commands:

C<dumpx> -- show files in hex and other forms

C<chr>, C<ord> -- get information about characters.

=head1 Licensing

Copyrigh 2014, Steven J. DeRose. Released under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See L<http://creativecommons.org/licenses/by-sa/3.0/>.
        """,
        formatter_class=MarkupHelpFormatter
    )
    parser.add_argument(
        "--badChar",          type=int, metavar='M', default=ord('?'),
        help='Code point of char to print for unprintables.')
    parser.add_argument(
        "--blankRows",        type=int, metavar='N', default=8,
        help='Insert a blank line after every N rows.')
    parser.add_argument(
        "--decimal",          action='store_true',
        help='Show decimal code point under each character.')
    parser.add_argument(
        "--entity",           type=str, metavar='X', default="",
        choices = [ "dec", "hex" ],
        help='Include a row with HTML/XML numeric character references, ' +
        'in dec or hex.')
    parser.add_argument(
        "--format",           type=str, metavar='F', default="text",
        choices = [ "text", "html" ],
        help='What format to write the data in.')
    parser.add_argument(
        "--min",              type=int, metavar='M', default=0,
        help='First code point.')
    parser.add_argument(
        "--max",              type=int, metavar='M', default=255,
        help='Last code point.')
    parser.add_argument(
        "--oencoding",        type=str, metavar='E',
        help='Use this character set for output files.')
    parser.add_argument(
        "--perCell",          type=int, metavar='C', default=4,
        help='Number of spaces to allow for each column of the chart.')
    parser.add_argument(
        "--perRow",           type=int, metavar='R', default=16,
        help='Number of code points to show in each row of the chart.')
    parser.add_argument(
        "--quiet", "-q",      action='store_true',
        help='Suppress most messages.')
    parser.add_argument(
        "--ucategory",        action='store_true',
        help='Show the Unicode character-class mnemonic under each character.')
    parser.add_argument(
        "--utf8",             action='store_true',
        help='Show UTF-8 hexadecimal under each character.')
    parser.add_argument(
        "--verbose", "-v",    action='count',       default=0,
        help='Add more messages (repeatable).')
    parser.add_argument(
        "--version",          action='version',     version='Version of '+__version__,
        help='Display version information, then exit.')

    args0 = parser.parse_args()
    lg.setVerbose(args0.verbose)

    if (args0.min>=args0.max or args0.min<0 or args0.max>65535):
        lg.fatal("--min and/or --max out of range.")

    # Make sure cells are wide enough for utf display (check dec/hex too?)
    if (args0.utf8 and (
        args0.max >= 0x0000080 and args0.perCell<4 or
        args0.max >= 0x0000800 and args0.perCell<6 or
        args0.max >= 0x0010000 and args0.perCell<8 or
        args0.max >= 0x0200000 and args0.perCell<10 or
        args0.max >= 0x4000000 and args0.perCell<12)):
        lg.error("--perCell width of %d is too narrow for --utf8 of --max %d." %
            (args0.perCell, args0.max))
    return(args0)


def printable(i):
    if (i<=32):
        i = 0x2400 + i
    elif (re.match(r'\s', unichr(i), re.U)):
        i = 0x2420 # SP
    elif (i>=128 and i<160):
        i = int(args.badChar)
    try:
        u = unichr(i)
    except UnicodeDecodeError as e:
        lg.error("Can't map %d to Unicode:\n    %s" % (i, e))
    return(u)

def makeCell(s):
    c = startCell + s.rjust(args.perCell) + endCell
    return(c)

def uprint(s=""):
    print(s)

def getUClass(u):
    """Returns the Unicode class of a character, as a 2-letter mnemonic.
    """
    ucat  = unicodedata.category(u)
    return(ucat)

###############################################################################
###############################################################################
# Main
#
args = processOptions()

if (args.oencoding):
    sys.stdout = codecs.getwriter(args.oencoding)(sys.stdout)

if (args.format == "html"):
    startCell = "<td>"
    endCell = "</td>"
    startRow = "<tr>"
    endRow = "</tr>"
elif (args.format == "text"):
    startCell = ""
    endCell = ""
    startRow = ""
    endRow = ""
else:
    lg.fatal("Unknown --format '%s'." % args.format)

theStart = int(args.min / args.perRow)
theEnd = args.max
if (args.max % args.perRow):
    finalBlanks = args.perRow - (args.max % args.perRow)
else:
    finalBlanks = 0

nRows = (theEnd-theStart) / args.perRow
lg.vMsg(1, "range: %d to %d, in %d rows." % (theStart, theEnd, nRows))

if (args.format == "html"):
    uprint("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
	"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
	<meta http-equiv="content-type" content="text/html; charset=utf-8" />
	<title>Untitled</title>
</head>
<body>
""")

head = "        "
for n in range(0,args.perRow):
    head += ("%4x" % n).center(args.perCell)
sep  = "-" * len(head)
uprint(head)
uprint(sep)

for row in range(0, nRows):
    if (startRow): uprint(startRow)
    buf1 = makeCell("x%04x:  " % (theStart + (row*args.perRow)))
    buf2 = makeCell("  dec:  ")
    buf3 = makeCell("  utf:  ")
    buf4 = makeCell(" ucat:  ")
    buf5 = makeCell(" ents:  ")

    for col in range(0,args.perRow):
        codePoint = theStart + (row*args.perRow) + col
        theChar = unichr(codePoint)
        buf1 += makeCell(printable(codePoint))
        buf2 += makeCell(("%d" % codePoint))
        theBytes = unichr(codePoint).encode('utf-8')
        cell = ""
        esc = ""
        for b in theBytes:
            cell += "%02x" % (ord(b))
            esc += "%%02x" % (ord(b))
        buf3 += makeCell(cell)
        buf4 += makeCell(getUClass(theChar))
        if (args.entity == "dec"): buf5 += makeCell("&#%d;" % codePoint)
        else: buf5 += makeCell("&#x%x;" % codePoint)
        buf6 = makeCell(esc)

    uprint(buf1)
    if (args.decimal):   uprint(buf2)
    if (args.utf8):      uprint(buf3)
    if (args.ucategory): uprint(buf4)
    if (args.entity):    uprint(buf5)
    if (endRow): uprint(endRow)

    if (not row % args.blankRows):
        if (startRow): uprint(startRow)
        uprint("")
        uprint(head)
        uprint(sep)
        if (endRow): uprint(endRow)

if (args.format == "html"):
    uprint("""</body>
</html>
""")
sys.exit()

