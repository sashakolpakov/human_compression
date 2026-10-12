#!/usr/bin/env python3
"""Portable binding/render and bounded scope checks; not a proof verifier."""
from pathlib import Path
import argparse,copy,hashlib,json,re,subprocess
from pypdf import PdfReader
ROOT=Path(__file__).resolve().parent

def need(c,m):
    if not c:raise ValueError(m)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pincheck(root,e,pathkey='path'):
    p=root/e[pathkey];need(p.is_file(),'missing '+str(p));need(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'binding '+str(p))
def envs(text):
    pat=r'\\begin\{(theorem|lemma|proposition|proof)\}(.*?)\\end\{\1\}'
    return [{'kind':m.group(1),'sha256':hashlib.sha256(m.group(0).encode()).hexdigest()} for m in re.finditer(pat,text,re.S)]
def validate_scope(c,m,d,n,i):
    need(c['status']=='AUTHOR_COMPLETE_CORRECTED_PRINCIPAL_CANDIDATE_PENDING_DISTINCT_REVIEW','status')
    need(c['source_id']=='L031','sourceid');need(c['mathematical_gap_in_principal_contract'] is None,'principal gap')
    need(c['new_question_credit']==0 and c['new_formal_declarations']==0 and not c['whole_source_formalized'],'no extra credit')
    need(c['new_measurement_or_factor'] is None and c['historical_software_cost'] is None,'unknown costs')
    need(len(c['principal_targets'])==4,'four principal targets')
    rr=m['dispositions'];ids=[r['id'] for r in rr]
    need(len(ids)==57 and len(set(ids))==57,'unique complete dispositions')
    need(m['source_pages']==12 and m['corrected_principal_contract_not_literal_equivalence'],'source scope')
    by={r['id']:r for r in rr}
    for k in ['Theorem1.4.binary','Proposition3.3.binary']:
        need(by[k]['status']=='CORRECTED_FALSE_SOURCE_CLAUSE','binary correction '+k)
    need(by['Section6.intermediateType']['status']=='CORRECTED_SOURCE_IDENTIFICATION','type correction')
    need(by['Corollary1.5.typeSelection']['status']=='CORRECTED_PROOF_ROUTE','primitive route')
    need(by['Theorem6.1.rankBound']['whole_proof_routes']==['retained/rank_bound/centralizer_bound.tex'],'rank route')
    for r in rr:
        need(r['whole_proof_routes'],'empty route')
        need(all((ROOT/p).is_file() for p in r['whole_proof_routes']),'proof closure')
        need(all(1<=p<=12 for p in r['source_physical_pages']),'source locator')
    for k in ['Section7.binaryOtherGenerators','Section7.derivedOrthogonal','Section7.PSL']:
        need(by[k]['status']=='SOURCE_RECORDED_QUESTION','question retained')
    need(d['finite_premises']==[] and d['full_external_or_runtime_cost'] is None,'finite/external boundary')
    need(len(d['complete_own_proof_papers'])==7 and len(set(d['complete_own_proof_papers']))==7,'seven full papers')
    need({e['id'] for e in d['retained_external_inputs']}=={'Taylor11.39','Taylor11.42','Taylor11.43','Dickson_SL2','Arf','MS2E16','low_dimension_classical','small_identifications'},'external closure')
    need(all(x['full_external_proof_cost'] is None for x in d['retained_external_inputs']),'unknown external proof costs')
    need([x['pages'] for x in n['documents']]==[5,3,5,2,2,2,4] and n['total_pages']==23,'native boundary')
    need(i['required_mathematical_programs']==[] and i['required_mathematical_data']==[],'no finite premise')
    need(i['historical_source_software_cost'] is None and i['software_inclusive_factor'] is None,'symmetric software')
    need(all(e['role'] in ['optional_validation','operational_historical_review','operational_current'] for e in i['whole_executable_files']),'roles')
    need(len({e['path'] for e in i['whole_executable_files']})==len(i['whole_executable_files']),'whole executable uniqueness')
    return True

def controls(c,m,d,n,i):
    tests=[]
    def run(name,mut):
        cc,mm,dd,nn,ii=copy.deepcopy((c,m,d,n,i));mut(cc,mm,dd,nn,ii)
        try:validate_scope(cc,mm,dd,nn,ii)
        except (ValueError,KeyError):tests.append({'name':name,'rejected':True});return
        raise ValueError('control accepted '+name)
    run('wrong source',lambda c,m,d,n,i:c.update(source_id='L011'))
    run('whole acceptance premature',lambda c,m,d,n,i:c.update(status='ACCEPTED'))
    run('question credit',lambda c,m,d,n,i:c.update(new_question_credit=1))
    run('full formal claim',lambda c,m,d,n,i:c.update(whole_source_formalized=True))
    run('software zero',lambda c,m,d,n,i:c.update(historical_software_cost=0))
    run('new factor',lambda c,m,d,n,i:c.update(new_measurement_or_factor=2))
    run('missing principal target',lambda c,m,d,n,i:c['principal_targets'].pop())
    run('duplicate disposition',lambda c,m,d,n,i:m['dispositions'].__setitem__(-1,copy.deepcopy(m['dispositions'][0])))
    run('missing disposition',lambda c,m,d,n,i:m['dispositions'].pop())
    run('literal equivalence',lambda c,m,d,n,i:m.update(corrected_principal_contract_not_literal_equivalence=False))
    run('binary correction suppressed',lambda c,m,d,n,i:next(x for x in m['dispositions'] if x['id']=='Proposition3.3.binary').update(status='RECOVERED'))
    run('plus correction suppressed',lambda c,m,d,n,i:next(x for x in m['dispositions'] if x['id']=='Section6.intermediateType').update(status='RECOVERED'))
    run('primitive choice claimed',lambda c,m,d,n,i:next(x for x in m['dispositions'] if x['id']=='Corollary1.5.typeSelection').update(status='RECOVERED'))
    run('rank proof omitted',lambda c,m,d,n,i:next(x for x in m['dispositions'] if x['id']=='Theorem6.1.rankBound').update(whole_proof_routes=[]))
    run('question claimed solved',lambda c,m,d,n,i:next(x for x in m['dispositions'] if x['id']=='Section7.PSL').update(status='RECOVERED'))
    run('finite premise introduced',lambda c,m,d,n,i:d['finite_premises'].append('GAP'))
    run('free classical proof',lambda c,m,d,n,i:d['retained_external_inputs'][0].update(full_external_proof_cost=0))
    run('missing acquired paper',lambda c,m,d,n,i:d['complete_own_proof_papers'].pop())
    run('truncated interfaces',lambda c,m,d,n,i:n['documents'][2].update(pages=4))
    run('missing raw helper',lambda c,m,d,n,i:i['whole_executable_files'].append(copy.deepcopy(i['whole_executable_files'][0])))
    run('optional promoted premise',lambda c,m,d,n,i:i['required_mathematical_programs'].append('oracle.py'))
    run('software factor',lambda c,m,d,n,i:i.update(software_inclusive_factor=1))
    return tests

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--render',action='store_true');a.add_argument('--study-root',type=Path);a.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');o=a.parse_args();o.out.mkdir(parents=True,exist_ok=True)
    manifest=ROOT/'manifest.json';nexports=0
    if manifest.exists():
        for e in read(manifest)['exports']:pincheck(ROOT,e);nexports+=1
    c=read(ROOT/'source_contract.json');m=read(ROOT/'source_map.json');d=read(ROOT/'dependencies.json');n=read(ROOT/'native_documents.json');i=read(ROOT/'program_inventory.json')
    validate_scope(c,m,d,n,i)
    copied=read(ROOT/'migration.json')['immutable_copies']
    for e in copied:pincheck(ROOT,e,'target')
    for e in i['whole_executable_files']:pincheck(ROOT,e)
    actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.py')}
    need(actual=={e['path'] for e in i['whole_executable_files']},'complete whole executable inventory')
    for f,spans in read(ROOT/'proof_spans.json')['papers'].items():need(envs((ROOT/f).read_text())==spans,'proof spans '+f)
    source=False
    if o.study_root:pincheck(o.study_root,m['source']);source=True
    result={'status':'PASS','manifest_exports_verified':nexports,'immutable_copies':len(copied),'source_dispositions':len(m['dispositions']),'native_pages':n['total_pages'],'source_pin_checked':source,'controls':controls(c,m,d,n,i),'rendered':[],'mathematics_proved_by_checker':False,'new_original_credit':0,'new_formal_declarations':0}
    for x in n['documents']:
        p=ROOT/x['pdf'];need(len(PdfReader(p).pages)==x['pages'],'page count '+str(p))
        if o.render:
            t=ROOT/x['tex'];b=o.out/t.stem;b.mkdir(exist_ok=True)
            for j in range(2):
                r=subprocess.run([o.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(b.resolve()),t.name],cwd=t.parent,text=True,capture_output=True)
                (b/f'pass{j+1}.txt').write_text(r.stdout+r.stderr);need(r.returncode==0,'TeX '+str(t))
            diag=[l for l in (b/(t.stem+'.log')).read_text().splitlines() if 'Warning' in l or 'Overfull' in l];need(not diag,'TeX diagnostics '+str(diag))
            q=b/(t.stem+'.pdf');need([y.extract_text() for y in PdfReader(q).pages]==[y.extract_text() for y in PdfReader(p).pages],'page text '+str(p))
            result['rendered'].append({'pdf':x['pdf'],'pages':x['pages'],'exact_page_texts':True,'diagnostics':diag})
    (o.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['controls','rendered']}|{'negative_controls':len(result['controls']),'fresh_native_documents':len(result['rendered'])}))
if __name__=='__main__':main()
