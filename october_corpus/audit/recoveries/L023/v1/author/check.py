"""Exact complete-contract/component binding and native replay; no implicit adoption."""
from pathlib import Path
import argparse,copy,hashlib,json,re,shutil,subprocess,sys
from pypdf import PdfReader
R=Path(__file__).resolve().parent
def need(x,m):
    if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((R/n).read_text())
def bound(base,x):
    p=base/x['path'];need(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'binding '+str(p))
def run(cmd,cwd=None,timeout=120):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout)
    need(p.returncode==0,p.stdout[-3000:]+p.stderr[-3000:]);return p.stdout+p.stderr
def validate(s,m,p,h,c):
    need(s['status']=='COMPLETE_CORRECTED_PRINCIPAL_SUBMISSION_PENDING_ROOT_ADOPTION','adoption boundary')
    need(not s['theorem_set_equivalence'] and not s['whole_original_adopted'],'literal source limitations')
    need(m['remaining_principal']==[] and len(m['rows'])==70,'full source scope')
    rows={x['id']:x for x in m['rows']};need(len(rows)==70,'unique source dispositions')
    need(m['all_named_numbers']==list(range(1,11)),'all named source items')
    need(sum(k.startswith('Table1.q') for k in rows)==12,'complete table')
    for k in ['Abstract.infinite_geometries','S5.infinite_geometries']:need(rows[k]['disposition']=='RECOVERED_BY_UNIFORM_COMPLETION','infinite existence paid')
    need(rows['L7']['disposition']=='REFUTED','false universal construction')
    need(rows['S5.final_problem']['disposition']=='ANSWERED_BY_ATTRIBUTED_LATER_WORK','later answer attribution')
    need(rows['T1.6']['disposition']=='ANCILLARY_PARITY_CORRECTED','printed borrowed parity')
    need(rows['S4.other_orders']['disposition']=='ANCILLARY_EXPERIMENT_NOT_EXHAUSTED','experimental scope')
    need(s['new_question_credit']==s['new_Lean_declarations']==0 and s['new_factor'] is None,'credit limits')
    need(c['native_acquisition_pages']==[4,3,1,5,3],'all whole proof dependencies')
    req=sorted(x['path'] for x in p['whole_files'] if x['role']=='REQUIRED_MATHEMATICAL_PROGRAM')
    need(req==['components/geometry/certificate.py','components/polynomial/polynomial_table.g'],'required finite programs')
    need(p['required_stored_data']==[],'no invented finite database')
    need(any(x['path']=='check.py' and x['role']=='OPERATIONAL_REPLAY' for x in p['whole_files']),'current driver inventory')
    need(not h['proof_premise_of_completion'] and h['new_question_credit']==0,'historical answer boundary')
    need(h['authors']==['Dimitri Leemans','Klara Stokes','Philippe Tranchida'],'all later-work authors')
    need(s['required_inherited_even_theorem']=='Jones–Poulton, source reference 18, Theorem 2.3','even-family retained input')
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',required=True,type=Path);a.add_argument('--study-root',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--programs',action='store_true');q=a.parse_args()
    need(not q.out.exists(),'fresh output required');q.out.mkdir(parents=True)
    manifest=read('manifest.json')
    for x in manifest['exports']:bound(R,x)
    c=read('components.json')
    for x in c['exact_copies']:
        bound(R,x['copy']);need(x['source']['sha256']==x['copy']['sha256'] and x['source']['bytes']==x['copy']['bytes'],'exact component transfer')
        if q.study_root:bound(q.study_root,x['source'])
    for item in c['components']:
        base=R/Path(item['local_manifest']).parent
        for x in json.loads((base/'manifest.json').read_text())['exports']:bound(base,x)
    s=read('scope.json');m=read('source_map.json');p=read('program_inventory.json');h=read('historical_question.json')
    validate(s,m,p,h,c)
    expected_raw={str(x.relative_to(R)) for x in R.rglob('*') if x.suffix in ['.py','.g','.lean']}
    need({x['path'] for x in p['whole_files']}==expected_raw,'whole actual program inventory')
    for x in p['whole_files']:bound(R,x)
    for x in m['rows']:
        route=x['route'];need((R/route).is_file() or (R/'components'/route).is_file(),'actual source route '+x['id'])
    if q.study_root:
        for x in [m['source_pdf'],m['source_text']]+h['bindings']:bound(q.study_root,x)
    controls=[]
    mutations=[('literal theorem-set equivalence',0,lambda b:b.update(theorem_set_equivalence=True)),('self-adoption',0,lambda b:b.update(whole_original_adopted=True)),('new question credit',0,lambda b:b.update(new_question_credit=1)),('omit required even theorem',0,lambda b:b.update(required_inherited_even_theorem='none')),('drop source row',1,lambda b:b['rows'].pop()),('drop named item',1,lambda b:b['all_named_numbers'].pop()),('restore false L7',1,lambda b:next(x for x in b['rows'] if x['id']=='L7').update(disposition='RECOVERED')),('lose infinite completion',1,lambda b:next(x for x in b['rows'] if x['id']=='S5.infinite_geometries').update(disposition='PENDING')),('stale final question',1,lambda b:next(x for x in b['rows'] if x['id']=='S5.final_problem').update(disposition='UNANSWERED')),('promote experiment',1,lambda b:next(x for x in b['rows'] if x['id']=='S4.other_orders').update(disposition='COMPLETE_CENSUS')),('omit required certificate',2,lambda b:b.update(whole_files=[x for x in b['whole_files'] if x['path']!='components/geometry/certificate.py'])),('omit current driver',2,lambda b:b.update(whole_files=[x for x in b['whole_files'] if x['path']!='check.py'])),('historical result becomes premise',3,lambda b:b.update(proof_premise_of_completion=True)),('missing coauthor',3,lambda b:b['authors'].pop()),('free previous proof',4,lambda b:b['native_acquisition_pages'].pop())]
    for name,i,f in mutations:
        data=copy.deepcopy([s,m,p,h,c]);f(data[i])
        try:validate(*data)
        except ValueError:controls.append({'control':name,'rejected':True})
        else:raise ValueError('mutation accepted '+name)
    programs=[]
    if q.programs:
        for key in ['polynomial','geometry']:
            out=q.out/(key+'_replay');cmd=[sys.executable,'-B','-O',str(R/'components'/key/'check.py'),'--out',str(out)]
            (q.out/(key+'.stdout')).write_text(run(cmd,timeout=150));programs.append(key)
    native_pages=0
    if q.render:
        for n in read('native_acquisition.json')['documents']:
            b=q.out/'native'/n['key'];b.mkdir(parents=True)
            tex=R/n['tex'];shutil.copyfile(tex,b/tex.name)
            for i in range(2):(b/f'pass{i}.txt').write_text(run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',tex.name],b,60))
            log=(b/tex.with_suffix('.log').name).read_text();bad=[x for x in log.splitlines() if any(y in x for y in ['Overfull','Underfull','LaTeX Warning'])]
            need(bad==n['accepted_diagnostic_lines'],'native diagnostics '+n['key'])
            hashes=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(b/tex.with_suffix('.pdf').name).pages]
            need(hashes==n['page_text_sha256'],'native exact page texts '+n['key']);native_pages+=len(hashes)
    report={'status':'PASS_COMPLETE_CORRECTED_SUBMISSION_REPLAY','exports':len(manifest['exports']),'exact_component_copies':len(c['exact_copies']),'source_dispositions':len(m['rows']),'named_source_items':10,'finite_table_rows':12,'whole_program_files':len(p['whole_files']),'required_finite_replays':programs,'native_pages':native_pages,'controls':controls,'whole_original_adopted':False,'new_question_credit':0,'new_factor':None}
    (q.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
