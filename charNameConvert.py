#!/usr/bin/env python3
#
# charNameConvert.py
# 2022-06-15: Written by Steven J. DeRose.
#
import sys
import os
import codecs
import re
from enum import IntEnum
from subprocess import check_output
import xml.dom.minidom
from xml.dom.minidom import Node

#import string
#from collections import defaultdict, namedtuple
from typing import Dict  # , Union, List, IO,

from PowerWalk import PowerWalk, PWType

import logging
lg = logging.getLogger("charNameConvert.py")
def info0(msg:str) -> None:
    if (args.verbose >= 0): lg.info(msg)
def info1(msg:str) -> None:
    if (args.verbose >= 1): lg.info(msg)
def info2(msg:str) -> None:
    if (args.verbose >= 2): lg.info(msg)
def fatal(msg:str) -> None:
    lg.critical(msg); sys.exit()

__metadata__ = {
    "title"        : "charNameConvert.py",
    "description"  : "Interface Rahtz's huge table of tex/xml/afii/etc char names.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.7",
    "created"      : "2022-06-15",
    "modified"     : "2022-06-15",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__["modified"]

descr = """
=Name=
    """ +__metadata__["title"] + ": " + __metadata__["description"] + """


=Description=

Provide a Python interface to a set of "extended" information about special character
names provided by many organizations. These
are based on (imho, superb) work by my old friend Sebastian Rahtz,
David Carlisle, and others [https://www.w3.org/Math/characters/unicode.xml].

==Usage from code==

The API (currently) only handles conversion of code points and bare names.
It doesn't know anything about HTML "&", TEX "\\", etc. So if you want to recognize
or transform references in a particular document/file syntax, you'll need to do
that on top. One possible example, to go from TEX to HTML special characters,
such as \\phi to &phgr;:

    from charNameConvert import charNameConvert
    cnc = charNameConvert(os.environ["HOME"]+"/myStuff/unicode.xml")
    cmap:Dict = cnc.getMap(CharStd.latex, CharStd.html)

    def fixChar(m):
        if "\\"+m.group(1) in cmap: return "&" + cmap[m.group(1) + ";"]
        return m

    for rec in sys.stdin.readlines():
        rec = re.sub(r"\\\\(\\w+)(?![\\[\\{])", fixChar, rec)
        print rec

Note that unlike most other data in the source, latex, varlatex, IEEE, AMS, and Springer
include backslashes. In some cases, latex has to also include more complex
markup, such as achieving Unicode MATHEMATICAL BOLD via \\mathbf{X}

==Usage on the command line==

    charNameConvert.py --from [name1] --to [name2] [options] [files]

This will convert stdin by replacing any character references in the input,
which are encoded by the syntax rules of system [name1],
to their equivalent in the --to standard. For example:

    charNameConvert.py --from LaTeX --to html

would change \\phi to &phgr;, among many others.

You can omit --from, in which case literal characters outside the normal
ASCII range will be affected. The input character set defaults to utf-8,
but can be changed with --iencoding.

Similarly, if you omit --to, characters whose encoding is recognized in the
input, will be written out as literals in the output.

I expect to add options to handle numeric character references as well.

The input and output formats supported are (for U+2022 BULLET as example):

* latex    -- \\textbullet
* xml      -- &bull;
* xml10    -- &#8226;
* xml16    -- &#x2022;
* literal  -- [an encoded character per se]

The "xml" cases are slightly special, because the source data only includes
the name, not the "&" and ";". So these are recognized and generated
specially. Also,
you can specify --fallback for what to do if a character is recognized, but
does not exist in the requested output format. It can be one of:

* "unchanged"
* "literal"
* "xml10"
* "xml16" (this is the default)

For example, a character with no html named entity, will be written as &#x___;,
where "___" is the hex character code, if you specify --fallback xml10.


==Names of supported character standards==

The source-names used here are mostly the same as in the source data (sample below).
But note that different SGML or XML
schemas can define their own entity names, which may use the same name in
different ways. Therefore, we use the names of the entity sets (such as "html4-symbol")
rather than just "entity":

    * afii
    * latex
    * mathlatex
    * APS
    * ACS
    * Wolfram
    * html4
    * isopub
    * mmlalias
    * description (this is generally the full unicode name)

Particular font position is also available, via two properties:
    * fontname
    * fontpos="1"

Finally, for the "to" side of a conversion, you can specify these forms:
    * slashu -- the hex Unicode code point, like \uFFFF

=Source format=

After some preliminaries, the data consists of a long series of elements like this:

<character id="U02022" dec="8226" mode="mixed" type="binaryop">
 <afii>EB6E</afii>
 <latex>\textbullet </latex>
 <mathlatex>\bullet</mathlatex>
 <APS>bull</APS>
 <ACS>bbull</ACS>
 <Wolfram>Bullet</Wolfram>
 <entity id="bull" set="html4-symbol">
  <desc>bullet = black small circle</desc>
 </entity>
 <entity id="bull" set="8879-isopub">
  <desc>/bullet B: =round bullet, filled</desc>
 </entity>
 <entity id="bullet" set="mmlalias">
   <desc>alias ISOPUB bull</desc>
 </entity>
 <font name="hlcra" pos="1"/>
 <description>BULLET</description>
</character>

The data sometimes has entries like this, which are presently ignored:
    <surrogate mathvariant="sans-serif-bold-italic" ref="U003D6"/>

=Related commands and data=

The source data on character names is from [https://www.w3.org/Math/characters/unicode.xml].
A copy is also available at [https://github.com/sderose/Charsets.git/blob/master/unicode.xml].


=Known bugs and Limitations=

Some entries are for a combination of characters, as shown below. These generate
a warning during loading (except with -q), and are discarded.

    <character id="U0003C-020D2" dec="60-8402" type="other" mode="unknown">
     <entity id="nvlt" set="9573-13-isoamsn">
      <desc>not, vert, less-than</desc>
     </entity>
     <description unicode="combination">LESS-THAN SIGN with vertical line</description>
    </character>

Some information in the source is not used, such as the "type" and "mode" attributes
of characters.

Various integrity checks are done, such as making sure the hex and decimal code points
match for each character. This is usually done by a bare assertion, so if they ever
come up you'll have to look in the data or code to see what happened.

I haven't done anything special for  surrogate, Elsevier, or bmp.


=To do=

Add support for getting the code point in various bases, for either the "from"
or the "to" side.


=History=

* 2022-06-15: Written by Steven J. DeRose.


=Rights=

Copyright 2022-06-15 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See [http://creativecommons.org/licenses/by-sa/3.0/] for more information.

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""


###############################################################################
#
CHARSTD_MIN = 1
CHARSTD_MAX = 19

class CharStd(IntEnum):
    afii            = 1
    latex           = 2
    mathlatex       = 3
    varlatex        = 4
    ACS             = 5
    AIP             = 6
    APS             = 7
    IEEE            = 8
    Springer        = 9
    Wolfram         = 10
    html4           = 11
    isopub          = 12
    mmlalias        = 13
    surrogate       = 14
    Elsevier        = 15
    bmp             = 16
    prop            = 17
    font            = 18
    description     = 19


###############################################################################
#
class CharStdInfo:
    def __init__(self, codePoint:int):
        assert codePoint >= 0 and codePoint <= 0x1FFFF
        self.codePoint  = codePoint
        self.names = [ None for i in range(CHARSTD_MAX+1) ]

    def addStd(self, whichStd:CharStd, value:str):
        stdNum = int(whichStd)
        try:
            if (self.names[stdNum] is not None):
                print("Duplicate prop %s for %05x." % (whichStd.name, self.codePoint))
                return False
            self.names[stdNum] = value
        except IndexError as e:
            print("Can't set prop '%s' (stdNum %d) for code point %05x.\n    %s" %
                (whichStd.name, stdNum, self.codePoint, e))
            return False
        return True

    def tostring(self, exclude:Dict) -> str:
        buf = "U+%05x: \n" % self.codePoint
        for i in range(CHARSTD_MIN, CHARSTD_MAX+1):
            stdName = CharStd(i).name
            if (exclude and stdName in exclude): continue
            try:
                if (CharStd(i) == CharStd.html4): curName = self.getXML(self.codePoint)
                else: curName = self.names[i]
            except IndexError as e:
                print("std #%d (%s) out of range:\n    %s" % (i, stdName, e))
            if (curName is None): curName = "--"
            buf += "    %-12s: %s\n" % (stdName, curName)
        return buf

    def getXML(self, codePoint:int):
        x = self.names[CharStd.html4]
        print("getXML for cp %05x, html name is: %s" % (codePoint, x if x else "[none]"))
        if (x is not None): return "&%s;" % (x)
        if (args.fallback == "unchanged"): return "unchanged"
        if (args.fallback == "xml10"):   return "&#%04d;" % (codePoint)
        if (args.fallback == "xml16"):   return "&#%04x;" % (codePoint)
        if (args.fallback == "literal"): return chr(codePoint)  # not checking gt lt etc.
        assert False, "Bad --fallback value '%s'." % (args.fallback)


###############################################################################
# See charNameConvert.py for
#
propNames = """{
    "ACS":          ( F, X,    S,  str, "freq:61", ),
    "AIP":          ( F, X,    S,  str, "freq:394", ),
    "AMS":          ( F, X,    S,  str, "freq:526", ),
    "APS":          ( F, X,    S,  str, "freq:463", ),
    "Elsevier":     ( F, X,    S,  str, "freq:745", ),
    "IEEE":         ( F, X,    S,  str, "freq:223", ),
    "Springer":     ( F, X,    S,  str, "freq:30", ),
    "Wolfram":      ( F, X,    S,  str, "freq:695", ),
    "afii":         ( F, X,    S,  str, "freq:1170", ),
    "bmp":          ( F, X,    S,  str, "freq:24", ),
    #"character":    ( F, X,    S,  str, "freq:5646", ),
    "charlist":     ( P, X,    S,  str, "freq:1", ),
    "comment":      ( P, X,    S,  str, "freq:210", ),
    "desc":         ( P, X,    S,  str, "freq:3974", ),
    "description":  ( P, X,    S,  str, "freq:5646", ),
    "elsrender":    ( F, X,    S,  str, "freq:50", ),
    #"entity":       ( F, X,    S,  str, "freq:3975", ),
    "entitygroups": ( P, X,    S,  str, "freq:1", ),
    "font":         ( P, X,    S,  str, "freq:560", ),
    "group":        ( P, X,    S,  str, "freq:5", ),
    "latex":        ( F, X,    S,  str, "freq:2480", ),
    "mathlatex":    ( F, X,    S,  str, "freq:198", ),
    "mathvariant":  ( F, X,    S,  str, "freq:13", ),
    "mathvariants": ( F, X,    S,  str, "freq:1", ),
    "set":          ( F, X,    S,  str, "freq:56", ),
    "surrogate":    ( F, X,    S,  str, "freq:1016", ),
    "varlatex":     ( F, X,    S,  str, "freq:18", ),
    "xref":         ( P, X,    S,  str, "freq:63", ),
    #"@image":       ( F, X,    S,  str, "freq:1442", ),
    #"@mode":        ( F, X,    S,  str, "freq:4321", ),
    #"@type":        ( F, X,    S,  str, "freq:4321", ),
}"""

class charNameConvert(dict):
    """Add in information from Sebastian Rahtz et al's great DB mapping
    chars across various representations.
    TODO: Finish the Sebastian mappings.
    """
    def __init__(self, path:str=None):
        super(charNameConvert, self).__init__()
        self.sourceUrl = "https://www.w3.org/Math/characters/unicode.xml"
        self.charDict = {}
        self.nCombinations = 0

        if (path is None):
            self.path = os.path.join(os.environ["HOME"], ".strfchr", "unicode.xml")
        else:
            self.path = path
        self.loadData()

    def downloadData(self):
        if (not os.path.exists(self.path)):
            check_output([ "curl", self.sourceUrl, ">>", self.path ])
        if (not os.path.exists(self.path)):
            lg.fatal("Could not download data from '%s'.", self.sourceUrl)

    def loadData(self):
        # Pick which ones to show with tostring()
        excl = set([
            #"description", 	"html4", 	"latex",
            "mathlatex", 	"varlatex",
            "ACS", 	        "AIP", 	        "APS", 	    "IEEE", 	"Springer",
            "Wolfram", 	    "isopub", 	    "mmlalias", "surrogate",
            "Elsevier", 	"bmp", 	        "prop", 	"font",     "afii",
        ])

        self.downloadData()

        #DomExtensions.DomExtensions.patchDom()
        xdom = xml.dom.minidom.parse(self.path)
        #print(xdom.toprettyxml())

        charList = xdom.documentElement
        assert charList.nodeName == "charlist"
        print("charList child count: %d" % (len(charList.childNodes)))

        nChars = 0
        self.charDict = {}
        for charEl in charList.childNodes:
            if (charEl.nodeName != "character"): continue
            idVal = charEl.getAttribute("id")
            dec = charEl.getAttribute("dec")
            if (args.verbose): print("loading char %5s (d%06s)" % (idVal, dec))
            if ("-" in idVal):
                if not args.quiet:
                    lg.warning("Combination character, id '%s' (ignored).", idVal)
                self.nCombinations += 1
                continue
            try:
                assert re.match(r"U[0-9a-f]{5,5}$", idVal, re.I)
                assert dec.isdecimal()
                dec = int(dec, 10)
                assert int(idVal[1:],16) == dec
            except ValueError as e:
                print("ValueError (idVal '%s', dec '%s') in:\n%s\n%s" %
                    (idVal, dec, charEl.toprettyxml() if args.verbose else "", e))
                continue

            ci = CharStdInfo(dec)
            self.charDict[dec] = ci
            nChars += 1
            for propEl in charEl.childNodes:
                if (propEl.nodeType == xml.dom.Node.TEXT_NODE
                    and propEl.data.strip() == ""): continue
                assert propEl.nodeType == xml.dom.Node.ELEMENT_NODE
                prop = propEl.nodeName
                val = self.getText(propEl)
                if (prop == "afii"):        rc = ci.addStd(CharStd.afii, val)
                elif (prop == "latex"):     rc = ci.addStd(CharStd.latex, val)
                elif (prop == "mathlatex"): rc = ci.addStd(CharStd.mathlatex, val)
                elif (prop == "varlatex"):  rc = ci.addStd(CharStd.varlatex, val)
                elif (prop == "ACS"):       rc = ci.addStd(CharStd.ACS, val)
                elif (prop == "AIP"):       rc = ci.addStd(CharStd.AIP, val)
                elif (prop == "IEEE"):      rc = ci.addStd(CharStd.IEEE, val)
                elif (prop == "Springer"):  rc = ci.addStd(CharStd.Springer, val)
                elif (prop == "APS"):       rc = ci.addStd(CharStd.APS, val)
                elif (prop == "Wolfram"):   rc = ci.addStd(CharStd.Wolfram, val)
                elif (prop == "surrogate"): continue
                elif (prop == "entity"):
                    prop = propEl.getAttribute("set")
                    if (prop == "html-symbol"): prop = "html"
                    elif (prop == "8879-isopub"): prop = "isopub"
                    val = propEl.getAttribute("id")
                    rc = ci.addStd(CharStd.prop, val)       # TODO cast to CharStd
                elif (prop == "font"):
                    nam = propEl.getAttribute("name")
                    pos = propEl.getAttribute("pos")
                    try:
                        assert int(pos) >= 0 and int(pos) < 0x1FFFF
                    except (AssertionError, ValueError):
                        print("font: @pos '%s' bad for name '%s':\n%s" %
                            (pos, nam, propEl.toprettyxml() if args.verbose else ""))
                    val = nam + " " + pos
                    rc = ci.addStd(CharStd.font, val)
                elif (prop == "description"):
                    rc = ci.addStd(CharStd.description, val)
                else:
                    if (not args.quiet):
                        lg.warning("Unexpected spec '%s'.", prop)
                if (not rc):
                    lg.warning("******* Problem with prop '%s', val '%s' in:\n%s",
                        prop, val, charEl.toprettyxml() if args.verbose else "")
            print(ci.tostring(exclude=excl))
        lg.info("Char defs processed: %d.", nChars)
        assert len(self.charDict) == nChars

    def getMap(self, fr, to) -> Dict:
        # Takes either str names or CharStd enum values.
        if isinstance(fr, str): fr = CharStd(fr)
        newMap = {}
        for _k, v in self.charDict.items():
            newMap[v.names[fr]] = newMap[v.names[to]]
        return newMap

    @staticmethod
    def getText(node:Node):
        if (node.nodeType == Node.TEXT_NODE): return node.data
        buf = ""
        for ch in node.childNodes:
            buf += charNameConvert.getText(ch)
        return buf

    @staticmethod
    def getChild(node:Node, ename:str) -> Node:
        for ch in node.childNodes:
            if (ch.nodeName == ename): return ch
        return None


###############################################################################
#
def doChart():
    print("Starting chart, LaTeX to XML.")
    cnc = charNameConvert(os.environ["sjdUtilsDir"]+"/Public/CharSets/unicode.xml")
    print("%d chars loaded." % (len(cnc.charDict)))
    cnmap:Dict = cnc.getMap(CharStd.latex, CharStd.html4)

    # Collect all the LaTeX special-char strings
    latexCodes = {}
    for codePoint, info in cnmap.items():
        if (info.names[CharStd.latex] is None): continue
        latexCodes[info.names[CharStd.latex]] = (codePoint, info.names[CharStd.html4])
    print("latex special characters found: %d.", len(latexCodes))

    opener = """
\\documentclass{article}
\\usepackage[english]{babel}
\\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage[colorlinks=true, allcolors=blue]{hyperref}

\\title{List of LaTeX special characters}
\\author{charNameConvert.py}
"""
    print(opener)

    for latexCode in sorted(latexCodes.keys()):
        cp, ent = latexCodes[latexCodes]
        print("    %s & ^^^^%04x & \\&%s; //" % (latexCode, cp, ent))

    print("""
    -30-
""")

cmap = None

def doOneFile(path:str) -> int:
    """Read and deal with one individual file.
    """
    global cmap
    if (not path):
        if (sys.stdin.isatty()): print("Waiting on STDIN...")
        fh = sys.stdin
    else:
        try:
            fh = codecs.open(path, "rb", encoding=args.iencoding)
        except IOError as e:
            info0("Cannot open '%s':\n    %s" % (path, e))
            return 0

    cnc = charNameConvert(os.environ["sjdUtilsDir"]+"/Public/CharSets/unicode.xml")
    cmap = cnc.getMap(CharStd.latex, CharStd.html4)

    for rec in fh.readlines():
        rec = re.sub(r"\\\\(\\w+)(?![\\[\\{])", fixChar, rec)
        print(rec)

def fixChar(m):
    if "\\"+m.group(1) in cmap: return "&" + cmap[m.group(1) + ";"]
    return m


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse

    def processOptions() -> argparse.Namespace:
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--iencoding", type=str, metavar="E", default="utf-8",
            help="Assume this character coding for input. Default: utf-8.")
        parser.add_argument(
            "--chart", action="store_true",
            help="Output a chart in TEX, of all the TEX characters.")
        parser.add_argument(
            "--fallback", type=str, default="xml16",
            choices=[ "literal", "xml10", "xml16", "unchanged" ],
            help="With --to xml, if no xml named entity if available, use this form.")
        parser.add_argument(
            "--from", type=str, default="literal",
            choices=[ "literal", "xml", "xml10", "xml16", "latex" ],
            help="Input in this format.")
        parser.add_argument(
            "--oencoding", type=str, metavar="E", default="utf-8",
            help="Use this character coding for output. Default: iencoding.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--to", type=str, default="literal",
            choices=[ "literal", "xml", "xml10", "xml16", "latex" ],
            help="Output in this format.")
        parser.add_argument(
            "--unicode", action="store_const", dest="iencoding",
            const="utf8", help="Assume utf-8 for input files.")
        parser.add_argument(
            "--verbose", "-v", action="count", default=0,
            help="Add more messages (repeatable).")
        parser.add_argument(
            "--version", action="version", version=__version__,
            help="Display version information, then exit.")

        PowerWalk.addOptionsToArgparse(parser)

        parser.add_argument(
            "files", type=str, nargs=argparse.REMAINDER,
            help="Path(s) to input file(s)")

        args0 = parser.parse_args()
        return(args0)


    ###########################################################################
    #
    args = processOptions()
    if (args.iencoding and not args.oencoding):
        args.oencoding = args.iencoding
    if (args.oencoding):
        # https://stackoverflow.com/questions/4374455/
        # sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
        sys.stdout.reconfigure(encoding="utf-8")

    if (args.chart):
        doChart()
        sys.exit()

    if (len(args.files) == 0):
        info0("charNameConvert.py: No files specified....")
        doOneFile(None)
    else:
        pw = PowerWalk(args.files, open=False, close=False,
            encoding=args.iencoding)
        pw.setOptionsFromArgparse(args)
        for path0, fh0, what0 in pw.traverse():
            if (what0 != PWType.LEAF): continue
            doOneFile(path0)
        if (not args.quiet):
            info0("charNameConvert.py: Done, %d files.\n" % (pw.getStat("regular")))
