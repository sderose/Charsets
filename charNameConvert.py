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
from collections import defaultdict
from typing import Dict, List  # , Union, IO,

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

Provide an interface to information about special character
names as defined by many organizations. These
are based on (imho, superb) data assembled by my old friend Sebastian Rahtz,
David Carlisle, and others [https://www.w3.org/Math/characters/unicode.xml].

You can get a chart of equivalents, or do conversions from/to the various
representations, as well as literal Unicode characters. In the case of HTML or XML, 
decimal and hexadecimal character references are also available, either as
the preferred representation, or as the fallback when no named entity is available.

==Usage from code==

The API (currently) only handles conversion of code points and bare names.
It doesn't know anything about HTML "&", TEX "\\", etc. So if you want to recognize
or transform references in a particular document/file syntax, you'll need to do
that on top. One possible example, to go from TEX to HTML special characters,
such as \\phi to &phgr;:

    from charNameConvert import charNameConvert
    cnc = charNameConvert(os.environ["HOME"]+"/myStuff/unicode.xml")
    cmap:Dict = cnc.getMap("latex", "html4")

    def fixChar(m):
        if "\\"+m.group(1) in cmap: return "&" + cmap[m.group(1) + ";"]
        return m

    for rec in sys.stdin.readlines():
        rec = re.sub(r"\\\\(\\w+)(?![\\[\\{])", fixChar, rec)
        print rec

Note that latex, varlatex, IEEE, AMS, and Springer
include backslashes (and sometimes more),
such as achieving Unicode MATHEMATICAL BOLD via \\mathbf{X}.
Entities, however, are stored with no "&" or ";" (but those are adding
during conversion).

==Usage on the command line==

    charNameConvert.py --frCode [name1] --toCode [name2] [options] [files]

This will convert stdin by replacing any character references in the input,
which are encoded by the syntax rules of system [name1],
to their equivalent in the --to standard. For example:

    charNameConvert.py --frCode LaTeX --to html

would change \\phi to &phgr;, among many others.

You can omit --frCode, in which case literal characters outside the normal
ASCII range will be affected. The input character set defaults to utf-8,
but can be changed with --iencoding.

Similarly, if you omit --toCode, characters whose encoding is recognized in the
input, will be written out as literals in the output.

I expect to add options to handle numeric character references as well.

The input and output formats supported are (for U+2022 BULLET as example):

* latex    -- \\textbullet
* xml      -- &bull;
* xml10    -- &#8226;
* xml16    -- &#x2022;
* literal  -- [an encoded character per se]
* slashu   == \\uFFFF as used in various languages

The "xml" cases are slightly special, because the source data only includes
the name, not the "&" and ";". So these are recognized and generated
specially. Also,
you can specify --fallback for what to do if a character is recognized, but
does not exist in the requested output format. It can be one of:

* "unchanged"
* "literal"
* "xml10"
* "xml16" (this is the default)
* "slashu"
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
    * mmlalias (this seems to have many duplicates)
    * description (this is generally the full unicode name)

Particular font position is also available, via two properties:
    * fontname
    * fontpos="1"

Finally, you can specify these forms:
    * slashu -- the hex Unicode code point, like \\uFFFF
    * url -- this is not yet supported, but will %-escape the UTF-8 bytes.
    
For output, \\U000FFFFF is used for Unicode code points too large for \\uFFFF.
If you set --short, \\xFF will be used when possible.

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

There is an enormous collection of TeX character sets at 
[https://ctan.org/pkg/comprehensive].


=Known bugs and Limitations=

The --entitySets feature, for giving a prioritized list of which sets to try for
translating (in or out), is unfinished, as is an equivalent feature for multiple
latex libraries.

Several entity sets define multiple names for a single character, such as
'entity.9573-13-isoamsr' defining 'smile' and 'ssmile' both to U+2323 (at least
according to the source data I have). Only the first is kept. This should be no
serious problem for output, but the others won't be recognized on input.

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

I haven't done anything special for  surrogate, mmlextra, Elsevier, or bmp.

I've found one apparent error: U027FA has a 'font' entry for name 'hlcry'
that specifies position '40)'. It is discarded.


=To do=

Implement priority of latex, varlatex, mathlaex, mathvariant. Similar to 
how XML entity sets work.

Add a feature to take any XML entity set(s), and write out TeX definitions to
make them available with the same names.... E.g.:
    \\def{\\bgr}{^^^^03b2}  % GREEK SMALL LETTER BETA

Bonus points: Make &bgr; work directly in TeX....


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
# Standard formats we know about. 
# Probably just add the entity-sets to these, and ditch the enum.
#
class CharStd(IntEnum):  # TODO: Drop
    slashu          = 0  # Special
    afii            = 1
    latex           = 2
    mathlatex       = 3  # ?
    varlatex        = 4  # ?
    ACS             = 5
    AIP             = 6
    APS             = 7
    IEEE            = 8
    Springer        = 9
    Wolfram         = 10
    html4           = 11 # Special
    isopub          = 12 # Special
    mmlalias        = 13 # Special -- duplicates
    surrogate       = 14
    Elsevier        = 15
    bmp             = 16
    prop            = 17
    font            = 18  # Special (tuple)
    description     = 19
    
# The names for different charset standards or expressions. These are
# mostly element type names in the source, with the corresponding name
# or string as their text content. However:
#     "entity" is repeatable and has a set-name and ent name; 
#     "slashu" is custom, to hold the \\u or similar value
#     "description" is just that.
#     "font", not yet supported, has to be a tuple. 
#
# First item:  says whether to show by default in tostring(), --chart,...
INCL = True
EXCL = False
# Second item: TODO What were these?
F = P = 1
# Third item: What kind of value?
# TODO: What to do with cases that are not in Unicode?
OTHER = 0
NAME  = 1    # For ones that are just a name, like entity.xxx
LATEX = 2    # For ones that take a LaTeX string as value
FONT  = 3    # A font name plus position in that font


propNames = {
    #               (EXCL,  ?,   type, freq),
    "ACS":          (EXCL,  F,    str, "61", ),
    "AIP":          (EXCL,  F,    str, "394", ),
    "AMS":          (EXCL,  F,    str, "526", ),
    "APS":          (EXCL,  F,    str, "463", ),
    "Elsevier":     (EXCL,  F,    str, "745", ),
    "IEEE":         (EXCL,  F,    str, "223", ),
    "Springer":     (EXCL,  F,    str, "30", ),
    "Wolfram":      (EXCL,  F,    str, "695", ),
    "afii":         (EXCL,  F,    str, "1170", ),
    "bmp":          (EXCL,  F,    str, "24", ),
    #"character":    (EXCL,  F,   str, "5646", ),
    "charlist":     (EXCL,  P,    str, "1", ),      # ?
    "comment":      (EXCL,  P,    str, "210", ),
    "desc":         (EXCL,  P,    str, "3974", ),   # ?
    "description":  (INCL,  P,    str, "5646", ),
    "elsrender":    (EXCL,  F,    str, "50", ),
    "entity":       (EXCL,  F,   NAME, "3975", ),   # SPECIAL
    "entitygroups": (EXCL,  P,    str, "1", ),      # ?
    "font":         (EXCL,  P,   FONT, "560", ),
    "group":        (EXCL,  P,  OTHER, "5", ),
    "latex":        (INCL,  F,  LATEX, "2480", ),
    "literal":      (EXCL,  F,    str, ),           # SPECIAL
    "mathlatex":    (INCL,  F,  LATEX, "198", ),
    "mathvariant":  (INCL,  F,  LATEX, "14", ),
    "set":          (EXCL,  F,  OTHER, "56", ),
    "surrogate":    (EXCL,  F,    str, "1016", ),
    "varlatex":     (INCL,  F,  LATEX, "18", ),
    "xref":         (EXCL,  P,  OTHER, "63", ),
    #"@image":       (EXCL,  F,    str, "1442", ),
    #"@mode":        (EXCL,  F,    str, "4321", ),
    #"@type":        (EXCL,  F,    str, "4321", ),
}


###############################################################################
# The entity sets mentioned in the source data. To translate these, specify
# --from or --to "xml" and then give a list of these with --entitySets.
# TODO: Provide way to scan for outright conflicts over the same name?
#
entitySetMap = {
    "8879-isoamsa":		"=",  # freq 56
    "8879-isoamsb":		"=",  # freq 42
    "8879-isoamsc":		"=",  # freq 10
    "8879-isoamsn":		"=",  # freq 59
    "8879-isoamso":		"=",  # freq 18
    "8879-isoamsr":		"=",  # freq 84
    "8879-isobox":		"=",  # freq 40
    "8879-isocyr1":		"=",  # freq 67
    "8879-isocyr2":		"=",  # freq 26
    "8879-isodia":		"=",  # freq 14
    "8879-isogrk1":		"=",  # freq 49
    "8879-isogrk2":		"=",  # freq 20
    "8879-isogrk3":		"=",  # freq 43
    "8879-isogrk4":		"=",  # freq 43
    "8879-isolat1":		"=",  # freq 62
    "8879-isolat2":		"=",  # freq 121
    "8879-isonum":		"=",  # freq 76
    "8879-isopub":		"=",  # freq 84
    "8879-isotech":		"=",  # freq 62
    #
    "9573-13-isoamsa":	"=",  # freq 146
    "9573-13-isoamsb":	"=",  # freq 119
    "9573-13-isoamsc":	"=",  # freq 22
    "9573-13-isoamsn":	"=",  # freq 90
    "9573-13-isoamso":	"=",  # freq 52
    "9573-13-isoamsr":	"=",  # freq 180
    "9573-13-isogrk3":	"=",  # freq 43
    "9573-13-isogrk4":	"=",  # freq 43
    "9573-13-isomfrk":	"=",  # freq 52
    "9573-13-isomopf":	"=",  # freq 26
    "9573-13-isomscr":	"=",  # freq 52
    "9573-13-isotech":	"=",  # freq 161
    #
    "html4-lat1":		"=",  # freq 96
    "html4-special":	"=",  # freq 32
    "html4-symbol":		"=",  # freq 124
    #
    "ISOAMSA":		    "=",  # freq 10
    "ISOAMSC":		    "=",  # freq 1    # Is this right? TODO
    "ISOAMSO":		    "=",  # freq 1    # Is this right? TODO
    "ISOAMSR":		    "=",  # freq 4
    #
    "ISObox":	        "=",  # freq 40
    #
    "ISOCYR1":		    "=",  # freq 67
    "ISOCYR2":		    "=",  # freq 26
    #
    "ISODIA":		    "=",  # freq 9
    #
    "ISOGRK1":		    "=",  # freq 49
    "ISOGRK2":		    "=",  # freq 20
    "ISOGRK3":		    "=",  # freq 2    # Is this right? TODO
    #
    "ISOLAT2":		    "=",  # freq 117  # I guess lat1 is redundant w/ html4?
    #
    "ISOPUB":		    "=",  # freq 66
    #
    "ISOTECH":		    "=",  # freq 1    # Is this right? TODO
    #
    "mmlalias":		    "=",  # freq 548
    "mmlextra":		    "=",  # freq 107
    #
    "predefined":		"=",  # freq 5    # XML predefined set, useful w/ --fallback.
    #
    "STIX":		        "=",  # freq 688
}

# Provide shorthand for set of entity sets. See expandEntitySets(),
# which is called from processOptions().
entitySetGroups = [ 
    "8879", "9573", "html49", "ISOAMS", "ISOCYR", "ISOGRK", "mml"
]

# Similar for LaTeX sets
texGroups = [
    "latex", "varlatex", "mathlatex", "mathvariant"
]

def expandEntitySets(eSets:list):
    newList = []
    for es in eSets:
        if (es in entitySetMap):
            newList.append(es)
        elif (es in entitySetGroups):
            for cand in entitySetMap.keys():
                if cand.startswith(es): newList.append(cand)
        else:
            assert False
    return newList

    
###############################################################################
#
class CharStdInfo:
    """Data on one Unicode character, as expressed in a ton of systems.
    """
    NOT_AVAILABLE = "--"  # Show for missing code in --chart.
    
    def __init__(self, codePoint:int):
        assert codePoint >= 0 and codePoint <= 0x1FFFF
        self.codePoint  = codePoint
        # .names may be a character name (as in XML) or a whole LaTeX command.
        self.names = {}
        self.names["slashu"] = self.getSlash(codePoint, args.short)
        self.names["literal"] = chr(codePoint)
        
    def addStd(self, whichStd:str, value:str):
        try:
            if (whichStd in self.names):
                if (not args.quiet):
                    info0("Duplicate prop %s for U+%05x." % (whichStd, self.codePoint))
                return False
            self.names[whichStd] = value
        except IndexError as e:
            print("Can't set prop '%s' for code point %05x.\n    %s" %
                (whichStd, self.codePoint, e))
            return False
        return True

    def tostring(self, include:Dict=None, compact:bool=True) -> str:
        if (compact): buf = "n=\"0x%05x" % self.codePoint
        else: buf = "U+%05x: \n" % self.codePoint
        
        for stdName in include.keys():
            if (stdName == "html4"):
                curName = self.getXML()
            elif (stdName in self.names):
                curName = self.names[stdName]
            else:
                curName = CharStdInfo.NOT_AVAILABLE
            if (compact):
                buf += " %s=\"%s\"" % (stdName, curName)
            else:
                buf += "    %-12s: %s\n" % (stdName, curName)
        return buf

    def getXML(self):
        """Find, assemble, and return an XML entity reference to the given 
        character. This depends on which entity set(s) are chosen.
        If no named entity is found among the chosen sets, a fallback is
        generated, to a numeric character reference, a backslash code,
        or the literal character.
        """
        codePoint = self.codePoint
        x = self.names["html4"]
        #print("getXML for cp %05x, html name is: %s" % (codePoint, x if x else "[none]"))
        if (x is not None): return "&%s;" % (x)
        if (args.fallback == "unchanged"): return "unchanged"
        if (args.fallback == "xml10"):   return "&#%04d;" % (codePoint)
        if (args.fallback == "xml16"):   return "&#%04x;" % (codePoint)
        if (args.fallback == "literal"): return chr(codePoint)  # not checking gt lt etc.
        if (args.fallback == "slashu"):  return self.getSlash(codePoint, args.short)
        assert False, "Bad --fallback value '%s'." % (args.fallback)

    def findEntity(self, eSets:list) -> str:
        """Search the sequence of selected entity sets for the first one that
        has the given character, and return it the entity name.
        """
        for eSet in eSets:
            if ("entity."+eSet in self.names): return self.names["entity."+eSet]
        return None

    def findAllEntities(self, eSets:list) -> List:
        """Search the sequence of selected entity sets and return a list of 
        pairs, each of (entitySetName, entityName).
        """
        found = []
        for eSet in eSets:
            if ("entity."+eSet in self.names):
                found.append( (eSet, self.names["entity."+eSet]) )
        return found

    @staticmethod
    def getSlash(codePoint:int, short:bool=False):
        if (short and codePoint <= 0xFF): return "\\x%02x" % (codePoint)
        if (codePoint <= 0xFFFF): return "\\u%04x" % (codePoint)
        else: return "\\U%08x" % (codePoint)


###############################################################################
#
class charNameConvert():
    """Gather information from Sebastian Rahtz et al's great DB,
    mapping character expressions across various representations.
    TODO: Finish the entity and font mappings.
    """
    def __init__(self, path:str=None):
        super(charNameConvert, self).__init__()
        self.sourceUrl = "https://www.w3.org/Math/characters/unicode.xml"
        self.charDict = {}  # codepoint: CharStdInfo
        self.nCombinations = 0
        self.displayProps = []

        if (path is None):
            self.path = os.path.join(os.environ["HOME"], ".strfchr", "unicode.xml")
        else:
            self.path = path

        self.setDisplayProps()
        self.loadData()

    def setDisplayProps(self, dp:List=None) -> None:
        """Make a list of all the properties to include (TODO: Option for this?)
        TODO: Add the entity.xxx ones?
        """
        if (dp):
            self.displayProps = dp
        else:
            self.displayProps = []
            for k, v in propNames.items():
                if (v[0]): self.displayProps.append(k)
                    
    def downloadData(self) -> None:
        if (not os.path.exists(self.path)):
            check_output([ "curl", self.sourceUrl, ">>", self.path ])
        if (not os.path.exists(self.path)):
            lg.fatal("Could not download data from '%s'.", self.sourceUrl)

    def loadData(self, incl:Dict=None) -> None:
        self.downloadData()

        #DomExtensions.DomExtensions.patchDom()
        xdom = xml.dom.minidom.parse(self.path)
        #print(xdom.toprettyxml())

        charList = xdom.documentElement
        assert charList.nodeName == "charlist"
        info1("charList child count: %d" % (len(charList.childNodes)))

        nChars = 0
        self.charDict = {}
        for charEl in charList.childNodes:
            if (charEl.nodeName != "character"): continue
            idVal = charEl.getAttribute("id")
            dec = charEl.getAttribute("dec")
            info1("loading char %5s (d%06s)" % (idVal, dec))
            if ("-" in idVal):
                if not args.quiet:
                    descNode = self.getChild(charEl, "description")
                    desc = self.getText(descNode) if descNode else "???"
                    info1("Combination character ignored, id '%s' (%s)." % (idVal, desc))
                self.nCombinations += 1
                continue
            try:
                assert re.match(r"U[0-9a-f]{5,5}$", idVal, re.I)
                assert dec.isdecimal()
                dec = int(dec, 10)
                assert int(idVal[1:], 16) == dec
            except ValueError as e:
                lg.warning("ValueError (idVal '%s', dec '%s') in:\n%s\n%s",
                    idVal, dec, charEl.toprettyxml() if args.verbose else "", e)
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
                if (prop == "entity"):
                    # Move the entity-set name to our property name
                    # (not real happy with this approach...)
                    eSet = propEl.getAttribute("set")
                    if (eSet == "mmlalias"): continue  # Avoid duplicates for now: TODO
                    prop = "entity." + eSet
                    val = propEl.getAttribute("id")
                    rc = ci.addStd(prop, val)
                elif (prop == "font"):
                    nam = propEl.getAttribute("name")
                    pos = propEl.getAttribute("pos")
                    try:
                        assert int(pos) >= 0 and int(pos) < 0x1FFFF
                    except (AssertionError, ValueError):
                        # One known error in data, 'hlcry' -> pos '40)'.
                        lg.warning("font: @pos '%s' bad for name '%s':\n%s",
                            pos, nam, self.maybeXml(charEl))
                        continue
                    val = nam + " " + pos
                    rc = ci.addStd("font", val)
                elif (prop == "description"):
                    rc = ci.addStd("description", val)
                elif (prop in propNames): 
                    rc = ci.addStd(prop, val)
                else:
                    if (not args.quiet):
                        lg.warning("Unexpected property spec '%s'.", prop)
                    continue
                if (not rc):
                    lg.warning("******* Problem adding prop '%s', val '%s' in:\n%s",
                        prop, val, self.maybeXml(charEl))
            if (args.verbose > 1 and incl and len(incl) > 0):
                lg.info(ci.tostring(include=incl))
        lg.info("Char defs loaded: %d (%d non-Unicode combinations ignored).",
            nChars, self.nCombinations)
        assert len(self.charDict) == nChars

    def getMap(self, fr, to) -> Dict:
        """Create a dict mapping all the fr->to pairs known.
        TODO: Need to handle the multiple-entity-sets and multiple LaTeX sets cases!
        """
        newMap = {}
        targetMissing = 0
        for codePoint, charStdInfo in self.charDict.items():
            try:
                if (fr not in charStdInfo.names):
                    continue
                if (to not in charStdInfo.names):
                    targetMissing += 1
                else:
                    newMap[charStdInfo.names[fr]] = charStdInfo.names[to]
            except KeyError as e:
                fatal("getMap failed to get from '%s' to '%s' for %04x:\n    %s" %
                    (fr, to, codePoint, e))
            if (targetMissing):
                lg.warning("%d characters in '%s' not mappable to '%s'.", 
                    targetMissing, fr, to)
        return newMap

    @staticmethod
    def getText(node:Node) -> str:
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

    @staticmethod
    def maybeXml(node:Node):
        #if (not args.verbose): return ""
        return re.sub(r"\n\s*\n+", "\n", node.toprettyxml(), flags=re.M)
        

###############################################################################
#
def doChart(frCode:str, toCode:str, incl:List=None) -> None:
    print("Starting chart, '%s' to '%s'." % (frCode, toCode))
    cnc = charNameConvert(os.environ["sjdUtilsDir"]+"/Public/CharSets/unicode.xml")
    print("%d chars loaded." % (len(cnc.charDict)))
    cnmap:Dict = cnc.getMap(frCode, toCode)

    # Collect all the LaTeX special-char strings
    mappableCodes = {}
    for codePoint, info in cnmap.items():
        frCode = info.names[frCode]
        if (frCode is None or frCode == CharStdInfo.NOT_AVAILABLE): continue
        toCode = info.names[toCode]
        mappableCodes[info.names[frCode]] = (codePoint, toCode)
    print("Mappable special characters found: %d.", len(mappableCodes))

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

    for mappableCode in sorted(mappableCodes.keys()):
        codePoint, mappedCode = mappableCodes[mappableCode]
        print(cnc.charDict[codePoint].tostring())
        #print("    %s & ^^^^%04x & \\&%s; //" % (mappableCode, codePoint, mappedCode))

    print("""
    -30-
""")

cmap = None
notFound = defaultdict(int)

def doOneFile(path:str) -> int:
    """Read and deal with one individual file.
    """
    global cmap, notFound
    notFound = defaultdict(int)

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
    cmap = cnc.getMap(args.fromCode, args.toCode)
    
    for rec in fh.readlines():
        rec = re.sub(r"(\\\w+)(?!\w)", fixChar, rec)
        print(rec)
        
    if (len(notFound) > 0):
        lg.warning("Some characters not mapped in '%s'.", path)
        # TODO: Option to print the list

def fixChar(m) -> str:
    if m.group(1) in cmap:
        return cmap[m.group(1)]
    notFound[m.group(1)] += 1
    return m.group(1)


###############################################################################
# Main
#
if __name__ == "__main__":
    import argparse

    esChoices = list(entitySetMap.keys()).extend(entitySetGroups)
    
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
            help="Output a chart in TEX, of the --frCode/--toCode equivalents.")
        parser.add_argument(
            "--compact", action="store_true",
            help="With --chart, use a one-line per codepoint format.")
        parser.add_argument(
            "--entitySets", "-e", type=str, action="append", choices=esChoices,
            help="Which entity sets to check, in order (repeatable).")
        parser.add_argument(
            "--fallback", type=str, default="xml16",
            choices=[ "literal", "xml10", "xml16", "unchanged", "slashu" ],
            help="With --toCode xml, if no xml named entity if available, use this form.")
        parser.add_argument(
            "--frCode", type=str, default="literal",
            choices=[ "literal", "xml", "xml10", "xml16", "latex", "slashu" ],
            help="Input in this format.")
        parser.add_argument(
            "--includeCode", action="append", type=str, choices=esChoices,
            help="With --chart, include these encodings. Repeatable (ordered).")
        parser.add_argument(
            "--oencoding", type=str, metavar="E", default="utf-8",
            help="Use this character coding for output. Default: iencoding.")
        parser.add_argument(
            "--quiet", "-q", action="store_true",
            help="Suppress most messages.")
        parser.add_argument(
            "--short", action="store_true",
            help="With --toCode slashu, use \\xFF form when possible.")
        parser.add_argument(
            "--toCode", type=str, default="literal",
            choices=[ "literal", "xml", "xml10", "xml16", "latex", "slashu" ],
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

        # Support shorthand for groups, like all 8879, etc.
        if (args0.entitySets):
            args0.entitySets = expandEntitySets(args0.entitySets)
        
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
        doChart(args.frCode, args.toCode, args.includeCode)
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
