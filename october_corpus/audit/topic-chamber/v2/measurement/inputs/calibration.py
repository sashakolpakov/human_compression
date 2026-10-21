"""Visible source glyphs, with exact font-dictionary and original-byte evidence.

CMEX byte12 is a visible vertical delimiter extension decoded as whitespace.
The two N016 Type3 characters are embedded bitmap bullets, not missing text.
Each repair preserves one visible glyph; no mathematical statement is repaired.
"""
ALIASES={}
def add(key,font,byte,raw,out,name):
    ALIASES[key,font,byte,raw]=(out,name)
for byte,raw,out,name in [(12,'\x0c','⏐','vextendsingle'),
 (16,'\x10','(','parenleftBig'),(17,'\x11',')','parenrightBig'),
 (48,'\uf8eb','⎛','parenlefttp'),(49,'\uf8f6','⎞','parenrighttp'),
 (64,'\uf8ed','⎝','parenleftbt'),(65,'\uf8f8','⎠','parenrightbt'),
 (84,'T','⋂','intersectiontext'),(92,'\\','⋂','intersectiondisplay')]:
    add('L008','/VWZFEJ+CMEX10',byte,raw,out,name)
add('L008','/FRCAGV+CMSY10',71,'G','𝒢','G')
for c,out in [('K','𝒦'),('L','ℒ'),('M','ℳ'),('P','𝒫'),('Q','𝒬'),('R','ℛ'),('T','𝒯')]:
    add('N016','/SATFGU+CMSY10',ord(c),c,out,c)
add('N016','/F91',136,'\x88','•','a136')

def glyph_alias(key,c,font,event=None):
    candidates=[k for k in ALIASES if k[0]==key and k[1]==font and k[3]==c]
    if not candidates:return None
    if event is None:raise ValueError('Actual PDF text event required')
    entry=ALIASES.get((key,font,event['encoded_byte'],c))
    if entry is None:return None
    out,name=entry
    if event['glyph_name']!=name:raise ValueError('Actual glyph name differs')
    return out
