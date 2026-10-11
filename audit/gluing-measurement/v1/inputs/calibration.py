"""Only literal, visually verified distinctions; no symbolic reconstruction."""
SCRIPTS={'B':'ℬ','C':'𝒞','G':'𝒢','H':'ℋ','O':'𝒪'}
def output(r):
 f,g=r['font'],r['glyph_name']
 if 'CMSY' in f and g in SCRIPTS:return SCRIPTS[g]
 if g=='mapsto':return '⊢'
 return None
