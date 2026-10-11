"""Visible glyph identities, bound to actual dictionary and text events.

Right-brace byte9 is decoded as a tab. The four mapsto vertical strokes and
separate right-arrow glyphs remain separate; no formula is merged. Wide tilde
accents keep one spacing-tilde character, with placement cost unknown.
"""
ALIASES={}
def add(font,byte,raw,out,name):
    ALIASES['F010',font,byte,raw]=(out,name)
for byte,raw,out,name in [(0,'\0','(','parenleftbig'),(1,'\1',')','parenrightbig'),
 (8,'\b','{','braceleftbig'),(9,'\t','}','bracerightbig'),(40,'(','{','braceleftBigg'),
 (56,'\uf8f1','⎧','bracelefttp'),(58,'\uf8f3','⎩','braceleftbt'),
 (60,'\uf8f2','⎨','braceleftmid'),(62,'\uf8f4','⎪','braceex'),
 (71,'G','⨆','unionsqdisplay'),(101,'e','˜','tildewide')]:
    add('/AYZVIA+CMEX10',byte,raw,out,name)
add('/HVIIAG+CMEX7',101,'e','˜','tildewide')
add('/TUCRSU+CMSY10',55,'7','∣','mapsto')
add('/TUCRSU+CMSY10',71,'G','𝒢','G')
def glyph_alias(key,c,font,event=None):
    candidates=[k for k in ALIASES if k[0]==key and k[1]==font and k[3]==c]
    if not candidates:return None
    if event is None:raise ValueError("Actual PDF event required")
    entry=ALIASES.get((key,font,event["encoded_byte"],c))
    if entry is None:return None
    out,name=entry
    if event["glyph_name"]!=name:raise ValueError("Actual glyph name differs")
    return out
