"""Only visually verified substitutions; curved graph components stay literal."""
SCRIPTS={'D':'𝒟','F':'ℱ','G':'𝒢','P':'𝒫','T':'𝒯'}
STROKES={'a61':'╲','a1':'╱','a95':'─','a59':'╲','a0':'╱','a63':'╲','a3':'╱','a74':'╲','a77':'╲'}
def output(r):
 f,g,c=r['font'],r['glyph_name'],r['decoded_text']
 if 'XYDASH' in f:return STROKES[g]
 if 'CMSY' in f and g in SCRIPTS:return SCRIPTS[g]
 if g=='mapsto':return '⊢'
 # XYCIRC octants have no exact standard Unicode equivalent. Their literal
 # decoded names remain in every variant; geometry/assembly stays unmeasured.
 return None
