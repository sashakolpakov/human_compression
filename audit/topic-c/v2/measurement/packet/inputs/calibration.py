"""Declared visible-glyph aliases. No mathematical or linguistic rewriting."""
# L088 glyph names are read from its embedded CFF encodings and checked on
# complete rendered pages. TeX control aliases at 0/161 share the same outline.
L088_SYMBOLS = {'\x02':'×','\x03':'∗','\x12':'⊆','\x14':'≤','\x15':'≥',
 '\x18':'∼','!':'→','2':'∈','6':'̸',';':'∅','\\':'∩','f':'{','g':'}',
 'h':'⟨','i':'⟩','j':'|','n':'\\'}
L088_SMALL_SYMBOLS={'0':'′','2':'∈','[':'∪','f':'{','g':'}','n':'\\'}
L088_ITALICS={'\x11':'η','\x16':'μ','\x17':'ν','\x1b':'σ','\x1c':'τ',
 '!':'ω',';':',','=':'/'}
F014_EXT={'\x00':'(','\x01':')','\x08':'{','\t':'}','\x0b':'⟩','\x0c':'⎪',
 '\x10':'(','\x11':')','\x14':'[','\x15':']','\x1c':'⟨','\x1d':'⟩',
 '\uf8ee':'⎡','\uf8ef':'⎢','\uf8f0':'⎣','\uf8f9':'⎤','\uf8fa':'⎥','\uf8fb':'⎦',
 'P':'∑','X':'∑','!':')'}

def glyph_alias(key, c, font):
    if key=='L088':
        if 'CharterBT' in font:
            return {"'":'’','\x02':'ﬁ','\x03':'ﬂ','\x1e':'`','\x93':'“','\x94':'”',
                    '\x96':'–','\xad':'-'}.get(c)
        if 'CMSY10' in font:return L088_SYMBOLS.get(c)
        if 'CMSY7' in font:return L088_SMALL_SYMBOLS.get(c)
        if 'CMSY9' in font:return {'f':'{','g':'}'}.get(c)
        if 'CMMI' in font:return L088_ITALICS.get(c)
        if ('CMR10' in font or 'CMBX12' in font) and c=='\0':return 'Γ'
        if 'LCIRCLE10' in font and c=='i':return '○'
        if 'LINE10' in font:return {'\0':'╱','@':'╲'}.get(c)
    if key=='F014':
        if font=='/FOZNML+CMEX10':return F014_EXT.get(c)
        # The source uses the mapsto vertical stroke and a separate arrow;
        # preserve those separate pieces, rather than merging a formula.
        if font=='/FWQTPO+CMSY10' and c=='7':return '∣'
    return None

# These four whitespace-looking CMEX glyphs are actual source operators,
# separately located in the PDF text stream. Other newlines/spaces are layout.
F014_WHITESPACE = {(8,249.5,533.7):'(', (8,272.9,282.6):'(',
                  (8,307.6,216.5):'(', (10,331.3,634.0):'⟨'}
