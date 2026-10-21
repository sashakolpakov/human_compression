"""Visible glyph distinctions only, applied solely in the calibrated sensitivity."""
SCRIPTS={'K':'𝒦','L':'ℒ','M':'ℳ','N':'𝒩','P':'𝒫','Q':'𝒬','R':'ℛ','T':'𝒯'}
def output(r):
 f,g=r['font'],r['glyph_name']
 if 'CMSY' in f and g in SCRIPTS:return SCRIPTS[g]
 if g=='mapsto':return '⊢'
 return None
