"""Operational additive assembly checker; no new mathematical algorithm."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parent
PINS={'positive':'351781693d099f31666832dc6c0f25c6c15fb5afc49173330d911e5dc66d7f1d','positive_review':'4b4cb87e96de7cd77753ef62759b2ebd04388b0b795c026610055f74464c2c48','counterexample':'a23c9ae2badd98f722a5ef70526caacfd3fdac32b9f513fd3786eeb9a308f86f','counterexample_review':'b4149d858e1617f0c1d8e279231443db869c669f9c378c73a33196d8b12daf57'}
CHANGES={'L122.Lemma1_bare_existence':'REFUTED_LITERAL_EXISTENTIAL_BY_ACTUAL_COSET_GEOMETRY','L122.Method1':'CORRECTED_ORDER_THREE_ON_COSETS_SUFFICIENT_UNQUALIFIED_EXISTENCE_REFUTED'}
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads((R/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(base,x):
    p=base/x['path'];need(p.is_file() and p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'binding '+x['path'])
def validate(s,c,i):
    old=load('components/positive/source_contract.json')
    need(c['source']==old['source'] and c['source']['pages']==6,'entire exact primary')
    rows=c['dispositions'];prior=old['dispositions'];need(len(rows)==len(prior)==36,'all 36 source rows')
    for x,y in zip(rows,prior):
        for k in ['id','claim','source_physical_pages']:need(x[k]==y[k],'unaltered source identity '+k)
        need(x['prior_status']==y['status'],'prior status')
        need(x['status']==CHANGES.get(x['id'],y['status']),'exact current disposition')
        need(bool(x['current_route']),'paid route')
    need(c['unresolved_principal_obligations']==s['unresolved_principal_obligations']==[],'no silently remaining principal gap')
    need(c['principal_disposition_coverage_complete'] is True and s['principal_disposition_coverage_complete'] is True,'current complete disposition')
    need(c['complete_original_recovery_claim'] is False and s['whole_original_accepted'] is False,'assembly acceptance separate')
    need(c['theorem_set_equivalence_claim'] is False and c['all_original_theorems_follow_claim'] is False,'corrected/refuted theorem scope')
    need(c['new_question_answer'] is False and c['new_formalization'] is False,'no new question/formal credit')
    need(s['source_credit'] is None and s['new_question_credit']==s['new_Lean_declarations']==0,'no assigned counts')
    need(s['numerical_factor'] is None and s['software_inclusive_factor'] is None,'no factors')
    need([x['pages'] for x in s['documents']]==[4,4,3,2] and s['whole_native_pages']==13 and s['scientific_pages']==11,'whole native boundary')
    need(s['theorem_set_equivalence'] is False and s['all_original_theorems_follow'] is False,'no literal theorem equivalence')
    need(s['roles']['assembly_review']=='PENDING','distinct assembly review required')
    files=i['files'];roles={x['path']:x['role'] for x in files}
    expected={'components/positive/programs/verify_examples.g':'REQUIRED_MATHEMATICAL_PROGRAM','components/positive/data/seeds.g':'REQUIRED_MATHEMATICAL_DATA','components/counterexample/certificate.py':'REQUIRED_MATHEMATICAL_PROGRAM','components/counterexample/data.json':'REQUIRED_MATHEMATICAL_DATA','components/positive/optional_small_oracle.py':'OPTIONAL_VALIDATION','components/counterexample/controls.py':'OPTIONAL_VALIDATION','components/positive/check.py':'OPERATIONAL_DRIVER','components/counterexample/check.py':'OPERATIONAL_DRIVER','check.py':'OPERATIONAL_DRIVER'}
    expected.update({str(p.relative_to(R)):'ARCHIVED_DISCOVERY_NOT_PREMISE' for p in (R/'components/counterexample/discovery').iterdir()})
    need(roles==expected and len(files)==15,'whole executable/data inventory')
    need(i['formal_files']==[] and i['source_executable_listings']==[],'source listing/formal scope')
    need(i['source_historical_software_cost'] is None and i['external_GAP_and_classical_model_cost'] is None and i['software_inclusive_factor'] is None,'unknown software not zero')
    return True
def controls(s,c,i):
    cases=[('omit source row',1,lambda x:x['dispositions'].pop()),('restore pending bare lemma',1,lambda x:next(z for z in x['dispositions'] if z['id']=='L122.Lemma1_bare_existence').update(status='UNRESOLVED_PRINCIPAL_OBLIGATION')),('silently change source claim',1,lambda x:x['dispositions'][0].update(claim='other')),('unqualified Method1',1,lambda x:next(z for z in x['dispositions'] if z['id']=='L122.Method1').update(status='PROVED')),('free common',0,lambda x:x.update(whole_native_pages=9)),('old pending treated current',0,lambda x:x.update(unresolved_principal_obligations=['L122.Lemma1_bare_existence'])),('premature acceptance',0,lambda x:x.update(whole_original_accepted=True)),('theorem equivalence',0,lambda x:x.update(theorem_set_equivalence=True)),('new question',0,lambda x:x.update(new_question_credit=1)),('factor assigned',0,lambda x:x.update(numerical_factor=1)),('required program optional',2,lambda x:x['files'][0].update(role='OPTIONAL_VALIDATION')),('data omitted',2,lambda x:x['files'].pop(3)),('driver omitted',2,lambda x:x['files'].pop(8)),('unknown source software zero',2,lambda x:x.update(source_historical_software_cost=0)),('source shortened',1,lambda x:x['source'].update(pages=5))]
    passed=[]
    for n,k,f in cases:
        z=copy.deepcopy([s,c,i]);f(z[k])
        try:validate(*z)
        except (ValueError,KeyError,StopIteration):passed.append(n)
        else:raise ValueError('control escaped: '+n)
    return passed
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--programs',action='store_true');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');a=ap.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    if (R/'manifest.json').exists():
        for x in load('manifest.json')['exports']:bind(R,x)
    comps=load('components.json');need({x['id']:x['manifest_sha256'] for x in comps}==PINS,'four exact accepted components')
    n=0
    for x in comps:
        need(sha(R/x['manifest_path'])==PINS[x['id']],'component manifest');m=load(x['manifest_path'])
        need(len(m['exports'])==len(x['exports']),'complete component exports')
        for y,z in zip(x['exports'],m['exports']):
            need(y['path']==x['current_directory']+'/'+z['path'] and all(y[k]==z[k] for k in ['bytes','sha256']),'exact relocation');bind(R,y)
            if a.study_root:bind(a.study_root,dict(y,path=y['source_path']))
            n+=1
        n+=1
    need(n==56,'all inherited files')
    s,c,i=map(load,['scope.json','source_contract.json','program_inventory.json']);validate(s,c,i)
    for x in i['files']:
        if 'sha256' in x:bind(R,x)
    cs=controls(s,c,i);reports={}
    for name in ['positive','counterexample']:
        cmd=[sys.executable,'-B','-O',str(R/'components'/name/'check.py'),'--out',str(a.out/name)]
        if a.render:cmd+=['--render','--pdflatex',a.pdflatex]
        if a.study_root:cmd+=['--study-root',str(a.study_root)]
        if a.programs and name=='positive':cmd+=['--programs','--gap',a.gap]
        p=subprocess.run(cmd,capture_output=True,text=True);(a.out/(name+'.stdout')).write_text(p.stdout+p.stderr);need(p.returncode==0,'component replay '+name)
        reports[name]=json.loads((a.out/name/'report.json').read_text())
    need(reports['positive']['source_dispositions']==36 and len(reports['positive']['controls'])==24,'positive exact scope')
    need(reports['counterexample']['full_correlation_order']==44064 and reports['counterexample']['controls']==9,'actual counterexample scope')
    pages=0
    if a.render:
        from pypdf import PdfReader
        d=a.out/'addendum';d.mkdir();shutil.copy2(R/'current_contract.tex',d/'current_contract.tex')
        for j in range(2):
            p=subprocess.run([a.pdflatex,'-halt-on-error','-interaction=nonstopmode','current_contract.tex'],cwd=d,capture_output=True,text=True);(d/f'run{j}.log').write_text(p.stdout+p.stderr);need(p.returncode==0,'addendum native render')
        log=(d/'current_contract.log').read_text();need(not any(t in log for t in ['Overfull','LaTeX Warning:','Undefined control sequence']),'clean addendum')
        actual=[p.extract_text() for p in PdfReader(d/'current_contract.pdf').pages];prior=[p.extract_text() for p in PdfReader(R/'current_contract.pdf').pages];need(actual==prior and len(actual)==2,'exact addendum pages');pages=13
    report=dict(status='PASS_CURRENT_COMPLETE_CONTRACT_ASSEMBLY',components=4,exact_copied_files=n,source_dispositions=36,changed_disposition_statuses=2,additional_current_routes=1,assembly_controls=cs,positive_controls=24,counterexample_controls=9,positive_GAP_repeated=a.programs,counterexample_integer_certificate_fresh=True,native_pages_rebuilt=pages,whole_original_acceptance=False,new_question_credit=0,new_Lean_declarations=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
