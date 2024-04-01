#!/usr/bin/env python3
#
# makeCharChart: Display info on range of Unicode code points.
# 2013-04-24: Written by Steven J. DeRose.
#
import sys
import argparse
import re
import codecs
import unicodedata
from math import floor
import logging

lg = logging.getLogger("makeCharChart")

__metadata__ = {
    "title"        : "makeCharChart",
    "description"  : "Display info on range of Unicode code points.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 2.7.6, 3.6",
    "created"      : "2013-04-24",
    "modified"     : "2020-02-14",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']


descr = """
=Usage=

Display a chart of the characters in any given range of (Unicode) code points.
The characters are written assuming a given encoding (I<--oencoding>), which
should match the device/program you want to display with.

The chart can be written in your choice of ''text'' or ''html''.

C0 control characters are shown as their associated 'pictures' (U+2400 and
following). The layout is like:

               0   1   2   3   4   5   6   7   8   9   a   b   c   d   e   f
    ------------------------------------------------------------------------
    x0020:         !   "   #   $   %   &   '   (   )   *   +   ,   -   .   /
    x0030:     0   1   2   3   4   5   6   7   8   9   :   ;   <   =   >   ?
    x0040:     @   A   B   C   D   E   F   G   H   I   J   K   L   M   N   O
    x0050:     P   Q   R   S   T   U   V   W   X   Y   Z   [   \\   ]   ^   _
    x0060:     `   a   b   c   d   e   f   g   h   i   j   k   l   m   n   o
    x0070:     p   q   r   s   t   u   v   w   x   y   z   {   |   }   ~
=
Specify the desired code point range via ''--min'' and ''--max'', which can
be given as decimal, 0x hex, or 0 octal. Each row of the chart will begin
at a character whose code point is a multiple of the number of columns shown
per row (''--perRow'', default 16).


=Related commands=

`dumpx`, `od` -- show files in hex and other forms

`chr`, `ord`, `CharDisplay.py` -- get information about characters.

=Known bugs and Limitations=

Doesn't do anything special for fullwidth characters in text mode.

Probably should offer octal, too. Maybe full `CharDisplay.py` layout?


=Rights=

Copyright 2013 by Steven J. DeRose. This work is licensed under a Creative Commons
Attribution-Share Alike 3.0 Unported License. For further information on
this license, see [http://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities] or
[http://github.com/sderose].


=History=

* Written 2013-04-24 by Steven J. DeRose.
* 2014-10-28: Renamed from showASCIIChart. Support Unicode, HTML, options.
* 2020-02-14: New layout, lint, allow hex and octal option values.
Move sep line to right place. Fix HTML.


=Options=
"""


def printable(i):
    if (i<=32):
        i = 0x2400 + i
    elif (re.match(r'\s', chr(i), re.U)):
        i = 0x2420 # SP
    elif (i>=128 and i<160):
        i = int(args.badChar)
    try:
        u = chr(i)
    except UnicodeDecodeError as e:
        lg.error("Can't map %d to Unicode:\n    %s", i, e)
    return u

def uprint(s=""):
    print(s)

def getUClass(u):
    """Returns the Unicode class of a character, as a 2-letter mnemonic.
    """
    ucat  = unicodedata.category(u)
    return ucat


###############################################################################
#
def doHTML():
    theStart = int(args.min / args.perRow)
    theEnd = args.max
    #if (args.max % args.perRow):
    #    finalBlanks = args.perRow - (args.max % args.perRow)
    #else:
    #    finalBlanks = 0

    nRows = floor((theEnd-theStart) / args.perRow)
    lg.log(logging.INFO-1, "range: %d to %d, in %d rows.", theStart, theEnd, nRows)

    uprint("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <title>Untitled</title>
    <style type="text/css">
    td   { text-align:center; }
    </style>
</head>
<body>
<p>&#160;</p>
<table border="border">
""")

    head = makeHTMLHead()
    for row in range(0, nRows):
        firstValue = theStart + row*args.perRow

        if (row % args.blankRows == 0):
            uprint(head)

        uprint("<tr>")
        buf1 = makeHTMLCell("x%04x:  " % firstValue)
        buf2 = makeHTMLCell("  dec:  ")
        buf3 = makeHTMLCell("  utf:  ")
        buf4 = makeHTMLCell(" ucat:  ")
        buf5 = makeHTMLCell(" ents:  ")

        for col in range(0,args.perRow):
            codePoint = firstValue + col
            theChar = chr(codePoint)
            buf1 += makeHTMLCell(printable(codePoint))
            buf2 += makeHTMLCell(("%d" % codePoint))
            theBytes = chr(codePoint).encode('utf-8')
            cell = ""
            esc = ""
            for b in theBytes:
                cell += "%02x" % (b)
                esc += "%%%02x" % (b)
            buf3 += makeHTMLCell(cell)
            buf4 += makeHTMLCell(getUClass(theChar))
            if (args.entity == "dec"): buf5 += makeHTMLCell("&#%d;" % codePoint)
            else: buf5 += makeHTMLCell("&#x%x;" % codePoint)
            #buf6 = makeHTMLCell(esc)

        uprint(buf1)
        if (args.decimal):   uprint(buf2)
        if (args.utf8):      uprint(buf3)
        if (args.ucategory): uprint(buf4)
        if (args.entity):    uprint(buf5)
        uprint("</tr>")

    uprint("</table>\n</body>\n</html>\n")

def makeHTMLHead():
    head = '<tr style="font-weight:bold;"><th>&#160;</th>'
    for n in range(0, args.perRow):
        head += ("<th>%x</th>" % n)
    head += "</tr>\n"
    return head

def makeHTMLCell(s):
    c = "<td>%s</td>" % (s)
    return c


###############################################################################
def doText():
    theStart = int(args.min / args.perRow)
    theEnd = args.max
    #if (args.max % args.perRow):
    #    finalBlanks = args.perRow - (args.max % args.perRow)
    #else:
    #    finalBlanks = 0

    nRows = floor((theEnd-theStart) / args.perRow)
    lg.log(logging.INFO-1, "range: %d to %d, in %d rows.", theStart, theEnd, nRows)

    head = makeTextHead()
    sepLine  = "-" * len(head)

    for row in range(0, nRows):
        firstValue = theStart + row*args.perRow
        # OR: if (
        if ((row % args.blankRows) == 0):
            uprint("")
            uprint(head)
            uprint(sepLine)

        buf1 = makeTextCell("x%04x:  " + str(firstValue))
        buf2 = makeTextCell("  dec:  ")
        buf3 = makeTextCell("  utf:  ")
        buf4 = makeTextCell(" ucat:  ")
        buf5 = makeTextCell(" ents:  ")

        for col in range(0,args.perRow):
            codePoint = firstValue + col
            theChar = chr(codePoint)
            buf1 += makeTextCell(printable(codePoint))
            buf2 += makeTextCell(("%d" % codePoint))
            theBytes = chr(codePoint).encode('utf-8')
            cell = ""
            esc = ""
            for b in theBytes:
                cell += "%02x" % (b)
                esc += "%%%02x" % (b)
            buf3 += makeTextCell(cell)
            buf4 += makeTextCell(getUClass(theChar))
            if (args.entity == "dec"): buf5 += makeTextCell("&#%d;" % codePoint)
            else: buf5 += makeTextCell("&#x%x;" % codePoint)
            #buf6 = makeTextCell(esc)

        uprint(buf1)
        if (args.decimal):   uprint(buf2)
        if (args.utf8):      uprint(buf3)
        if (args.ucategory): uprint(buf4)
        if (args.entity):    uprint(buf5)

def makeTextHead():
    head = "        "
    for n in range(0, args.perRow):
        head += ("%4x" % n).center(args.perCell)
    return head

def makeTextCell(s):
    c = s.rjust(args.perCell)
    return c


###############################################################################
# Main
#
def anyInt(x):
    return int(x, 0)

def processOptions():
    try:
        from BlockFormatter import BlockFormatter
        parser = argparse.ArgumentParser(
            description=descr, formatter_class=BlockFormatter)
    except ImportError:
        parser = argparse.ArgumentParser(description=descr)

    parser.add_argument(
        "--badChar", type=anyInt, metavar='M', default=ord('?'),
        help='Code point of char to print for unprintables.')
    parser.add_argument(
        "--blankRows", type=anyInt, metavar='N', default=8,
        help='Insert a blank line after every N rows.')
    parser.add_argument(
        "--decimal", action='store_true',
        help='Show decimal code point under each character.')
    parser.add_argument(
        "--entity", type=str, metavar='X', default="",
        choices = [ "dec", "hex" ],
        help='Include a row with HTML/XML numeric character references, ' +
        'in "dec" or "hex".')
    parser.add_argument(
        "--format", type=str, metavar='F', default="text",
        choices = [ "text", "html" ],
        help='What format to write the data in ("text" or "html").')
    parser.add_argument(
        "--min", type=anyInt, metavar='M', default=0,
        help='First code point to include in display.')
    parser.add_argument(
        "--max", type=anyInt, metavar='M', default=255,
        help='Last code point to include in display.')
    parser.add_argument(
        "--oencoding", type=str, metavar='E',
        help='Use this character set for output files.')
    parser.add_argument(
        "--perCell", type=anyInt, metavar='C', default=4,
        help='Number of spaces to allow for each column of the chart.')
    parser.add_argument(
        "--perRow", type=anyInt, metavar='R', default=16,
        help='Number of code points to show in each row of the chart.')
    parser.add_argument(
        "--quiet", "-q", action='store_true',
        help='Suppress most messages.')
    parser.add_argument(
        "--ucategory", action='store_true',
        help='Show Unicode character-category mnemonics under characters.')
    parser.add_argument(
        "--utf8", action='store_true',
        help='Show UTF-8 hexadecimal under each character.')
    parser.add_argument(
        "--verbose", "-v", action='count', default=0,
        help='Add more messages (repeatable).')
    parser.add_argument(
        "--version", action='version',
        version='Version of '+__version__,
        help='Display version information, then exit.')

    args0 = parser.parse_args()
    if (lg and args0.verbose):
        logging.basicConfig(level=logging.INFO - args0.verbose)

    if (args0.min>=args0.max or args0.min<0 or args0.max>0x1FFFF):
        lg.fatal("--min and/or --max out of range.")

    # Make sure cells are wide enough for utf display (check dec/hex too?)
    if (args0.utf8 and (
        args0.max >= 0x0000080 and args0.perCell<4 or
        args0.max >= 0x0000800 and args0.perCell<6 or
        args0.max >= 0x0010000 and args0.perCell<8 or
        args0.max >= 0x0200000 and args0.perCell<10 or
        args0.max >= 0x4000000 and args0.perCell<12)):
        lg.error("--perCell width of %d is too narrow for --utf8 of --max %d.",
            args0.perCell, args0.max)
    return args0

args = processOptions()

if (args.oencoding):
    sys.stdout = codecs.getwriter(args.oencoding)(sys.stdout)

if (args.format == "html"):
    doHTML()
elif (args.format == "text"):
    doText()
else:
    lg.fatal("Unknown --format '%s'.", args.format)
    sys.exit()
