#Charsets Repo#

[https://www.github.com/sderose/Charsets]

Utilities for working with Unicode and other character sets.

See also `CharDisplay.py`, currently in my PYTHONLIBS repo.

As with all my utilities, use "-h" to get help.

#
#=UnicodeLists subdirectory==

This subdirectory has lists of characters in various important categories, such
as whitespace, dashes, quotation marks, currency, brackets, etc. Ones with
extension `.py` are
generally declarations of Python lists, with one entry per code point, with
the character code point and formal name. You can generate such lists
using the `ord` or `strfchr.py` commands (see below).
For example, with `ord` you can select all characters whose
Unicode full names match a given regex, and export the list in many
formats, such as JSON, an HTML table, Perl or Python lists or dicts, etc.


## Highlights ##

`countChars` -- Reports lots of statistics on character use in files.
Very handy for figuring out what's in allegedly "plain text" files.

* `mathAlphanumerics.py` -- Recodes Latin and/or Greek letters and Arabic
digits, to alternate forms provided in Unicode. For example Unicode has
a "MATHEMATICAL BOLD ITALIC" set of Latin letters:
    Upper:𝑻𝑯𝑬 𝑸𝑼𝑰𝑪𝑲 𝑶𝑵𝒀𝑿 𝑮𝑶𝑩𝑳𝑰𝑵 𝑱𝑼𝑴𝑷𝑺 𝑶𝑽𝑬𝑹 𝑻𝑯𝑬 𝑳𝑨𝒁𝒀 𝑫𝑾𝑨𝑹𝑭
    Lower:𝒕𝒉𝒆 𝒒𝒖𝒊𝒄𝒌 𝒐𝒏𝒚𝒙 𝒈𝒐𝒃𝒍𝒊𝒏 𝒋𝒖𝒎𝒑𝒔 𝒐𝒗𝒆𝒓 𝒕𝒉𝒆 𝒍𝒂𝒛𝒚 𝒅𝒘𝒂𝒓𝒇

* There's a family of utilities for getting access to specific properties and
representations of Unicode (and other) characters:

    ** `ord`
    ** `CharDisplay.py` ([)in ../PYTHONLIBS at the moment)
    ** `strfchr.py`

As commands, these takes a code point number(s) in any of the usual bases, and
print a variety of information about that character. Some can also display
charts of particular ranges or categories, or search for characters by
regexes matched to their Unicode names, or show informations about a few
other character sets such as Latin-1 and CP1252.

    ** `showInvisibles.py` (and showInvisibles, an older Perl version)
    ** `showInvisibles`(), equivalent functions from sjdUtils.py and sjdUtils.pm.

These convert special (say, nonprintable or nonASCII) characters to viewable
forms. Several different options are available, such as converting control
characters to their "Control Picture" Unicode symbols (U+2400...), colorizing,
escaping via \x, \u, etc.


## Short descriptions ##

* `changeCase` -- a *nix filter to modify case, to --case Upper, Lower,
Words, Records, or Sentences.

* `changeEncoding` (Perl) -- convert form one encoding to another. "iconv" is
better overall, this is an older Perl module.

* `changeLineEnds` (Perl) -- convert between Mac, Windows, and *nix style line boundaries.

* `chr` (Perl) -- given a Unicode code point number(s) in octal, decimal, or hex,
or control character mnemonic,
show a bunch of information about the Unicode character(s). I prefer `ord`
(see below), which is similar but has many more features.

* `countByCase` (Perl) -- count characters in the input by what case they are.

* `countChars` (Perl) -- count what characters occur in the input, and produce a frequency
table, as well as totals by Unicode script and block, etc. A nice way to verify
data you were told was Unicode or ASCII.
Also breaks down distributions by Unicode plane, script, and block, and
reports coding errors and CP1252 characters.

* `getCharsByScript` (Perl) -- pull out the Unicode characters of a given script.

* `isUTF8` (Perl) -- report whether the file is legit utf-8 or not.

* `makeCharChart.py` -- Create a nice HTML chart showing information about chosen
characters. You may also find the "Unisearcher"
at [http://www.isthisthingon.org/unicode/index.php] very useful.

* `makeFontSamples.py` -- Grabs all the fonts it can find and makes an
HTML file with a sample in each. See also `BashSetup/setupFunctions:bigchar`.

* `mathAlphanumerics.py` -- Recodes Latin and/or Greek letters and Arabic
digits, to alternate forms provided in Unicode. For example Unicode has
a "MATHEMATICAL BOLD ITALIC" set of Latin letters:
    Upper:𝑻𝑯𝑬 𝑸𝑼𝑰𝑪𝑲 𝑶𝑵𝒀𝑿 𝑮𝑶𝑩𝑳𝑰𝑵 𝑱𝑼𝑴𝑷𝑺 𝑶𝑽𝑬𝑹 𝑻𝑯𝑬 𝑳𝑨𝒁𝒀 𝑫𝑾𝑨𝑹𝑭
    Lower:𝒕𝒉𝒆 𝒒𝒖𝒊𝒄𝒌 𝒐𝒏𝒚𝒙 𝒈𝒐𝒃𝒍𝒊𝒏 𝒋𝒖𝒎𝒑𝒔 𝒐𝒗𝒆𝒓 𝒕𝒉𝒆 𝒍𝒂𝒛𝒚 𝒅𝒘𝒂𝒓𝒇

* `normalizeSpace` (Perl) -- normalize whitespace in the input, as defined for XML. Knows
about Unicode and many other encodings, and also provides options to
normalize dashes, control characters, quotes, and private-use characters.

* `normalizeUnicode` (Perl) -- perform Unicode normalization (there are 4 types) on
the input.


* `ord` (Perl) -- the opposite of "chr": given some specification of a character(s),
show a lot of information about it (example below).
It can accept characters as literals, as code points specified in various bases,
*nix jargon, Unicode names, HTML entity names, etc.

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

A -f option ("find") lets you identify all characters whose Unicode names match
a given regular expression, and write information about them in several
different --outputFormat, such as Python or Perl declarations, HTML tables,
JSON, etc. This search is also the default action if no character can be
found by other methods.

It's smart enough to notice if you ask about C1 control characters, which are
used for printable characters in old Windows character set. If it sees those,
it displays a warning and tells you where the equivalent Unicode character is.

`ord` also has many other options, such as `--c1` which displays a chart of
the C1 control characters; `--math` which shows you all the
"mathematical" variants of the Latin and Greek letters (see also
`mathAlphanumerics.py`); and several `--findXXX`
options for collecting characters by matching names or other properties.


* `showInvisibles` (Perl) -- convert control, non-ASCII, and/or whitespace characters to
visible forms. You have your choice of representations, from Unicode "control pictures"
(tiny mnemonics for control characters, at U+2400 and following); backslash codes;
URI escaping (so you can use this to URI-escape the input), and colorizing.
This is the Perl version, a Python version is also available, as "showInvisibles.py"

* `showInvisibles.py` -- Python version of "showInvisibles" (see prior entry).

* `showUnicodeCharsInClass.py`

* `toHiragana` (Python) -- a toy that transliterates Latin orthography approximately to Hiragana.
I wrote this to help me learn Hiragana even though I don't know Japanese.

* `transliterate` (Perl) -- convert once-popular transliterations of Greek, to Unicode.
This mainly handles Betacode and CCAT text (always be careful because the
conventional transliteration differs between Classicists and Theologians).
