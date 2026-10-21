"""Exact source-specific encoded glyph rules; no font-name-only dispatch."""
import json
from pathlib import Path
from font_tools import need
RULES=json.loads((Path(__file__).resolve().parent/'glyph_rules.json').read_text())['rules']
def aliases_from(audit):
 out=[]
 for rule in RULES:
  hits=[r for r in audit[rule['source']]['encoded_glyph_classes'] if r['font_identity']==rule['font_identity'] and r['encoded_byte']==rule['encoded_byte']]
  need(len(hits)==1,'one actual source dictionary/byte class');r=hits[0]
  for k in ['font_identity','font_dictionary_object','font','encoded_byte','glyph_name','occurrences','font_stream_sha256']:need(r[k]==rule[k],'exact calibrated glyph '+k)
  need(r['decoded_text']==rule['input'] and r['glyph_evidence']['outline_sha256']==rule['outline_sha256'],'actual visible outline and extraction');out.append(dict(rule))
 need(len(out)==37 and sum(r['occurrences'] for r in out)==780,'37 complete classes /780 occurrences')
 return out
