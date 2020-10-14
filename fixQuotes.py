#!/usr/bin/env python
#
# fixQuotes.py: Mess with various quotation marks and such.
# 2020-10-14: Written by Steven J. DeRose.
#
from __future__ import print_function
import sys, os
import codecs
import re
#import string

from PowerWalk import PowerWalk, PWType

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY3:
    #from html.parser import HTMLParser
    #from html.entities import codepoint2name, name2codepoint
    #string_types = str
    #from io import StringIO
    def unichr(n): return chr(n)
    def unicode(s, encoding='utf-8', errors='strict'): str(s, encoding, errors)

__metadata__ = {
    'title'        : "fixQuotes.py",
    'rightsHolder' : "Steven J. DeRose",
    'creator'      : "http://viaf.org/viaf/50334488",
    'type'         : "http://purl.org/dc/dcmitype/Software",
    'language'     : "Python 3.7",
    'created'      : "2020-10-14",
    'modified'     : "2020-10-14",
    'publisher'    : "http://github.com/sderose",
    'license'      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']


descr = """
=Description=

Convert quotations between various forms.

If an input file's extension is htm, html, xml, or svg, then the file
is parsed and only the text nodes are affected (that is, quotes in markup
are not touched).


=Related Commands=


=Known bugs and Limitations=

Does not protect quotes inside markup, such as around attributes.

Does not yet handle nested cases for translation to markup.

Cannot yet translate <q> to literal quotes (etc.).

Does not do anything for characters represented
via backslash codes, named or numeric entities, etc.

=History=

* 2020-10-14: Written by Steven J. DeRose.


=To do=

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

dirCount = 0
fileCount = 0

singlePairs = {
    'splain':   [ "'",    "'" ],     # Apostrophe / single quotation mark
    'single':   [ 0x2018, 0x2019 ],  # "LEFT SINGLE QUOTATION MARK",
    'sangle':   [ 0x2039, 0x203A ],  # "SINGLE LEFT-POINTING ANGLE QUOTATION MARK",
    'slow9':    [ 0x201A, 0x201B ],  # "SINGLE LOW-9 QUOTATION MARK",
    'sprime':   [ 0x2032, 0x2035 ],  # "PRIME", "REVERSED PRIME",
    'scommaO':  [ 0x275B, 0x275C ],  # Heavy Single Turned Comma QM Ornament
}

doublePairs = {
    'dplain':   [ '"',    '"' ],     # Double quotation mark
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

def makeXtab(leftSingle, rightSingle, leftDouble, rightDouble):
    src = tgt = u''
    for l, r in singlePairs.values():
        src += l + r
        tgt += leftSingle + rightSingle
    for l, r in doublePairs.values():
        src += l + r
        tgt += leftDouble + rightDouble
    return str.maketrans(src, tgt)

def makeQuoteExpr():
    """Create regex to match entire quotes.
    Does not yet handle nested cases!
    """
    lefts = rights = u''
    for l, r in singlePairs.values():
        lefts += l
        rights += r
    for l, r in doublePairs.values():
        lefts += l
        rights += r
    expr = r'([%s])(.*?)([%s])' % (l, r)
    return re.compile(expr)

def toTag(s, theRegex, tagName):
    """Does not yet handle nested cases!
    """
    tgt = "<%s>\\1</%s>" % (tagName, tagName)
    return re.sub(theRegex, tgt, s)


###############################################################################
#
def warn(lvl, msg):
    if (args.verbose >= lvl): sys.stderr.write(msg + "\n")
    if (lvl < 0): sys.exit()

def doOneFile(path, xtab):
    """Read and deal with one individual file.
    """
    if (not path):
        if (sys.stdin.isatty()): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            sys.stderr.write("Cannot open '%s':\n    %s" %
                (e), stat="readError")
            return 0

    recnum = 0
    for rec in fh.readlines():
        recnum += 1
        print(rec.translate(xtab))
    return(recnum)

def doOneXmlFile(path, xtab):
    """Parse and load
    """
    from xml.dom import minidom
    from DomExtensions import DomExtensions
    DomExtensions.patchDom(minidom)
    xdoc = minidom.parse(path)
    docEl = xdoc.documentElement
    tns = docEl.getTextNodesIn(docEl)
    for tn in tns:
        tn.data = tn.data.translate(xtab)
    print(docEl.collectAllXml2())
    return(0)


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse
    def anyInt(x):
        return int(x, 0)

    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--leftSingle",       type=str, metavar='E', default="'")
        parser.add_argument(
            "--rightSingle",      type=str, metavar='E', default="'")
        parser.add_argument(
            "--leftDouble",       type=str, metavar='E', default="\"")
        parser.add_argument(
            "--rightDouble",      type=str, metavar='E', default="\"")

        parser.add_argument(
            "--iencoding",        type=str, metavar='E', default="utf-8",
            help='Assume this character set for input files. Default: utf-8.')
        parser.add_argument(
            "--oencoding",        type=str, metavar='E',
            help='Use this character set for output files.')
        parser.add_argument(
            "--quiet", "-q",      action='store_true',
            help='Suppress most messages.')
        parser.add_argument(
            "--recursive",        action='store_true',
            help='Descend into subdirectories.')
        parser.add_argument(
            "--toTag",            type=str, metavar='T', default='',
            help='Convert quotations to XML elements of this name (such as "q").')
        parser.add_argument(
            "--unicode",          action='store_const',  dest='iencoding',
            const='utf8', help='Assume utf-8 for input files.')
        parser.add_argument(
            "--verbose", "-v",    action='count',       default=0,
            help='Add more messages (repeatable).')
        parser.add_argument(
            "--version", action='version', version=__version__,
            help='Display version information, then exit.')

        parser.add_argument(
            'files',             type=str,
            nargs=argparse.REMAINDER,
            help='Path(s) to input file(s)')

        args0 = parser.parse_args()
        if (args0.color == None):
            args0.color = ("USE_COLOR" in os.environ and sys.stderr.isatty())
        #lg.setColors(args0.color)
        #if (args0.verbose): lg.setVerbose(args0.verbose)
        return(args0)

    ###########################################################################
    #
    fileCount = 0
    args = processOptions()

    xtab0 = makeXtab(
        args.leftSingle, args.rightSingle, args.leftDouble, args.rightDouble)

    if (len(args.files) == 0):
        warn(0, "No files specified....")
        doOneFile(None, xtab0)
    else:
        pw = PowerWalk(".", open=True, close=True,
            encoding=args.iencoding, recursive=args.recursive)
        for path0, fh0, what0 in pw.traverse():
            if (what0 != PWType.LEAF): continue
            fileCount += 1
            ext = os.path.splitext(path0)
            if (ext in [ ".htm", ".html", ".xml", ".svg" ]):
                doOneXmlFile(path0, xtab0)
            else:
                doOneFile(path0, xtab0)

    if (not args.quiet):
        warn(0, "Done, %d files.\n" % (fileCount))
