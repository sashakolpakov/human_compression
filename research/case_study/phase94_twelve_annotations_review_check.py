#!/usr/bin/env python3
"""Independent frozen sidecar, semantic-delta and exact reader recovery checks.

No author annotation module is imported. This is an integrity/evidence check;
the accompanying report records the separate human-style semantic review.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
EXPECTED='4837610763a1f6a13b62428d95f93dbdcb000d276e44d13add769748f7361236'
def sha(b):return hashlib.sha256(b).hexdigest()
def need(ok,msg):
    if not ok:raise ValueError(msg)
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--study-root',type=Path,default=BASE);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();p=a.study_root
    need(not a.output.exists() and not a.output.is_symlink(),'Refusing existing output')
    manifest=p/'phase91_n009_annotations_manifest.json';need(sha(manifest.read_bytes())==EXPECTED,'frozen manifest')
    mf=json.loads(manifest.read_text());before={}
    for group in ['files','bound_infrastructure']:
        for f,b in mf[group].items():
            content=(p/f).read_bytes();need(sha(content)==b['sha256'] and len(content)==b['bytes'],'binding '+f);before[f]=sha(content)
    for f,h in mf['all_sidecar_bindings'].items():need(sha((p/f).read_bytes())==h,'evidence '+f);before[f]=h
    side=json.loads((p/'phase91_n009_annotations.json').read_text());old=json.loads((p/'phase79_eleven_attribution.json').read_text())
    raw=(p/side['manuscript']['path']).read_bytes();text=raw.decode();need(len(raw)==317916 and sha(raw)==side['manuscript']['sha256'],'complete proof')
    notes=side['notes'];ordered=sorted(notes,key=lambda n:(n['insert_after_codepoint'],n['id']));need(notes==ordered,'stable annotation order')
    need(len(notes)==len({n['id'] for n in notes})==41,'note inventory')
    markers=dict(Counter(c for n in notes for c in n['markers']));need(markers==dict(B=39,I=20,R=25,L=1,C=8,V=14),'sign inventory')
    new={n['id']:n for n in notes};changes=[];same=[]
    semantic=lambda n:{k:v for k,v in n.items() if k not in ['id','label','anchor','insert_after_codepoint']}
    for n in old['notes']:
        ident={'S24':'S25','S25':'S26'}.get(n['id'],n['id'])
        (same if semantic(n)==semantic(new[ident]) else changes).append(ident)
    need(len(same)==25 and sorted(changes)==sorted(side['rebase']['changed_existing_notes']),'all semantic deltas')
    need(new['S02']['lean']==next(n for n in old['notes'] if n['id']=='S02')['lean'],'exact old Lean scope')
    need(all(n['historical_novelty']=='not established' for n in notes if 'I' in n['markers']),'no unverified novelty')
    need(side['quantitative_factor'] is None and not side['previously_open_conjecture_cleared'],'scope limits')
    for n in notes:
        anchor=n['anchor'];snippet=text[anchor['start_codepoint']:anchor['end_codepoint_exclusive']]
        need(sha(snippet.encode())==anchor['sha256_utf8'] and snippet.startswith(anchor['exact_prefix']),'actual proof anchor '+n['id'])
        need(anchor['start_codepoint']<n['insert_after_codepoint']<=anchor['end_codepoint_exclusive'],'inside span '+n['id'])
    ledger=(p/'phase91_n009_annotations_ledger.md').read_text();recoveries={}
    for extension,pandoc in [('md',False),('pandoc.md',True)]:
        path=p/('phase91_n009_annotations_reader.'+extension);reader=path.read_text();start=reader.index(text.split('\n',1)[0]+'\n')
        need(reader.endswith('\n\n'+ledger),'complete ledger suffix');body=reader[start:-len('\n\n'+ledger)]
        # Reconstruct the annotated proof directly from untouched original spans.
        pieces=[];cursor=0;inserted=0
        for n in ordered:
            pos=n['insert_after_codepoint'];pieces.append(text[cursor:pos]);cursor=pos
            note='**'+' '.join('['+c+']' for c in n['markers'])+' — '+n['id']+'.** '+n['summary']
            insert=('\n\n::: {.audit-margin data-note="'+n['id']+'" data-codes="'+' '.join(n['markers'])+'"}\n'+note+'\n:::\n') if pandoc else '\n\n> '+note+'\n'
            pieces.append(insert);inserted+=len(insert)
        pieces.append(text[cursor:]);need(''.join(pieces)==body,'entire annotation weaving '+extension)
        # Strip in reverse at positions computed solely from source offsets.
        recovered=body;offsets=[];extra=0
        for n,insert in zip(ordered,pieces[1::2]):
            pos=n['insert_after_codepoint']+extra;offsets.append((pos,len(insert)));extra+=len(insert)
        for pos,length in reversed(offsets):recovered=recovered[:pos]+recovered[pos+length:]
        need(recovered.encode()==raw,'all bytes recovered '+extension)
        recoveries[extension]={'notes':41,'sha256':sha(recovered.encode()),'bytes':len(raw),'reader_sha256':sha(path.read_bytes())}
    for f,h in before.items():need(sha((p/f).read_bytes())==h,'input preserved '+f)
    result={'status':'PASS_INDEPENDENT_ANNOTATION_INTEGRITY','author_manifest_sha256':EXPECTED,'notes':41,'markers':markers,'semantic_unchanged':same,'semantic_changed':changes,'new_notes':side['rebase']['new_notes'],'recoveries':recoveries,'bindings_checked':len(before),'all_inputs_unchanged':True,'imports_author_code':False,'new_mathematical_or_Lean_replay':False,'PDF_layout_review':False,'twelve_factor':None}
    with a.output.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
    print(json.dumps(result))
if __name__=='__main__':main()
