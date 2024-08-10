# Python form for info on old MacRoman character set.
# See also other forms such as Perl and XSV data.
# From 'chr' by Steven J. DeRose, as of 2015-09-15.
#
# Keyed by MacRoman hex code point. Value is a tuple of:
#     Corresponding Unicode hex code point
#     HTML entity name
#     Unicode character name (in mixed case)
#
macRomanData = {
    0x80: ( 0x00C4, "Auml",    "Latin capital letter A with diaeresis" ),
    0x81: ( 0x00C5, "Aring",   "Latin capital letter A with ring above" ),
    0x82: ( 0x00C7, "Ccedil",  "Latin capital letter C with cedilla" ),
    0x83: ( 0x00C9, "Eacute",  "Latin capital letter E with acute" ),
    0x84: ( 0x00D1, "Ntilde",  "Latin capital letter N with tilde" ),
    0x85: ( 0x00D6, "Ouml",    "Latin capital letter O with diaeresis" ),
    0x86: ( 0x00DC, "Uuml",    "Latin capital letter U with diaeresis" ),
    0x87: ( 0x00E1, "aacute",  "Latin small letter a with acute" ),
    0x88: ( 0x00E0, "agrave",  "Latin small letter a with grave" ),
    0x89: ( 0x00E2, "acirc",   "Latin small letter a with circumflex" ),
    0x8A: ( 0x00E4, "auml",    "Latin small letter a with diaeresis" ),
    0x8B: ( 0x00E3, "atilde",  "Latin small letter a with tilde" ),
    0x8C: ( 0x00E5, "aring",   "Latin small letter a with ring above" ),
    0x8D: ( 0x00E7, "ccedil",  "Latin small letter c with cedilla" ),
    0x8E: ( 0x00E9, "eacute",  "Latin small letter e with acute" ),
    0x8F: ( 0x00E8, "egrave",  "Latin small letter e with grave" ),
    0x90: ( 0x00EA, "ecirc",   "Latin small letter e with circumflex" ),
    0x91: ( 0x00EB, "euml",    "Latin small letter e with diaeresis" ),
    0x92: ( 0x00ED, "iacute",  "Latin small letter i with acute" ),
    0x93: ( 0x00EC, "igrave",  "Latin small letter i with grave" ),
    0x94: ( 0x00EE, "icirc",   "Latin small letter i with circumflex" ),
    0x95: ( 0x00EF, "iuml",    "Latin small letter i with diaeresis" ),
    0x96: ( 0x00F1, "ntilde",  "Latin small letter n with tilde" ),
    0x97: ( 0x00F3, "oacute",  "Latin small letter o with acute" ),
    0x98: ( 0x00F2, "ograve",  "Latin small letter o with grave" ),
    0x99: ( 0x00F4, "ocirc",   "Latin small letter o with circumflex" ),
    0x9A: ( 0x00F6, "ouml",    "Latin small letter o with diaeresis" ),
    0x9B: ( 0x00F5, "otilde",  "Latin small letter o with tilde" ),
    0x9C: ( 0x00FA, "uacute",  "Latin small letter u with acute" ),
    0x9D: ( 0x00F9, "ugrave",  "Latin small letter u with grave" ),
    0x9E: ( 0x00FB, "ucirc",   "Latin small letter u with circumflex" ),
    0x9F: ( 0x00FC, "uuml",    "Latin small letter u with diaeresis" ),
    0xA0: ( 0x2020, "dagger",  "dagger" ),
    0xA1: ( 0x00B0, "deg",     "degree sign" ),
    0xA2: ( 0x00A2, "cent",    "cent sign" ),
    0xA3: ( 0x00A3, "pound",   "pound sign" ),
    0xA4: ( 0x00A7, "sect",    "section sign" ),
    0xA5: ( 0x2022, "bull",    "bullet" ),
    0xA6: ( 0x00B6, "para",    "pilcrow sign" ),
    0xA7: ( 0x00DF, "szlig",   "Latin small letter sharp s" ),
    0xA8: ( 0x00AE, "reg",     "registered sign" ),
    0xA9: ( 0x00A9, "copy",    "copyright sign" ),
    0xAA: ( 0x2122, "trade",   "trade mark sign" ),
    0xAB: ( 0x00B4, "acute",   "acute accent" ),
    0xAC: ( 0x00A8, "uml",     "diaeresis" ),
    0xAD: ( 0x2260, "ne",      "not equal to" ),
    0xAE: ( 0x00C6, "AElig",   "Latin capital letter AE" ),
    0xAF: ( 0x00D8, "Oslash",  "Latin capital letter O with stroke" ),
    0xB0: ( 0x221E, "infin",   "infinity" ),
    0xB1: ( 0x00B1, "plusmn",  "plus-minus sign" ),
    0xB2: ( 0x2264, "le",      "less-than or equal to" ),
    0xB3: ( 0x2265, "ge",      "greater-than or equal to" ),
    0xB4: ( 0x00A5, "yen",     "yen sign" ),
    0xB5: ( 0x00B5, "micro",   "micro sign" ),
    0xB6: ( 0x2202, "part",    "partial differential" ),
    0xB7: ( 0x2211, "sum",     "n-ary summation" ),
    0xB8: ( 0x220F, "prod",    "n-ary product" ),
    0xB9: ( 0x03C0, "pi",      "Greek small letter pi" ),
    0xBA: ( 0x222B, "int",     "integral" ),
    0xBB: ( 0x00AA, "ordf",    "feminine ordinal indicator" ),
    0xBC: ( 0x00BA, "ordm",    "masculine ordinal indicator" ),
    0xBD: ( 0x03A9, "Omega",   "Greek capital letter Omega" ),
    0xBE: ( 0x00E6, "aelig",   "Latin small letter ae" ),
    0xBF: ( 0x00F8, "oslash",  "Latin small letter o with stroke" ),
    0xC0: ( 0x00BF, "iquest",  "inverted question mark" ),
    0xC1: ( 0x00A1, "iexcl",   "inverted exclamation mark" ),
    0xC2: ( 0x00AC, "not",     "not sign" ),
    0xC3: ( 0x221A, "radic",   "square root" ),
    0xC4: ( 0x0192, "fnof",    "Latin small letter f with hook" ),
    0xC5: ( 0x2248, "asymp",   "almost equal to" ),
    0xC6: ( 0x2206, None,      "increment" ),  ### No entity
    0xC7: ( 0x00AB, "laquo",   "left-pointing double angle quotation mark" ),
    0xC8: ( 0x00BB, "raquo",   "right-pointing double angle quotation mark" ),
    0xC9: ( 0x2026, "hellip",  "horizontal ellipsis" ),
    0xCA: ( 0x00A0, "nbsp",    "no-break space" ),
    0xCB: ( 0x00C0, "Agrave",  "Latin capital letter A with grave" ),
    0xCC: ( 0x00C3, "Atilde",  "Latin capital letter A with tilde" ),
    0xCD: ( 0x00D5, "Otilde",  "Latin capital letter O with tilde" ),
    0xCE: ( 0x0152, "OElig",   "Latin capital ligature OE" ),
    0xCF: ( 0x0153, "oelig",   "Latin small ligature oe" ),
    0xD0: ( 0x2013, "ndash",   "en dash" ),
    0xD1: ( 0x2014, "mdash",   "em dash" ),
    0xD2: ( 0x201C, "ldquo",   "left double quotation mark" ),
    0xD3: ( 0x201D, "rdquo",   "right double quotation mark" ),
    0xD4: ( 0x2018, "lsquo",   "left single quotation mark" ),
    0xD5: ( 0x2019, "rsquo",   "right single quotation mark" ),
    0xD6: ( 0x00F7, "divide",  "division sign" ),
    0xD7: ( 0x25CA, "loz",     "lozenge" ),
    0xD8: ( 0x00FF, "yuml",    "Latin small letter y with diaeresis" ),
    0xD9: ( 0x0178, "Yuml",    "Latin capital letter Y with diaeresis" ),
    0xDA: ( 0x2044, "frasl",   "fraction slash" ),
    0xDB: ( 0x20AC, "euro",    "euro sign" ),
    0xDC: ( 0x2039, "lsaquo",  "single left-pointing angle quotation mark" ),
    0xDD: ( 0x203A, "rsaquo",  "single right-pointing angle quotation mark" ),
    0xDE: ( 0xFB01, None,      "Latin small ligature fi" ),  ### No entity
    0xDF: ( 0xFB02, None,      "Latin small ligature fl" ),  ### No entity
    0xE0: ( 0x2021, "Dagger",  "double dagger" ),
    0xE1: ( 0x00B7, "middot",  "middle dot" ),
    0xE2: ( 0x201A, "sbquo",   "single low-9 quotation mark" ),
    0xE3: ( 0x201E, "bdquo",   "double low-9 quotation mark" ),
    0xE4: ( 0x2030, "permil",  "per mille sign" ),
    0xE5: ( 0x00C2, "Acirc",   "Latin capital letter A with circumflex" ),
    0xE6: ( 0x00CA, "Ecirc",   "Latin capital letter E with circumflex" ),
    0xE7: ( 0x00C1, "Aacute",  "Latin capital letter A with acute" ),
    0xE8: ( 0x00CB, "Euml",    "Latin capital letter E with diaeresis" ),
    0xE9: ( 0x00C8, "Egrave",  "Latin capital letter E with grave" ),
    0xEA: ( 0x00CD, "Iacute",  "Latin capital letter I with acute" ),
    0xEB: ( 0x00CE, "Icirc",   "Latin capital letter I with circumflex" ),
    0xEC: ( 0x00CF, "Iuml",    "Latin capital letter I with diaeresis" ),
    0xED: ( 0x00CC, "Igrave",  "Latin capital letter I with grave" ),
    0xEE: ( 0x00D3, "Oacute",  "Latin capital letter O with acute" ),
    0xEF: ( 0x00D4, "Ocirc",   "Latin capital letter O with circumflex" ),
    0xF0: ( 0xF8FF, None,      "Apple logo" ),  ### No entity
    0xF1: ( 0x00D2, "Ograve",  "Latin capital letter O with grave" ),
    0xF2: ( 0x00DA, "Uacute",  "Latin capital letter U with acute" ),
    0xF3: ( 0x00DB, "Ucirc",   "Latin capital letter U with circumflex" ),
    0xF4: ( 0x00D9, "Ugrave",  "Latin capital letter U with grave" ),
    0xF5: ( 0x0131, None,      "Latin small letter dotless i" ),  ### No entity
    0xF6: ( 0x02C6, "circ",    "modifier letter circumflex accent" ),
    0xF7: ( 0x02DC, "tilde",   "small tilde" ),
    0xF8: ( 0x00AF, "macr",    "macron" ),
    0xF9: ( 0x02D8, None,      "breve" ),  ### No entity
    0xFA: ( 0x02D9, None,      "dot above" ),  ### No entity
    0xFB: ( 0x02DA, None,      "ring above" ),  ### No entity
    0xFC: ( 0x00B8, "cedil",   "cedilla" ),
    0xFD: ( 0x02DD, None,      "double acute accent" ),  ### No entity
    0xFE: ( 0x02DB, None,      "ogonek" ),  ### No entity
    0xFF: ( 0x02C7, None,      "caron" ),  ### No entity
}