#!/usr/bin/env python3
"""Portable binding, scope, optional-diagnostic and native-render replay.

The written uniform arguments require distinct mathematical review;
the finite diagnostics are never proof premises.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def load(path):
    return json.loads(path.read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def binding(root, item):
    path = root / item['path']
    need(path.is_file(), 'missing file: '+str(path))
    raw = path.read_bytes()
    need(len(raw)==item['bytes'] and sha(raw)==item['sha256'], 'binding: '+str(path))

def page_texts(path):
    return [p.extract_text() for p in PdfReader(path).pages]

def scope_check(scope, roles, route, common, application):
    need(scope['original_id']=='F011', 'one fixed original')
    need(scope['whole_original_credit']==0 and scope['measurements'] is None, 'no admission or ratio')
    need(scope['new_formalization'] is None and scope['new_question_credit']==0, 'no formal/question credit')
    need(scope['unresolved_principal']==[], 'complete principal candidate')
    need(scope['source_conjecture_status']=='RECORDED_UNANSWERED_NO_CURRENT_STATUS_CLAIM', 'unanswered conjecture')
    need(scope['primary']['sha256']=='9a864806aba2fab588a65ff20da6ba0ebdf8d68ebd9319695204dcecbac7b0bd', 'source edition')
    need(scope['source_pages']==10 and scope['direct_source_page_views']==list(range(1,11)), 'source extent')
    need(scope['native_pages']=={'common':4,'application':4}, 'complete written boundary')
    need(len(scope['rows'])==22 and len({x['id'] for x in scope['rows']})==22, 'unique complete source dispositions')
    rows={x['id']:x for x in scope['rows']}
    need('Centered' in rows['Theorem3.5']['disposition'] and 'proved' in rows['Theorem3.5']['disposition'], 'stronger theorem route')
    need('false' in rows['Proposition3.1']['disposition'], 'cardinality correction')
    need('Borrowed' in rows['Introduction_square_field_upper']['disposition'], 'borrowed upper bound')
    need(roles['required_mathematical_programs']==[] and roles['formal_files']==[], 'no finite/formal premise')
    need(len(roles['optional_validation'])==1 and roles['optional_validation'][0]['path']=='diagnostics.py', 'whole optional program')
    need(roles['source_software_cost'] is None and roles['software_inclusive_factor'] is None, 'unknown historical software')
    need(roles['operational_drivers']==['check.py'], 'whole driver scope')
    need(len(route['environments'])==13 and len(route['retained_inputs'])==3, 'proof and input closure')
    need('of order at least $n$' in common, 'stronger order exclusion')
    need('s+\\varphi(n-1)' in common and 'K+\\alpha T' in common, 'extra order cost')
    need('T\\le n/\\alpha+1/p\\le B+2+1/p' in common, 'correct rounding')
    need('i+j-(n-1)' in application and 'at most $n-2$' in application, 'centered exponent proof')
    need('q\\equiv7\\pmod8' in application and 'If $q>7$' in application, 'stronger theorem hypotheses')
    need('(q-7)/4>0' in application, 'small tuple case')

def controls(s, r, p, c, a):
    cases=[]
    for key,value in [('whole_original_credit',1),('measurements',0),('new_formalization','complete'),('new_question_credit',1),('source_conjecture_status','SOLVED'),('source_pages',9),('unresolved_principal',['Theorem3.5'])]:
        ss=copy.deepcopy(s);ss[key]=value;cases.append((key,ss,r,p,c,a))
    ss=copy.deepcopy(s);ss['rows'][1]['id']=ss['rows'][0]['id'];cases.append(('duplicate source ID',ss,r,p,c,a))
    rr=copy.deepcopy(r);rr['required_mathematical_programs']=['diagnostics.py'];cases.append(('validation as premise',s,rr,p,c,a))
    rr=copy.deepcopy(r);rr['source_software_cost']=0;cases.append(('unknown software as zero',s,rr,p,c,a))
    pp=copy.deepcopy(p);pp['retained_inputs']=pp['retained_inputs'][:-1];cases.append(('missing classical input',s,r,pp,c,a))
    cases.append(('missing extra order cost',s,r,p,c.replace('s+\\varphi(n-1)','s'),a))
    cases.append(('wrong rounding',s,r,p,c.replace('T\\le n/\\alpha+1/p\\le B+2+1/p','T\\le B+2'),a))
    cases.append(('lost centering',s,r,p,c,a.replace('i+j-(n-1)','i+j')))
    cases.append(('lost small case',s,r,p,c,a.replace('(q-7)/4>0','(q-7)/4')))
    passed=[]
    for label,ss,rr,pp,cc,aa in cases:
        try:
            scope_check(ss,rr,pp,cc,aa)
        except (ValueError,KeyError):
            passed.append(label)
        else:
            raise ValueError('accepted malformed scope: '+label)
    return passed

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--study-root',type=Path)
    ap.add_argument('--render',action='store_true')
    ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex')
    args=ap.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    manifest=load(HERE/'manifest.json') if (HERE/'manifest.json').exists() else None
    if manifest:
        for item in manifest['exports']:
            binding(HERE,item)
    s=load(HERE/'source_contract.json');r=load(HERE/'program_roles.json');p=load(HERE/'proof_map.json')
    c=(HERE/'square_patterns.tex').read_text();a=(HERE/'diophantine_tuples.tex').read_text()
    scope_check(s,r,p,c,a)
    for item in p['environments']:
        lines=(HERE/item['path']).read_text().splitlines(keepends=True)
        raw=''.join(lines[item['start_line']-1:item['end_line']]).encode()
        need(sha(raw)==item['sha256'], 'proof span: '+item['label'])
    if args.study_root:
        binding(args.study_root,s['primary'])
        for item in s['prior_work']:
            binding(args.study_root,item)
    completed=subprocess.run([sys.executable,'-B','-O',str(HERE/'diagnostics.py')],capture_output=True,text=True)
    need(completed.returncode==0,'optional diagnostics: '+completed.stderr)
    diagnostic=json.loads(completed.stdout)
    need(diagnostic==load(HERE/'diagnostic_report.json'),'optional diagnostic receipt')
    (args.out/'diagnostics.json').write_text(json.dumps(diagnostic,indent=2)+'\n')
    need(not diagnostic['uniform_proof_premise'],'finite checks are optional')
    rendered=[]
    for stem in ['square_patterns','diophantine_tuples']:
        old=page_texts(HERE/(stem+'.pdf'))
        need(len(old)==4,'whole PDF pages: '+stem)
        need([sha(t.encode()) for t in old]==p['page_text_sha256'][stem],'PDF page-text bindings')
        if args.render:
            with tempfile.TemporaryDirectory(prefix='F011_render_') as tmp:
                build=Path(tmp);shutil.copy2(HERE/(stem+'.tex'),build/(stem+'.tex'))
                for _ in range(2):
                    done=subprocess.run([args.pdflatex,'-halt-on-error','-interaction=nonstopmode',stem+'.tex'],cwd=build,capture_output=True,text=True)
                    need(done.returncode==0,'native compilation: '+done.stdout[-1500:])
                log=(build/(stem+'.log')).read_text()
                bad=[line for line in log.splitlines() if any(t in line for t in ['Overfull','undefined','Warning'])]
                need(not bad,'render diagnostics: '+repr(bad))
                need(page_texts(build/(stem+'.pdf'))==old,'native rendered page texts: '+stem)
                shutil.copy2(build/(stem+'.pdf'),args.out/(stem+'.pdf'))
                rendered.append({'document':stem,'pages':4,'native_compiler':'pdflatex','page_text_equal':True,'diagnostics':bad})
    report={'status':'PASS','manifest_sha256':sha((HERE/'manifest.json').read_bytes()) if manifest else None,'exports':len(manifest['exports']) if manifest else None,'source_dispositions':22,'proof_environments':13,'native_pages':8,'study_bindings_checked':bool(args.study_root),'optional_degree_cases':diagnostic['degree_cases'],'optional_pattern_cases':len(diagnostic['prime_field_pattern_cases']),'optional_centered_instances':sum(x['valid_centered_instances'] for x in diagnostic['centered_prime_cases']),'optional_stronger_parameter_cases':len(diagnostic['stronger_parameter_cases']),'negative_controls':controls(s,r,p,c,a),'render':rendered,'scope':'Author replay only. Distinct mathematical review required; no registration, ratios, new question or formal claims.'}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
