#!/usr/bin/env python
#
# showCharsInPythonClass
#
from __future__ import print_function
import sys, argparse
#import re
import regex as re
import unicodedata

PY3 = sys.version_info[0] == 3
if PY3:
    def unichr(nn): return chr(nn)
    #def unicode(s, encoding='utf-8', errors='strict'): return str(s, encoding, errors)

__metadata__ = {
    'title'        : "showUnicodeCharsInClass.py",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 2.7.6, 3.6",
    'created'      : "2015-03-31",
    'modified'     : "2020-02-14",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr = """
=Description=

Display all Unicode characters in a given numeric range, that are in a given
Unicode character category.

Use ''--showCategories'' to get a list of the category mnemonics.

=Output formats available=

For example, for various values of [F] and [Category] in:
    showUnicodeCharsInClass.py --format [F] [Category]

==chart==

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

==xsv==

Category ''Cf'':

    <Rec Hex='00ad' Cat='Cf' Name='SOFT HYPHEN' />
    <Rec Hex='0600' Cat='Cf' Name='ARABIC NUMBER SIGN' />
    <Rec Hex='070f' Cat='Cf' Name='SYRIAC ABBREVIATION MARK' />
    <Rec Hex='200b' Cat='Cf' Name='ZERO WIDTH SPACE' />

==bycode==

    \\xad        : 'SOFT HYPHEN',
    \\u0600      : 'ARABIC NUMBER SIGN',
    \\u070f      : 'SYRIAC ABBREVIATION MARK',
    \\u200b      : 'ZERO WIDTH SPACE',

==byname==

    "SOFT HYPHEN"                           : \\xad,
    "ARABIC NUMBER SIGN"                    : \\u0600,
    "SYRIAC ABBREVIATION MARK"              : \\u070f,
    "ZERO WIDTH SPACE"                      : \\u200b,

==bracket==

This generates the list in a form that can be put into a regular expression as
a [...] group:
    [\\xad\\u0600-\\u0603\\u06dd\\u070f\\u17b4-\\u17b5\\u200b-\\u200f\\u202a-\\u202e\\u2060-\\u2064\\u206a-\\u206f\\ufeff\\ufff9-\\ufffb]

Ranges of contiguous characters are combined via "-". Characters are encoded
using the smallest hex escape they can (probably should add a `--width` option).

=Related Commands=

`ord`, `mathAlphanumerics`, `countChars`,
`makeCharChart.py`, `getCharsByScript`.

=Known bugs and Limitations=

Should offer same display layouts as `ord`.

Should "-" or "^" be the first member of a category, I<--format brakcet>
would get confused.

Long lines with <--format bracket> are not wrapped.

Should have a way to find all chars matching some regex (but see `ord`).

=History=

* 2015-03-31: Written. Copyright by Steven J. DeRose.

* 2018-11-07: Cleanup, move to Python 3.

* 2020-02-14: New layout. Lint.

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
    "Cc":  "Other, Control",
    "Cf":  "Other, Format",
    "Cn":  "Other, Not Assigned (no characters in the file have this property)",
    "Co":  "Other, Private Use",
    "Cs":  "Other, Surrogate",
    "LC":  "Letter, Cased",
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
        '--find',             type=str,
        help='Retrieve characters whose formal names match this regex.')
    parser.add_argument(
        '--first',            type=any_int, default=32,
        help='First code point to check.')

    oChoices = [ "chart", "xsv", "bycode", "byname", "bracket" ]
    parser.add_argument(
        '--format',            type=str, default="chart",
        choices=oChoices,
        help='How to arrange the output. Choices: ' + str(oChoices))
    parser.add_argument(
        '--last',             type=any_int, default=65535,
        help='Last code point to check.')
    parser.add_argument(
        "--metaregex",        action='store_true',
        help='With --bracket, make a regex to expand \\p{xx} to a []-group.')
    parser.add_argument(
        "--quiet", "-q",      action='store_true',
        help='Suppress most messages.')
    parser.add_argument(
        "--showCategories",      action='store_true',
        help='Display the 2-letter codes and their meanings.')
    parser.add_argument(
        "--verbose", "-v",    action='count',       default=0,
        help='Add more messages (repeatable).')
    parser.add_argument(
        "--version",          action='version',     version='Version of '+__version__,
        help='Display version information, then exit.')

    parser.add_argument(
        'charCategory',          type=str, default="", nargs='?',
        help='2-letter abbreviation for character category to display.')

    args0 = parser.parse_args()
    return(args0)


def makeEsc(nn, literals=False):
    """Make the smallest hex-escape for the character. If requested, use
    literal characters for ASCII which are not regex metacharacters.
    In that case, --bracket should not quote those characters, others should.

    @param nn: The code point
    @param literals: If True, leave most ASCII G0 characters as themselves.
    """
    ch = unichr(nn)
    if (literals):
        if (ch in "\\()[]{}'\"-^"): return("\\x%02x" % (nn))
        if (nn>32 and nn<127):      return(ch)
    if (nn<256):                    return("\\x%02x" % (nn))
    if (nn<65536):                  return("\\u%04x" % (nn))
    return("\\U%08x" % (nn))


###############################################################################
###############################################################################
# Main
#
args = processOptions()

if (args.showCategories):
    print("Unicode character category mnemonics:")
    chCategories = sorted(unicodeCategories.keys())
    for chc in chCategories:
        print("    %2s: %s" % (chc, unicodeCategories[chc]))
    sys.exit()

if (args.charCategory not in unicodeCategories):
    sys.stderr.write("Unknown cateogory mnemonic '%s'." % (args.charCategory))
    sys.exit()

ccat = args.charCategory

#ex = r'\d'                      # yes
ex = r'[\p{Letter}]'            # no
#ex = r'[[:Digit:]]'             # no
#ex = r'\p{Ll}'                  # no

cex = re.compile(ex, re.U)

brack = u'['
n = 0
lastOne = -99
inARange = False
for codePoint in range(args.first, args.last+1):
    c = unichr(codePoint)
    flag = 0
    try:
        nm = unicodedata.name(c)
    except ValueError as e:
        continue

    gotOne = False
    if (args.find):
        if (re.search(args.find, nm, re.I)): gotOne = True
    else:
        if (unicodedata.category(c).startswith(ccat)):
            gotOne = True

    if (not gotOne): continue

    n += 1
    if (args.format == "chart"):
        print("    U+%04x '%s' (%-2s) (%d) %s" %
            (codePoint, c, unicodedata.category(c), int(bool(flag)), nm))
    elif (args.format == "xsv"):
        print("<Rec Hex='%04x' Cat='%s' Name='%s' />" %
            (codePoint, unicodedata.category(c), nm))
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

if (args.format == "bracket"):
    if (inARange): brack += makeEsc(lastOne, literals=False)
    brack += u']'
    if (args.metaregex):
        lhs = "\\\\p\\{" + ccat + "\\}"
        brack = "R = re.sub(r'%s', '%s', R)" % (lhs, brack)
    print(brack)

if (not args.quiet):
    sys.stderr.write("Done. %d of %d characters [u+%04x:u+%04x]\n" %
        (n, args.last-args.first+1, args.first, args.last+1))
    qual = "    in category %s (%s)" % (ccat, unicodeCategories[ccat])
    if (args.find): qual = "    matching /%s/" % (args.find)
    print(qual)
