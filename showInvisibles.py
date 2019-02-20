#!/usr/bin/env python
#
# showInvisibles: make control and whitespace chars visible.
#
# 2007-01-16: Written by Steven J. DeRose.
# 2007-12-31 sjd: Getopt, version, etc.
# 2010-09-27 sjd: Cleanup, -base, -pad, -color, factor out makeCharRef().
# 2011-01-24 sjd: Add control pictures and alternates. binmode STDOUT.
# 2012-01-23 sjd: Fix -color and -base. Use sjdUtils.
# Optimize color-escaping instead of doing on/off for every char.
# 2012-01-23: Converted by perl2python.
# 2012-01-25 sjd: Cleanup.
# 2015-10-13: Update argparse usage. pylint.
#
# To do:
#     Options for what to do with line-ends?
#     Compare to showInvisibles (no .py), and probably discard as obsolete.
#
from __future__ import print_function
import sys
import os
import re
import argparse
#import subprocess
#import string
#import math
#import codecs, locale

from sjdUtils import sjdUtils
from alogging import ALogger

__version__ = "2015-10-13"

global args
args = None
#lg = ALogger(1)


###############################################################################
# Process options
#
def processOptions():
    parser = argparse.ArgumentParser(description="""
=pod

=head1 Description

showinvisible [options]

Make control characters and space visible by substituting the Unicode
"control symbols" for them.
Also make non-ASCII characters visible by substituting XML numeric
character references (I<&#2022;> etc).
Can also colorize the changed characters.

Useful for visualizing return/linefeed, space/tab, etc. Can also be used
to escape undesired characters in a file to ease later processing (in that
case, specify I<--nocolor -s>).

(Python version; also available in Perl)

=head1 Known bugs and limitations

Options I<-b> and I<-u> are unfinished.


=head1 Ownership

This work by Steven J. DeRose is licensed under a Creative Commons
Attribution-Share Alike 3.0 Unported License. For further information on
this license, see L<http://creativecommons.org/licenses/by-sa/3.0/>.

For the most recent version, see L<http://www.derose.net/steve/utilities/>.

=head1 Options

=cut
""")
    parser.add_argument(
        "--backSlashes",      action='store_true',  default=True,
        help='Use \\ hex-codes to display characters.')
    parser.add_argument(
        "--base",             type=int,             default=10,
        help='Use base 10 or 16 for XML character references.')
    parser.add_argument(
        "--color",            action='store_true',
        help='Colorize the formerely-invisible characters.')
    parser.add_argument(
        "--nocolor",          action='store_false', dest="color",
        help='Turn off colorizing.')
    parser.add_argument(
        "--lfAs",             type=str,             default="LF",
        help='Whether to show Line Feeds as LF: LF, or NL: NL symbol.')
    parser.add_argument(
        "--name",             action='store_true',
        help='Show names for control chars, instead of entities or symbols.')
    parser.add_argument(
        "--pad",              type=int,             default=4,
        help='How many digits (minimum) for XML numeric character references.')
    parser.add_argument(
        "--pics",             action='store_true',  default=True,
        help='Use Unicode control pictures u\'2400... for control chars.')
    parser.add_argument(
        "--pix",              action='store_true',
        help='Synonym for -pics.')
    parser.add_argument(
        "--quiet", "-q",      action='store_true',
        help='Suppress most messages.')
    parser.add_argument(
        "-s",                 action='store_true',  dest='leaveSpaces',
        help='Leave regular spaces (u\'0020) as-is.')
    parser.add_argument(
        "--spaceAs",          type=str,
        help='Show spaces as: B: slashed b, U: serifed _, or SP: SP symbol.')
    parser.add_argument(
        "--uri",              action='store_true',
        help='Show URI-style (%XX) escapes for invisible characters.')
    parser.add_argument(
        "--verbose", "-v",    action='count',       default=0,
        help='Show more messages (repeatable).')
    parser.add_argument(
        "--version", action='version', version=__version__,
        help='Display version information, then exit.')
    parser.add_argument(
        'files',              nargs=argparse.REMAINDER,
        help='Path(s) to input file(s).')

    args0 = parser.parse_args()
    if (args0.verbose): print(args)

    # Check arg values
    #
    if (not (args0.base==10 or args0.base==16)):
        print("Can only do --base 10 or 16.")

    args0.spaceAs = args0.spaceAs.upper()
    if (not re.match(r'(B|U|SP)$', args0.spaceAs)):
        print("--spaceAs must be B, U, or SP.")

    args0.lfAs = args0.lfAs.upper()
    if (not re.match(r'(LF|NL)$', args0.lfAs)):
        print("--lfAs must be LF or NL.")
    return(args0)


###############################################################################
#
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
    "\\s"]
if (backslashCodes[32] != "\\s"):
    print("backslashCodes messed up.")
    exit(0)

if (os.environ["PYTHONIOENCODING"] != "utf_8"):
    print("PYTHONIOENCODING is not utf_8.")
    exit(0)


###############################################################################
###############################################################################
# Construct an XML numeric character reference to the given code point.
# Use the appropriate args.base.
#
def makeCharRef(n):
    if (args.base == 10):
        theFm = '{0:0' + str(args.pad) + 'd}'
        ref = "&#" + theFm.format(n) + ";"
    else:
        theFm = '{0:0' + str(args.pad) + 'x}'
        ref = "&#x" + theFm.format(n) + ";"
    return(ref)


###############################################################################
# Symbols are available for control chars and space: decimal 00-32.
#
def getControlPic(charNum):
    if (charNum == 32):
        if (args.spaceAs == "B"):   return(unichr(0x2422))
        elif (args.spaceAs == "U"): return(unichr(0x2423))
        return(unichr(0x2420))
    if (charNum == 10):
        if (args.lfAs == "LF"):     return(unichr(0x240A))
        return(unichr(0x2424))
    return(unichr(0x2400 + charNum))


###############################################################################
# Called only for chars <= 32
# (could actually be called for everything, so we can catch \\, %, etc.)
#
def getNameForControl(n):
    rc = ""
    if (args.name):
        if (n > len(names)):
            lg.warning("Control #" + n + " out of range for names -- check code.")
        rc = "*" + names[n] + "*"
    elif (args.backSlashes):
        if (backslashCodes[n]):
            rc = backslashCodes[n]
        else:
            rc = makeCharRef(n)
    elif (args.uri):
        rc = "%02x" % (n)
    else:
        rc = makeCharRef(n)
    return rc



###############################################################################
###############################################################################
# Main
#
args = processOptions()

if (not sys.argv[0]):
    fh = sys.stdin
elif (os.path.isfile(sys.argv[0])):
    fh = open(sys.argv[0], "r")
else:
    lg.warning("Can't find file.")
    sys.exit(0)


su = sjdUtils()
cs = ""
ce = ""
if (args.color):
    cs = su.getColorString("red")
    ce = su.getColorString("off")
    if (args.verbose):
        print("Turned on " + cs + "color" + ce + ".")

#print("lengths: " + str(len(cs)) + ", " + str(len(ce)))
#print("test color: " + cs + "hello" + ce + " ok?")

# Do the real work
#
nControls = nHigh = 0
colorState = 0

rec = fh.readline()
while (rec):
    for i in (range(0,len(rec))):
        c = rec[i]
        o = ord(c)
        toprint = ""
        if (o < 32 or (o == 32 and not args.leaveSpaces)):
            nControls += 1
            if (args.pics): toprint = getControlPic(o)
            else: toprint = getNameForControl(o)
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

if (not args.quiet):
    lg.warning("Done. Control characters: %d, chars > 127: %d." %
        (nControls, nHigh))

sys.exit(0)
