# Unicode whitespace characters.
# Each is assigned a tuple of (nominal width, flags, name)
# Widths are only approximate, taking an "em" as basically 1.0.
# The flags are:
#     ?  -- The nominal width is not really applicable (e.g., for vertical tab)
#     ^  -- This is a vertical thing
#
USpaces = {
    # Unicode   width  name
    0x00009:  ( 1.00, "?",  "CHARACTER TABULATION"),
    0x0000A:  ( 0.00, "^?", "LINE FEED"),
    0x0000B:  ( 1.00, "?",  "LINE TABULATION"),
    0x0000C:  ( 0.00, "^?", "FORM FEED"),
    0x0000D:  ( 0.00, "?",  "CARRIAGE RETURN"),
    0x00020:  ( 1.00, "",   "SPACE"),
    0x00089:  ( 1.00, "?",  "CHARACTER TABULATION WITH JUSTIFICATION"),  # Not in Perl \s
    0x000A0:  ( 1.00, "",   "NO-BREAK SPACE"),              # Not in Perl \s
    0x01680:  ( 1.00, "",   "OGHAM SPACE MARK"),
    0x0180E:  ( 1.00, "?",  "MONGOLIAN VOWEL SEPARATOR"),   # In Perl \s
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
    0x02028:  ( 0.00, "^?", "LINE SEPARATOR"),              # In Perl \s
    0x02029:  ( 0.00, "^?", "PARAGRAPH SEPARATOR"),         # In Perl \s
    0x0200B:  ( 0.00, "",   "ZERO WIDTH SPACE"),            # Not in Perl \s
    0x0202F:  ( 0.10, "",   "NARROW NO-BREAK SPACE"),
    0x0205F:  ( 1.00, "",   "MEDIUM MATHEMATICAL SPACE"),
    0x03000:  ( 1.00, "",   "IDEOGRAPHIC SPACE"),
    0x0303F:  ( 1.00, "",   "IDEOGRAPHIC HALF FILL SPACE"), # Not in Perl \s

    # This isn't really a "space"....
    0x02420:  ( 1.00, "",   "SYMBOL FOR SPACE"),            # Not in Perl \s
}
