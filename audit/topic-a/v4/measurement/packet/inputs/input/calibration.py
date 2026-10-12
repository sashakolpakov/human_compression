"""Input-specific glyph identities; event/dictionary bindings are checked separately.

Ordinary ligature extraction and separate negation/arrow components are retained.
This table does not transplant a prior PDF's glyph encoding.
"""
RULES={
 '/GIYIZD+CMEX10':{'bracketlefttp':'⎡','bracketrighttp':'⎤','bracketleftbt':'⎣','bracketrightbt':'⎦','bracketleftex':'⎢','bracketrightex':'⎥'},
 '/ZSWOKF+MSBM10':{'Z':'ℤ'},
 '/IAPURH+CMSY10':{'mapsto':'⊢','U':'𝒰'},
 '/LAEBDV+CMEX10':{'parenleftbig':'(','parenrightbig':')','parenleftbigg':'(','parenrightbigg':')','braceleftBigg':'{','summationtext':'∑','summationdisplay':'∑'},
 '/ATEODA+MSBM10':{'Z':'ℤ'},
}
def output(row):
    value=RULES.get(row['font'],{}).get(row['glyph_name'])
    return value if value is not None and value!=row['decoded_text'] else None
