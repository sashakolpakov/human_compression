"""Exact visible component substitutions; no scientific statement repair."""
SPECIAL={'mapsto':'⊢','parenleftbig':'(','parenrightbig':')','angbracketleftbig':'⟨','angbracketrightbig':'⟩','vextendsingle':'⏐','braceleftBigg':'{','angbracketleftBig':'⟨','angbracketrightBig':'⟩','intersectiondisplay':'⋂','tildewide':'˜'}
def output(row):
 f,g,c=row['font'],row['glyph_name'],row['decoded_text']
 if 'CMSY' in f and g=='G':return '𝒢'
 if 'XYDASH' in f:return {'a8':'╱','a54':'╲','a72':'╲','a118':'╱'}[g]
 if g in SPECIAL and SPECIAL[g]!=c:return SPECIAL[g]
 return None
if __name__=='__main__':
 from pathlib import Path
 import json,unicodedata
 O=Path(__file__).resolve().parent;a=json.loads((O/'font_audit.json').read_text())['N007'];rows=[]
 for r in a['encoded_glyph_classes']:
  out=output(r)
  if out is not None:rows.append(dict(font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=out,output_name=unicodedata.name(out),occurrences=r['occurrences'],glyph_evidence=r['glyph_evidence']))
 (O/'glyph_aliases.json').write_text(json.dumps(dict(status='AUTHOR_ACTUAL_OUTLINES_VIEWED_PENDING_DISTINCT_REVIEW',aliases=rows),ensure_ascii=False,indent=2)+'\n');print(len(rows),'classes',sum(r['occurrences'] for r in rows),'occurrences')
