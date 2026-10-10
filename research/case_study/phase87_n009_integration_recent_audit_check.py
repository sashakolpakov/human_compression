#!/usr/bin/env python3
"""Independent read-only phase78 binding/transcription/output-coverage checks.

This supplements the full human-style mathematical/code review and fresh GAP
replay. It neither repeats the census nor establishes its mathematics by hashes.
Private primary snapshots are required. Writes one new JSON file only.
"""
import argparse
from collections import Counter
import hashlib
from html import unescape
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parent
EXPECTED_MANIFEST='0705f2e8a1f27cc3f60a92a4076c4edcb98b4324fb6273232db1df0e7c1ea72a'
EXPECTED_MANUSCRIPT='15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def require(condition,label):
    if not condition:raise ValueError(label)
def read(path):return json.loads(path.read_text())
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-root',type=Path,default=ROOT)
    ap.add_argument('--replay-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();root=a.input_root;out=a.output;replay=a.replay_dir
    require(not out.exists(),'Refusing existing output')
    manifest=root/'phase78_n009_integration_manifest.json'
    require(digest(manifest)==EXPECTED_MANIFEST,'Frozen manifest hash')
    mf=read(manifest)
    for b in mf['files']:require(digest(root/b['path'])==b['sha256'],'Frozen file '+b['path'])
    manuscript=root/'phase78_n009_integration_manuscript.md';require(digest(manuscript)==EXPECTED_MANUSCRIPT,'Manuscript hash')
    m=manuscript.read_text();prior=(root/'phase65_petrial_integration_manuscript.md').read_text()
    ledger=read(root/'phase78_n009_integration_ledger.json');oldledger=read(root/'phase65_petrial_integration_ledger.json')
    require(len(ledger['contracts'])==120,'Complete contracts')
    mapped={r['integration_id']:r for r in ledger['contracts']};require(len(mapped)==120,'Unique contract IDs')
    for r in oldledger['contracts']:
        old=r['integrated_proof_span'];new=mapped[r['integration_id']]['integrated_proof_span']
        require(prior[old['start_codepoint']:old['end_codepoint_exclusive']]==m[new['start_codepoint']:new['end_codepoint_exclusive']],'Prior actual proof-span continuity')
    newrows=[r for r in ledger['contracts'] if r.get('paper')=='N009']
    require(len(newrows)==33 and sum(r['source_reference'].startswith('Table ') for r in newrows)==6,'27 statements and six tables')
    sections=lambda text:{int(match[1]):match[0] for match in re.finditer(r'^## (\d+)\. .*?(?=^## |\Z)',text,re.M|re.S)}
    oldsec=sections(prior);newsec=sections(m)
    unchanged=[n for n in range(1,24) if oldsec[n]==newsec[n]]
    require(unchanged==[3,4,5,6,7,8,9,10,12,14,15,16,17,18,19,20,21,22,23],'Nineteen full unchanged sections')
    blocks=re.findall(r'^```(gap|python)\n(.*?)^```',m,re.M|re.S)
    oldblocks=re.findall(r'^```(gap|python)\n(.*?)^```',prior,re.M|re.S)
    require(len(blocks)==8 and blocks[1:5]==oldblocks[1:5],'Complete old/new code continuity')
    for i,name in [(0,'census.g'),(5,'finite.g'),(6,'data.g'),(7,'run.py')]:
        require(blocks[i][1]==(root/('phase78_n009_integration_'+name)).read_text(),'Complete new printed input '+name)
    require('after reversing its endpoints and conjugating all three generators by b' in m,'Explicit square marking conversion')
    require(not any(x.get('id')=='B-retained-6' for x in ledger['retained_background']['Unified']),'Old catalogue input removed')
    # Parse each complete Atlas defining presentation afresh, without importing
    # the author's HTML parser or executable GAP data.
    data=(root/'phase78_n009_integration_data.g').read_text()
    models={}
    for hit in re.finditer(r'rec\(label:=("[^"]+"),order:=(\d+),typ:=(\[[^\n]+?\]),words:=(\[[^\n]+\])\)',data):
        label=json.loads(hit[1]);require(label not in models,'Unique model label')
        models[label]={'order':int(hit[2]),'type':json.loads(hit[3]),'words':json.loads(hit[4])}
    require(len(models)==72,'All 72 defining models')
    primary=read(root/'phase78_n009_integration_intake.json')['primary_assets'];word_count=0;source_bindings=[]
    for item in primary:
        path=root/item['path'];require(digest(path)==item['sha256'],'Private primary hash '+item['path'])
        source_bindings.append({'path':item['path'],'sha256':item['sha256']})
        if 'label' not in item:continue
        html=path.read_text();pres=[unescape(x) for x in re.findall(r'<pre\b[^>]*>(.*?)</pre>',html,re.S|re.I)]
        matches=[re.search(r'\brels\s*:=\s*\[(.*?)\]',x,re.S) for x in pres]
        matches=[x for x in matches if x];require(len(matches)==1,'One complete relator block')
        words=[]
        for raw in matches[0][1].split(','):
            raw=raw.strip();require(re.fullmatch(r's\d+(?:\s*\*\s*s\d+)*',raw) is not None,'Literal primary word grammar')
            words.append(''.join(str(int(n)+1) for n in re.findall(r's(\d+)',raw)))
        model=models[item['label']];require(model['words']==words,'All exact defining words '+item['label'])
        name=re.search(r'Atlas Canonical Name\s*<span[^>]*>(.*?)</span>',html,re.S)
        require(name is not None and unescape(name[1]).strip()==item['label'],'Canonical primary name')
        lab=re.fullmatch(r'\{([\d,]+)\}\*(\d+)[a-z]?',item['label'])
        require(lab is not None and list(map(int,lab[1].split(',')))==model['type'] and int(lab[2])==model['order'],'Named type/order')
        require(all(set(w)<=set('1234'[:len(model['type'])+1]) for w in words),'Generator index scope')
        word_count+=len(words)
    # Complete classification output coverage, including every table6 row and
    # every accepted high-rank marking, independently of the author's runner.
    report=read(replay/'phase78_n009_integration_run.json')
    require(report['status']=='PASS','Fresh mathematical replay status')
    require(report['software']=={'GAP':'4.15.1','NQ':'2.5.11'},'Exact current replay toolchain')
    for b in report['inputs']:
        require(digest(root/b['path'])==b['sha256']==digest(replay/b['path']),'Fresh replay program binding')
    for b in report['outputs']:require(digest(replay/b['path'])==b['sha256'],'Fresh replay output binding')
    rows=json.loads(re.search(r'rows78:=(\[.*\])\s*;;',data,re.S)[1])
    require(len(rows)==107,'107 source data rows')
    get=lambda suffix:read(replay/('phase78_n009_integration_'+suffix+'.json'))
    dual=dict(get('duals'));require(all(dual.get(v)==k for k,v in dual.items()),'Dual-name involution')
    canon=lambda pair:min(tuple(pair),(dual[pair[1]],dual[pair[0]]))
    rowmap={canon(r[0]):r for r in rows};require(len(rowmap)==107,'Distinct source end-pair orbits')
    facets=get('facet_matches');require(len(facets)==214,'199+15 full higher-rank ordered markings')
    require(all(canon(r[2]) in rowmap for r in facets),'Every accepted higher-rank marking covered by source rows')
    independently_counted=[]
    for key,row in rowmap.items():
        hits=[r for r in facets if canon(r[2])==key];fixed=sum(r[3] for r in hits)
        require((len(hits)+fixed)%2==0 and (len(hits)+fixed)//2==row[2],'Every reversal row count')
        require(all(min(r[1],r[1][::-1])==min(row[3],row[3][::-1]) for r in hits),'Every row type')
        independently_counted.append({'pair':list(key),'ordered':len(hits),'fixed':fixed,'classes':(len(hits)+fixed)//2})
    require(sum(x['classes'] for x in independently_counted)==113,'All 105+8 high-rank classes covered')
    require(sum(r[2] for r in rows if len(r[3])==3)==105 and sum(r[2] for r in rows if len(r[3])==4)==8,'Separate rank totals')
    universals=get('universal_orders');require(len(universals)==106,'All finite universal rows')
    require(Counter(x[1] for x in universals)=={1024:101,2048:5},'Exact finite universal histogram')
    require({tuple(x[0]):x[1] for x in universals}=={tuple(r[0]):r[1] for r in rows if r[1]},'Every finite universal order linked to its exact row')
    require([r for r in rows if r[1]==0]==[[['{4,4}*128','{4,4}*64'],0,2,[4,4,4]]],'Sole retained infinite row')
    expected5=[((4,4),1),((4,8),8),((4,16),14),((4,32),4),((4,64),2),((4,128),2),((8,8),22),((8,16),40),((8,32),8),((8,64),4),((16,16),10),((16,32),10)]
    accepted3=read(replay/'phase78_d3_k5.accepted.json');actual5=[]
    for typ,count in expected5:
        hits=[r for r in accepted3 if min(tuple(r[1]),tuple(reversed(r[1])))==typ]
        require((len(hits)+sum(r[4] for r in hits))//2==count,'All Table5 type counts')
        actual5.append({'type':typ,'classes':count})
    require(sum(x[1] for x in expected5)==125 and len(accepted3)==235 and sum(r[4] for r in accepted3)==15,'Complete rank3 totals')
    seeds=read(replay/'phase78_d3_k3.seed.json');require(len(seeds)==4 and sorted(x[1] for x in seeds)==[1,2,3,4],'All exact seed patterns')
    require(get('table4_literal_matches')==[[1,1],[2,2],[3,3],[4,4],[5,3],[6,1],[7,7],[8,3]],'Exact literal Table4 discrepancy')
    require(len(get('all_presentations'))==214,'All raw finite presentations')
    result={'status':'PASS','scope':'Independent hash/transcription/coverage checks supplement complete proof/code reading and fresh exact GAP replay; no proof-by-hash claim',
      'reviewed_manifest_sha256':EXPECTED_MANIFEST,'reviewed_manuscript_sha256':EXPECTED_MANUSCRIPT,
      'prior_source_adapters_byte_identical':87,'unchanged_full_sections':unchanged,'complete_code_blocks':8,
      'new_source_numbered_items':27,'new_source_tables':6,'independently_parsed_primary_models':72,'independently_parsed_complete_defining_words':word_count,
      'primary_bindings':source_bindings,'all214_high_rank_markings_covered':True,'table6_independent_counts':independently_counted,
      'table5_independent_counts':actual5,'total_high_rank_classes':113,'total_rank3_classes':125,
      'full_finite_universal_rows_checked':106,'finite_universal_orders':{'1024':101,'2048':5},'retained_infinite_row':True,
      'frozen_source_or_author_files_modified':False,'no_new_Lean_or_ratio_or_priority_claim':True}
    with out.open('x',encoding='utf8') as f:json.dump(result,f,indent=2,ensure_ascii=False);f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['primary_bindings','table6_independent_counts','table5_independent_counts']}))
if __name__=='__main__':main()
