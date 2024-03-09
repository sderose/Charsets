#!/usr/bin/env python3
#
# fixQuotes.py: Mess with various quotation marks and such.
# 2020-10-14: Written by Steven J. DeRose.
#
import sys
import os
import codecs
import re

from PowerWalk import PowerWalk, PWType

__metadata__ = {
    'title'        : "fixQuotes",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 3.7",
    'created'      : "2020-10-14",
    'modified'     : "2020-11-19",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']


descr = """
=Description=

Convert quotations between various forms. By default, turn them all
into ASCII apostrophe or double-quote.

If an input file's extension is htm, html, xml, or svg, then the file
is parsed and only the text nodes are affected (that is, quotes in markup
are not touched).

For example, to use from a command line:

    fixQuotes myFile.txt

or, to use from Python code:

    from fixQuotes import FixQuotes
    qf = FixQuotes()
    myString = qf.fix(myString)

Either way would accomplish the default change, which takes all
open and close double quotes (angle, curly, 9, etc) to '"',
and all singles to "'":

    These ‘quotes’ are ”very” 'important', `aren't` `they'?

to
    These 'quotes' are "very" 'important', `aren't` `they'?

Note that back-quotes (aka grave accent) are not affected unless you
specifically set `--backQuotes`. This is because of the alternative
conventions for them, as shown in the example above.


=Methods=

You can set similarly-named keyword options when constructing
a `fixQuotes` instance,
as you can set on the command line (q.v.):

* backQuotes:bool=False

* leftSingle:str="'"

* rightSingle:str="'"

* leftDouble:str="\""

* rightDouble:str="\""

* ignoreQuote:list=None

* iencoding:str="utf-8",

* normalizeSpaces:bool=False

* toTag:str=''


=Related Commands=

My `showKeyCodes`, which will take keystrokes and tell you what got sent.

My `normalizeUnicode.py` (and .pl), which do a variety of other character
set mappings.


=Known bugs and Limitations=

Weird things can happend with console and pipe i/o for non-ASCII. The
iencoding and oencoding options, and the defaults in Python 3 (though not 2)
''should'' handle it fine, but I'm not completely certain.

Does not protect quotes inside markup, such as around attributes, unless
the extension is one we know about (htm, html, xml, svg).

Does not yet handle nested cases for translation ''to'' markup.

Cannot yet translate ''<q>'' etc. to literal quotes (etc.).

Does not do anything for characters represented
via backslash codes, named or numeric entities, etc.

`--normalizeSpaces` does not affect hard space (`&nbsp;` or `U+000A0`).


=To do

* Better option naming and organization.
* Separate 'educate' option to got from plain to curly or other pairs.


=History=

* 2020-10-14: Written by Steven J. DeRose.
* 2020-10-19: Hook up PowerWalk options.
Start making into a class.


=To do=

* Re-run various tests, having introduced FixQuotes class.
* Add `...' case.
* Add HTML and XML in/out, like <q> and settable.
* Perhaps support non-single-character (xtab) mappings, like to "''"
* Add entity, backslash, and other formats.
    \'
    &#34; &#x22; &quot;
    &#39; &#x27; &apos;


=Rights=

Copyright 2020-10-14 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/ for more information].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""
class FixQuotes:
    singlePairs = {
        # 'back':   [ 0x0060, 0x0060 ],  # GRAVE ACCENT
        'splain':   [ 0x0027, 0x0027 ],  # Apostrophe / single quotation mark
        'single':   [ 0x2018, 0x2019 ],  # "SINGLE QUOTATION MARK",
        'sangle':   [ 0x2039, 0x203A ],  # "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
        'slow9':    [ 0x201A, 0x201B ],  # "SINGLE LOW-9 QUOTATION MARK",
        'sprime':   [ 0x2032, 0x2035 ],  # "PRIME", "REVERSED PRIME",
        'scommaO':  [ 0x275B, 0x275C ],  # Heavy Single Turned Comma QM Ornament
    }

    doublePairs = {
        'dplain':   [ 0x0022, 0x0022 ],  # Double quotation mark
        'double':   [ 0x201C, 0x201D ],  # "LEFT DOUBLE QUOTATION MARK",
        'dangle':   [ 0x00AB, 0x00BB ],  # "LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *",
        'dlow9':    [ 0x201E, 0x201F ],  # "DOUBLE LOW-9 QUOTATION MARK",
        'dprime':   [ 0x301E, 0x301E ],  # "DOUBLE PRIME QUOTATION MARK",
        'tprime':   [ 0x2034, 0x2037 ],  # "TRIPLE PRIME", "REVERSED TRIPLE PRIME",

        'rdprime':  [ 0x2057, 0x301D ],  # "REVERSED DOUBLE PRIME QUOTATION MARK",
            # = "QUADRUPLE PRIME"

        'fullwidth':[ 0xFF02, 0xFF02 ],  # Fullwidth Quotation Mark
        'dcommaO':  [ 0x275D, 0x275E ],  # Heavy Double Turned Comma QM Ornament
        'hangleO':  [ 0x276E, 0x276F ],  # Heavy Left-pointing Angle QM Ornament
        'sshdcommonO':  [ 0x1F677, 0x1F678 ],  # Sans-serif Heavy Double Comma QM Ornament
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
        toTag:str=''
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

        sp = self.singlePairs.copy()
        dp = self.doublePairs.copy()
        if (args.ignoreQuote):
            for q0 in args.ignoreQuote:
                if (q0 in sp): del sp[q0]
                elif (q0 in dp): del dp[q0]
                else: raise ValueError(
                    "Unknown quote type to ignore: '%s'." % (q0))
        if (args.backQuotes):
            sp['back'] = [ 0x0060, 0x0060 ]

        self.xtab = self.makeXtab(sp, dp,
            self.leftSingle, self.rightSingle,
            self.leftDouble, self.rightDouble)

        self.quoteExpr = self.makeQuoteExpr()

    def makeXtab(self, sp, dp,
        leftSingle, rightSingle, leftDouble, rightDouble):
        src = tgt = ""
        for l, r in sp.values():
            src += chr(l) + chr(r)
            tgt += leftSingle + rightSingle
        for l, r in dp.values():
            src += chr(l) + chr(r)
            tgt += leftDouble + rightDouble
        warn(2, "Making xtab:\n    |%2d| #%s#\n    |%2d| #%s#" %
            (len(src), src, len(tgt), tgt))
        return str.maketrans(src, tgt)

    @staticmethod
    def makeQuoteExpr():
        """Create regex to match entire quotes.
        Does not yet handle nested cases!
        """
        expr = ""
        for l, r in FixQuotes.singlePairs.values():
            expr += chr(l) + r'.*?' + chr(r) + '|'
        for l, r in FixQuotes.doublePairs.values():
            expr += chr(l) + r'.*?' + chr(r) + '|'
        expr = expr[0:-1]
        warn(2, "Making regex:\n    #%s#" % (expr))
        return re.compile(expr)

    def fix(self, s:str):
        if (self.toTag):
            return self.fixToTag(s, self.quoteExpr, self.toTag)
        else:
            return s.translate(self.xtab)

    @staticmethod
    def fixToTag(s, theRegex, tagName):
        """Does not yet handle nested cases!
        """
        tgt = "<%s>\\1</%s>" % (tagName, tagName)
        return re.sub(theRegex, tgt, s)

    @staticmethod
    def normalizeSpace(s, compress=False):
        """\\s doesn't include hard space.
        """
        if (compress):
            return re.sub(r'[\s\xA0]+', ' ', s, flags=re.UNICODE)
        return re.sub(r'[\s\xA0]', ' ', s, flags=re.UNICODE)


###############################################################################
#
dirCount = 0
fileCount = 0

def warn(lvl, msg):
    if (args.verbose >= lvl): sys.stderr.write(msg + "\n")
    if (lvl < 0): sys.exit()

def doOneFile(path, fixer):
    """Read and deal with one individual file.
    """
    if (not path):
        if (sys.stdin.isatty()): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            warn(0, "Cannot open '%s':\n    %s" % (e))
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
    from DomExtensions import DomExtensions
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
            help='Also map backquote U+0060 to apostrophe.')
        parser.add_argument(
            "--leftSingle", type=str, metavar='E', default="'")
        parser.add_argument(
            "--rightSingle", type=str, metavar='E', default="'")
        parser.add_argument(
            "--leftDouble", type=str, metavar='E', default="\"")
        parser.add_argument(
            "--rightDouble", type=str, metavar='E', default="\"")

        qNames = list(FixQuotes.singlePairs.keys())
        qNames.extend(FixQuotes.doublePairs.keys())
        parser.add_argument(
            "--ignoreQuote", type=str, action='append', choices=qNames,
            help='Drop the named quote type from the list to recognize.')

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

        PowerWalk.addOptionsToArgparse(parser)

        parser.add_argument(
            'files', type=str, nargs=argparse.REMAINDER,
            help='Path(s) to input file(s)')

        args0 = parser.parse_args()
        return(args0)

    def runTest(fixer):
        sample = ("""<q class="foo">The 'quick' "brown" ‘fox’ “jumped” """ +
            """`over` the dog's cat's.</q>""")
        print(sample)
        result = fixer.fix(sample)
        print(result)


    ###########################################################################
    #
    fileCount = 0
    args = processOptions()

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

    if (args.oencoding):
        sys.stdout.reconfigure(encoding='utf-8')

    pw = PowerWalk(args.files, open=True, close=True,
        encoding=args.iencoding, recursive=args.recursive)
    pw.setOptionsFromArgparse(args)

    if (args.test):
        runTest(fixerObj)
    elif (len(args.files) == 0):
        #if (sys.stdin.isatty): warn(0, "fixQuotes: No files specified....")
        doOneFile(None, fixerObj)
    else:
        for path0, fh0, what0 in pw.traverse():
            if (what0 != PWType.LEAF): continue
            fileCount += 1
            ext = os.path.splitext(path0)
            if (ext in [ ".htm", ".html", ".xml", ".svg" ]):
                doOneXmlFile(path0, fixerObj)
            else:
                doOneFile(path0, fixerObj)
