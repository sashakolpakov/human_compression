"""Proposed glyph identities, requiring actual outline and independent review.

Keys bind source/replacement identity, actual font name, encoded byte and
literal extracted character; the extractor additionally binds dictionary,
event, page and context. No mathematical statement is corrected.
"""
import json,unicodedata
from pathlib import Path

SPECIAL={'bracelefttp':'⎧','braceleftmid':'⎨','braceleftbt':'⎩','braceex':'⎪',
 'minus':'−','periodcentered':'·','multiply':'×','reflexsubset':'⊆',
 'lessequal':'≤','greaterequal':'≥','similar':'∼','arrowright':'→',
 'similarequal':'≃','element':'∈','mapsto':'⊢','intersection':'∩','union':'∪',
 'braceleft':'{','braceright':'}','angbracketleft':'⟨','angbracketright':'⟩',
 'bar':'|','backslash':'\\','negationslash':'̸'}
SCRIPTS={'A':'𝒜','B':'ℬ','F':'ℱ','G':'𝒢','H':'ℋ','I':'ℐ','M':'ℳ','P':'𝒫','Q':'𝒬'}

def proposed_output(row):
    c=row['decoded_text'];font=row['font'];name=row['glyph_name']
    if 'CMSY' in font and name in SCRIPTS:return SCRIPTS[name]
    if name in SPECIAL and (name in ['bracelefttp','braceleftmid','braceleftbt','braceex'] or 'CMSY' in font):
        out=SPECIAL[name]
        if c!=out:return out
    return None

def glyph_alias(key,c,font,event,aliases):
    candidates=[r for r in aliases if r['document']==key and r['font']==font and r['input']==c]
    if not candidates:return None
    if event is None:raise ValueError('actual PDF event required for glyph repair')
    matches=[r for r in candidates if r['font_identity']==event['font_identity'] and r['encoded_byte']==event['encoded_byte'] and r['glyph_name']==event['glyph_name']]
    if not matches:return None
    if len(matches)!=1:raise ValueError('ambiguous glyph identity')
    return matches[0]['output']

if __name__=='__main__':
    p=Path(__file__).resolve().parent;audits=json.loads((p/'font_audit.json').read_text());rows=[]
    for key,a in audits.items():
        for r in a['encoded_glyph_classes']:
            out=proposed_output(r)
            if out is not None:
                rows.append(dict(document=key,font=r['font'],font_identity=r['font_identity'],encoded_byte=r['encoded_byte'],glyph_name=r['glyph_name'],input=r['decoded_text'],output=out,occurrences=r['occurrences'],output_name=unicodedata.name(out),glyph_evidence=r['glyph_evidence']))
    (p/'proposed_aliases.json').write_text(json.dumps(dict(status='PROPOSED_PENDING_VISUAL_AND_INDEPENDENT_REVIEW',aliases=rows),ensure_ascii=False,indent=2)+'\n')
    print(len(rows),'actual-font classes proposed;',sum(r['occurrences'] for r in rows),'occurrences; no factors')
