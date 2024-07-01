#!/usr/bin/env python3
#
# isASCII.py: Check character set/encoding of a file(s).
# 2020-11-18: Written by Steven J. DeRose.
#
import sys
import codecs
import re
from collections import defaultdict
from unicodedata import normalize
from PowerWalk import PowerWalk, PWType

PY3 = sys.version_info[0] == 3
if (PY3):
    #from io import StringIO
    def unicode(s, encoding="utf-8", errors="strict"): str(s, encoding, errors)
    if (sys.version_info[1] < 7):
        def isascii(s):
            if (re.match(r"^[\x01-\x7F]+$", s)): return True
            return False
    else:
        def isascii(s):
            return s.isascii()

# See if this Python build can handle Unicode > 0xFFFF.
#
wideBuild = True
try:
    ord(chr(0x10FFFF))
except ValueError:
    wideBuild = False

__metadata__ = {
    "title"        : "isASCII",
    "description"  : "Check character set/encoding of a file(s).",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.7",
    "created"      : "2020-11-18",
    "modified"     : "2021-04-09",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]


descr = """
=Description=

Test whether the file includes only ASCII characters (see the `--charset`
option to test for other character sets).

==Usage==

    isASCII.py [options] [files]

With `--charset [x], can verify for other sets of acceptable characters:
'ascii', 'lower', 'upper', 'alpha', 'alnum', 'latin1', 'latin-1', 'xmlchars'.

The script can report (for each file):

* The location and code point of every undesired character (turn off with `-q`).
* Total number of occurrences of each undesired character (turn on with `--counts`).
* "ASCII" or "non-ASCII", following by ": " and the path (turn off with `--no-flag`).

`--normalize` can be used to convert to any of the Unicode normal forms before
checking the individual characters. However, after doing so column numbers apply to
the normalized form, which will sometimes not be the same as the original.

Remember that a file's ''encoding'' is not the same as the ''character set''
used. For example, a UTF-8 or UCS-2 encoded file, might happen
to only contain characters that are included in ASCII or Latin-1.


=Related Commands=

My `XMLRegexes.py` provides XML character-set checking code.

My `countChars` generates an atlas of what characters occur in a given file(s),
with frequencies, organized by plane, block, script, ....

My `ord`, `CharDisplay.py`, and `strfchr.py` provide information on Unicode characters.


=Known bugs and Limitations=

The Unicode Byte-Order Mark (aka U+0FEFF, aka `ZERO WIDTH NO-BREAK SPACE`),
is not in most `--charsets` is reported, which you may or may not want.


=History=

* 2020-11-18: Written by Steven J. DeRose.
* 2021-04-08f: Fix driver bug. Add counting, -q message, --counts, --noflag.


=To do=

* Add support for doing a Unicode compatibility (de)composition first, so users
can determine how bad a loss they'll take if they force to ASCII.

* Do curly quotes get compatibility-mapped to straight quotes?


=Rights=

Copyright 2020-11-18 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/ for more information].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
#
def warning(msg):
    sys.stderr.write(msg + "\n")


###############################################################################
# See https://github.com/sderose/XML.git/PARSERS/blob/master/XMLRegexes.py
#
def UEscape(codePoint):
    if (codePoint > 0xFFFF):
        return "\\U" + ("%08x" % (codePoint))
    return "\\u" + ("%04x" % (codePoint))

def UEscapeFunction(mat):
    return UEscape(ord(mat.group(1)))

_THE_END_ = 0xFFFC   # Python re seems to die on U+FFFD

xmlCharRanges = [
    (0x00009, 0x00009),
    (0x0000A, 0x0000A),
    (0x0000D, 0x0000D),
    (0x00020, 0x0D7FF),
    (0xE000, _THE_END_),
]
if (wideBuild):
    xmlCharRanges.append( (0x10000, 0x10FFFF) )
xmlChars = ""
for st, en in xmlCharRanges:
    if (st==en): xmlChars += UEscape(st)
    else: xmlChars += UEscape(st) + "-" + UEscape(en)
xmlChars += r"^[%s]+$" % (xmlChars)
xmlCharsExpr = re.compile(xmlChars, re.UNICODE)


###############################################################################
#
def doOneFile(path):
    """Read and deal with one individual file.
    """
    if (not path):
        if (sys.stdin.isatty()): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            sys.stderr.write("Cannot open '%s':\n    %s" % (e))
            return 0
        if (not args.quiet): warning("Starting file '%s'." % (path))

    recnum = 0
    nBad = 0
    charCounts = defaultdict(int)
    for rec in fh.readlines():
        recnum += 1
        if (args.normalize != "NONE"):
            rec = normalize(args.normalize, rec)
        for i in range(len(rec)):
            c = rec[i]
            if (args.allow and c in args.allow):    # Exception per --allow
                continue
            if (c == "\uFEFF"):                    # Ignore BOM
                warning("Unicode BOM found at record %d, column %d." % (recnum, i))
                continue

            # Check against whatever set of ok characters user chose
            if (args.charset == "ascii"):
                if (isascii(c)): continue  # Srsly, not in Python until 3.7?
            elif (args.charset == "lower"):
                if (c.islower()): continue
            elif (args.charset == "upper"):
                if (c.isupper()): continue
            elif (args.charset == "alpha"):
                if (c.isalpha()): continue
            elif (args.charset == "alnum"):
                if (c.isalnum()): continue
            elif (args.charset == "latin1" or args.charset == "latin-1"):
                if (islatin1(c)): continue
            elif (args.charset == "xmlchars"):
                if (isxmlchars(c)): continue
            else:
                warning("Unknown --charset '%s'." % (args.charset))
                sys.exit()

            nBad += 1
            charCounts[c] += 1
            if (not args.quiet):
                print("    Record %6d, column %4d: char 0x%05x (d%06d) '%s'" %
                (recnum, i, ord(c), ord(c), c))
            if (args.max and nBad>=args.max):
                print("--max of %d reached, stopping." % (args.max))
                break

    fh.close()
    if (args.counts):
        for c in sorted(charCounts.keys()):
            print("  U+%05x (d%6d) '%s':  %6d" %
                (ord(c), ord(c), c, charCounts[c]))
    if (not args.noflag):
        print("%sASCII: %s" % ("non-" if nBad>0 else "", path))
    return(nBad, charCounts)

def islatin1(s):
    if (s==""): return False  # To be like str.isxxx()
    for c in s:
        o = ord(c)
        if (o < 1 or o > 255): return False
        if (o > 127 and o < 160): return False
    return True

def isxmlchars(s):
    if (s==""): return False  # To be like str.isxxx()
    if (re.match(xmlCharsExpr, s)): return True
    return False


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse

    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--allow", type=str,
            help="Extra characters to allow, beyond --charset.")
        parser.add_argument(
            "--charset", type=str,
            choices=[ "ascii", "lower", "upper", "alpha", "alnum",
              "latin1", "latin-1", "xmlchars" ], default="ascii",
            help="What set of characters to look for exceptions to.")
        parser.add_argument(
            "--counts", action="store_true",
            help="Show counts of bad characters (per file).")
        parser.add_argument(
            "--normalize", type=str, default="NONE",
            choices=[ "NFC", "NFD", "NFKC", "NFKD" ],
            help="Do Unicode normalization of the specified kind first.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--max", type=int, default=0,
            help="Stop each file after this many errors.")
        parser.add_argument(
            "--noflag", "--no-flag", action="store_true",
            help="Suppress the ASCII/non-ASCII line for each file.")
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

        PowerWalk.addOptionsToArgparse(parser)

        parser.add_argument(
            "files", type=str,
            nargs=argparse.REMAINDER,
            help="Path(s) to input file(s)")

        args0 = parser.parse_args()
        return(args0)


    ###########################################################################
    #
    nBadFiles = nBadChars = 0
    args = processOptions()

    if (len(args.files) == 0):
        nBad0, charCounts0 = doOneFile("")
        sys.exit()

    pw = PowerWalk(args.files, open=False, close=False,
        encoding=args.iencoding, recursive=args.recursive)
    pw.applyOptionsFromArgparse(args)
    for path0, fh0, what0 in pw.traverse():
        if (what0 != PWType.LEAF): continue
        nBad0, charCounts0 = doOneFile(path0)
        if (nBad0):
            warning("Found %d bad chars in file '%s'." % (nBad0, path0))
            nBadFiles += 1
            nBadChars += nBad0

    if (not args.quiet):
        warning("%d files checked, %d chars in %d files not in '%s'.\n" %
            (pw.getStat("regular"), nBadChars, nBadFiles, args.charset))
