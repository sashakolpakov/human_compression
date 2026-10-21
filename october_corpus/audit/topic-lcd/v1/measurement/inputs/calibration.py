"""Visible input-specific glyph repairs, selected after actual outline review.

No rewrite of valid ligature extraction; NFC/NFKC remain separate. A mapsto
font component has no arrowhead: preserve the adjacent arrow as its own event.
"""
SCRIPT={'B':'ℬ','D':'𝒟','E':'ℰ','F':'ℱ','G':'𝒢','H':'ℋ','J':'𝒥','O':'𝒪','P':'𝒫','Q':'𝒬','S':'𝒮'}
BOLD_SCRIPT={'D':'𝓓','Q':'𝓠'}
BLACKBOARD={'C':'ℂ','F':'𝔽','Q':'ℚ','R':'ℝ'}
EXTENSION={'parenleftbig':'(','parenrightbig':')','parenleftbigg':'(','parenrightbigg':')',
           'floorleftbigg':'⌊','floorrightbigg':'⌋','summationtext':'∑','summationdisplay':'∑',
           'producttext':'∏','productdisplay':'∏'}
def output(row):
    font,glyph,text=row['font'],row['glyph_name'],row['decoded_text'];value=None
    if 'CMBSY' in font:value=BOLD_SCRIPT.get(glyph)
    elif 'CMSY' in font:
        value='⊢' if glyph=='mapsto' else SCRIPT.get(glyph)
    elif 'MSBM' in font:value=BLACKBOARD.get(glyph)
    elif 'CMEX' in font:value=EXTENSION.get(glyph)
    elif 'CMMIB' in font and glyph=='dotlessj':value='ȷ'
    return value if value is not None and value!=text else None
