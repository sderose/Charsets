#!/usr/bin/env python
#
# strfchr.py: Flexible conversion between character representations.
# 2021-04-08: Written by Steven J. DeRose
#
#pylint: disable=I1101
#
import sys
import re
import os
import unicodedata
import html
from html.entities import codepoint2name  # name2codepoint
import xml
from enum import Enum
from subprocess import check_output
#from typing import Union

from CharDisplay import getCharInfo
# TODO Fix
from CharDisplay import myCodepoint2script, myCodepoint2block, unicodeCategories, unixJargon

import DomExtensions
from alogging import ALogger
lg = ALogger(1)

__metadata__ = {
    "title"        : "strfchr.py",
    "description"  : "Flexible conversion between character representations.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.6",
    "created"      : "2021-04-08",
    "modified"     : "2021-04-08",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr="""
=Description=

Convert special characters between a ton of representations.

This is modeled after *nix utilities like `strftime`, `stat`,
shell prompt strings, and similar,
that provide a large number of %-codes (see below) so you can construct
a derived format from the data about a given "thing".

For example:

    strfchr.py --min 0xA0 --max 0xA3
        -f 'chr(%x): ( %x, "%l", { "script":"%S", "end":"%N" }),'

produces lines like:

    chr(0x00a0): ( 0x00a0, " ", { "script":"Common", "end":"  &nbsp;" }),
    chr(0x00a1): ( 0x00a1, "¡", { "script":"Common", "end":"  &iexcl;" }),
    chr(0x00a2): ( 0x00a2, "¢", { "script":"Common", "end":"  &cent;" }),

This example format might be used to make a Python list.

To get the list of %-codes, the corresponding names, and a bit of
information about each, use `strfchr --help-codes`. As you might
expect, "%%" can be used to get a literal percent-sign).
"%{name}" can also be used, with longer names for the forms or properties.

There is a set of "extended" information, that can be loaded on request to
provide mappings to many other special character representations. These
are based on (imho, superb) work by my old friend Sebastian Rahtz,
David Carlisle, and others [https://www.w3.org/Math/characters/unicode.xml]

You can use it from code, or in 3 ways from the command-line, all of
which will display one line for each code point involved,
formatted per `-f`:
* if you specify --min and --max you get the code points in that range
* if you provide one or more arguments that are single characters or
integers (such as 0xFF, 255, or 0377), a line will be printed for each.
* otherwise, you can type text and at the end the characters in that text
will be used.

TEX/LATEX, AFII, and other conversions are coming.


=Related Commands=

* My `CharDisplay.py` (and older Perl `ord`).
* My`showInvisibles.py` uses this.


=Known bugs and Limitations=

Should display better values for some properties, like YES/NO.

Need to integrate Sebastian et al's excellent data from
[https://www.w3.org/Math/characters/unicode.xml].


=To Do=

* Integrate with `ord` or `CharDisplay`?
* Finish TEX &c. support
* Options for minwidth, hex case, lfAs, spaceAs, controlAs.
* Option to escape quotes, backslash, etc. in generated output.
* Provide a few named formats, such as:
    PYDICT: '    "%u":  "%N",'
    PYLIST: '    myChars[%{HEXINT}] = "%{LITERAL}"'
* Perhaps, add full-string encoding with a way to specify a different
format for different ranges of chars. For example:
  [
    (    0,    32, "%{MNEMONIC}" ),
    (   32,   255, "%{LITERAL}),
    (  256, 65535, "%{SLASH4})
    (65536,    -1, "%{SLASH0})
  ]
* Support MIRROROF property.
* Way to set the particular fallback for undefined cases, such as
requesting MNEMONIC or CONTROLPIC for non-control chars.


=History=

  2021-04-08: Written by Steven J. DeRose.
  2021-04-20: Finish basic functionality.


=Rights=

Copyright 2021-04-08 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
For further information on this license, see
[https://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""

class Planes(Enum):
    pass

class Scripts(Enum):
    pass

class Block(Enum):
    pass

Categories = {
    "C":   "Other (all subtypes)",
    "L":   "Letter (all subtypes)",
    "M":   "Mark (all subtypes)",
    "N":   "Number (all subtypes)",
    "P":   "Punctuation (all subtypes)",
    "S":   "Symbol (all subtypes)",
    "Z":   "Separator (all subtypes)",

    "Cc":  "Other, Control",
    "Cf":  "Other, Format",
    "Cn":  "Other, Not Assigned",
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
    "Pf":  "Punctuation, Final quote",
    "Pi":  "Punctuation, Initial quote",
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

C0names = [
    "NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
    "BS",  "HT",  "LF",  "VT",  "FF",  "CR",  "SO",  "SI",
    "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB",
    "CAN",  "EM", "SUB", "ESC",  "FS",  "GS",  "RS",  "US",
    "SP"
]

C1names = [
    "PAD", "HOP",  "BPH", "NBH", "IND", "NEL", "SSA", "ESA",
    "HTS", "HTJ",  "VTS", "PLD", "PLU",  "RI", "SS2", "SS3",
    "DCS", "PU1",  "PU2", "STS", "CCH",  "MW", "SPA", "EPA",
    "SOS", "SGCI", "SCI", "CSI",  "ST", "OSC",  "PM", "APC",
    "NBS"
]

cp1252ToUnicode = {
    0x80 : 0x20AC,   # EURO SIGN
    # 0x81 UNUSED
    0x82 : 0x201A,   # SINGLE LOW-9 QUOTATION MARK
    0x83 : 0x0192,   # LATIN SMALL LETTER F WITH HOOK
    0x84 : 0x201E,   # DOUBLE LOW-9 QUOTATION MARK
    0x85 : 0x2026,   # HORIZONTAL ELLIPSIS
    0x86 : 0x2020,   # DAGGER
    0x87 : 0x2021,   # DOUBLE DAGGER
    0x88 : 0x02C6,   # MODIFIER LETTER CIRCUMFLEX ACCENT
    0x89 : 0x2030,   # PER MILLE SIGN
    0x8A : 0x0160,   # LATIN CAPITAL LETTER S WITH CARON
    0x8B : 0x2039,   # SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x8C : 0x0152,   # LATIN CAPITAL LIGATURE OE
    # 0x8D UNUSED
    0x8E : 0x017D,   # LATIN CAPITAL LETTER Z WITH CARON
    # 0x8F UNUSED
    # 0x90 UNUSED
    0x91 : 0x2018,   # LEFT SINGLE QUOTATION MARK
    0x92 : 0x2019,   # RIGHT SINGLE QUOTATION MARK
    0x93 : 0x201C,   # LEFT DOUBLE QUOTATION MARK
    0x94 : 0x201D,   # RIGHT DOUBLE QUOTATION MARK
    0x95 : 0x2022,   # BULLET
    0x96 : 0x2013,   # EN DASH
    0x97 : 0x2014,   # EM DASH
    0x98 : 0x02DC,   # SMALL TILDE
    0x99 : 0x2122,   # TRADE MARK SIGN
    0x9A : 0x0161,   # LATIN SMALL LETTER S WITH CARON
    0x9B : 0x203A,   # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x9C : 0x0153,   # LATIN SMALL LIGATURE OE
    # 0x9D UNUSED
    0x9E : 0x017E,   # LATIN SMALL LETTER Z WITH CARON
    0x9F : 0x0178,   # LATIN CAPITAL LETTER Y WITH DIAERESIS
}

###############################################################################
#
UnicodeProperties = {
    # name:         ( typ, dft, descr, ),
    "AHex":		( ),
    "Alpha":		( ),
    "Bidi_C":		( ),
    "Bidi_M":		( ),
    "CE":		( ),
    "CI":		( ),
    "CWCF":		( ),
    "CWCM":		( ),
    "CWKCF":		( ),
    "CWL":		( ),
    "CWT":		( ),
    "CWU":		( ),
    "Cased":		( ),
    "Comp_Ex":		( ),
    "DI":		( ),
    "Dash":		( ),
    "Dep":		( ),
    "Dia":		( ),
    "Ext":		( ),
    "FC_NFKC":		( ),
    "GCB":		( ),
    "Gr_Base":		( ),
    "Gr_Ext":		( ),
    "Gr_Link":		( ),
    "Hex":		( ),
    "Hyphen":		( ),
    "IDC":		( ),
    "IDS":		( ),
    "IDSB":		( ),
    "IDST":		( ),
    "Ideo":		( ),
    "InMC":		( ),
    "InSC":		( ),
    "JSN":		( ),
    "Join_C":		( ),
    "LOE":		( ),
    "Lower":		( ),
    "Math":		( ),
    "NChar":		( ),
    "NFC_QC":		( ),
    "NFD_QC":		( ),
    "NFKC_CF":		( ),
    "NFKC_QC":		( ),
    "NFKD_QC":		( ),
    "OAlpha":		( ),
    "ODI":		( ),
    "OGr_Ext":		( ),
    "OIDC":		( ),
    "OIDS":		( ),
    "OLower":		( ),
    "OMath":		( ),
    "OUpper":		( ),
    "Pat_Syn":		( ),
    "Pat_WS":		( ),
    "QMark":		( ),
    "Radical":		( ),
    "SB":		( ),
    "SD":		( ),
    "STerm":		( ),
    "Term":		( ),
    "UIdeo":		( ),
    "Upper":		( ),
    "VS":		( ),
    "WB":		( ),
    "WSpace":		( ),
    "XIDC":		( ),
    "XIDS":		( ),
    "XO_NFC":		( ),
    "XO_NFD":		( ),
    "XO_NFKC":		( ),
    "XO_NFKD":		( ),
    "age":		( ),
    "bc":		( ),
    "blk":		( ),
    "bmg":		( ),
    "ccc":		( ),
    "cf":		( ),
    "cp":		( ),
    "dm":		( ),
    "dt":		( ),
    "ea":		( ),
    "gc":		( ),
    "hst":		( ),
    "isc":		( ),
    "jg":		( ),
    "jt":		( ),
    "lb":		( ),
    "lc":		( ),
    "na":		( ),
    "na1":		( ),
    "nt":		( ),
    "nv":		( ),
    "sc":		( ),
    "scf":		( ),
    "scx":		( ),
    "slc":		( ),
    "stc":		( ),
    "suc":		( ),
    "tc":		( ),
    "uc":		( ),

    # Occasional (67 cases)
    "first":		( ),
    "last":		( ),
}


###############################################################################
#
class UDBEntry(dict):
    pass


###############################################################################
# https://www.unicode.org/Public/5.2.0/ucdxml/
# https://www.unicode.org/reports/tr44/
class UnicodeDBAccess:
    NORMATIVE_FILES = [
    ]

    def __init__(self):
        pass

    def readUDB(self, path:str):
        """
        """
        #FILENAME = "ucd.nounihan.flat.xml"
        #FILENAME2 = "ucd.unihan.flat.xml"
        EXPECTEDFIELDS = 15
        _TYPES = [ ]
        charEntries = {}

        lastN = 0
        docEl = xml.dom.minidom.parse(path)
        for centry in docEl.eachElement("char"):
            rec = centry.nodeValue()
            if (rec[0] == "@"): continue
            assert rec.isascii(), "UnicodeData not all ASCII"
            if rec.strip() == "": continue
            fields = rec.split(";")
            assert len(fields) == EXPECTEDFIELDS
            n = int(fields[0], 16)
            assert n > lastN
            lastN = n
            UdbEntry()



###############################################################################
#
class InfoValues(Enum):
    P = "Property"
    F = "Format"
    f = "Limited-scope format"
    C = "Calculable"
    c = "Calculable via library"
    X = "None"
    S = "In Sebastian file"

class CharInfo:
    """Store, look up, calculate, and return various properties of a char.
    """
    P = InfoValues.P
    F = InfoValues.F
    f = InfoValues.f
    C = InfoValues.C
    c = InfoValues.c
    X = InfoValues.X
    S = InfoValues.S

    __infoItems__ = {  # cf CharDisplay.charProperties
        # Properties (vs. representations)
        "BLOCKNAME":   ( P, X,    0,   str,  "General Punctuation" ),
        "CATEGORYABBR":( P, X,    0,   str,  "Po" ),
        "CATEGORYNAME":( P, X,    0,   str,  "Punctuation, Other" ),
        "PLANENAME":   ( P, X,    0,   str,  "Basic Multilingual" ),
        "PLANENUMBER": ( P, C,    0,   int,  "0" ),
        "SCRIPTNAME":  ( P, X,    0,   str,  "Common" ),
        "UNAME":       ( P, c,    0,   str,  "LATIN SMALL LETTER A WITH CIRCUMFLEX" ),
        "UNORM":       ( P, c,    0,   str,  "LATIN_SMALL_LETTER_A_WITH_CIRCUMFLEX" ),
        "JARGON":      ( P, X,    0,   str,  "[*nix jargon file entries, if any]" ),

        #"DECOMP":
        "NFC":         ( P, X,    0,   str,  unicodedata.normalize("NFC", chr(0xE2)) ),
        "NFD":         ( P, X,    0,   str,  unicodedata.normalize("NFD", chr(0xE2)) ),
        "NFKC":        ( P, X,    0,   str,  unicodedata.normalize("NFKC", chr(0xE2)) ),
        "NFKD":        ( P, X,    0,   str,  unicodedata.normalize("NFKD", chr(0xE2)) ),

        "EAWIDTH":     ( P, X,    0,   float, "" ),
        "WIDTH":       ( P, X,    0,   float, "" ),
        "NUMERICVALUE":( P, X,    0,   float, "" ),

        "ISURI":       ( P, X,    0,   bool,  "NO" ),
        "ISFPI":       ( P, X,    0,   bool,  "NO" ),
        "ISNUMERIC":   ( P, X,    0,   bool,  "NO" ),
        "ISBIDI":      ( P, X,    0,   bool,  "NO" ),
        "ISCOMBINING": ( P, X,    0,   bool,  "NO" ),
        "ISCOMBINED":  ( P, X,    0,   bool,  "YES" ),
        "ISMIRROR":    ( P, X,    0,   bool,  "NO" ),
        "MIRROROF":    ( P, X,    0,   str,   "" ),

        # Alternate forms
        # Different ways to display any character
        # name:       (P/F, calc, Seb, typ, example),
        "LITERAL":     ( F, C,    0,   str,  chr(0x00E2)),
        "SLASH0":      ( F, C,    0,   str,  "\\x{e2}" ),
        "SLASH2":      ( F, C,    0,   str,  "\\xe2" ),
        "SLASH4":      ( F, C,    0,   str,  "\\u00e2" ),
        "SLASH8":      ( F, C,    0,   str,  "\\U000000e2" ),
        "DECENTITY":   ( F, C,    0,   str,  "&#226;" ),
        "HEXENTITY":   ( F, C,    0,   str,  "&#xe2;" ),
        "NAMEDENTITY": ( F, c,    0,   str,  "&acirc;" ),
        "BININT":      ( F, C,    0,   str,  "0b01110010"),
        "OCTINT":      ( F, C,    0,   str,  "0342" ),
        "DECINT":      ( F, C,    0,   str,  "226" ),
        "HEXINT":      ( F, C,    0,   str,  "0xE2" ),
        "UPLUS":       ( F, C,    0,   str,  "U+00E2" ),
        "URI":         ( F, C,    0,   str,  "%c3%a2" ),
        "UTF8":        ( F, C,    0,   str,  "\\xc3\\xa2" ),

        # TODO FROMCP1252 ??

        # For control characters only
        "MNEMONIC":    ( f, c,    0,   str,  "[SOH and other control-char abbrs]" ),
        "CONTROLPIC":  ( f, c,    0,   str,  "[Unicode CONTROL PICTUREs]" ),

        # Ones that requires lookup, not calculation


    }

    __extendedItems__ = {  # From Sebastian's file
        "ACS":          ( F, X,    S,  str, "freq:61", ),
        "AIP":          ( F, X,    S,  str, "freq:394", ),
        "AMS":          ( F, X,    S,  str, "freq:526", ),
        "APS":          ( F, X,    S,  str, "freq:463", ),
        "Elsevier":     ( F, X,    S,  str, "freq:745", ),
        "IEEE":         ( F, X,    S,  str, "freq:223", ),
        "Springer":     ( F, X,    S,  str, "freq:30", ),
        "Wolfram":      ( F, X,    S,  str, "freq:695", ),
        "afii":         ( F, X,    S,  str, "freq:1170", ),
        "bmp":          ( F, X,    S,  str, "freq:24", ),
        #"character":    ( F, X,    S,  str, "freq:5646", ),
        "charlist":     ( P, X,    S,  str, "freq:1", ),
        "comment":      ( P, X,    S,  str, "freq:210", ),
        "desc":         ( P, X,    S,  str, "freq:3974", ),
        "description":  ( P, X,    S,  str, "freq:5646", ),
        "elsrender":    ( F, X,    S,  str, "freq:50", ),
        #"entity":       ( F, X,    S,  str, "freq:3975", ),
        "entitygroups": ( P, X,    S,  str, "freq:1", ),
        "font":         ( P, X,    S,  str, "freq:560", ),
        "group":        ( P, X,    S,  str, "freq:5", ),
        "latex":        ( F, X,    S,  str, "freq:2480", ),
        "mathlatex":    ( F, X,    S,  str, "freq:198", ),
        "mathvariant":  ( F, X,    S,  str, "freq:13", ),
        "mathvariants": ( F, X,    S,  str, "freq:1", ),
        "set":          ( F, X,    S,  str, "freq:56", ),
        "surrogate":    ( F, X,    S,  str, "freq:1016", ),
        "varlatex":     ( F, X,    S,  str, "freq:18", ),
        "xref":         ( P, X,    S,  str, "freq:63", ),
        #"@image":       ( F, X,    S,  str, "freq:1442", ),
        #"@mode":        ( F, X,    S,  str, "freq:4321", ),
        #"@type":        ( F, X,    S,  str, "freq:4321", ),
    }

    def __init__(self, wh):
        self.ERROR = None
        if (isinstance(wh, int)):
            self.n = wh
            self.c = chr(wh)
        else:
            self.c = wh
            self.n = ord(wh)
        self.setCharInfo()

    def getitem(self, k):
        if (k not in CharInfo.__infoItems__ and
            k not in CharInfo.__extendedItems__):
            raise KeyError("Unknown character property '%s'." % (k))

    # For forms we can easily calculate, use properties.
    #
    @property
    def LITERAL(self): return self.c

    @property
    def PLANENUMBER(self):
        return self.n >> 16
    def PLANENAME(self):
        pnum = self.n >> 16
        if (pnum ==  0): pname = "Basic Multilingual"
        elif (pnum ==  1): pname = "Supplementary Multilingual"
        elif (pnum ==  2): pname = "Supplementary Ideographic"
        elif (pnum == 16): pname = "Supplementary Private Use Area B"
        elif (pnum == 15): pname = "Supplementary Private Use Area A"
        elif (pnum == 14): pname = "Supplementary Special-purpose"
        elif (pnum >=  3): pname = "Unassigned"
        else             : pname = "-UNKNOWN-"
        return pname
    @property
    def JARGON(self):
        if (self.c in unixJargon): return unixJargon[self.c]
        return None

    @property
    def SLASH0(self): return "\\x{%x}" % (self.n)
    @property
    def SLASH2(self):
        if (self.n <= 0xFF): return "\\x%02x" % (self.n)
        return getFallback(self)
    @property
    def SLASH4(self):
        if (self.n <= 0xFFFF): return "\\u%04x" % (self.n)
        return getFallback(self)
    @property
    def SLASH8(self): return "\\U%08x" % (self.n)
    @property
    def DECENTITY(self): return "&#%4d;" % (self.n)
    @property
    def HEXENTITY(self): return "&#x%04x;" % (self.n)
    @property
    def NAMEDENTITY(self):
        nam = cinfo["entNamed"]
        if (nam): return nam
        return getFallback(self)

    @property
    def BININT(self):                       # 0342
        assert False
        #if   (self.n <= 0xFF): return "%08b" % (self.n)
        #elif (self.n <= 0xFFFF): return "%016b" % (self.n)
        #return "%020b" % (self.n)
    @property
    def OCTINT(self): return "%o" % (self.n)
    @property
    def DECINT(self): return "%d" % (self.n)
    @property
    def HEXINT(self): return "0x%04x" % (self.n)

    @property
    def UTF8(self):
        buf = "\\x"
        myBytes = self.c.encode("utf-8")
        for b in myBytes: buf += "%02x" % (b)
        return buf
    @property
    def URL(self): urlquote(self.c.encode("utf-8"))
    @property
    def MNEMONIC(self):
        if (self.n <= 0x20): return C0names[self.n]
        if (0x80 <= self.n <= 0x9F): return C1names[self.n-0x80]
        return getFallback(self)
    @property
    def CONTROLPIC(self):
        if (self.n <= 0x20): return chr(0x2400+self.n)
        return getFallback(self)

    ###########################################################################
    #
    # pylint: disable=W0201
    #
    def setCharInfo(self):
        """Gather a lot of info about the given code point.
        See https://docs.python.org/2/library/unicodedata.html
        """
        c = self.c
        n = self.n
        if (n > 0xFFFFF):
            self.ERROR = "[Out of range]"
            return charInfo

        if (n == 0xEFBFBD):
            self.ERROR = "UTF-8 of U+FFFD (Replacement Character)"
            return charInfo

        self.NAME = unicodedata.name(self.c, None)
        if (not self.NAME):  # Includes private use chars.
            self.ERROR = "Cannot find name for U+%05x." % (n)
            self.NAME = "[???]"

        self.SCRIPTNAME = myCodepoint2script(n)
        self.BLOCKNAME = myCodepoint2block(n)

        self.NUMVAL = unicodedata.numeric(self.c, None)
        self.CATEGORYABBR = unicodedata.category(self.c)
        self.CATEGORYNAME = None
        if (self.CATEGORYNAME in unicodeCategories):
            self.CATEGORYNAME = unicodeCategories[self.CATEGORYNAME][1]

        # Alternate forms
        buf = "\\x"
        myBytes = self.c.encode("utf-8")
        for b in myBytes: buf += "%02x" % (b)
        self.UTF = buf
        self.URI = urlquote(self.c.encode("utf-8"))
        self.HEXENTITY = "&#x%05x;" % (n)
        self.DECENTITY = "&#%d;" % (n)
        #print("type: %s" % (type(codepoint2name)))
        if (n in codepoint2name):
            self.NAMEDENTITY = "  &%s;" % (codepoint2name[n])
        else:
            self.NAMEDENTITY = None

        # Properties
        #
        self.ISURI = n<128 and re.match(CharDisplay.okInUriExpr, c)
        # ISFPI
        self.ISBIDI = unicodedata.bidirectional(self.c)
        self.COMBINING = unicodedata.combining(self.c)
        self.EAWIDTH = unicodedata.east_asian_width(self.c)
        self.ISMIRROR = unicodedata.mirrored(self.c)
        # MIRROROF

        self.DECOMP = unicodedata.decomposition(self.c)
        self.NFC = unicodedata.normalize("NFC",  self.c)
        self.NFKC = unicodedata.normalize("NFKC", self.c)
        self.NFD = unicodedata.normalize("NFD",  self.c)
        self.NFKD = unicodedata.normalize("NFKD", self.c)

        return charInfo


###############################################################################
#

class Sebastian(dict):
    def __init__(self, path:str=None):
        #super(dict, self).__init__()
        self.sourceUrl = "https://www.w3.org/Math/characters/unicode.xml"
        if (path is None):
            self.path = os.path.join(os.environ["HOME"], ".strfchr", "unicode.xml")
        else:
            self.path = path
        self.loadData()

    def loadData(self):
        if (not os.path.exists(self.path)):
            check_output([ "curl", self.sourceUrl, ">>", self.path ])
        if (not os.path.exists(self.path)):
            lg.fatal("Could not download data from '%s'." % (self.sourceUrl))
        DomExtensions.patchDom()
        xdoc = xml.dom.minidom.parse(self.path)

        charList = xdoc.getChild("charlist")
        nChars = 0
        for charEl in charList.childNodes:
            if (charEl.nodeName != "character"): continue
            idVal = charEl.getAttribute("id")
            dec = charEl.getAttribute("dec")
            assert idVal[0]=="U" and idVal[1:].isdigit()
            assert int(idVal[1:].lstrip("0")) == int(dec)
            ci = CharInfo(int(dec))
            for propEl in charEl.childNodes:
                if propEl.nodeType != xml.dom.Node.ELEMENT_NODE: continue
                prop = propEl.nodeName
                if (prop not in CharInfo.__infoItems__ or
                    CharInfo.__infoItems__[prop][2]!="C"):
                    assert False, "Unexpected prop '%s'." % (prop)
                propVal = propEl.innerText()
                ci.setprop(prop, propVal)
                # TODO: A few have attributes....
            d = charEl.getChild("description")
            d_unicode = d.getAttribute("unicode")
            d_text = d.innerText()
            nChars += 1


###############################################################################
#
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
    #"t": "TEX",
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
    #"": "ISMIRROR",
}
__name2mnemonic__ = {}
for k0, v0 in __mnemonicMap__.items():
    if (v0 not in CharInfo.__infoItems__.keys()):
        assert False, ("Name '%s' (<'%s') not found in __intoItems__." %
            (v0, k0))
    iiLen = len(CharInfo.__infoItems__[v0])
    if (iiLen != 5):
        assert False, ("Mnemonic '%s' in __intoItems__, bad length %d." %
            (v0, iiLen))
    __name2mnemonic__[v0] = k0

# Selected Unicode combining chars
# https://github.com/sderose/Charsets/Unicode/asPython/blob/master/combining.py
#
__unicodeCombining__ = {  # The ones that have ready-made (La)TEX codes
    # codept:  TEX    Unicode name
    0x00300: ( "\\`", "COMBINING GRAVE ACCENT" ),
    0x00301: ( "\\'", "COMBINING ACUTE ACCENT" ),
    0x00302: ( "\\^", "COMBINING CIRCUMFLEX ACCENT" ),
    0x00303: ( "\\~", "COMBINING TILDE" ),
    0x00304: ( "\\=", "COMBINING MACRON" ),
    0x00305: ( "\\=", "COMBINING OVERLINE" ),
    0x00306: ( "\\u", "COMBINING BREVE" ),
    0x00307: ( "\\.", "COMBINING DOT ABOVE" ),
    0x00308: ( "\\\"", "COMBINING DIAERESIS" ),
    0x0030a: ( "\\r", "COMBINING RING ABOVE" ),
    0x0030b: ( "\\H", "COMBINING DOUBLE ACUTE ACCENT" ),
    0x00326: ( "\\c", "COMBINING COMMA BELOW" ),
    0x00327: ( "\\c", "COMBINING CEDILLA" ),
    0x00328: ( "\\k", "COMBINING OGONEK" ),
}

__moreUnicodeCombining__ = {
    0x00309: ( " ",   "COMBINING HOOK ABOVE" ),
    0x0030c: ( " ", "COMBINING CARON" ),
    0x0030d: ( " ", "COMBINING VERTICAL LINE ABOVE" ),
    0x0030e: ( " ", "COMBINING DOUBLE VERTICAL LINE ABOVE" ),
    0x0030f: ( " ", "COMBINING DOUBLE GRAVE ACCENT" ),

    0x00310: ( " ", "COMBINING CANDRABINDU" ),
    0x00311: ( " ", "COMBINING INVERTED BREVE" ),
    0x00312: ( " ", "COMBINING TURNED COMMA ABOVE" ),
    0x00313: ( " ", "COMBINING COMMA ABOVE" ),
    0x00314: ( " ", "COMBINING REVERSED COMMA ABOVE" ),
    0x00315: ( " ", "COMBINING COMMA ABOVE RIGHT" ),
    0x00316: ( " ", "COMBINING GRAVE ACCENT BELOW" ),
    0x00317: ( " ", "COMBINING ACUTE ACCENT BELOW" ),
    0x00318: ( " ", "COMBINING LEFT TACK BELOW" ),
    0x00319: ( " ", "COMBINING RIGHT TACK BELOW" ),
    0x0031a: ( " ", "COMBINING LEFT ANGLE ABOVE" ),
    0x0031b: ( " ", "COMBINING HORN" ),
    0x0031c: ( " ", "COMBINING LEFT HALF RING BELOW" ),
    0x0031d: ( " ", "COMBINING UP TACK BELOW" ),
    0x0031e: ( " ", "COMBINING DOWN TACK BELOW" ),
    0x0031f: ( " ", "COMBINING PLUS SIGN BELOW" ),

    0x00320: ( " ", "COMBINING MINUS SIGN BELOW" ),
    0x00321: ( " ", "COMBINING PALATALIZED HOOK BELOW" ),
    0x00322: ( " ", "COMBINING RETROFLEX HOOK BELOW" ),
    0x00323: ( " ", "COMBINING DOT BELOW" ),
    0x00324: ( " ", "COMBINING DIAERESIS BELOW" ),
    0x00325: ( " ", "COMBINING RING BELOW" ),
    0x00329: ( " ", "COMBINING VERTICAL LINE BELOW" ),
    0x0032a: ( " ", "COMBINING BRIDGE BELOW" ),
    0x0032b: ( " ", "COMBINING INVERTED DOUBLE ARCH BELOW" ),
    0x0032c: ( " ", "COMBINING CARON BELOW" ),
    0x0032d: ( " ", "COMBINING CIRCUMFLEX ACCENT BELOW" ),
    0x0032e: ( " ", "COMBINING BREVE BELOW" ),
    0x0032f: ( " ", "COMBINING INVERTED BREVE BELOW" ),

    0x00330: ( " ", "COMBINING TILDE BELOW" ),
    0x00331: ( " ", "COMBINING MACRON BELOW" ),
    0x00332: ( " ", "COMBINING LOW LINE" ),
    0x00333: ( " ", "COMBINING DOUBLE LOW LINE" ),
    0x00334: ( " ", "COMBINING TILDE OVERLAY" ),
    0x00335: ( " ", "COMBINING SHORT STROKE OVERLAY" ),
    0x00336: ( " ", "COMBINING LONG STROKE OVERLAY" ),
    0x00337: ( " ", "COMBINING SHORT SOLIDUS OVERLAY" ),
    0x00338: ( " ", "COMBINING LONG SOLIDUS OVERLAY" ),
    0x00339: ( " ", "COMBINING RIGHT HALF RING BELOW" ),
    0x0033a: ( " ", "COMBINING INVERTED BRIDGE BELOW" ),
    0x0033b: ( " ", "COMBINING SQUARE BELOW" ),
    0x0033c: ( " ", "COMBINING SEAGULL BELOW" ),
    0x0033d: ( " ", "COMBINING X ABOVE" ),
    0x0033e: ( " ", "COMBINING VERTICAL TILDE" ),
    0x0033f: ( " ", "COMBINING DOUBLE OVERLINE" ),

    0x00340: ( " ", "COMBINING GRAVE TONE MARK" ),
    0x00341: ( " ", "COMBINING ACUTE TONE MARK" ),
    0x00342: ( " ", "COMBINING GREEK PERISPOMENI" ),
    0x00343: ( " ", "COMBINING GREEK KORONIS" ),
    0x00344: ( " ", "COMBINING GREEK DIALYTIKA TONOS" ),
    0x00345: ( " ", "COMBINING GREEK YPOGEGRAMMENI" ),
    0x00346: ( " ", "COMBINING BRIDGE ABOVE" ),
    0x00347: ( " ", "COMBINING EQUALS SIGN BELOW" ),
    0x00348: ( " ", "COMBINING DOUBLE VERTICAL LINE BELOW" ),
    0x00349: ( " ", "COMBINING LEFT ANGLE BELOW" ),
    0x0034a: ( " ", "COMBINING NOT TILDE ABOVE" ),
    0x0034b: ( " ", "COMBINING HOMOTHETIC ABOVE" ),
    0x0034c: ( " ", "COMBINING ALMOST EQUAL TO ABOVE" ),
    0x0034d: ( " ", "COMBINING LEFT RIGHT ARROW BELOW" ),
    0x0034e: ( " ", "COMBINING UPWARDS ARROW BELOW" ),
    0x0034f: ( " ", "COMBINING GRAPHEME JOINER" ),

    0x00350: ( " ", "COMBINING RIGHT ARROWHEAD ABOVE" ),
    0x00351: ( " ", "COMBINING LEFT HALF RING ABOVE" ),
    0x00352: ( " ", "COMBINING FERMATA" ),
    0x00353: ( " ", "COMBINING X BELOW" ),
    0x00354: ( " ", "COMBINING LEFT ARROWHEAD BELOW" ),
    0x00355: ( " ", "COMBINING RIGHT ARROWHEAD BELOW" ),
    0x00356: ( " ", "COMBINING RIGHT ARROWHEAD AND UP ARROWHEAD BELOW" ),
    0x00357: ( " ", "COMBINING RIGHT HALF RING ABOVE" ),
    0x00358: ( " ", "COMBINING DOT ABOVE RIGHT" ),
    0x00359: ( " ", "COMBINING ASTERISK BELOW" ),
    0x0035a: ( " ", "COMBINING DOUBLE RING BELOW" ),
    0x0035b: ( " ", "COMBINING ZIGZAG ABOVE" ),
    0x0035c: ( " ", "COMBINING DOUBLE BREVE BELOW" ),
    0x0035d: ( " ", "COMBINING DOUBLE BREVE" ),
    0x0035e: ( " ", "COMBINING DOUBLE MACRON" ),
    0x0035f: ( " ", "COMBINING DOUBLE MACRON BELOW" ),

    0x00360: ( " ", "COMBINING DOUBLE TILDE" ),
    0x00361: ( " ", "COMBINING DOUBLE INVERTED BREVE" ),
    0x00362: ( " ", "COMBINING DOUBLE RIGHTWARDS ARROW BELOW" ),
    0x00363: ( " ", "COMBINING LATIN SMALL LETTER A" ),
    0x00364: ( " ", "COMBINING LATIN SMALL LETTER E" ),
    0x00365: ( " ", "COMBINING LATIN SMALL LETTER I" ),
    0x00366: ( " ", "COMBINING LATIN SMALL LETTER O" ),
    0x00367: ( " ", "COMBINING LATIN SMALL LETTER U" ),
    0x00368: ( " ", "COMBINING LATIN SMALL LETTER C" ),
    0x00369: ( " ", "COMBINING LATIN SMALL LETTER D" ),
    0x0036a: ( " ", "COMBINING LATIN SMALL LETTER H" ),
    0x0036b: ( " ", "COMBINING LATIN SMALL LETTER M" ),
    0x0036c: ( " ", "COMBINING LATIN SMALL LETTER R" ),
    0x0036d: ( " ", "COMBINING LATIN SMALL LETTER T" ),
    0x0036e: ( " ", "COMBINING LATIN SMALL LETTER V" ),
    0x0036f: ( " ", "COMBINING LATIN SMALL LETTER X" ),
}

__texDiacritics__ = [  # Can these be combined?
    # name           entAbbr      combiner    texAbbr example
    ( "grave",        "grave",    chr(0x0300), r"`",  r"{\`A}" ),
    ( "acute",        "acute",    chr(0x0301), r"'",  r"{\'A}" ),
    ( "circumflex",   "circ",     chr(0x0302), r"^",  r"{\^A}" ),
    ( "tilde",        "tilde",    chr(0x0303), r"~",  r"{\~A}" ),
    ( "bar above",    "",         chr(0x0304), r"=",  r"{\=A}" ),  # macron
    ( "breve above",  "",         chr(0x0306), r"u ", r"{\u A}" ),
    ( "dot above",    "",         chr(0x0307), r".",  r"{\.C}" ),
    ( "umlaut",       "uml",      chr(0x0308), r"\"", r'{\"A}' ),  # two dots above, trema, diaeresis
    ( "ring above",   "ring",     chr(0x030A), r"r ", r"{\r A}" ), # We use generic LaTeX2e notation \r
    ( "double acute", "",         chr(0x030B), r"H ", r"{\H O}" ),
    ( "hachek",       "caron",    chr(0x030C), r"v ", r"{\v C}" ),  # caron
    ( "cedilla",      "",         chr(0x0327), r"c ", r"{\c C}" ),
    ( "comma below",  "",         chr(0x0326), r"c ", r"{\c S}" ),
    ( "ogonek",       "",         chr(0x0328), r"k ", r"{\k A}" ),
]

combinersKnownInTex = {}
for td in __texDiacritics__:
    combinersKnownInTex[td[2]] = td

def entityToTex(eref:str) -> str:
    """
    """
    c = html.decode(eref)
    if (len(c) != 1): raise KeyError()
    decomp = unicodedata.normalize("NFKD", c)
    buf = ""
    for part in decomp:
        if (part in combinersKnownInTex):
            buf += combinersKnownInTex[part][3]
        else:
            buf += part
    return buf

# TODO: Does name2codepoint handle numerics?
# how to get from codepoint to TEX?
# https://tex.stackexchange.com/questions/9790/mapping-from-unicode-character-to-latex-symbol-for-bibtex
# https://www.w3.org/Math/characters/unicode.xml

###############################################################################
#
from functools import partial

def strfchr(n, fmt:str) -> str:
    """Make something from a character or code point, kind of like strftime().
    Replace instances of %x, %%, and %{name} with the right data.
    """
    if (isinstance(n, str)): n = ord(n[0])
    cmapper = partial(mapperFunc, theCodepoint=n)
    return re.sub(r"%({[^}]+}|.)", cmapper, fmt)

def mapperFunc(mat, theCodepoint:int) -> str:
    fmtCode = mat.group(1)
    if (fmtCode == "%"): return "%"
    try:
        val = codePointToDatum(theCodepoint, what=fmtCode)
    except KeyError as e:
        lg.fatal("KeyError for code point 0x%04x: %s" % (theCodepoint, e))
    return val


###############################################################################
#
__cinfoCache__ = {}

def codePointToDatum(codePoint:int, what:str) -> str:
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
        return  (codePoint)
    elif (what == "SLASH4"):               # \\u00e2
        if (codePoint <= 0xFFFF): return "\\u%04x" % (codePoint)
        return getFallback(codePoint)
    elif (what == "SLASH8"):               # \\U000000e2
        return "\\U%08x" % (codePoint)

    elif (what == "DECENTITY"):            # &#226;
        return "&#%4d;" % (codePoint)
    elif (what == "HEXENTITY"):            # &#xe2;
        return "&#x%04x;" % (codePoint)
    elif (what == "NAMEDENTITY"):          # &acirc;
        nam = cinfo["NAMEDENTITY"]
        if (nam): return nam
        return getFallback(codePoint)
    elif (what == "BININT"):               # 0342
        assert False, "binary decoding not yet supported."
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
        return cinfo["URI"]

    # On to non-representations (properties)
    #
    elif (what == "BLOCKNAME"):        # "General Punctuation" ),
        return cinfo["BLOCKNAME"]
    elif (what == "CATEGORYABBR"):     # "Po" ),
        return cinfo["CATEGORYABBR"]
    elif (what == "CATEGORYNAME"):     # "Punctuation, Other" ),
        return cinfo["CATEGORYNAME"]
    elif (what == "PLANENUMBER"):      # "0" ),
        return cinfo["PLANENUMBER"]
    elif (what == "PLANENAME"):        # "Basic Multilingual" ),
        return cinfo["PLANENAME"]
    elif (what == "SCRIPTNAME"):       # "Common" ),
        return cinfo["SCRIPTNAME"]

    elif (what == "EAWIDTH"):          # "A" ),
        return cinfo["EAWIDTH"]
    elif (what == "WIDTH"):            # "" ),
        return cinfo["WIDTH"]
    elif (what == "NUMERICVALUE"):     # "" ),
        return cinfo["NUMERICVALUE"]

    elif (what == "ISNUMERIC"):        # "NO" ),
        return cinfo["ISNUMERIC"]
    elif (what == "ISBIDI"):           # "NO" ),
        return cinfo["ISBIDI"]
    elif (what == "ISCOMBINING"):      # "NO" ),
        return cinfo["ISCOMBINING"]
    elif (what == "ISCOMBINED"):       # "YES" ),
        return cinfo["ISCOMBINED"]
    elif (what == "ISURI"):            # "NO" ),
        return cinfo["ISURI"]
    elif (what == "ISMIRROR"):         # "NO" ),
        return cinfo["ISMIRROR"]
    elif (what == "MIRROROF"):         # "NO" ),
        return cinfo["MIRROROF"]

    elif (what == "DECOMP"):           # ... ),
        return cinfo["DECOMP"]
    elif (what == "NFC"):              # ... ),
        return cinfo["NFC"]
    elif (what == "NFD"):              # ... ),
        return cinfo["NFD"]
    elif (what == "NFKC"):             # ... ),
        return cinfo["NFKC"]
    elif (what == "NFKD"):             # ... ),
        return cinfo["NFKD"]

    else:
        raise KeyError("Unknown datum code '%s'." % (what))

def getFallback(codePoint:int):
    # TODO Make an option for what to use here
    return "&#x%04x;" % (codePoint)


###############################################################################
#
def getTexEquivalent(codePoint:int):  # TODO: Finish, move to html2latex.py
    return "\\x{%04x}" % (codePoint)

# Following started from utf8tobibtex.py
#
charInfo = [
    ( r"\\", r"{\\textbackslash}" ),
    ( r"&", r"\&" ),
    ( r"#", r"\#" ),
    ( r"%", r"\%" ),
    ( r"\$", r"\\\$" ),
    ( r"~", r"\~{}" ),
    ( r"<", r"{\\textless}" ),
    ( r">", r"{\\textgreater}" ),
    ( r"_", r"\_" ),
    ( r"\^", r"\\\^{}" ),
    ( r"\|", r"{\\textbar}" ),
    ( r'"', r"{\dq}" ), # Needs the babel package
    ( r"£", r"{\pounds}" ),
    ( r"©", r"{\copyright}" ),
    ( r"§", r"{\S}" ),

  # A few special letters
    ( r"Æ", r"{\AE}" ),
    ( r"æ", r"{\ae}" ),
    ( r"Ð", r"{\DH}" ),
    ( r"ð", r"{\dh}" ),
    ( r"Đ", r"{\DJ}" ),
    ( r"đ", r"{\dj}" ),
    ( r"ı", r"{\i}" ),
    ( r"Ĳ", r"{\IJ}" ),
    ( r"ĳ", r"{\ij}" ),
    ( r"ȷ", r"{\j}" ),
    ( r"Ł", r"{\L}" ),
    ( r"ł", r"{\l}" ),
    ( r"Ŋ", r"{\NG}" ),
    ( r"ŋ", r"{\\ng}" ),
    ( r"Ø", r"{\O}" ),
    ( r"ø", r"{\o}" ),
    ( r"Œ", r"{\OE}" ),
    ( r"œ", r"{\oe}" ),
    ( r"ẞ", r"{\SS}" ),
    ( r"ß", r"{\ss}" ),
    ( r"Þ", r"{\TH}" ),
    ( r"þ", r"{\\th}" ),
 ]


def showCodes():
    print("""List of %-codes for format strings (U+00E2 as example).
    P/F: Property or Format?         Calc: Can be easily derived
    Seb: In Sebastian Rahtz's db?    Type: datatype of value\n""")
    print("  code:  name             P/F Calc Seb  Type  Example")
    for k, v in CharInfo.__infoItems__.items():
        try:
            mn = "%" + __name2mnemonic__[k]
        except KeyError:
            mn = chr(0x2205)  # Empty set
        print("    %2s:  %-16s %3s %4s %3d %5s  %s" %
            (mn, k, v[0].name, v[1].name, v[2], v[3].__name__, v[4]))
    return


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse
    def anyInt(x):
        return int(x, 0)

    DFT_FORMAT = "%8 %4 %2 %0 %N (URI %F)"

    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--format", "-f", type=str, metavar="F", default=DFT_FORMAT,
            help="Specify what to print, using %%_ and/or %%{___} codes.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--help-codes", action="store_true",
            help="Display a list of %%-codes and names, and exit.")
        parser.add_argument(
            "--max", type=anyInt, metavar="N",
            help="If this and --min are set, show codepoints in that range.")
        parser.add_argument(
            "--min", type=anyInt, metavar="N",
            help="If this and --max are set, show codepoints in that range.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Add more messages (repeatable).")
        parser.add_argument(
            "--version", action="version", version=__version__,
            help="Display version information, then exit.")

        parser.add_argument(
            "codePoints", type=str,
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

    if (args.min and args.max):
        for n0 in range(args.min, args.max):
            print(strfchr(n0, fmt=args.format))
        sys.exit()

    if (args.codePoints):
        for n0 in args.codePoints:
            if (len(n0)==1): n0 = ord(n0)
            else: n0 = int(n0, 0)
            print(strfchr(n0, fmt=args.format))
        sys.exit()

    if (sys.stdin.isatty()):
        print("Format string in effect is: %s" % (args.format))
        print("Enter some text (^D to exit)...")
    for rec0 in sys.stdin.readlines():
        for i0, c0 in enumerate(rec0):
            n0 = ord(c0)
            print("  %2d: U+%04x '%s': %s" % (i0, n0, c0, strfchr(n0, fmt=args.format)))
