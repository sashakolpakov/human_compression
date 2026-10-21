"""Occurrence/embedded-byte-bound visible glyph repair for exact L014 v1 PDF.

These rules concern extracted glyph identity, not the mathematical correctness of
any printed formula. Ordinary/generated whitespace and printed hyphens remain.
"""
ALIASES = {
    ('/DHFIAV+CMSY10', 80, 'P'): ('𝒫', 'P'),
    ('/BYUDJP+MSBM10', 70, 'F'): ('𝔽', 'F'),
    ('/BYUDJP+MSBM10', 78, 'N'): ('ℕ', 'N'),
    ('/BYUDJP+MSBM10', 90, 'Z'): ('ℤ', 'Z'),
    ('/SCAAAW+CMEX10', 50, '\uf8ee'): ('⎡', 'bracketlefttp'),
    ('/SCAAAW+CMEX10', 54, '\uf8ef'): ('⎢', 'bracketleftex'),
    ('/SCAAAW+CMEX10', 52, '\uf8f0'): ('⎣', 'bracketleftbt'),
    ('/SCAAAW+CMEX10', 51, '\uf8f9'): ('⎤', 'bracketrighttp'),
    ('/SCAAAW+CMEX10', 55, '\uf8fa'): ('⎥', 'bracketrightex'),
    ('/SCAAAW+CMEX10', 53, '\uf8fb'): ('⎦', 'bracketrightbt'),
    ('/YZXNWX+MSAM10', 67, '⊳'): ('⊲', 'triangleleft'),
}


def glyph_alias(key, character, font, event=None):
    if key != 'L014':
        return None
    possible = [(byte, out, name) for (face, byte, raw), (out, name) in ALIASES.items()
                if face == font and raw == character]
    if not possible:
        return None
    if event is None or event.get('font') != font:
        raise ValueError('TOPIC_F_MEASUREMENT_REJECT: actual font event is required')
    result = ALIASES.get((font, event.get('encoded_byte'), character))
    if result is None or result[1] != event.get('glyph_name'):
        raise ValueError('TOPIC_F_MEASUREMENT_REJECT: actual embedded glyph/byte differs')
    return result[0]
