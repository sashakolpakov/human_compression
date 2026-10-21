#!/usr/bin/env python3
"""Recheck exact N006 review bindings/interfaces; optional full scientific replay."""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess,sys
import local_models
ROOT=Path(__file__).resolve().parent

def need(b,s):
    if not b: raise RuntimeError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def exports(m):
    e=m['exports'];return [dict(v,path=k) for k,v in e.items()] if isinstance(e,dict) else e
def exact(root,row):
    rel=Path(row['path']);need(not rel.is_absolute() and '..' not in rel.parts,'invalid bound relative path')
    p=root/rel;need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'changed input: '+str(rel));return p

def scope(r,f,formal):
    need(r['status']=='ACCEPTED_COMPLETE_CORRECTED_N006_PRINCIPAL_CONTRACT','review status')
    need(r['source_id']=='N006' and r['source_rows']==27 and r['source_pages']==22,'source scope')
    need(r['current_paper_pages']=={'common':8,'application':8,'nine_case_note':5,'HN_note':4},'complete PDF pages')
    need(r['findings']['source_exceptions_outside_acceptance']==['Fi22','Fi24prime'],'exceptions remain separate')
    need(r['findings']['source_false_clauses_not_counted_as_true'] and r['findings']['lamplighter_missing_square_corrected'],'literal source corrections')
    need(r['findings']['all_ten_affirmative_cases'] and not r['findings']['remaining_mathematical_defects'],'whole affirmative scope')
    need(r['retained_proof_cost'] is None,'retained proof costs unknown')
    need(r['formal']=={'declarations':17,'reused':8,'new':9,'standard_axioms_only':True,'geometry_formalized':False,'full_module_generation_formalized':False,'sporadic_formalized':False},'formal boundary')
    need(not r['primary_exports'] and r['measurement_factor'] is None and all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no publication credit or ratio')
    cases=f['cases'];need([v['socle'] for v in cases]==['M12','J2','HS','He','Suz','J3','M22','McL','ON','HN'],'exact ten cases')
    need(all(v['IP_pairs_per_marking']==64 and v['flag_equalities_per_marking']==3 for v in cases),'full IP and independent flag criterion')
    need(f['HN_order_is_retained_not_enumerated'] and f['external_classification_proof_cost'] is None,'HN generation trust')
    need(f['HN_IP']=={'proper_pairs':49,'elementary_full_subset_pairs':15,'streamed_product_counts':[376,1056]},'HN proper and elementary pairs')
    need(f['source_exceptions_not_reviewed']==['Fi22','Fi24prime'],'new exception work separate')
    need(formal['new_declarations']==9 and formal['reused_declarations']==8 and not formal['full_geometry_formalized'],'formal review matches')

def mutations(r,f,formal):
    tests=[('omit_HN','f',lambda x:x['cases'].pop()),('drop_flag_checks','f',lambda x:x['cases'][0].update(flag_equalities_per_marking=0)),('enumerated_HN_claim','f',lambda x:x.update(HN_order_is_retained_not_enumerated=False)),('seven_page_app','r',lambda x:x['current_paper_pages'].update(application=7)),('include_Fi22','r',lambda x:x['findings'].update(source_exceptions_outside_acceptance=['Fi24prime'])),('complete_formalization','r',lambda x:x['formal'].update(geometry_formalized=True)),('zero_external_proof_cost','r',lambda x:x.update(retained_proof_cost=0)),('false_literal_source','r',lambda x:x['findings'].update(lamplighter_missing_square_corrected=False)),('eight_reused_as_new','formal',lambda x:x.update(new_declarations=17))]
    out=[]
    for name,key,alter in tests:
        d={'r':copy.deepcopy(r),'f':copy.deepcopy(f),'formal':copy.deepcopy(formal)};alter(d[key])
        try:scope(d['r'],d['f'],d['formal'])
        except RuntimeError:out.append({'name':name,'rejected':True})
        else:raise RuntimeError('mutation accepted: '+name)
    return out

def logs():
    a=load(ROOT/'replay/nine/report.json');h=load(ROOT/'replay/HN/report.json');l=load(ROOT/'replay/formal/report.json')
    need(a['status']==h['status']==l['status']=='PASS','fresh replay status')
    need(a['complete_nine_existence_cases'] and a['outer_route_obstruction_checked'] and set(a['parts'])=={'eight','on','outer-orders'},'nine complete replay')
    for x in a['logs'].values():need(sha(ROOT/'replay/nine'/x['log'])==x['sha256'],'nine log binding')
    need(h['complete_HN_case'] and not h['full_group_order_enumerated'] and h['named_group_and_maximal_classification_retained'],'HN fresh report boundary')
    need(sha(ROOT/'replay/HN'/h['finite_replay']['log'])==h['finite_replay']['sha256'],'HN log binding')
    texts={k:(ROOT/'replay/nine'/f'{k}.log').read_text().replace('\\\n','') for k in ['eight','on','outer-orders']}
    for v in load(ROOT/'finite_review.json')['cases'][:8]:
        for tag,key in [('polytope','string_pair_orders_01_02_12'),('hypertope' if v['socle'] in ['M12','J2','HS','He','Suz','J3'] else 'halving','triangle_pair_orders_01_02_12')]:
            match=re.search(re.escape(v['socle'])+r'\.2-'+tag+r' order=(\d+) pair_orders=\[([^]]+)\]',texts['eight']);need(match is not None,'missing finite table row')
            need(int(match[1])==v['full_extension_order'] and [int(x) for x in match[2].split(',')]==v[key],'wrong finite table output')
    need('pair_orders=[ 8, 2, 11 ]' in texts['on'] and 'pair_orders=[8,8,11]' in texts['on'],'ON orders')
    hn=(ROOT/'replay/HN/hn.log').read_text().replace('\\\n','')
    need('proper_IP=49 product_tests=376 type=[12,2,5]' in hn and 'proper_IP=49 product_tests=1056 type=[12,12,5]' in hn,'HN all local conditions')
    need(len(l['modules'])==3 and sum(len(m['axioms']) for m in l['modules'])==17,'all formal reports')
    allowed={'propext','Classical.choice','Quot.sound'}
    for m in l['modules']:
        name=Path(m['source']['file']).stem+'.txt';need(sha(ROOT/'replay/formal'/name)==m['log_sha256'],'formal log binding')
        need(all(set(v['axioms'])<=allowed for v in m['axioms']),'unallowed axiom')
    need(len(a['controls'])==6 and len(h['controls'])==12 and len(l['countermodels'])==5,'actual fresh control coverage')
    need(all(v['rejected'] for v in a['controls']+h['controls']),'finite control rejection')
    return {'nine_controls':6,'HN_controls':12,'formal_countermodels':5,'fresh_formal_declarations':17}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--verify-primary',action='store_true');ap.add_argument('--programs',action='store_true');ap.add_argument('--formal',action='store_true');ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--lean',type=Path);ap.add_argument('--packages',type=Path);ap.add_argument('--atlas-nine',type=Path);ap.add_argument('--atlas-hn',type=Path);args=ap.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(),'fresh output path required')
    if (ROOT/'manifest.json').exists():
        for row in exports(load(ROOT/'manifest.json')):exact(ROOT,row)
    args.out.mkdir(parents=True);study=args.study_root.resolve();bindings=load(ROOT/'bindings.json');checked=0
    for row in bindings['files']:exact(study,row);checked+=1
    for row in bindings['packets']:
        p=exact(study,row);checked+=1
        for item in exports(load(p)):exact(p.parent,item);checked+=1
    if args.verify_primary:
        for row in bindings['primary_inputs']:exact(study,row);checked+=1
    r=load(ROOT/'review.json');f=load(ROOT/'finite_review.json');formal=load(ROOT/'formal_review.json');scope(r,f,formal)
    source=load(study/'corpus161_N006_recovery/source_scope.draft.json');proof=load(ROOT/'proof_reading.json')
    need(len(source['rows'])==27 and [x['id'] for x in source['rows']]==[x['id'] for x in proof['rows']],'exact source row inventory')
    for src,dst in zip(source['rows'],proof['rows']):need(src['source_locator']==dst['source_locator'] and src['proof']==dst['proof_routes'],'source proof routes')
    for m in formal['modules']:
        p=study/'corpus161_N006_recovery/formal'/m['file'];need(sha(p)==m['sha256'],'formal byte scope')
    models=json.loads(json.dumps(local_models.run()));need(models==load(ROOT/'local_models.json'),'independent literal models')
    observed=logs();controls=mutations(r,f,formal)
    optional=[]
    def run(cmd,key):
        p=subprocess.run(cmd,capture_output=True,text=True);(args.out/(key+'.stdout')).write_text(p.stdout+p.stderr);need(p.returncode==0,'optional replay failed: '+key);optional.append(key)
    if args.programs:
        need(args.gap and args.atlas_nine and args.atlas_hn,'program replay requires GAP and both explicit external Atlas roots')
        run([sys.executable,'-B','-O',str(study/'corpus161_N006_sporadic/check.py'),'--gap',args.gap,'--atlas-root',str(args.atlas_nine),'--out',str(args.out/'fresh_nine')],'nine')
        run([sys.executable,'-B','-O',str(study/'corpus161_N006_HN/check.py'),'--gap',args.gap,'--atlas-root',str(args.atlas_hn),'--out',str(args.out/'fresh_HN')],'HN')
    if args.formal:
        need(args.lean and args.packages,'formal replay requires explicit pinned compiler and packages')
        run([sys.executable,'-B','-O',str(study/'corpus161_N006_recovery/formal/check.py'),'--lean',str(args.lean),'--packages',str(args.packages),'--out',str(args.out/'fresh_formal')],'formal')
    report={'status':'PASS','exact_input_bindings':checked,'source_rows':27,'affirmative_cases':10,'current_PDF_pages':25,'fresh_evidence':observed,'independent_model_controls':models['controls'],'semantic_controls':controls,'new_expensive_replays':optional,'primary_files_verified':args.verify_primary,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    (args.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
