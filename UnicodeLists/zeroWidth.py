# Don't forget combining characters...
#
zeroWidthUnicodeChars = {
    chr(0x200B):  "Zero-width space",
    chr(0x200C): "Zero-width non-joiner",
    chr(0x200D): "Zero-width joiner",
    chr(0x2060): "Word joiner",   # (fairly new)
    chr(0xFEFF): "Zero-width no-break space",
    # chr(0x035F): "Combing grapheme joiner",
}
