"""Portable proof-binding/native replay; optional examples are not proof premises."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys
from pypdf import PdfReader
R=Path(__file__).resolve().parent
def need(x,m):
    if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((R/n).read_text())
def run(cmd,cwd=None):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True)
    need(p.returncode==0,p.stdout[-3000:]+p.stderr[-3000:]);return p.stdout+p.stderr
def validate(s,d):
    need(not s['whole_original_acceptance'],'whole-source boundary')
    need(s['B_norm']==1 and len(s['noncommuting_hypothesis'])==3,'actual algebra hypotheses')
    need(not s['individual_vector_norm_nonzero_required'],'isotropic vectors included')
    need(s['signed_vector_injection_scope']=='vertices incident with one fixed face','injection scope')
    need(not s['full_normalizer_identification'],'no full normalizer identification')
    need(not s['general_unrestricted_Lemma7_recovered'],'universal source claim remains false')
    need(s['infinite_actual_geometries_proved'] and s['full_group_chamber_orbits']==2,'actual infinite family')
    need(not s['new_finite_premise'] and s['required_new_programs']==[],'written proof, no finite premise')
    need(s['new_question_credit']==0 and s['new_Lean_declarations']==0,'credit scope')
    h=d['historical_question_result']
    need(not h['mathematical_premise_of_this_completion'] and h['new_question_credit']==0,'historical answer role')
    need(s['final_source_question_status']=='answered by attributed separately accepted later L015 work','final question status')
    need([x['pages'] for x in d['whole_native_dependencies']]==[4,5],'whole inherited papers paid')
def main():
    p=argparse.ArgumentParser();p.add_argument('--out',required=True,type=Path);p.add_argument('--render',action='store_true');p.add_argument('--examples',action='store_true');p.add_argument('--study-root',type=Path);a=p.parse_args()
    need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True)
    m=read('manifest.json')
    for x in m['exports']:
        f=R/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'export '+x['path'])
    d=read('dependencies.json');s=read('scope.json');validate(s,d)
    if a.study_root:
        for x in d['bindings']:
            f=a.study_root/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'external '+x['path'])
    mutations=[('whole-original claim','whole_original_acceptance',True),('drop norm-one condition','B_norm',0),('drop isotropic cases','individual_vector_norm_nonzero_required',True),('global injection','signed_vector_injection_scope','all vertices'),('unjustified full normalizer','full_normalizer_identification',True),('restore false source lemma','general_unrestricted_Lemma7_recovered',True),('finite examples become premise','new_finite_premise',True),('new question credit','new_question_credit',1),('stale final-question status','final_source_question_status','unanswered')]
    controls=[]
    for name,k,v in mutations:
        b=copy.deepcopy(s);b[k]=v
        try:validate(b,d)
        except ValueError:controls.append({'name':name,'rejected':True})
        else:raise ValueError('mutation passed '+name)
    for name,change in [('free prior paper',lambda b:b['whole_native_dependencies'].pop()),('historical answer becomes premise',lambda b:b['historical_question_result'].update(mathematical_premise_of_this_completion=True))]:
        b=copy.deepcopy(d);change(b)
        try:validate(s,b)
        except ValueError:controls.append({'name':name,'rejected':True})
        else:raise ValueError('dependency mutation passed '+name)
    examples=0
    if a.examples:
        (a.out/'examples.log').write_text(run([sys.executable,'-B','-O',str(R/'check_vectors.py'),'--out',str(a.out/'vector_result.json')]))
        v=json.loads((a.out/'vector_result.json').read_text());need(v==read('vector_result.json'),'optional exact receipt')
        examples=sum(x['norm_one_nonzero_coordinate_cases'] for x in v['rows'])
    pages=0
    if a.render:
        b=a.out/'native';b.mkdir();shutil.copyfile(R/'odd_completion.tex',b/'odd_completion.tex')
        for i in range(2):(b/f'run{i}.txt').write_text(run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','odd_completion.tex'],b))
        log=(b/'odd_completion.log').read_text();need(not any(t in log for t in ['Overfull','Underfull','LaTeX Warning']),'native diagnostics')
        texts=[hashlib.sha256((p.extract_text() or '').encode()).hexdigest() for p in PdfReader(b/'odd_completion.pdf').pages]
        need(texts==read('native.json')['page_text_sha256'],'exact native page texts');pages=len(texts)
    report={'status':'PASS_BOUNDED_AUTHOR_REPLAY','exports':len(m['exports']),'external_bindings':len(d['bindings']) if a.study_root else 0,'source_routes':len(read('source_map.json')['rows']),'native_pages':pages,'optional_vector_cases':examples,'scope_controls':controls,'new_finite_premise':False,'whole_original_acceptance':False}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
