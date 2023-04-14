#!/usr/bin/env python3
#
# showCharsInPythonClass: Retrieve lists of characters by category (Ll, etc).
# 2015-03-31: Written by Steven J. DeRose.
#
import sys
import argparse
import unicodedata

import regex

__metadata__ = {
    "title"        : "showUnicodeCharsInClass.py",
    "description"  : "Retrieve lists of characters by category (Ll, etc).",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 2.7.6, 3.6",
    "created"      : "2015-03-31",
    "modified"     : "2023-02-27",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Description=

[Unfinished]

Display all Unicode characters in a given numeric range (default U+0020 to U+FFFF),
that are in a given Unicode character category or categories. For example:

    showUnicodeCharsInClass.py Lt

will display all titlecase characters (Unicode category "Letter, Titlecase").

The --find [regex] option may be used as an additional filter, to discard any
characters whose full Unicode names do not match [regex].

Use ""--showCategories'' to get a list of the category mnemonics (single-letter
mnemonics may be used to catch a broader category).


=Output formats available=

The resulting list is available in several forms via --format, though always in
numeric code point order.

Examples below show the first several items displayed
for various values of --format and various categories in:

    showUnicodeCharsInClass.py --format [F] [Category]

== --format chart==

Category ''Po'':

    U+0021 '!' (Po) (0) EXCLAMATION MARK
    U+0022 '"' (Po) (0) QUOTATION MARK
    U+0023 '#' (Po) (0) NUMBER SIGN
    U+0025 '%' (Po) (0) PERCENT SIGN
    U+0026 '&' (Po) (0) AMPERSAND
    U+0027 ''' (Po) (0) APOSTROPHE
    U+0028 '(' (Ps) (0) LEFT PARENTHESIS
    U+0029 ')' (Pe) (0) RIGHT PARENTHESIS
    U+002a '*' (Po) (0) ASTERISK
    U+002c ',' (Po) (0) COMMA
    U+002d '-' (Pd) (0) HYPHEN-MINUS
    U+002e '.' (Po) (0) FULL STOP
    U+002f '/' (Po) (0) SOLIDUS
    U+003a ':' (Po) (0) COLON
    U+003b ';' (Po) (0) SEMICOLON
    U+003f '?' (Po) (0) QUESTION MARK
    U+0040 '@' (Po) (0) COMMERCIAL AT
    ...

== --format xsv==

Category ''Cf'':

    <Rec Hex='00ad' Cat='Cf' Name='SOFT HYPHEN' />
    <Rec Hex='0600' Cat='Cf' Name='ARABIC NUMBER SIGN' />
    <Rec Hex='070f' Cat='Cf' Name='SYRIAC ABBREVIATION MARK' />
    <Rec Hex='200b' Cat='Cf' Name='ZERO WIDTH SPACE' />

== --format bycode==

    \\xad        : 'SOFT HYPHEN',
    \\u0600      : 'ARABIC NUMBER SIGN',
    \\u070f      : 'SYRIAC ABBREVIATION MARK',
    \\u200b      : 'ZERO WIDTH SPACE',

== --format byname==

    "SOFT HYPHEN"                           : \\xad,
    "ARABIC NUMBER SIGN"                    : \\u0600,
    "SYRIAC ABBREVIATION MARK"              : \\u070f,
    "ZERO WIDTH SPACE"                      : \\u200b,

== --format bracket==

This generates the list in a form that can be put into a regular expression as
a [...] group:
    [\\xad\\u0600-\\u0603\\u06dd\\u070f\\u17b4-\\u17b5\\u200b-\\u200f\\u202a-\\u202e\\u2060-\\u2064\\u206a-\\u206f\\ufeff\\ufff9-\\ufffb]

Ranges of contiguous characters are combined via "-". Characters are encoded
using the smallest hex escape they can (probably should add a `--width` option).


=Related Commands=

`ord`, `mathAlphanumerics`, `countChars`,
`makeCharChart.py`, `getCharsByScript`.
`findCodePointsInClass.py' (obsolete, I forgot I wrote this...)


=Known bugs and Limitations=

Should offer same display layouts as `ord`.

Should "-" or "^" be the first member of a category, I<--format bracket>
will get confused.

Long lines with <--format bracket> are not wrapped.

Should have a way to find all chars matching some regex (but see `ord`).

You cannot currently request category 'LC' (Letter, cased). I believe it is
just shorthand for anything in Lu, Ll, or Lt, and no character is directly "in"
it. But I need to check that.

Note that by default, this searches only the BMP (specifically, U+0020 to U+FFFF).
Options allow setting a wider or narrower range.


=To do=

* Output option to call CharDisplay.py. Or just integrate this whole thing as a search
option there.


=History=

* 2015-03-31: Written by Steven J. DeRose.
* 2018-11-07: Cleanup, move to Python 3.
* 2020-02-14: New layout. Lint.
* 2021-07-24: Allow requesting multiple categories.
* 2023-02-27: Lint, testing, various fixes esp. to options, controls, unassigned chars.


=Rights=

Copyright 2015 by Steven J. DeRose. This work is licensed under a Creative Commons
Attribution-Share Alike 3.0 Unported License. For further information on
this license, see http://creativecommons.org/licenses/by-sa/3.0/.

For the most recent version, see [http://www.derose.net/steve/utilities] or
[http://github.com/sderose].


=Options=
"""


###############################################################################
# http://www.fileformat.info/info/unicode/category/index.htm
#
unicodeCategories = {
    "C":   "Other",
    "L":   "Letter",
    "M":   "Mark",
    "N":   "Number",
    "P":   "Punctuation",
    "S":   "Symbol",
    "Z":   "Separator",

    "Cc":  "Other, Control",
    "Cf":  "Other, Format",
    "Cn":  "Other, Not Assigned",
    "Co":  "Other, Private Use",
    "Cs":  "Other, Surrogate",
    "LC":  "Letter, Cased",  # sic -- two caps!
    "Ll":  "Letter, Lowercase",
    "Lm":  "Letter, Modifier",
    "Lo":  "Letter, Other",
    "Lt":  "Letter, Titlecase",
    "Lu":  "Letter, Uppercase",
    "Mc":  "Mark, Spacing Combining",
    "Me":  "Mark, Enclosing",
    "Mn":  "Mark, Nonspacing",
    "Nd":  "Number, Decimal Digit",
    "Nl":  "Number, Letter",
    "No":  "Number, Other",
    "Pc":  "Punctuation, Connector",
    "Pd":  "Punctuation, Dash",
    "Pe":  "Punctuation, Close",
    "Pf":  "Punctuation, Final quote (may behave like Ps or Pe depending on usage)",
    "Pi":  "Punctuation, Initial quote (may behave like Ps or Pe depending on usage)",
    "Po":  "Punctuation, Other",
    "Ps":  "Punctuation, Open",
    "Sc":  "Symbol, Currency",
    "Sk":  "Symbol, Modifier",
    "Sm":  "Symbol, Math",
    "So":  "Symbol, Other",
    "Zl":  "Separator, Line",
    "Zp":  "Separator, Paragraph",
    "Zs":  "Separator, Space",
}

def any_int(x):
    return int(x,0)


###############################################################################
#
def processOptions():
    try:
        from BlockFormatter import BlockFormatter
        parser = argparse.ArgumentParser(
            description=descr, formatter_class=BlockFormatter)
    except ImportError:
        parser = argparse.ArgumentParser(description=descr)

    parser.add_argument(
        "--find", type=str, default="",
        help="Retrieve characters whose formal names match this regex.")
    parser.add_argument(
        "--first", "--min", type=any_int, default=0x0020,
        help="First code point to check.")

    oChoices = [ "chart", "xsv", "bycode", "byname", "bracket" ]
    parser.add_argument(
        "--format", type=str, default="chart", choices=oChoices,
        help="How to arrange the output. Choices: " + str(oChoices))
    parser.add_argument(
        "--last", "--max", type=any_int, default=0xFFFF,
        help="Last code point to check.")
    parser.add_argument(
        "--metaregex", action="store_true",
        help="With --bracket, make a regex to expand \\p{xx} to a []-group.")
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="Suppress most messages.")
    parser.add_argument(
        "--showCategories", action="store_true",
        help="Display the 2-letter codes and their meanings.")
    parser.add_argument(
        "--verbose", "-v", action="count", default=0,
        help="Add more messages (repeatable).")
    parser.add_argument(
        "--version", action="version", version="Version of "+__version__,
        help="Display version information, then exit.")

    parser.add_argument(
        "charCategories", type=str, default="", nargs=argparse.REMAINDER,
        help="1- or 2-letter abbreviation(s) for character category(s) to display.")

    args0 = parser.parse_args()
    return(args0)

def makeEsc(nn, literals=False):
    """Make the smallest hex-escape for the character. If requested, use
    literal characters for ASCII which are not regex metacharacters.
    In that case, --bracket should not quote those characters, others should.

    @param nn: The code point
    @param literals: If True, leave most ASCII G0 characters as themselves.
    """
    ch = chr(nn)
    if (literals):
        if (ch in "\\()[]{}'\"-^"): return("\\x%02x" % (nn))
        if (nn>32 and nn<127): return(ch)
    if (nn<256): return("\\x%02x" % (nn))
    if (nn<65536): return("\\u%04x" % (nn))
    return("\\U%08x" % (nn))

def inAnyRequestedCategory(uchar:str):
    """Check whether the given character is in any of the categories (1- or 2-letter)
    requested by the user.
    """
    thisCat = unicodedata.category(uchar)
    warn(1, "U+%04x '%s' is category '%s'." % (ord(uchar), uchar, thisCat))
    for cc in args.charCategories:
        if thisCat.startswith(cc): return True
    return False


###############################################################################
# Main
#
def warn(level:int, msg:str):
    if (args.verbose >= level): sys.stderr.write(msg + "\n")

args = processOptions()

if (args.find): args.find = "(?i)" + args.find  # No regex.IGNORECASE

if (args.showCategories):
    print("Unicode character category mnemonics:")
    chCategories = sorted(unicodeCategories.keys())
    for chc in chCategories:
        print("    %2s: %s" % (chc, unicodeCategories[chc]))
    sys.exit()

if (not args.charCategories):
    warn(0, "No category mnemonic(s) requested. Use --showCategories for a list.\n")
    sys.exit()

for ccat in args.charCategories:
    if (ccat == "LC"):
        warn(0, "Category 'LC' is for Ll | Lu | Lt; no character is 'LC' per se.")
        sys.exit()
    if (ccat in unicodeCategories): continue
    warn(0, "Unknown cateogory mnemonic '%s'." % (ccat))
    sys.exit()

#ex = r"\d"                      # yes
ex = r"[\p{Letter}]"            # no
#ex = r"[[:Digit:]]"             # no
#ex = r"\p{Ll}"                  # no

cex = regex.compile(ex)  # (inherently UNICODE)

if (args.format == "chart"):
    print("    codept lit cat  Unicode name")

brack = "["
nFound = 0
lastOne = -99
inARange = False

warn(1, "Scanning code points from U+%04x to U+%04x..." % (args.first, args.last))
nTried = 0
nUnnamed = 0
nNotInCat = 0
nNoMatch = 0

for codePoint in range(args.first, args.last+1):
    nTried += 1
    c = chr(codePoint)

    # Control, private use, unassigned characters have no names available.
    try:
        nm = unicodedata.name(c)
    except ValueError:
        nUnnamed += 1
        if (not args.quiet):
            warn(2, "Code point U+%04x has no unicodedata.name." % (codePoint))
        nm = "[???]"

    if (not inAnyRequestedCategory(c)):
        nNotInCat += 1
        continue

    if (args.find and not regex.search(args.find, nm)):
        nNoMatch += 1
        continue

    theCat = unicodedata.category(c)
    if (theCat == "Cn"): continue

    nFound += 1

    if (args.format == "chart"):  # the default
        try:
            print("    U+%04x '%s' (%-2s) %s" % (codePoint, c, theCat, nm))
        except UnicodeEncodeError:
            print("    U+%04x [???]] (%-2s) %s" % (codePoint, theCat, nm))
    elif (args.format == "xsv"):
        print("<Rec Hex='%04x' Cat='%s' Name='%s' />" %
            (codePoint, theCat, nm))
    elif (args.format == "bycode"):
        print("    %-12s: '%s'," % (makeEsc(codePoint), nm))
    elif (args.format == "byname"):
        print("    %-40s: %s," % ('"'+nm+'"', makeEsc(codePoint)))
    elif (args.format == "bracket"):
        if (not inARange):
            if (codePoint == lastOne+1):
                inARange = True
                brack += "-"
            else:
                brack += makeEsc(codePoint, literals=False)
        else:
            if (codePoint == lastOne+1):
                pass
            else:
                brack += makeEsc(lastOne,
                    literals=False) + makeEsc(codePoint, literals=False)
                inARange = False
    else:
        print("--format fail")
        sys.exit()
    lastOne = codePoint

if (not args.quiet):
    warn(0, "Done. %d of %d characters [U+%04x:U+%04x] in categories:\n" %
        (nFound, args.last-args.first+1, args.first, args.last+1))
    qual = ""
    for ccat in args.charCategories:
        qual += "    %-2s (%s)\n" % (ccat, unicodeCategories[ccat])
    if (args.find):
        qual = "    matching /%s/\n" % (args.find)
    print(qual, end="")
    print("Totals:  Tried %d, unnamed %d, not in category %d, in but not matched %d." %
        (nTried, nUnnamed, nNotInCat, nNoMatch))
