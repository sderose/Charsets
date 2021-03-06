# Characters that can plausibly be used as list-marker bullets.
# Not including Emoji.
#
# Possible additions:
#     Arrows, pointing hands,
#     reference mark 0x0203b
#     flower punctuation mark 0x02055
#     geometric shapes, math symbols, misc technical
#
bullets = {
    # Bullets per se
    0x02022: 'BULLET',
    0x02023: 'TRIANGULAR BULLET',
    0x02043: 'HYPHEN BULLET',
    0x0204c: 'BLACK LEFTWARDS BULLET',
    0x0204d: 'BLACK RIGHTWARDS BULLET',
    0x02219: 'BULLET OPERATOR',
    0x025ce: 'BULLSEYE',
    0x025d8: 'INVERSE BULLET',
    0x025e6: 'WHITE BULLET',
    0x02619: 'REVERSED ROTATED FLORAL HEART BULLET',
    0x029be: 'CIRCLED WHITE BULLET',
    0x029bf: 'CIRCLED BULLET',

    # Daggers
    0x02020: 'DAGGER',
    0x02021: 'DOUBLE DAGGER',
    0x02e36: 'DAGGER WITH LEFT GUARD',
    0x02e37: 'DAGGER WITH RIGHT GUARD',
    0x02e38: 'TURNED DAGGER',

    # Asterisks
    0x0002a: 'ASTERISK',
    0x02042: 'ASTERISM',
    0x0204e: 'LOW ASTERISK',
    0x02051: 'TWO ASTERISKS ALIGNED VERTICALLY',
    0x02217: 'ASTERISK OPERATOR',
    0x0229b: 'CIRCLED ASTERISK OPERATOR',
    0x02722: 'FOUR TEARDROP-SPOKED ASTERISK',
    0x02723: 'FOUR BALLOON-SPOKED ASTERISK',
    0x02724: 'HEAVY FOUR BALLOON-SPOKED ASTERISK',
    0x02725: 'FOUR CLUB-SPOKED ASTERISK',
    0x02731: 'HEAVY ASTERISK',
    0x02732: 'OPEN CENTRE ASTERISK',
    0x02733: 'EIGHT SPOKED ASTERISK',
    0x0273a: 'SIXTEEN POINTED ASTERISK',
    0x0273b: 'TEARDROP-SPOKED ASTERISK',
    0x0273c: 'OPEN CENTRE TEARDROP-SPOKED ASTERISK',
    0x0273d: 'HEAVY TEARDROP-SPOKED ASTERISK',
    0x02743: 'HEAVY TEARDROP-SPOKED PINWHEEL ASTERISK',
    0x02749: 'BALLOON-SPOKED ASTERISK',
    0x0274a: 'EIGHT TEARDROP-SPOKED PROPELLER ASTERISK',
    0x0274b: 'HEAVY EIGHT TEARDROP-SPOKED PROPELLER ASTERISK',
    0x029c6: 'SQUARED ASTERISK',
    0x02a6e: 'EQUALS WITH ASTERISK',
    0x0a673: 'SLAVONIC ASTERISK',
    0x0fe61: 'SMALL ASTERISK',
    0x0ff0a: 'FULLWIDTH ASTERISK',

    # Unicode 'Dingbats' block
    #
    0x02701: 'UPPER BLADE SCISSORS',
    0x02702: 'BLACK SCISSORS',
    0x02703: 'LOWER BLADE SCISSORS',
    0x02704: 'WHITE SCISSORS',
    0x02705: 'WHITE HEAVY CHECK MARK',
    0x02706: 'TELEPHONE LOCATION SIGN',
    0x02707: 'TAPE DRIVE',
    0x02708: 'AIRPLANE',
    0x02709: 'ENVELOPE',
    0x0270a: 'RAISED FIST',
    0x0270b: 'RAISED HAND',
    0x0270c: 'VICTORY HAND',
    0x0270d: 'WRITING HAND',
    0x0270e: 'LOWER RIGHT PENCIL',
    0x0270f: 'PENCIL',
    0x02710: 'UPPER RIGHT PENCIL',
    0x02711: 'WHITE NIB',
    0x02712: 'BLACK NIB',
    0x02713: 'CHECK MARK',
    0x02714: 'HEAVY CHECK MARK',
    0x02715: 'MULTIPLICATION X',
    0x02716: 'HEAVY MULTIPLICATION X',
    0x02717: 'BALLOT X',
    0x02718: 'HEAVY BALLOT X',
    0x02719: 'OUTLINED GREEK CROSS',
    0x0271a: 'HEAVY GREEK CROSS',
    0x0271b: 'OPEN CENTRE CROSS',
    0x0271c: 'HEAVY OPEN CENTRE CROSS',
    0x0271d: 'LATIN CROSS',
    0x0271e: 'SHADOWED WHITE LATIN CROSS',
    0x0271f: 'OUTLINED LATIN CROSS',
    0x02720: 'MALTESE CROSS',
    0x02721: 'STAR OF DAVID',
    #0x02722: 'FOUR TEARDROP-SPOKED ASTERISK',
    #0x02723: 'FOUR BALLOON-SPOKED ASTERISK',
    #0x02724: 'HEAVY FOUR BALLOON-SPOKED ASTERISK',
    #0x02725: 'FOUR CLUB-SPOKED ASTERISK',
    0x02726: 'BLACK FOUR POINTED STAR',
    0x02727: 'WHITE FOUR POINTED STAR',
    0x02728: 'SPARKLES',
    0x02729: 'STRESS OUTLINED WHITE STAR',
    0x0272a: 'CIRCLED WHITE STAR',
    0x0272b: 'OPEN CENTRE BLACK STAR',
    0x0272c: 'BLACK CENTRE WHITE STAR',
    0x0272d: 'OUTLINED BLACK STAR',
    0x0272e: 'HEAVY OUTLINED BLACK STAR',
    0x0272f: 'PINWHEEL STAR',
    0x02730: 'SHADOWED WHITE STAR',
    #0x02731: 'HEAVY ASTERISK',
    #0x02732: 'OPEN CENTRE ASTERISK',
    #0x02733: 'EIGHT SPOKED ASTERISK',
    0x02734: 'EIGHT POINTED BLACK STAR',
    0x02735: 'EIGHT POINTED PINWHEEL STAR',
    0x02736: 'SIX POINTED BLACK STAR',
    0x02737: 'EIGHT POINTED RECTILINEAR BLACK STAR',
    0x02738: 'HEAVY EIGHT POINTED RECTILINEAR BLACK STAR',
    0x02739: 'TWELVE POINTED BLACK STAR',
    #0x0273a: 'SIXTEEN POINTED ASTERISK',
    #0x0273b: 'TEARDROP-SPOKED ASTERISK',
    #0x0273c: 'OPEN CENTRE TEARDROP-SPOKED ASTERISK',
    #0x0273d: 'HEAVY TEARDROP-SPOKED ASTERISK',
    0x0273e: 'SIX PETALLED BLACK AND WHITE FLORETTE',
    0x0273f: 'BLACK FLORETTE',
    0x02740: 'WHITE FLORETTE',
    0x02741: 'EIGHT PETALLED OUTLINED BLACK FLORETTE',
    0x02742: 'CIRCLED OPEN CENTRE EIGHT POINTED STAR',
    #0x02743: 'HEAVY TEARDROP-SPOKED PINWHEEL ASTERISK',
    0x02744: 'SNOWFLAKE',
    0x02745: 'TIGHT TRIFOLIATE SNOWFLAKE',
    0x02746: 'HEAVY CHEVRON SNOWFLAKE',
    0x02747: 'SPARKLE',
    0x02748: 'HEAVY SPARKLE',
    #0x02749: 'BALLOON-SPOKED ASTERISK',
    #0x0274a: 'EIGHT TEARDROP-SPOKED PROPELLER ASTERISK',
    #0x0274b: 'HEAVY EIGHT TEARDROP-SPOKED PROPELLER ASTERISK',
    0x0274c: 'CROSS MARK',
    0x0274d: 'SHADOWED WHITE CIRCLE',
    0x0274e: 'NEGATIVE SQUARED CROSS MARK',
    0x0274f: 'LOWER RIGHT DROP-SHADOWED WHITE SQUARE',
    0x02750: 'UPPER RIGHT DROP-SHADOWED WHITE SQUARE',
    0x02751: 'LOWER RIGHT SHADOWED WHITE SQUARE',
    0x02752: 'UPPER RIGHT SHADOWED WHITE SQUARE',
    0x02753: 'BLACK QUESTION MARK ORNAMENT',
    0x02754: 'WHITE QUESTION MARK ORNAMENT',
    0x02755: 'WHITE EXCLAMATION MARK ORNAMENT',
    0x02756: 'BLACK DIAMOND MINUS WHITE X',
    0x02757: 'HEAVY EXCLAMATION MARK SYMBOL',
    0x02758: 'LIGHT VERTICAL BAR',
    0x02759: 'MEDIUM VERTICAL BAR',
    0x0275a: 'HEAVY VERTICAL BAR',
    0x0275b: 'HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT',
    0x0275c: 'HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT',
    0x0275d: 'HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT',
    0x0275e: 'HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT',
    0x0275f: 'HEAVY LOW SINGLE COMMA QUOTATION MARK ORNAMENT',
    0x02760: 'HEAVY LOW DOUBLE COMMA QUOTATION MARK ORNAMENT',
    0x02761: 'CURVED STEM PARAGRAPH SIGN ORNAMENT',
    0x02762: 'HEAVY EXCLAMATION MARK ORNAMENT',
    0x02763: 'HEAVY HEART EXCLAMATION MARK ORNAMENT',
    0x02764: 'HEAVY BLACK HEART',
    0x02765: 'ROTATED HEAVY BLACK HEART BULLET',
    0x02766: 'FLORAL HEART',
    0x02767: 'ROTATED FLORAL HEART BULLET',
    0x02768: 'MEDIUM LEFT PARENTHESIS ORNAMENT',
    0x02769: 'MEDIUM RIGHT PARENTHESIS ORNAMENT',
    0x0276a: 'MEDIUM FLATTENED LEFT PARENTHESIS ORNAMENT',
    0x0276b: 'MEDIUM FLATTENED RIGHT PARENTHESIS ORNAMENT',
    0x0276c: 'MEDIUM LEFT-POINTING ANGLE BRACKET ORNAMENT',
    0x0276d: 'MEDIUM RIGHT-POINTING ANGLE BRACKET ORNAMENT',
    0x0276e: 'HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT',
    0x0276f: 'HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT',
    0x02770: 'HEAVY LEFT-POINTING ANGLE BRACKET ORNAMENT',
    0x02771: 'HEAVY RIGHT-POINTING ANGLE BRACKET ORNAMENT',
    0x02772: 'LIGHT LEFT TORTOISE SHELL BRACKET ORNAMENT',
    0x02773: 'LIGHT RIGHT TORTOISE SHELL BRACKET ORNAMENT',
    0x02774: 'MEDIUM LEFT CURLY BRACKET ORNAMENT',
    0x02775: 'MEDIUM RIGHT CURLY BRACKET ORNAMENT',
    0x02776: 'DINGBAT NEGATIVE CIRCLED DIGIT ONE',
    0x02777: 'DINGBAT NEGATIVE CIRCLED DIGIT TWO',
    0x02778: 'DINGBAT NEGATIVE CIRCLED DIGIT THREE',
    0x02779: 'DINGBAT NEGATIVE CIRCLED DIGIT FOUR',
    0x0277a: 'DINGBAT NEGATIVE CIRCLED DIGIT FIVE',
    0x0277b: 'DINGBAT NEGATIVE CIRCLED DIGIT SIX',
    0x0277c: 'DINGBAT NEGATIVE CIRCLED DIGIT SEVEN',
    0x0277d: 'DINGBAT NEGATIVE CIRCLED DIGIT EIGHT',
    0x0277e: 'DINGBAT NEGATIVE CIRCLED DIGIT NINE',
    0x0277f: 'DINGBAT NEGATIVE CIRCLED NUMBER TEN',
    0x02780: 'DINGBAT CIRCLED SANS-SERIF DIGIT ONE',
    0x02781: 'DINGBAT CIRCLED SANS-SERIF DIGIT TWO',
    0x02782: 'DINGBAT CIRCLED SANS-SERIF DIGIT THREE',
    0x02783: 'DINGBAT CIRCLED SANS-SERIF DIGIT FOUR',
    0x02784: 'DINGBAT CIRCLED SANS-SERIF DIGIT FIVE',
    0x02785: 'DINGBAT CIRCLED SANS-SERIF DIGIT SIX',
    0x02786: 'DINGBAT CIRCLED SANS-SERIF DIGIT SEVEN',
    0x02787: 'DINGBAT CIRCLED SANS-SERIF DIGIT EIGHT',
    0x02788: 'DINGBAT CIRCLED SANS-SERIF DIGIT NINE',
    0x02789: 'DINGBAT CIRCLED SANS-SERIF NUMBER TEN',
    0x0278a: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT ONE',
    0x0278b: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT TWO',
    0x0278c: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT THREE',
    0x0278d: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT FOUR',
    0x0278e: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT FIVE',
    0x0278f: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT SIX',
    0x02790: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT SEVEN',
    0x02791: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT EIGHT',
    0x02792: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT NINE',
    0x02793: 'DINGBAT NEGATIVE CIRCLED SANS-SERIF NUMBER TEN',
    0x02794: 'HEAVY WIDE-HEADED RIGHTWARDS ARROW',
    0x02795: 'HEAVY PLUS SIGN',
    0x02796: 'HEAVY MINUS SIGN',
    0x02797: 'HEAVY DIVISION SIGN',
    0x02798: 'HEAVY SOUTH EAST ARROW',
    0x02799: 'HEAVY RIGHTWARDS ARROW',
    0x0279a: 'HEAVY NORTH EAST ARROW',
    0x0279b: 'DRAFTING POINT RIGHTWARDS ARROW',
    0x0279c: 'HEAVY ROUND-TIPPED RIGHTWARDS ARROW',
    0x0279d: 'TRIANGLE-HEADED RIGHTWARDS ARROW',
    0x0279e: 'HEAVY TRIANGLE-HEADED RIGHTWARDS ARROW',
    0x0279f: 'DASHED TRIANGLE-HEADED RIGHTWARDS ARROW',
    0x027a0: 'HEAVY DASHED TRIANGLE-HEADED RIGHTWARDS ARROW',
    0x027a1: 'BLACK RIGHTWARDS ARROW',
    0x027a2: 'THREE-D TOP-LIGHTED RIGHTWARDS ARROWHEAD',
    0x027a3: 'THREE-D BOTTOM-LIGHTED RIGHTWARDS ARROWHEAD',
    0x027a4: 'BLACK RIGHTWARDS ARROWHEAD',
    0x027a5: 'HEAVY BLACK CURVED DOWNWARDS AND RIGHTWARDS ARROW',
    0x027a6: 'HEAVY BLACK CURVED UPWARDS AND RIGHTWARDS ARROW',
    0x027a7: 'SQUAT BLACK RIGHTWARDS ARROW',
    0x027a8: 'HEAVY CONCAVE-POINTED BLACK RIGHTWARDS ARROW',
    0x027a9: 'RIGHT-SHADED WHITE RIGHTWARDS ARROW',
    0x027aa: 'LEFT-SHADED WHITE RIGHTWARDS ARROW',
    0x027ab: 'BACK-TILTED SHADOWED WHITE RIGHTWARDS ARROW',
    0x027ac: 'FRONT-TILTED SHADOWED WHITE RIGHTWARDS ARROW',
    0x027ad: 'HEAVY LOWER RIGHT-SHADOWED WHITE RIGHTWARDS ARROW',
    0x027ae: 'HEAVY UPPER RIGHT-SHADOWED WHITE RIGHTWARDS ARROW',
    0x027af: 'NOTCHED LOWER RIGHT-SHADOWED WHITE RIGHTWARDS ARROW',
    0x027b0: 'CURLY LOOP',
    0x027b1: 'NOTCHED UPPER RIGHT-SHADOWED WHITE RIGHTWARDS ARROW',
    0x027b2: 'CIRCLED HEAVY WHITE RIGHTWARDS ARROW',
    0x027b3: 'WHITE-FEATHERED RIGHTWARDS ARROW',
    0x027b4: 'BLACK-FEATHERED SOUTH EAST ARROW',
    0x027b5: 'BLACK-FEATHERED RIGHTWARDS ARROW',
    0x027b6: 'BLACK-FEATHERED NORTH EAST ARROW',
    0x027b7: 'HEAVY BLACK-FEATHERED SOUTH EAST ARROW',
    0x027b8: 'HEAVY BLACK-FEATHERED RIGHTWARDS ARROW',
    0x027b9: 'HEAVY BLACK-FEATHERED NORTH EAST ARROW',
    0x027ba: 'TEARDROP-BARBED RIGHTWARDS ARROW',
    0x027bb: 'HEAVY TEARDROP-SHANKED RIGHTWARDS ARROW',
    0x027bc: 'WEDGE-TAILED RIGHTWARDS ARROW',
    0x027bd: 'HEAVY WEDGE-TAILED RIGHTWARDS ARROW',
    0x027be: 'OPEN-OUTLINED RIGHTWARDS ARROW',
    0x027bf: 'DOUBLE CURLY LOOP',
}
