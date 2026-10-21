"""Eight actual viewed source aliases; no own-PDF Unicode rewriting."""
def output(r):
 f,g=r['font'],r['glyph_name']
 if 'CMSY' in f:
  if g=='mapsto':return '⊢'
  return {'G':'𝒢','L':'ℒ','O':'𝒪','P':'𝒫'}.get(g)
 if 'MSBM' in f:return {'K':'𝕂','R':'ℝ','Z':'ℤ'}.get(g)
 return None
