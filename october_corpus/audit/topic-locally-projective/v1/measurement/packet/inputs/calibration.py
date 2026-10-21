"""Eight actual font/byte classes, identified from these embedded outlines.

Both raw variants remain unchanged. No source formula, historical count,
ligature or printed hyphen is emended. The mapsto tail remains separate
from its adjacent right-arrow glyph. Own Unicode PDF text is unchanged.
"""
SCRIPT={'K':'𝒦','L':'ℒ','P':'𝒫','Q':'𝒬'}
def classify(r,key):
 f,g,c=r['font'],r['glyph_name'],r['decoded_text']
 if key in ('L084','L095') and 'CMSY' in f and g in SCRIPT:
  return SCRIPT[g],'visible_symbol','Embedded calligraphic mathematical letter; preserve the visible alphabet rather than its plain-capital encoding alias.'
 if key=='L084' and f=='/MarVoSym' and r['encoded_byte']==66 and g=='B':
  return '✉','visible_symbol','Literal correspondence-envelope outline at the author address; not the plain letter B.'
 if key=='L095' and 'LASY10' in f and g=='a50':
  return '□','visible_symbol','Literal open square marking proof end; not the extracted eight-point star.'
 if key=='L095' and 'CMSY' in f and g=='mapsto':
  return '⊢','visible_symbol','Literal mapsto tail component; the adjacent arrowright glyph remains independently counted. No assembly of two events into one.'
 return None

def aliases_from(audits):
 import unicodedata
 out=[]
 for key,a in audits.items():
  for r in a['encoded_glyph_classes']:
   t=classify(r,key)
   if t is None:continue
   c,kind,reason=t
   out.append(dict(source=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=c,output_name=unicodedata.name(c),occurrences=r['occurrences'],kind=kind,reason=reason,glyph_evidence=r['glyph_evidence']))
 return out
