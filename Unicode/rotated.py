# Unicode characters that are rotated ("turned") Latin
# See https://stackoverflow.com/questions/2995340/

a = "Z⅄XꤵꓥꓵꓕSꓤÒꓒONꟽ⅂ꓘᒋIΗ⅁ℲƎꓷↃꓭꓯzʎxʍʌnʇsɹbdouɯןʞſ̣ᴉɥɓɟǝpɔqɐ068᠘9૬ҺƐᘔl¡¿؛˙‘‚„⅋"

rotated = [
    # Latin SMALL
    [ 'A',  'ɐ', 0x0250, 'LATIN SMALL LETTER TURNED A' ],
    # b USE q
    # c
    # d USE p
    [ 'E',  'ǝ', 0x01DD, 'LATIN SMALL LETTER TURNED E' ],
    [ 'E',  'ᴈ', 0x1D08, 'LATIN SMALL LETTER TURNED OPEN E' ],
    [ 'F',  'ⅎ', 0x214E, 'TURNED SMALL F' ],
    [ 'G',  'ᵷ', 0x1D77, 'LATIN SMALL LETTER TURNED G' ],
    [ 'H',  'ɥ', 0x0265, 'LATIN SMALL LETTER TURNED H' ],
    [ 'I',  'ᴉ', 0x1D09, 'LATIN SMALL LETTER TURNED I' ],
    # j
    [ 'K',  'ʞ', 0x029E, 'LATIN SMALL LETTER TURNED K' ],
    [ 'L',  'ꞁ', 0xA781, 'LATIN SMALL LETTER TURNED L' ],
    [ 'M',  'ɯ', 0x026F, 'LATIN SMALL LETTER TURNED M' ],
    [ 'M',  'ᴟ', 0x1D1F, 'LATIN SMALL LETTER SIDEWAYS TURNED M' ],
    # n USE u
    # o USE o
    # p USE d
    # q USE b
    [ 'R',  'ɹ', 0x0279, 'LATIN SMALL LETTER TURNED R' ],
    # s USE s
    [ 'T',  'ʇ', 0x0287, 'LATIN SMALL LETTER TURNED T' ],
    # u USE n
    [ 'V',  'ʌ', 0x028C, 'LATIN SMALL LETTER TURNED V' ],
    [ 'W',  'ʍ', 0x028D, 'LATIN SMALL LETTER TURN ED W' ],
    # x USE x
    [ 'Y',  'ʎ', 0x028E, 'LATIN SMALL LETTER TURNED Y' ],
    # z USE z

    # Latin CAPITAL
    [ 'A',  'Ɐ', 0x2C6F, 'LATIN CAPITAL LETTER TURNED A' ],
    # A or USE for all U+2200
    # B
    # C
    # D
    [ 'E',  'ⱻ', 0x2C7B, 'LATIN LETTER SMALL CAPITAL TURNED E' ],
    [ 'F',  'Ⅎ', 0x2132, 'TURNED CAPITAL F' ],
    [ 'G',  '⅁', 0x2141, 'TURNED SANS-SERIF CAPITAL G' ],
    # H USE H
    # I USE I
    # J
    # K
    [ 'L',  'Ꞁ', 0xA780, 'LATIN CAPITAL LETTER TURNED L' ],
    [ 'L',  '⅂', 0x2142, 'TURNED SANS-SERIF CAPITAL L' ],
    [ 'M',  'Ɯ', 0x019C, 'LATIN CAPITAL LETTER TURNED M' ],
    # N USE N
    # O USE O
    # P
    # Q
    [ 'R',  'ᴚ', 0x1D1A, 'LATIN LETTER SMALL CAPITAL TURNED R' ],
    # S USE S
    # T
    # U
    [ 'V',  'Ʌ', 0x0245, 'LATIN CAPITAL LETTER TURNED V' ],
    # W USE M
    # X USE X
    [ 'Y',  '⅄', 0x2144, 'TURNED SANS-SERIF CAPITAL Y' ],
    # Z USE Z

    [ 'D',  '⅋', 0x214B, 'TURNED AMPERSAND' ],
    [ 'N',  '⌙', 0x2319, 'TURNED NOT SIGN' ],
    [ 'E',  '⦢', 0x29A2, 'TURNED ANGLE' ],
    # SELF: #$%*~-=+|\/ PAIR: () [] {} <>
    # $ ? USE U+00BF, ! USE U+00A1

    [ 'H+',  'ʮ', 0x02AE, 'LATIN SMALL LETTER TURNED H WITH FISHHOOK' ],
    [ 'H+',  'ʯ', 0x02AF, 'LATIN SMALL LETTER TURNED H WITH FISHHOOK AND TAIL' ],
    [ 'M+',  'ɰ', 0x0270, 'LATIN SMALL LETTER TURNED M WITH LONG LEG' ],
    [ 'R+',  'ɺ', 0x027A, 'LATIN SMALL LETTER TURNED R WITH LONG LEG' ],
    [ 'R+',  'ɻ', 0x027B, 'LATIN SMALL LETTER TURNED R WITH HOOK' ],
    [ 'R+',  'ⱹ', 0x2C79, 'LATIN SMALL LETTER TURNED R WITH TAIL' ],
    [ 'AE',  'ᴂ', 0x1D02, 'LATIN SMALL LETTER TURNED AE' ],
    [ 'OE',  'ᴔ', 0x1D14, 'LATIN SMALL LETTER TURNED OE' ],

    # Why are these called "Latin"?
    [ 'G+',  'Ꝿ', 0xA77E, 'LATIN CAPITAL LETTER TURNED INSULAR G' ],
    [ 'G+',  'ꝿ', 0xA77F, 'LATIN SMALL LETTER TURNED INSULAR G' ],
    [ 'ALPHA',  'ɒ', 0x0252, 'LATIN SMALL LETTER TURNED ALPHA' ],
    [ 'DELTA',  'ƍ', 0x018D, 'LATIN SMALL LETTER TURNED DELTA' ],

    # Modifiers
    [ 'R',  'ʴ', 0x02B4, 'MODIFIER LETTER SMALL TURNED R' ],
    [ 'R+',  'ʵ', 0x02B5, 'MODIFIER LETTER SMALL TURNED R WITH HOOK' ],
    [ ',',  'ʻ', 0x02BB, 'MODIFIER LETTER TURNED COMMA' ],
    [ 'A',  'ᵄ', 0x1D44, 'MODIFIER LETTER SMALL TURNED A' ],
    [ 'AE',  'ᵆ', 0x1D46, 'MODIFIER LETTER SMALL TURNED AE' ],
    [ 'E+',  'ᵌ', 0x1D4C, 'MODIFIER LETTER SMALL TURNED OPEN E' ],
    [ 'I',  'ᵎ', 0x1D4E, 'MODIFIER LETTER SMALL TURNED I' ],
    [ 'M',  'ᵚ', 0x1D5A, 'MODIFIER LETTER SMALL TURNED M' ],
    [ 'ALPHA',  'ᶛ', 0x1D9B, 'MODIFIER LETTER SMALL TURNED ALPHA' ],
    [ 'H',  'ᶣ', 0x1DA3, 'MODIFIER LETTER SMALL TURNED H' ],
    [ 'M+',  'ᶭ', 0x1DAD, 'MODIFIER LETTER SMALL TURNED M WITH LONG LEG' ],
    [ 'V',  'ᶺ', 0x1DBA, 'MODIFIER LETTER SMALL TURNED V' ],

    # Combining
    [ ',',  '̒', 0x0312, 'COMBINING TURNED COMMA ABOVE' ],

    [ 'ORNAMENT',  '❛', 0x275B, 'HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT' ],
    [ 'ORNAMENT',  '❝', 0x275D, 'HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT' ],

    [ 'IOTA',  '℩', 0x2129, 'TURNED GREEK SMALL LETTER IOTA' ],
    [ 'GAN',  'ჹ', 0x10F9, 'GEORGIAN LETTER TURNED GAN' ],
    ]