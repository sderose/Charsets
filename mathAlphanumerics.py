#!/usr/bin/env python
#
# mathAlphanumerics.py: Map Latin etc. to special math areas.
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
    'modified'     : "2020-07-25",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr = """
=Description=

Provide support for using the many Unicode variations on alphabets and digits.

''Note:'' Throughout this package, "script" has a slightly different meaning
than "Unicode script": It means just the basic 'Latin' or 'Greek' alphabet, or
the set of ten 'Digits'. "font" does not refer to typographic fonts
per se, but to Unicode's sets of variations on the basic "scripts" just named,
such as "MATHEMATICAL SANS-SERIF BOLD ITALIC" (the names used here are taken
directly from the Unicode character names, except that "MATHEMATICAL" may be
omitted and case is ignored).

Using this package directly from the command line (without `-h`) will
do the chosen translation on `stdin`.

To see a list of the variant "font" names available for the selected
`--script`, (for example, "SANS-SERIF BOLD ITALIC"), with a sample of each and
the code point where each starts:

    mathAlphanumerics.py --show -v

Scripts supported include "Latin" (the default), "Greek", and "Digits"
(see `--script`).

'''Note:''' This will only work is your display medium supports Unicode,
and the exact results depend on the font(s) in use. Even then, a few
characters appear to be missing, such as "PARENTHESIZED DIGIT ZERO". When a
mapping is not available, the character is left unchanged.

==Usage==

You can just pipe Unicode text through this like:

    cat eggs.txt | mathAlphanumerics --font 'BOLD ITALIC' | lpr

The default `--script` is Latin, and the default `--font`
is `MATHEMATICAL BOLD` (you can omit `MATHEMATICAL ` from names).

Or you can call the package from Python, like:

    import mathAlphanumerics.py
    s2 = mathAlphanumerics.convert(text,
            scriptName="Latin", fontName="Mathematical Bold")

or

    xtab = mathAlphanumerics.getTranslateTable(
        'Latin', 'Mathematical Sans-serif Bold Italic')
    s = s.translate(xtab)

==Accented and other characters==

This only translates the unaccented basic letters and digits. However, you can
use Unicode `canonical decomposition` first, so diacritics become separate
characters. You can then use this package to modify the base characters

    import unicodedata
    s = unicodedata.normalize('NFD', myString).translate(xtab)

The result should be reasonable, although imperfect. For example,
diacritic placement could be odd, such as the
conflicting with an enclosing circle or being off center for italics.
And the diacritic itself will not be bold, circled, etc.

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

==convert(s, scriptName="Latin", fontName='Bold')==

Just convert characters in the string `s` that are from the given "script" to the specified "font".

For 'Latin', uppercase, lowercase, and digits are converted (when available).

For 'Greek', uppercase and lowercase are converted (when available).

For 'Digits', only digits 0-9 are converted (and only when available).

==getTranslateTable(scriptName="Latin", fontName='BOLD')==

Return a Python 3 translation table generated for the specified `script`
and `font`. Exceptions are integrated, and omissions are omitted.

==makePartialXtab(srcStart, srcEnd, tgtStart)==

=Variables=

==LatinFontDict==

A dict keyed by the common part of Unicode names for characters in the
alternate Latin alphabets such as 'FRAKTUR BOLD' (here called "fonts").
"MATHEMATICAL" is always omitted from the keys. The values are 4-tuples.
For example:

    'SCRIPT':           ( 0x1d49c, 0x1d4b6, None, 'BEFHILMR ego')
    'NEGATIVE SQUARED': ( 0x1f170, None,    None, '' ),

The tuples contain the starting code points for the uppercase,
lowerecase, and digits, and a string listing characters which are not at
the "expected" point (often '', and next-most often '0').
If the range does not exist (or if I failed to locate it), it is listed as None.
If the first character of the described range does not actually exist, the
starting codepoint is still specified as if it did, but the first character
is listed among the exceptions, and `exceptions` maps it to None.

==GreekFontDict==

Like `LatinFontDict`, but for Greek. None of these include digits or exceptions.

==DigitFontDict==

Like `LatinFontDict`, but for sets of the digits 0-9.
This includes other number-ish sets, such as Roman numerals, playing cards, etc,
although many of these do not include zero (which is therefore left unchanged
by `convert()` etc.
The uppercase and lowercase start-points are always None, and the
exceptions are always either '' or '0'.

==exceptions==

This is a simple list of code point pairs, mapping characters that
one might expect to be in the supported sets, but are either at some code
pointe elsewhere in Unicode, or not in Unicode at all (as far as I know).
The former are mapped to the codepoint elsewhere, and the latter to None.
For example:

    0X1D455: 0X210E,  # MATHEMATICAL ITALIC SMALL H (PLANCK CONSTANT)
    0X1D49D: 0X212C,  # MATHEMATICAL SCRIPT CAPITAL B

The `exceptions` lists has no information (except comments) saying which
"script" or "font" each exception is from. If needed, this could be
determined by comparing the key of interest to the ranges whose starts are
listed in `LatinFontDict`, `GreekFontDict`, and `DigitFontDict`.

==EnglishSentences==

This list is used by the testing options to get an English sentence containing
all the Latin letters. See [https://en.wikipedia.org/wiki/Pangram]. It
seemed too ironic to name it "LatinSentences."

==LatinSentences==

EnglishSentences`, but actually in Latin, not just Latin script.
See [http://thecampvs.com/2009/03/16/latin-hexameter-pangrams],
[https://latin.stackexchange.com/questions/550/is-there-a-latin-version-of-quick-brown-fox], etc.

=Related Commands=

My `ord --math` will show a list of these characters.

`UnicodeAltLatin.py` a previous draft of this.


=Known bugs and Limitations=

Characters with diacritics must be decomposed first.

Cannot translate multiple scripts simultaneously.

Punctuation is not yet supported, such as superscript and subscript
parentheses, plus, minus, etc. Some superscript letters might be
added via "Modifier letters", but are not supported yet.

Non-Latin digit series are not fully integrated and tested.

Numbers beyond single digits (such as for roman numerals,
circled numbered, etc.) are not supported.

"Modifier letters" are not supported.

This package does not provide a way to translate the various alternate
set back to plain Latin or Greek or Digits. However, this can be done
pretty well with Unicode "compatibility composition".

"MONOSPACE" is not very distinctive on terminals that always use monospace
anyway.

[https://www.unicode.org/reports/tr25/tr25-6.html#_Toc2] notes that the
Mathematical Greek uppercase sets include "nabla ∇ (U+2207) and the variant of theta Θ given by U+03F4", and lowercase include
"the partial differential sign ∂ (U+2202) and the six glyph variants of ε, θ, κ, φ, ρ, and π, given by U+03F5, U+03D1, U+03F0, U+03D5, U+03F1, and U+03D6."
They are not supported here.


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

=To do=

* Rename

* Better testing for non-Latin digits.

* Possibly add a "PLAIN" 'font' that just does null translation.

* Possibly add combining characters such as underscore, strike-through, and
overline.

* Possibly add turned (cf reversed)
    U+02c6f	Ɐ	LATIN CAPITAL LETTER TURNED A
    e => schwa
    U+02132	Ⅎ	TURNED CAPITAL F
    U+02141	⅁	TURNED SANS-SERIF CAPITAL G
    U+02142	⅂	TURNED SANS-SERIF CAPITAL L
    U+0a780	Ꞁ	LATIN CAPITAL LETTER TURNED L
    U+0a78d	Ɥ	LATIN CAPITAL LETTER TURNED H
    U+0019c	Ɯ	LATIN CAPITAL LETTER TURNED M
    U+00245	Ʌ	LATIN CAPITAL LETTER TURNED V
    U+02144	⅄	TURNED SANS-SERIF CAPITAL Y

    U+00250	ɐ	LATIN SMALL LETTER TURNED A
    b => q
    U+02184	ↄ	LATIN SMALL LETTER REVERSED C
    d => p
    U+001dd	ǝ	LATIN SMALL LETTER TURNED E
    U+0214e	ⅎ	TURNED SMALL F
    U+01d77	ᵷ	LATIN SMALL LETTER TURNED G
    U+00265	ɥ	LATIN SMALL LETTER TURNED H
    U+01d09	ᴉ	LATIN SMALL LETTER TURNED I
    j => medial s?
    U+0029e	ʞ	LATIN SMALL LETTER TURNED K
    U+0a781	ꞁ	LATIN SMALL LETTER TURNED L
    U+0026f	ɯ	LATIN SMALL LETTER TURNED M
    n => u
    o = o
    p => d
    q => b
    U+00279	ɹ	LATIN SMALL LETTER TURNED R
    s = s
    U+00287	ʇ	LATIN SMALL LETTER TURNED T
    u => n
    U+0028c	ʌ	LATIN SMALL LETTER TURNED V
    U+0028d	ʍ	LATIN SMALL LETTER TURNED W
    x = x
    U+0028e	ʎ	LATIN SMALL LETTER TURNED Y
    z = z

* Possibly add reversed
    c => U+02183	Ↄ	ROMAN NUMERAL REVERSED ONE HUNDRED
    U+0018e	Ǝ	LATIN CAPITAL LETTER REVERSED E
    U+02143	⅃	REVERSED SANS-SERIF CAPITAL L

    U+02184	ↄ	LATIN SMALL LETTER REVERSED C
    U+00258	ɘ	LATIN SMALL LETTER REVERSED E

* Possibly add small cap (not in a neat 26-char block)
    U+01d00	ᴀ	LATIN LETTER SMALL CAPITAL A
    U+00299	ʙ	LATIN LETTER SMALL CAPITAL B  (far)
    U+01d04	ᴄ	LATIN LETTER SMALL CAPITAL C
    U+01d05	ᴅ	LATIN LETTER SMALL CAPITAL D
    U+01d07	ᴇ	LATIN LETTER SMALL CAPITAL E
    U+0a730	ꜰ	LATIN LETTER SMALL CAPITAL F  (far)
    U+00262	ɢ	LATIN LETTER SMALL CAPITAL G  (far)
    U+0029c	ʜ	LATIN LETTER SMALL CAPITAL H  (far)
    U+0026a	ɪ	LATIN LETTER SMALL CAPITAL I  (far)
    U+01d0a	ᴊ	LATIN LETTER SMALL CAPITAL J
    U+01d0b	ᴋ	LATIN LETTER SMALL CAPITAL K
    U+0029f	ʟ	LATIN LETTER SMALL CAPITAL L  (far)
    U+01d0d	ᴍ	LATIN LETTER SMALL CAPITAL M
    U+00274	ɴ	LATIN LETTER SMALL CAPITAL N  (far)
    U+01d0f	ᴏ	LATIN LETTER SMALL CAPITAL O
    U+01d18	ᴘ	LATIN LETTER SMALL CAPITAL P
    q???
    U+00280	ʀ	LATIN LETTER SMALL CAPITAL R  (far)
    U+0a731	ꜱ	LATIN LETTER SMALL CAPITAL S  (far)
    U+01d1b	ᴛ	LATIN LETTER SMALL CAPITAL T
    U+01d1c	ᴜ	LATIN LETTER SMALL CAPITAL U
    U+01d20	ᴠ	LATIN LETTER SMALL CAPITAL V
    U+01d21	ᴡ	LATIN LETTER SMALL CAPITAL W
    x???
    U+0028f	ʏ	LATIN LETTER SMALL CAPITAL Y  (far)
    U+01d22	ᴢ	LATIN LETTER SMALL CAPITAL Z

* Possibly add superscript
    U+02071	ⁱ	SUPERSCRIPT LATIN SMALL LETTER I
    U+0207f	ⁿ	SUPERSCRIPT LATIN SMALL LETTER N

* Possibly add subscript
    U+02090	ₐ	LATIN SUBSCRIPT SMALL LETTER A
    U+02091	ₑ	LATIN SUBSCRIPT SMALL LETTER E
    U+02095	ₕ	LATIN SUBSCRIPT SMALL LETTER H
    U+01d62	ᵢ	LATIN SUBSCRIPT SMALL LETTER I
    U+02c7c	ⱼ	LATIN SUBSCRIPT SMALL LETTER J
    U+02096	ₖ	LATIN SUBSCRIPT SMALL LETTER K
    U+02097	ₗ	LATIN SUBSCRIPT SMALL LETTER L
    U+02098	ₘ	LATIN SUBSCRIPT SMALL LETTER M
    U+02099	ₙ	LATIN SUBSCRIPT SMALL LETTER N
    U+02092	ₒ	LATIN SUBSCRIPT SMALL LETTER O
    U+0209a	ₚ	LATIN SUBSCRIPT SMALL LETTER P
    U+01d63	ᵣ	LATIN SUBSCRIPT SMALL LETTER R
    U+0209b	ₛ	LATIN SUBSCRIPT SMALL LETTER S
    U+0209c	ₜ	LATIN SUBSCRIPT SMALL LETTER T
    U+01d64	ᵤ	LATIN SUBSCRIPT SMALL LETTER U
    U+01d65	ᵥ	LATIN SUBSCRIPT SMALL LETTER V
    U+02093	ₓ	LATIN SUBSCRIPT SMALL LETTER X

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

    biFeatures = [ 'Bold', 'Italic' ]

    """These are the 'fonts' available as Unicode 'Mathematical' variations on
    Latin. A similar list is available for Greek, and for digits.
    NOTE: "MATHEMATICAL is omitted for compactness.
    """
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
        #0X0245F: 0X24EA,  # CIRCLED DIGIT ZERO
        #0x02488: None,    # DIGIT FULL STOP ZERO
        #0X024F4: None,    # DOUBLE CIRCLED DIGIT ZERO
        #0X02744: None,    # NEGATIVE CIRCLED DIGIT 0
        #0X02789: None,    # [DINGBAT] CIRCLED SANS-SERIF 0
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
    def convert(ss, scriptName="Latin", fontName='Bold'):
        xtab = mathAlphanumerics.getTranslateTable(scriptName, fontName)
        return ss.translate(xtab)

    @staticmethod
    def getTranslateTable(scriptName="Latin", fontName='BOLD'):
        #if (PY3):
        #    raise NotImplementedError("No maketrans in Python 3.")
        if (scriptName == 'Latin'):
            tbl = mathAlphanumerics.LatinFontDict
            uSrcStart = ord('A'); uSrcEnd = ord('Z')
            lSrcStart = ord('a'); lSrcEnd = ord('z')
            dSrcStart = ord('0'); dSrcEnd = ord('9')
        elif (scriptName == 'Greek'):
            tbl = mathAlphanumerics.GreekFontDict
            uSrcStart = 0x00391; uSrcEnd = 0x003a9
            lSrcStart = 0x003b1; lSrcEnd = 0x003c9
            dSrcStart = dSrcEnd = None
        elif (scriptName == 'Digit'):
            tbl = mathAlphanumerics.DigitFontDict
            uSrcStart = uSrcEnd = None
            lSrcStart = lSrcEnd = None
            dSrcStart = ord('0'); dSrcEnd = ord('9')
        else: raise ValueError(
            "Unknown scriptName '%s', must be Latin|Greek|Digit." %
                (scriptName))

        fontName = fontName.upper()
        if (fontName not in tbl):
            raise ValueError("Unknown fontName '%s' for script '%s'." %
                (fontName, scriptName))

        uTgtStart, lTgtStart, dTgtStart, _ = tbl[fontName]
        src = tgt = u''
        if (uTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(uSrcStart, uSrcEnd, uTgtStart)
            src += ss; tgt += tt
        if (lTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(lSrcStart, lSrcEnd, lTgtStart)
            src += ss; tgt += tt
        if (dTgtStart):
            ss, tt = mathAlphanumerics.makePartialXtab(dSrcStart, dSrcEnd, dTgtStart)
            src += ss; tgt += tt
        xtab = str.maketrans(ss, tt)
        return xtab

    @staticmethod
    def makePartialXtab(srcStart, srcEnd, tgtStart):
        srcTab = tgtTab = u""
        tgtCode = tgtStart
        for srcCode in range(srcStart, srcEnd):
            if (tgtCode not in mathAlphanumerics.exceptions):
                finalCode = tgtCode
            else:
                finalCode = unichr(mathAlphanumerics.exceptions[tgtCode])
            if (finalCode is not None):
                srcChar = unichr(srcCode)
                tgtChar = unichr(finalCode)
                if (srcChar is None or tgtChar is None):
                    raise ValueError("Bad code point 0x%05x or 0x%05x." %
                        (srcCode,finalCode))
                srcTab += srcChar
                tgtTab += tgtChar
            tgtCode += 1
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
            "--font",             type=str, default="BOLD ITALIC",
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

    if (args.script == 'Greek'):
        scr = 'Greek'
        fonts = mathAlphanumerics.GreekFontDict
    elif (args.script == 'Digits'):
        scr = 'Digits'
        fonts = mathAlphanumerics.DigitFontDict
    else:  # 'Latin'
        scr = 'Latin'
        fonts = mathAlphanumerics.LatinFontDict

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
            scriptName=args.script, fontName=args.font)
        print('    ' + txt + "\n    " + s)

    elif (args.test):
        testXtabs(fonts)

    else:  # translate stdin
        xt = mathAlphanumerics.getTranslateTable(scr, args.font)
        import io
        istream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        #sys.stdin.reconfigure(encoding='utf-8')
        for rec in istream:
            print(rec.translate(xt))

    sys.exit()
