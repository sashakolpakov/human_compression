#!/usr/bin/env python3
"""Read-only assembly/provenance check; optional new GAP replay is separate.

A successful hash/structure check is not a mathematical independent review.
Without --primary-check, private source-capture checks are explicitly skipped.
No old GAP program is rerun by this verifier.
"""
import argparse
from collections import Counter
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
import time
ROOT=Path(__file__).resolve().parent
P='phase78_n009_integration_'

def req(x,msg):
    if not x:raise RuntimeError(msg)

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hs(s):return hashlib.sha256(s.encode()).hexdigest()
def rd(s):return json.loads((ROOT/s).read_text())

class Pre(HTMLParser):
    def __init__(self):super().__init__();self.on=False;self.blocks=[];self.buf=[]
    def handle_starttag(self,t,a):
        if t=='pre':self.on=True;self.buf=[]
    def handle_endtag(self,t):
        if t=='pre':self.on=False;self.blocks.append(''.join(self.buf))
    def handle_data(self,s):
        if self.on:self.buf.append(s)

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--primary-check',action='store_true')
    ap.add_argument('--run-new-gap',type=Path)
    a=ap.parse_args();req(not a.output.exists(),'Refusing existing verification output')
    if a.run_new_gap:req(not a.run_new_gap.exists(),'Refusing existing GAP output directory')
    start=time.monotonic();assembly=rd(P+'assembly.json');ledger=rd(P+'ledger.json');intake=rd(P+'intake.json')
    if (ROOT/(P+'manifest.json')).exists():
        manifest=rd(P+'manifest.json')
        for r in manifest['files']:req(sha(ROOT/r['path'])==r['sha256'],'Manifest input hash: '+r['path'])
    m=(ROOT/assembly['manuscript']['path']).read_text();old=(ROOT/assembly['base']['path']).read_text()
    req(sha(ROOT/assembly['manuscript']['path'])==assembly['manuscript']['sha256']==ledger['manuscript']['sha256'],'Manuscript binding')
    req(sha(ROOT/assembly['base']['path'])==assembly['base']['sha256'],'Frozen predecessor binding')
    for r in intake['retained_input_bindings']:req(sha(ROOT/r['path'])==r['sha256'],'Retained input hash '+r['path'])
    req(len(ledger['contracts'])==120 and len({r['integration_id'] for r in ledger['contracts']})==120,'Contract row count/uniqueness')
    for r in ledger['contracts']:
        p=r['integrated_proof_span'];req(hs(m[p['start_codepoint']:p['end_codepoint_exclusive']])==p['sha256_utf8'],'Actual integrated proof span '+r['integration_id'])
    previous=rd('phase65_petrial_integration_ledger.json')['contracts']
    current={r['integration_id']:r for r in ledger['contracts']}
    for r in previous:
        p=r['integrated_proof_span'];q=current[r['integration_id']]['integrated_proof_span']
        req(old[p['start_codepoint']:p['end_codepoint_exclusive']]==m[q['start_codepoint']:q['end_codepoint_exclusive']],'Prior proof adapter continuity')
    sec=lambda t,n: re.search(r'^## '+str(n)+r'\. .*?(?=^## |\Z)',t,re.M|re.S)[0]
    for r in assembly['hash_preserved_sections']:
        req(hs(sec(old,r['section']))==r['sha256']==hs(sec(m,r['section'])),'Unchanged section')
    req(len(assembly['hash_preserved_sections'])==19,'Nineteen whole proof sections')
    req(list(map(int,re.findall(r'^## (\d+)\.',m,re.M)))==list(range(1,27)),'Section numbering')
    tags=re.findall(r'\\tag\{([^}]+)\}',m);req(len(tags)==len(set(tags)),'Equation label uniqueness')
    blocks=re.findall(r'^```(gap|python)\n(.*?)^```',m,re.M|re.S)
    prior=re.findall(r'^```(gap|python)\n(.*?)^```',old,re.M|re.S)
    req(len(blocks)==8 and blocks[1:5]==prior[1:5],'Program continuity B–E')
    for (lang,code),record in zip(blocks,assembly['code_appendices']):
        req(lang==record['language'] and len(code.encode())==record['bytes'] and hs(code)==record['sha256'],'Complete code appendix binding')
    for index,name in [(0,'census.g'),(5,'finite.g'),(6,'data.g'),(7,'run.py')]:
        req(blocks[index][1]==(ROOT/(P+name)).read_text(),'Printed executable equals standalone file')
    rows=[r for r in ledger['contracts'] if r['paper']=='N009'];req(len(rows)==33,'Complete N009 inventory')
    req(Counter(r['source_reference'].split()[0] for r in rows)['Table']==6,'Six table targets')
    req(not any(r.get('id')=='B-retained-6' for r in ledger['retained_background']['Unified']),'Removed catalogue still live')
    req(not any(x.get('id')=='B-retained-6' for r in ledger['contracts'] for x in r.get('selected_imported_inputs',[]) if isinstance(x,dict)),'Removed catalogue still required by a source')
    replay=rd(P+'author_replay.json')
    for r in replay['inputs']:req(sha(ROOT/r['path'])==r['sha256'],'Fresh replay input hash')
    req(sha(ROOT/(P+'run.py'))==replay['runner']['sha256'],'Fresh replay runner hash')
    for source,dest in [('census.log','census.log'),('finite.log','finite.log')]:
        expected=next(x['sha256'] for x in replay['outputs'] if x['path']==source)
        req(sha(ROOT/(P+dest))==expected,'Durable fresh replay log')
    req(replay['status']=='PASS' and replay['total_census_meets']==539264 and replay['complete_presentations']==214 and replay['presentation_IP_meets']==43840,'Fresh complete execution scope')
    primary_count=0
    if a.primary_check:
        data=(ROOT/(P+'data.g')).read_text()
        entries={}
        for match in re.finditer(r'rec\(label:=("[^"]+"),order:=(\d+),typ:=(\[[^\n]*?\]),words:=(\[[^\n]*\])\)',data):
            entries[json.loads(match[1])]=json.loads(match[4])
        req(len(entries)==72,'All complete primary presentation data')
        for r in intake['primary_assets']:
            path=ROOT/r['path'];req(sha(path)==r['sha256'],'Primary capture hash')
            if 'label' not in r:continue
            html=path.read_text();parser=Pre();parser.feed(html)
            blocks=[b for b in parser.blocks if re.search(r'rels\s*:=',b)]
            req(len(blocks)==1,'Unique primary GAP presentation block')
            rels=re.search(r'rels\s*:=\s*\[(.*?)\]',blocks[0],re.S)[1].split(',')
            words=[]
            for w in rels:
                req(not re.sub(r's\d+|\s|\*','',w),'Primary word grammar')
                words.append(''.join(str(int(j)+1) for j in re.findall(r's(\d+)',w)))
            req(words==entries[r['label']],'Exact primary defining words '+r['label'])
            name=re.search(r'Atlas Canonical Name\s*<span[^>]*>(.*?)</span>',html,re.S)
            req(name is not None and unescape(name[1]).strip()==r['label'],'Exact primary canonical label')
            primary_count+=1
    if a.run_new_gap:
        run=subprocess.run([sys.executable,str(ROOT/(P+'run.py')),'--output-dir',str(a.run_new_gap)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
        req(run.returncode==0,'Fresh new GAP replay failed: '+run.stderr)
    report=dict(status='PASS',kind='Read-only assembly/continuity/provenance checks, not independent mathematical proof review',manuscript=assembly['manuscript'],proof_spans=120,prior_proof_spans_exact=87,unchanged_sections=19,full_programs=8,old_programs_B_C_D_E_unchanged=True,new_source_numbered_items=27,new_source_tables=6,primary_source_captures_checked=a.primary_check,primary_named_presentations_checked=primary_count,primary_source_capture_check_skipped=not a.primary_check,fresh_new_gap_replayed=a.run_new_gap is not None,old_gap_replayed=False,source_count_admitted=0,ratio=None,elapsed_seconds=round(time.monotonic()-start,6))
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))

if __name__=='__main__':main()
