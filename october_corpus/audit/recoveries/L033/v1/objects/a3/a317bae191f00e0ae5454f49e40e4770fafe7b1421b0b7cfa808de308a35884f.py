"""Acquire declared flat exports and bindings only; never discover nested records."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import json,hashlib,importlib.util
S=Path('/Users/sasha/medusa/research/leemans');R=Path('/Users/sasha/medusa/math_compression')
spec=importlib.util.spec_from_file_location('records',S/'reboot_20261013/component_review_records.py');records=importlib.util.module_from_spec(spec);spec.loader.exec_module(records)
class Closure:
 def __init__(self):self.files={}
 def add(self,p,row=None):
  p=Path(p);item=records.pin(p)
  if row and (item['sha256']!=row['sha256']or item['bytes']!=row['bytes']):raise ValueError('Changed '+str(p))
  self.files[str(p)]=item;return item
 def binding(self,row,base=S):
  p=Path(row['path'])
  if p.is_absolute():return self.add(p,row)
  roots={'study':S,'public':R,'repo':R,'absolute':Path('/')}
  candidates=[roots[row['namespace']]/p]if row.get('namespace')in roots else [S/p,R/p,Path(base)/p]
  for q in candidates:
   if q.is_file() and hashlib.sha256(q.read_bytes()).hexdigest()==row['sha256']:return self.add(q,row)
  raise ValueError('Unresolved '+str(p))
 def packet(self,path):
  P=S/path;self.add(P/'manifest.json');m=json.loads((P/'manifest.json').read_text())
  for row in m['exports']:
   p=Path(row['path']);self.add(p if p.is_absolute()else P/p,row)
  ds=m.get('dependencies',[])
  if not isinstance(ds,list):ds=[] # Some manifests store the count here; the flat file carries the rows.
  if (P/'dependencies.json').is_file():ds+=json.loads((P/'dependencies.json').read_text())
  for row in ds:self.binding(row,P)
 def finish(self,name,status,record):
  self.add(Path(__file__));records.finish(name,status,record,list(self.files.values()))
