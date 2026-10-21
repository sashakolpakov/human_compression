"""Visible Topic G glyph identities, bound to actual font bytes and occurrences.

The font outlines were inspected independently of the decoded characters.
No global character replacement is permitted. Actual and generated whitespace
are retained. Serif/italic style alone is not recoded as a mathematical alphabet.
"""
ALIASES = {}
def add(key,font,byte,raw,out,name):
    ALIASES[key,font,byte,raw]=(out,name)
for byte,raw,out,name in [(56,'\uf8f1','⎧','bracelefttp'),(58,'\uf8f3','⎩','braceleftbt'),
                          (60,'\uf8f2','⎨','braceleftmid'),(62,'\uf8f4','⎪','braceex')]:
    add('L009','/KMZCHH+LMMathExtension10-Regular',byte,raw,out,name)
for c,out in {'F':'𝔽','Z':'ℤ'}.items():
    add('L009','/DDHMCF+MSBM10',ord(c),c,out,c)
for c,out in {'D':'𝒟','L':'ℒ','P':'𝒫','Q':'𝒬','T':'𝒯'}.items():
    add('L009','/TCEDQP+LMMathSymbols10-Regular',ord(c),c,out,c)
for c,out in {'A':'𝒜','B':'ℬ','F':'ℱ','H':'ℋ','L':'ℒ','P':'𝒫','S':'𝒮'}.items():
    add('L092','/VDSZLX+CMSY10',ord(c),c,out,c)
add('L092','/CGSUNQ+LASY10',50,'2','□','a50')
add('L092','/DDDNSV+LINE10',34,'"','╱','a34')
add('L092','/DDDNSV+LINE10',98,'b','╲','a98')
add('L092','/UERUKV+LCIRCLE10',116,'t','●','a116')

def glyph_alias(key,c,font,event=None):
    candidates=[k for k in ALIASES if k[0]==key and k[1]==font and k[3]==c]
    if not candidates:return None
    if event is None:raise ValueError('Actual PDF event required for visible glyph identity')
    entry=ALIASES.get((key,font,event['encoded_byte'],c))
    if entry is None:return None
    out,name=entry
    if event['glyph_name']!=name:raise ValueError('Actual embedded glyph name differs')
    return out
