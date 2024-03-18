#!/usr/bin/env python3
#
# makeFontSamples.py: Create HTML with sample of various fonts.
# 2019-07-03: Written by Steven J. DeRose.
#
import sys
import os
import argparse
import re

from typing import List
from subprocess import check_output

__metadata__ = {
    "title"        : "makeFontSamples",
    "description"  : "Create HTML with sample of various fonts.",
    "rightsHolder" : "Steven J. DeRose",
    "creator"      : "http://viaf.org/viaf/50334488",
    "type"         : "http://purl.org/dc/dcmitype/Software",
    "language"     : "Python 3.7",
    "created"      : "2019-07-03",
    "modified"     : "2023-05-17",
    "publisher"    : "http://github.com/sderose",
    "license"      : "https://creativecommons.org/licenses/by-sa/3.0/"
}
__version__ = __metadata__['modified']

descr = """
=Description=

Collects fonts and makes an HTML file with a sample of each.

There are options to change sample text, font-size, etc.

==Usage==

    makeFontSamples.py --fontSize 24 --sample "Smyth, H. W., Greek Grammar'"

Pipe the output to a file, and then open in a browser.

Or, use `--list` to just get a list of font names instead of full HTML.

==Looking for fonts in all the wrong places==

By default, uses the (Mac-specific?) `fc-list` command to get a list of
font family names.

However, if you specify `--scan`, it will looks through a list of likely
directories for font files, and use that for the list. It's not very good at
extracting the desired name, though.

MS Office adds its own fonts, apparently in "Contents/Resources/Dfonts"
inside the app bundle(s?). These are also checked if the dir is there.
Add more directies with `--dir` (repeatable).

If font files with the same name are found in multiple directories, only the first
one found is reported.


=Related Commands=

MacOS `Font Book`.

`fc-list` command: gets a list of font family names (Mac-specific?).

Wikipedia has some nice samples at [https://en.wikipedia.org/wiki/List_of_serif_typefaces].


=Known bugs and Limitations=

The resulting HTML doesn't seem to work in Firefox.

This only knows about MacOS conventional paths; though you can use `--dirs` to
add specify others.

This includes fonts even if the browser can't actually see them.


=To Do=

* Identify the type of each font (ttf, ps,...).
* Show full path, not just name.
* Extract and display the actual name, not just the filename
* Suppress alts like demibold, bold, heavy, italic, condensed, light, extra bold
* Options to exclude fonts with non-ASCII names.
* Would be really nice to categorize by:
** serif/sans/script/mono/display/dingbats
** charset supported
** accessibility to browser


=History=

* 2019-07-03: Written by Steven J. DeRose.
* 2020-08-20: New layout?
* 2021-10-14: Factor out list of directories to look in. Add --dir, --fontSize
* 2023-05-17: Make safe vs. missing dirs. Factor out getting font-list, and
introduce 'fc-list'.


=Rights=

Copyright 2019-07-03 by Steven J. DeRose. This work is licensed under a
Creative Commons Attribution-Share-alike 3.0 unported license.
For further information on this license, see
[https://creativecommons.org/licenses/by-sa/3.0].

For the most recent version, see [http://www.derose.net/steve/utilities]
or [https://github.com/sderose].


=Options=
"""

fontExtensions = [
    "ttf", "ttc", "otf", "ps",
]

HOME = os.environ["HOME"]

fontDirs = [
    "/System/Library/Fonts",
    "/Library/Fonts",
    os.path.join(HOME, "Library/Fonts"),
    "/Applications/Microsoft Word.app/Contents/Resources/DFonts",
    os.path.join(HOME, "/Applications/Microsoft Word.app/Contents/Resources/DFonts"),
]

htmlOpen = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>Font Samples</title>
    <style type="text/css">
        body { margin-left: 24pt; }
        dt   { margin-top: 12pt; }
        dd   { font-size:%5.2fpt; }
    </style>
</head>
<body>
"""

htmlClose = """</body>
</html>
"""

def scanFontDirs(dirs:List) -> List:
    fontNames = []
    for d in dirs:
        if (not os.path.isdir(d)):
            sys.stderr.write("No font dir at %s.\n" % (d))
            continue
        for f in os.listdir(d):
            if (f not in fontNames): fontNames[f] = d
    return fontNames

def getFclist() -> List:
    fcl = check_output(["fc-list", ":", "family" ])
    fclu = fcl.decode(encoding="utf-8")
    fontNames = set([ re.sub(",.*", "", x) for x in fclu.split(sep="\n") ])
    return list(fontNames)


###############################################################################
# Main
#
if __name__ == "__main__":
    def processOptions():
        try:
            from BlockFormatter import BlockFormatter
            parser = argparse.ArgumentParser(
                description=descr, formatter_class=BlockFormatter)
        except ImportError:
            parser = argparse.ArgumentParser(description=descr)

        parser.add_argument(
            "--color", # Don't default. See below.
            help='Colorize the output.')
        parser.add_argument(
            "--dirs", type=str, action='append',
            help='Add a directory to the list of places to look for fonts. Repeatable.')
        parser.add_argument(
            "--fontSize", "--font-size", type=int, default=24,
            help='Font size in points, to have the HTML use.')
        parser.add_argument(
            "--iencoding", type=str, metavar='E', default="utf-8",
            help='Assume this character set for input files. Default: utf-8.')
        parser.add_argument(
            "--list", action='store_true',
            help='Just list the available fonts.')
        parser.add_argument(
            "--oencoding", type=str, metavar='E',
            help='Use this character set for output files.')
        parser.add_argument(
            "--quiet", "-q", action='store_true',
            help='Suppress most messages.')
        parser.add_argument(
            "--sample", type=str, metavar='E',
            default='The quick fox jumped over the lazy aardvark.',
            help="Sample text to use.")
        parser.add_argument(
            "--scan", action='store_true',
            help='Do a hard scan for font files, instead of using fc-list.')
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
        if (args0.color is None):
            args0.color = ("CLI_COLOR" in os.environ and sys.stderr.isatty())
        return(args0)

    ###########################################################################
    #
    args = processOptions()
    print("Finding fonts...")

    if (args.dirs): fontDirs.extend(args.dirs)
    if (args.scan):
        fonts = scanFontDirs(fontDirs)
    else:
        fonts = getFclist()

    fonts.sort()

    if (args.list):
        print("\n".join(fonts))
        sys.exit()

    print(htmlOpen % (args.fontSize))
    print("<dl>")
    nFonts = 0
    for font in sorted(fonts):
        fam = re.sub(r'\.\w+$', '', font)
        print('<dt>%s</dt><dd style="font-family:%s;">%s</dd>' %
            (font, fam, args.sample))
        nFonts += 1
    print("</dl>")
    print(htmlClose)

    if (not args.quiet): sys.stderr.write("Done, found %d fonts.\n" % (nFonts))
