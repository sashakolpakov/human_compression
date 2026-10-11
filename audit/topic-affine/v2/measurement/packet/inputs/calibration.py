"""Visible aliases from this source's exact fonts; no text/style modernization.

The four mathematical alphabet glyphs and four brace pieces were read from
embedded Type1 outlines and the actual pages. Mappings apply only with the
bound encoded byte, font and original decoded character. Actual space bytes
in the first-page arXiv banner remain unchanged.
"""
ALIASES = {
    ('/USZEKP+CMSY10',80,'P'): ('𝒫','P'),
    ('/USZEKP+CMSY10',85,'U'): ('𝒰','U'),
    ('/YBTCZC+MSBM10',90,'Z'): ('ℤ','Z'),
    ('/YBTCZC+MSBM10',70,'F'): ('𝔽','F'),
    ('/PUNXDP+CMEX10',56,'\uf8f1'): ('⎧','bracelefttp'),
    ('/PUNXDP+CMEX10',60,'\uf8f2'): ('⎨','braceleftmid'),
    ('/PUNXDP+CMEX10',58,'\uf8f3'): ('⎩','braceleftbt'),
    ('/PUNXDP+CMEX10',62,'\uf8f4'): ('⎪','braceex'),
}

def glyph_alias(key, character, font, event=None):
    if key != 'L012':
        return None
    candidates=[(b,value) for (f,b,c),value in ALIASES.items() if f==font and c==character]
    if not candidates:
        return None
    if event is None:
        raise ValueError('Source glyph requires its original encoded PDF event')
    result=ALIASES.get((font,event['encoded_byte'],character))
    if result is None:
        raise ValueError('Unreviewed byte sharing an extracted glyph')
    if event['glyph_name']!=result[1]:
        raise ValueError('Embedded glyph does not match the calibrated identity')
    return result[0]
