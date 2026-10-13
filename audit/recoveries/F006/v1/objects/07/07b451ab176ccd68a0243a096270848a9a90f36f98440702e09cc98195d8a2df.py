#!/usr/bin/env python3
"""Portable bindings/native rendering only; no acquired finite or Lean rerun."""
from pathlib import Path
import argparse, copy, hashlib, json, shutil, subprocess
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent

def require(c, m):
    if not c:
        raise ValueError(m)

def load(p):
    return json.loads(p.read_text())

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def binding(root, b, key='path'):
    p = root / b[key]
    require(p.is_file() and p.stat().st_size == b['bytes'] and sha(p) == b['sha256'], 'binding ' + b[key])

def scope_check(s, d, inventory):
    require(s['domain'] == {'odd_n_minimum':5,'even_n_minimum':6}, 'parameter endpoints')
    require(s['upper_bounds']['even_string_involutions'] == 'at most n-1, including disconnected strings', 'even upper scope')
    require(s['existence'] == {'odd_n':'all ranks 3 through n','even_n':'all ranks 3 through n-1'}, 'rank intervals')
    require(s['whole_original_credit'] == s['new_question_credit'] == s['new_Lean_declarations'] == s['new_finite_searches'] == 0, 'bounded credit')
    require(s['new_factor'] is None and not s['full_formalization'], 'no factor/formal claim')
    require(d['full_external_proof_costs'] is None, 'external costs retained')
    required = [x for x in inventory['whole_files'] if x['current_role'] == 'required_complete_S5_S6_search']
    require(len(required) == 1 and required[0]['path'].endswith('/small_extremal.g'), 'whole finite premise')
    require(any(x['current_role']=='required_saved_finite_results' and x['path'].endswith('/finite_results.json') for x in inventory['whole_files']), 'whole finite data')

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--out', type=Path, required=True)
    p.add_argument('--render', action='store_true')
    p.add_argument('--study-root', type=Path)
    p.add_argument('--public-root', type=Path)
    p.add_argument('--pdflatex', default='/opt/homebrew/bin/pdflatex')
    p.add_argument('--pdftotext', default='/opt/homebrew/bin/pdftotext')
    a = p.parse_args(); a.out.mkdir(parents=True, exist_ok=False)
    m = load(ROOT/'manifest.json')
    for b in m['exports']:
        binding(ROOT,b)
    copies = load(ROOT/'copy_map.json')['files']
    for b in copies:
        binding(ROOT,b,'target')
        if a.public_root:
            binding(a.public_root,b,'source')
    source = load(ROOT/'source.json')
    if a.study_root:
        binding(a.study_root,source)
        require(len(PdfReader(a.study_root/source['path']).pages)==13,'source pages')
    inventory = load(ROOT/'program_inventory.json')
    for b in inventory['whole_files']:
        binding(ROOT,b)
    s=load(ROOT/'scope.json');d=load(ROOT/'dependencies.json')
    scope_check(s,d,inventory)
    rows=load(ROOT/'source_map.json')['rows']
    require(len(rows)==20 and len({r['id'] for r in rows})==20,'twenty unique bounded routes')
    require(next(r for r in rows if r['id']=='F006.L19')['status']=='RECOVERED_WITH_INTERMEDIATE_INTERSECTION_CORRECTION','literal source correction')
    inherited=[]
    omissions=load(ROOT/'nested_manifest_scope.json')
    for mp in sorted((ROOT/'retained').rglob('manifest.json')):
        absent=[];checked=0
        for b in load(mp)['exports']:
            if (mp.parent/b['path']).is_file():
                binding(mp.parent,b);checked+=1
            else:
                absent.append(b['path'])
        expected=omissions.get(str(mp.relative_to(ROOT)),[])
        require(absent==expected,'only expressly inherited non-invoked omissions')
        inherited.append({'manifest':str(mp.relative_to(ROOT)),'exports_checked':checked,'noninvoked_historical_exports_not_copied':absent})
    controls=[]
    mutations=[('odd_endpoint',lambda x:x['domain'].update(odd_n_minimum=3)),('even_endpoint',lambda x:x['domain'].update(even_n_minimum=4)),('whole_credit',lambda x:x.update(whole_original_credit=1)),('new_factor',lambda x:x.update(new_factor=1)),('formal_claim',lambda x:x.update(full_formalization=True)),('even_rank_n',lambda x:x['existence'].update(even_n='all ranks 3 through n'))]
    for name,mutate in mutations:
        bad=copy.deepcopy(s);mutate(bad)
        try:scope_check(bad,d,inventory)
        except ValueError:controls.append(name)
        else:raise ValueError('accepted false scope '+name)
    bad=copy.deepcopy(inventory);bad['whole_files']=[x for x in bad['whole_files'] if x['current_role']!='required_complete_S5_S6_search']
    try:scope_check(s,d,bad)
    except ValueError:controls.append('dropped_required_search')
    else:raise ValueError('accepted missing search')
    texts=[]
    for doc in load(ROOT/'manuscripts.json'):
        require(sha(ROOT/doc['tex'])==doc['tex_sha256'] and sha(ROOT/doc['pdf'])==doc['pdf_sha256'],'native manuscript pin')
        require(len(PdfReader(ROOT/doc['pdf']).pages)==doc['pages'],'native page count')
        rec={'tex':doc['tex'],'pages':doc['pages'],'rendered':False}
        if a.render:
            stem=Path(doc['tex']).stem;out=a.out/stem;out.mkdir()
            for i in range(2):
                r=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(out),doc['tex']],cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
                (out/f'pass{i}.log').write_text(r.stdout);require(r.returncode==0,'native TeX compile')
            log=(out/f'{stem}.log').read_text()
            require('Overfull' not in log and 'undefined references' not in log and 'LaTeX Warning:' not in log,'clean native diagnostics')
            pdf=out/doc['pdf'];require(len(PdfReader(pdf).pages)==doc['pages'],'rendered pages')
            original=subprocess.check_output([a.pdftotext,'-layout',str(ROOT/doc['pdf']),'-'])
            fresh=subprocess.check_output([a.pdftotext,'-layout',str(pdf),'-'])
            require(original==fresh,'exact complete page texts')
            rec.update(rendered=True,exact_page_text=True,pdf_sha256=sha(pdf))
        texts.append(rec)
    report={'status':'PASS_BOUNDED_DN_BINDING_REPLAY','exports':len(m['exports']),'complete_public_copies':len(copies),'whole_raw_files':len(inventory['whole_files']),'source_routes':20,'inherited_manifests':inherited,'controls':controls,'native_documents':texts,'old_finite_searches_repeated':0,'Lean_repeated':0,'source_checked':bool(a.study_root),'public_copies_checked_against_repo':bool(a.public_root),'whole_original_credit':0,'new_factor':None}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('inherited_manifests','native_documents')}))

if __name__=='__main__':
    main()
