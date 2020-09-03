#README for sjd "Charsets" repo#

This directory mainly contains a variety of tools for manipulating data
in various character sets and encoding, especially Unicode.

## Highlights ##

* `countChars` -- Lots of statistics on character use in files.

* `ord` -- really nice shell access to information about Unicode characters.

* `mathAlphanumerics.py` -- Must be tried to be believed.


## Short descriptions ##

* `changeCase` -- a *nix filter to modify case, to --case Upper, Lower,
Words, Records, or Sentences.

* `changeEncoding` -- convert form one encoding to another. "iconv" is
better overall, this is an older Perl module.

* `changeLineEnds` -- Mess with, or just identify, Mac vs. DOS vs. Unix
style line-breaks.

* `chr` -- Much like `ord`.

* `countByCase` -- count characters in the input by what case they are.

* `countChars` -- Count statistics of character use in files. Reports
frequencies (with character names as well as literals and code points),
and can report all specific locations of particular characters or ranges.
Also break down distributions by Unicode plane, script, and block, and
reports coding errors.

* `getCharsByScript` -- pull out the Unicode characters of a given script.

* `isUTF8` -- Test whether a file is legit UTF-8.

* `makeCharChart.py` -- Create a nice HTML chart showing information about
chosen characters. You may also find the "Unisearcher"
at [http://www.isthisthingon.org/unicode/index.php] very useful.

* `makeFontSamples.py` -- Grabs all the fonts it can find and makes an
HTML file with a sample in each.

* `mathAlphanumerics.py` -- provides somewhat easier access to the very many
alternate Latin and Greek alphabets and Latin digits in Unicode,
such as sans-serif bold, Fraktur, circled, etc.. Many of these
are in the "Mathematical Alphanumeric Symbols" area, but other sets are
supported as well. This package can translate regular Latin and Greek to
any of these. This is more pain than it might seem, because many of the
variants have members that are not in the "expected" place (for example,
MATHEMATICAL ITALIC does not have "h" between "g" and "i", because an earlier
version of Unicode defined Planck constant somewhere else. This package
quietly takes care of all that. It does not handle diacritics,
though that may be added. A few characters are simply missing, particularly
the digit 0. `normalizeUnicode` can undo most of the Latin alphabet transforms.

* `normalizeSpace` -- Do XML-style space normalization on any data.
Can also do more aggressive Unicode space normalization, and has options
to deal with dashes, line-ends, control characters, Unicode private use areas,
and quotes.

* `normalizeUnicode` -- Character normalization on steroids. You can
separately choose most kinds of equivalence defined for Unicode compatibility
decomposition. Can even undo most of the Latin mappings provided by
`mathAlphanumerics.py`.

* `ord` -- Provide tons of data about characters, from their URL encodings
to their Unix Jargon names, Unicode script, plane, and block, etc. Can
also search the Unicode character space and generate lists of found
characters in a wide variety of useful formats. You can pick characters
by hex, decimal, or octal, or mnemonics or literals. Reports are like:

    %ord SPLAT
    Unicode Name:    NUMBER SIGN
    Unicode Script:  Common
    Unicode Block:   Basic Latin
    Unicode Plane:   0: Basic Multilingual
    Literal:         #
    Bases:           o0043 d0035 x0023
    Unicode:         U+0023, utf8 \x23, URI %23
    Entities:        &#35; &#x23; #
    Unix jargon:     Common: number sign; pound; pound sign; hash; sharp; crunch; hex; mesh. Rare: grid; cross-hatch; octothorpe; flash; pig-pen; tic-tac-toe; scratchmark; thud; thump; splat

* `showInvisibles` and `showInvisibles.py` -- Turn
various characters to viewable forms. By
default, turns control characters into the tiny mnemonics known as Unicode
"Control Pictures", but can also turn various characters to hex backslash
codes, URL escapes, and/or colorize them. Should, but does not yet, offer
conversion to XML or HTML character references.

* `showUnicodeCharsInClass.py` --

* `toHiragana` -- Rudimentary Latin to Hiragana transliteration. Written in
hopes of forcing myself to learn Hiragan.

* `transliterate` -- convert once-popular transliterations of Greek, to Unicode.
This mainly handles Betacode and CCAT text (always be careful because the
conventional transliteration differs between Classicists and Theologians).


=======

=The `Unicode/` subdirectory=

This has lists of selected Unicode characters in various useful
categories, such as brackets, left/right paired characters in general,
spaces, dashes, quotes. Theses are mostly available as declared lists
in Perl or Python form..

For example, Unicode/asPython/spaces.py contains lines like:

    USpaces = {
        0x0009:  'CHARACTER TABULATION',
        0x000A:  'LINE FEED',
        ...
        0x0020:  'SPACE',
        ...
        0x3000:  'IDEOGRAPHIC SPACE',
        0x303F:  'IDEOGRAPHIC HALF FILL SPACE',
    }

This can be produced by `ord --listFormat PYTHONN -f SPACE` (`ord` is also
available in this repo).
The `-f SPACE` means to select all characters whose formal name matches
the string (actually regex) "SPACE".
Several other formats are available,
such as mapping literal characters to names,
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

Some of the lists included are:

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

#Unicode/asPython/UnicodeSpecials.py#

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


