"""Actual viewed glyphs: calibrated sensitivity only, never raw-primary edits."""
GREEK={'Phi1':'Φ','Psi1':'Ψ','Gamma1':'Γ','Lambda1':'Λ','Omega1':'Ω','Delta1':'Δ'}
SCRIPT={'K':'𝒦','M':'ℳ','P':'𝒫','T':'𝒯','X':'𝒳','Y':'𝒴'}
DOUBLE={'P':'ℙ','T':'𝕋'}
def output(r):
 f,g=r['font'],r['glyph_name']
 if 'MTMI' in f and g in GREEK:return GREEK[g]
 if 'CMSY' in f and g in SCRIPT:return SCRIPT[g]
 if 'MSBM' in f and g in DOUBLE:return DOUBLE[g]
 if 'MarVoSym' in f and g=='B':return '✉'
 if 'MTSYN' in f and g=='mapsto':return '⊢'
 return None
