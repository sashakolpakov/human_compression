#!/usr/bin/env python3
"""Separate author integrity/negative controls; no annotation-engine imports."""
import argparse
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

BASE = Path(__file__).resolve().parent
PREFIX = 'phase91_n009_annotations'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def need(test, message):
    if not test:
        raise ValueError(message)


def bindings(value):
    if isinstance(value, dict):
        if {'path','sha256','bytes'} <= value.keys():
            yield value
        for child in value.values():
            yield from bindings(child)
    elif isinstance(value, list):
        for child in value:
            yield from bindings(child)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--study-root',type=Path,default=BASE)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args();base=args.study_root.resolve();out=args.output_dir
    need(not out.exists() and not out.is_symlink(),'output exists; refusing overwrite')
    sidepath=base/(PREFIX+'.json');side=json.loads(sidepath.read_text())
    bound={x['path']:x for x in bindings(side)}
    before={name:sha((base/name).read_bytes()) for name in bound}
    for name,s in bound.items():
        need(before[name]==s['sha256'] and (base/name).stat().st_size==s['bytes'],'binding '+name)
    original=(base/side['manuscript']['path']).read_bytes();text=original.decode()
    need(len(original)==317916 and sha(original)=='15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801','original proof')
    notes=side['notes'];need(len(notes)==41,'notes')
    markers=dict(Counter(c for row in notes for c in row['markers']))
    need(markers==dict(B=39,C=8,I=20,L=1,R=25,V=14),'marker inventory')
    for row in notes:
        a=row['anchor'];snippet=text[a['start_codepoint']:a['end_codepoint_exclusive']]
        need(sha(snippet.encode())==a['sha256_utf8'] and snippet.startswith(a['exact_prefix']),'anchor '+row['id'])
        need(a['start_codepoint']<row['insert_after_codepoint']<=a['end_codepoint_exclusive'],'insertion')
        need('I' not in row['markers'] or row['historical_novelty']=='not established','novelty')
    old=json.loads((base/'phase79_eleven_attribution.json').read_text())
    semantic=lambda row:{k:v for k,v in row.items() if k not in ['id','label','anchor','insert_after_codepoint']}
    current={r['id']:r for r in notes};changed=[];unchanged=[]
    for row in old['notes']:
        ident={'S24':'S25','S25':'S26'}.get(row['id'],row['id'])
        (unchanged if semantic(row)==semantic(current[ident]) else changed).append(ident)
    need(set(changed)==set(side['rebase']['changed_existing_notes']),'semantic change inventory')
    need(len(unchanged)==25,'unchanged meanings')
    added=set(current)-{ {'S24':'S25','S25':'S26'}.get(r['id'],r['id']) for r in old['notes']}
    need(added==set(side['rebase']['new_notes']),'added notes')
    need(current['S02']['lean']==next(r for r in old['notes'] if r['id']=='S02')['lean'],'inherited Lean scope')
    ordered=sorted(notes,key=lambda r:(r['insert_after_codepoint'],r['id']))
    ledger=(base/(PREFIX+'_ledger.md')).read_text()
    suffix='\n\n'+ledger
    recoveries={}
    for ext,pandoc in [('md',False),('pandoc.md',True)]:
        reader=(base/(PREFIX+'_reader.'+ext)).read_text()
        start=reader.index('# Marked kernels, coordinates and geometric recognition\n')
        need(reader.endswith(suffix),'ledger suffix')
        body=reader[start:-len(suffix)];cursor=0;chunks=[]
        for row in ordered:
            signs=' '.join('['+s+']' for s in row['markers'])
            note='**'+signs+' — '+row['id']+'.** '+row['summary']
            if pandoc:
                insert='\n\n::: {.audit-margin data-note="'+row['id']+'" data-codes="'+' '.join(row['markers'])+'"}\n'+note+'\n:::\n'
            else:
                insert='\n\n> '+note+'\n'
            index=body.find(insert,cursor);need(index>=cursor,'written note missing')
            chunks.append(body[cursor:index]);cursor=index+len(insert)
            need(sum(len(c) for c in chunks)==row['insert_after_codepoint'],'actual insertion position')
        chunks.append(body[cursor:]);recovered=''.join(chunks).encode()
        need(recovered==original,'stripped proof')
        recoveries[ext]=dict(bytes=len(recovered),sha256=sha(recovered))
    out.mkdir()
    commands=[]
    def run(label,argv,expect=0,needle=None):
        r=subprocess.run(argv,capture_output=True,text=True)
        need((r.returncode==0)==(expect==0),'exit '+label)
        if needle:need(needle in r.stdout+r.stderr,'negative diagnostic '+label)
        commands.append(dict(label=label,argv=argv,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
        return r
    rebuilt=out/'sidecar.json'
    run('fresh sidecar',[sys.executable,'-O',str(base/(PREFIX+'_build.py')),'--study-root',str(base),'--output',str(rebuilt)])
    need(rebuilt.read_bytes()==sidepath.read_bytes(),'rebuilt sidecar')
    fresh=out/'reader'
    argv=[sys.executable,'-O',str(base/(PREFIX+'_generate.py')),'--study-root',str(base),'--output-dir',str(fresh)]
    run('fresh readers',argv)
    for src,dest in [('reader.md','reader.md'),('reader.pandoc.md','reader.pandoc.md'),('ledger.md','ledger.md'),('report.json','check.json')]:
        need((fresh/src).read_bytes()==(base/(PREFIX+'_'+dest)).read_bytes(),'generated '+src)
    snapshot={p.name:sha(p.read_bytes()) for p in fresh.iterdir() if p.is_file()}
    run('existing reader refusal',argv,1,'output directory exists')
    need(snapshot=={p.name:sha(p.read_bytes()) for p in fresh.iterdir() if p.is_file()},'reader files clobbered')
    run('existing sidecar refusal',[sys.executable,'-O',str(base/(PREFIX+'_build.py')),'--output',str(rebuilt)],1,'output exists')
    need(rebuilt.read_bytes()==sidepath.read_bytes(),'sidecar clobbered')
    for label,change in [('stale_anchor',lambda d:d['notes'][0]['anchor'].update(sha256_utf8='0'*64)),('wrong_proof',lambda d:d['manuscript'].update(sha256='0'*64)),('unauthorized_M',lambda d:d['notes'][0]['markers'].append('M')),('unauthorized_O',lambda d:d['notes'][0]['markers'].append('O'))]:
        bad=copy.deepcopy(side);change(bad);path=out/(label+'.json');path.write_text(json.dumps(bad))
        target=out/(label+'_should_not_exist')
        run(label,[sys.executable,'-O',str(base/(PREFIX+'_generate.py')),'--study-root',str(base),'--sidecar',str(path),'--output-dir',str(target)],1)
        need(not target.exists(),'adverse output created')
    latex=run('Lua margin control',['pandoc',str(base/(PREFIX+'_reader.pandoc.md')),'--from=markdown+tex_math_single_backslash-raw_tex','--to=latex','--lua-filter='+str(base/'phase79_eleven_attribution_margins.lua')])
    need(latex.stdout.count('\\marginpar{')==41,'margin command count')
    after={name:sha((base/name).read_bytes()) for name in bound}
    need(before==after,'changed input')
    report=dict(status='PASS_AUTHOR_INTEGRITY_CONTROLS',checker_sha256=sha(Path(__file__).read_bytes()),
                notes=41,markers=markers,semantic_changed=changed,semantic_unchanged=unchanged,new_notes=sorted(added),
                exact_reader_recoveries=recoveries,bound_input_hashes=before,all_inputs_unchanged=True,
                fresh_sidecar_and_readers_byte_identical=True,existing_reader_files_preserved=len(snapshot),
                all_adverse_tests_rejected_before_output=True,lua_margin_commands=41,
                optimized_python=True,independent_semantic_review=False,new_mathematical_replay=False,
                new_Lean_build=False,PDF_typesetting_or_visual_review=False,twelve_source_factor=None,
                commands=[{k:v for k,v in row.items() if k!='stdout'} if row['label']=='Lua margin control' else row for row in commands])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','notes','markers','existing_reader_files_preserved','lua_margin_commands','twelve_source_factor']},indent=2))


if __name__=='__main__':
    main()
