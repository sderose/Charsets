    # chttp://www.fileformat.info/info/unicode/category/Pi/list.htm
    # Cf 'ord --find QUOT'

    ###########################################################################
    ### See findUnbalancedQuotes.py for these organized in pairs.
    ###########################################################################

    #Punctuation_Initial
    #
    ULQuotes = {
        0x000AB:  "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        0x02018:  "LEFT SINGLE QUOTATION MARK",
        0x0201A:  "SINGLE LOW-9 QUOTATION MARK",
        0x0201C:  "LEFT DOUBLE QUOTATION MARK",
        0x0201E:  "DOUBLE LOW-9 QUOTATION MARK",
        0x02039:  "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        0x02E02:  "LEFT SUBSTITUTION BRACKET",
        0x02E04:  "LEFT DOTTED SUBSTITUTION BRACKET",
        0x02E09:  "LEFT TRANSPOSITION BRACKET",
        0x02E0C:  "LEFT RAISED OMISSION BRACKET",
        0x02E1C:  "LEFT LOW PARAPHRASE BRACKET",
        0x02E20:  "LEFT VERTICAL BAR WITH QUILL",
    }

    #Punctuation_Final
    #
    URQuotes = {
        0x000BB:  "RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        0x02019:  "RIGHT SINGLE QUOTATION MARK",
        0x0201B:  "SINGLE HIGH-REVERSED-9 QUOTATION MARK",
        0x0201D:  "RIGHT DOUBLE QUOTATION MARK",
        0x0201F:  "DOUBLE HIGH-REVERSED-9 QUOTATION MARK",
        0x0203A:  "SINGLE RIGHT-POINTING ANGLE QUOTATION MARK",
        0x02358:  "APL FUNCTIONAL SYMBOL QUOTE UNDERBAR",
        0x0235E:  "APL FUNCTIONAL SYMBOL QUOTE QUAD",
        0x02E03:  "RIGHT SUBSTITUTION BRACKET",
        0x02E05:  "RIGHT DOTTED SUBSTITUTION BRACKET",
        0x02E0A:  "RIGHT TRANSPOSITION BRACKET",
        0x02E0D:  "RIGHT RAISED OMISSION BRACKET",
        0x02E1D:  "RIGHT LOW PARAPHRASE BRACKET",
        0x02E21:  "RIGHT VERTICAL BAR WITH QUILL",
    }

    qPairs = [
        [ "'",    "'" ],     # Apostrophe / single quotation mark
        [ '"',    '"' ],     # Double quotation mark
        # [ 0x00FF02, 0x00FF02 ],  # Fullwidth Quotation Mark
        # [ 0x0301E, 0x0301E ],  # "DOUBLE PRIME QUOTATION MARK",
        [ 0x000AB, 0x000BB ],  # "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        [ 0x02018, 0x02019 ],  # "LEFT SINGLE QUOTATION MARK",
        [ 0x0201A, 0x0201B ],  # "SINGLE LOW-9 QUOTATION MARK",
        [ 0x0201C, 0x0201D ],  # "LEFT DOUBLE QUOTATION MARK",
        [ 0x0201E, 0x0201F ],  # "DOUBLE LOW-9 QUOTATION MARK",
        [ 0x02039, 0x0203A ],  # "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        [ 0x02E02, 0x02E03 ],  # "LEFT SUBSTITUTION BRACKET",
        [ 0x02E04, 0x02E05 ],  # "LEFT DOTTED SUBSTITUTION BRACKET",
        [ 0x02E09, 0x02E0A ],  # "LEFT TRANSPOSITION BRACKET",
        [ 0x02E0C, 0x02E0D ],  # "LEFT RAISED OMISSION BRACKET",
        [ 0x02E1C, 0x02E1D ],  # "LEFT LOW PARAPHRASE BRACKET",
        [ 0x02E20, 0x02E21 ],  # "LEFT VERTICAL BAR WITH QUILL",
        [ 0x0301D, 0x0301F ],  # "REVERSED DOUBLE PRIME QUOTATION MARK",
        [ 0x02032, 0x02035 ],  # "PRIME", "REVERSED PRIME",
        [ 0x02034, 0x02037 ],  # "TRIPLE PRIME", "REVERSED TRIPLE PRIME",
        [ 0x02057, 0x0301D ],  # "QUADRUPLE PRIME", "REVERSED DOUBLE PRIME QUOTATION MARK",
        [ 0x00275B, 0x00275C ],  # Heavy Single Turned Comma Quotation Mark Ornament
        [ 0x00275D, 0x00275E ],  # Heavy Double Turned Comma Quotation Mark Ornament
        [ 0x00276E, 0x00276F ],  # Heavy Left-pointing Angle Quotation Mark Ornament
        [ 0x01F677, 0x01F678 ],  # Sans-serif Heavy Double Comma Quotation Mark Ornament
    ]


    # Not in:  "the Unicode categories, but perhaps relevant:
    UOtherQuotes = {
        0x00060:  "GRAVE ACCENT",

        0x0201A:  "SINGLE LOW-9 QUOTATION MARK",
        0x0201E:  "DOUBLE LOW-9 QUOTATION MARK",

        0x0275B:  "HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT",
        0x0275C:  "HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT",
        0x0275D:  "HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT",
        0x0275E:  "HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT",
        0x0276E:  "HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT",
        0x0276F:  "HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT",

        0x02032:  "PRIME",
        0x02035:  "REVERSED PRIME",
        0x02034:  "TRIPLE PRIME",
        0x02037:  "REVERSED TRIPLE PRIME",
        0x02057:  "QUADRUPLE PRIME",
        0x0301D:  "REVERSED DOUBLE PRIME QUOTATION MARK",
        0x0301E:  "DOUBLE PRIME QUOTATION MARK",
        0x0301F:  "LOW DOUBLE PRIME QUOTATION MARK",

        0x00027:  "APOSTROPHE",
        0x00149:  "LATIN SMALL LETTER N PRECEDED BY APOSTROPHE",
        0x002bc:  "MODIFIER LETTER APOSTROPHE",
        0x002ee:  "MODIFIER LETTER DOUBLE APOSTROPHE",
        0x0055a:  "ARMENIAN APOSTROPHE",
        0x007f4:  "NKO HIGH TONE APOSTROPHE",
        0x007f5:  "NKO LOW TONE APOSTROPHE",
        0x0ff07:  "FULLWIDTH APOSTROPHE",
    }


































