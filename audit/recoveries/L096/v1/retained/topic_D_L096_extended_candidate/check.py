#!/usr/bin/env python3
"""Portable exact inputs, residue quantifiers, controls, optional finite replay.
No source table number is used to admit or reject an input geometry.
"""
import argparse,copy,hashlib,importlib.util,itertools,json,shutil,subprocess,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(ok,msg):
    if not ok:raise ValueError(msg)
def load_module(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m

def validate_rows(rows,inputs):
    expected={(name,i+1) for name,p in inputs.items() for i in range(len(p['rows']))}
    require(len(rows)==len(expected),'row count')
    require({(r['member'],r['active_row']) for r in rows}==expected,'row identities')
    residue_count=type_count=0
    for r in rows:
        src=inputs[r['member']];n=src['metadata']['rank'];I=set(range(1,n+1));a=r['active_row']
        require(r['construction_row']==src['metadata']['active_to_construction'][a-1],'final active archive order')
        require(r['rank']==n and not r['published_label_verified'],'rank/label boundary')
        require(r['computed_all_ranks'] is True,'uncomputed rank')
        expected_subsets={tuple(c) for k in range(n) for c in itertools.combinations(sorted(I),k)}
        require(len(r['residues'])==len(expected_subsets),'residue multiplicity')
        require({tuple(x['fixed_types']) for x in r['residues']}==expected_subsets,'all base residues')
        for x in r['residues']:
            rest=sorted(I-set(x['fixed_types']));k=len(rest);residue_count+=1
            require(x['types']==rest and x['residue_rank']==k,'residue type complement')
            require(x['flag_transitive'] is True,'orbit theorem without flag transitivity')
            require(x['order']*x['flag_orbit_size']==r['order'],'flag orbit size')
            require(x['extension_tests']==k*2**(k-1),'missing eligible extension')
            require(len(x['parabolic_orders'])==k,'parabolic ordering')
            require(x['primitive_checked_types']==rest[:len(x['primitive_types'])],'primitive prefix labels')
            require(len(x['primitive_types'])>0 and (any(x['primitive_types']) or len(x['primitive_types'])==k),'incomplete weak primitivity decision')
            if k>=2:
                require(len(x['type_results'])==k and all(type(t) is bool for t in x['type_results']),'every type tested')
                require(x['IP']==all(x['type_results']) and x['WIP']==any(x['type_results']),'local universal/existential type')
                require(len(x['negative_witnesses'])==sum(not t for t in x['type_results']),'negative witness for each failed type')
                require(sorted(w['type'] for w in x['negative_witnesses'])==[i for i,t in zip(rest,x['type_results']) if not t],'failure type mapping')
                type_count+=k
            else:require(x['firm']==(x['panel_size']>=2),'panel firmness')
        byrank=[]
        for k in range(2,n+1):
            rr=[x for x in r['residues'] if x['residue_rank']==k]
            byrank.append({'rank':k,'base_residues':len(rr),'actual_residues':sum(x['flag_orbit_size'] for x in rr),'IPk':all(x['IP'] for x in rr),'WIPk':all(x['WIP'] for x in rr)})
        require(r['by_rank']==byrank,'all-rank residue aggregation')
        panels=[x for x in r['residues'] if x['residue_rank']==1]
        filters={'flag_transitive':True,'firm':all(x['firm'] for x in panels),'residually_connected':all(x['connected'] for x in r['residues']),'RWPRI':all(any(x['primitive_types']) for x in r['residues']),'twoT1':all(x['two_transitive'] for x in panels),'IP2':byrank[0]['IPk']}
        require(r['filters']==filters and r['source_filter_pass']==all(filters.values()),'actual geometry filters')
        require(r['IP']==all(x['IPk'] for x in byrank) and r['WIP']==all(x['WIPk'] for x in byrank),'full property/all ranks')
    return {'rows':len(rows),'base_residues_including_panels':residue_count,'rank_at_least_two_type_decisions':type_count}

def signature(rows):
    result=[]
    for r in rows:
        z={k:r[k] for k in ['member','active_row','construction_row','order','rank','borel_order','parabolic_orders','filters','source_filter_pass','by_rank','IP','WIP']}
        z['residues']=[{k:x[k] for k in ['fixed_types','types','residue_rank','order','parabolic_orders','flag_orbit_size','flag_transitive','connected']+(['type_results','IP','WIP'] if x['residue_rank']>=2 else ['panel_size','firm','two_transitive'])} for x in r['residues']]
        result.append(z)
    return sorted(result,key=lambda r:(r['member'],r['active_row']))

def parse_log(path,prefix):
    raw=path.read_text().replace('\\\n','')
    require('Error,' not in raw and 'Syntax warning' not in raw,'GAP diagnostic')
    return [json.loads(x[len(prefix):]) for x in raw.splitlines() if x.startswith(prefix)]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',required=True);ap.add_argument('--out',required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--all-mathieu',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args();study=Path(a.study_root);out=Path(a.out);out.mkdir(parents=True,exist_ok=False)
    if (ROOT/'manifest.json').exists():
        for e in json.loads((ROOT/'manifest.json').read_text())['exports']:
            p=ROOT/e['path'];require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'frozen export '+e['path'])
    bindings=json.loads((ROOT/'bindings.json').read_text())
    for e in bindings['inputs']:
        p=study/e['path'];require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'external binding '+e['path'])
    prep=load_module('archive_parser',ROOT/'prepare_archive.py');inputs={}
    for folder,members in [('data_m11',['m11.rk3','m11.rk4']),('data_m12',['m12.rk3','m12.rk4','m12.rk5'])]:
        cmd=['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'prepare_archive.py'),'--archive',str(study/'sources/L096_supplementary_archive.tar'),'--out',str(out/folder),'--members',*members]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=30);require(p.returncode==0,p.stderr)
        for name in ['inputs.g','selected_inputs.json','archive_inventory.json']:require((out/folder/name).read_bytes()==(ROOT/folder/name).read_bytes(),'literal parse '+folder+'/'+name)
        inputs.update(json.loads((ROOT/folder/'selected_inputs.json').read_text()))
    rows=json.loads((ROOT/'mathieu_results.json').read_text())['rows'];summary=validate_rows(rows,inputs)
    receipt=json.loads((ROOT/'author_execution.json').read_text())
    retained=[]
    for e in receipt['mathematical_result_logs']:
        path=ROOT/e['path'];require(sha(path)==e['sha256'],'result receipt binding')
        retained+=parse_log(path,'RESULT|')
    require(signature(retained)==signature(rows),'retained finite program outputs')
    for e in receipt['executed_math_inputs']:
        require(sha(ROOT/e['path'])==e['sha256'],'actually executed mathematical input')
    controls=[]
    def reject(name,mutate):
        bad=copy.deepcopy(rows);mutate(bad)
        try:validate_rows(bad,inputs)
        except (ValueError,KeyError,IndexError,TypeError):controls.append(name);return
        raise ValueError('control accepted: '+name)
    reject('drop_geometry',lambda rr:rr.pop())
    reject('ignore_final_geo_reorder',lambda rr:rr[0].update(construction_row=1))
    reject('invent_published_label',lambda rr:rr[0].update(published_label_verified=True))
    reject('omit_rank_two_residue',lambda rr:rr[0]['residues'].pop())
    reject('wrong_remaining_types',lambda rr:rr[0]['residues'][0].update(types=[1]))
    reject('omit_eligible_extension',lambda rr:rr[0]['residues'][0].update(extension_tests=0))
    reject('drop_flag_transitivity',lambda rr:rr[0]['residues'][0].update(flag_transitive=False))
    reject('replace_full_weak_by_top_rank',lambda rr:rr[0].update(WIP=not rr[0]['WIP']))
    reject('ignore_source_filters',lambda rr:next(r for r in rr if not r['source_filter_pass']).update(source_filter_pass=True))
    reject('omit_negative_witness',lambda rr:next(x for r in rr for x in r['residues'] if x.get('negative_witnesses'))['negative_witnesses'].pop())
    # Grammar controls do not execute source code or infer labels from comments.
    sample='g:=G;geo:=[];geosub:=[];h:=sub<g|(1,2)>;h:=sub<g|(2,3)>;Append(~geo,geosub);geo:=[geo[1]];/*geo:=[geo[9]];*/'
    m,_=prep.parse(sample.encode(),'m11.rk2');require(m['active_to_construction']==[1],'commented selection');controls.append('commented_selection_ignored')
    for name,s in [('nonliteral_expression',sample.replace('(1,2)','System(1)')),('invalid_selection',sample.replace('geo:=[geo[1]]','geo:=[geo[2]]'))]:
        try:prep.parse(s.encode(),'m11.rk2')
        except ValueError:controls.append(name)
        else:raise ValueError('parser accepted '+name)
    execution=[]
    if a.programs:
        for f in ['shadow_residues.g','run_m11.g','run_m12.g','run_m12_batch.g','small_models.g','identify.g','panel_failure.g']:shutil.copyfile(ROOT/f,out/f)
        batch_scripts=[]
        if a.all_mathieu:
            for first,last in [(1,10),(11,20),(21,30),(31,38),(39,39),(40,40),(41,41)]:
                name=f'm12_batch_{first}_{last}.g'
                (out/name).write_text(f'L096First:={first};;L096Last:={last};;Read("run_m12_batch.g");;\n')
                batch_scripts.append(name)
        for script in ['identify.g','run_m11.g']+batch_scripts+['small_models.g','panel_failure.g']:
            t=time.monotonic()
            with (out/(script+'.stdout.log')).open('w') as so,(out/(script+'.stderr.log')).open('w') as se:p=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',script],cwd=out,stdout=so,stderr=se,timeout=480)
            require(p.returncode==0,'GAP exit');raw=(out/(script+'.stdout.log')).read_text();err=(out/(script+'.stderr.log')).read_text();require('Error,' not in raw and not err and 'PASS_' in raw,'GAP completion');execution.append({'script':script,'seconds':time.monotonic()-t})
        recomputed=parse_log(out/'run_m11.g.stdout.log','RESULT|')
        for name in batch_scripts:recomputed+=parse_log(out/(name+'.stdout.log'),'RESULT|')
        want=[r for r in rows if a.all_mathieu or r['member'].startswith('m11')]
        require(signature(recomputed)==signature(want),'fresh mathematical signatures')
        p=subprocess.run(['/Users/sasha/.venvs/global/bin/python','-B','-O',str(ROOT/'check_small_models.py'),'--log',str(out/'small_models.g.stdout.log'),'--out',str(out/'small_oracle.json')],capture_output=True,text=True,timeout=60);require(p.returncode==0,p.stderr)
    if a.render:
        from pypdf import PdfReader
        shutil.copyfile(ROOT/'residue_shadows.tex',out/'residue_shadows.tex')
        for j in range(2):
            p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','residue_shadows.tex'],cwd=out,capture_output=True,text=True,timeout=60);(out/f'render{j}.log').write_text(p.stdout+p.stderr);require(p.returncode==0,'render')
        require(not any(x in p.stdout for x in ['Overfull','undefined','Missing character']),'render diagnostics')
        require([p.extract_text() for p in PdfReader(out/'residue_shadows.pdf').pages]==[p.extract_text() for p in PdfReader(ROOT/'residue_shadows.pdf').pages],'exact scientific page text')
    report={'status':'PASS','scope':'65 literal active Mathieu inputs; complete residue quantifiers and actual geometry filters. No published row labels or full L096 recovery.','coverage':summary,'integrity_and_quantifier_controls':controls,'fresh_programs':execution,'source_archives_reparsed':5,'full_source_credit':0,'measurement_factor':None};(out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
