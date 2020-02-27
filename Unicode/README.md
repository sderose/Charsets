This directory mainly contains lists of selected Unicode characters,
expressed as Python, Perl, or other data objects.

Generally, they just declare a dict that maps the code point to the Unicode name.
For example, asPython/spaces.py looks like:

    USpaces = {
        0x0009:  'CHARACTER TABULATION',
        0x000A:  'LINE FEED',
        ...
        0x0020:  'SPACE',
        ...
        0x3000:  'IDEOGRAPHIC SPACE',
        0x303F:  'IDEOGRAPHIC HALF FILL SPACE',
    }

This is the same as produced by `ord --listFormat PYTHONN -f SPACE`.
The `-f SPACE` means to select all characters whose formal name matches
the string (actually regex) "SPACE".
Other formats are available, such as mapping literal characters to names,
or creating strings of the found character; or for Perl; or as an HTML chart,
or as a full information block about each character.

In a few cases, there is additional information such as the "polarity" of
bracket characters, and/or the literal character as a string:

    UBrackets = {
        0x0028:  ( "L", "LEFT PARENTHESIS" ),
        0x0029:  ( "R", "RIGHT PARENTHESIS" ),
        0x005B:  ( "L", "LEFT SQUARE BRACKET" ),
        0x005D:  ( "R", "RIGHT SQUARE BRACKET" ),
        ...
    }

Lists included are:

    boxDrawing.py
    brackets.py
    currency.py
    dashes.py
    fractions.py
    fullstops.py
    latinLetters.py
    ligatures.py
    quote.py
    rotated.py
    sentenceBounds.py
    spaces.py
    xmlPredefined.py

=UnicodeSpecials.py=

This file is special. It defines a class, which in turn defines a bunch of
variables with useful lists, which include things like bracket side, space width, etc.

    class UnicodeSpecials:
    def __init__(self):
        self.brackets = { ... }
        self.currency = { ... }
        self.dashes = { ... }
        self.fractions = { ... }
        self.ligatures = { ... }
        self.ULQuotes = { ... } # Punctuation_Initial
        self.URQuotes = { ... } # Punctuation_Final
        self.UOtherQuotes = { ... }
        self.USpaces = { ... }


