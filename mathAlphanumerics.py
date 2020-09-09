#!/usr/bin/env python
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

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    def unichr(n): return chr(n)

__metadata__ = {
    'title'        : "mathAlphanumerics.py",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 2.7.6",
    'created'      : "<2006-10-04",
    'modified'     : "2020-08-27",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr = """
=Description=

Provide support for using the many Unicode variations on alphabets and digits,
either as a command-line filter or via an API.

You can just pipe Unicode text through this like, with options for
the desired script to translate (`--script`,
and the Unicode range (`--font` because that's how it's being used).

    cat eggs.txt | mathAlphanumerics --script Latin --font 'BOLD ITALIC'

Or you can call the package from Python in two ways::

    import mathAlphanumerics.py
    s2 = mathAlphanumerics.convert(text,
            script="Latin", font="Mathematical Bold")


    xtab = mathAlphanumerics.getTranslateTable(
        'Latin', 'Mathematical Sans-serif Bold Italic')
    s = s.translate(xtab)

To see a list of the various names available for the selected
`--script`, (for example, "SANS-SERIF BOLD ITALIC"), with a sample of each and
the code point where each starts:

    mathAlphanumerics.py --show -v

'''Note:''' This will only work is your display medium supports Unicode,
and the exact results depend on the font(s) in use. Even then, a few
characters seem to be unavailable in Unicode, such as
"PARENTHESIZED DIGIT ZERO".
When a mapping is not available, the character is left unchanged.

The `--script` choices are "Latin" (the default), "Greek", or "Digits".

The `--font` options (the default is 'ITALIC') are:

For Latin:
    'BOLD'                         UPPER LOWER DIGITS
    'ITALIC'                       UPPER LOWER
    'BOLD ITALIC'                  UPPER LOWER
    'SANS-SERIF'                   UPPER LOWER DIGITS
    'SANS-SERIF BOLD'              UPPER LOWER DIGITS
    'SANS-SERIF ITALIC'            UPPER LOWER
    'SANS-SERIF BOLD ITALIC'       UPPER LOWER
    'SCRIPT'                       UPPER LOWER
    'BOLD SCRIPT'                  UPPER LOWER
    'FRAKTUR'                      UPPER LOWER
    'BOLD FRAKTUR'                 UPPER LOWER
    'DOUBLE-STRUCK'                UPPER LOWER DIGITS
    'MONOSPACE'                    UPPER LOWER DIGITS
    'CIRCLED'                      UPPER LOWER DIGITS
    'PARENTHESIZED'                UPPER LOWER DIGITS
    "FULLWIDTH"                    UPPER LOWER DIGITS

    'SQUARED'                      UPPER
    'NEGATIVE SQUARED'             UPPER
    'REGIONAL INDICATOR SYMBOL'    UPPER
    'NEGATIVE CIRCLED'             UPPER
    'SUPERSCRIPT'                  DIGITS (alphabet unfinished)
    'SUBSCRIPT'                    DIGITS (alphabet unfinished)

For Greek:
    'BOLD'                         UPPER LOWER
    'ITALIC'                       UPPER LOWER
    'BOLD ITALIC'                  UPPER LOWER
    'SANS-SERIF BOLD'              UPPER LOWER
    'SANS-SERIF BOLD ITALIC'       UPPER LOWER


For Digits, many additional sets are available.
In addition to those already listed (I cannot personally evaluate the results
for most of these; error reports are welcome):

    'DIGIT COMMA'
    'DIGIT FULL STOP'
    'ARABIC-INDIC'
    'EXTENDED ARABIC-INDIC'
    'NKO'
    'DEVANAGARI'
    'BENGALI'
    'GURMUKHI'
    'GUJARATI'
    'ORIYA'
    'TAMIL'
    'TELUGU'
    'KANNADA'
    'MALAYALAM'
    'SINHALA LITH'
    'THAI'
    'LAO'
    'TIBETAN'
    'MYANMAR'
    'MYANMAR SHAN'
    'KHMER'
    'MONGOLIAN'
    'LIMBU'
    'NEW TAI LUE'
    'TAI THAM HORA'
    'TAI THAM THAM'
    'BALINESE'
    'SUNDANESE'
    'LEPCHA'
    'OL CHIKI'
    'IDEOGRAPHIC NUMBER'
    'VAI'
    'SAURASHTRA'
    'COMBINING DEVANAGARI'
    'KAYAH LI'
    'JAVANESE'
    'CHAM'
    'MEETEI MAYEK'

Some additional digit sets are available except for ZERO.

    'CIRCLED'
    'DINGBAT NEGATIVE CIRCLED'
    'DOUBLE CIRCLED'
    'PARENTHESIZED'
    'FULL STOP'
    'DINGBAT CIRCLED SANS-SERIF'
    'DINGBAT NEGATIVE CIRCLED SANS-SERIF'

I expect to add other special "effects", but some might not be supported in the "translate table" method:
    TURNED (aka ROTATED)
    STRIKETHROUGH
    UNDERLINE
    OVERLINE

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

==getFontDict(script='Latin')==

Return `LatinFontDict`, `GreekFontDict`, or `DigitFontDict`, as appropriate.
See their descriptions below.

==getStartCodePoint(script='Latin', font='BOLD', group='U')==

Return the code point of the first character for the given `script` in the given `font` variation (such as "SANS-SERIF BOLD", etc.). By default, gets
the position of A for Latin, alpha for Greek, or Digit for 0). Pass `group` as 'U', 'L', or 'D' respectively, to get the position of the first uppercase,
lowercase, or digit for "fonts" as needed.
Typically, the uppercase range is first, immediately followed by the lowercase
range, and the digits are elsewhere.

The "starting" code point is reported as where the "font" ''would'' begin if
it were all there. Thus, the "PARENTHESIZED" Latin digits are listed as
beginning at U+02473 even though U+2473 is actually "CIRCLED NUMBER TWENTY".
But the script knows there is no "PARENTHESIZED DIGIT ZERO", and will
leave '0' untranslated in this case.

==convert(s, script="Latin", font='Bold')==

Just convert characters in the string `s` that are from the given "script" to the specified "font".

For 'Latin', uppercase, lowercase, and digits are converted (when available).

For 'Greek', uppercase and lowercase are converted (when available).

For 'Digits', only digits 0-9 are converted (and only when available).

==getTranslateTable(script="Latin", font='BOLD')==

Return a Python 3 translation table generated for the specified `script`
and `font`. Exceptions are integrated, and omissions are omitted.

==makePartialXtab(srcStart, srcEnd, tgtStart)==


=Related Commands=

My `ord --math` will display a list of these characters.


=Known bugs and Limitations=

==Inherent issues==

If the display environment doesn't handle Unicode, or the font in use has
problems with any of the characters needed, the result may not be ideal.

Unicode intents most of these characters for special mathematical uses, such
as ensuring that you get the fancy "R" conventionally use to refer to the set
of all real numbers (which takes too long write out in full). Using these
characters for formatting is a little weird. But Gæð a wyrd swa hio scel.

Monospace fonts for Unicode, may not really make all the characters the same
width; so horizontal alignment may creep off. "FULLWIDTH" may pose similar
problems.

"MONOSPACE" is not very distinctive on terminals that always use monospace
anyway.

"SANS-SERIF" is not very distinctive if your default font is that way, too.

"SCRIPT" may look a lot like italic, especially to the unpracticed eye.

Sets such as MATHEMATICAL ITALIC are generally defined in Unicode as a contiguous range; but occasionally one or a few members are somewhere else
entirely (such as MATHEMATICAL ITALIC SMALL H), and the "expected" slot among
the rest of the letter is left undefined. In practice, this often means that
Unicode fonts do not define quite the same "look" to the exceptional characters.

The implementation here knows where
the ranges start, and then has a list of "exceptions" (in a class variable
of that name). There is an edge case when the ''first'' character of the
range does not exist, or exists but is exceptional. In such cases, the code
treats the range as beginning at where the first character *would* be if it
were not missing or an exception. This ''may'' lead to problems if your data
contains that character.

For example, PARENTHESIZED DIGIT ONE is U+2474, so we would expect the ZERO
at U+2473. But U+2473 is CIRCLED NUMBER TWENTY. This package should takes the
exceptions into account when building a translation table, so everything should
be ok when the translation table is used -- at that point the "fake" value is
not involved.

Characters with diacritics must be decomposed first. To do this in Python:

    import unicodedata
    s = unicodedata.normalize('NFD', s)


==Script-specific issues

Many scripts that use accented Latin or Greek characters, do not have accents
on all characters. So if you don't decompose first (discussed above), you'll
get only '''some''' of the characters translated.

Cannot translate multiple scripts simultaneously.

Punctuation is not yet supported, such as superscript and subscript
parentheses, plus, minus, etc. For many of the (pseudo-) fonts it might not
make sense anyway; but for some it does.

Superscript, subscript, turned, and strikethrough are not finished.

Non-Latin digit series are not well integrated or tested.

Numbers beyond single digit values (such as for roman numerals,
circled numbered, etc.) are not supported.

"Modifier letters" are not supported.

This package does not provide a way to translate the various alternate
set back to plain Latin or Greek or Digits. However, this can be done
pretty well with Unicode "compatibility decomposition":

    import unicodedata
    s = unicodedata.normalize('NFKD', s)

[https://www.unicode.org/reports/tr25/tr25-6.html#_Toc2] notes that the
Mathematical Greek sets include several less-used characters,
such as uppercase nabla (U+2207) and a variant of theta (U+03F4);
and lowercase partial differential sign (U+2202) and glyph variants of
epsilon (U+03F5), theta (U+03D1), kappa (U+03F0),
phi (U+03D5), rho (U+03F1), and pi (U+03D6).
They are not supported here (yet).


=Notes=

Using Unicode Mathematical character to achieve formatting may be slightly odd,
but alternatives are limited given current terminal and shell technology,
which typically support Unicode but not font-changes or
effects (other than ANSI terminal color and effect escapes, which are quite
limited).

Not all of the variant alphabets are contiguous blocks of characters, or
even complete.
This script maps the discontiguous cases anyway, using an "exceptions" table
(if it fails, that's a bug). If the target character does not exist,
the source character is left unchanged.

There are some additional scripts and forms that are not supported:

    Some squared CJK
    Parenthesized ideographs, Hangul, and Korean characters.
    Circled italic latin C, R
    Double-Struck Italic D, e, i, j
    Squared Latin Small Letter D
    Old Italic letters at U+10300 and following
    circled katakana U+032d0
    some circled hangul and ideographs U+3260
    circled number X on black square U+3248
    superscript and subscript sets (very incomplete)

    aeox schwa hklmnpst; i=1d62, r=1d63, u=1d64, v=1d65, j=2c7c
    [ 'subscript latin upper (...209c)', 0x02090 ],
https://en.wikipedia.org/wiki/Unicode_subscripts_and_superscripts#Uses,
superscripts: i=2071 n=207f,
subscripts: iruv, grk bgrfx 0x1d62...0x1d6a aeoxhklmnpst
      combining diacriticals marks has aeioucdhmrtvx
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
* ''2018-08-29: Port to Python.''
* 2018-08-29ff: Split from Perl colorstring, and Ported.
* 2018-09-04: Merged from incomplete `UnicodeAltLatin.py`
* 2020-07-25: Lose remaining upper/lower separations. Big cleanup.
Support complete upper/lower/digit translation tables. Add `--test`.
Add support for in-pipe translation.
* 2020-09-03: Improve translation-table construction.


=To do=

* Cleaner way to request, like splitting out bold and italic -- though
you only get the full set of { roman, bold, italic, bold-italic } for
plain and sans-serif.

* Better testing for non-Latin digits.

* Possibly add combining characters such as underscore, strike-through, and
overline. There's even COMBINING ENCLOSING CIRCLE (and SQUARE).

* Possibly add turned (cf reversed), using:
    Problem: there isn't a reserved range for these
    --- uppercase ---
        U+02c6f LATIN CAPITAL LETTER TURNED A
        B C D                                        ???
        E => exists
        U+02132 TURNED CAPITAL F
        U+02141 TURNED SANS-SERIF CAPITAL G
        U+0a78d LATIN CAPITAL LETTER TURNED H (why is this not itself?)
        I => I
        J ?                                        ???
        K ?                                        ???
        U+0a780 LATIN CAPITAL LETTER TURNED L
            U+02142 TURNED SANS-SERIF CAPITAL L
        U+0019c LATIN CAPITAL LETTER TURNED M
        N => N
        O => O
        P =>                                        ??? eth?
        Q =>                                        ???
        R =>                                        ???
        S => S
        T =>                                        ???
        U => U+2229 intersection?
        U+00245 LATIN CAPITAL LETTER TURNED V
        W =>                                        ???
        X => X
        U+02144 TURNED SANS-SERIF CAPITAL Y

        --- lowercase ---
        U+00250 LATIN SMALL LETTER TURNED A
        b => q
        U+02184 LATIN SMALL LETTER REVERSED C
        d => p
        U+001dd LATIN SMALL LETTER TURNED E (or e => schwa)
        U+0214e TURNED SMALL F
        U+01d77 LATIN SMALL LETTER TURNED G
        U+00265 LATIN SMALL LETTER TURNED H
        U+01d09 LATIN SMALL LETTER TURNED I
        j => medial s?
        U+0029e LATIN SMALL LETTER TURNED K
        U+0a781 LATIN SMALL LETTER TURNED L
        U+0026f LATIN SMALL LETTER TURNED M
        n => u
        o = o
        p => d
        q => b
        U+00279 LATIN SMALL LETTER TURNED R
        s = s
        U+00287 LATIN SMALL LETTER TURNED T
        u => n
        U+0028c LATIN SMALL LETTER TURNED V
        U+0028d LATIN SMALL LETTER TURNED W
        x = x
        U+0028e LATIN SMALL LETTER TURNED Y
        z = z

* Possibly add reversed (horizontally)
    --- uppercase ---
    C => U+02183 ROMAN NUMERAL REVERSED ONE HUNDRED
    U+0018e LATIN CAPITAL LETTER REVERSED E
    I => I
    U+02143 REVERSED SANS-SERIF CAPITAL L
    M => M
    O => O
    T => T
    U => U
    V => V
    W => W
    X => X
    Y => Y

    --- lowercase ---
    b => d
    U+02184 LATIN SMALL LETTER REVERSED C
    d => b
    U+00258 LATIN SMALL LETTER REVERSED E
    i => i
    l => l
    m => m?
    n => n?
    o => o
    p => q
    q => p
    u => u?
    v => v
    w => w
    x => x

* Possibly add small cap (not in a neat 26-char block)
    U+01d00 LATIN LETTER SMALL CAPITAL A
    U+00299 LATIN LETTER SMALL CAPITAL B  (far)
    U+01d04 LATIN LETTER SMALL CAPITAL C
    U+01d05 LATIN LETTER SMALL CAPITAL D
    U+01d07 LATIN LETTER SMALL CAPITAL E
    U+0a730 LATIN LETTER SMALL CAPITAL F  (far)
    U+00262 LATIN LETTER SMALL CAPITAL G  (far)
    U+0029c LATIN LETTER SMALL CAPITAL H  (far)
    U+0026a LATIN LETTER SMALL CAPITAL I  (far)
    U+01d0a LATIN LETTER SMALL CAPITAL J
    U+01d0b LATIN LETTER SMALL CAPITAL K
    U+0029f LATIN LETTER SMALL CAPITAL L  (far)
    U+01d0d LATIN LETTER SMALL CAPITAL M
    U+00274 LATIN LETTER SMALL CAPITAL N  (far)
    U+01d0f LATIN LETTER SMALL CAPITAL O
    U+01d18 LATIN LETTER SMALL CAPITAL P
    q???
    U+00280 LATIN LETTER SMALL CAPITAL R  (far)
    U+0a731 LATIN LETTER SMALL CAPITAL S  (far)
    U+01d1b LATIN LETTER SMALL CAPITAL T
    U+01d1c LATIN LETTER SMALL CAPITAL U
    U+01d20 LATIN LETTER SMALL CAPITAL V
    U+01d21 LATIN LETTER SMALL CAPITAL W
    x???
    U+0028f LATIN LETTER SMALL CAPITAL Y  (far)
    U+01d22 LATIN LETTER SMALL CAPITAL Z

* Possibly add superscript
    U+02071 SUPERSCRIPT LATIN SMALL LETTER I
    U+0207f SUPERSCRIPT LATIN SMALL LETTER N

* Add subscript (this is not a block with empties like most others)
    U+02090 LATIN SUBSCRIPT SMALL LETTER A
    U+02091 LATIN SUBSCRIPT SMALL LETTER E
    U+02095 LATIN SUBSCRIPT SMALL LETTER H
    U+01d62 LATIN SUBSCRIPT SMALL LETTER I  (far)
    U+02c7c LATIN SUBSCRIPT SMALL LETTER J  (far)
    U+02096 LATIN SUBSCRIPT SMALL LETTER K
    U+02097 LATIN SUBSCRIPT SMALL LETTER L
    U+02098 LATIN SUBSCRIPT SMALL LETTER M
    U+02099 LATIN SUBSCRIPT SMALL LETTER N
    U+02092 LATIN SUBSCRIPT SMALL LETTER O
    U+0209a LATIN SUBSCRIPT SMALL LETTER P
    U+01d63 LATIN SUBSCRIPT SMALL LETTER R  (far)
    U+0209b LATIN SUBSCRIPT SMALL LETTER S
    U+0209c LATIN SUBSCRIPT SMALL LETTER T
    U+01d64 LATIN SUBSCRIPT SMALL LETTER U  (far)
    U+01d65 LATIN SUBSCRIPT SMALL LETTER V  (far)
    U+02093 LATIN SUBSCRIPT SMALL LETTER X  (far)

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
        'Fullwidth', 'Script', 'Fraktur', 'Double-Struck', 'Sans-serif',
        'Monospace', 'Parenthesized', 'Circled', 'Squared',
        'Negative-circled', 'Negative-squared', 'Regional symbol'
    ]

    # These are the 'fonts' available as Unicode 'Mathematical' variations on
    # Latin. A similar list is available for Greek, and for digits.
    # NOTE: "MATHEMATICAL is omitted for compactness.
    #
    LatinFontDict = {
        ####### Following are "Mathematical":
        # Name                      ( Upper    Lower,   Digits   Exceptions )
        'BOLD':                     ( 0x1d400, 0x1d41a, 0x1d7ce, '' ),
        'ITALIC':                   ( 0x1d434, 0x1d44e, None,    'h' ),
        'BOLD ITALIC':              ( 0x1d468, 0x1d482, None,    '' ),

        'SANS-SERIF':               ( 0x1d5a0, 0x1d5ba, 0x1d7e2, '' ),
        'SANS-SERIF BOLD':          ( 0x1d5d4, 0x1d5ee, 0x1d7ec, '' ),
        'SANS-SERIF ITALIC':        ( 0x1d608, 0x1d622, None,    '' ),
        'SANS-SERIF BOLD ITALIC':   ( 0x1d63c, 0x1d656, None,    '' ),

        'SCRIPT':                   ( 0x1d49c, 0x1d4b6, None, 'BEFHILMR ego'),
        'BOLD SCRIPT':              ( 0x1d4d0, 0x1d4ea, None,    '' ),

        'FRAKTUR':                  ( 0x1d504, 0x1d51e, None,    'CHIRZ' ),
        'BOLD FRAKTUR':             ( 0x1d56c, 0x1d586, None,    '' ),

        'DOUBLE-STRUCK':            ( 0x1d538, 0x1d552, 0x1d7d8, 'CHNPQRZ' ),
        'MONOSPACE':                ( 0x1d670, 0x1d68a, 0x1d7f6, '' ),

        ####### Following aren't "Mathematical":

        'CIRCLED':                  ( 0x024b6, 0x024d0, 0x0245f, '' ),
        'PARENTHESIZED':            ( 0x1f110, 0x0249c, 0x02473, '' ),
        "FULLWIDTH":                ( 0x0FF21, 0x0FF41, 0x0FF10, '' ),

        ####### Not available in lower case:

        'SQUARED':                    ( 0x1f130, None,    None,    '' ),
        'NEGATIVE SQUARED':           ( 0x1f170, None,    None,    '' ),
        'REGIONAL INDICATOR SYMBOL':  ( 0x1f1e6, None,    None,    '' ),
        'NEGATIVE CIRCLED':           ( 0x1f150, None,    None,    '' ),  # 0x02775 ???
        'SUPERSCRIPT':                ( None,    None,    0x02070, '123' ),
        'SUBSCRIPT':                  ( None,    None,    0x02080, '' ),

        ####### Unfinished:
        #'Subscript Latin Small'   : [],  # aehijklmnoprstuvx
    }

    GreekFontDict = {
        'BOLD':                       ( 0X1D6A8, 0X1D6C2, None, '' ),
        'ITALIC':                     ( 0X1D6E2, 0X1D6FC, None, '' ),
        'BOLD ITALIC':                ( 0X1D71C, 0X1D736, None, '' ),
        'SANS-SERIF BOLD':            ( 0X1D756, 0X1D770, None, '' ),
        # No Mathematical Greek Sans Serif Italic, apparently?
        'SANS-SERIF BOLD ITALIC':     ( 0X1D790, 0X1D7AA, None, '' ),

        ########## Unfinished:
        #'SUPERSCRIPT GREEK SMALL':   (),
        #'SUBSCRIPT GREEK SMALL':     (),
    }

    # Some of these sets lack a zero. in those cases the set is listed as
    # beginning where the zero *would* be naturally -- just before the 1.
    # TODO: Delete ones redundant with Latin list above
    #
    DigitFontDict = {
        # [ NAME                          UC    LC    DIGITS   exceptions ]
        # These are covered above:
        'BOLD':                         [ None, None, 0x1d7Ce, '' ],
        # no italic or bold italic
        'SANS SERIF':                   [ None, None, 0x1d7e2, '' ],
        'SANS SERIF BOLD':              [ None, None, 0x1d7ec, '' ],
        # no sans serif italic or bold italic
        # no script or fraktur
        'DOUBLE STRUCK':                [ None, None, 0x1d7d8, '' ],
        'MONOSPACE':                    [ None, None, 0x1d7f6, '' ],

        'FULLWIDTH':                    [ None, None, 0x0ff110, '' ],

        # no squared, negative squared, or regional indicator symbol
        #'NEGATIVE CIRCLED':             [ None, None, 0x024eb, '0' ],
        'SUPERSCRIPT LATIN':            [ None, None, 0x02070, '' ],
        'SUBSCRIPT LATIN':              [ None, None, 0x02080, '' ],

        'DIGIT COMMA':                  [ None, None, 0x1f101, '' ],
        'DIGIT FULL STOP':              [ None, None, 0x02488, '' ],

        # Starting at 1 (but offset is to where zero *would* be)
        'CIRCLED':                      [ None, None, 0x0245f, '0' ],
        'DINGBAT NEGATIVE CIRCLED':     [ None, None, 0x02775, '0' ],
        'DOUBLE CIRCLED':               [ None, None, 0x024f3, '0' ],
        'PARENTHESIZED':                [ None, None, 0x02473, '0' ],

        'FULL STOP':                    [ None, None, 0x02487, '0' ],
        'DINGBAT CIRCLED SANS-SERIF':   [ None, None, 0x0277f, '0' ],
        'DINGBAT NEGATIVE CIRCLED SANS-SERIF': [ None, None, 0x02789, '0' ],

        # circled number on black square 10-80 by 10 @ U+03248, 0 @ ????

        'ARABIC-INDIC':                 [ None, None, 0x00660, '' ],
        'EXTENDED ARABIC-INDIC':        [ None, None, 0x006F0, '' ],
        'NKO':                          [ None, None, 0x007c0, '' ],
        'DEVANAGARI':                   [ None, None, 0x00966, '' ],
        'BENGALI':                      [ None, None, 0x009e6, '' ],
        'GURMUKHI':                     [ None, None, 0x00a66, '' ],
        'GUJARATI':                     [ None, None, 0x00aE6, '' ],
        'ORIYA':                        [ None, None, 0x00b66, '' ],
        'TAMIL':                        [ None, None, 0x00bE6, '' ],
        'TELUGU':                       [ None, None, 0x00c66, '' ],
        'KANNADA':                      [ None, None, 0x00cE6, '' ],
        'MALAYALAM':                    [ None, None, 0x00d66, '' ],
        'SINHALA LITH':                 [ None, None, 0x00dE6, '' ],
        'THAI':                         [ None, None, 0x00E50, '' ],
        'LAO':                          [ None, None, 0x00Ed0, '' ],
        'TIBETAN':                      [ None, None, 0x00f20, '' ],
        'MYANMAR':                      [ None, None, 0x01040, '' ],
        'MYANMAR SHAN':                 [ None, None, 0x01090, '' ],
        'KHMER':                        [ None, None, 0x017e0, '' ],
        'MONGOLIAN':                    [ None, None, 0x01810, '' ],
        'LIMBU':                        [ None, None, 0x01946, '' ],
        'NEW TAI LUE':                  [ None, None, 0x019d0, '' ],
        'TAI THAM HORA':                [ None, None, 0x01a80, '' ],
        'TAI THAM THAM':                [ None, None, 0x01a90, '' ],
        'BALINESE':                     [ None, None, 0x01b50, '' ],
        'SUNDANESE':                    [ None, None, 0x01bb0, '' ],
        'LEPCHA':                       [ None, None, 0x01c40, '' ],
        'OL CHIKI':                     [ None, None, 0x01c50, '' ],
        'IDEOGRAPHIC NUMBER':           [ None, None, 0x03007, '' ],
        'VAI':                          [ None, None, 0x0a620, '' ],
        'SAURASHTRA':                   [ None, None, 0x0a8d0, '' ],
        'COMBINING DEVANAGARI':         [ None, None, 0x0a8e0, '' ],
        'KAYAH LI':                     [ None, None, 0x0a900, '' ],
        'JAVANESE':                     [ None, None, 0x0a9d0, '' ],
        'CHAM':                         [ None, None, 0x0aa50, '' ],
        'MEETEI MAYEK':                 [ None, None, 0x0abf0, '' ],

        # Some other related sets
        'ROMAN NUMERAL':                [ None, None, 0x0215f,   '0' ],
        'SMALL ROMAN NUMERAL':          [ None, None, 0x0216f,   '0' ],

        'PLAYING CARDS, SPADE':         [ None, None, 0x1f0a0,   '0' ],
        'PLAYING CARDS, HEART':         [ None, None, 0x1f0b0,   '0' ],
        'PLAYING CARDS, DIAMOND':       [ None, None, 0x1f0c0,   '0' ],
        'PLAYING CARDS, CLUB':          [ None, None, 0x1f0d0,   '0' ],

        'MAHJONG TILES, CHARACTER':     [ None, None, 0x1f006,   '0' ],
        'MAHJONG TILES, BAMBOO':        [ None, None, 0x1f00f,   '0' ],
        'MAHJONG TILES, CIRCLE':        [ None, None, 0x1f018,   '0' ],
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

        # Missing or misplaced zeros in digit sets (re-check)
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

    # TODO: Finish alternate sets that are trickier.
    #
    # Combing-char effects
    # These can't be done by handing back a translate table.
    # Also 'TURNED', which can be done just as exceptions.
    #
    specialDict = {
        # Name               Char
        'UNDERLINE':        [  ],
        'STRIKE':           [  ],
        'OVERLINE':         [  ],
        'SLASHED':          [  ],
    }


    ###########################################################################
    # Maybe make init take a target spec, then convert() uses it...
    #
    def __init__(self):
        return

    @staticmethod
    def getStartCodePoint(script='Latin', font='BOLD', group='U'):
        font = re.sub(r'^MATHEMATICAL ', 'M', font.upper())
        fontDict = mathAlphanumerics.getFontDict(script=script)
        if (font not in fontDict):
            raise ValueError("Uknown %s font '%s'." % (script, font))
        charInfo = fontDict[font]
        if (group == 'U'): return charInfo[0]
        if (group == 'L'): return charInfo[1]
        if (group == 'D'): return charInfo[2]
        raise ValueError(
            "Uknown %s 'group', must be 'U', 'L', or 'D'." % (script))

    @staticmethod
    def getFontDict(script='Latin'):
        """Return a dict of the "fonts" for the specified script.
        """
        if (script == 'Latin'):
            return mathAlphanumerics.LatinFontDict
        elif (script == 'Greek'):
            return mathAlphanumerics.GreekFontDict
        elif (script == 'Digit'):
            return mathAlphanumerics.DigitFontDict
        else: raise ValueError(
            "Unknown script '%s', must be Latin|Greek|Digit." %
                (script))

    @staticmethod
    def convert(ss, script="Latin", font='Bold'):
        xtab = mathAlphanumerics.getTranslateTable(script, font)
        return ss.translate(xtab)

    @staticmethod
    def getTranslateTable(script="Latin", font='BOLD'):
        #if (PY3):
        #    raise NotImplementedError("No maketrans in Python 3.")
        if (script == 'Latin'):
            tbl = mathAlphanumerics.LatinFontDict
            uSrcStart = ord('A'); uSrcEnd = ord('Z')
            lSrcStart = ord('a'); lSrcEnd = ord('z')
            dSrcStart = ord('0'); dSrcEnd = ord('9')
        elif (script == 'Greek'):
            tbl = mathAlphanumerics.GreekFontDict
            uSrcStart = 0x00391; uSrcEnd = 0x003a9
            lSrcStart = 0x003b1; lSrcEnd = 0x003c9
            dSrcStart = dSrcEnd = None
        elif (script == 'Digit'):
            tbl = mathAlphanumerics.DigitFontDict
            uSrcStart = uSrcEnd = None
            lSrcStart = lSrcEnd = None
            dSrcStart = ord('0'); dSrcEnd = ord('9')
        else: raise ValueError(
            "Unknown script '%s', must be Latin|Greek|Digit." %
                (script))

        font = font.upper()
        if (font not in tbl):
            raise ValueError("Unknown font '%s' for script '%s'." %
                (font, script))

        uTgtStart, lTgtStart, dTgtStart, _ = tbl[font]
        src = tgt = u''
        if (uTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(
                uSrcStart, uSrcEnd, uTgtStart)
            src += ss; tgt += tt
        if (lTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(
                lSrcStart, lSrcEnd, lTgtStart)
            src += ss; tgt += tt
        if (dTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(
                dSrcStart, dSrcEnd, dTgtStart)
            src += ss; tgt += tt
        xtab = str.maketrans(ss, tt)
        return xtab

    @staticmethod
    def makePartialXtab(srcStart, srcEnd, tgtStart):
        """This takes the actual first and last character codes. I noticed
        too late that this is a bit unlike the usual Python "end+1". I may
        fix it sometime.
        @return the 2 strings, which caller can make an xtab from, or pass
        to something like 'tr', or whatever.
        """
        srcTab = tgtTab = u""
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
                srcChar = unichr(srcCode)
                tgtChar = unichr(finalCode)
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
        "Cwm fjord bank glyphs vext quiz",
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
        'gaza frequens Libycum duxit Karthago triumphum',

        'heu Zama, quam Scipio celeber dux frangit inique',

        'venerat, insano Cassandrae incensus amore' +
        'et gener auxilium Priamo Phrygibusque ferebat',

        'obstipui, steteruntque comae et vox faucibus haesit.' +
        'Hunc Polydorum auri quondam cum pondere magno',

        'Nox erat, et terris animalia somnus habebat:' +
        'effigies sacrae divom Phrygiique Penates',

        'infelix Theseus; Phlegyasque miserrimus omnis' +
        'admonet, et magna testatur voce per umbras:',

        'Forte die sollemnem illo rex Arcas honorem' +
        'Amphitryoniadae magno divisque ferebat',

        'a quo post Itali fluvium cognomine Thybrim' +
        'diximus, amisit verum vetus Albula nomen;',

        'Haud procul hinc saxo incolitur fundata vetusto' +
        'urbis Agyllinae sedes, ubi Lydia quondam',

        'quid gravidam bellis urbem et corda aspera temptas?' +
        'Nosne tibi fluxas Phrygiae res vertere fundo',

        'Nosne tibi fluxas Phrygiae res vertere fundo' +
        'conamur, nos, an miseros qui Troas Achivis',

        'Tarquitus exultans contra fulgentibus armis' +
        'silvicolae Fauno Dryope quem nympha crearat',

        'ut bivias armato obsidam milite fauces.' +
        'Tu Tyrrhenum equitem conlatis excipe signis;',

        'Fovit ea volnus lympha longaevus Iapyx' +
        'ignorans, subitoque omnis de corpore fugit',

        'quantus Athos aut quantus Eryx aut ipse coruscis' +
        'cum fremit ilicibus quantus gaudetque nivali',
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
            "--font",             type=str, default="ITALIC",
            help='Character variant to convert to. Default: all.')
        parser.add_argument(
            "--indeosperamus",    action='store_true',
            help='Use actual Latin for sample sentences.')
        parser.add_argument(
            "--missing",          type=anyInt, default=0x2623,
            help=('Show this code point for undefined characters. ' +
            'Default: biohazar (U+2623).'))
        parser.add_argument(
            "--quiet", "-q",      action='store_true',
            help='Suppress most messages.')
        parser.add_argument(
            "--sample",           type=str, default=None,
            help='Sample text to convert (see also --to).')
        parser.add_argument(
            "--script",           type=str, default="Latin",
            choices=[ 'Latin', 'Greek', 'Digits' ],
            help='Script to translate to a variant "font". Default: Latin.')
        parser.add_argument(
            "--show",             action='store_true',
            help='List all fonts for the chosen script. Add -v for samples.')
        parser.add_argument(
            "--test",             action='store_true',
            help='Test getTranslateTable().')
        parser.add_argument(
            "--verbose", "-v",    action='count', default=0,
            help='Add more messages (repeatable).')
        parser.add_argument(
            "--version", action='version', version=__version__,
            help='Display version information, then exit.')

        args0 = parser.parse_args()
        return(args0)

    messageIssued = False

    def showAlternates(altList, MISSING=None):
        """Print a list of all the available variants. With -v, add samples.
        """
        global messageIssued
        for k in (sorted(altList.keys())):
            if (altList[k] is None):
                print("%-50s    DOES NOT EXIST" % (k))
                continue
            try:
                Ustart, Lstart, Dstart, _ = altList[k]
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

    def gatherChars(startCode, n, MISSING=0x0005f):
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
                buf += "%s " % (unichr(codePoint))
        except ValueError:
            if (not messageIssued): print(
                "    ******* Out of unichr() range *******")
            messageIssued = True
        return buf

    def testXtabs(altList, sample=None):
        """Given one of the lists, like mathAlphanumerics.LatinFontDict, set up
        translate tables and print the result on a sample sentence.
        """
        if (not sample): sentence = getRandomSentence()

        for k in (sorted(altList.keys())):
            if (altList[k] is None):
                print("%-50s    DOES NOT EXIST" % (k))
                continue
            xtab = mathAlphanumerics.getTranslateTable(args.script, k)
            print('    ' + sentence.upper().translate(xtab))
            print('    ' + sentence.lower().translate(xtab))
            print('    ' + '0123456789'.translate(xtab))

    def getRandomSentence():
        import random
        if (args.indeosperamus):
            return random.choice(mathAlphanumerics.LatinSentences)
        else:
            return random.choice(mathAlphanumerics.EnglishSentences)

    ###########################################################################
    #
    args = processOptions()

    try:
        _ = unichr(0x1d49c)
    except ValueError as e:
        warn(-1, "Character over U+FFFF failed. Upgrade Python?\n  %s\n" % (e))

    if (args.script == 'Greek'):
        scr = 'Greek'
        fonts = mathAlphanumerics.GreekFontDict
    elif (args.script == 'Digits'):
        scr = 'Digits'
        fonts = mathAlphanumerics.DigitFontDict
    elif (args.script == 'Latin'):
        scr = 'Latin'
        fonts = mathAlphanumerics.LatinFontDict
    else:
        warn(-1, "Unknown 'script': '%s'." % (args.script))

    if (args.show):
        messageIssued = False
        print("\nAvailable alts for %s:" % (scr))
        showAlternates(fonts, args.missing)
        if (not args.verbose): print("(to see samples, use -v)")

    elif (args.sample):
        args.font = args.font.title()
        print("\nSample conversion for %s '%s':" % (scr, args.font))
        if (args.sample is None):
            args.sample = getRandomSentence()
        txt = args.sample
        if (txt == '' or txt == '*'): txt = getRandomSentence()
        s = mathAlphanumerics.convert(txt,
            script=args.script, font=args.font)
        print('    ' + txt + "\n    " + s)

    elif (args.test):
        testXtabs(fonts)

    else:  # translate stdin
        if (sys.stdin.isatty()):
            print("Waiting on stdin...")
        xt = mathAlphanumerics.getTranslateTable(scr, args.font)
        import io
        istream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        #sys.stdin.reconfigure(encoding='utf-8')
        for rec in istream:
            print(rec.translate(xt))

    sys.exit()