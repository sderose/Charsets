# A dict of the Unicode Scripts mentioned in Scripts.txt.
# Note that the Unicode Script names are very close to Block names,
# but not the same:
#     * They use underwscores, not spaces
#     * They only include blocks for writing natural lanauges
#       (plus "Common" and "Inherited")
#     * "Extended", "Supplement", etc. are merged
#
# As for blocks, the language codes given here are my best estimate.
# Same scripts are used for multiple languages, and some languages used
# multiple scripts.
#
# The Script code is taken from ISO 15924 when possible (that standard also
# has many scripts which are not mentioned in Unicode).
#
# I have set the language code to:
#     An ISO 693-3 code when it seems clearly applicable.
#     "" when a script seems to be the primary script for multiple languages,
#     "None" for Common and Inherited, and
#     "_??" when I don't know or can't find an ISO-639-3 code (yet).
#     "_ID" for Han
#     "_CY" for Cyrillic
#
# Type and script are Enum-erated below, but I have not added them for
# many entries yet.
#
# To do:
#     Sync new information with Blocks.py.
#
# History:
# 2023-05-03: Assembled by Steven J. DeRose, sderose@acm.org.
#
from enum import Enum

class ScriptType(Enum):
    SYLL   = "Syllabary"
    ALPH   = "Alphabetic"
    ABUG   = "Abugida"
    HEIR   = "Hierogrlyphic"
    IDEO   = "Iedographic"
    SPEC   = "Alternative script for special purpose(s)"
    STEN   = "Stenographic or shorthand system"

SYLL = ScriptType("SYLL")
ALPH = ScriptType("ALPH")
ABUG = ScriptType("ABUG")
HEIR = ScriptType("HEIR")
IDEO = ScriptType("IDEO")
SPEC = ScriptType("SPEC")
STEN = ScriptType("STEN")


class ScriptStatus(Enum):
    CUR    = "In use currently/recently"
    OBS    = "Language or script is in little/no current use"

CUR = ScriptStatus("CUR")
OBS = ScriptStatus("OBS")

UnicodeScripts = {
    # Unicode Script name               ( Code,   LG, type, status )
    "Adlam":                            ( "Adlm", "FUL", ),  #
    "Ahom":                             ( "Ahom", "AHO", ),
    "Anatolian_Hieroglyphs":            ( "Hluw", "_??", ),  #
    "Arabic":                           ( "Arab", "ARA", CUR, ),
    "Armenian":                         ( "Armn", "HYE", CUR, ),
    "Avestan":                          ( "Avst", "AVE", ),
    "Balinese":                         ( "Bali", "BAN", ),
    "Bamum":                            ( "Bamu", "BAX", OBS ),  # 19c
    "Bassa_Vah":                        ( "Bass", "BSQ", ),
    "Batak":                            ( "Batk", "BYA", ),
    "Bengali":                          ( "Beng", "BEN", CUR, ),
    "Bhaiksuki":                        ( "Bhks", "SAN", OBS ),  # 11-12c <Brahmi
    "Bopomofo":                         ( "Bopo", "CMN", SYLL, ),  #
    "Brahmi":                           ( "Brah", "_??", ),  #
    "Braille":                          ( "Brai", "", SPEC,  CUR, ),
    "Buginese":                         ( "Bugi", "BUG", ),
    "Buhid":                            ( "Buhd", "BKU", ),
    "Canadian_Aboriginal":              ( "Cans", "", ),
    "Carian":                           ( "Cari", "XCR", ),
    "Caucasian_Albanian":               ( "Aghb", "_??", ),  #
    "Chakma":                           ( "Cakm", "CCP", ),
    "Cham":                             ( "Cham", "CJA", ABUG ),  # <Brahmi
    "Cherokee":                         ( "Cher", "CHR", ),
    "Common":                           ( "", None, ),  # *******
    "Coptic":                           ( "Copt", "_??", ),  #
    "Cuneiform":                        ( "Xsux", "_??", OBS ),  #   # Sumerian &c
    "Cypriot":                          ( "Cprt", "", SYLL ),
    "Cyrillic":                         ( "Cyrl", "_CY", CUR, ),
    "Deseret":                          ( "Dsrt", "ENG", OBS ),  # 19c EN spelling reform
    "Devanagari":                       ( "Deva", "", ABUG, CUR, ),
    "Duployan":                         ( "Dupl", "FRA", STEN ),  #
    "Egyptian_Hieroglyphs":             ( "Egyp", "EGY", OBS ),
    "Elbasan":                          ( "Elba", "SQI", ALPH, OBS ),  # 18c
    "Ethiopic":                         ( "Ethi", "GEZ", CUR, ),  # aka Ge'ez
    "Georgian":                         ( "Geor", "KAT", ),
    "Glagolitic":                       ( "Glag", "CHU", OBS, ),  # 9c OC Slavonic
    "Gothic":                           ( "Goth", "GOT", ),
    "Grantha":                          ( "Gran", "_??", ),  #
    "Greek":                            ( "Grek", "ELL", CUR, ),
    "Gujarati":                         ( "Gujr", "GUJ", CUR, ),
    "Gurmukhi":                         ( "Guru", "_??", ),  #   # Punjabi
    "Han":                              ( "Hani", "_ID", CUR, ),
    "Hangul":                           ( "Hang", "", CUR, ),
    "Hanunoo":                          ( "Hano", "HNN", ),
    "Hatran":                           ( "Hatr", "_??", ),  #
    "Hebrew":                           ( "Hebr", "HEB", CUR, ),
    "Hiragana":                         ( "Hira", "JPN", CUR, ),
    "Imperial_Aramaic":                 ( "Armi", "ARC", ),
    "Inherited":                        ( "", None, ),  # *******
    "Inscriptional_Pahlavi":            ( "Phli", "PAL", ),
    "Inscriptional_Parthian":           ( "Prti", "XPR", ),
    "Javanese":                         ( "Java", "JAV", ),
    "Kaithi":                           ( "Kthi", "_??", ),  #
    "Kannada":                          ( "Knda", "KAN", ),
    "Katakana":                         ( "Kana", "JPN", ),
    "Kayah_Li":                         ( "Kali", "_??", ),  #
    "Kharoshthi":                       ( "Khar", "_??", ),  #
    "Khmer":                            ( "Khmr", "KHM", ),
    "Khojki":                           ( "Khoj", "_??", ),  #
    "Khudawadi":                        ( "Sind", "_??", ),  # aka Sindhi
    "Lao":                              ( "Laoo", "LAO", ),
    "Latin":                            ( "Latn", "LAT", ALPH, CUR ),
    "Lepcha":                           ( "Lepc", "LEP", ),
    "Limbu":                            ( "Limb", "LIF", ),
    "Linear_A":                         ( "Lina", "_??", OBS, ),  #
    "Linear_B":                         ( "Linb", "_??", OBS, ),  #
    "Lisu":                             ( "Lisu", "LIS", ),
    "Lycian":                           ( "Lyci", "XLC", ),
    "Lydian":                           ( "Lydi", "XLD", ),
    "Mahajani":                         ( "Mahj", "_??", ),  #
    "Malayalam":                        ( "Mlym", "MAL", CUR, ),
    "Mandaic":                          ( "Mand", "MID", ),
    "Manichaean":                       ( "Mani", "XMN", ),
    "Marchen":                          ( "Marc", "_??", ),  #
    "Masaram_Gondi":                    ( "Gonm", "_??", ),  #
    "Meetei_Mayek":                     ( "Mtei", "_??", ),  # aka Meitei Mayek
    "Mende_Kikakui":                    ( "Mend", "MEN", ),
    "Meroitic_Cursive":                 ( "Merc", "XMR", ),
    "Meroitic_Hieroglyphs":             ( "Mero", "XMR", ),
    "Miao":                             ( "Pird", "_??", ),  #
    "Modi":                             ( "Modi", "_??", ),  #
    "Mongolian":                        ( "Mong", "MON", ),
    "Mro":                              ( "Mroo", "_??", ),  #
    "Multani":                          ( "Mult", "_??", ),  #
    "Myanmar":                          ( "Mymr", "_??", ),  #
    "Nabataean":                        ( "Nbat", "_??", ),  #
    "New_Tai_Lue":                      ( "Talu", "_??", ),  #
    "Newa":                             ( "Newa", "_??", ),  #
    "NKo":                              ( "Mkoo", "_??", ),  # N'Ko
    "Nushu":                            ( "Nshu", "_??", ),  #
    "Ogham":                            ( "Ogam", "_??", ),  #
    "Ol_Chiki":                         ( "Olck", "_??", ),  #
    "Old_Hungarian":                    ( "Hung", "OHU", OBS, ),
    "Old_Italic":                       ( "Ital", "_??", OBS, ),  #
    "Old_North_Arabian":                ( "Narb", "ARA", OBS, ),
    "Old_Permic":                       ( "Perm", "_??", OBS, ),  #
    "Old_Persian":                      ( "Xpeo", "PEO", OBS, ),
    "Old_South_Arabian":                ( "Sarb", "ARA", OBS, ),
    "Old_Turkic":                       ( "Orkh", "_??", OBS, ),  #
    "Oriya":                            ( "Orya", "ORI", ),
    "Osage":                            ( "Osge", "OSA", ),
    "Osmanya":                          ( "Osma", "_??", ),  #
    "Pahawh_Hmong":                     ( "Hmng", "HMN", ),
    "Palmyrene":                        ( "Palm", "_??", ),  #
    "Pau_Cin_Hau":                      ( "Pauc", "_??", ),  #
    "Phags_Pa":                         ( "Phag", "_??", ),  #
    "Phoenician":                       ( "Phnx", "PHN", OBS, ),
    "Psalter_Pahlavi":                  ( "Phlp", "PAL", ),
    "Rejang":                           ( "Rjng", "REJ", ),
    "Runic":                            ( "Runr", "_??", ),  #
    "Samaritan":                        ( "Samr", "SAM", ),
    "Saurashtra":                       ( "Saur", "SAZ", ),
    "Sharada":                          ( "Shrd", "_??", ),  #
    "Shavian":                          ( "Shaw", "_??", ),  #
    "Siddham":                          ( "Sidd", "_??", ),  #
    "SignWriting":                      ( "Sgnw", "_??", ),  #
    "Sinhala":                          ( "Sinh", "SIN", ),
    "Sora_Sompeng":                     ( "Sora", "_??", ),  #
    "Soyombo":                          ( "Soyo", "_??", ),  #
    "Sundanese":                        ( "Sund", "SUN", ),
    "Syloti_Nagri":                     ( "Sylo", "_??", ),  #
    "Syriac":                           ( "Syrc", "SYC", ),  # cf Syre Syrj Syrn
    "Tagalog":                          ( "Tglg", "TGL", ),
    "Tagbanwa":                         ( "Tagb", "TBW", ),
    "Tai_Le":                           ( "Tale", "_??", ),  #
    "Tai_Tham":                         ( "Lana", "_??", ),  # aka Lanna
    "Tai_Viet":                         ( "Tavt", "_??", ),  #
    "Takri":                            ( "Takr", "_??", ),  #
    "Tamil":                            ( "Taml", "TAM", ),
    "Tangut":                           ( "Tang", "TXG", ),
    "Telugu":                           ( "Telu", "TEL", ),
    "Thaana":                           ( "Thaa", "_??", ),  #
    "Thai":                             ( "Thai", "THA", CUR, ),
    "Tibetan":                          ( "Tibt", "BOD", ),
    "Tifinagh":                         ( "Tfng", "_??", ),  #
    "Tirhuta":                          ( "Tirh", "_??", ),  #
    "Ugaritic":                         ( "Ugar", "UGA", OBS, ),
    "Vai":                              ( "Vaii", "VAI", ),
    "Warang_Citi":                      ( "Wara", "_??", ),  #
    "Yi":                               ( "Yiii", "", ),
    "Zanabazar_Square":                 ( "Zanb", "MON", OBS, ),  # Also Tibetan, Sanskrit, ),
}
