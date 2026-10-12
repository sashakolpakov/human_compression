#!/usr/bin/env python3
"""Portable replay and weakening controls; old full enumerations are reused."""
import argparse
import copy
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path
import certificate
import weights


def need(test,message):
    if not test:
        raise ValueError(message)


def run(command,cwd,log,marker=None):
    p=subprocess.run(list(map(str,command)),cwd=cwd,text=True,capture_output=True,timeout=120)
    s=p.stdout+p.stderr;log.write_text(s)
    need(p.returncode==0 and 'Error,' not in s,'failed command: '+repr(command))
    need(marker is None or marker in s,'missing success marker')
    return p.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path);p.add_argument('--gap',default='/opt/homebrew/bin/gap')
    p.add_argument('--cc',default='cc');p.add_argument('--render',action='store_true');p.add_argument('--pdflatex',default='pdflatex')
    a=p.parse_args();root=Path(__file__).resolve().parent
    if (root/'manifest.json').exists():
        for row in json.loads((root/'manifest.json').read_text())['exports']:
            f=root/row['path'];need(f.is_file()and f.stat().st_size==row['bytes']and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],'frozen export '+row['path'])
    binding=json.loads((root/'bindings.json').read_text())
    if a.study_root:
        for row in binding['inputs']:
            f=a.study_root/row['path'];need(f.is_file()and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],'external binding '+row['path'])
    for name,sha in binding['retained_copies'].items():
        need(hashlib.sha256((root/'retained'/name).read_bytes()).hexdigest()==sha,'retained copy '+name)
    prior={x['path']:x for x in json.loads((root/'retained/enumeration_manifest.json').read_text())['exports']}
    for name in ['105_adjacency.json','105_differences.json','bases/105_adjacency.txt','bases/105_differences.txt','receipt.json']:
        need(hashlib.sha256((root/'retained'/name).read_bytes()).hexdigest()==prior[name]['sha256'],'enumeration manifest cross-binding '+name)
    need(hashlib.sha256((root/'steiner_construction.py').read_bytes()).hexdigest()==prior['method/check_graph_codes.py']['sha256'],'complete shared construction')
    distance={x['path']:x for x in json.loads((root/'retained/distance_author_manifest.json').read_text())['exports']}
    need(hashlib.sha256((root/'enumerate_sparse_messages.c').read_bytes()).hexdigest()==distance['enumerate_sparse_messages.c']['sha256'],'complete shared sparse enumerator')
    inventory=json.loads((root/'program_inventory.json').read_text())
    for row in inventory['required_math_files']+inventory['required_data']:
        f=root/row['path'];need(f.stat().st_size==row['bytes']and hashlib.sha256(f.read_bytes()).hexdigest()==row['sha256'],'whole program/data inventory '+row['path'])
    contexts=json.loads((root/'proof_contexts.json').read_text());tex=(root/'modules.tex').read_text()
    need(hashlib.sha256(tex.encode()).hexdigest()==contexts['tex_sha256'],'written proof binding')
    lines=tex.splitlines(keepends=True)
    for row in contexts['contexts']:
        need(hashlib.sha256(''.join(lines[row['start_line']-1:row['end_line']]).encode()).hexdigest()==row['sha256'],'proof context '+row['id'])
    out=a.out.resolve();out.mkdir(parents=True,exist_ok=False)
    data=json.loads((root/'module_data.json').read_text());retained=root/'retained'
    result=certificate.inspect(data,retained,out/'certificate')
    run([a.gap,'-q','-b','-T',out/'certificate/constructed.g',root/'identify_modules.g'],out/'certificate',out/'module.log','LCD105_MODULES_PASS')
    tables=json.loads((root/'source_tables.json').read_text())
    weight_results={}
    for name,k,label in [('adjacency',20,'C'),('differences',19,'D')]:
        weight_results[label]=weights.full(json.loads((retained/f'105_{name}.json').read_text()),k,tables[label])
    (out/'complete_weights.json').write_text(json.dumps(weight_results,indent=2)+'\n')
    run([a.cc,'-O3',root/'enumerate_sparse_messages.c','-o',out/'sparse'],out,out/'compile.log')
    extra=[];restricted_records=[]
    for candidate in result['extra_codes_pending_distance_enumeration']:
        i=candidate['id'];s=run([out/'sparse',out/f'certificate/extra{i}_basis.txt'],out,out/f'extra{i}.log')
        record=json.loads(s);restricted_records.append(record)
        (out/f'extra{i}.json').write_text(json.dumps(record,indent=2)+'\n')
        extra.append(weights.restricted(record,candidate))
    controls=[]
    mutations=[]
    d=copy.deepcopy(data);d['minimum33_seeds'].pop();mutations.append(('missing minimum orbit',d,'complete retained minimum33 count'))
    d=copy.deepcopy(data);d['coordinate_generators'][0][0]=d['coordinate_generators'][0][1];mutations.append(('nonpermutation generator',d,'permutation generators'))
    d=copy.deepcopy(data);d['filtration_basis'][0]=d['filtration_basis'][1][:];mutations.append(('singular filtration',d,'filtration basis nonsingular'))
    d=copy.deepcopy(data);d['polynomial']=[0];mutations.append(('zero rank-one witness',d,'rank-one algebra element'))
    d=copy.deepcopy(data);d['code20_bases'][2]=d['code20_bases'][1];mutations.append(('duplicate20-module',d,'distinct simple submodules'))
    for i,(name,changed,message)in enumerate(mutations):
        try:certificate.inspect(changed,retained,out/f'mutation{i}')
        except (ValueError,RuntimeError)as e:
            need(message in str(e),'wrong mutation failure '+name+': '+str(e));controls.append({'name':name,'rejected_at':str(e)})
        else:raise ValueError('mutation accepted '+name)
    changed=copy.deepcopy(restricted_records[0]);changed['restricted_weight_counts'][30]+=2
    donor=next(i for i in range(31,106)if changed['restricted_weight_counts'][i]>=2)
    changed['restricted_weight_counts'][donor]-=2
    try:weights.restricted(changed,result['extra_codes_pending_distance_enumeration'][0])
    except ValueError as e:
        need('restricted distance and minimum-set exhaustion' in str(e),'wrong restricted rejection');controls.append({'name':'wrong minimum-orbit exhaustion count','rejected_at':str(e)})
    else:raise ValueError('wrong restricted count accepted')
    for k in [1,2,3,4]:
        n=7;B=[[int(j==i)if j<k else(i+2*j+1)%3 for j in range(n)]for i in range(k)]
        f=out/f'small{k}.txt';f.write_text(f'{n} {k} 3 {min(k,3)}\n'+''.join(''.join(map(str,row))+'\n'for row in B))
        record=json.loads(run([out/'sparse',f],out,out/f'small{k}.log'))
        expected=[0]*(n+1)
        for coeff in itertools.product(range(3),repeat=k):
            if sum(x!=0 for x in coeff)>min(k,3):continue
            w=sum(sum(coeff[i]*B[i][j]for i in range(k))%3!=0 for j in range(n));expected[w]+=1
        need(record['restricted_weight_counts']==expected,'literal sparse arithmetic')
        controls.append({'name':f'literal ternary oracle dimension{k}','status':'PASS'})
    if a.render:
        render=out/'render';render.mkdir()
        for i in range(2):log=run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(render),root/'modules.tex'],root,out/f'render{i}.log')
        need(not any(s in log for s in ['Overfull','Missing character','undefined references']),'render diagnostics')
    report={'status':'PASS','scope':'bounded L050105-coordinate obligations','certificate':result,
            'identification':json.loads((out/'certificate/module_identification.json').read_text()),
            'main_weights':{k:{x:y for x,y in v.items()if x!='full_dual_distribution'}for k,v in weight_results.items()},
            'additional_codes':extra,'controls':controls,'rendered':a.render,'external_bindings_checked':bool(a.study_root),
            'full_enumerations_repeated':False,'whole_source_admission':False}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','controls':len(controls),'additional_codes':extra},sort_keys=True))


if __name__=='__main__':main()
