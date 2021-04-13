#!/usr/bin/env python
#
# strfchr.py: Flexible conversion between character representations.
# 2021-04-08: Written by Steven J. DeRose
#
import sys
import re
#import string
import unicodedata

from CharDisplay import getCharInfo
from alogging import ALogger
lg = ALogger(1)

__metadata__ = {
    'title'        : "strfchr.py",
    "description"  : "Flexible conversion between character representations.",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 3.6",
    'created'      : "2021-04-08",
    'modified'     : "2021-04-08",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr="""
=Description=

Convert special characters between a ton of representations.

This is modeled after *nix utilities like `strftime`, bash PS1, and similar,
that provide a large number of %-codes (or similar) so you can construct
a derived format from the data about a given "thing".

Notably, this includes TEX/LATEX conversions.

For example:

    strfchar --min 0xA0 --max 0xFF -f '"'    chr(%x):  ( %i, "%t", "%n" ),'

Will produce lines you can paste into a Python `dict` definition, to create
a map from literal non-ASCII Latin-1 characters, to tuples consisting
of their integer code point, TEX expression, and full Unicode name.

To get the list of %-codes, use `strfchr --help-codes` (as you might
expect, "%%" can also be used, to get a literal percent-sign).

You can use it from the command-line, or from code.


=Related Commands=

* My `CharDisplay.py` (and older Perl `ord`).
* My`showInvisibles.py` uses this.


=Known bugs and Limitations=

Should display better values for properties, like YES/NO.


=To Do=

* Incorporate into `ord` or `CharDisplay`?
* Option to escape quotes, backslash, etc. in generated output.
* Move the TEX support into `html2latex.py`?
* Options for minwidth, hex case, lfAs, spaceAs, controlAs.


=History=

  2021-04-08: Written by Steven J. DeRose.



=Rights=

Copyright 2021-04-08 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
For further information on this license, see
[https://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
# Some encodings can be modified by width and case settings.
# `isRepr` below, is 1 for infoItems that uniquely represent
# the character, as opposed to being values for a character,
# that many other characters may also have.
# However, not all representations cover all characters.
# If not defined, a fallback representation is returned instead.
#
__infoItems__ = {
    # name:          (isRep, example),
    #----------------------------------
    "LITERAL":       ( 1, chr(0x00E2)),

    # Code point based
    "SLASH0":        ( 1, "\\x{e2}" ),  # ["v" for variable-length]
    "SLASH2":        ( 1, "\\xe2" ),
    "SLASH4":        ( 1, "\\u00e2" ),
    "SLASH8":        ( 1, "\\U000000e2" ),
    "DECENTITY":     ( 1, "&#226;" ),
    "HEXENTITY":     ( 1, "&#xe2;" ),
    "NAMEDENTITY":   ( 1, "&acirc;" ),
    "BININT":        ( 1, "0b01110010"),
    "OCTINT":        ( 1, "0342" ),
    "DECINT":        ( 1, "226" ),
    "HEXINT":        ( 1, "0xE2" ),

    # Unicode notions
    "UNAME":         ( 1, "LATIN SMALL LETTER A WITH CIRCUMFLEX" ),
    "UNORM":         ( 1, "LATIN_SMALL_LETTER_A_WITH_CIRCUMFLEX" ),
    "UPLUS":         ( 1, "U+00E2" ),

    # App based
    "TEX":           ( 1, "{\\^a}" ),
    "URI":           ( 1, "%c3%a2" ),
    "UTF8":          ( 1, "\\xc3\\xa2" ),

    # For control characters only
    "MNEMONIC":      ( 1, "[SOH and other control-char abbrs]" ),
    "CONTROLPIC":    ( 1, "[Unicode CONTROL PICTUREs]" ),

    # Properties (vs. representations)
    "BLOCKNAME":     ( 0, "General Punctuation" ),
    "CATEGORYABBR":  ( 0, "Po" ),
    "CATEGORYNAME":  ( 0, "Punctuation, Other" ),
    "PLANENUMBER":   ( 0, "0" ),
    "PLANENAME":     ( 0, "Basic Multilingual" ),
    "SCRIPTNAME":    ( 0, "Common" ),

    "NFC":           ( 0, unicodedata.normalize("NFC", chr(0xE2)) ),
    "NFD":           ( 0, unicodedata.normalize("NFD", chr(0xE2)) ),
    "NFKC":          ( 0, unicodedata.normalize("NFKC", chr(0xE2)) ),
    "NFKD":          ( 0, unicodedata.normalize("NFKD", chr(0xE2)) ),

    "EAWIDTH":       ( 0, "A" ),
    "WIDTH":         ( 0, "" ),
    "NUMERICVALUE":  ( 0, "" ),
    "ISNUMERIC":     ( 0, "NO" ),
    "ISBIDI":        ( 0, "NO" ),
    "ISCOMBINING":   ( 0, "NO" ),
    "ISCOMBINED":    ( 0, "YES" ),
    "ISURI":         ( 0, "NO" ),
    "MIRROR":        ( 0, "NO" ),
}

__mnemonicMap__ = {
    "l": "LITERAL",
    "0": "SLASH0",
    "2": "SLASH2",
    "4": "SLASH4",
    "8": "SLASH8",

    "D": "DECENTITY",
    "X": "HEXENTITY",
    "N": "NAMEDENTITY",
    "b": "BININT",
    "o": "OCTINT",
    "d": "DECINT",
    "x": "HEXINT",
    "u": "UNORM",
    "U": "UNAME",
    "+": "UPLUS",

    # App based
    "t": "TEX",
    "f": "UTF8",
    "F": "URI",   # Escaped UTF8

    # For control characters only
    "M": "MNEMONIC",
    "m": "CONTROLPIC",

    # Properties (vs. representations)
    "B": "BLOCKNAME",
    "g": "CATEGORYABBR",
    "G": "CATEGORYNAME",
    "p": "PLANENUMBER",
    "P": "PLANENAME",
    "S": "SCRIPTNAME",

    "c": "NFC",
    "C": "NFD",
    "k": "NFKC",
    "K": "NFKD",

    "e": "EAWIDTH",
    "w": "WIDTH",
    "v": "NUMERICVALUE",
    "#": "ISNUMERIC",
    #"": "ISBIDI",
    #"": "ISCOMBINING",
    #"": "ISCOMBINED",
    #"": "ISURI",
    #"": "MIRROR",
}
__name2mnemonic__ = {}
for k0, v0 in __mnemonicMap__.items():
    assert v0 in __infoItems__.keys()
    assert len(__infoItems__[v0]) == 2
    __name2mnemonic__[v0] = k0

# Selected Unicode combining chars
# https://github.com/sderose/Charsets/Unicode/asPython/blob/master/combining.py
#
__unicodeCombining__ = {
    # codept:  TEX    Unicode name
    0x00300: ( "\\`", 'COMBINING GRAVE ACCENT' ),
    0x00301: ( "\\'", 'COMBINING ACUTE ACCENT' ),
    0x00302: ( "\\^", 'COMBINING CIRCUMFLEX ACCENT' ),
    0x00303: ( "\\~", 'COMBINING TILDE' ),
    #0x00304: ( " ",   'COMBINING MACRON' ),
    0x00305: ( "\\=", 'COMBINING OVERLINE' ),
    0x00306: ( "\\u", 'COMBINING BREVE' ),
    0x00307: ( "\\.", 'COMBINING DOT ABOVE' ),
    0x00308: ( "\\\"", 'COMBINING DIAERESIS' ),
    0x00309: ( " ",   'COMBINING HOOK ABOVE' ),
    0x0030a: ( "\\r", 'COMBINING RING ABOVE' ),
    0x0030b: ( "\\H", 'COMBINING DOUBLE ACUTE ACCENT' ),
    0x00326: ( "\\c", 'COMBINING COMMA BELOW' ),    # *******
    0x00327: ( "\\c", 'COMBINING CEDILLA' ),        # *******
    0x00328: ( "\\k", 'COMBINING OGONEK' ),         # *******
}
__moreUnicodeCombining__ = {
    0x0030c: ( " ", 'COMBINING CARON' ),
    0x0030d: ( " ", 'COMBINING VERTICAL LINE ABOVE' ),
    0x0030e: ( " ", 'COMBINING DOUBLE VERTICAL LINE ABOVE' ),
    0x0030f: ( " ", 'COMBINING DOUBLE GRAVE ACCENT' ),

    0x00310: ( " ", 'COMBINING CANDRABINDU' ),
    0x00311: ( " ", 'COMBINING INVERTED BREVE' ),
    0x00312: ( " ", 'COMBINING TURNED COMMA ABOVE' ),
    0x00313: ( " ", 'COMBINING COMMA ABOVE' ),
    0x00314: ( " ", 'COMBINING REVERSED COMMA ABOVE' ),
    0x00315: ( " ", 'COMBINING COMMA ABOVE RIGHT' ),
    0x00316: ( " ", 'COMBINING GRAVE ACCENT BELOW' ),
    0x00317: ( " ", 'COMBINING ACUTE ACCENT BELOW' ),
    0x00318: ( " ", 'COMBINING LEFT TACK BELOW' ),
    0x00319: ( " ", 'COMBINING RIGHT TACK BELOW' ),
    0x0031a: ( " ", 'COMBINING LEFT ANGLE ABOVE' ),
    0x0031b: ( " ", 'COMBINING HORN' ),
    0x0031c: ( " ", 'COMBINING LEFT HALF RING BELOW' ),
    0x0031d: ( " ", 'COMBINING UP TACK BELOW' ),
    0x0031e: ( " ", 'COMBINING DOWN TACK BELOW' ),
    0x0031f: ( " ", 'COMBINING PLUS SIGN BELOW' ),

    0x00320: ( " ", 'COMBINING MINUS SIGN BELOW' ),
    0x00321: ( " ", 'COMBINING PALATALIZED HOOK BELOW' ),
    0x00322: ( " ", 'COMBINING RETROFLEX HOOK BELOW' ),
    0x00323: ( " ", 'COMBINING DOT BELOW' ),
    0x00324: ( " ", 'COMBINING DIAERESIS BELOW' ),
    0x00325: ( " ", 'COMBINING RING BELOW' ),
    0x00329: ( " ", 'COMBINING VERTICAL LINE BELOW' ),
    0x0032a: ( " ", 'COMBINING BRIDGE BELOW' ),
    0x0032b: ( " ", 'COMBINING INVERTED DOUBLE ARCH BELOW' ),
    0x0032c: ( " ", 'COMBINING CARON BELOW' ),
    0x0032d: ( " ", 'COMBINING CIRCUMFLEX ACCENT BELOW' ),
    0x0032e: ( " ", 'COMBINING BREVE BELOW' ),
    0x0032f: ( " ", 'COMBINING INVERTED BREVE BELOW' ),

    0x00330: ( " ", 'COMBINING TILDE BELOW' ),
    0x00331: ( " ", 'COMBINING MACRON BELOW' ),
    0x00332: ( " ", 'COMBINING LOW LINE' ),
    0x00333: ( " ", 'COMBINING DOUBLE LOW LINE' ),
    0x00334: ( " ", 'COMBINING TILDE OVERLAY' ),
    0x00335: ( " ", 'COMBINING SHORT STROKE OVERLAY' ),
    0x00336: ( " ", 'COMBINING LONG STROKE OVERLAY' ),
    0x00337: ( " ", 'COMBINING SHORT SOLIDUS OVERLAY' ),
    0x00338: ( " ", 'COMBINING LONG SOLIDUS OVERLAY' ),
    0x00339: ( " ", 'COMBINING RIGHT HALF RING BELOW' ),
    0x0033a: ( " ", 'COMBINING INVERTED BRIDGE BELOW' ),
    0x0033b: ( " ", 'COMBINING SQUARE BELOW' ),
    0x0033c: ( " ", 'COMBINING SEAGULL BELOW' ),
    0x0033d: ( " ", 'COMBINING X ABOVE' ),
    0x0033e: ( " ", 'COMBINING VERTICAL TILDE' ),
    0x0033f: ( " ", 'COMBINING DOUBLE OVERLINE' ),

    0x00340: ( " ", 'COMBINING GRAVE TONE MARK' ),
    0x00341: ( " ", 'COMBINING ACUTE TONE MARK' ),
    0x00342: ( " ", 'COMBINING GREEK PERISPOMENI' ),
    0x00343: ( " ", 'COMBINING GREEK KORONIS' ),
    0x00344: ( " ", 'COMBINING GREEK DIALYTIKA TONOS' ),
    0x00345: ( " ", 'COMBINING GREEK YPOGEGRAMMENI' ),
    0x00346: ( " ", 'COMBINING BRIDGE ABOVE' ),
    0x00347: ( " ", 'COMBINING EQUALS SIGN BELOW' ),
    0x00348: ( " ", 'COMBINING DOUBLE VERTICAL LINE BELOW' ),
    0x00349: ( " ", 'COMBINING LEFT ANGLE BELOW' ),
    0x0034a: ( " ", 'COMBINING NOT TILDE ABOVE' ),
    0x0034b: ( " ", 'COMBINING HOMOTHETIC ABOVE' ),
    0x0034c: ( " ", 'COMBINING ALMOST EQUAL TO ABOVE' ),
    0x0034d: ( " ", 'COMBINING LEFT RIGHT ARROW BELOW' ),
    0x0034e: ( " ", 'COMBINING UPWARDS ARROW BELOW' ),
    0x0034f: ( " ", 'COMBINING GRAPHEME JOINER' ),

    0x00350: ( " ", 'COMBINING RIGHT ARROWHEAD ABOVE' ),
    0x00351: ( " ", 'COMBINING LEFT HALF RING ABOVE' ),
    0x00352: ( " ", 'COMBINING FERMATA' ),
    0x00353: ( " ", 'COMBINING X BELOW' ),
    0x00354: ( " ", 'COMBINING LEFT ARROWHEAD BELOW' ),
    0x00355: ( " ", 'COMBINING RIGHT ARROWHEAD BELOW' ),
    0x00356: ( " ", 'COMBINING RIGHT ARROWHEAD AND UP ARROWHEAD BELOW' ),
    0x00357: ( " ", 'COMBINING RIGHT HALF RING ABOVE' ),
    0x00358: ( " ", 'COMBINING DOT ABOVE RIGHT' ),
    0x00359: ( " ", 'COMBINING ASTERISK BELOW' ),
    0x0035a: ( " ", 'COMBINING DOUBLE RING BELOW' ),
    0x0035b: ( " ", 'COMBINING ZIGZAG ABOVE' ),
    0x0035c: ( " ", 'COMBINING DOUBLE BREVE BELOW' ),
    0x0035d: ( " ", 'COMBINING DOUBLE BREVE' ),
    0x0035e: ( " ", 'COMBINING DOUBLE MACRON' ),
    0x0035f: ( " ", 'COMBINING DOUBLE MACRON BELOW' ),

    0x00360: ( " ", 'COMBINING DOUBLE TILDE' ),
    0x00361: ( " ", 'COMBINING DOUBLE INVERTED BREVE' ),
    0x00362: ( " ", 'COMBINING DOUBLE RIGHTWARDS ARROW BELOW' ),
    0x00363: ( " ", 'COMBINING LATIN SMALL LETTER A' ),
    0x00364: ( " ", 'COMBINING LATIN SMALL LETTER E' ),
    0x00365: ( " ", 'COMBINING LATIN SMALL LETTER I' ),
    0x00366: ( " ", 'COMBINING LATIN SMALL LETTER O' ),
    0x00367: ( " ", 'COMBINING LATIN SMALL LETTER U' ),
    0x00368: ( " ", 'COMBINING LATIN SMALL LETTER C' ),
    0x00369: ( " ", 'COMBINING LATIN SMALL LETTER D' ),
    0x0036a: ( " ", 'COMBINING LATIN SMALL LETTER H' ),
    0x0036b: ( " ", 'COMBINING LATIN SMALL LETTER M' ),
    0x0036c: ( " ", 'COMBINING LATIN SMALL LETTER R' ),
    0x0036d: ( " ", 'COMBINING LATIN SMALL LETTER T' ),
    0x0036e: ( " ", 'COMBINING LATIN SMALL LETTER V' ),
    0x0036f: ( " ", 'COMBINING LATIN SMALL LETTER X' ),
}
__texDiacritics__ = {
    #"grave":		( r'À', r'{\`A}' ),
    #"acute":		( r'Á', r"{\'A}" ),
    #"double acute":	( r'Ő', r'{\H O}' ),
    #"circumflex":	( r'Â', r'{\^A}' ),
    "hachek":		( r'Č', r'{\\v C}' ),
    #"dot above":	( r'Ċ', r'{\.C}' ),
    #"umlaut)":		( r'Ä', r'{\"A}' ),  # two dots above, trema, /diaeresis
    #"tilde":		( r'Ã', r'{\~A}' ),
    #"bar above":	( r'Ā', r'{\=A}' ),
    #"breve above":	( r'Ă', r'{\u A}' ),
    #"ring above":	( r'Å', r'{\r A}' ), # We use generic LaTeX2e notation \r
    #"cedilla":		( r'Ç', r'{\c C}' ),
    #"comma below":	( r'Ș', r'{\c S}' ),
    #"ogonek":		( r'Ą', r'{\k A}' ),
}

def buildTable(minChar, maxChar):
    """Collect all the diacritics
       Add the specials

    """
    for codePoint in range(minChar, maxChar):
        _c = chr(codePoint)


###############################################################################
#
from functools import partial
from typing import Union

def strfchr(n:Union[str, int], fmt:str) -> str:
    """Make something from one character, kind of like strftime().
    """
    if (isinstance(n, str)): n = ord(n[0])
    cmapper = partial(mapperFunc, theCodepoint=n)
    return re.sub(r"%(.)", cmapper, fmt)

def mapperFunc(mat, theCodepoint:int) -> str:
    fmtCode = mat.group(1)
    if (fmtCode == "%"): return "%"
    return codePointToEncoding(theCodepoint, what=fmtCode)


###############################################################################
#
__cinfoCache__ = {}

def codePointToEncoding(codePoint:int, what:str) -> str:
    """Given a character's code point, and what mnemonic or named
    form/property you want, get that value.
    """
    if (codePoint in __cinfoCache__):
        cinfo = __cinfoCache__[codePoint]
    else:
        cinfo = __cinfoCache__[codePoint] = getCharInfo(codePoint)

    # Allow mnemonics
    if (what in __mnemonicMap__): what = __mnemonicMap__[what]

    if (what == "LITERAL"):                # ...
        return chr(codePoint)

    elif (what == "SLASH0"):               # \\x{e2}
        return "\\x{%x}" % (codePoint)
    elif   (what == "SLASH2"):             # \\xe2
        if (codePoint <= 0xFF): return "\\x%02x" % (codePoint)
        return gefFallback(codePoint)
    elif (what == "SLASH4"):               # \\u00e2
        if (codePoint <= 0xFFFF): return "\\u%04x" % (codePoint)
        return gefFallback(codePoint)
    elif (what == "SLASH8"):               # \\U000000e2
        return "\\U%08x" % (codePoint)

    elif (what == "DECENTITY"):            # &#226;
        return "&#%4d;" % (codePoint)
    elif (what == "HEXENTITY"):            # &#xe2;
        return "&#x%04x;" % (codePoint)
    elif (what == "NAMEDENTITY"):          # &acirc;
        nam = cinfo['entNamed']
        if (nam): return nam
        return gefFallback(codePoint)
    elif (what == "BININT"):               # 0342
        assert False
        #if   (codePoint <= 0xFF): return "%08b" % (codePoint)
        #elif (codePoint <= 0xFFFF): return "%016b" % (codePoint)
        #return "%020b" % (codePoint)
    elif (what == "OCTINT"):               # 0342
        return "%o" % (codePoint)
    elif (what == "DECINT"):               # 226
        return "%d" % (codePoint)
    elif (what == "HEXINT"):               # 0x00e2
        return "0x%04x" % (codePoint)

    elif (what == "UNAME"):                # LATIN SMALL LETTER A WITH CIRCUMFLEX
        return cinfo["name"]
    elif (what == "UNORM"):                # LATIN_SMALL_LETTER_A_WITH_CIRCUMFLEX
        return cinfo["name"].replace(" ", "_")
    elif (what == "UPLUS"):                # U+00E2
        return "U+%04x" % (codePoint)

    elif (what == "UTF8"):                 # \\xc3\\xa2
        return cinfo["utf8"]
    elif (what == "TEX"):                  # {\\^a} # TODO
        return getTexEquivalent(codePoint)
    elif (what == "URI"):                  # %c3%a2
        return cinfo["uri"]

    # On to non-representations (properties)
    #
    elif (what == "BLOCKNAME"):        # "General Punctuation" ),
        assert False
    elif (what == "CATEGORYABBR"):     # "Po" ),
        assert False
    elif (what == "CATEGORYNAME"):     # "Punctuation, Other" ),
        assert False
    elif (what == "PLANENUMBER"):      # "0" ),
        assert False
    elif (what == "PLANENAME"):        # "Basic Multilingual" ),
        assert False
    elif (what == "SCRIPTNAME"):       # "Common" ),
        assert False

    elif (what == "NFC"):              # ... ),
        return cinfo['NFC']
    elif (what == "NFD"):              # ... ),
        return cinfo['NFD']
    elif (what == "NFKC"):             # ... ),
        return cinfo['NFKC']
    elif (what == "NFKD"):             # ... ),
        return cinfo['NFKD']

    elif (what == "EAWIDTH"):          # "A" ),
        return cinfo['eawidth']
    elif (what == "WIDTH"):            # "" ),
        assert False
    elif (what == "NUMERICVALUE"):     # "" ),
        assert False
    elif (what == "ISNUMERIC"):        # "NO" ),
        assert False
    elif (what == "ISBIDI"):           # "NO" ),
        return cinfo['bidi']
    elif (what == "ISCOMBINING"):      # "NO" ),
        return cinfo['combining']
    elif (what == "ISCOMBINED"):       # "YES" ),
        return cinfo['combined']
    elif (what == "ISURI"):            # "NO" ),
        assert False
    elif (what == "MIRROR"):           # "NO" ),
        return cinfo['mirror']

    else:
        assert False, "Unknown character info item '%s'." % (what)

def gefFallback(codePoint):
    # TODO Make an option for what to use here
    return "&#x%04x;" % (codePoint)


###############################################################################
#
def getTexEquivalent(codePoint):  # TODO: Finish, move to html2latex.py
    return "\\x{%04x}" % (codePoint)

# Following started from utf8tobibtex.py
#
charInfo = [
    ( r'\\', r'{\\textbackslash}' ),
    ( r'&', r'\&' ),
    ( r'#', r'\#' ),
    ( r'%', r'\%' ),
    ( r'\$', r'\\\$' ),
    ( r'~', r'\~{}' ),
    ( r'<', r'{\\textless}' ),
    ( r'>', r'{\\textgreater}' ),
    ( r'_', r'\_' ),
    ( r'\^', r'\\\^{}' ),
    ( r'\|', r'{\\textbar}' ),
    ( r'"', r'{\dq}' ), # Needs the babel package
    ( r'£', r'{\pounds}' ),
    ( r'©', r'{\copyright}' ),
    ( r'§', r'{\S}' ),

  # A few special letters
    ( r'Æ', r'{\AE}' ),
    ( r'æ', r'{\ae}' ),
    ( r'Ð', r'{\DH}' ),
    ( r'ð', r'{\dh}' ),
    ( r'Đ', r'{\DJ}' ),
    ( r'đ', r'{\dj}' ),
    ( r'ı', r'{\i}' ),
    ( r'Ĳ', r'{\IJ}' ),
    ( r'ĳ', r'{\ij}' ),
    ( r'ȷ', r'{\j}' ),
    ( r'Ł', r'{\L}' ),
    ( r'ł', r'{\l}' ),
    ( r'Ŋ', r'{\NG}' ),
    ( r'ŋ', r'{\\ng}' ),
    ( r'Ø', r'{\O}' ),
    ( r'ø', r'{\o}' ),
    ( r'Œ', r'{\OE}' ),
    ( r'œ', r'{\oe}' ),
    ( r'ẞ', r'{\SS}' ),  # LaTeX representation is "SS"
    ( r'ß', r'{\ss}' ),
    ( r'Þ', r'{\TH}' ),
    ( r'þ', r'{\\th}' ),
 ]


def showCodes():
    print("List of %-codes for format strings (U+00E2 as example):")
    for k, v in __infoItems__.items():
        try:
            mn = "%" + __name2mnemonic__[k]
        except KeyError:
            mn = chr(0x2205)  # Empty set
        print('    %2s:  %-16s %s %s' % (mn, k, v[0], v[1]))
    return


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse
    from PowerWalk import PowerWalk, PWType

    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--format", type=str, metavar="F", default="%8 %4 %2 %0 %N (URI %F)",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--help-codes", action="store_true",
            help="Display a list of %%-codes and exit.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
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

        if (args0.help_codes):
            showCodes()
            sys.exit()

        return(args0)


    ###########################################################################
    #
    args = processOptions()

    if (args.help_codes):
        showCodes()
        sys.exit()

    if (sys.stdin.isatty()):
        print("Format string in effect is: %s" % (args.format))
        print("Enter some text (^D to exit)...")
    for rec in sys.stdin.readlines():
        for i, c in enumerate(rec):
            n = ord(c)
            print("  %2d: U+%04x '%s': %s" % (i, n, c, strfchr(n, fmt=args.format)))
