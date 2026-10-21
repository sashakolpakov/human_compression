"""Literal actual-outline substitutions, never source mathematics corrections."""
import unicodedata
SPECIAL={'vextendsingle':'⏐','angbracketleftBigg':'⟨','angbracketrightBigg':'⟩','intersectiontext':'⋂','intersectiondisplay':'⋂','productdisplay':'∏','mapsto':'⊢'}
SCRIPT={'C':'𝒞','F':'ℱ','G':'𝒢','H':'ℋ','L':'ℒ','O':'𝒪','P':'𝒫','Q':'𝒬','U':'𝒰','W':'𝒲'}
def output(row):
 f,g,c=row['font'],row['glyph_name'],row['decoded_text']
 if 'CMSY' in f and g in SCRIPT:return SCRIPT[g]
 if f=='/Marvosym' and g=='letter':return '✉'
 if g in SPECIAL and SPECIAL[g]!=c:return SPECIAL[g]
 return None
if __name__=='__main__':
 from pathlib import Path
 import json
 O=Path(__file__).resolve().parent;audits=json.loads((O/'font_audit.json').read_text());rows=[]
 for key,a in audits.items():
  for r in a['encoded_glyph_classes']:
   out=output(r)
   if out is not None:rows.append(dict(document=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=out,output_name=unicodedata.name(out),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']))
 (O/'glyph_aliases.json').write_text(json.dumps(dict(status='ACTUAL_OUTLINES_VIEWED_PENDING_DISTINCT_REVIEW',aliases=rows),ensure_ascii=False,indent=2)+'\n');print('aliases',len(rows),'occurrences',sum(r['occurrences'] for r in rows))
