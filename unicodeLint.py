#!/usr/bin/env python
#
# unicodeLInt.py
#
# 2015-11-22: Written. Copyright by Steven J. DeRose.
# Creative Commons Attribution-Share-alike 3.0 unported license.
# See http://creativecommons.org/licenses/by-sa/3.0/.
#
# To do:
#
from __future__ import print_function
import sys, os, argparse
import re
#import string
#import math
#import subprocess
import codecs

#import pudb
#pudb.set_trace()

from sjdUtils import sjdUtils
from MarkupHelpFormatter import MarkupHelpFormatter

global args, su, lg

__version__ = "2015-11-22"
__metadata__ = {
    'creator'      : "Steven J. DeRose",
    'cre_date'     : "2015-11-22",
    'language'     : "Python 2.7.6",
    'version_date' : "2015-11-22",
    'src_date'     : "$LastChangedDate$",
    'src_version'  : "$Revision$",
}

# See http://stackoverflow.com/questions/6162484
#
perlRe = r'\b(tr|m|s)/.*'
perlPatterns = [
    ( perlRe + r'\[\^?a-z\]',                 '\\P{Lowercase_Letter}', ),
    ( perlRe + r'\[\^?A-Z\]',                 '\\P{Uppercase_Letter}', ),
    ( perlRe + r'\[\^?(a-z|A-Z){2}\]',        '\\P{Alphabetic}', ),
    ( perlRe + r'\[\^?0-9\]',                 '\\P{Digit}' ),
    ( perlRe + r'\[\^?(a-z|A-Z|0-9){3}\]',    '\\P{Alphanumeric}', ),
    ( perlRe + r'(\\n|\\r)+',              '\\R', ),
    ( perlRe + r'\[\^?aeiou\]',               '???', ),
    #( perlRe + r'\$/',                     '', ),
    #( perlRe + r'\\s',                     '\\h' or '\\v' ???
    #(  r'\\w',                    '', ),
    #( r'\b(lt|gt|le|ge|eq|ne)\b', 'Unicode::Collate->new(level=>1)->\$1($a, $b)', ),
    # uc(), lc()...
    #( r'\bopen\b',                '??? if no "encoding"', ),
    #( r'\\x0*1?FFFF',              '', ),
    #( r'\b(lc\(uc\($\w+\)\)|uc\(lc\(\$\w+\)\))', '', ),

]
perlPatternsC = []

# Should complicate these to allow reordering of token lists
#
perlUse = r'^ use  '   # '  ' for \\s+
perlSetups = [
    perlUse + r'5.01[24].*;',
    perlUse + r'utf8.*;',
    perlUse + r'strict.*;',
    perlUse + r'autodie.*;',
    perlUse + r'warnings.*;',    # FIX: Collides with next one
    perlUse + r'warnings  qw< FATAL  utf8 >.*;',
    perlUse + r'open  qw< :std  :utf8 >.*;',
    perlUse + r'charnames  qw< :full >.*;',
    perlUse + r'feature  qw< unicode_strings >.*;',
    perlUse + r'File::Basename  qw< basename >.*;',
    perlUse + r'Carp  qw< carp  croak  confess  cluck >.*;',
    perlUse + r'Encode  qw< encode  decode >.*;',
    perlUse + r'Unicode::Normalize  qw< NFD  NFC >.*;',
]
perlSetupsC = []
perlSetupsSeen = []

###############################################################################
#
def processOptions():
    global args, su, lg
    parser = argparse.ArgumentParser(
        description="""

=head1 Description

=head1 Related Commands

=head1 Known bugs and Limitations

=head1 Licensing

Copyright 2015 by Steven J. DeRose. This script is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See http://creativecommons.org/licenses/by-sa/3.0/ for more information.

=head1 Options
        """,
        formatter_class=MarkupHelpFormatter
    )
    parser.add_argument(
        "--iencoding",        type=str, metavar='E', default="utf-8",
        help='Assume this character set for input files. Default: utf-8.')
    parser.add_argument(
        "--no-setup",         action='store_true',
        help='Suppress checks for Unicode-relevant "use..." lines.')
    parser.add_argument(
        "--quiet", "-q",      action='store_true',
        help='Suppress most messages.')
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
    su = sjdUtils()
    lg = su.lg
    su.setVerbose(args0.verbose)
    return(args0)


###############################################################################
#
def tryOneItem(path):
    "Try to open a file (or directory, if -r is set)"
    su.hMsg(1, "Starting item '%s'" % (path))
    recnum = 0
    if (not os.path.exists(path)):
        lg.error("Couldn't find '%s'." % (path), stat="cantOpen")
    elif (args.extension != '' and not path.endswith(args.extension)):
        lg.bumpStat("wrongExtension")
    elif (os.path.isdir(path)):
        lg.bumpStat("totalDirs")
        if (args.recursive):
            for child in os.listdir(path):
                recnum += tryOneItem(os.path.join(path,child))
    else:
        try:
            fh = codecs.open(path, mode="r", encoding=args.iencoding)
        except:
            lg.error("Couldn't open '%s'." % (path), stat="cantOpen")
            return(0)
        lg.bumpStat("totalFiles")
        recnum = readOneFile(path,fh)
        fh.close()
    return(recnum)


###############################################################################
#
def doOneFile(path):
    lg.hMsg(1, "Starting file '%s'" % (path))
    recnum = 0
    rec = ""
    try:
        fh = codecs.open(path, mode='r', encoding=args.iencoding)
    except IOError as e:
        lg.error("Can't open '%s'." % (path), stat="CantOpen")
        return(0)
    lang = "";
    rec = fh.readline()
    if (rec.startswith('#!')):
        if (re.search(r'\bperl', rec)): lang = 'perl'
        if (re.search(r'\bpython', rec)): lang = 'python'

    perlSetupsSeen = [ ]
    for p in perlSetups: perlSetupsSeen.append(0)

    while (True):
        try:
            rec = fh.readline()
        except Exception as e:
            lg.error("Error (%s) reading record %d of '%s'." %
                (type(e), recnum, path), stat="readError")
            break
        if (len(rec) == 0): break # EOF
        recnum += 1
        rec = re.sub(r'^([^"\']*)#.*$', '\\1', rec.strip())
        if (rec.startswith("use ")):
            lg.vMsg(2, "Use: %s" % (rec))
            for i, p in enumerate(perlSetupsC):
                if (re.match(p, rec)):
                    lg.vMsg(2, "Matched by %s" % (perlSetups[i]))
                    perlSetupsSeen[i] += 1
        else:
            for i, p in enumerate(perlPatternsC):
                if (re.search(p, rec)):
                    print("%s:%d: %s" % (path, recnum, rec));
                    lg.vMsg(1, "  was matched by: " + perlPatterns[i][0])
                    break
    fh.close()
    if (not args.no_setup):
        for i, p in enumerate(perlSetups):
            if (perlSetupsSeen[i] == 0): print("%s:Missing: %s" %
                (path, perlSetups[i]))
    return(recnum)



###############################################################################
###############################################################################
# Main
#
args = processOptions()

for p in perlPatterns:
    try:
        lg.vMsg(2, "Compiling pattern: " + p[0])
        perlPatternsC.append(re.compile(p[0]))
    except Exception as e:
        lg.eMsg(-1, "Bad regex: %s\n    %s" % (p[0], e))

for p in perlSetups:
    try:
        expr = re.sub(r'  ', r'\\s+', p)
        expr = re.sub(r' ', r'\\s*', expr)
        lg.vMsg(2, "Compiling setup: " + expr)
        perlSetupsC.append(re.compile(expr))
    except Exception as e:
        lg.eMsg(-1, "Bad regex: %s\n    %s" % (expr, e))


if (len(args.files) == 0):
    lg.error("No files specified....")
    sys.exit()

for f in (args.files):
    lg.bumpStat("totalFiles")
    recs = doOneFile(f)
    lg.bumpStat("totalRecords", amount=recs)

if (not args.quiet):
    su.vMsg(0,"Done.")
    su.showStats()
