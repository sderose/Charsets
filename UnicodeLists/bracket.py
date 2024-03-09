# The first item indicate which side the bracket goes on:
#     L (left), R (right), T (top), B (bottom), or ? (ambiguous)
#
UBrackets = {
    0x00028:  ( "L", "LEFT PARENTHESIS" ),
    0x00029:  ( "R", "RIGHT PARENTHESIS" ),
    0x0005B:  ( "L", "LEFT SQUARE BRACKET" ),
    0x0005D:  ( "R", "RIGHT SQUARE BRACKET" ),
    0x0007B:  ( "L", "LEFT CURLY BRACKET" ),
    0x0007D:  ( "R", "RIGHT CURLY BRACKET" ),
    0x02045:  ( "L", "LEFT SQUARE BRACKET WITH QUILL" ),
    0x02046:  ( "R", "RIGHT SQUARE BRACKET WITH QUILL" ),
    0x0207D:  ( "L", "SUPERSCRIPT LEFT PARENTHESIS" ),
    0x0207E:  ( "R", "SUPERSCRIPT RIGHT PARENTHESIS" ),
    0x0208D:  ( "L", "SUBSCRIPT LEFT PARENTHESIS" ),
    0x0208E:  ( "R", "SUBSCRIPT RIGHT PARENTHESIS" ),
    0x02329:  ( "L", "LEFT-POINTING ANGLE BRACKET" ),
    0x0232A:  ( "R", "RIGHT-POINTING ANGLE BRACKET" ),
    0x0239B:  ( "L", "LEFT PARENTHESIS UPPER HOOK" ),
    0x0239C:  ( "L", "LEFT PARENTHESIS EXTENSION" ),
    0x0239D:  ( "L", "LEFT PARENTHESIS LOWER HOOK" ),
    0x0239E:  ( "R", "RIGHT PARENTHESIS UPPER HOOK" ),
    0x0239F:  ( "R", "RIGHT PARENTHESIS EXTENSION" ),
    0x023A0:  ( "R", "RIGHT PARENTHESIS LOWER HOOK" ),
    0x023A1:  ( "L", "LEFT SQUARE BRACKET UPPER CORNER" ),
    0x023A2:  ( "L", "LEFT SQUARE BRACKET EXTENSION" ),
    0x023A3:  ( "L", "LEFT SQUARE BRACKET LOWER CORNER" ),
    0x023A4:  ( "R", "RIGHT SQUARE BRACKET UPPER CORNER" ),
    0x023A5:  ( "R", "RIGHT SQUARE BRACKET EXTENSION" ),
    0x023A6:  ( "R", "RIGHT SQUARE BRACKET LOWER CORNER" ),
    0x023A7:  ( "L", "LEFT CURLY BRACKET UPPER HOOK" ),
    0x023A8:  ( "L", "LEFT CURLY BRACKET MIDDLE PIECE" ),
    0x023A9:  ( "L", "LEFT CURLY BRACKET LOWER HOOK" ),
    0x023AA:  ( "X", "CURLY BRACKET EXTENSION" ),
    0x023AB:  ( "R", "RIGHT CURLY BRACKET UPPER HOOK" ),
    0x023AC:  ( "R", "RIGHT CURLY BRACKET MIDDLE PIECE" ),
    0x023AD:  ( "R", "RIGHT CURLY BRACKET LOWER HOOK" ),
    0x023B0:  ( "?", "UPPER LEFT OR LOWER RIGHT CURLY BRACKET SECTION" ),
    0x023B1:  ( "?", "UPPER RIGHT OR LOWER LEFT CURLY BRACKET SECTION" ),
    0x023B4:  ( "T", "TOP SQUARE BRACKET" ),
    0x023B5:  ( "B", "BOTTOM SQUARE BRACKET" ),
    0x023B6:  ( "B", "BOTTOM SQUARE BRACKET OVER TOP SQUARE BRACKET" ),
    0x023DC:  ( "T", "TOP PARENTHESIS (mathematical use)" ),
    0x023DD:  ( "B", "BOTTOM PARENTHESIS (mathematical use)" ),
    0x023DE:  ( "T", "TOP CURLY BRACKET (mathematical use)" ),
    0x023DF:  ( "B", "BOTTOM CURLY BRACKET (mathematical use)" ),
    0x023E0:  ( "T", "TOP TORTOISE SHELL BRACKET (mathematical use)" ),
    0x023E1:  ( "B", "BOTTOM TORTOISE SHELL BRACKET (mathematical use)" ),
    0x02768:  ( "L", "MEDIUM LEFT PARENTHESIS ORNAMENT" ),
    0x02769:  ( "R", "MEDIUM RIGHT PARENTHESIS ORNAMENT" ),
    0x0276A:  ( "L", "MEDIUM FLATTENED LEFT PARENTHESIS ORNAMENT" ),
    0x0276B:  ( "R", "MEDIUM FLATTENED RIGHT PARENTHESIS ORNAMENT" ),
    0x0276C:  ( "L", "MEDIUM LEFT-POINTING ANGLE BRACKET ORNAMENT" ),
    0x0276D:  ( "R", "MEDIUM RIGHT-POINTING ANGLE BRACKET ORNAMENT" ),
    0x02770:  ( "L", "HEAVY LEFT-POINTING ANGLE BRACKET ORNAMENT" ),
    0x02771:  ( "R", "HEAVY RIGHT-POINTING ANGLE BRACKET ORNAMENT" ),
    0x02772:  ( "L", "LIGHT LEFT TORTOISE SHELL BRACKET ORNAMENT" ),
    0x02773:  ( "R", "LIGHT RIGHT TORTOISE SHELL BRACKET ORNAMENT" ),
    0x02774:  ( "L", "MEDIUM LEFT CURLY BRACKET ORNAMENT" ),
    0x02775:  ( "R", "MEDIUM RIGHT CURLY BRACKET ORNAMENT" ),
    0x027E6:  ( "L", "MATHEMATICAL LEFT WHITE SQUARE BRACKET" ),
    0x027E7:  ( "R", "MATHEMATICAL RIGHT WHITE SQUARE BRACKET" ),
    0x027E8:  ( "L", "MATHEMATICAL LEFT ANGLE BRACKET" ),
    0x027E9:  ( "R", "MATHEMATICAL RIGHT ANGLE BRACKET" ),
    0x027EA:  ( "L", "MATHEMATICAL LEFT DOUBLE ANGLE BRACKET" ),
    0x027EB:  ( "R", "MATHEMATICAL RIGHT DOUBLE ANGLE BRACKET" ),
    0x027EC:  ( "L", "MATHEMATICAL LEFT WHITE TORTOISE SHELL BRACKET" ),
    0x027ED:  ( "R", "MATHEMATICAL RIGHT WHITE TORTOISE SHELL BRACKET" ),
    0x027EE:  ( "L", "MATHEMATICAL LEFT FLATTENED PARENTHESIS" ),
    0x027EF:  ( "R", "MATHEMATICAL RIGHT FLATTENED PARENTHESIS" ),
    0x02983:  ( "L", "LEFT WHITE CURLY BRACKET" ),
    0x02984:  ( "R", "RIGHT WHITE CURLY BRACKET" ),
    0x02985:  ( "L", "LEFT WHITE PARENTHESIS" ),
    0x02986:  ( "R", "RIGHT WHITE PARENTHESIS" ),
    0x02987:  ( "L", "Z NOTATION LEFT IMAGE BRACKET" ),
    0x02988:  ( "R", "Z NOTATION RIGHT IMAGE BRACKET" ),
    0x02989:  ( "L", "Z NOTATION LEFT BINDING BRACKET" ),
    0x0298A:  ( "R", "Z NOTATION RIGHT BINDING BRACKET" ),
    0x0298B:  ( "L", "LEFT SQUARE BRACKET WITH UNDERBAR" ),
    0x0298C:  ( "R", "RIGHT SQUARE BRACKET WITH UNDERBAR" ),
    0x0298D:  ( "L", "LEFT SQUARE BRACKET WITH TICK IN TOP CORNER" ),
    0x0298E:  ( "R", "RIGHT SQUARE BRACKET WITH TICK IN BOTTOM CORNER" ),
    0x0298F:  ( "L", "LEFT SQUARE BRACKET WITH TICK IN BOTTOM CORNER" ),
    0x02990:  ( "R", "RIGHT SQUARE BRACKET WITH TICK IN TOP CORNER" ),
    0x02991:  ( "L", "LEFT ANGLE BRACKET WITH DOT" ),
    0x02992:  ( "R", "RIGHT ANGLE BRACKET WITH DOT" ),
    0x02993:  ( "L", "LEFT ARC LESS-THAN BRACKET" ),
    0x02994:  ( "R", "RIGHT ARC GREATER-THAN BRACKET" ),
    0x02995:  ( "L", "DOUBLE LEFT ARC GREATER-THAN BRACKET" ),
    0x02996:  ( "R", "DOUBLE RIGHT ARC LESS-THAN BRACKET" ),
    0x02997:  ( "L", "LEFT BLACK TORTOISE SHELL BRACKET" ),
    0x02998:  ( "R", "RIGHT BLACK TORTOISE SHELL BRACKET" ),
    0x029FC:  ( "L", "LEFT-POINTING CURVED ANGLE BRACKET" ),
    0x029FD:  ( "R", "RIGHT-POINTING CURVED ANGLE BRACKET" ),
    0x02E02:  ( "L", "LEFT SUBSTITUTION BRACKET" ),
    0x02E03:  ( "R", "RIGHT SUBSTITUTION BRACKET" ),
    0x02E04:  ( "L", "LEFT DOTTED SUBSTITUTION BRACKET" ),
    0x02E05:  ( "R", "RIGHT DOTTED SUBSTITUTION BRACKET" ),
    0x02E09:  ( "L", "LEFT TRANSPOSITION BRACKET" ),
    0x02E0A:  ( "R", "RIGHT TRANSPOSITION BRACKET" ),
    0x02E0C:  ( "L", "LEFT RAISED OMISSION BRACKET" ),
    0x02E0D:  ( "R", "RIGHT RAISED OMISSION BRACKET" ),
    0x02E1C:  ( "L", "LEFT LOW PARAPHRASE BRACKET" ),
    0x02E1D:  ( "R", "RIGHT LOW PARAPHRASE BRACKET" ),
    0x02E22:  ( "L", "TOP LEFT HALF BRACKET" ),
    0x02E23:  ( "R", "TOP RIGHT HALF BRACKET" ),
    0x02E24:  ( "L", "BOTTOM LEFT HALF BRACKET" ),
    0x02E25:  ( "R", "BOTTOM RIGHT HALF BRACKET" ),
    0x02E26:  ( "L", "LEFT SIDEWAYS U BRACKET" ),
    0x02E27:  ( "R", "RIGHT SIDEWAYS U BRACKET" ),
    0x02E28:  ( "L", "LEFT DOUBLE PARENTHESIS" ),
    0x02E29:  ( "R", "RIGHT DOUBLE PARENTHESIS" ),
    0x03008:  ( "L", "LEFT ANGLE BRACKET" ),
    0x03009:  ( "R", "RIGHT ANGLE BRACKET" ),
    0x0300A:  ( "L", "LEFT DOUBLE ANGLE BRACKET" ),
    0x0300B:  ( "R", "RIGHT DOUBLE ANGLE BRACKET" ),
    0x0300C:  ( "L", "LEFT CORNER BRACKET" ),
    0x0300D:  ( "R", "RIGHT CORNER BRACKET" ),
    0x0300E:  ( "L", "LEFT WHITE CORNER BRACKET" ),
    0x0300F:  ( "R", "RIGHT WHITE CORNER BRACKET" ),
    0x03010:  ( "L", "LEFT BLACK LENTICULAR BRACKET" ),
    0x03011:  ( "R", "RIGHT BLACK LENTICULAR BRACKET" ),
    0x03014:  ( "L", "LEFT TORTOISE SHELL BRACKET" ),
    0x03015:  ( "R", "RIGHT TORTOISE SHELL BRACKET" ),
    0x03016:  ( "L", "LEFT WHITE LENTICULAR BRACKET" ),
    0x03017:  ( "R", "RIGHT WHITE LENTICULAR BRACKET" ),
    0x03018:  ( "L", "LEFT WHITE TORTOISE SHELL BRACKET" ),
    0x03019:  ( "R", "RIGHT WHITE TORTOISE SHELL BRACKET" ),
    0x0301A:  ( "L", "LEFT WHITE SQUARE BRACKET" ),
    0x0301B:  ( "R", "RIGHT WHITE SQUARE BRACKET" ),
    0x0FD3E:  ( "L", "ORNATE LEFT PARENTHESIS" ),
    0x0FD3F:  ( "R", "ORNATE RIGHT PARENTHESIS" ),
    0x0FE17:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT WHITE LENTICULAR BRACKET" ),
    0x0FE35:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT PARENTHESIS" ),
    0x0FE36:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT PARENTHESIS" ),
    0x0FE37:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT CURLY BRACKET" ),
    0x0FE38:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT CURLY BRACKET" ),
    0x0FE39:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT TORTOISE SHELL BRACKET" ),
    0x0FE3A:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT TORTOISE SHELL BRACKET" ),
    0x0FE3B:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT BLACK LENTICULAR BRACKET" ),
    0x0FE3C:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT BLACK LENTICULAR BRACKET" ),
    0x0FE3D:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT DOUBLE ANGLE BRACKET" ),
    0x0FE3E:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT DOUBLE ANGLE BRACKET" ),
    0x0FE3F:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT ANGLE BRACKET" ),
    0x0FE40:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT ANGLE BRACKET" ),
    0x0FE41:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT CORNER BRACKET" ),
    0x0FE42:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT CORNER BRACKET" ),
    0x0FE43:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT WHITE CORNER BRACKET" ),
    0x0FE44:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT WHITE CORNER BRACKET" ),
    0x0FE47:  ( "L", "PRESENTATION FORM FOR VERTICAL LEFT SQUARE BRACKET" ),
    0x0FE48:  ( "R", "PRESENTATION FORM FOR VERTICAL RIGHT SQUARE BRACKET" ),
    0x0FE59:  ( "L", "SMALL LEFT PARENTHESIS" ),
    0x0FE5A:  ( "R", "SMALL RIGHT PARENTHESIS" ),
    0x0FE5B:  ( "L", "SMALL LEFT CURLY BRACKET" ),
    0x0FE5C:  ( "R", "SMALL RIGHT CURLY BRACKET" ),
    0x0FE5D:  ( "L", "SMALL LEFT TORTOISE SHELL BRACKET" ),
    0x0FE5E:  ( "R", "SMALL RIGHT TORTOISE SHELL BRACKET" ),
    0x0FF08:  ( "L", "FULLWIDTH LEFT PARENTHESIS" ),
    0x0FF09:  ( "R", "FULLWIDTH RIGHT PARENTHESIS" ),
    0x0FF3B:  ( "L", "FULLWIDTH LEFT SQUARE BRACKET" ),
    0x0FF3D:  ( "R", "FULLWIDTH RIGHT SQUARE BRACKET" ),
    0x0FF5B:  ( "L", "FULLWIDTH LEFT CURLY BRACKET" ),
    0x0FF5D:  ( "R", "FULLWIDTH RIGHT CURLY BRACKET" ),
    0x0FF5F:  ( "L", "FULLWIDTH LEFT WHITE PARENTHESIS *" ),
    0x0FF60:  ( "R", "FULLWIDTH RIGHT WHITE PARENTHESIS *" ),
    0x0FF62:  ( "L", "HALFWIDTH LEFT CORNER BRACKET" ),
    0x0FF63:  ( "R", "HALFWIDTH RIGHT CORNER BRACKET" ),
    0x01D11:  ( "X", "5 MUSICAL SYMBOL BRACKET" ),
    0x01D15:  ( "X", "6 MUSICAL SYMBOL PARENTHESIS NOTEHEAD" ),
    #0x0E002:  ( "L", "8    TAG LEFT PARENTHESIS" ),
    #0x0E002:  ( "R", "9    TAG RIGHT PARENTHESIS" ),
    #0x0E005:  ( "L", "B    TAG LEFT SQUARE BRACKET" ),
    #0x0E005:  ( "R", "D    TAG RIGHT SQUARE BRACKET" ),
    #0x0E007:  ( "L", "B    TAG LEFT CURLY BRACKET" ),
    #0x0E007:  ( "R", "D    TAG RIGHT CURLY BRACKET" ),
}

UBracketPairss = {
    #   LEFT    RIGHT
    (0x00028, 0x00029): "LEFT PARENTHESIS",
    (0x0005B, 0x0005D): "LEFT SQUARE BRACKET",
    (0x0007B, 0x0007D): "LEFT CURLY BRACKET",
    (0x02045, 0x02046): "LEFT SQUARE BRACKET WITH QUILL",
    (0x0207D, 0x0207E): "SUPERSCRIPT LEFT PARENTHESIS",
    (0x0208D, 0x0208E): "SUBSCRIPT LEFT PARENTHESIS",
    (0x02329, 0x0232A): "LEFT-POINTING ANGLE BRACKET",
    (0x02768, 0x02769): "MEDIUM LEFT PARENTHESIS ORNAMENT",
    (0x0276A, 0x0276B): "MEDIUM FLATTENED LEFT PARENTHESIS ORNAMENT",
    (0x0276C, 0x0276D): "MEDIUM LEFT-POINTING ANGLE BRACKET ORNAMENT",
    (0x02770, 0x02771): "HEAVY LEFT-POINTING ANGLE BRACKET ORNAMENT",
    (0x02772, 0x02773): "LIGHT LEFT TORTOISE SHELL BRACKET ORNAMENT",
    (0x02774, 0x02775): "MEDIUM LEFT CURLY BRACKET ORNAMENT",
    (0x027E6, 0x027E7): "MATHEMATICAL LEFT WHITE SQUARE BRACKET",
    (0x027E8, 0x027E9): "MATHEMATICAL LEFT ANGLE BRACKET",
    (0x027EA, 0x027EB): "MATHEMATICAL LEFT DOUBLE ANGLE BRACKET",
    (0x027EC, 0x027ED): "MATHEMATICAL LEFT WHITE TORTOISE SHELL BRACKET",
    (0x027EE, 0x027EF): "MATHEMATICAL LEFT FLATTENED PARENTHESIS",
    (0x02983, 0x02984): "LEFT WHITE CURLY BRACKET",
    (0x02985, 0x02986): "LEFT WHITE PARENTHESIS",
    (0x02987, 0x02988): "Z NOTATION LEFT IMAGE BRACKET",
    (0x02989, 0x0298A): "Z NOTATION LEFT BINDING BRACKET",
    (0x0298B, 0x0298C): "LEFT SQUARE BRACKET WITH UNDERBAR",
    (0x0298D, 0x0298E): "LEFT SQUARE BRACKET WITH TICK IN TOP CORNER",
    (0x0298F, 0x02990): "LEFT SQUARE BRACKET WITH TICK IN BOTTOM CORNER",
    (0x02991, 0x02992): "LEFT ANGLE BRACKET WITH DOT",
    (0x02993, 0x02994): "LEFT ARC LESS-THAN BRACKET",
    (0x02995, 0x02996): "DOUBLE LEFT ARC GREATER-THAN BRACKET",
    (0x02997, 0x02998): "LEFT BLACK TORTOISE SHELL BRACKET",
    (0x029FC, 0x029FD): "LEFT-POINTING CURVED ANGLE BRACKET",
    (0x02E02, 0x02E03): "LEFT SUBSTITUTION BRACKET",
    (0x02E04, 0x02E05): "LEFT DOTTED SUBSTITUTION BRACKET",
    (0x02E09, 0x02E0A): "LEFT TRANSPOSITION BRACKET",
    (0x02E0C, 0x02E0D): "LEFT RAISED OMISSION BRACKET",
    (0x02E1C, 0x02E1D): "LEFT LOW PARAPHRASE BRACKET",
    (0x02E22, 0x02E23): "TOP LEFT HALF BRACKET",
    (0x02E24, 0x02E25): "BOTTOM LEFT HALF BRACKET",
    (0x02E26, 0x02E27): "LEFT SIDEWAYS U BRACKET",
    (0x02E28, 0x02E29): "LEFT DOUBLE PARENTHESIS",
    (0x03008, 0x03009): "LEFT ANGLE BRACKET",
    (0x0300A, 0x0300B): "LEFT DOUBLE ANGLE BRACKET",
    (0x0300C, 0x0300D): "LEFT CORNER BRACKET",
    (0x0300E, 0x0300F): "LEFT WHITE CORNER BRACKET",
    (0x03010, 0x03011): "LEFT BLACK LENTICULAR BRACKET",
    (0x03014, 0x03015): "LEFT TORTOISE SHELL BRACKET",
    (0x03016, 0x03017): "LEFT WHITE LENTICULAR BRACKET",
    (0x03018, 0x03019): "LEFT WHITE TORTOISE SHELL BRACKET",
    (0x0301A, 0x0301B): "LEFT WHITE SQUARE BRACKET",
    (0x0FD3E, 0x0FD3F): "ORNATE LEFT PARENTHESIS",
    (0x0FE35, 0x0FE36): "PRESENTATION FORM FOR VERTICAL LEFT PARENTHESIS",
    (0x0FE37, 0x0FE38): "PRESENTATION FORM FOR VERTICAL LEFT CURLY BRACKET",
    (0x0FE39, 0x0FE3A): "PRESENTATION FORM FOR VERTICAL LEFT TORTOISE SHELL BRACKET",
    (0x0FE3B, 0x0FE3C): "PRESENTATION FORM FOR VERTICAL LEFT BLACK LENTICULAR BRACKET",
    (0x0FE3D, 0x0FE3E): "PRESENTATION FORM FOR VERTICAL LEFT DOUBLE ANGLE BRACKET",
    (0x0FE3F, 0x0FE40): "PRESENTATION FORM FOR VERTICAL LEFT ANGLE BRACKET",
    (0x0FE41, 0x0FE42): "PRESENTATION FORM FOR VERTICAL LEFT CORNER BRACKET",
    (0x0FE43, 0x0FE44): "PRESENTATION FORM FOR VERTICAL LEFT WHITE CORNER BRACKET",
    (0x0FE47, 0x0FE48): "PRESENTATION FORM FOR VERTICAL LEFT SQUARE BRACKET",
    (0x0FE59, 0x0FE5A): "SMALL LEFT PARENTHESIS",
    (0x0FE5B, 0x0FE5C): "SMALL LEFT CURLY BRACKET",
    (0x0FE5D, 0x0FE5E): "SMALL LEFT TORTOISE SHELL BRACKET",
    (0x0FF08, 0x0FF09): "FULLWIDTH LEFT PARENTHESIS",
    (0x0FF3B, 0x0FF3D): "FULLWIDTH LEFT SQUARE BRACKET",
    (0x0FF5B, 0x0FF5D): "FULLWIDTH LEFT CURLY BRACKET",
    (0x0FF5F, 0x0FF60): "FULLWIDTH LEFT WHITE PARENTHESIS",
    (0x0FF62, 0x0FF63): "HALFWIDTH LEFT CORNER BRACKET",
}
