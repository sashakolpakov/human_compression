"""Proposed event-bound glyph calibration; diagram proxies are not literal Unicode.

The original pypdf strings remain in both raw variants. Curve and line
components receive one directional counting proxy per actual PDF event.
The separate text-only sensitivity removes those components, without
claiming to measure the discarded diagram geometry or to repair a theorem.
"""
SPECIAL={'mapsto':'⊢','parenleftbig':'(','parenrightbig':')','angbracketleftbig':'⟨','angbracketrightbig':'⟩','vextendsingle':'⏐','braceleftBigg':'{','angbracketleftBig':'⟨','angbracketrightBig':'⟩','intersectiondisplay':'⋂','intersectiontext':'⋂','tildewide':'˜','unionsqtext':'⨆','circleplustext':'⨁','producttext':'∏'}
BRACES={'bracehtipdownleft':'◜','bracehtipdownright':'◝','bracehtipupleft':'◟','bracehtipupright':'◞'}
CIRCLES={'c16':'◟','c17':'◟','c18':'◞','c19':'◞','c20':'◝','c21':'◝','c22':'◜','c23':'◜'}
DASH={'N007':{'a8':'╱','a54':'╲','a72':'╲','a118':'╱'},'N006':{'a0':'╱','a62':'╲','a95':'─'}}
def classify(row,key):
 f,g,c=row['font'],row['glyph_name'],row['decoded_text']
 if 'XYDASH' in f:return DASH[key][g],'graphical_proxy','One direction-based line proxy per encoded stroke; exact slope, length and connectivity unmeasured.'
 if 'XYCIRC' in f:return CIRCLES[g],'graphical_proxy','One quadrant proxy per encoded curved fragment. Eight events form one source circle; arc angle and layout are not represented by Unicode.'
 if g in BRACES:return BRACES[g],'graphical_proxy','One directional proxy per underbrace tip fragment; not a literal Unicode extraction or complete underbrace geometry.'
 if 'CMSY' in f and g=='G':return '𝒢','visible_symbol','Actual calligraphic G outline; preserve visible mathematical alphabet.'
 if g in SPECIAL and SPECIAL[g]!=c:return SPECIAL[g],'visible_symbol','Actual mathematical glyph/individual delimiter component identified from embedded outline; no formula emendation.'
 return None

def aliases_from(audits):
 import unicodedata
 result=[]
 for key,audit in audits.items():
  for r in audit['encoded_glyph_classes']:
   x=classify(r,key)
   if x is None:continue
   out,kind,reason=x
   result.append(dict(source=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=out,output_name=unicodedata.name(out),occurrences=r['occurrences'],kind=kind,reason=reason,glyph_evidence=r['glyph_evidence']))
 return result
if __name__=='__main__':
 from pathlib import Path
 import json
 o=Path(__file__).resolve().parent;a=aliases_from(json.loads((o/'font_audit.json').read_text()))
 (o/'glyph_aliases.json').write_text(json.dumps(dict(status='PROPOSED_CALIBRATION_PENDING_DISTINCT_INPUT_REVIEW',diagram_proxy_is_literal_unicode_extraction=False,full_graphics_cost=None,text_only_alternative='Replace only the identified graphical_proxy events by separators; retain all ordinary text, formula symbols, labels and other counted content.',aliases=a),ensure_ascii=False,indent=2)+'\n')
 print({k:(sum(x['source']==k for x in a),sum(x['occurrences'] for x in a if x['source']==k)) for k in ['N007','N006']})
