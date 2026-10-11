#!/usr/bin/env python3
"""Bounded publication review; no source extraction, GAP or Lean execution."""
from pathlib import Path
from fractions import Fraction
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess

BASELINE='1eb5745123e610459f413a3473ec7b0029591843'
ADMISSION='d7a0a50047b5cf96c2a565c1ce116eec3a3094813dbb035ec67bddb6a32f8f4d'
B='audit/topic-d/v2/measurement/'
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def functions(s):
    return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name!='main'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--study',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output')
    admission=read(a.repo/B/'admission.json');need(sha(a.repo/B/'admission.json')==ADMISSION,'exact staged admission')
    for r in admission['artifacts']:
        f=a.repo/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'published artifact '+r['path'])
    copies={}
    for old,new in [('topic_D_measurement_results','packet'),('topic_D_measurement_results_independent_review','arithmetic_review'),('topic_D_measurement_results_root_adoption','root_adoption')]:
        src=a.study/old;dst=a.repo/B/new
        need((src/'manifest.json').read_bytes()==(dst/'manifest.json').read_bytes(),'same frozen manifest '+old)
        rows=read(src/'manifest.json')['exports']
        for r in rows:
            need((src/r['path']).read_bytes()==(dst/r['path']).read_bytes(),'unchanged copy '+r['path'])
            need(sha(dst/r['path'])==r['sha256'],'frozen export '+r['path'])
        copies[new]=len(rows)
    vp=a.repo/'scripts/verify_snapshot.py'
    old=subprocess.check_output(['git','show',BASELINE+':scripts/verify_snapshot.py'],cwd=a.repo,text=True)
    of,nf=functions(old),functions(vp.read_text())
    need(len(of)==26 and all(nf.get(k)==v for k,v in of.items()),'prior checker interface changed')
    need(set(nf)-set(of)=={'check_topic_d_measurement'},'unexpected checker addition')
    mainnode=next(n for n in ast.parse(vp.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='main')
    need(sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='check_topic_d_measurement' for n in ast.walk(mainnode))==1,'main must call new checker once')
    spec=importlib.util.spec_from_file_location('public_verifier',vp);v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    need(v.check_topic_d_measurement()==(240,180),'public new function result')
    packet=a.repo/B/'packet';r=read(packet/'results.json');recount=read(packet/'independent/recount_corrected.json')
    pairs=[('L066','D1'),('L074','D2'),('L104','D3')];fractions=0;keys=set()
    for c in r['coordinates']:
        variant,form,unit=c['variant'],c['normalization'],c['unit'];keys.add((variant,form,unit))
        docs={n:d['variants'][variant][form][unit] for n,d in recount['documents'].items()}
        source=sum(docs[s] for s,d in pairs);written=docs['U_D']+sum(docs[d] for s,d in pairs)
        raw=sum(x['variants'][form][unit] for x in recount['raw_records']['raw_program_alternative'].values())
        for rep,den in [('written_papers',written),('including_printed_program',written+docs['CODE']),('including_raw_program_alternative',written+raw)]:
            q=c['comparisons'][rep];f=Fraction(source,den)
            need(q['numerator']==source and q['denominator']==den and q['reduced_numerator']==f.numerator and q['reduced_denominator']==f.denominator and q['exact_fraction']==str(f) and q['factor']==float(f),'combined exact fraction');fractions+=1
        for (source_name,app),q in zip(pairs,c['per_result']):
            f=Fraction(docs[source_name],docs[app]);need(q['source']==source_name and q['application']==app and q['numerator']==docs[source_name] and q['denominator']==docs[app] and q['exact_fraction']==str(f) and q['factor']==float(f),'conditional fraction');fractions+=1
    need(len(keys)==30 and fractions==180,'all policy coordinates')
    controls=[];load=v.load
    mutations=[
      ('wrong_admission_count',B+'admission.json',lambda x:x.update(required_programs=4)),
      ('rejected_adoption',B+'root_adoption/review.json',lambda x:x.update(status='REJECT')),
      ('cross_topic_discount',B+'packet/results.json',lambda x:x.update(cross_topic_common_discount=True)),
      ('hidden_prepaid_code',B+'packet/results.json',lambda x:x.update(conditional_prepaid='Given U.')),
      ('dropped_full_program',B+'packet/results.json',lambda x:x['complete_mathematical_programs'].pop()),
      ('wrong_fraction',B+'packet/results.json',lambda x:x['coordinates'][0]['comparisons']['written_papers'].update(exact_fraction='1')),
      ('source_status_changed',B+'packet/inputs/source_contract_boundary.json',lambda x:x['rows'][0].update(current_status='EXCLUDED')),
      ('wrong_scientific_pdf',B+'packet/inputs/publication_binding.json',lambda x:x['scientific_documents']['U_D'].update(pdf_sha256='0'*64)),
      ('unknown_as_zero',B+'admission.json',lambda x:x['unknown_external_costs'].update(historical_software=0)),
      ('formal_scope_inflated',B+'admission.json',lambda x:x.update(source_specific_formalization=True)),
    ]
    for name,path,mutate in mutations:
        def changed(p,path=path,mutate=mutate):
            x=copy.deepcopy(load(p))
            if str(p)==path:mutate(x)
            return x
        v.load=changed
        try:v.check_topic_d_measurement()
        except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('semantic mutation accepted '+name)
        finally:v.load=load
    # The existing integrity helper is also exercised with the exact public
    # artifact and a false digest; no published file is modified.
    bad=copy.deepcopy(admission['artifacts'][0]);bad['sha256']='0'*64
    try:v.check_bindings([bad])
    except ValueError as e:controls.append(dict(name='changed_bound_artifact',rejected=True,reason=str(e)))
    else:raise ValueError('bad digest accepted')
    links=[]
    for name in ['README.rst','audit/completion.rst',B+'README.rst']:
        f=a.repo/name
        for target in re.findall(r'<([^<>\n]+)>`_',f.read_text()):
            if re.match(r'\w+://',target) or target.startswith('#'):continue
            path=target.split('#')[0];need((f.parent/path).exists(),'missing local link '+name+': '+target);links.append(dict(document=name,target=target))
    report=dict(status='PASS_BOUNDED_D_NUMERICAL_PUBLICATION_REVIEW',baseline=BASELINE,admission_sha256=ADMISSION,copy_exports=copies,artifacts_bound=len(admission['artifacts']),prior_non_main_AST_unchanged=26,new_function_result=[240,180],independent_fraction_recount=fractions,coordinates=30,semantic_controls=controls,semantic_control_method='In-memory load substitution after reading the real bound bytes; one direct corrupted-digest integrity check. No public files changed.',local_links_checked=len(links),primary=r['primary'],no_primary_extraction_or_font_reaudit=True,no_gap_or_lean_rerun=True)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','copy_exports','artifacts_bound','independent_fraction_recount','local_links_checked']}))
if __name__=='__main__':main()
