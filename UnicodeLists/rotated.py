# Unicode characters that are rotated ("turned") Latin
# See https://stackoverflow.com/questions/2995340/

a = "Z⅄XꤵꓥꓵꓕSꓤÒꓒONꟽ⅂ꓘᒋIΗ⅁ℲƎꓷↃꓭꓯzʎxʍʌnʇsɹbdouɯןʞſ̣ᴉɥɓɟǝpɔqɐ068᠘9૬ҺƐᘔl¡¿؛˙‘‚„⅋"

rotated = {
    # Latin SMALL
    0x00250: (  'A',  'ɐ', 'LATIN SMALL LETTER TURNED A'  ),
    # b USE q
    # c
    # d USE p
    0x001DD: (  'E',  'ǝ', 'LATIN SMALL LETTER TURNED E'  ),
    0x01D08: (  'E',  'ᴈ', 'LATIN SMALL LETTER TURNED OPEN E'  ),
    0x0214E: (  'F',  'ⅎ', 'TURNED SMALL F'  ),
    0x01D77: (  'G',  'ᵷ', 'LATIN SMALL LETTER TURNED G'  ),
    0x00265: (  'H',  'ɥ', 'LATIN SMALL LETTER TURNED H'  ),
    0x01D09: (  'I',  'ᴉ', 'LATIN SMALL LETTER TURNED I'  ),
    # j
    0x0029E: (  'K',  'ʞ', 'LATIN SMALL LETTER TURNED K'  ),
    0x0A781: (  'L',  'ꞁ', 'LATIN SMALL LETTER TURNED L'  ),
    0x0026F: (  'M',  'ɯ', 'LATIN SMALL LETTER TURNED M'  ),
    0x01D1F: (  'M',  'ᴟ', 'LATIN SMALL LETTER SIDEWAYS TURNED M'  ),
    # n USE u
    # o USE o
    # p USE d
    # q USE b
    0x00279: (  'R',  'ɹ', 'LATIN SMALL LETTER TURNED R'  ),
    # s USE s
    0x00287: (  'T',  'ʇ', 'LATIN SMALL LETTER TURNED T'  ),
    # u USE n
    0x0028C: (  'V',  'ʌ', 'LATIN SMALL LETTER TURNED V'  ),
    0x0028D: (  'W',  'ʍ', 'LATIN SMALL LETTER TURN ED W'  ),
    # x USE x
    0x0028E: (  'Y',  'ʎ', 'LATIN SMALL LETTER TURNED Y'  ),
    # z USE z

    # Latin CAPITAL
    0x02C6F: (  'A',  'Ɐ', 'LATIN CAPITAL LETTER TURNED A'  ),
    # A or USE for all U+2200
    # B
    # C
    # D
    0x02C7B: (  'E',  'ⱻ', 'LATIN LETTER SMALL CAPITAL TURNED E'  ),
    0x02132: (  'F',  'Ⅎ', 'TURNED CAPITAL F'  ),
    0x02141: (  'G',  '⅁', 'TURNED SANS-SERIF CAPITAL G'  ),
    # H USE H
    # I USE I
    # J
    # K
    0x0A780: (  'L',  'Ꞁ', 'LATIN CAPITAL LETTER TURNED L'  ),
    0x02142: (  'L',  '⅂', 'TURNED SANS-SERIF CAPITAL L'  ),
    0x0019C: (  'M',  'Ɯ', 'LATIN CAPITAL LETTER TURNED M'  ),
    # N USE N
    # O USE O
    # P
    # Q
    0x01D1A: (  'R',  'ᴚ', 'LATIN LETTER SMALL CAPITAL TURNED R'  ),
    # S USE S
    # T
    # U
    0x00245: (  'V',  'Ʌ', 'LATIN CAPITAL LETTER TURNED V'  ),
    # W USE M
    # X USE X
    0x02144: (  'Y',  '⅄', 'TURNED SANS-SERIF CAPITAL Y'  ),
    # Z USE Z

    0x0214B: (  'D',  '⅋', 'TURNED AMPERSAND'  ),
    0x02319: (  'N',  '⌙', 'TURNED NOT SIGN'  ),
    0x029A2: (  'E',  '⦢', 'TURNED ANGLE'  ),
    # SELF: #$%*~-=+|\/ PAIR: () [] {} <>
    # $ ? USE U+00BF, ! USE U+00A1

    0x002AE: (  'H+',  'ʮ', 'LATIN SMALL LETTER TURNED H WITH FISHHOOK'  ),
    0x002AF: (  'H+',  'ʯ', 'LATIN SMALL LETTER TURNED H WITH FISHHOOK AND TAIL'  ),
    0x00270: (  'M+',  'ɰ', 'LATIN SMALL LETTER TURNED M WITH LONG LEG'  ),
    0x0027A: (  'R+',  'ɺ', 'LATIN SMALL LETTER TURNED R WITH LONG LEG'  ),
    0x0027B: (  'R+',  'ɻ', 'LATIN SMALL LETTER TURNED R WITH HOOK'  ),
    0x02C79: (  'R+',  'ⱹ', 'LATIN SMALL LETTER TURNED R WITH TAIL'  ),
    0x01D02: (  'AE',  'ᴂ', 'LATIN SMALL LETTER TURNED AE'  ),
    0x01D14: (  'OE',  'ᴔ', 'LATIN SMALL LETTER TURNED OE'  ),

    # Why are these called "Latin"?
    0x0A77E: (  'G+',  'Ꝿ', 'LATIN CAPITAL LETTER TURNED INSULAR G'  ),
    0x0A77F: (  'G+',  'ꝿ', 'LATIN SMALL LETTER TURNED INSULAR G'  ),
    0x00252: (  'ALPHA',  'ɒ', 'LATIN SMALL LETTER TURNED ALPHA'  ),
    0x0018D: (  'DELTA',  'ƍ', 'LATIN SMALL LETTER TURNED DELTA'  ),

    # Modifiers
    0x002B4: (  'R',  'ʴ', 'MODIFIER LETTER SMALL TURNED R'  ),
    0x002B5: (  'R+',  'ʵ', 'MODIFIER LETTER SMALL TURNED R WITH HOOK'  ),
    0x002BB: (  ',',  'ʻ', 'MODIFIER LETTER TURNED COMMA'  ),
    0x01D44: (  'A',  'ᵄ', 'MODIFIER LETTER SMALL TURNED A'  ),
    0x01D46: (  'AE',  'ᵆ', 'MODIFIER LETTER SMALL TURNED AE'  ),
    0x01D4C: (  'E+',  'ᵌ', 'MODIFIER LETTER SMALL TURNED OPEN E'  ),
    0x01D4E: (  'I',  'ᵎ', 'MODIFIER LETTER SMALL TURNED I'  ),
    0x01D5A: (  'M',  'ᵚ', 'MODIFIER LETTER SMALL TURNED M'  ),
    0x01D9B: (  'ALPHA',  'ᶛ', 'MODIFIER LETTER SMALL TURNED ALPHA'  ),
    0x01DA3: (  'H',  'ᶣ', 'MODIFIER LETTER SMALL TURNED H'  ),
    0x01DAD: (  'M+',  'ᶭ', 'MODIFIER LETTER SMALL TURNED M WITH LONG LEG'  ),
    0x01DBA: (  'V',  'ᶺ', 'MODIFIER LETTER SMALL TURNED V'  ),

    # Combining
    0x00312: (  ',',  '̒', 'COMBINING TURNED COMMA ABOVE'  ),

    0x0275B: (  'ORNAMENT',  '❛', 'HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT'  ),
    0x0275D: (  'ORNAMENT',  '❝', 'HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT'  ),

    0x02129: (  'IOTA',  '℩', 'TURNED GREEK SMALL LETTER IOTA'  ),
    0x010F9: (  'GAN',  'ჹ', 'GEORGIAN LETTER TURNED GAN'  ),
}
