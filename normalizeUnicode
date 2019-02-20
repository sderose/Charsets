#!/usr/bin/perl -w
#
# normalizeUnicode 
#
# 2010-11-19ff: Written by Steven J. DeRose.
#     Mostly pulled from domExtensions.
# 
# To do:
#     ?? Generalize to be able to operate on any \p{name} classes??
#     Deal with ligature/accent interaction (combining long s).
#     Finish packagizing.
#     Updates from findKeyWords.
#     Entities?
# Possible additions:
#     old italic, gothic, etc. U'10300
#     roman numerals, enclosed alphanumerics
#     vertical forms U'fe00
#     Greek and Cyrillic and Hebrew math variants?
#     ellipsis, punc ligatures U'203c...
#     sup/sub U'2070
#     Halfwidth/fullwidth U'ff00
#     Non-Latin ligatures.
#     supplemental punct U'
#     Arrows? U'2190, 2799, 27f0, 2900, 2b00
#     letterlike symbols U'2100, fractions, 
#     braille U'2800
#     high surrogates U'd800, low surrogates U'dc00
#
use strict;
use Getopt::Long;
use Unicode::Normalize;
#use ../MODULES/SimplifyUnicode;

our $VERSION_DATE = "2012-11-29";

my $ignoreCase    = 0;
my $ilineends     = "U";
my $oencoding     = "";
my $olineends     = "U";
my $quiet         = 0;
my $tickInterval  = 10000;
my $verbose       = 0;

# The real options
my $accents	      = "unchanged";
my $allLigatures  = 0;
my $ligatures	  = "unchanged";
my $maths	      = "unchanged";
my $dashes	      = 0;
my $dquotes	      = 0;
my $squotes	      = 0;
my $bquote	      = 0;
my $quotes	      = 0;
my $spaces	      = 0;

###############################################################################
#
Getopt::Long::Configure ("ignore_case");
my $result = GetOptions(
    "allLigatures!"           => \$allLigatures,
    "h|help"                  => sub {
        system "perldoc $0";
        exit;
    },
    "ilineends=s"             => \$ilineends,
    "olineends=s"             => \$olineends,
    "q!"                      => \$quiet,
    "tick=i"                  => \$tickInterval,
    "v+"                      => \$verbose,
    "version"                 => sub {
        die "Version of $VERSION_DATE, by Steven J. DeRose.\n";
    },

    "accents=s"               => \$accents,
    "ligatures=s"             => \$ligatures,
    "maths=s"                 => \$maths,
    "dashes!"                 => \$dashes,
    "dquotes!"                => \$dquotes,
    "squotes!"                => \$squotes,
    "bquote!"                 => \$bquote,
    "quotes!"                 => sub { $dquotes = $squotes = 1; },
    "spaces!"                 => \$spaces,
    );

($result) || die "Bad options.\n";


###############################################################################
# Set implied options, validate option values...
#
($accents =~ m/^(atomic|unchanged|molecular|unaccent|space|delete)$/) ||

($ligatures =~ m/^(atomic|unchanged|molecular|unaccent|space|delete)$/) ||
    die "Bad value for -ligatures.\n";

($maths =~ m/^(atomic|unchanged|molecular|tag|space|delete)$/) ||
    die "Bad value for -accents.\n";

my $fh;
my $file = shift;
if ($file) {
    (-f $file) || die "Can't find input file '$file'.\n";
}
else {
	($quiet) || warn "Reading from stdin...\n";
    $file = "-";
}

open $fh, "<$file" || die "Failed to open input file '$file'.\n";
binmode($fh, ":encoding(utf8)");

if ($oencoding) {
    print "";
    binmode(STDOUT, ":encoding($oencoding)");
}

$ilineends = uc(substr($ilineends."U",0,1));
if    ($ilineends eq "M") { $/ = chr(13); }
elsif ($ilineends eq "D") { $/ = chr(13).chr(10); }
else { }

$olineends = uc(substr($olineends."U",0,1));
if    ($olineends eq "M") { $\ = chr(13); }
elsif ($olineends eq "D") { $\ = chr(13).chr(10); }
else { }


###############################################################################
###############################################################################
# Main
#
my $norm = new normalizeChars();

my $recnum = 0;
while (my $rec = <$fh>) {
    $recnum++;
    ($recnum % $tickInterval == 0) && warn "Processed $recnum records.\n";
    chomp $rec;
    if ($accents ne "unchanged") {
        $rec = $norm->handle_Diacritics($rec);
    }
    if ($ligatures ne "unchanged") {
        $rec = $norm->handle_Ligatures($rec);
    }
    if ($maths ne "unchanged") {
        $rec = $norm->handle_Maths($rec);
    }
    if ($dashes) {
        $rec = $norm->normalize_DashChars($rec);
    }
    if ($quotes) {
        $rec = $norm->normalize_DQuoteChars($rec);
        $rec = $norm->normalize_SQuoteChars($rec);
        $rec =~ s/`/'/g;
    }
    else {
        if ($dquotes) {
            $rec = $norm->normalize_DQuoteChars($rec);
        }
        if ($squotes) {
            $rec = $norm->normalize_SQuoteChars($rec);
        }
        if ($bquote) {
            $rec =~ s/`/'/g;
        }
    }
    if ($spaces) {
        $rec = $norm->normalize_SpaceChars($rec);
    }
    print $rec;
}

($quiet) || warn "Done, $recnum records processed.\n";

exit;



###############################################################################
###############################################################################
#
package normalizeChars;

sub new {
    my ($class) = @_;
    my $self = {
        # configuration
        accentOption  => "unchanged",
        ligatureDomain=> "all",
        ligatureOption=> "unchanged",
        mathOption    => "unchanged",

        # data
        dQuoteChars   => setupDQuotes(),     # Strings
        sQuoteChars   => setupSQuotes(),
        spaceChars    => setupSpaces(),
        dashChars     => setupDashes(),
        ligatureChars => setupLigatures(),
        mathStarts    => setupMaths(),       # HashRefs
        lig2seqBasic  => undef,
        seq2ligBasic  => undef,
        lig2seq       => undef,
        seq2lig       => undef,
    };
    bless $self, $class;
    return($self);
}

sub setAccentOption {
    my ($self,$v) = @_;
    $self->{accentOption} = $v;
}

sub setLigatureDomain {
    my ($self,$v) = @_;
    $self->{ligatureDomain} = $v;
}

sub setLigatureOption {
    my ($self,$v) = @_;
    $self->{ligatureOption} = $v;
}

sub setMathOption {
    my ($self,$v) = @_;
    $self->{mathOption} = $v;
}

###############################################################################
#
sub normalize_Space {
    my ($self,$s) = @_;
    $s =~ s/\s\s+/ /g;
    $s =~ s/^\s+//g;
    $s =~ s/\s+$//g;
    return($s);
}

sub normalize_DashChars {
    my ($self,$s) = @_;
    $s =~ s/[$self->{dashChars}]/-/g;
    return($s);
}

sub normalize_DQuoteChars {
    my ($self,$s) = @_;
    $s =~ s/[$self->{dQuoteChars}]/"/g;
    return($s);
}

sub normalize_SQuoteChars {
    my ($self,$s) = @_;
    $s =~ s/[$self->{sQuoteChars}]/'/g;
    return($s);
}

sub normalize_SpaceChars {
    my ($self,$s) = @_;
    $s =~ s/[$self->{spaceChars}]/ /g;
    return($s);
}


###############################################################################
#
sub handle_Diacritics {
    my ($self,$rec) = @_;        
    if ($accents eq "atomic") {
        die "unsupported -accents handling '$accents'\n";
    }
    elsif ($accents eq "molecular") {
        die "unsupported -accents handling '$accents'\n";
    }
    elsif ($accents eq "space") {
        die "unsupported -accents handling '$accents'\n";
    }
    elsif ($accents eq "delete") {
        die "unsupported -accents handling '$accents'\n";
    }
    elsif ($accents eq "translit") {
        $rec = NFD($rec);
        $rec =~ s/\pM//g;
    }
    else {
        # unchanged
    }
    return($rec);
}

sub handle_Ligatures {
    my ($self, $ligatures) = @_;
    my $s = "";
    my $s2lRef = $self->{seq2lig};
    my %s2l = %$s2lRef;
    if ($ligatures eq "space") {
        for my $lig (keys %s2l) {
            $s =~ s/$lig/ /g;
        }
    }
    elsif ($ligatures eq "delete") {
        for my $lig (keys %s2l) {
            $s =~ s/$lig//g;
        }
    }
    elsif ($ligatures eq "atomic") {
        for my $lig (keys %s2l) {
            $s =~ s/$lig/$s2l{$lig}/g;
        }
        die "unsupported -ligatures handling '$ligatures'\n";
    }
    elsif ($ligatures eq "molecular") {
        for my $lig (keys %s2l) {
            $s =~ s/$lig/$s2l{$lig}/g;
        }
        die "unsupported -ligatures handling '$ligatures'\n";
    }
    else {
        # unchanged
    }
    return($s);
}

sub handle_Maths {
    my ($self,$rec) = @_;
    my $buf = "";
    for (my $i=0; $i<lenght($rec); $i++) {
        my $c = substr($rec,$i,1);
        if (my $letter = math2letter(ord($c))) {
            $buf .= $letter;
        }
        else {
            $buf .= $c;
        }
    }
    return($buf);
}


###############################################################################
# Return basic ASCII letter if we got a math letter; else undef.
#
sub math2letter {
    my ($self,$n) = @_;
    my $mathStartsRef = $self->{mathStarts};
    my %ms = %$mathStartsRef;
    for my $mathRange (keys %ms) {
        my $diff = $n - $mathRange;
        next unless ($n>=0 && $n<26);
        my $type = $ms{$mathRange};
        if ($type eq "UPPER") {
            return(substr("ABCDEFGHIJKLMNOPQRSTUVWXYZ",$diff,1));
        }
        elsif ($type eq "LOWER") {
            return(substr("abcdefghijklmnopqrstuvwxyz",$diff,1));
        }
        else {
            die "Bad math alphabet type '$type'.\n";
        }
    }
    return(undef);
}


###############################################################################
#
sub setupDashes {
    my ($self) = @_;
    my $dashChars = 
        # Leave out regular hyphen so doesn't mess up regex, and since it's
        # what we normalize *to*.
        #
        chr(0x000ad) . # soft hyphen
        chr(0x0058a) . # armenian hyphen      
        chr(0x01806) . # mongolian todo soft hyphen
        chr(0x01b60) . # balinese pameneng (line-breaking hyphen)
        chr(0x02010) . # 008208) . hyphen) .        '-',
        chr(0x02011) . # non-breaking hyphen,
        chr(0x02012) . # figure dash
        chr(0x02013) . # 008211) . ndash,         '-',
        chr(0x02014) . # 008212, mdash,         '--',
        chr(0x02015) . # 008213, horbar,        '--',
        chr(0x02027) . # hyphenation point
        chr(0x02043) . # hyphen bullet
        chr(0x02053) . # swung dash
        #chr(0x21E0) .	# LEFTWARDS DASHED ARROW
        #chr(0x21E1) .	# UPWARDS DASHED ARROW
        #chr(0x21E2) .	# RIGHTWARDS DASHED ARROW
        #chr(0x21E3) .	# DOWNWARDS DASHED ARROW
        chr(0x0229d) . # circled dash
        chr(0x02448) . # ocr dash

        # Box-drawing dashes
        #
        #chr(0x2504) .	# ... LIGHT TRIPLE DASH HORIZONTAL
        #chr(0x2505) .	# ... HEAVY TRIPLE DASH HORIZONTAL
        #chr(0x2508) .	# ... LIGHT QUADRUPLE DASH HORIZONTAL
        #chr(0x2509) .	# ... HEAVY QUADRUPLE DASH HORIZONTAL
        #chr(0x254C) .	# ... LIGHT DOUBLE DASH HORIZONTAL
        #chr(0x254D) .	# ... HEAVY DOUBLE DASH HORIZONTAL

        chr(0x02e17) . # double oblique hyphen
        chr(0x02E1A) . # HYPHEN WITH DIAERESIS
        chr(0x0301c) . # wave dash
        chr(0x03030) . # wavy dash
        chr(0x030a0) . # katakana-hiragana double hyphen
        chr(0x0FE49) . # DASHED OVERLINE
        chr(0x0FE4D) . # DASHED LOW LINE
        chr(0x0FE58) . # small em dash
        chr(0x0fe63) . # small hyphen-minus
        chr(0x0ff0d) . # fullwidth hyphen-minus
        "";
    return($dashChars);
}

sub setupDQuotes {
    my ($self) = @_;
    my $dQuoteChars = 
    chr(0x00AB) .	# LEFT-POINTING DOUBLE ANGLE QUOTATION MARK *
    chr(0x00BB) .	# RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK *
    chr(0x201C) .	# LEFT DOUBLE QUOTATION MARK
    chr(0x201D) .	# RIGHT DOUBLE QUOTATION MARK
    chr(0x201E) .	# DOUBLE LOW-9 QUOTATION MARK
    chr(0x201F) .	# DOUBLE HIGH-REVERSED-9 QUOTATION MARK
    chr(0x2358) .	# APL FUNCTIONAL SYMBOL QUOTE UNDERBAR
    chr(0x235E) .	# APL FUNCTIONAL SYMBOL QUOTE QUAD
    chr(0x275D) .	# HEAVY DOUBLE TURNED COMMA QUOTATION MARK ORNAMENT
    chr(0x275E) .	# HEAVY DOUBLE COMMA QUOTATION MARK ORNAMENT
    chr(0x301D) .	# REVERSED DOUBLE PRIME QUOTATION MARK
    chr(0x301E) .	# DOUBLE PRIME QUOTATION MARK
    chr(0x301F) .	# LOW DOUBLE PRIME QUOTATION MARK
    "";
    return($dQuoteChars);
}

sub setupSQuotes {
    my ($self) = @_;
    my $sQuoteChars =
    chr(0x2018) .	# LEFT SINGLE QUOTATION MARK
    chr(0x2019) .	# RIGHT SINGLE QUOTATION MARK
    chr(0x201A) .	# SINGLE LOW-9 QUOTATION MARK
    chr(0x201B) .	# SINGLE HIGH-REVERSED-9 QUOTATION MARK
    chr(0x2039) .	# SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    chr(0x203A) .	# SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    chr(0x275B) .	# HEAVY SINGLE TURNED COMMA QUOTATION MARK ORNAMENT
    chr(0x275C) .	# HEAVY SINGLE COMMA QUOTATION MARK ORNAMENT
    chr(0x276E) .	# HEAVY LEFT-POINTING ANGLE QUOTATION MARK ORNAMENT
    chr(0x276F) .	# HEAVY RIGHT-POINTING ANGLE QUOTATION MARK ORNAMENT
    "";
    return($sQuoteChars);
}


sub setupSpaces {
    my ($self) = @_;
    my $spaceChars = 
    chr(0x0009) .    # TAB
    chr(0x000A) .    # LINE FEED
    chr(0x000B) .    # VERTICAL TAB
    chr(0x000C) .    # FORM FEED
    chr(0x000D) .    # CARRIAGE RETURN
    chr(0x0020) .    # SPACE
    chr(0x00A0) .    # NO-BREAK SPACE

    chr(0x1680) .    # OGHAM SPACE MARK

    chr(0x2002) .    # EN SPACE
    chr(0x2003) .    # EM SPACE
    chr(0x2004) .    # THREE-PER-EM SPACE
    chr(0x2005) .    # FOUR-PER-EM SPACE
    chr(0x2006) .    # SIX-PER-EM SPACE
    chr(0x2007) .    # FIGURE SPACE
    chr(0x2008) .    # PUNCTUATION SPACE
    chr(0x2009) .    # THIN SPACE
    chr(0x200A) .    # HAIR SPACE
    chr(0x200B) .    # ZERO WIDTH SPACE
    chr(0x202F) .    # NARROW NO-BREAK SPACE
    chr(0x205F) .    # MEDIUM MATHEMATICAL SPACE

    chr(0x2409) .    # SYMBOL FOR HORIZONTAL TABULATION
    chr(0x240B) .    # SYMBOL FOR VERTICAL TABULATION
    chr(0x2420) .    # SYMBOL FOR SPACE

    chr(0x3000) .    # IDEOGRAPHIC SPACE
    chr(0x303F) .    # IDEOGRAPHIC HALF FILL SPACE

    chr(0xFEFF) .    # ZERO WIDTH NO-BREAK SPACE (= byte-order mark)
    "";
    return($spaceChars);
}

# Non-Latin ligatures are not here yet, because there are *lots* of them.
#
sub setupLigatures {
    my %seq2ligBasic = (
        "ff"    => chr(0xFB00),
        "ff"    => chr(0xFB01),
        "fl"    => chr(0xFB02),
        "ffi"   => chr(0xFB03),
        "ffl"   => chr(0xFB04),
        );

    my %seq2lig = (
        "AE"    => chr(0x00C6), #	= latin capital ligature ae (1.0)
        "ae"    => chr(0x00E6), #	= latin small ligature ae (1.0)
        "IJ"    => chr(0x0132), #	LATIN CAPITAL LIGATURE IJ
        "ij"    => chr(0x0133), #	LATIN SMALL LIGATURE IJ
        "OE"    => chr(0x0152), #	LATIN CAPITAL LIGATURE OE
        "oe"    => chr(0x0153), #	LATIN SMALL LIGATURE OE
        "st"    => chr(0xFB06), #   LATIN SMALL LIGATURE ST

      # (chr(0x017F)."t") => chr(0xFB05), # long-s t
      # (chr(0x017F)."s") => chr(0x00DF), # in origin ligature of long s, s
        # there's also a combining long s at 1de5 and some accented one.
        );

    my %lig2seqBasic = ();
    my %lig2seq = ();

    # Add the basic to the main map
    for my $seq (keys %seq2ligBasic) {
        $seq2lig{$seq} = $seq2ligBasic{$seq};
    }

    # Make both reverse maps
    for my $seq (keys %seq2lig) {
        my $lig = $seq2lig{$seq};
        $lig2seq{$lig} = $seq;
        if (defined $seq2ligBasic{$seq}) {
            $lig2seqBasic{$lig} = $seq;
        }
    }

    my $foo = qq {
0587	ARMENIAN SMALL LIGATURE ECH YIWN
FB13	ARMENIAN SMALL LIGATURE MEN NOW
FB14	ARMENIAN SMALL LIGATURE MEN ECH
FB15	ARMENIAN SMALL LIGATURE MEN INI
FB16	ARMENIAN SMALL LIGATURE VEW NOW
FB17	ARMENIAN SMALL LIGATURE MEN XEH

04A4	CYRILLIC CAPITAL LIGATURE EN GHE
04B4	CYRILLIC CAPITAL LIGATURE TE TSE (Abkhasian)
04D4	CYRILLIC CAPITAL LIGATURE A IE

FB1F	HEBREW LIGATURE YIDDISH YOD YOD PATAH
FB4F	HEBREW LIGATURE ALEF LAMED
05F0	HEBREW LIGATURE YIDDISH DOUBLE VAV
05F1	HEBREW LIGATURE YIDDISH VAV YOD
05F2	HEBREW LIGATURE YIDDISH DOUBLE YOD
    };
}

sub setupMathAlphabets {
    my %mathAlphabetStarts = (
         0x1d400 => "UPPER",  # mathematical bold
         0x1d41A => "LOWER",
         0x1d434 => "UPPER",  # mathematical italic
         0x1d434 => "LOWER",
         0x1d468 => "UPPER",  # mathematical bold italic
         0x1d482 => "LOWER",
         0x1d49C => "UPPER",  # mathematical script
         0x1d4B6 => "LOWER",
         0x1d4D0 => "UPPER",  # mathematical bold script
         0x1d4EA => "LOWER",
         0x1d504 => "UPPER",  # mathematical fraktur
         0x1d51E => "LOWER",
         0x1d538 => "UPPER",  # mathematical double-struck
         0x1d552 => "LOWER",
         0x1d56C => "UPPER",  # mathematical bold fraktur
         0x1d586 => "LOWER",
         0x1d5A0 => "UPPER",  # mathematical sans-serif
         0x1d58A => "LOWER",
         0x1d5D4 => "UPPER",  # mathematical sans-serif bold
         0x1d5EE => "LOWER",
         0x1d608 => "UPPER",  # mathematical sans-serif italic
         0x1d622 => "LOWER",
         0x1d63C => "UPPER",  # mathematical sans-serif bold italic
         0x1d656 => "LOWER",
         0x0249c => "LOWER",  # parenthesized lower (no upper!)
         0x024b6 => "UPPER",  # circled upper
         0x024d0 => "LOWER",  # circled lower
         0x1d670 => "UPPER",  # mathematical monospace
         0x1d68a => "LOWER",
        );
    # (couple extras at 1d6a4, dotless i, j)
    # greek upper+lower: 1d6a8, 1d6e2, etc.
    return(\%mathAlphabetStarts);
}



###############################################################################
###############################################################################
###############################################################################
#
=pod

=head1 Usage

normalizeUnicode [options] file

Map various classes of Unicode characters. 

For example, can reduce all the
different whitespace characters to ' '; all the hyphens and dashes to '-',
and deal with various kinds of quotes, ligatures, accented characters, etc.


=head1 Options

(prefix 'no' to negate where applicable)

Several options control what is done to various classes of Unicode characters.
See the next section for descriptions of the available actions.

=over 

=item * B<--accents> <t>

What to do with diacritics:
I<atomic>, I<unchanged>, I<molecular>, I<unaccent>, I<space>, I<delete>.

=item * B<--allLigatures>

Count all Latin ligatures, not just the very
common ones (fi fl ffi ffl).

=item * B<--ligatures> <t>

What to do with ligatures:
I<atomic>, I<unchanged>, I<molecular>, I<space>, I<delete>.
See also I<--allLigatures>.

=item * B<--maths> <t>

What to do withfont-variations of 
basic Latin alphabet (that Unicode defines for math usage).
I<atomic>, I<unchanged>, I<molecular>, I<tag>, I<space>, I<delete>.
Note: Only handles Latin, not Greek or Hebrew letters so far.

=item * B<--dashes>

Turn all hyphens, dashes, etc. to hyphen.

=item * B<--dquotes>

Turn all funky double-quotes to straight.

=item * B<--squotes>

Turn all funky single-quotes to straight
(does not include back-quote, for which see I<--bquote>.

=item * B<--bquote>

Turn backquote to apostrophe.

=item * B<--quotes>

Shorthand for I<--dquotes -squotes>.

=item * B<--spaces>

Turn all whitespace (except CR, LF, and TAB)
to a normal space.

=item * B<--quiet> OR B<-q>
Suppress most messages.

=item * B<--verbose> OR B<-v>
Add more messages (repeatable).

=item * B<--version>

Show version info and exit.

=back



=head1 Action descriptions

The actions available are drawn from this list:

=over

=item * I<molecular>: use more/more complex characters wherever possible,
such as precombined character+diacritic combinations; ligatures, etc.

=item * I<unchanged>: leave them however they were in the input.

=item * I<atomic>: use fewer/simpler distinct characters, such as by
breaking ligatures apart, or splitting accented characters into separate
base and combining characters.

=item * I<space>: delete characters from the category in question, and
put in a space where they were (see also I<delete>).

=item * I<tag>: For characters that are (in the author's opinion) formatting
variations of more basic characters, express them via XML markup instead.
For the moment, a <span> element will be used (similar to HTML). For
example, I<--maths tag> would turn I<Double-struck Capital R> (U'211D) into:

    <span class='uchar doublestruck x211d'>r</span>

=item * I<delete>: delete characters from the category in question
(see also I<space>).

=back



=head1 Known Bugs and Limitations

Only a few settings for ligatures, accents, and maths are finished.
Math characters and ligatures are only handled for Latin alphabet so far.

This is gradually becoming a package.



=head1 Related commands

iconv, tuples, nonascii, entify, normalizeEntities.



=head1 Ownership

This work by Steven J. DeRose is licensed under a Creative Commons 
Attribution-Share Alike 3.0 Unported License. For further information on
this license, see L<http://creativecommons.org/licenses/by-sa/3.0/>.

For the most recent version, see L<http://www.derose.net/steve/utilities/>.

=cut
