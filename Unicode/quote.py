    # chttp://www.fileformat.info/info/unicode/category/Pi/list.htm
    # Cf 'ord --find QUOTATION'

    ###########################################################################
    ### See findUnbalancedQuotes.py for these organized in pairs.
    ###########################################################################

    #Punctuation_Initial
    #
    ULQuotes = {
        0x00AB:  "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        0x2018:  "LEFT SINGLE QUOTATION MARK",
        0x201A:  "SINGLE LOW-9 QUOTATION MARK",
        0x201C:  "LEFT DOUBLE QUOTATION MARK",
        0x201E:  "DOUBLE LOW-9 QUOTATION MARK",
        0x2039:  "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        0x2E02:  "LEFT SUBSTITUTION BRACKET",
        0x2E04:  "LEFT DOTTED SUBSTITUTION BRACKET",
        0x2E09:  "LEFT TRANSPOSITION BRACKET",
        0x2E0C:  "LEFT RAISED OMISSION BRACKET",
        0x2E1C:  "LEFT LOW PARAPHRASE BRACKET",
        0x2E20:  "LEFT VERTICAL BAR WITH QUILL",
    }

    #Punctuation_Final
    #
    URQuotes = {
        0x00BB:  "RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        0x2019:  "RIGHT SINGLE QUOTATION MARK",
        0x201B:  "SINGLE HIGH-REVERSED-9 QUOTATION MARK",
        0x201D:  "RIGHT DOUBLE QUOTATION MARK",
        0x201F:  "DOUBLE HIGH-REVERSED-9 QUOTATION MARK",
        0x203A:  "SINGLE RIGHT-POINTING ANGLE QUOTATION MARK",
        0x2358:  "APL FUNCTIONAL SYMBOL QUOTE UNDERBAR",
        0x235E:  "APL FUNCTIONAL SYMBOL QUOTE QUAD",
        0x2E03:  "RIGHT SUBSTITUTION BRACKET",
        0x2E05:  "RIGHT DOTTED SUBSTITUTION BRACKET",
        0x2E0A:  "RIGHT TRANSPOSITION BRACKET",
        0x2E0D:  "RIGHT RAISED OMISSION BRACKET",
        0x2E1D:  "RIGHT LOW PARAPHRASE BRACKET",
        0x2E21:  "RIGHT VERTICAL BAR WITH QUILL",
    }

    qPairs = [
        [ "'",    "'" ],     # Apostrophe / single quotation mark
        [ '"',    '"' ],     # Double quotation mark
        # [ 0x0FF02, 0x0FF02 ],  # Fullwidth Quotation Mark
        # [ 0x301E, 0x301E ],  # "DOUBLE PRIME QUOTATION MARK",
        [ 0x00AB, 0x00BB ],  # "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        [ 0x2018, 0x2019 ],  # "LEFT SINGLE QUOTATION MARK",
        [ 0x201A, 0x201B ],  # "SINGLE LOW-9 QUOTATION MARK",
        [ 0x201C, 0x201D ],  # "LEFT DOUBLE QUOTATION MARK",
        [ 0x201E, 0x201F ],  # "DOUBLE LOW-9 QUOTATION MARK",
        [ 0x2039, 0x203A ],  # "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        [ 0x2E02, 0x2E03 ],  # "LEFT SUBSTITUTION BRACKET",
        [ 0x2E04, 0x2E05 ],  # "LEFT DOTTED SUBSTITUTION BRACKET",
        [ 0x2E09, 0x2E0A ],  # "LEFT TRANSPOSITION BRACKET",
        [ 0x2E0C, 0x2E0D ],  # "LEFT RAISED OMISSION BRACKET",
        [ 0x2E1C, 0x2E1D ],  # "LEFT LOW PARAPHRASE BRACKET",
        [ 0x2E20, 0x2E21 ],  # "LEFT VERTICAL BAR WITH QUILL",
        [ 0x301D, 0x301F ],  # "REVERSED DOUBLE PRIME QUOTATION MARK",
        [ 0x2032, 0x2035 ],  # "PRIME", "REVERSED PRIME",
        [ 0x2034, 0x2037 ],  # "TRIPLE PRIME", "REVERSED TRIPLE PRIME",
        [ 0x2057, 0x301D ],  # "QUADRUPLE PRIME", "REVERSED DOUBLE PRIME QUOTATION MARK",
        [ 0x0275B, 0x0275C ],  # Heavy Single Turned Comma Quotation Mark Ornament
        [ 0x0275D, 0x0275E ],  # Heavy Double Turned Comma Quotation Mark Ornament
        [ 0x0276E, 0x0276F ],  # Heavy Left-pointing Angle Quotation Mark Ornament
        [ 0x1F677, 0x1F678 ],  # Sans-serif Heavy Double Comma Quotation Mark Ornament
    ]


# Not in:  "the Unicode categories, but perhaps relevant:
    UOtherQuotes = {
        0x0060:  "GRAVE ACCENT",

        0x201A:  "SINGLE LOW-9 QUOTATION MARK",
        0x201E:  "DOUBLE LOW-9 QUOTATION MARK",

        0x275B:  "HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT",
        0x275C:  "HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT",
        0x275D:  "HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT",
        0x275E:  "HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT",
        0x276E:  "HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT",
        0x276F:  "HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT",

        0x2032:  "PRIME",
        0x2035:  "REVERSED PRIME",
        0x2034:  "TRIPLE PRIME",
        0x2037:  "REVERSED TRIPLE PRIME",
        0x2057:  "QUADRUPLE PRIME",
        0x301D:  "REVERSED DOUBLE PRIME QUOTATION MARK",
        0x301E:  "DOUBLE PRIME QUOTATION MARK",
        0x301F:  "LOW DOUBLE PRIME QUOTATION MARK",

        0x0027:  "APOSTROPHE",
        0x0149:  "LATIN SMALL LETTER N PRECEDED BY APOSTROPHE",
        0x02bc:  "MODIFIER LETTER APOSTROPHE",
        0x02ee:  "MODIFIER LETTER DOUBLE APOSTROPHE",
        0x055a:  "ARMENIAN APOSTROPHE",
        0x07f4:  "NKO HIGH TONE APOSTROPHE",
        0x07f5:  "NKO LOW TONE APOSTROPHE",
        0xff07:  "FULLWIDTH APOSTROPHE",
    }


































