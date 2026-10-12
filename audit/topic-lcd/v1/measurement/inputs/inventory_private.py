"""Fresh exact-event inventory; all primary text/events stay in private/."""
from pathlib import Path
import json
from pdf_text import extract
from font_tools import actual_event_alignment
H=Path(__file__).resolve().parent;S=H.parent
A={};E={};M={}
for row in json.loads((H/'document_map.json').read_text())['documents']:
 key=row['key'];pdf=S/row['path'];raw,fonts,pages,meta=extract(pdf,False)
 (H/'private'/f'{key}_raw.txt').write_text(raw)
 events,audit=actual_event_alignment(pdf,raw,fonts,pages,type1_math_only=key=='A_F017',generated_newline_offsets=set(meta['generated_newline_offsets']))
 A[key]=audit;E[key]=events;M[key]={'pages':pages,'meta':meta,'fonts':fonts}
 print(key,len(pages),len(audit['encoded_glyph_classes']),flush=True)
(H/'font_audit.json').write_text(json.dumps(A,ensure_ascii=False,indent=2)+'\n')
(H/'private/events.json').write_text(json.dumps(E,ensure_ascii=False)+'\n')
(H/'private/extraction_metadata.json').write_text(json.dumps(M,ensure_ascii=False)+'\n')
