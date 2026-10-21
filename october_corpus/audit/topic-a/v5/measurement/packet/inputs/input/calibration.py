"""Input-specific, individually viewed mathematical glyph repairs; drawing aliases stay literal."""
from pathlib import Path
import json
H=Path(__file__).resolve().parent
ROWS=json.loads((H/'calibration_rules.json').read_text())['rules']
RULES={(r['font_identity'],r['encoded_byte']):r for r in ROWS}
assert len(RULES)==len(ROWS)
DRAWING={(r['font_identity'],r['encoded_byte']):r for r in json.loads((H/'drawing_policy.json').read_text())['classes']}
def output(row):
 r=RULES.get((row['font_identity'],row['encoded_byte']))
 if r is None:return None
 for k in ('font_dictionary_sha256','effective_encoding_sha256','decoded_text','glyph_name','font_stream_sha256'):
  if row[k]!=r[k]:raise ValueError('actual glyph binding differs: '+k)
 return r['output']
def drawing(row):
 return (row['font_identity'],row['encoded_byte'])in DRAWING
