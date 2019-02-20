#!/usr/bin/env python
#
# showCharsInPythonClass
#
# 2015-03-31: Written. Copyright by Steven J. DeRose.
# Creative Commons Attribution-Share-alike 3.0 unported license.
# See http://creativecommons.org/licenses/by-sa/3.0/.
# 2018-11-07: Cleanup, Py 3.
#
# To do:
#     Find all chars matching some regex.
#
from __future__ import print_function
import sys, os, argparse
import regex as re
import codecs
import unicodedata

from sjdUtils import sjdUtils
from alogging import ALogger
from MarkupHelpFormatter import MarkupHelpFormatter

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
    string_types = basestring
else:
    string_types = str
    def unichr(n): return chr(n)
    def unicode(s, encoding='utf-8', errors='strict'): str(s, encoding, errors)

__version__ = "2018-11-07"

oChoices = [ "chart", "xsv", "bycode", "byname", "bracket" ]

###############################################################################
# http://www.fileformat.info/info/unicode/category/index.htm
#
uclasses = {
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
descr = """
=head1 Description

Displays all Unicode characters in a given numeric range, that are in a given
Unicode character class.

Use I<--showClasses> to get a list of the class mnemonics.

=head2 Output formats available

For example, for various values of [F] and [Category] in:
    showUnicodeCharsInClass.py --format [F] [Category]

=over

=item * B<chart>

Category I<Po>:

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

=item * B<xsv>

Category I<Cf>:

    <Rec Hex='00ad' Cat='Cf' Name='SOFT HYPHEN' />
    <Rec Hex='0600' Cat='Cf' Name='ARABIC NUMBER SIGN' />
    <Rec Hex='070f' Cat='Cf' Name='SYRIAC ABBREVIATION MARK' />
    <Rec Hex='200b' Cat='Cf' Name='ZERO WIDTH SPACE' />

=item * B<bycode>

    \\xad        : 'SOFT HYPHEN',
    \\u0600      : 'ARABIC NUMBER SIGN',
    \\u070f      : 'SYRIAC ABBREVIATION MARK',
    \\u200b      : 'ZERO WIDTH SPACE',

=item * B<byname>

    "SOFT HYPHEN"                           : \\xad,
    "ARABIC NUMBER SIGN"                    : \\u0600,
    "SYRIAC ABBREVIATION MARK"              : \\u070f,
    "ZERO WIDTH SPACE"                      : \\u200b,

=item * B<bracket> -- usable in a regex:

    [\\xad\\u0600-\\u0603\\u06dd\\u070f\\u17b4-\\u17b5\\u200b-\\u200f\\u202a-\\u202e\\u2060-\\u2064\\u206a-\\u206f\\ufeff\\ufff9-\\ufffb]

Ranges of contiguous characters are combined via "-". Characters are encoded
using the smallest hex escape they can.


=head1 Related Commands


=head1 Known bugs and Limitations

Cannot seem to get regex-matching on classes to work, with either
F<re> or F<regex>.

Should "-" or "^" be the first member of a class, I<--format brakcet>
would get confused.

Long lines with <--format bracket> are not wrapped.


=head1 Licensing

Copyright 2015 by Steven J. DeRose. This script is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See http://creativecommons.org/licenses/by-sa/3.0/ for more information.

=head1 Options
        """

def processOptions():
    "Parse command-line options and arguments."
    try:
        from MarkupHelpFormatter import MarkupHelpFormatter
        formatter = MarkupHelpFormatter
    except ImportError:
        formatter = None
    parser = argparse.ArgumentParser(
        description=descr, formatter_class=formatter)

    parser.add_argument(
        "--color",  # Don't default. See below.
        help='Colorize the output.')
    parser.add_argument(
        '--find',             type=str,
        help='Retrieve characters whose formal names match this regex.')
    parser.add_argument(
        '--first',            type=any_int, default=32,
        help='First code point to check.')
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
        "--showClasses",      action='store_true',
        help='Display the 2-letter codes and their meanings.')
    parser.add_argument(
        "--verbose", "-v",    action='count',       default=0,
        help='Add more messages (repeatable).')
    parser.add_argument(
        "--version",          action='version',     version='Version of '+__version__,
        help='Display version information, then exit.')

    parser.add_argument(
        'charClass',          type=str,
        help='2-letter abbreviation for character class to display.')

    args0 = parser.parse_args()
    su = sjdUtils()
    su.setVerbose(args.verbose)
    if (args0.color is None):
        args0.color = ("USE_COLOR" in os.environ and sys.stderr.isatty())
    su.setColors(args0.color)
    return(args0)


def makeEsc(n, literals=False, qlits=True):
    """Make the smallest hex-escape for the character. If requested, use
    literal characters for ASCII which are not regex metacharacters.
    In that case, --bracket should not quote those characters, others should.
    """
    c = unichr(n)
    if (literals):
        if (c in "\\()[]{}'\"-^"): return("\\x%02x" % (n))
        if (n>32 and n<127):       return(c)
    if (n<256):                    return("\\x%02x" % (n))
    if (n<65536):                  return("\\u%04x" % (n))
    return("\\U%08x" % (n))


###############################################################################
###############################################################################
# Main
#
args = processOptions()

if (args.showClasses):
    print("Unicode character class mnemonics:")
    chclasses = sorted(uclasses.keys())
    for chcl in chclasses:
        print("    %2s: %s" % (chcl, uclasses[chcl]))
    sys.exit()

cc = unicode(args.charClass[0])
if (len(cc)>2):
    sys.stderr.write("Class mnemonic too long.\n")
    sys.exit()

ex = r'\d'                      # yes
ex = r'[\p{Letter}]'            # no
ex = r'[[:Digit:]]'             # no
ex = r'\p{Ll}'                  # no

cex = re.compile(ex, re.U)

brack = u'['
n = 0
lastOne = -99
inARange = False
for codePoint in range(args.first, args.last+1):
    c = unicode(unichr(codePoint))
    flag = 0
    try:
        nm = unicodedata.name(c)
    except ValueError as e:
        continue

    gotOne = False
    if (args.find):
        if (re.search(args.find, nm, re.I)): gotOne = True
    else:
        if (unicodedata.category(c).startswith(cc)):
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
                brack += makeEsc(codePoint, qlits=False)
        else:
            if (codePoint == lastOne+1):
                pass
            else:
                brack += makeEsc(lastOne) + makeEsc(codePoint, qlits=False)
                inARange = False
    else:
        print("--format fail")
        sys.exit()
    lastOne = codePoint

if (args.format == "bracket"):
    if (inARange): brack += makeEsc(lastOne, qlits=False)
    brack += u']'
    if (args.metaregex):
        lhs = "\\\\p\\{" + cc + "\\}"
        brack = "R = re.sub(r'%s', '%s', R)" % (lhs, brack)
    print(brack)

if (not args.quiet):
    qual = "in class " + cc
    if (args.find): qual = "matching /%s/" % (args.find)
    sys.stderr.write("Done, %d of %d characters (u+%04x:u+%04x) %s.\n" %
        (n, args.last-args.first+1, args.first, args.last+1, qual))
if (args.verbose): su.showStats();
