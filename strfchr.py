#!/usr/bin/env python3
#
# strfchr.py: Flexible conversion between character representations.
# 2021-04-08: Written by Steven J. DeRose.
#
#pylint: disable=I1101
#
import sys
import re
import codecs
import unicodedata
import xml
import html
from html.entities import codepoint2name  # name2codepoint
from urllib.parse import quote as urlquote
from enum import Enum
#from typing import Union
from functools import partial

from CharDisplay import getCharInfo
# TODO Fix
from CharDisplay import myCodepoint2script, myCodepoint2block, unicodeCategories, unixJargon
import CharDisplay

#import DomExtensions
from alogging import ALogger
lg = ALogger(1)

__metadata__ = {
    "title"        : "strfchr",
    "description"  : "Flexible conversion between character representations.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.6",
    "created"      : "2021-04-08",
    "modified"     : "2023-11-23",
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
* charNameConvert.py -- a set of "extended" information, that can be loaded on request to
provide mappings to many other special character representations. These
are based on (imho, superb) work by my old friend Sebastian Rahtz,
David Carlisle, and others [https://www.w3.org/Math/characters/unicode.xml]


=Known bugs and Limitations=

Should display better values for some properties, like YES/NO.

Need to integrate Sebastian et al's excellent data from
[https://www.w3.org/Math/characters/unicode.xml].


=To Do=

* Check and add [X]ID_Start / [X]ID_Continue [http://unicode.org/reports/tr31/]
[http://unicode.org/reports/tr31/]
* Add a property(s) that gets you an ascified or latin1ified version, say:
    if (c.isASCII() and c.isPrint()): return literal
    elif (ord(c) <= 0xFF): return "\\x%02x" % ord(c)
    elif (ord(c) < = 0xFFFF): return "\\u%04x" % ord(c)
    else: eturn "\\x{%x}" % ord(c)
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
  2021-10-28: Lint fixes. Support loading from XML or CSV(ish). fill out
info on normative files, char props, etc.


=Rights=

Copyright 2021-04-08 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
For further information on this license, see
[https://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""

verbose = 0
def log(lvl:int, msg:str) -> None:
    if (verbose >= lvl): sys.stderr.write(msg+"\n")

try:
    import charNameConvert
    sebastian = charNameConvert.charNameConvert()
except ImportError:
    pass

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
# typename      must match         tgt type
UNKNOWN = (str, r".*",             str,   )
UBOOL   = (str, r"^[NY]$",         bool,  )
UDECINT = (str, r"^[\d]{1,8}$",    int,   )
UHEXINT = (str, r"^[\dA-F]{1,5}$", int,   )
OHEXINT = (str, r"^([\dA-F]{1,5}|#)$", str,   )   # Optional UHEXINT
UHEXINTS = (str, r"^([\dA-F]{1,5})(\s+[\dA-F]{1,5})*$", int,   )  # 1 or more
UTOKEN  = (str, r"^\w+$",          str,   )
UTBOOL  = (str, r"%[NYM]$",        str,   )
UGCAT   = (str, r"^[A-Z][a-z]$",   str,   )
OCTO    = True  # Signals that "#" is ok

# ??  Prepended_Concatenation_Mark; "InPC" ??
# Many more unihan properties, all starting with "k".
#
UnicodeProperties = {
    # Attribute name   (  freq, ),  #
    "AHex":            (   254, None, UBOOL,   ),  # ASCII_Hex_Digit
    "Alpha":           (  2122, None, UBOOL,   ),  # Alphabetic
    "Bidi_C":          (   239, None, UBOOL,   ),  # Bidi_Control
    "Bidi_M":          (   595, None, UBOOL,   ),  # mirrored
    "CE":              (   310, None, UBOOL,   ),  # Composition_Exclusion
    "CI":              (  1136, None, UBOOL,   ),  # Case_Ignorable
    "CWCF":            (  1302, None, UBOOL,   ),  # Changes_When_Casefolded
    "CWCM":            (   682, None, UBOOL,   ),  # Changes_When_Casemapped
    "CWKCF":           (  1637, None, UBOOL,   ),  # Changes_When_NFKC_Casefolded
    "CWL":             (  1255, None, UBOOL,   ),  # Changes_When_Lowercased
    "CWT":             (  1278, None, UBOOL,   ),  # Changes_When_Titlecased
    "CWU":             (  1256, None, UBOOL,   ),  # Changes_When_Uppercased
    "Cased":           (   742, None, UBOOL,   ),  # Cased
    "Comp_Ex":         (   363, None, UBOOL,   ),  # Full_Composition_Exclusion
    "DI":              (   276, None, UBOOL,   ),  # Default_Ignorable_Code_Point
    "Dash":            (   257, None, UBOOL,   ),  # Dash
    "Dep":             (   247, None, UBOOL,   ),  #
    "Dia":             (   683, None, UBOOL,   ),  # Diacritic
    # Emoji properties
    "Emoji":           (   683, None, UBOOL,   ),  #
    "EPres":           (   683, None, UBOOL,   ),  #
    "EMod":            (   683, None, UBOOL,   ),  #
    "EBase":           (   683, None, UBOOL,   ),  #
    "EComp":           (   683, None, UBOOL,   ),  #
    "ExtPict":         (   683, None, UBOOL,   ),  #
    #
    "EqUIdeo":         (     0, None, UHEXINT, ),  # Equivalent_Unified_Ideograph
    "Ext":             (   260, None, UBOOL,   ),  # Extender
    "FC_NFKC":         (   840, None,    "",   ),  #
    "GCB":             (  1672, None,   str,   ),  # Grapheme_Cluster_Break (2-3 letter code  )
    "Gr_Base":         (  1429, None, UBOOL,   ),  # Grapheme_Base
    "Gr_Ext":          (   921, None, UBOOL,   ),  # Grapheme_Extend
    "Gr_Link":         (   259, None, UBOOL,   ),  # Grapheme_Link
    "Hex":             (   276, None, UBOOL,   ),  # Hex_Digit
    "Hyphen":          (   243, None, UBOOL,   ),  # Hyphen
    "IDC":             (  1482, None, UBOOL,   ),  # ID_Continue,
    "IDS":             (  2472, None, UBOOL,   ),  # ID_Start
    "IDSB":            (   235, None, UBOOL,   ),  # IDS_Binary_Operator
    "IDST":            (   234, None, UBOOL,   ),  # IDS_Trinary_Operator
    "Ideo":            (   254, None, UBOOL,   ),  # Ideographic
    "InSC":            (     0, None, UTOKEN,  ),  # Indic_Syllabic_Category
    "JSN":             (   298, None, UTOKEN,  ),  # Jamo_Short_Name r"[A-Z]{0,3}"?
    "Join_C":          (   234, None, UBOOL,   ),  # Join_Control
    "LOE":             (   247, None, UBOOL,   ),  # Logical_Order_Exception
    "Lower":           (  1805, None, UBOOL,   ),  # Lower_Case
    "Math":            (   521, None, UBOOL,   ),  # Math
    "NChar":           (   250, None, UBOOL,   ),  #
    # Normal forms
    "NFC_QC":          (   466, None, UTBOOL,  ),  # ..._Quick_Check { "Y" | "N" | "M" }?
    "NFD_QC":          (   754, None, UBOOL,   ),  # ..._Quick_Check { "Y" | "N" }?
    "NFKC_CF":         (  5952, OCTO, OHEXINT, ),  #  NKFC_Casefold { "#" | code-points }?
    "NFKC_QC":         (   822, None, UTBOOL,  ),  # ..._Quick_Check { "Y" | "N" | "M" }?
    "NFKD_QC":         (  1048, None, UBOOL,   ),  # ..._Quick_Check { "Y" | "N" }?
    #
    "OAlpha":          (   959, None, UBOOL,   ),  # Other_Alphabetic
    "ODI":             (   242, None, UBOOL,   ),  # Other_Default_Ignorable_Code_Point
    "OGr_Ext":         (   255, None, UBOOL,   ),  # Other_Grapheme_Extend
    "OIDC":            (   243, None, UBOOL,   ),  # Other_ID_Continue
    "OIDS":            (   236, None, UBOOL,   ),  # Other_ID_Start
    "OLower":          (   381, None, UBOOL,   ),  # Other_Lower_Case
    "OMath":           (   484, None, UBOOL,   ),  # Other_Math
    "OUpper":          (   274, None, UBOOL,   ),  # Other_Upper_Case
    "Pat_Syn":         (   384, None, UBOOL,   ),  # Pattern_Syntax
    "Pat_WS":          (   243, None, UBOOL,   ),  # Pattern_White_Space
    "QMark":           (   261, None, UBOOL,   ),  # Quotation_Mark
    "Radical":         (   235, None, UBOOL,   ),  # Radical
    "RI":              (     0, None, UBOOL,   ),  # Regional_Indicator
    "SB":              (  4514, None,   str,   ),  # Sentence_Break (2 letter code  )
    "SD":              (   278, None, UBOOL,   ),  # Soft_Dotted
    "STerm":           (   298, None, UBOOL,   ),  # Sentence_Terminal
    "Term":            (   393, None, UBOOL,   ),  # Terminal_Punctuation
    "UIdeo":           (   248, None, UBOOL,   ),  # Unified_Ideograph
    "Upper":           (  1701, None, UBOOL,   ),  # Upper_Case
    "VS":              (   235, None, UBOOL,   ),  #
    "WB":              (  2933, None,  str,    ),  # Word_Break (2-8 letter code)
    "WSpace":          (   258, None, UBOOL,   ),  # White_Space
    "XIDC":            (  1501, None, UBOOL,   ),  # XID_Continue
    "XIDS":            (  2493, None, UBOOL,   ),  # XID_Start
    "XO_NFC":          (   314, None, UBOOL,   ),  #
    "XO_NFD":          (   729, None, UBOOL,   ),  #
    "XO_NFKC":         (   818, None, UBOOL,   ),  #
    "XO_NFKD":         (  1205, None, UBOOL,   ),  #
    "age":             (  2213, None,  "1.1",  ),  # Version introduced, as \d+\.\d+
    "bc":              (  1745, None,  "BN",   ),  # bidirectional class
    "blk":             (                       ),  # Block name (_ not space)
    "bmg":             (   594, None, UHEXINT, ),  # code point of mirror character
    "bpb":             (     0,                ),  # bidi paired bracket
    "bpt":             (     0,                ),  # bidi paired bracket type
    "ccc":             (   694, None, UDECINT, ),  # decimal representation of the combining class.
    "cf":              (  1349, OCTO, UHEXINT, ),  # Case_Folding { "#" | code-points }?
    "cp":              ( 33248, None, UHEXINT, ),  # code point (hex)
    "cps":             (   511, None, UNKNOWN, ),  #
    "desc":            (    93, None, UNKNOWN, ),  #
    "dm":              ( 17062, OCTO,     "#", ),  # decomposition mapping { "#"|code-points }?
    "dt":              (  1968, None,     str, ),  # decomposition type { "can" |"com"|"enc"|"fin"
    #|"font"|"fra"|"init"|"iso"|"med"|"nar" |"nb"  |"sml"|"sqr" |"sub"|"sup"|"vert"|"wide"|"none"}?
    "ea":              (   929, None, UBOOL,   ),  # East Asian Width { "A"|"F"|"H"|"N"|"Na"|"W" }?
    "first-cp":        (   631, None, UNKNOWN, ),  #
    "gc":              (  4986, None,  UGCAT,  ),  # General Category (Lu, etc.)
    "hst":             (   658, None,  "NA",   ),  # Hangul_Syll_Type { L|LV|LVT|T|V|NA }?
    "ideograph":       (   237, None, UNKNOWN, ),  #
    "isc":             (   232, None,   str,   ),  # ISO 10646 comment
    "jg":              (   460, None,   str,   ),  # joining group (bug enum)
    "jt":              (  1093, None,   str,   ),  # joining class { "U"|"C"|"T"|"D"|"L"|"R" }?
    "last-cp":         (   631, None, UNKNOWN, ),  #
    "lb":              (  3254, None,   str,   ),  # Line_Break  (big enum of 2-3 letter codes)
    "lc":              (  1261, OCTO,   "#",   ),  #
    "na":              ( 32416, None,    "",   ),  # Current name
    "na1":             (  2236, None, UNKNOWN, ),  # Name in 1.0
    "name":            (   615, None, UNKNOWN, ),  #
    "new":             (     6, None, UNKNOWN, ),  #
    "nt":              (  1120, None,  "None", ),  # numeric type { "None"|"De"|"Di"|"Nu" }?
    "number":          (   237, None, UNKNOWN, ),  #
    "nv":              (  1384, None,    "",   ),  # numeric value, represented as a fraction
    "old":             (     6, None, UNKNOWN, ),  #
    "radical":         (   237, None, UNKNOWN, ),  #
    "sc":              (  1371, None,  "Zyyy", ),  # script (big enum of 4-char abbrs)
    "scf":             (  1273, None, OHEXINT, ),  # Simple_Case_Folding
    "slc":             (  1261, OCTO,  "#",    ),  #
    "scx":             (     0, None,          ),  # script extension { list { script + }}?
    "stc":             (  1269, OCTO,  "#",    ),  #
    "suc":             (  1269, OCTO,  "#",    ),  #
    "tc":              (  1317, OCTO,  "#",    ),  #
    "uc":              (  1344, OCTO,  "#",    ),  #
    "version":         (     6, None, UNKNOWN, ),  #
    "vo":              (     0, None, str,     ),  # Vertical_Orientation { "U"|"R"|"Tu"|"Tr" }?
    "when":            (    93, None, UNKNOWN, ),  #
    "xmlns":           (     1, None, UNKNOWN, ),  #
}


###############################################################################
#
class UdbEntry(dict):
    """A class intended to represent instances of entries from the Unicode
    Database (see https://unicode.org/ucd/)
    Keyed on the integer codepoint.
    TODO: Better as a namedtuple?
    """
    def __init__(self, props:dict):
        super(UdbEntry, self).__init__()
        for k, v in props.items():
            self[k] = v


###############################################################################
#
class UnicodeDBAccess:  # TODO: Unfinished
    """The "grouped" XML looks like the sample below.
    The attributes appear to inherit in the obvious manner; documentation
    is at [https://www.unicode.org/reports/tr42/].

    <group age="1.1" na="" JSN="" gc="Cc" ccc="0" dt="none" dm="#" nt="None"
    nv="" bc="BN" Bidi_M="N" bmg="" suc="#" slc="#" stc="#" uc="#" lc="#"
    tc="#" scf="#" cf="#" jt="U" jg="No_Joining_Group" ea="N" lb="CM" sc="Zyyy"
    Dash="N" WSpace="N" Hyphen="N" QMark="N" Radical="N" Ideo="N" UIdeo="N"
    IDSB="N" IDST="N" hst="NA" DI="N" ODI="N" Alpha="N" OAlpha="N" Upper="N"
    OUpper="N" Lower="N" OLower="N" Math="N" OMath="N" Hex="N" AHex="N"
    NChar="N" VS="N" Bidi_C="N" Join_C="N" Gr_Base="N" Gr_Ext="N" OGr_Ext="N"
    Gr_Link="N" STerm="N" Ext="N" Term="N" Dia="N" Dep="N" IDS="N" OIDS="N"
    XIDS="N" IDC="N" OIDC="N" XIDC="N" SD="N" LOE="N" Pat_WS="N" Pat_Syn="N"
    GCB="CN" WB="XX" SB="XX" CE="N" Comp_Ex="N" NFC_QC="Y" NFD_QC="Y"
    NFKC_QC="Y" NFKD_QC="Y" XO_NFC="N" XO_NFD="N" XO_NFKC="N" XO_NFKD="N"
    FC_NFKC="" CI="N" Cased="N" CWCF="N" CWCM="N" CWKCF="N" CWL="N" CWT="N"
    CWU="N" NFKC_CF="#" isc="">

    <char cp="0000" na1="NULL"/>
    <char cp="0001" na1="START OF HEADING"/>
    <char cp="0002" na1="START OF TEXT"/>
    <char cp="0003" na1="END OF TEXT"/>
    <char cp="0004" na1="END OF TRANSMISSION"/>
    <char cp="0005" na1="ENQUIRY"/>
    <char cp="0006" na1="ACKNOWLEDGE"/>
    <char cp="0007" na1="BELL"/>
    <char cp="0008" na1="BACKSPACE"/>
    <char cp="0009" bc="S" lb="BA" WSpace="Y" Pat_WS="Y" SB="SP"
        na1="CHARACTER TABULATION"/>
    <char cp="000A" bc="B" lb="LF" WSpace="Y" Pat_WS="Y" GCB="LF" WB="LF" SB="LF"
        na1="LINE FEED (LF)"/>
    <char cp="000B" bc="S" lb="BK" WSpace="Y" Pat_WS="Y" WB="NL" SB="SP"
        na1="LINE TABULATION"/>
    <char cp="000C" bc="WS" lb="BK" WSpace="Y" Pat_WS="Y" WB="NL" SB="SP"
        na1="FORM FEED (FF)"/>
    <char cp="000D" bc="B" lb="CR" WSpace="Y" Pat_WS="Y" GCB="CR" WB="CR" SB="CR"
        na1="CARRIAGE RETURN (CR)"/>
    <char cp="000E" na1="SHIFT OUT"/>
    <char cp="000F" na1="SHIFT IN"/>
    <char cp="0010" na1="DATA LINK ESCAPE"/>
    <char cp="0011" na1="DEVICE CONTROL ONE"/>
    <char cp="0012" na1="DEVICE CONTROL TWO"/>
    <char cp="0013" na1="DEVICE CONTROL THREE"/>
    <char cp="0014" na1="DEVICE CONTROL FOUR"/>
    <char cp="0015" na1="NEGATIVE ACKNOWLEDGE"/>
    <char cp="0016" na1="SYNCHRONOUS IDLE"/>
    <char cp="0017" na1="END OF TRANSMISSION BLOCK"/>
    <char cp="0018" na1="CANCEL"/>
    <char cp="0019" na1="END OF MEDIUM"/>
    <char cp="001A" na1="SUBSTITUTE"/>
    <char cp="001B" na1="ESCAPE"/>
    <char cp="001C" bc="B" na1="INFORMATION SEPARATOR FOUR"/>
    <char cp="001D" bc="B" na1="INFORMATION SEPARATOR THREE"/>
    <char cp="001E" bc="B" na1="INFORMATION SEPARATOR TWO"/>
    <char cp="001F" bc="S" na1="INFORMATION SEPARATOR ONE"/></group>
    ...
    """
    NORMATIVE_BASE_URI = "https://www.unicode.org/Public/5.2.0/ucdxml/"
    NORMATIVE_XML_FILES = [
        "ucd.all.flat.zip",             # 2009-09-28 19:35  6.6M
        "ucd.all.grouped.zip",          # 2009-09-28 19:35  5.6M
        "ucd.nounihan.flat.zip",        # 2009-09-28 19:35  563K
        "ucd.nounihan.grouped.zip",     # 2009-09-28 19:35  359K
        "ucd.unihan.flat.zip",          # 2009-09-28 19:36  5.3M
        "ucd.unihan.grouped.zip",       # 2009-09-28 19:36  5.3M
        "ucdxml.readme.txt",            # 2009-09-28 19:36  5.3M
        "ucd.unihan.grouped.zip",       # 2009-09-28 19:38  1.0K
    ]

    NORMATIVE_CSV_FILES = [
        "ArabicShaping.txt",        # 2009-08-17 13:39  13K
        "BidiMirroring.txt",        # 2009-05-22 15:10  23K
        "BidiTest.txt",             # 2009-06-03 12:17  3.2M
        "Blocks.txt",               # 2009-05-19 18:24  6.6K
        "CJKRadicals.txt",          # 2009-05-28 13:52  4.7K
        "CaseFolding.txt",          # 2009-05-28 18:25  63K
        "CompositionExclusions.txt",# 2009-05-22 15:10  7.9K
        "DerivedAge.txt",           # 2009-09-21 14:01  71K
        "DerivedCoreProperties.txt",# 2009-08-26 12:39  752K
        "DerivedNormalizationProps.txt",# 2009-08-31 14:48  737K
        "EastAsianWidth.txt",       # 2009-06-09 19:49  779K
        "HangulSyllableType.txt",   # 2009-05-22 18:28  50K
        "Index.txt",                # 2009-07-09 13:56  148K
        "Jamo.txt",                 # 2009-05-22 15:10  3.2K
        "LineBreak.txt",            # 2009-08-17 14:24  835K
        "NameAliases.txt",          # 2009-05-22 15:10  1.1K
        "NamedSequences.txt",       # 2009-09-14 14:50  15K
        "NamedSequencesProv.txt",   # 2009-09-14 14:50  2.5K
        "NamesList.html",           # 2009-09-15 17:01  21K
        "NamesList.txt",            # 2009-09-04 12:28  1.0M
        "NormalizationCorrections.txt", # 2009-05-22 16:07  2.0K
        "NormalizationTest.txt",    # 2009-08-24 16:03  2.2M
        "PropList.txt",             # 2009-08-24 16:02  90K
        "PropertyAliases.txt",      # 2009-08-24 19:00  5.9K
        "PropertyValueAliases.txt", # 2009-08-24 19:00  36K
        "ReadMe.txt",               # 2009-09-30 18:33  410
        "Scripts.txt",              # 2009-08-24 16:03  119K
        "SpecialCasing.txt",        # 2009-09-22 20:05  16K
        "StandardizedVariants.html",# 2009-09-28 18:25  33K
        "StandardizedVariants.txt", # 2008-09-18 19:45  7.5K
        "UnicodeData.txt",          # 2009-08-17 13:38  1.2M
        "Unihan.zip",               # 2009-08-31 15:58  5.9M
    ]

    EXPECTEDFIELDS = 15
    #FILENAME = "ucd.nounihan.flat.xml"
    #FILENAME2 = "ucd.unihan.flat.xml"
    _TYPES = [ ]

    def __init__(self):
        """Load and provide access to the Unicode database.
        A lot of the data is in Python lib unicodedata, but not all, afaict.
        The official site provides the data in XML and in a CSV-ish form using
        ";" delimiters, "#" comments, and special meaning for indented lines.
        I'm going with the XML.

        https://www.unicode.org/Public/5.2.0/ucdxml/
        https://www.unicode.org/reports/tr44/
        """
        self.version = None
        self.charEntries = {}

    def readUdbXml(self, path:str):
        #FILENAME = "ucd.nounihan.flat.xml"
        #FILENAME2 = "ucd.unihan.flat.xml"
        _TYPES = [ ]
        #charEntries = {}

        lastCpInt = 0
        docEl = xml.dom.minidom.parse(path)
        for groupEl in docEl.eachElement("group"):
            groupProperties = {}
            for aname, avalue in groupEl.attributes.items():
                assert aname in UnicodeProperties
                groupProperties[aname] = avalue
            groupObj = UdbEntry(groupProperties)
            assert "cp" not in groupObj

            for charEl in groupEl.childNodes:
                # TODO: stash name-alias child elements?
                if (charEl.nodeName != "char"): continue
                charProperties = groupProperties.copy()
                for aname, avalue in charEl.attributes.items():
                    assert aname in UnicodeProperties
                    charProperties[aname] = avalue
                cpInt = int(charProperties["cp"], 16)
                assert cpInt > lastCpInt
                lastCpInt = cpInt
                self.charEntries[cpInt] = UdbEntry(charProperties)

    def readUdbTextish(self, path:str):
        #charEntries = {}
        ufh = codecs.open(path, "rb", encoding="utf-8")
        lastN = 0
        recnum = 0
        for recnum, rec in enumerate(ufh.readlines()):
            if (rec[0] in "@#"): continue
            assert rec.isascii(), "UnicodeData not all ASCII"
            if rec.strip() == "": continue
            fields = rec.split(";")
            if (len(fields) != UnicodeDBAccess.EXPECTEDFIELDS):
                log(0, "Record %d: expected %d fields but found %d: '%s'\n" %
                    (recnum, UnicodeDBAccess.EXPECTEDFIELDS, len(fields), rec))
                continue
            n = int(fields[0], 16)
            assert n > lastN
            lastN = n
            self.charEntries[n] = UdbEntry(fields)
        return recnum


###############################################################################
# Shorthand used by classes Sebastian and CharInfo
#
class InfoValues(Enum):
    P = "Property"
    F = "Format"
    f = "Limited-scope format"
    C = "Calculable"
    c = "Calculable via library"
    X = "None"
    S = "In Sebastian file"

P = InfoValues.P
F = InfoValues.F
f = InfoValues.f
C = InfoValues.C
c = InfoValues.c
X = InfoValues.X
S = InfoValues.S


###############################################################################
#
class CharInfo:
    """Store, look up, calculate, and return various properties of a char.
    These are my own names, and combine Unicode intrinsic properties, with
    ways you might want to see them (for example, the code point itself
    is available in various based, the literal in UTF-8, etc.)
    """
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

    def __init__(self, wh):
        self.ERROR = None
        if (isinstance(wh, int)):
            self.n = wh
            self.c = chr(wh)
        else:
            self.c = wh
            self.n = ord(wh)
        self.setCharInfo()

    def setProp(self, k, value):
        if (k not in CharInfo.__infoItems__ and
            (sebastian and k not in charNameConvert.propNames)):
            raise KeyError("Unknown character property '%s'." % (k))
        setattr(self, k, value)

    def getitem(self, k):
        if (k not in CharInfo.__infoItems__ and
            (sebastian and k not in charNameConvert.propNames)):
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
        if (pnum == 0):    pname = "Basic Multilingual"
        elif (pnum == 1):  pname = "Supplementary Multilingual"
        elif (pnum == 2):  pname = "Supplementary Ideographic"
        elif (pnum == 16): pname = "Supplementary Private Use Area B"
        elif (pnum == 15): pname = "Supplementary Private Use Area A"
        elif (pnum == 14): pname = "Supplementary Special-purpose"
        elif (pnum >= 3):  pname = "Unassigned"
        else: pname = "-UNKNOWN-"
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
        nam = codePointToDatum(self.n, "entNamed")
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
        """Gather a lot of info about the given code point, and store
        in self.xxxx
        See https://docs.python.org/2/library/unicodedata.html
        """
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
        # TODO: Add XIDENTSTART, XIDENTCONTINUE
        self.ISFPI = CharDisplay.okInFPI(self.n)
        self.ISURI = CharDisplay.okInURI(self.n)
        self.ISBIDI = unicodedata.bidirectional(self.c)
        self.COMBINING = unicodedata.combining(self.c)
        self.EAWIDTH = unicodedata.east_asian_width(self.c)
        self.ISMIRROR = unicodedata.mirrored(self.c)
        # TODO: Add MIRROROF

        self.DECOMP = unicodedata.decomposition(self.c)
        self.NFC = unicodedata.normalize("NFC",  self.c)
        self.NFKC = unicodedata.normalize("NFKC", self.c)
        self.NFD = unicodedata.normalize("NFD",  self.c)
        self.NFKD = unicodedata.normalize("NFKD", self.c)

        return charInfo


###############################################################################
# Define single-character mnemonics to support in format-strings.
# For example, indicate that the literal character is to be insierted with "%l".
# You can also say %{LITERAL}, though.
#
__mnemonicMap__ = {
    "l": "LITERAL",
    "0": "SLASH0",
    "2": "SLASH2",
    "4": "SLASH4",
    "8": "SLASH8",

    # Capitals are the same as lowers here, but "packaged" as XML entities".
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
    ( "umlaut",       "uml",      chr(0x0308), r"\"", r'{\"A}' ),
    ( "ring above",   "ring",     chr(0x030A), r"r ", r"{\r A}" ),
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
    ec = html.unescape(eref)
    if (len(ec) != 1): raise KeyError()
    decomp = unicodedata.normalize("NFKD", ec)
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
    elif (what == "SLASH2"):               # \\xe2
        if (codePoint <= 0xFF): return "\\x%02x" % (codePoint)
        return codePoint
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
            "--help-codes", "--list-codes", action="store_true",
            help="Display a list of %%-codes and names, and exit.")
        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
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
    verbose = args.verbose

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
