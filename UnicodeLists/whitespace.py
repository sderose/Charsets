# Unicode whitespace characters.
# Each is assigned a tuple of (nominal width, flags, name)
# Widths are only approximate, taking an "em" as basically 1.0.
# The flags are:
#     ?  -- The nominal width is not really applicable (e.g., for vertical tab)
#     ^  -- This is a vertical thing
#
#pylint: disable=C0301

USpaces = {
    # Unicode  width flags  name
    0x00009:  ( 1.00, "?",  "CHARACTER TABULATION"),
    0x0000A:  ( 0.00, "^?", "LINE FEED"),
    0x0000B:  ( 1.00, "?",  "LINE TABULATION"),
    0x0000C:  ( 0.00, "^?", "FORM FEED"),
    0x0000D:  ( 0.00, "?",  "CARRIAGE RETURN"),
    0x00020:  ( 1.00, "",   "SPACE"),
    # WARNING: In CP1252 \\x89 is per mille symbol (U+2030)
    0x00089:  ( 1.00, "?",  "CHARACTER TABULATION WITH JUSTIFICATION"),
    #
    0x01680:  ( 1.00, "",   "OGHAM SPACE MARK"),
    0x0180E:  ( 1.00, "?",  "MONGOLIAN VOWEL SEPARATOR"),
    0x02000:  ( 0.50, "",   "EN QUAD"),
    0x02001:  ( 1.00, "",   "EM QUAD"),
    0x02002:  ( 0.50, "",   "EN SPACE"),
    0x02003:  ( 1.00, "",   "EM SPACE"),
    0x02004:  ( 0.33, "",   "THREE-PER-EM SPACE"),
    0x02005:  ( 0.25, "",   "FOUR-PER-EM SPACE"),
    0x02006:  ( 0.17, "",   "SIX-PER-EM SPACE"),
    0x02007:  ( 1.00, "",   "FIGURE SPACE"),
    0x02008:  ( 1.00, "",   "PUNCTUATION SPACE"),
    0x02009:  ( 0.00, "",   "THIN SPACE"),
    0x0200A:  ( 0.10, "",   "HAIR SPACE"),
    0x02028:  ( 0.00, "^?", "LINE SEPARATOR"),
    0x02029:  ( 0.00, "^?", "PARAGRAPH SEPARATOR"),
    0x0200B:  ( 0.00, "",   "ZERO WIDTH SPACE"),
    0x0202F:  ( 0.10, "",   "NARROW NO-BREAK SPACE"),
    0x0205F:  ( 1.00, "",   "MEDIUM MATHEMATICAL SPACE"),
    0x02060:  ( 1.00, "",   "WORD JOINER"),
    0x03000:  ( 1.00, "",   "IDEOGRAPHIC SPACE"),
    0x0303F:  ( 1.00, "",   "IDEOGRAPHIC HALF FILL SPACE"),
    0x0FeFF:  ( 0.00, "",   "ZERO WIDTH NO-BREAK SPACE"),  # aka BOM

    ### Weird/edge cases
    #
    #0x00008:  ( -1.00, "",  "BACKSPACE"),
    #0x000FF:  ( -1.00, "",  "LATIN SMALL LETTER Y WITH DIAERESIS"), ## old DEL
    #0x000A0:  ( -1.00, "",  "NO-BREAK SPACE"
    #
    # Symbols for whitespace control chars (class So).
    #0x02420:  ( 1.00, "",   "SYMBOL FOR SPACE"
    #0x02408:  ( 1.00, "",   "SYMBOL FOR BACKSPACE"
    #0x02409:  ( 1.00, "",   "SYMBOL FOR HORIZONTAL TABULATION"
    #0x0240a:  ( 1.00, "",   "SYMBOL FOR LINE FEED"
    #0x0240b:  ( 1.00, "",   "SYMBOL FOR VERTICAL TABULATION"
    #0x0240c:  ( 1.00, "",   "SYMBOL FOR FORM FEED"
    #0x0240d:  ( 1.00, "",   "SYMBOL FOR CARRIAGE RETURN"
    #0x02422:  ( 1.00, "",   "BLANK SYMBOL"
    #0x02423:  ( 1.00, "",   "OPEN BOX"
    #0x02424:  ( 1.00, "",   "SYMBOL FOR NEWLINE"
}


# Much more detailed information follows, saying which characters are in which
# categories, for a number of specs and languages.
# See also:
#     http://unicode.org/L2/L2003/03139-posix-classes.htm
#     https://docs.python.org/3.11/library/stdtypes.html?highlight=str%20strip#str.strip
#     https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap07.html
# TODO:
#     Determine the UNK ones
#     Add locale "en_US.UTF-8" columns
#
key = [
    ( "BL",    "Posix locale [:blank:]" ),
    ( "SP",    "Posix locale [:space:]" ),
    ( "WS",    "Unicode white_space" ),
    ( "Z",     "Unicode category Z" ),
    ( "ST",    "Does Python strip() strip it?" ),
    ( "(S)",   "Actual result from strip()" ),       # not in tuples
    ( "BK",    "Unicode is breaking space" ),
    ( "RE",    "Matched by Python re \\s" ),         # not in tuples
    ( "IS",    "Recognized by Python isspace()" ),   # not in tuples
    ( "PL",    "Recognized by Perl re \\s" ),        # not in tuples
    ( "NAME",  "Unicode formal character name" ),
]

INWS = INZ = INSTRIP = INBREAK = INBL = INSP = INPL = 1
NOWS = NOZ = NOSTRIP = NOBREAK = NOBL = NOSP = NOPL = 0
UNK = "?"

possibles = {
    # cdpoint     0     1     2    3        4        5    6   7
    #  CHAR      BL    SP    WS    Z       ST       BK    PL  NAME
    "\u0008": (NOBL, NOSP, NOWS, NOZ, NOSTRIP,     UNK, NOPL, "<BACKSPACE>"),
    "\u0009": (INBL, INSP, INWS, NOZ, INSTRIP, INBREAK, INPL, "<CHARACTER TABULATION (NOBL, NOSP, HT)>"),
    "\u000A": (NOBL, INSP, INWS, NOZ, INSTRIP, INBREAK, INPL, "<LINE FEED (NOBL, NOSP, LF)>"),
    "\u000B": (NOBL, INSP, INWS, NOZ, INSTRIP, INBREAK, INPL, "<LINE TABULATION (NOBL, NOSP, VT)>"),
    "\u000C": (NOBL, INSP, INWS, NOZ, INSTRIP, INBREAK, INPL, "<FORM FEED (NOBL, NOSP, FF)>"),
    "\u000D": (NOBL, INSP, INWS, NOZ, INSTRIP, INBREAK, INPL, "<CARRIAGE RETURN (NOBL, NOSP, CR)>"),
    "\u001c": (NOBL, NOSP, NOWS, NOZ, NOSTRIP,     UNK, NOPL, "INFORMATION SEPARATOR FOUR"),
    "\u001d": (NOBL, NOSP, NOWS, NOZ, NOSTRIP,     UNK, NOPL, "INFORMATION SEPARATOR THREE"),
    "\u001e": (NOBL, NOSP, NOWS, NOZ, NOSTRIP,     UNK, NOPL, "INFORMATION SEPARATOR TWO"),
    "\u001f": (NOBL, NOSP, NOWS, NOZ, NOSTRIP,     UNK, NOPL, "INFORMATION SEPARATOR ONE"),
    "\u0020": (INBL, INSP, INWS, INZ, INSTRIP, INBREAK, INPL, "SPACE"),
    # C1 controls
    "\u0085": (NOBL, NOSP, INWS, NOZ, INSTRIP, INBREAK, NOPL, "<NEXT LINE (NOBL, NOSP, NEL)>"),
    "\u0089": ( UNK,  UNK,  UNK, UNK,     UNK,     UNK,  UNK, "CHARACTER TABULATION WITH JUSTIFICATION"),
    "\u00A0": (NOBL, NOSP, INWS, INZ, INSTRIP, NOBREAK, NOPL, "NO-BREAK SPACE"),
    # BMP past Latin-1
    "\u1361": (NOBL, NOSP, NOWS, NOZ, NOSTRIP, INBREAK, NOPL, "ETHIOPIC WORDSPACE"),
    "\u1680": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "OGHAM SPACE MARK"),
    "\u180E": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, NOPL, "MONGOLIAN VOWEL SEPARATOR"),
    "\u2000": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "EN QUAD"),
    "\u2001": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "EM QUAD"),
    "\u2002": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "EN SPACE"),
    "\u2003": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "EM SPACE"),
    "\u2004": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "THREE-PER-EM SPACE"),
    "\u2005": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "FOUR-PER-EM SPACE"),
    "\u2006": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "SIX-PER-EM SPACE"),
    "\u2007": (NOBL, NOSP, INWS, INZ, INSTRIP, NOBREAK, INPL, "FIGURE SPACE"),
    "\u2008": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "PUNCTUATION SPACE"),
    "\u2009": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "THIN SPACE"),
    "\u200A": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "HAIR SPACE"),
    "\u200B": (NOBL, NOSP, NOWS, INZ, INSTRIP, INBREAK, NOPL, "ZERO WIDTH SPACE"),
    "\u2028": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "LINE SEPARATOR"),
    "\u2029": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "PARAGRAPH SEPARATOR"),
    "\u202F": (NOBL, NOSP, INWS, INZ, INSTRIP, NOBREAK, INPL, "NARROW NO-BREAK SPACE"),
    "\u205F": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "MEDIUM MATHEMATICAL SPACE"),
    "\u2060": ( UNK,  UNK,  UNK, UNK,     UNK,     UNK,  UNK, "WORD JOINER"),
    "\u2408": (NOBL, NOSP, NOWS, NOZ, NOSTRIP, INBREAK, NOPL, "SYMBOL FOR BACKSPACE"),
    "\u2420": (NOBL, NOSP, NOWS, NOZ, NOSTRIP, INBREAK, NOPL, "SYMBOL FOR SPACE"),
    "\u3000": (NOBL, NOSP, INWS, INZ, INSTRIP, INBREAK, INPL, "IDEOGRAPHIC SPACE"),
    "\u303f": (NOBL, NOSP, NOWS, NOZ, NOSTRIP, INBREAK, NOPL, "IDEOGRAPHIC HALF FILL SPACE"),
    "\ufeff": (NOBL, NOSP, NOWS, NOZ, NOSTRIP, INBREAK, NOPL, "ZERO WIDTH NO-BREAK SPACE"),
}
