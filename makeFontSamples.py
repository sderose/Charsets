#!/usr/bin/env python
#
# makeFontSamples.py
#
# 2019-07-03: Written. Copyright by Steven J. DeRose.
# Creative Commons Attribution-Share-alike 3.0 unported license.
# See http://creativecommons.org/licenses/by-sa/3.0/.
#
# To do:
#
from __future__ import print_function
import sys, os
import argparse
import re

__metadata__ = {
    'creator'      : "Steven J. DeRose",
    'cre_date'     : "%DATE%",
    'language'     : "Python 3.7",
    'version_date' : "%DATE%",
}
__version__ = __metadata__['version_date']


###############################################################################
###############################################################################
# Main
#
if __name__ == "__main__":
    def processOptions():
        descr = """
=head1 Description

Collects fonts from the directories where MacOS keeps them, and makes
an HTML file wioth a sample of each.

The list could be shortened by leaving out files that are variants of a single
font-family, or ones that Browsers don't seem to use.

=head1 Related Commands

=head1 Known bugs and Limitations

=head1 Licensing

Copyright %DATE% by Steven J. DeRose. This script is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
See http://creativecommons.org/licenses/by-sa/3.0/ for more information.

=head1 Options
"""

        try:
            from MarkupHelpFormatter import MarkupHelpFormatter
            formatter = MarkupHelpFormatter
        except ImportError:
            formatter = None
        parser = argparse.ArgumentParser(
            description=descr, formatter_class=formatter)

        parser.add_argument(
            "--color",  # Don't default. See below.
            help='Colorize the output.')
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
            "--sample",           type=str, metavar='E',
            default='The quick ND fox jumped over the lazy aardvark.',
            help="Sample text to use.")
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
        return(args0)

    ###########################################################################
    #
    args = processOptions()
    print("Finding fonts...")

    fonts = os.listdir("/System/Library/Fonts") + os.listdir("/Library/Fonts")

    print("""<html>
<head>
<style type="text/css">
    dt   { margin-top: 12pt; }
    dd   { font-size:larger; }
</style>
</head>
<body>
<dl>
""")

    for font in sorted(fonts):
        fam = re.sub(r'\.\w+$', '', font)
        print('<dt>%s</dt><dd style="font-family:%s;">%s</dd>\n' %
            (font, fam, args.sample))

    print("""</dl>
</body>
</html>
""")
