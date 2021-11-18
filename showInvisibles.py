#!/usr/bin/env python
#
# showInvisibles: make control and whitespace chars visible.
# 2007-01-1: Written by Steven J. DeRose.
#
from __future__ import print_function
import sys
import os
import codecs
import argparse

from sjdUtils import sjdUtils
import strfchr

PY3 = sys.version_info[0] == 3
if PY3:
    def unichr(n): return chr(n)

__metadata__ = {
    'title'        : "showInvisibles.py",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 2.7.6, 3.6",
    'created'      : "2007-01-16",
    'modified'     : "2021-04-08",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

def warn(msg):
    if (args.verbose): sys.stderr.write(msg+"\n")

descr = """
=Description=

showinvisible.py [options]

(Python version; also available in Perl)

Make control characters and space visible by substituting the Unicode
"control symbols" for them.
Also make non-ASCII characters visible by substituting XML numeric
character references (`&#2022;` etc).
Can also colorize the changed characters.

Useful for visualizing return/linefeed, space/tab, etc. Can also be used
to escape undesired characters in a file to ease later processing (in that
case, specify `--nocolor -s`).


=Known bugs and limitations=

Options `-b` and `-u` are unfinished.


=Related commands=

`ord`, `CharDisplay`. `strfchr.py`.


=History=

* 2007-01-16: Written by Steven J. DeRose.
* 2007-12-31 sjd: Getopt, version, etc.
* 2010-09-27 sjd: Cleanup, -base, -pad, -color, factor out makeCharRef().
* 2011-01-24 sjd: Add control pictures and alternates. binmode STDOUT.
* 2012-01-23 sjd: Fix -color and -base. Use sjdUtils.
* Optimize color-escaping instead of doing on/off for every char.
* 2012-01-23: Converted by perl2python.
* 2012-01-25 sjd: Cleanup.
* 2015-10-13: Update argparse usage. pylint.
* 2021-04-08ff: Better option handling. Drop -s/leaveSpace for --spaceAs SELF.
Hook up to new strfchr.py. Add lots of formats from there.


=To do=

* Options for what to do with line-ends?
* Support bgcolor (nice way to show whitespace chars).


=Rights=

Copyright 2007 by Steven J. DeRose. This work is licensed under a Creative Commons
Attribution-Share Alike 3.0 Unported License. For further information on
this license, see [http://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities] or
[http://github.com/sderose].


=Options=
"""


###############################################################################
#
spaceChoices = [ "B", "U", "SP", "SELF", ]
lfChoices = [ "LF", "NL", "SELF", ]

names = [
    "NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
    "BS",  "HT",  "NL",  "VT",  "FF",  "CR",  "SO",  "SI",
    "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB",
    "CAN", "EM",  "SUB", "ESC", "FS",  "GS",  "RS",  "US",
    "SP"]
if (names[32] != "SP"):
    print("names messed up.")
    exit(0)

backslashCodes = [
    "\\0", "",    "",    "",    "",    "",    "",    "",
    "",    "\\t", "\\n", "\\v", "\\f", "\\r", "",    "",
    "",    "",    "",    "",    "",    "",    "",    "",
    "",    "",    "",    "\\e", "",    "",    "",    "",
    "\\s"
]
assert (backslashCodes[32] == "\\s"), "BackslashCodes messed up."
assert os.environ["PYTHONIOENCODING"] == "utf_8", "PYTHONIOENCODING not utf_8."


###############################################################################
# Construct an XML numeric character reference to the given code point.
# Use the appropriate args.base.
#
def makeCharRef(n):
    if (args.base == 10):
        theFm = '{0:0' + str(args.width) + 'd}'
        ref = "&#" + theFm.format(n) + ";"
    else:
        theFm = '{0:0' + str(args.width) + 'x}'
        ref = "&#x" + theFm.format(n) + ";"
    return ref


###############################################################################
# Called only for chars <= 32
# (could actually be called for everything, so we can catch \\, %, etc.)
#
def mapControlChar(charNum, what=""):
    if (args.spaceUnchanged and chr(charNum).isspace()):
        return chr(charNum)
    if (charNum == 32):
        if (args.spaceAs == "SELF"): return(" ")
        elif (args.spaceAs == "B"): return(unichr(0x2422))
        elif (args.spaceAs == "U"): return(unichr(0x2423))
        elif (args.spaceAs == "SP"): return(unichr(0x2420))
        else: assert False, "Unsupported spaceAs value '%s'" % (args.spaceAs)
    if (charNum == 10):
        if (args.lfAs == "SELF"): return("\n")
        if (args.lfAs == "LF"): return(unichr(0x240A))
        if (args.lfAs == "NL"): return(unichr(0x2424))
        else: assert False, "Unsupported lfAs value '%s'" % (args.lfAs)

    if (args.pics):
        return chr(0x2400 + charNum)
    if (what=="ENTITY16"):
        return unichr(0x2400 + charNum)
    if (args.name):
        if (charNum > len(names)):
            warn("Control U+%04x out of range for names -- check code." % (charNum))
        return "*%s*" % (names[charNum])
    if (args.backSlashes and backslashCodes[charNum]):
        return backslashCodes[charNum]
    if (args.uri):
        return "%02x" % (charNum)
    return strfchr.strfchr(charNum, what)


###############################################################################
#
def doOneFile(path, fh):
    nControls = nHigh = 0
    colorState = 0

    rec = fh.readline()
    while (rec):
        for i in (range(0, len(rec))):
            c = rec[i]
            o = ord(c)
            toprint = ""
            if (o < 32):
                nControls += 1
                toprint = mapControlChar(o)
            elif (o > 127):
                nHigh += 1
                toprint = makeCharRef(o)

            if (toprint):
                if (not colorState):
                    print(cs, end='')
                    colorState = 1
                print(toprint, end="")
            else:
                if (colorState):
                    print(ce, end="")
                    colorState = 0
                print(c, end="")
        if (colorState):
            print(ce, end="")
            colorState = 0
        print("")
        rec = fh.readline()

    if (not args.quiet): return
    warn("File '%s': Control characters: %d, chars > 127: %d." %
        (path, nControls, nHigh))


###############################################################################
# Main
#
oformatChoices = strfchr.__mnemonicMap__.keys()

def processOptions():
    parser = argparse.ArgumentParser(description=descr)

    # TODO: Combine these options into --oformat [x]
    parser.add_argument(
        "--backSlashes", action='store_true', default=True,
        help='Use \\ hex-codes to display characters.')
    parser.add_argument(
        "--name", action='store_true',
        help='Show names for control chars, instead of entities or symbols.')
    parser.add_argument(
        "--pics", "--pix", action='store_true', default=True,
        help='Use Unicode control pictures (U+2400...) for control chars.')
    parser.add_argument(
        "--uri", action='store_true',
        help='Show URI-style (%XX) escapes for invisible characters.')

    parser.add_argument(
        "--base", type=int, default=10, choices=[ 10, 16 ],
        help='Use base 10 or 16 for XML character references.')
    parser.add_argument(
        "--color", action='store_true',
        help='Colorize the formerely-invisible characters.')
    parser.add_argument(
        "--nocolor", action='store_false', dest="color",
        help='Turn off colorizing.')
    parser.add_argument(
        "--iencoding", type=str, metavar="E", default="utf-8",
        help="Assume this character coding for input. Default: utf-8.")
    parser.add_argument(
        "--lfAs", type=str, default="LF", choices=lfChoices,
        help='Whether to show Line Feeds as SELF, LF: LF, or NL: NL symbol.')
    parser.add_argument(
        "--oformat", type=str, default="ENTITY16", choices=oformatChoices,
        help="How to write out invisible characters.")
    parser.add_argument(
        "--quiet", "-q", action='store_true',
        help='Suppress most messages.')
    parser.add_argument(
        "-spaceUnchanged", action='store_true',
        help='Leave whitespace as-is.')
    parser.add_argument(
        "--spaceAs", type=str, default="SELF", choices = spaceChoices,
        help='Show spaces as: SELF, B: slashed b, U: serifed _, or SP: SP symbol.')
    parser.add_argument(
        "--verbose", "-v", action='count', default=0,
        help='Show more messages (repeatable).')
    parser.add_argument(
        "--version", action='version', version=__version__,
        help='Display version information, then exit.')
    parser.add_argument(
        "--width", "--pad", type=int, default=4,
        help='How many digits (minimum) for XML numeric character references.')

    parser.add_argument(
        'files', nargs=argparse.REMAINDER,
        help='Path(s) to input file(s).')

    args0 = parser.parse_args()
    if (args0.verbose): print(args)
    return args0


args = processOptions()

su = sjdUtils()
cs = ""
ce = ""
if (args.color):
    cs = su.getColorString("red")
    ce = su.getColorString("off")
    if (args.verbose):
        print("Turned on " + cs + "color" + ce + ".")

if (not args.files):
    if (sys.stdin.isatty()):
        sys.stderr.write("Waiting on STDIN...\n")
    doOneFile("[stdin]", sys.stdin)
    sys.exit()

for path0 in args.files:
    if (not os.path.isfile(path0)):
        warn("Can't find file '%s'." % (path0))
    else:
        with codecs.open(path0, "rb", encoding=args.iencoding) as fh0:
            doOneFile(path0, fh0)
