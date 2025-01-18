#!/usr/bin/env python3
#
# fixQuotes.py: Mess with various quotation marks and such.
# 2020-10-14: Written by Steven J. DeRose.
#
import sys
import os
import codecs
import re
from typing import List

__metadata__ = {
    "title"        : "fixQuotes",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.11",
    "created"      : "2020-10-14",
    "modified"     : "2024-07-05",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr = """
==Description==

Convert quotations between various Unicode forms or XML/HTML markup.
By default, turn them all into ASCII apostrophe or double-quote. or markup.
For example:

   These “quotes” are ‘very’ 'important', `aren't` `they'?

to

    These "quotes" are 'very' 'important', `aren't` `they'?

To covert to markup, use the `--toTag [tagname]` option.

Back-quotes (aka GRAVE ACCENT, U+0060) are not affected unless you
specifically set `--backQuotes`. This is because of the alternative
conventions for them, as shown in the example above.

Does not change lone apostrophes or quotes; there must be a left quote
(single or double, of any active type) and a right. To skip over
escaped right quotes, specify --escapeChar [char]. However, this does
not yet handle that char itself being escaped.

Does not handle nested quotes of a single type. such as:
    Amy said "Bill said "Chris is here.""

If an input file's extension is htm, html, xml, or svg, then the file
is parsed and only the text nodes are affected (that is, quotes in markup
such as those around attribute values are not touched).

==Usage==

For example, to use from a command line:

    fixQuotes --toTag "q" myFile.txt

or

    fixQuotes --singleSet "sangle" --doubleSet "dangle" myFile.txt

You can see a list of the named quoting character pairs with `--showNames`.

To use from Python code:

    from fixQuotes import FixQuotes
    qf = FixQuotes()
    myString = qf.fix(myString)


==Methods==

You can set similarly-named keyword options when constructing
a `fixQuotes` instance, as you can set on the command line (q.v.):

* backQuotes:bool=False

* leftSingle:str="'"

* rightSingle:str="'"

* leftDouble:str="\""

* rightDouble:str="\""

* ignoreQuote:list=None

* iencoding:str="utf-8",

* normalizeSpaces:bool=False

* toTag:str=''


==Related Commands==

My `showKeyCodes`, which will take keystrokes and tell you what got sent.

My `normalizeUnicode.py` (and .pl), which do a variety of other character
set mappings.


==Known bugs and Limitations==

Weird things can happen with console and pipe i/o for non-ASCII. The
--iencoding and --oencoding options, and the defaults in Python 3
''should'' handle it fine, but I'm not completely certain.

Does not protect quotes inside markup, such as around attributes, unless
the extension is one we know about (htm, html, xml, svg).

Does not yet handle nested cases for translation ''to'' markup.

Cannot yet translate ''<q>'' etc. to literal quotes (etc.).

Does not do anything for characters represented
via backslash codes, named or numeric entities, etc.

`--escapeChar` support doesn't consider the escapechar being escaped.

`--normalizeSpaces` does not affect hard space (`&nbsp;` or `U+000A0`).

--singleSet can only take singles, and --doubleSet doubles. You can do other
combinations by setting --leftSingle etc. separately (--showNames also shows
the hex code points and literals for all the named sets).


==To do==

* Better option naming and organization.
* Separate 'educate' option to get from plain to curly or other pairs.
* Perhaps should have something for MarkDown-ish '''xyz'''.


==History==

* 2020-10-14: Written by Steven J. DeRose.
* 2020-10-19: Hook up PowerWalk options. Start making into a class.
* 2024-07-05: Add --show. Take PowerWalk back out, too many options.


==To do==

* Re-run various tests, having introduced FixQuotes class.
* Add `...' case.
* Add HTML and XML in/out, like <q> and settable.
* Perhaps support non-single-character (xtab) mappings, like to "''"
* Add entity, backslash, and other formats.
    \'
    &#34; &#x22; &quot;
    &#39; &#x27; &apos;


==Rights==

Copyright 2020-10-14 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/ for more information].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


==Options==
"""

class FixQuotes:
    singlePairs = {
        # 'back':   [ 0x0060, 0x0060 ],  # GRAVE ACCENT
        "splain":   [ 0x0027, 0x0027 ],  # Apostrophe / single quotation mark
        "single":   [ 0x2018, 0x2019 ],  # "SINGLE QUOTATION MARK",
        "sangle":   [ 0x2039, 0x203A ],  # "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        "slow9":    [ 0x201A, 0x201B ],  # "SINGLE LOW-9 QUOTATION MARK",
        "sprime":   [ 0x2032, 0x2035 ],  # "PRIME", "REVERSED PRIME",
        "scommaO":  [ 0x275B, 0x275C ],  # HEAVY SINGLE TURNED COMMA QM ORNAMENT
    }

    doublePairs = {
        "dplain":   [ 0x0022, 0x0022 ],  # Double quotation mark
        "double":   [ 0x201C, 0x201D ],  # "LEFT DOUBLE QUOTATION MARK",
        "dangle":   [ 0x00AB, 0x00BB ],  # "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        "dlow9":    [ 0x201E, 0x201F ],  # "DOUBLE LOW-9 QUOTATION MARK",
        "dprime":   [ 0x301E, 0x301E ],  # "DOUBLE PRIME QUOTATION MARK",
        "tprime":   [ 0x2034, 0x2037 ],  # "TRIPLE PRIME", "REVERSED TRIPLE PRIME",

        "rdprime":  [ 0x2057, 0x301D ],  # "REVERSED DOUBLE PRIME QUOTATION MARK",
            # = "QUADRUPLE PRIME"

        "fullwidth":[ 0xFF02, 0xFF02 ],  # FULLWIDTH QUOTATION MARK
        "dcommaO":  [ 0x275D, 0x275E ],  # Heavy Double Turned Comma QM Ornament
        "hangleO":  [ 0x276E, 0x276F ],  # Heavy Left-pointing Angle QM Ornament
        "sshdcommonO": [ 0x1F677, 0x1F678 ],  # Sans-serif Heavy Double Comma QM Ornament
    }

    def __init__(self,
        backQuotes:bool=False,
        leftSingle:str="'",
        rightSingle:str="'",
        leftDouble:str="\"",
        rightDouble:str="\"",
        ignoreQuote:list=None,
        iencoding:str="utf-8",
        normalizeSpaces:bool=False,
        toTag:str="",
        escapeChar:str=""
        ):
        self.backQuotes         = backQuotes
        self.leftSingle         = leftSingle
        self.rightSingle        = rightSingle
        self.leftDouble         = leftDouble
        self.rightDouble        = rightDouble
        self.ignoreQuote        = ignoreQuote
        self.iencoding          = iencoding
        self.normalizeSpaces    = normalizeSpaces
        self.toTag              = toTag
        self.escapeChar         = escapeChar

        sp = self.singlePairs.copy()
        dp = self.doublePairs.copy()
        if (ignoreQuote):
            for q0 in ignoreQuote:
                if (q0 in sp): del sp[q0]
                elif (q0 in dp): del dp[q0]
                else: raise ValueError(
                    "Unknown quote type to ignore: '%s'." % (q0))
        if (backQuotes):
            sp['back'] = [ 0x0060, 0x0060 ]

        self.xtab = self.makeXtab(sp, dp,
            self.leftSingle, self.rightSingle,
            self.leftDouble, self.rightDouble)

        self.quoteExpr = self.makeQuoteExpr(self.escapeChar)

    def makeXtab(self, sp:List, dp:List,
        leftSingle:str, rightSingle:str, leftDouble:str, rightDouble:str):
        src = tgt = ""
        for l, r in sp.values():
            src += chr(l) + chr(r)
            tgt += leftSingle + rightSingle
        for l, r in dp.values():
            src += chr(l) + chr(r)
            tgt += leftDouble + rightDouble
        warning("Making xtab:\n    |%2d| #%s#\n    |%2d| #%s#" %
            (len(src), src, len(tgt), tgt))
        return str.maketrans(src, tgt)

    @staticmethod
    def makeQuoteExpr(escapeChar:str="") -> str:
        """Create regex to match entire quotes.
        Does not yet handle nested cases!
        """
        # Lookbehind for backslash or whatever
        if (escapeChar): escExpr = r"(?<!\\%s)" % (escapeChar)
        else: escExpr = ""

        expr = ""
        for l, r in FixQuotes.singlePairs.values():
            expr += chr(l) + r'.*?' + escExpr + chr(r) + '|'
        for l, r in FixQuotes.doublePairs.values():
            expr += chr(l) + r'.*?' + escExpr + chr(r) + '|'
        expr = expr[0:-1]
        warning("Making regex:\n    #%s#" % (expr))
        return re.compile(expr)

    def fix(self, s:str) -> str:
        if (self.toTag):
            return self.fixToTag(s, self.quoteExpr, self.toTag)
        else:
            return s.translate(self.xtab)

    @staticmethod
    def fixToTag(s:str, theRegex:str, tagName:str) -> str:
        """Does not yet handle nested cases!
        """
        tgt = "<%s>\\1</%s>" % (tagName, tagName)
        return re.sub(theRegex, tgt, s)

    @staticmethod
    def normalizeSpace(s:str, compress:bool=False) -> str:
        """\\s doesn't include hard space.
        """
        if (compress):
            return re.sub(r'[\s\xA0]+', ' ', s, flags=re.UNICODE)
        return re.sub(r'[\s\xA0]', ' ', s, flags=re.UNICODE)


###############################################################################
#
dirCount = 0
fileCount = 0
verbose = 0

def warning(msg:str) -> None:
    if verbose: sys.stderr.write(msg + "\n")

def doOneFile(path:str, fixer):
    """Read and deal with one individual file.
    """
    if (not path):
        if (sys.stdin.isatty() and not args.quiet): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            warning("Cannot open '%s':\n    %s" % (e))
            return 0

    recnum = 0
    for rec in fh.readlines():
        recnum += 1
        if (args.normalizeSpaces):
            rec = FixQuotes.normalizeSpace(rec)
        print(fixer.fix(rec))
    return(recnum)

def doOneXmlFile(path, fixer):
    """Parse and load
    """
    from xml.dom import minidom
    from domextensions import DomExtensions
    DomExtensions.patchDom(minidom.Node)
    xdoc = minidom.parse(path)
    docEl = xdoc.documentElement
    tns = docEl.getTextNodesIn(docEl)
    for tn in tns:
        s = tn.data
        if (args.normalizeSpaces):
            s = FixQuotes.normalizeSpace(s)
        tn.data = fixer.fix(s)
    print(docEl.collectAllXml2())
    return(0)


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse

    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--backQuotes", action='store_true',
            help='Also map backquote (U+0060) to apostrophe.')
        parser.add_argument(
            "--leftSingle", type=str, metavar='E', default="'",
            help="What to change left single quotes to. Default: \"'\".")
        parser.add_argument(
            "--rightSingle", type=str, metavar='E', default="'",
            help="What to change right single quotes to. Default: \"'\".")
        parser.add_argument(
            "--leftDouble", type=str, metavar='E', default="\"",
            help="What to change left double quotes to. Default: '\"'.")
        parser.add_argument(
            "--rightDouble", type=str, metavar='E', default="\"",
            help="What to change right double quotes to. Default: '\"'.")

        qNames = list(FixQuotes.singlePairs.keys())
        qNames.extend(FixQuotes.doublePairs.keys())
        parser.add_argument(
            "--ignoreQuote", type=str, action='append', choices=qNames,
            help='Drop the named quote type from the list to recognize. Repeatable.')
        parser.add_argument(
            "--singleSet", type=str, metavar='T', choices=qNames,
            help='Convert to this named pair of single-quote characters.')
        parser.add_argument(
            "--doubleSet", type=str, metavar='T', choices=qNames,
            help='Convert to this named pair of doubkle-quote characters')

        parser.add_argument(
            "--iencoding", type=str, metavar='E', default="utf-8",
            help='Assume this character set for input files. Default: utf-8.')
        parser.add_argument(
            "--normalizeSpaces", "--spaces", action='store_true',
            help='Also convert all Unicode whitespace to ASCII space.')
        parser.add_argument(
            "--oencoding", type=str, metavar='E', default="utf-8",
            help='Use this character set for output files.')
        parser.add_argument(
            "--quiet", "-q", action='store_true',
            help='Suppress most messages.')
        parser.add_argument(
            "--showNames", "--list", action='store_true',
            help='Display the named quote types, and exit.')
        parser.add_argument(
            "--test", action='store_true',
            help='Run a small self test.')
        parser.add_argument(
            "--toTag", type=str, metavar='T', default='',
            help='Convert quotations to XML elements of this name (such as "q").')
        parser.add_argument(
            "--unicode", action='store_const', dest='iencoding',
            const='utf8', help='Assume utf-8 for input files.')
        parser.add_argument(
            "--verbose", "-v", action='count', default=0,
            help='Add more messages (repeatable).')
        parser.add_argument(
            "--version", action='version', version=__version__,
            help='Display version information, then exit.')

        parser.add_argument(
            'files', type=str, nargs=argparse.REMAINDER,
            help='Path(s) to input file(s)')

        args0 = parser.parse_args()
        return(args0)

    def runTest(fixer):
        sample = ("""<q class="foo">The 'quick' "brown" """ +
            """`over` the dog's cat's.</q>""")
        print(sample)
        result = fixer.fix(sample)
        print(result)


    ###########################################################################
    #
    fileCount = 0
    args = processOptions()

    if (args.verbose):
        verbose = args.verbose

    if (args.showNames):
        print("Named quote types:")
        print("Singles:")
        for k, pair in FixQuotes.singlePairs.items():
            print("    %-12s [ U+%05x, U+%05x ] = [ '%s', '%s' ]" %
                (k, pair[0], pair[0], chr(pair[0]), chr(pair[0])))
        print("Doubles:")
        for k, pair in FixQuotes.doublePairs.items():
            print("    %-12s [ U+%05x, U+%05x ] = [ '%s', '%s' ]" %
                (k, pair[0], pair[0], chr(pair[0]), chr(pair[0])))
        sys.exit()

    fixerObj = FixQuotes(
        backQuotes      = args.backQuotes,
        leftSingle      = args.leftSingle,
        rightSingle     = args.rightSingle,
        leftDouble      = args.leftDouble,
        rightDouble     = args.rightDouble,
        ignoreQuote     = args.ignoreQuote,
        iencoding       = args.iencoding,
        normalizeSpaces = args.normalizeSpaces,
        toTag           = args.toTag
    )

    if (args.singleSet):
        fixerObj.leftSingle  = FixQuotes.singlePairs[args.singleSet][0]
        fixerObj.rightSingle = FixQuotes.singlePairs[args.singleSet][1]

    if (args.doubleSet):
        fixerObj.leftDouble  = FixQuotes.doublePairs[args.doubleSet][0]
        fixerObj.rightDouble = FixQuotes.doublePairs[args.doubleSet][1]

    if (args.oencoding):
        sys.stdout.reconfigure(encoding='utf-8')

    if (args.test):
        runTest(fixerObj)
    elif (len(args.files) == 0):
        #if (sys.stdin.isatty): warning("fixQuotes: No files specified....")
        doOneFile(None, fixerObj)
    else:
        for path0 in args.files:
            fileCount += 1
            ext = os.path.splitext(path0)
            if (ext in [ ".htm", ".html", ".xml", ".svg" ]):
                doOneXmlFile(path0, fixerObj)
            else:
                doOneFile(path0, fixerObj)
