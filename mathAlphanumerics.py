#!/usr/bin/env python3
#
# mathAlphanumerics.py: Map Latin, Greek, and digits to special math variants,
# such as bold, italic, fraktur, etc..
# Written <2006-10-04, Steven J. DeRose.
#
#pylint: disable=W0603
#
from __future__ import print_function
import sys
import re
import unicodedata
import string
from typing import List, Dict

__metadata__ = {
    "title"        : "mathAlphanumerics.py",
    "description"  : "Map Latin, Greek, and digits to special math variants.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 2.7.6, 3.7",
    "created"      : "<2006-10-04",
    "modified"     : "2021-12-20",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Description=

Provide support for using the many Unicode variations on alphabets and digits,
either as a command-line filter or via an API.

You can just pipe Unicode text through this like, with options for
the desired script to translate (`--script`,
and the Unicode range (`--font` because that's how it's being used).

    cat eggs.txt | mathAlphanumerics.py --script Latin --font 'BOLD ITALIC'

You can test on a sample phrase:

    mathAlphanumerics.py --script Latin --font 'FRAKTUR' --sample "Spam and eggs"


Or you can call the package from Python:

    import mathAlphanumerics
    s2 = mathAlphanumerics.convert(text,
            script="Latin", font="Mathematical Bold", decompose=True)

The `decompose` option separates diacritics from their base characters, so that the
base characters can be converted.

    xtab = mathAlphanumerics.getTranslateTable(
        "Latin", "Mathematical Sans-serif Bold Italic")
    s = s.translate(xtab)

The "scripts" known are "Latin", "Greek", and "Digits" (each has a different
selection of available "font" variations).
To see a list of the "fonts" available for the selected
`--script`

    mathAlphanumerics.py --script Greek --show

Add `-v` to also display a sample of each, and
the code point where each starts.

'''Note:''' This will only work is your display medium supports Unicode,
and the exact results depend on the font(s) in use. Even then, a few
characters seem to be unavailable in Unicode, such as
"PARENTHESIZED DIGIT ZERO".
When a mapping is not available, the character is left unchanged.

The `--script` choices are "Latin" (the default), "Greek", or "Digits".

The `--font` options (the default is "ITALIC") are:

For Latin:
    "BOLD"                         UPPER LOWER DIGITS
    "ITALIC"                       UPPER LOWER
    "BOLD ITALIC"                  UPPER LOWER
    "SANS-SERIF"                   UPPER LOWER DIGITS
    "SANS-SERIF BOLD"              UPPER LOWER DIGITS
    "SANS-SERIF ITALIC"            UPPER LOWER
    "SANS-SERIF BOLD ITALIC"       UPPER LOWER
    "SCRIPT"                       UPPER LOWER
    "BOLD SCRIPT"                  UPPER LOWER
    "FRAKTUR"                      UPPER LOWER
    "BOLD FRAKTUR"                 UPPER LOWER
    "DOUBLE-STRUCK"                UPPER LOWER DIGITS
    "MONOSPACE"                    UPPER LOWER DIGITS
    "CIRCLED"                      UPPER LOWER DIGITS
    "PARENTHESIZED"                UPPER LOWER DIGITS
    "FULLWIDTH"                    UPPER LOWER DIGITS

    "SQUARED"                      UPPER
    "NEGATIVE SQUARED"             UPPER
    "REGIONAL INDICATOR SYMBOL"    UPPER (???)
    "NEGATIVE CIRCLED"             UPPER
    "SUPERSCRIPT"                  DIGITS (alphabet unfinished)
    "SUBSCRIPT"                    DIGITS (alphabet unfinished)

For Greek:
    "BOLD"                         UPPER LOWER
    "ITALIC"                       UPPER LOWER
    "BOLD ITALIC"                  UPPER LOWER
    "SANS-SERIF BOLD"              UPPER LOWER
    "SANS-SERIF BOLD ITALIC"       UPPER LOWER

For Digits, many additional sets are available, mainly for a variety of orthographies.
In addition to those already listed (I cannot personally evaluate the results
for most of these; error reports are welcome):

    "DIGIT COMMA"
    "DIGIT FULL STOP"
    "ARABIC-INDIC"
    "EXTENDED ARABIC-INDIC"
    "NKO"
    "DEVANAGARI"
    "BENGALI"
    "GURMUKHI"
    "GUJARATI"
    "ORIYA"
    "TAMIL"
    "TELUGU"
    "KANNADA"
    "MALAYALAM"
    "SINHALA LITH"
    "THAI"
    "LAO"
    "TIBETAN"
    "MYANMAR"
    "MYANMAR SHAN"
    "KHMER"
    "MONGOLIAN"
    "LIMBU"
    "NEW TAI LUE"
    "TAI THAM HORA"
    "TAI THAM THAM"
    "BALINESE"
    "SUNDANESE"
    "LEPCHA"
    "OL CHIKI"
    "IDEOGRAPHIC NUMBER"
    "VAI"
    "SAURASHTRA"
    "COMBINING DEVANAGARI"
    "KAYAH LI"
    "JAVANESE"
    "CHAM"
    "MEETEI MAYEK"

Some additional digit sets are available except for ZERO.

    "CIRCLED"
    "DINGBAT NEGATIVE CIRCLED"
    "DOUBLE CIRCLED"
    "PARENTHESIZED"
    "FULL STOP"
    "DINGBAT CIRCLED SANS-SERIF"
    "DINGBAT NEGATIVE CIRCLED SANS-SERIF"

I expect to add other special "effects", but some might not be supported in the "translate table" method:
    "TURNED" (aka ROTATED)
    "STRIKETHROUGH"
    "UNDERLINE"
    "OVERLINE"


=Cautions=

* Some of the "fonts" are available only in uppercase, or lack digits.
* Some of the digit sets lack zero, as noted in the list above.
* Some fonts may not have include all these sets.
* Some fonts may not be aesthetically consistent for all these sets.
As an example, the role of MATHEMATICAL ITALIC SMALL H is filled by
PLANCK CONSTANT, which was added to Unicode much earlier than the rest
of that set. Some font designers might not have co-ordinated it's exact
size, stroke weight, alignment, or other characteristics with the rest
of the MATHEMATICAL ITALIC characters.
* Accented characters are only supported if decomposed. See the next
section for more detail on that.

==Accented and other characters==

This only translates the unaccented basic letters and digits. However, you can
use Unicode `canonical decomposition` first, so diacritics become separate
characters. You can then use this package to modify the base characters:

    import unicodedata
    s = unicodedata.normalize('NFD', myString).translate(xtab)

The result should be reasonable, although imperfect. For example,
diacritic placement could conflicting with an enclosing circle,
or be off center for italics. And the diacritic itself will not be bold, etc.

''Note:'' Throughout this package, "font" does not refer to typographic fonts
per se, but to Unicode's sets of variations (mostly intended for special
uses in mathematics),
such as "MATHEMATICAL SANS-SERIF BOLD ITALIC". The names used here are taken
directly from the Unicode character names, except that "MATHEMATICAL" may be
omitted and case is ignored).


=Methods=

Methods in this package are called statically.

==getFontDict(script="Latin")==

Return `LatinFontDict`, `GreekFontDict`, or `DigitFontDict`, as appropriate.
See their descriptions below.

==getStartCodePoint(script="Latin", font="BOLD", group="U")==

Return the code point of the first character for the given `script` in
the given `font` variation (such as "SANS-SERIF BOLD", etc.). By default, gets
the position of A for Latin, alpha for Greek, or Digit for 0). Pass `group`
as "U", "L", or "D" respectively, to get the position of the first uppercase,
lowercase, or digit for "fonts" as needed.
Typically, the uppercase range is first, immediately followed by the lowercase
range, and the digits are elsewhere.

The "starting" code point is reported as where the "font" ''would'' begin if
it were all there. Thus, the "PARENTHESIZED" Latin digits are listed as
beginning at U+02473 even though U+2473 is actually "CIRCLED NUMBER TWENTY".
But the script knows there is no "PARENTHESIZED DIGIT ZERO", and will
leave "0" untranslated in this case.

==convert(s, script="Latin", font="Bold")==

Just convert characters in the string `s` that are from the given "script" to the specified "font".

For "Latin", uppercase, lowercase, and digits are converted (when available).

For "Greek", uppercase and lowercase are converted (when available).

For "Digits", only digits 0-9 are converted (and only when available).

==getTranslateTable(script="Latin", font="BOLD")==

Return a Python 3 translation table generated for the specified `script`
and `font`. Exceptions are integrated, and omissions are omitted.

==makePartialXtab(srcStart, srcEnd, tgtStart)==


=Related Commands=

My `ord --math` will display a list of these characters.


=Known bugs and Limitations=

You can't specify "font" -names with re-ordered tokens. For example,
"BOLD FRAKTUR" (regardless of case) works, but not "FRAKTUR BOLD".

With `--makeHtmlComparison`, the generated HTML includes a few custom elements,
with styles applied via <head>:

    sans            { font-family:sans-serif; }
    serif           { font-family:serif; }
    cursive         { font-family:cursive; }
    monospace       { font-family:monospace; }

Modern browsers are fine with this, but it's not precisely "HTML". If that's a problem,
change them to something like '<span class="sans">', etc. Or better, change the
DOCTYPE to reference a schema that adds them.

The `--family` choice (if any) is applied to <body>, so these will override if for
the appropriate cases (I don't know what happens, for example, if you specify
a cursive font for --family, and then the SCRIPT row applies cursive on top of it --
perhaps it notices it's already cursive and keeps the active one; or perhaps it does
its own search and gives you the first one it finds.


==Script-specific issues

I'm note sure what "REGIONAL INDICATOR SYMBOL" is for -- it comes up as
flags on some systems; if that's normal it should be dropped here.

Many scripts that use accented Latin or Greek characters, do not have accents
on all characters. So if you don't decompose first (discussed above), you'll
get only '''some''' of the characters translated.

Cannot translate multiple scripts simultaneously.

Punctuation is not yet supported, such as superscript and subscript
parentheses, plus, minus, etc. For many of the (pseudo-) fonts it might not
make sense anyway; but for some it does.

Superscript, subscript, turned, and strikethrough are not finished.

Non-Latin digit series are not well integrated or tested.

Numbers > 9 (such as for roman numerals, circled numbers, etc.) are not supported.

"Modifier letters" are not supported.

This package does not provide a way to translate the various alternate
sets back to plain Latin or Greek or Digits. However, this can be done
pretty well with Unicode "compatibility decomposition":

    import unicodedata
    s = unicodedata.normalize("NFKD", s)

[https://www.unicode.org/reports/tr25/tr25-6.html#_Toc2] notes that the
Mathematical Greek sets include several less-used characters,
such as uppercase nabla (U+2207) and a variant of theta (U+03F4);
and lowercase partial differential sign (U+2202) and glyph variants of
epsilon (U+03F5), theta (U+03D1), kappa (U+03F0),
phi (U+03D5), rho (U+03F1), and pi (U+03D6).
They are not supported here (yet).

==Issues outside the script's control==

If the display environment doesn't handle Unicode, or the font in use has
problems with any of the characters needed, the result may not be ideal.

Unicode intends most of these characters for special mathematical uses, such
as ensuring that you get the fancy "R" (U+0211d), which is used to refer to
the set of real numbers because the set takes too long write out in full. Using
these characters for formatting is a little weird. But Gæð a wyrd swa hio scel.

Sets such as MATHEMATICAL ITALIC are generally defined in Unicode as a contiguous
range, but occasionally one or a few members are somewhere else
(such as MATHEMATICAL ITALIC SMALL H), and the "expected" slot among
the rest of the letter is left undefined. In practice, this also means that
Unicode fonts do not always define quite the same "look" to those  characters.
It strikes me that leaving those slots blank is mainly useful because it
slightly simplifies programs like this: ones that want to translate the entire
block rather than particular characters like

Monospace fonts for Unicode may not always display with all the characters the
same width. "FULLWIDTH" may pose similar problems.
Also, "MONOSPACE" is not very distinctive on terminals that always use monospace
anyway.

"SANS-SERIF" is not very distinctive if your default font is that way.

"SCRIPT" may look a lot like italic, especially to the unpracticed eye.

The implementation here knows where
the ranges start, and then has a list of "exceptions" (in a class variable
of that name). There is an edge case when the ''first'' character of the
range does not exist, or exists but is exceptional. In such cases, the code
treats the range as beginning at where the first character *would* be if it
were not missing or an exception. This ''may'' lead to problems if your data
contains that character.

For example, PARENTHESIZED DIGIT ONE is U+2474, so we would expect the ZERO
at U+2473. But U+2473 is CIRCLED NUMBER TWENTY. This package takes the
exceptions into account when building a translation table. When the character
is entirely missing (as in this example), the "basic" character (in this
case "1") is left unchanged (it is not even added to the translation table.

Characters with diacritics must be decomposed first, because the specialized
"fonts" do not generally include composed characters. To decompose
(that is, to split off the diacritic to a separate overstruck character),
do this in Python:

    import unicodedata
    s = unicodedata.normalize("NFD", s)


=Notes=

Using Unicode Mathematical characters to achieve formatting may be slightly odd,
but alternatives are limited given current terminal and shell technology,
which typically support Unicode but not font-changes or
effects (other than ANSI terminal color and effect escapes).

Some additional scripts and forms are not supported:

    Some squared CJK
    Parenthesized ideographs, Hangul, and Korean characters.
    Circled italic latin (missing C, R)
    Double-Struck Italic (missing D, e, i, j)
    Squared Latin (only Small Letter D?)
    Old Italic letters at U+10300 and following
    circled katakana U+032d0
    some circled hangul and ideographs U+3260
    circled number X on black square U+3248

    aeox schwa hklmnpst; i=1d62, r=1d63, u=1d64, v=1d65, j=2c7c
    [ "subscript latin upper (...209c)", 0x02090 ],
and suppl for rest of lc latin except jqy (seriously???)
      spacing modifier letters a few
      phonetic extensions has some latin/cyr/ipa
    2145-2149 double struck italics???
    213c-40 double struck pi, gamma, sigma
    (couple extras at 1d6a4, dotless i, j)
    213c-40 double struck pi, gamma, sigma


=History=

# Written sometime before 2006-10-04, by Steven J. DeRose.
* 2008-02-11 sjd: Add `--perl`, `perl -w`.
* 2008-09-03 sjd: BSD. Improve doc, error-checking, fix bug in `-all`.
* 2010-03-28 sjd: perldoc. Add [] to `-ps`.
* 2010-09-20ff sjd: Cleanup. Add `--color`; ls and dircolors support. Simplify
numeric handling of codes. Support color combinations. Add `-setenv`.
Change 'fg2_' prefix to 'bold_' and factor out of code.
* 2013-06-11: Add `--xterm256`, but just for `--list`.
* 2013-06-27: Add `--table`. Ditch "fg2_" and "b_" prefixes.
* 2014-07-09: Clean up doc. Add `--python`. Clean up `--perl`. fix `--list`.
* 2015-02-04: Support rest of effects beyond bold.
* 2015-08-25: Start syncing color-refs with sjdUtils.pm.
* 2016-01-01: Get rid of extraneous final newline with `-m`.
* 2016-07-21: Merge doc on color names w/ sjdUtils.p[my], etc.
* 2016-10-25: Clean up to integrate w/ ColorManager. Change names.
Debug new (hashless) way of doing colors.
* 2018-08-29: Port to Python.
* 2018-08-29ff: Split from Perl colorstring, and Ported.
* 2018-09-04: Merged from incomplete `UnicodeAltLatin.py`
* 2020-07-25: Lose remaining upper/lower separations. Big cleanup.
Support complete upper/lower/digit translation tables. Add `--test`.
Add support for in-pipe translation.
* 2020-09-03: Improve translation-table construction.
* 2021-02-18: Fix bug that dropped part of translate tables.
* 2021-02-23: Add option for Unicode normalization.
* 2021-12-20: Add --makeHtmlComparison. Add type hints.
* 2022-01-07: Add SMALLCAP, SUBSCRIPT, SUPERSCRIPT, ROTATED, UNDERLINE, DUNDERLINE,
OVERLINE, DOVERLINE, STRIKE, SLASHED, DSLASHED.


=To do=

* Cleaner way to request, like splitting out bold and italic -- though
you only get the full set of { roman, bold, italic, bold-italic } for
plain and sans-serif.

* Perhaps add feature to turn markup into fonts -- such as
    <i> ITALIC
    <b> BOLD
    <tt> MONOSPACE
         SANS SERIF
    <sub> SUBSCRIPT
    <sup> SUPERSCRIPT

But what of FRAKTUR, DOUBLE-STRUCK, SCRIPT, FULLWIDTH, and the enclosed ones? <span?>

* Better testing for non-Latin digits.

* Possibly add combining characters such as underscore, strike-through, and
overline. There's even COMBINING ENCLOSING CIRCLE (and SQUARE).

* Greek has some turned letters, too:
    "a":  chr(0x00252),  #  A  chr(0x2C6F)
    "b":            #
    "g":            #
    "d":  chr(0x0018D),  #  D  chr(0x2207) nabla
    "e":  chr(0x01D08),
    "z":            # =Zeta
    "h":            #  =Eta
    "q":            #  =Theta
    "i":  chr(0x02129),   # Iota
    "k":  chr(0x0029e),   # chr(0x0029e) LATIN SMALL LETTER TURNED K
    "l":            #  V
    "m":  chr(0x0019c),   # LATIN CAPITAL LETTER TURNED M
    "n":  chr(0x0028c),   #LATIN SMALL LETTER TURNED V
    "c":            #
    "o":            #  =Omicron
    "p":            #
    "r":            # ~~~d~~~
    "s":            #
    "t":            # =Tau
    "u":            # =Upsilon
    "f":  phi       # =Phi
    "x":  xi        # =Xi
    "ps":           #
    "w":            #

* Quarter-turned instead of half?
    "q":   # q CCW
    "q":   # m CW   chr(0x01d1f)

* Possibly add turned (cf reversed), using:
    Problem: there isn't a reserved range for these
    --- uppercase ---
        A U+02c6f LATIN CAPITAL LETTER TURNED A
        B                                          ???
        C                                          ???
        D                                          ???
        E => exists  U+02c7b(smallcap)
        F U+02132 TURNED CAPITAL F
        G U+02141 TURNED SANS-SERIF CAPITAL G
        H U+0a78d LATIN CAPITAL LETTER TURNED H (why is this not itself?)
        I => I
        J ?                                        ???
        K ?                                        ???
        L => U+0a780 LATIN CAPITAL LETTER TURNED L
        #U+02142 TURNED SANS-SERIF CAPITAL L
        M => U+0019c LATIN CAPITAL LETTER TURNED M
        N => N
        O => O
        P =>  ~~~d~~~                               ??? eth?
        Q =>                                        ???
        R =>                                        ??? U+01d1a	Latin Letter Small Capital Turned R
        S => S
        T =>                                        ???
        U => U+2229 intersection?
        V => U+00245 LATIN CAPITAL LETTER TURNED V
        W => ~~~M~~~                                ???
        X => X
        Y => U+02144 TURNED SANS-SERIF CAPITAL Y
        Z => Z                                      ???

        --- lowercase ---
        a => U+00250 LATIN SMALL LETTER TURNED A
        b => q
        c => U+02184 LATIN SMALL LETTER REVERSED C
        d => p
        e => U+001dd LATIN SMALL LETTER TURNED E (or e => schwa)
        f => U+0214e TURNED SMALL F
        g => U+01d77 LATIN SMALL LETTER TURNED G
        h => U+00265 LATIN SMALL LETTER TURNED H
        i => U+01d09 LATIN SMALL LETTER TURNED I
        j => medial s?
        k => U+0029e LATIN SMALL LETTER TURNED K
        l => U+0a781 LATIN SMALL LETTER TURNED L
        m => U+0026f LATIN SMALL LETTER TURNED M
        n => u
        o = o
        p => d
        q => b
        r => U+00279 LATIN SMALL LETTER TURNED R
        s = s
        t => U+00287 LATIN SMALL LETTER TURNED T
        u => n
        v => U+0028c LATIN SMALL LETTER TURNED V
        w => U+0028d LATIN SMALL LETTER TURNED W
        x = x
        y => U+0028e LATIN SMALL LETTER TURNED Y
        z = z

* Possibly add reversed (horizontally)
    --- uppercase ---
    "A":  "A",
    "B":                                     ???
    "C":  chr(0x02183),  # ROMAN NUMERAL REVERSED ONE HUNDRED
    "D":
    "E":  chr(0x0018e),  # LATIN CAPITAL LETTER REVERSED E
    "F":
    "G":
    "H":  "H",
    "I":  "I",
    "J":
    "K":
    "L":  chr(0x02143),  # REVERSED SANS-SERIF CAPITAL L
    "M":  "M",
    "N":
    "O":  "O",
    "P":  chr(0x0a7fc),   # LATIN EPIGRAPHIC LETTER REVERSED P
    "Q":
    "R":
    "S": # https://en.wikipedia.org/wiki/%C6%A7
    "T":  "T",
    "U":  "U",
    "V":  "V",
    "W":  "W",
    "X":  "X",
    "Y":  "Y",
    "Z":

    --- lowercase ---
    "a":
    "b":  "d",
    "c":  chr(0x02184),  # LATIN SMALL LETTER REVERSED C
    "d":  "b",
    "e":  chr(0x00258),  # LATIN SMALL LETTER REVERSED E
    "f":
    "g":
    "h":
    "i":  "i",
    "j":
    "k":
    "l":  "l",
    "m":  m?
    "n":  n?
    "o":  "o",
    "p":  "q",
    "q":  "p",
    "r":  chr(0x0027f),  # LATIN SMALL LETTER REVERSED R WITH FISHHOOK
    "s":
    "t":
    "u":  u?
    "v":  "v",
    "w":  "w",
    "x":  "x",
    "y":
    "z":

* Hook up smallCapMap (missing Q and X)

* Possibly add superscript
    "i":  chr(0x02071),  # SUPERSCRIPT LATIN SMALL LETTER I
    "n":  chr(0x0207f),  # SUPERSCRIPT LATIN SMALL LETTER N

* Non-alphanumeric variants: punctuation, esp. for superscript and subscript


=Rights=

Copyright 2006 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
For further information on this license, see
[https://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
#
def warn(lvl, msg):
    if (args.verbose >= lvl): sys.stderr.write(msg + "\n")
    if (lvl < 0): sys.exit()


###############################################################################
# Support Unicode alternate forms of Latin alphabet
# Greek and digits also defined for some of these
# See also bin/data/unicodeLatinAlphabets.py
#
class mathAlphanumerics:
    oneHotFeatures = [
        "Fullwidth", "Script", "Fraktur", "Double-Struck", "Sans-serif",
        "Monospace", "Parenthesized", "Circled", "Squared",
        "Negative-circled", "Negative-squared", "Regional symbol"
    ]

    # These are the "fonts" available as Unicode "Mathematical" variations on
    # Latin. A similar list is available for Greek, and for digits.
    # NOTE: "MATHEMATICAL is omitted for compactness.
    #
    LatinFontDict = {
        ####### Following are "Mathematical":
        # Name                       ( Upper    Lower,   Digits   Exceptions )
        "BOLD":                      ( 0x1d400, 0x1d41a, 0x1d7ce, "" ),
        "ITALIC":                    ( 0x1d434, 0x1d44e, None,    "h" ),
        "BOLD ITALIC":               ( 0x1d468, 0x1d482, None,    "" ),

        "SANS-SERIF":                ( 0x1d5a0, 0x1d5ba, 0x1d7e2, "" ),
        "SANS-SERIF BOLD":           ( 0x1d5d4, 0x1d5ee, 0x1d7ec, "" ),
        "SANS-SERIF ITALIC":         ( 0x1d608, 0x1d622, None,    "" ),
        "SANS-SERIF BOLD ITALIC":    ( 0x1d63c, 0x1d656, None,    "" ),

        "SCRIPT":                    ( 0x1d49c, 0x1d4b6, None, "BEFHILMR ego"),
        "BOLD SCRIPT":               ( 0x1d4d0, 0x1d4ea, None,    "" ),

        "FRAKTUR":                   ( 0x1d504, 0x1d51e, None,    "CHIRZ" ),
        "BOLD FRAKTUR":              ( 0x1d56c, 0x1d586, None,    "" ),

        "DOUBLE-STRUCK":             ( 0x1d538, 0x1d552, 0x1d7d8, "CHNPQRZ" ),
        "MONOSPACE":                 ( 0x1d670, 0x1d68a, 0x1d7f6, "" ),

        ####### Following aren't "Mathematical":

        "CIRCLED":                   ( 0x024b6, 0x024d0, 0x0245f, "" ),
        "PARENTHESIZED":             ( 0x1f110, 0x0249c, 0x02473, "" ),
        "FULLWIDTH":                 ( 0x0FF21, 0x0FF41, 0x0FF10, "" ),

        ####### Not available in lower case:

        "SQUARED":                   ( 0x1f130, None,    None,    "" ),
        "NEGATIVE SQUARED":          ( 0x1f170, None,    None,    "" ),
        "REGIONAL INDICATOR SYMBOL": ( 0x1f1e6, None,    None,    "" ),  # ???
        "NEGATIVE CIRCLED":          ( 0x1f150, None,    None,    "" ),  # 0x02775 ???
        "SUPERSCRIPT":               ( None,    None,    0x02070, "123" ),
        "SUBSCRIPT":                 ( None,    None,    0x02080, "" ),

        ####### Unfinished:
        #"Subscript Latin Small"   : [],  # aehijklmnoprstuvx
    }

    GreekFontDict = {
        "BOLD":                       ( 0X1D6A8, 0X1D6C2, None, "" ),
        "ITALIC":                     ( 0X1D6E2, 0X1D6FC, None, "" ),
        "BOLD ITALIC":                ( 0X1D71C, 0X1D736, None, "" ),
        "SANS-SERIF BOLD":            ( 0X1D756, 0X1D770, None, "" ),
        # No Mathematical Greek Sans Serif Italic, apparently?
        "SANS-SERIF BOLD ITALIC":     ( 0X1D790, 0X1D7AA, None, "" ),

        ########## Unfinished:
        #"SUPERSCRIPT GREEK SMALL":   (),
        #"SUBSCRIPT GREEK SMALL":     (),
    }

    # Some of these sets lack a zero. in those cases the set is listed as
    # beginning where the zero *would* be naturally -- just before the 1.
    # TODO: Delete ones redundant with Latin list above
    #
    DigitFontDict = {
        # [ NAME                          UC    LC    DIGITS   exceptions ]
        # These are covered above:
        "BOLD":                         [ None, None, 0x1d7Ce, "" ],
        # no italic or bold italic
        "SANS SERIF":                   [ None, None, 0x1d7e2, "" ],
        "SANS SERIF BOLD":              [ None, None, 0x1d7ec, "" ],
        # no sans serif italic or bold italic
        # no script or fraktur
        "DOUBLE STRUCK":                [ None, None, 0x1d7d8, "" ],
        "MONOSPACE":                    [ None, None, 0x1d7f6, "" ],

        "FULLWIDTH":                    [ None, None, 0x0ff110, "" ],

        # no squared, negative squared, or regional indicator symbol
        #"NEGATIVE CIRCLED":             [ None, None, 0x024eb, "0" ],
        "SUPERSCRIPT LATIN":            [ None, None, 0x02070, "" ],
        "SUBSCRIPT LATIN":              [ None, None, 0x02080, "" ],

        "DIGIT COMMA":                  [ None, None, 0x1f101, "" ],
        "DIGIT FULL STOP":              [ None, None, 0x02488, "" ],

        # Starting at 1 (but offset is to where zero *would* be)
        "CIRCLED":                      [ None, None, 0x0245f, "0" ],
        "DINGBAT NEGATIVE CIRCLED":     [ None, None, 0x02775, "0" ],
        "DOUBLE CIRCLED":               [ None, None, 0x024f3, "0" ],
        "PARENTHESIZED":                [ None, None, 0x02473, "0" ],

        "FULL STOP":                    [ None, None, 0x02487, "0" ],
        "DINGBAT CIRCLED SANS-SERIF":   [ None, None, 0x0277f, "0" ],
        "DINGBAT NEGATIVE CIRCLED SANS-SERIF": [ None, None, 0x02789, "0" ],

        # circled number on black square 10-80 by 10 @ U+03248, 0 @ ????

        "ARABIC-INDIC":                 [ None, None, 0x00660, "" ],
        "EXTENDED ARABIC-INDIC":        [ None, None, 0x006F0, "" ],
        "NKO":                          [ None, None, 0x007c0, "" ],
        "DEVANAGARI":                   [ None, None, 0x00966, "" ],
        "BENGALI":                      [ None, None, 0x009e6, "" ],
        "GURMUKHI":                     [ None, None, 0x00a66, "" ],
        "GUJARATI":                     [ None, None, 0x00aE6, "" ],
        "ORIYA":                        [ None, None, 0x00b66, "" ],
        "TAMIL":                        [ None, None, 0x00bE6, "" ],
        "TELUGU":                       [ None, None, 0x00c66, "" ],
        "KANNADA":                      [ None, None, 0x00cE6, "" ],
        "MALAYALAM":                    [ None, None, 0x00d66, "" ],
        "SINHALA LITH":                 [ None, None, 0x00dE6, "" ],
        "THAI":                         [ None, None, 0x00E50, "" ],
        "LAO":                          [ None, None, 0x00Ed0, "" ],
        "TIBETAN":                      [ None, None, 0x00f20, "" ],
        "MYANMAR":                      [ None, None, 0x01040, "" ],
        "MYANMAR SHAN":                 [ None, None, 0x01090, "" ],
        "KHMER":                        [ None, None, 0x017e0, "" ],
        "MONGOLIAN":                    [ None, None, 0x01810, "" ],
        "LIMBU":                        [ None, None, 0x01946, "" ],
        "NEW TAI LUE":                  [ None, None, 0x019d0, "" ],
        "TAI THAM HORA":                [ None, None, 0x01a80, "" ],
        "TAI THAM THAM":                [ None, None, 0x01a90, "" ],
        "BALINESE":                     [ None, None, 0x01b50, "" ],
        "SUNDANESE":                    [ None, None, 0x01bb0, "" ],
        "LEPCHA":                       [ None, None, 0x01c40, "" ],
        "OL CHIKI":                     [ None, None, 0x01c50, "" ],
        "IDEOGRAPHIC NUMBER":           [ None, None, 0x03007, "" ],
        "VAI":                          [ None, None, 0x0a620, "" ],
        "SAURASHTRA":                   [ None, None, 0x0a8d0, "" ],
        "COMBINING DEVANAGARI":         [ None, None, 0x0a8e0, "" ],
        "KAYAH LI":                     [ None, None, 0x0a900, "" ],
        "JAVANESE":                     [ None, None, 0x0a9d0, "" ],
        "CHAM":                         [ None, None, 0x0aa50, "" ],
        "MEETEI MAYEK":                 [ None, None, 0x0abf0, "" ],

        # Some other related sets
        "ROMAN NUMERAL":                [ None, None, 0x0215f,   "0" ],
        "SMALL ROMAN NUMERAL":          [ None, None, 0x0216f,   "0" ],

        "PLAYING CARDS, SPADE":         [ None, None, 0x1f0a0,   "0" ],
        "PLAYING CARDS, HEART":         [ None, None, 0x1f0b0,   "0" ],
        "PLAYING CARDS, DIAMOND":       [ None, None, 0x1f0c0,   "0" ],
        "PLAYING CARDS, CLUB":          [ None, None, 0x1f0d0,   "0" ],

        "MAHJONG TILES, CHARACTER":     [ None, None, 0x1f006,   "0" ],
        "MAHJONG TILES, BAMBOO":        [ None, None, 0x1f00f,   "0" ],
        "MAHJONG TILES, CIRCLE":        [ None, None, 0x1f018,   "0" ],
    } # digitSets

    # Map from expected but undefined code points, to where the char really is
    #
    exceptions = {
        # expect  actual    name
        0X02071: 0X000B9, # SUPERSCRIPT LATIN DIGIT ONE
        0X02072: 0X000B2, # SUPERSCRIPT LATIN DIGIT TWO
        0X02073: 0X000B3, # SUPERSCRIPT LATIN DIGIT THREE
        #
        0X1D455: 0X210E,  # MATHEMATICAL ITALIC SMALL H (PLANCK CONSTANT)
        0X1D49D: 0X212C,  # MATHEMATICAL SCRIPT CAPITAL B
        0X1D4A0: 0X2130,  # MATHEMATICAL SCRIPT CAPITAL E
        0X1D4A1: 0X2131,  # MATHEMATICAL SCRIPT CAPITAL F
        0X1D4A3: 0X210B,  # MATHEMATICAL SCRIPT CAPITAL H
        0X1D4A4: 0X2110,  # MATHEMATICAL SCRIPT CAPITAL I
        0X1D4A7: 0X2112,  # MATHEMATICAL SCRIPT CAPITAL L
        0X1D4A8: 0X2133,  # MATHEMATICAL SCRIPT CAPITAL M
        0X1D4AD: 0X211B,  # MATHEMATICAL SCRIPT CAPITAL R
        0X1D4BA: 0X212F,  # MATHEMATICAL SCRIPT SMALL E
        0X1D4BC: 0X0261,  # MATHEMATICAL SCRIPT SMALL G
        0X1D4C4: 0X2134,  # MATHEMATICAL SCRIPT SMALL O
        0X1D506: 0X212D,  # MATHEMATICAL FRAKTUR CAPITAL C
        0X1D50B: 0X210C,  # MATHEMATICAL FRAKTUR CAPITAL H
        0X1D50C: 0X2111,  # MATHEMATICAL FRAKTUR CAPITAL I
        0X1D515: 0X211C,  # MATHEMATICAL FRAKTUR CAPITAL R
        0X1D51D: 0X2128,  # MATHEMATICAL FRAKTUR CAPITAL Z
        0X1D53A: 0X2102,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL C
        0X1D53F: 0X210D,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL H
        0X1D545: 0X2115,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL N
        0X1D547: 0X2119,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL P
        0X1D548: 0X211A,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL Q
        0X1D549: 0X211D,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL R
        0X1D551: 0X2124,  # MATHEMATICAL DOUBLE-STRUCK CAPITAL Z

        # Missing or displaced zeros in digit sets (re-check)
        0x0245f: 0x024ea,  # CIRCLED DIGIT ZERO
        0x02774: 0x024ff,  # DINGBAT NEGATIVE CIRCLED DIGIT ZERO
        0x024f4: None,     # DOUBLE CIRCLED DIGIT ZERO
        0x02789: None,     # DINGBAT CIRCLED SANS-SERIF DIGIT ZERO
        0x02775: None,     # DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT ZERO
        0x02473: None,     # PARENTHESIZED ???  DIGIT ZERO
        0x024eb: 0x024ff,  # NEGATIVE CIRCLED DIGIT ZERO
        0x02488: 0x1f100,  # FULL STOPPED DIGIT ZERO
        0x024f5: None   ,  # DOUBLE CIRCLED DIGIT ZERO
        0x02780: 0x1f10b,  # DINGBAT CIRCLED SANS-SERIF DIGIT ZERO
        0x02776: 0x024ff,  # DINGBAT NEGATIVE CIRCLED DIGIT ZERO
        0x0278a: 0x1f10c,  # DINGBAT NEGATIVE CIRCLED SANS-SERIF DIGIT ZERO
        #
        0x02160: None,     # ROMAN NUMERALS DIGIT ZERO
        0x02170: None,     # SMALL ROMAN NUMERALS DIGIT ZERO
        0x1f0a1: None,     # PLAYING CARDS, SPADES DIGIT ZERO
        0x1f0b1: None,     # PLAYING CARDS, HEARTS DIGIT ZERO
        0x1f0c1: None,     # PLAYING CARDS, DIAMONDS DIGIT ZERO
        0x1f0d1: None,     # PLAYING CARDS, CLUBS DIGIT ZERO
        0x1f007: None,     # MAHJONG TILES, CHARACTERS DIGIT ZERO
        0x1f010: None,     # MAHJONG TILES, BAMBOOS DIGIT ZERO
        0x1f019: None,     # MAHJONG TILES, CIRCLES DIGIT ZERO

    }

    # Small caps should probably just apply to lowercase?
    smallCapMap = {
        "a": 0x01d00,  # LATIN LETTER SMALL CAPITAL A
        "b": 0x00299,  # LATIN LETTER SMALL CAPITAL B  (far)
        "c": 0x01d04,  # LATIN LETTER SMALL CAPITAL C
        "d": 0x01d05,  # LATIN LETTER SMALL CAPITAL D
        "e": 0x01d07,  # LATIN LETTER SMALL CAPITAL E
        "f": 0x0a730,  # LATIN LETTER SMALL CAPITAL F  (far) Unicode 5.1 (2008)
        "g": 0x00262,  # LATIN LETTER SMALL CAPITAL G  (far)
        "h": 0x0029c,  # LATIN LETTER SMALL CAPITAL H  (far)
        "i": 0x0026a,  # LATIN LETTER SMALL CAPITAL I  (far)
        "j": 0x01d0a,  # LATIN LETTER SMALL CAPITAL J
        "k": 0x01d0b,  # LATIN LETTER SMALL CAPITAL K
        "l": 0x0029f,  # LATIN LETTER SMALL CAPITAL L  (far)
        "m": 0x01d0d,  # LATIN LETTER SMALL CAPITAL M
        "n": 0x00274,  # LATIN LETTER SMALL CAPITAL N  (far)
        "o": 0x01d0f,  # LATIN LETTER SMALL CAPITAL O
        "p": 0x01d18,  # LATIN LETTER SMALL CAPITAL P
        "q": 0x0A7Af,  # LATIN LETTER SMALL CAPITAL Q  (far) Unicode 11.0 (2018?)
        "r": 0x00280,  # LATIN LETTER SMALL CAPITAL R  (far)
        "s": 0x0a731,  # LATIN LETTER SMALL CAPITAL S  (far) Unicode 5.1 (2008)
        "t": 0x01d1b,  # LATIN LETTER SMALL CAPITAL T
        "u": 0x01d1c,  # LATIN LETTER SMALL CAPITAL U
        "v": 0x01d20,  # LATIN LETTER SMALL CAPITAL V
        "w": 0x01d21,  # LATIN LETTER SMALL CAPITAL W
        #"x": None,
        "y": 0x0028f,  # LATIN LETTER SMALL CAPITAL Y  (far)
        "z": 0x01d22,  # LATIN LETTER SMALL CAPITAL Z
    }

    # https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts#Uses,
    subscriptMap = {
        "a": 0x02090,  # LATIN SUBSCRIPT SMALL LETTER A
        #"b"    beta?
        #"c"
        #"d"
        "e": 0x02091,  # LATIN SUBSCRIPT SMALL LETTER E
        #"f"
        #"g"
        "h": 0x02095,  # LATIN SUBSCRIPT SMALL LETTER H (MISSING on MAC?)... through T
        "i": 0x01d62,  # LATIN SUBSCRIPT SMALL LETTER I  (far)
        "j": 0x02c7c,  # LATIN SUBSCRIPT SMALL LETTER J  (far)
        "k": 0x02096,  # LATIN SUBSCRIPT SMALL LETTER K
        "l": 0x02097,  # LATIN SUBSCRIPT SMALL LETTER L
        "m": 0x02098,  # LATIN SUBSCRIPT SMALL LETTER M
        "n": 0x02099,  # LATIN SUBSCRIPT SMALL LETTER N
        "o": 0x02092,  # LATIN SUBSCRIPT SMALL LETTER O
        "p": 0x0209a,  # LATIN SUBSCRIPT SMALL LETTER P
        #"q"
        "r": 0x01d63,  # LATIN SUBSCRIPT SMALL LETTER R  (far)
        "s": 0x0209b,  # LATIN SUBSCRIPT SMALL LETTER S
        "t": 0x0209c,  # LATIN SUBSCRIPT SMALL LETTER T
        "u": 0x01d64,  # LATIN SUBSCRIPT SMALL LETTER U  (far)
        "v": 0x01d65,  # LATIN SUBSCRIPT SMALL LETTER V  (far)
        #"w"
        "x": 0x02093,  # LATIN SUBSCRIPT SMALL LETTER X  (far)
        #"y"
        #"z"
    }

    # Greek subscripts: bgrfx 0x1d62...0x1d6a aeoxhklmnpst

    # combining diacriticals marks has aeioucdhmrtvx

    # See https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts
    # Combining Diacritical Marks Supplement has most of the rest, but
    #     we"d need to insert something to place them over
    # Phonetic Extensions and  Phonetic Extensions Supplement have a bunch
    superscriptMap = {  # and +-=()
        #"a":  Feminine ordinal indicator
        "i": 0x02071,
        "n": 0x0207f,
        #"o":  Masculine ordinal indicator
        #"v":  In LAtin Extended-C
    }

    # Turned/rotated characters. Uppercase are mainly based on "Fraser" orthography,
    # for "Lisu" script.
    #
    lisuMap = {
        #                   # Name, alternatives?
        "A":   0x0a4ef,     # U+02c6f LATIN CAPITAL LETTER TURNED A
        "B":   0x0a4ed,     #
        "C":   0x0a4db,     #
        "D":   0x0a4f7,     #
        "E":   0x0a4f1,     # exists  U+02c7b(smallcap)
        "F":   0x0a4de,     # U+02132 TURNED CAPITAL F
        "G":   0x0a4e8,     # U+02141 TURNED SANS-SERIF CAPITAL G
        "H":   0x0a4e7,     # SAME ROTATED
        "I":   0x0a4f2,     # SAME ROTATED
        "J":   0x0a4e9,     #
        "K":   0x0a4d8,     #
        "L":   0x0a4f6,     # U+0a780 LATIN CAPITAL LETTER TURNED L, U+02142 TURNED SANS-SERIF CAPITAL L
        "M":   0x0019c,     # MISSING, USING U+0019c LATIN CAPITAL LETTER TURNED M
        "N":   0x0a4e0,     # SAME ROTATED
        "O":   0x0a4f3,     # SAME ROTATED
        "P":   0x0a4d2,     # Use d?
        "Q":   0x0a779,     # MISSING (cf 1/4-turn U+213A; U+0a779 LATIN CAPITAL LETTER INSULAR D)
        "R":   0x0a4e4,     # cf U+01d1a Latin Letter Small Capital Turned R
        "S":   0x0a4e2,     # SAME ROTATED
        "T":   0x0a4d5,     #
        "U":   0x0a4f5,     # cf U+2229 intersection?
        "V":   0x0a4e5,     # U+00245 LATIN CAPITAL LETTER TURNED V
        "W":   ord('M'),    # MISSING, ROTATED 'M'
        "X":   0x0a4eb,     # SAME ROTATED
        "Y":   0x02144,     # MISSING, USING U+02144 TURNED SANS-SERIF CAPITAL Y
        "Z":   0x0a4dc,     # SAME ROTATED
        #
        # turned/rotated lowercase ---
        "a":   0x00250,     # LATIN SMALL LETTER TURNED A
        "b":   ord("q"),    #
        "c":   0x02184,     # LATIN SMALL LETTER REVERSED C
        "d":   ord("p"),    #
        "e":   0x001dd,     # LATIN SMALL LETTER TURNED E (or"e":   schwa)
        "f":   0x0214e,     # TURNED SMALL F
        "g":   0x01d77,     # LATIN SMALL LETTER TURNED G
        "h":   0x00265,     # LATIN SMALL LETTER TURNED H
        "i":   0x01d09,     # LATIN SMALL LETTER TURNED I
        "j":   ord("m"),    # edial s?
        "k":   0x0029e,     # LATIN SMALL LETTER TURNED K
        "l":   0x0a781,     # LATIN SMALL LETTER TURNED L
        "m":   0x0026f,     # LATIN SMALL LETTER TURNED M
        "n":   ord("u"),    #
        "o":   ord("o"),    #
        "p":   ord("d"),    #
        "q":   ord("b"),    #
        "r":   0x00279,     # LATIN SMALL LETTER TURNED R
        "s":   ord("s"),    #
        "t":   0x00287,     # LATIN SMALL LETTER TURNED T
        "u":   ord("n"),    #
        "v":   0x0028c,     # LATIN SMALL LETTER TURNED V
        "w":   0x0028d,     # LATIN SMALL LETTER TURNED W
        "x":   ord("x"),    #
        "y":   0x0028e,     # LATIN SMALL LETTER TURNED Y
        "z":   ord("z"),    #
        #
        # See also [https://text-symbols.com/upside-down]
        # "0": ord("0"),    # SAME
        # "1":      # IOTA?
        # "2": 0x0218A,     # turned digit two
        # "3": 0x0218B,     # turned digit three, latin capital letter open e - backwards 3 flipped (u+0190)
        # "4": 0x0152d,     # canadian syllabics ya (u+152d)
        # "5": ord("5"),    # Close to same
        # "6": ord("9"),    # => 9
        # "7":              # MATHEMATICAL SANS-SERIF ITALIC CAPITAL L ?
        # "8": ord("8"),    # Close to same
        # "9": ord("6"),    # => 6
        #
        # "?": 0x000BF,     # iquest
        # "!": 0x000A1,
        # "&": 0x0214B,
        # most mirrored chars...
    }

    # TODO: Finish alternate sets that are trickier.
    #
    # Combing-char effects
    # These can't be done by handing back a translate table.
    # Also "TURNED", which can be done just as exceptions.
    #
    specialDict = {
        # Name               Char
        "SMALLCAP":         smallCapMap,
        "SUBSCRIPT":        subscriptMap,
        "SUPERSCRIPT":      superscriptMap,
        "ROTATED":          lisuMap,
    }

    # A few more can be made by composing a combining character with the base
    # TODO: Perhaps add an option to add any combining character one likes?
    combinerDict = {
        "UNDERLINE":        chr(0x00332),  # COMBINING LOW LINE
        "DUNDERLINE":       chr(0x00333),  # COMBINING DOUBLE LOW LINE
        "OVERLINE":         chr(0x00305),  # COMBINING OVERLINE
        "DOVERLINE":        chr(0x0033F),  # COMBINING DOUBLE OVERLINE
        "STRIKE":           chr(0x00336),  # COMBINING LONG STROKE OVERLAY
        "SLASHED":          chr(0x00338),  # COMBINING LONG SOLIDUS OVERLAY
        "DSLASHED":         chr(0x020EB),  # COMBINING LONG DOUBLE SOLIDUS OVERLAY
        # U+020dd    COMBINING ENCLOSING CIRCLE
        # U+020de    COMBINING ENCLOSING SQUARE
        # U+020e5    COMBINING REVERSE SOLIDUS OVERLAY
        # U+020df    COMBINING ENCLOSING DIAMOND
        # U+020e0    COMBINING ENCLOSING CIRCLE BACKSLASH
        # U+020e2    COMBINING ENCLOSING SCREEN
        # U+020e3    COMBINING ENCLOSING KEYCAP
        # U+020e4    COMBINING ENCLOSING UPWARD POINTING TRIANGLE
    }


    ###########################################################################
    # Maybe make init take a target spec, then convert() uses it...
    #
    def __init__(self):
        return

    @staticmethod
    def getStartCodePoint(script: str = "Latin", font: str = "BOLD", group: str = "U"):
        font = re.sub(r"^MATHEMATICAL ", "M", font.upper())
        fontDict = mathAlphanumerics.getFontDict(script=script)
        if (font not in fontDict):
            raise ValueError("Uknown %s font '%s'." % (script, font))
        charInfo = fontDict[font]
        if (group == "U"): return charInfo[0]
        if (group == "L"): return charInfo[1]
        if (group == "D"): return charInfo[2]
        raise ValueError(
            "Uknown %s 'group', must be 'U', 'L', or 'D'." % (script))

    @staticmethod
    def getFontDict(script: str = "Latin"):
        """Return a dict of the "fonts" for the specified script.
        """
        if (script == "Latin"):
            return mathAlphanumerics.LatinFontDict
        elif (script == "Greek"):
            return mathAlphanumerics.GreekFontDict
        elif (script == "Digit"):
            return mathAlphanumerics.DigitFontDict
        else: raise ValueError(
            "Unknown script '%s', must be Latin|Greek|Digit." %
                (script))

    @staticmethod
    def convert(ss: str, script: str = "Latin", font: str = "BOLD", decompose: bool = False):
        """Convert a string to the requested variant.
        """
        if (decompose):
            ss = unicodedata.normalize("NFD", ss)
            warn(1, "Decomposed: %s" % (ss))
        xtab = mathAlphanumerics.getTranslateTable(script, font)
        return ss.translate(xtab)

    @staticmethod
    def getTranslateTable(script: str = "Latin", font: str = "BOLD"):
        #if (PY3):
        #    raise NotImplementedError("No maketrans in Python 3.")
        if (script == "Latin"):
            tbl = mathAlphanumerics.LatinFontDict
            uSrcStart = ord("A"); uSrcEnd = ord("Z")
            lSrcStart = ord("a"); lSrcEnd = ord("z")
            dSrcStart = ord("0"); dSrcEnd = ord("9")
        elif (script == "Greek"):
            tbl = mathAlphanumerics.GreekFontDict
            uSrcStart = 0x00391; uSrcEnd = 0x003a9
            lSrcStart = 0x003b1; lSrcEnd = 0x003c9
            dSrcStart = dSrcEnd = None
        elif (script == "Digit"):
            tbl = mathAlphanumerics.DigitFontDict
            uSrcStart = uSrcEnd = None
            lSrcStart = lSrcEnd = None
            dSrcStart = ord("0"); dSrcEnd = ord("9")
        else: raise ValueError(
            "Unknown script '%s', must be Latin|Greek|Digit." %
                (script))

        font = font.upper()
        src = tgt = ""
        if (font in mathAlphanumerics.specialDict):
            for s, t in mathAlphanumerics.specialDict[font].items():
                src += s; tgt += chr(t)
        elif (font in mathAlphanumerics.combinerDict):
            combiningChar = mathAlphanumerics.combinerDict[font]
            tgt = []
            for s in string.ascii_lowercase:
                src += s
                tgt.append(s+combiningChar)
        elif (font not in tbl):
            raise ValueError("Unknown font '%s' for script '%s'." %
                (font, script))
        else:
            uTgtStart, lTgtStart, dTgtStart, _ = tbl[font]
            if (uTgtStart):
                srcPart,  tgtPart = mathAlphanumerics.makePartialXtab(
                    uSrcStart, uSrcEnd, uTgtStart)
                src += srcPart; tgt += tgtPart
            warn(1, "uppercase table for %s:\n    %s\n    %s" %
                (font, src, tgt))

            if (lTgtStart):
                srcPart,  tgtPart = mathAlphanumerics.makePartialXtab(
                    lSrcStart, lSrcEnd, lTgtStart)
                src += srcPart; tgt += tgtPart
            warn(1, "both-case table for %s:\n    %s\n    %s" %
                (font, src, tgt))

            if (dTgtStart):
                srcPart,  tgtPart = mathAlphanumerics.makePartialXtab(
                    dSrcStart, dSrcEnd, dTgtStart)
                src += srcPart; tgt += tgtPart

        warn(1, "full table for %s:\n    %s\n    %s" % (font, src, tgt))
        xtab = str.maketrans(src, tgt)
        return xtab

    @staticmethod
    def makePartialXtab(srcStart: int, srcEnd: int, tgtStart: int) -> List:
        """This takes the actual first and last character codes. I noticed
        too late that this is unlike the usual Python "end+1". I may
        fix it sometime.
        @return 'from' and 'to' strings. Caller can make an xtab from them,
        or pass them to something like "tr", or whatever.
        """
        srcTab = tgtTab = ""
        tgtCode = tgtStart
        pythonEnd = srcEnd + 1
        for i in range(pythonEnd-srcStart):
            srcCode = srcStart + i
            tgtCode = tgtStart + i
            if (tgtCode not in mathAlphanumerics.exceptions):
                finalCode = tgtCode
            elif (mathAlphanumerics.exceptions[tgtCode] is not None):
                finalCode = mathAlphanumerics.exceptions[tgtCode]
            else:
                continue  # No translation available!
            try:
                srcChar = chr(srcCode)
                tgtChar = chr(finalCode)
                srcTab += srcChar
                tgtTab += tgtChar
            except (ValueError, UnicodeDecodeError) as e:
                warn(0, "Bad code point 0x%05x or 0x%05x:\n    %s" %
                    (srcCode, finalCode, e))
                continue
        assert len(srcTab) == len(tgtTab)
        return srcTab, tgtTab

    # See https://en.wikipedia.org/wiki/Pangram
    #
    EnglishSentences = [
        "Sphinx of black quartz, judge my vow",
        "Jackdaws love my big sphinx of quartz",
        "Pack my box with five dozen liquor jugs",
        "The quick onyx goblin jumps over the lazy dwarf",
        "Cwm fjord bank glyphs vext quiz",  # Perfect
        # = "Symbols in a mountain hollow on the bank of an inlet
        # vexed an eccentric person."
        "How razorback-jumping frogs can level six piqued gymnasts!",
        "Cozy lummox gives smart squid who asks for job pen",
        "Amazingly few discotheques provide jukeboxes",
        "'Now fax quiz Jack!', my brave ghost pled",
        "Watch Jeopardy!, Alex Trebek's fun TV quiz game.",
        "Jived fox nymph grabs quick waltz.",
        "Glib jocks quiz nymph to vex dwarf.",
        "How vexingly quick daft zebras jump!",
        "The five boxing wizards jump quickly.",
        "Mr Jock, TV quiz PhD, bags few lynx",
    ]

    LatinSentences = [
        "gaza frequens Libycum duxit Karthago triumphum",

        "heu Zama, quam Scipio celeber dux frangit inique",

        "venerat, insano Cassandrae incensus amore" +
        "et gener auxilium Priamo Phrygibusque ferebat",

        "obstipui, steteruntque comae et vox faucibus haesit." +
        "Hunc Polydorum auri quondam cum pondere magno",

        "Nox erat, et terris animalia somnus habebat:" +
        "effigies sacrae divom Phrygiique Penates",

        "infelix Theseus; Phlegyasque miserrimus omnis" +
        "admonet, et magna testatur voce per umbras:",

        "Forte die sollemnem illo rex Arcas honorem" +
        "Amphitryoniadae magno divisque ferebat",

        "a quo post Itali fluvium cognomine Thybrim" +
        "diximus, amisit verum vetus Albula nomen;",

        "Haud procul hinc saxo incolitur fundata vetusto" +
        "urbis Agyllinae sedes, ubi Lydia quondam",

        "quid gravidam bellis urbem et corda aspera temptas?" +
        "Nosne tibi fluxas Phrygiae res vertere fundo",

        "Nosne tibi fluxas Phrygiae res vertere fundo" +
        "conamur, nos, an miseros qui Troas Achivis",

        "Tarquitus exultans contra fulgentibus armis" +
        "silvicolae Fauno Dryope quem nympha crearat",

        "ut bivias armato obsidam milite fauces." +
        "Tu Tyrrhenum equitem conlatis excipe signis;",

        "Fovit ea volnus lympha longaevus Iapyx" +
        "ignorans, subitoque omnis de corpore fugit",

        "quantus Athos aut quantus Eryx aut ipse coruscis" +
        "cum fremit ilicibus quantus gaudetque nivali",
    ]

    # From https://backpacker.gr/pangrams
    # (apparently Modern)
    #
    GreekSentences = [
        "κόλφω, βάδιζε μπροστά ξανθή ψυχή!",
        "Ξεσκεπάζω την ψυχοφθόρα βδελυγμία.",
        "Φθηνό μπλε βράδυ, στο Γκάζι ξεψυχώ.",
        "Βυθίζετε ψηφιακό εξοπλισμό εγχόρδων.",
        "Βύθιζες ψηφιακά χόρτα ξαπλωμένε δόγη!",
        "Ξοπίσω, ραβδίζω φλεγματικά τα ψυχανθή.",
        "Θα ξεφύγω με βία στην ψυχεδελική πρόζα.",
        "Βράζω γόπες με το φθηνό λάδι και ξεψυχώ.",
        "Βυθίζω χοντρή γίδα με ψηφιακό εξοπλισμό.",
        "Τρηχύν δ' υπερβάς φραγμόν εξύνθιζε κλώψ.",
    ]

    # Other languages
    # (see http://clagnut.com/blog/2380)
    #


###############################################################################
# Main
#
if __name__ == "__main__":
    def anyInt(x):
        return int(x, 0)

    def processOptions():
        import argparse
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--decompose", action="store_true",
            help="""If set, separate diacritics from their base characters. With this,
Latin or Greek characters with diacritics should work, even though Unicode does not
provide Mathematical and similar variants for most of them.""")
        parser.add_argument(
            "--family", type=str, default="",
            help="With --makeHtmlComparison, choose the font family for display.")
        parser.add_argument(
            "--font", type=str, default="ITALIC",
            help="Character variant to convert to. Default: ITALIC.")
        parser.add_argument(
            "--indeosperamus", action="store_true",
            help="Use actual Latin for sample sentences.")
        parser.add_argument(
            "--makeHtmlComparison", action="store_true",
            help="Write out an HTML document that compares Math quasi-fonts to formatted regulars.")
        parser.add_argument(
            "--missing", type=anyInt, default=0x2623,
            help=("Show this code point for undefined characters. " +
            "Default: biohazard (U+2623)."))
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--sample", type=str, default=None,
            help="Sample text to convert (see also --to).")
        parser.add_argument(
            "--script", type=str, default="Latin",
            choices=[ "Latin", "Greek", "Digits" ],
            help='Script to translate to a variant "font". Default: Latin.')
        parser.add_argument(
            "--show", action="store_true",
            help="List all fonts for the chosen script. Add -v for samples.")
        parser.add_argument(
            "--test", "--list", action="store_true",
            help="Test getTranslateTable().")
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Add more messages (repeatable).")
        parser.add_argument(
            "--version", action="version", version=__version__,
            help="Display version information, then exit.")

        args0 = parser.parse_args()
        return(args0)

    messageIssued = False

    def showAlternates(exceptionDict: Dict, MISSING: int = None):
        """Print a list of all the available variants. With -v, add samples.
        """
        for k in (sorted(exceptionDict.keys())):
            if (exceptionDict[k] is None):
                print("%-50s    DOES NOT EXIST" % (k))
                continue
            try:
                Ustart, Lstart, Dstart, _ = exceptionDict[k]
            except TypeError as e:
                print("******* Error on '%s':\n    %s" % (k, e))
                continue
            print("  %s:" % (k))
            if (args.verbose):
                if (Ustart is not None):
                    print("    U+%05x: %s" %
                        (Ustart, gatherChars(Ustart, 26, MISSING=MISSING)))
                if (Lstart is not None):
                    print("    U+%05x: %s" %
                        (Lstart, gatherChars(Lstart, 26, MISSING=MISSING)))
                if (Dstart is not None):
                    print("    U+%05x: %s" %
                        (Dstart, gatherChars(Dstart, 10, MISSING=MISSING)))
        print("******* Experimental *******\n%s" %
            ", ".join([ *mathAlphanumerics.specialDict, *mathAlphanumerics.combinerDict ]))

    def gatherChars(startCode: int, n: int, MISSING: int = 0x0005f):
        """Collecting n characters starting at a given code point.
        If any in the range are listed in 'exceptions', substitute them.
        """
        global messageIssued
        buf = ""
        try:
            for codePoint in range(startCode, startCode+n):
                if (codePoint in mathAlphanumerics.exceptions):
                    codePoint = mathAlphanumerics.exceptions[codePoint]
                    if (codePoint is None):
                        codePoint = MISSING
                buf += "%s " % (chr(codePoint))
        except ValueError:
            if (not messageIssued): print(
                "    ******* Out of chr() range *******")
            messageIssued = True
        return buf

    def testXtabs(script: str, exceptionDict: Dict, sample: str = None):
        """Given one of the lists, like mathAlphanumerics.LatinFontDict, set up
        translate tables and print the result on a sample sentence.
        """
        print("Testing xtabs for script '%s'." % (script))
        if (not sample): sample = getRandomSentence()

        for k in (sorted(exceptionDict.keys())):
            if (exceptionDict[k] is None):
                print("%-50s    DOES NOT EXIST" % (k))
                continue
            xtab = mathAlphanumerics.getTranslateTable(args.script, k)
            firstOrd = ord("A".translate(xtab))
            if (firstOrd != ord("A")):
                print("=== %s ('A' -> U+%04x)" % (k, firstOrd))
            else:
                print("=== %s ('A' not available)" % (k))
            print("    Upper:" + sample.upper().translate(xtab))
            print("    Lower:" + sample.lower().translate(xtab))
            digits = "0123456789".translate(xtab)
            if (digits == "0123456789"): digits = "[not available]"
            print("    Digit:" + digits)

    def getRandomSentence():
        import random
        if (args.indeosperamus):
            return random.choice(mathAlphanumerics.LatinSentences)
        else:
            return random.choice(mathAlphanumerics.EnglishSentences)

    def makeHC(fontFamily: str = ""):
        """Create an HTML file to show the special forms next to their
        formatted equivalents of the regular characters. For example,
        a row of MATHEMATICAL BOLD vs. regular in <B>.
        """
        mapping = {
            "BOLD":                        [ "b", ],  # UPPER LOWER DIGITS
            "ITALIC":                      [ "i", ],  # UPPER LOWER
            "BOLD ITALIC":                 [ "b", "i", ],  # UPPER LOWER
            "SANS-SERIF":                  [ "sans", ],  # UPPER LOWER DIGITS
            "SANS-SERIF BOLD":             [ "sans", "b", ],  # UPPER LOWER DIGITS
            "SANS-SERIF ITALIC":           [ "sans", "i", ],  # UPPER LOWER
            "SANS-SERIF BOLD ITALIC":      [ "sans", "b", "i", ],  # UPPER LOWER
            "SCRIPT":                      [ "cursive", ],  # UPPER LOWER  font-family: cursive;
            "BOLD SCRIPT":                 [ "cursive", "b", ],  # UPPER LOWER
            #"FRAKTUR":                     [ "b", ],  # UPPER LOWER
            #"BOLD FRAKTUR":                [ "b", ],  # UPPER LOWER
            #"DOUBLE-STRUCK":               [ "b", ],  # UPPER LOWER DIGITS
            "MONOSPACE":                   [ "mono", ],  # UPPER LOWER DIGITS  font-family: monospace;
            #"CIRCLED":                     [ "b", ],  # UPPER LOWER DIGITS
            #"PARENTHESIZED":               [ "b", ],  # UPPER LOWER DIGITS
            #"FULLWIDTH":                   [ "b", ],  # UPPER LOWER DIGITS
            #"SQUARED":                     [ "b", ],  # UPPER
            #"NEGATIVE SQUARED":            [ "b", ],  # UPPER
            #"NEGATIVE CIRCLED":            [ "b", ],  # UPPER
            "SUPERSCRIPT":                 [ "sup", ],  # DIGITS
            "SUBSCRIPT":                   [ "sub", ],  # DIGITS
        }

        upp = re.sub(r"(.)", "\\1 ", string.ascii_uppercase)
        low = re.sub(r"(.)", "\\1 ", string.ascii_lowercase)
        #dig = re.sub(r"(.)", "\\1 ", string.digits)

        fontChoice = ""
        if (fontFamily): fontChoice = "font-family:%s" % (fontFamily)
        print("""<html>
    <head>
        <title>Mathematical Unicode vs. HTML formatting</title>
        <style type="text/css">
            body            { margin-left:24pt; %s }
            table, tr, td   { border:thin black solid; border-collapse:collapse; }
            sans            { font-family:sans-serif; }
            serif           { font-family:serif; }
            cursive         { font-family:cursive; }
            monospace       { font-family:monospace; }
        </style>
    </head>
    <body>
        <h1>Comparing ASCII+HTML vs. Unicode MATHEMATICAL quasi-fonts</h1>
        <h3>(font: %s)</h3>""" %
            (fontChoice, fontFamily if fontFamily else "[default]"))
        for font, tags in mapping.items():
            print("<h2>%s</h2>" % (font))
            print("""<table>
            <tr><td>A</td><td>%s</td></tr>
            <tr><td>M</td><td>%s</td></tr>
            </table>""" % (makeAsciiSample(font, tags, upp), makeMathSample(font, tags, upp)))

            print("""<table>
            <tr><td>A</td><td>%s</td></tr>
            <tr><td>M</td><td>%s</td></tr>
            </table>""" % (makeAsciiSample(font, tags, low), makeMathSample(font, tags, low)))
        print("""</body>\n<html>""")
        return

    def makeAsciiSample(_fontName: str, tags: List, sample: str) -> str:
        bufAscii = ""
        for tag in tags: bufAscii += "<%s>" % (tag)
        bufAscii += sample
        for tag in reversed(tags): bufAscii += "</%s>" % (tag)
        return bufAscii

    def makeMathSample(fontName: str, _tags: List, sample: str) -> str:
        bufMath = mathAlphanumerics.convert(
            sample, script="Latin", font=fontName, decompose=False)
        # TODO: Add option to escape to ASCII
        return bufMath


    ###########################################################################
    #
    args = processOptions()

    try:
        _ = chr(0x1d49c)
    except ValueError as e0:
        warn(-1, "Character over U+FFFF failed. Upgrade Python?\n  %s\n" % (e0))

    if (args.makeHtmlComparison):
        makeHC(args.family)
        sys.exit()

    if (args.script == "Greek"):
        scr = "Greek"
        fonts = mathAlphanumerics.GreekFontDict
    elif (args.script == "Digits"):
        scr = "Digits"
        fonts = mathAlphanumerics.DigitFontDict
    elif (args.script == "Latin"):
        scr = "Latin"
        fonts = mathAlphanumerics.LatinFontDict
    else:
        warn(-1, "Unknown 'script': '%s'." % (args.script))

    if (args.show):
        messageIssued = False
        print("\nAvailable alts for %s (-v to include samples):" % (scr))
        showAlternates(fonts, args.missing)
        if (not args.verbose): print("(to see samples, use -v)")

    elif (args.test):
        testXtabs(args.script, fonts, sample=args.sample)

    elif (args.sample):
        args.font = args.font.title()
        print("\nSample conversion for script '%s', font '%s':" %
            (scr, args.font))
        if (args.sample is None):
            args.sample = getRandomSentence()
        txt = args.sample
        if (txt == "" or txt == "*"): txt = getRandomSentence()
        s0 = mathAlphanumerics.convert(txt,
            script=args.script, font=args.font, decompose=args.decompose)
        print("    Original:  " + txt +
            "\n    Converted: " + s0)

    else:  # translate stdin
        if (sys.stdin.isatty()):
            print("Waiting on stdin...")
        xt = mathAlphanumerics.getTranslateTable(scr, args.font)
        import io
        istream = io.TextIOWrapper(sys.stdin.buffer, encoding="utf-8")
        #sys.stdin.reconfigure(encoding="utf-8")
        for rec in istream:
            rec2 = mathAlphanumerics.convert(rec,
                script=args.script, font=args.font, decompose=args.decompose)
            print(rec2)

    sys.exit()
