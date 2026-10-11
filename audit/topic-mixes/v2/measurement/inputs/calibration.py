"""Observed embedded distinctions, calibrated sensitivity only; raw stays literal."""
SCRIPTS={'B':'ℬ','F':'ℱ','H':'ℋ','M':'ℳ','P':'𝒫'}
BRACES={'bracelefttp':'⎧','braceleftmid':'⎨','braceleftbt':'⎩','braceex':'⎪'}
def output(r):
 f,g=r['font'],r['glyph_name']
 if 'CMSY' in f and g in SCRIPTS:return SCRIPTS[g]
 if g=='mapsto':return '⊢'
 if 'CMEX' in f and g in BRACES:return BRACES[g]
 return None
