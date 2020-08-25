=Charsets REPO=

Utilities and data for working with Unicode and other character sets.

See also `CharDisplay.py`, in my PYTHONLIBS repo.

As with all my utilities, use "-h" to get help.

==Favorites==

* `ord` (and similar `chr'): Get you lots of information about characters chosen in
various ways. For example:

    ord bullet
        Unicode Name:    BULLET
        Unicode Script:  Common
        Unicode Block:   General Punctuation
        Unicode Plane:   0: Basic Multilingual
        Literal:         •
        Bases:           o20042 d8226 x2022
        Unicode:         U+2022, utf8 \xe2\x80\xa2, URI %e2%80%a2
        Entities:        &#8226; &#x2022; &bull;

You can ask it by name, code point in octal, decimal, or hex, the literal
character, *nix jargon names, HTML entity names, etc. If it can't match
a character to a request in one of those ways, it
searches in the text of Unicode names and prints
all matches.

It also has many other options, such as `--c1` which displays a chart of
the C1 control characters; `--math` which shows you all the
"mathematical" variants of the Latin and Greek letters; and several `--findXXX`
options for collecting characters by matching names or other properties.

`ord` can write out collected characters in a variety of forms, including as
Java, Perl, or Python lists or hashes mapping code point numbers or literal
characters to their name or other information. A bunch of useful collections,
hand-curated, as python declarations are in
[https://github.com/sderose/Charsets/Unicode]
(or soon will be -- ask me if they're not visible yet).

Note: You may or
may not see the special characters correctly in the following example,
or when using the command, depending on how your browser, shell, or
other tool is set up. For example, I see them correctly in Firefox but
not Safari, though neither actually formats the MarkDown file I'm reading:

    ord --math
    Latin:
    ******* PARENTHESIZED LOWER (U+0249c...):
      ⒜  ⒝  ⒞  ⒟  ⒠  ⒡  ⒢  ⒣  ⒤  ⒥  ⒦  ⒧  ⒨  ⒩  ⒪  ⒫  ⒬  ⒭  ⒮  ⒯  ⒰  ⒱  ⒲  ⒳  ⒴  ⒵
    ******* CIRCLED UPPER (U+024b6...):
      Ⓐ  Ⓑ  Ⓒ  Ⓓ  Ⓔ  Ⓕ  Ⓖ  Ⓗ  Ⓘ  Ⓙ  Ⓚ  Ⓛ  Ⓜ  Ⓝ  Ⓞ  Ⓟ  Ⓠ  Ⓡ  Ⓢ  Ⓣ  Ⓤ  Ⓥ  Ⓦ  Ⓧ  Ⓨ  Ⓩ
    ******* CIRCLED LOWER (U+024d0...):
      ⓐ  ⓑ  ⓒ  ⓓ  ⓔ  ⓕ  ⓖ  ⓗ  ⓘ  ⓙ  ⓚ  ⓛ  ⓜ  ⓝ  ⓞ  ⓟ  ⓠ  ⓡ  ⓢ  ⓣ  ⓤ  ⓥ  ⓦ  ⓧ  ⓨ  ⓩ
    ...

* `PYTHONLIBS/CharDisplay.py` is a Python version of most of the
same functionality, which can also be accessed as an API;
and `PYTHONLIBS/mathAlphanumerics.py`, which provides access to those same
mathematical variants as an API (it even quietly deals with the characters
that aren't where you'd expect them in Unicode).

* Wrappers to do basic operations in a pipe or shell: `normalizeSpace`,
`normalizeUnicode`, `showInvisible` (as Unicode "Control Pictures" and/or
backslash codes or entities), `isUTF8`, and `changeLineEnds`.

* Statistics gatherers such as `countChars`


=======

==Unicode/==

This subdirectory has lists of characters in various important categories, such
as whitespace, dashes, quotation marks, currency, brackets, etc. Ones with
extension `.py` are
generally declarations of Python lists, with one entry per code point, with
the character code point and formal name. You can also generate such list
via a regex search of names in the Unicode database, using various options
of the `ord` command (see below).


==UnicodeSamples==

A few samples for testing Unicode support.

* changeCase (Perl) -- a *nix filter to modify case, to --case Upper, Lower,
Words, Records, or Sentences.


==Other (not in subdirectories)==

* changeEncoding (Perl) -- convert form one encoding to another. "iconv" is
better overall, this is an older Perl module.

* changeLineEnds (Perl) -- convert between Mac, Windows, and *nix style line boundaries.

* chr (Perl) -- given a Unicode code point number(s) in octal, decimal, or hex,
or control character mnemonic,
show a bunch of information about the Unicode character(s). I prefer `ord`
(see below), which is similar but has many more features.

* countByCase (Perl) -- count characters in the input by what case they are.

* countChars (Perl) -- count what characters occur in the input, and produce a frequency
table, as well as totals by Unicode script and block, etc. A nice way to catch
data that someone told you was Unicode, but really isn't. It's especially vigilant
about catching and reporting CP1252 characters.

* getCharsByScript (Perl) -- pull out the Unicode characters of a given script.

* isUTF8 (Perl) -- report whether the file is legit utf-8 or not.

* makeCharChart.py -- Create a nice HTML chart showing information about chosen
characters. You may also find the "Unisearcher"
at [http://www.isthisthingon.org/unicode/index.php] very useful.

* normalizeSpace (Perl) -- normalize whitespace in the input, as defined for XML. Knows
about Unicode and many other encodings, and also provides options to
normalize dashes, control characters, quotes, and private-use characters.

* normalizeUnicode (Perl) -- perform Unicode normalization (there are 4 types) on
the input.

* ord (Perl) -- the opposite of "chr": given some specification of a character,
show a lot of information about it (example below). Or if a lot of characters fit,
it will list them with code point, literal, name, and in a number of formats,
including definitions of Perl or Python lists of tuples.
It can accept characters specified in lots of way,
including numbers in  various bases, *nix jargon, HTML entity names, etc.
A -f option ("find") lets you identify all characters whose Unicode names match
a given expression, and --outputFormat.

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

* showInvisibles (Perl) -- convert control, non-ASCII, and/or whitespace characters to
visible forms. You have your choice of representations, from Unicode "control pictures"
(tiny mnemonics for control characters, at U+2400 and following); backslash codes;
URI escaping (so you can use this to URI-escape the input), and colorizing.
This is the Perl version, a Python version is also available, as "showInvisibles.py"

* showInvisibles.py -- Python version of "showInvisibles" (see prior entry).

* showUnicodeCharsInClass.py

* toHiragana (Python) -- a toy that transliterates Latin orthography approximately to Hiragana.
I wrote this to help me learn Hiragana even though I don't know Japanese.

* transliterate (Perl) -- convert once-popular transliterations of Greek, to Unicode.
This mainly handles Betacode and CCAT text (always be careful because the
conventional transliteration differs between Classicists and Theologians).
