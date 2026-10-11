#!/usr/bin/env python3
"""Bounded replay of the independent L028 review, with optional native GAP tests."""
import argparse,copy,hashlib,json,math,pathlib,re,subprocess,time
from fractions import Fraction
HERE=pathlib.Path(__file__).resolve().parent
AUTHOR='8bb02e21f47ed9da60ef382a969a1fa009790889a8fe60c0561badbc20bae0da'
def need(ok,msg):
    if not ok: raise RuntimeError('REVIEW_REJECT '+msg)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def bound(root,r):
    q=pathlib.PurePosixPath(r['path']);need(not q.is_absolute() and '..' not in q.parts,'relative binding')
    p=root/q;need(p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'binding '+r['path'])
def properties(v):
    need(v['status']=='ACCEPTED_COMPLETE_CORRECTED_PRINCIPAL_CONTRACT','review status')
    need(v['author_manifest_sha256']==AUTHOR and v['source_id']=='L028','identity')
    need(v['roles']['current_author']=='enumeration_volume','current author')
    need(v['scope']['connected_symbols_only'] and v['scope']['oriented_and_unrooted_outputs'],'scope')
    need(v['scope']['general_nonstring_hypertope_theorem_reproved'] is False,'non-string limit')
    need(v['scope']['historical_timings_reproduced'] is False,'timing limit')
    need(v['scope']['original_SW_chapter_obtained'] is False and v['scope']['original_LS_proof_recovered'] is False,'retained inputs')
    need(v['scope']['journal_typesetting_obtained'] is False,'edition limit')
    need(v['formal']['declarations']==7 and v['formal']['whole_enumeration_formalized'] is False,'formal boundary')
    need(v['credit']==dict(source_admission=0,question=0,compression_ratio=None),'no self-admission')
def table_recount(rows):
    for r in rows:
        q=r['q'];family=r['family']
        if family in ('PSL3','PSU3'):
            if family=='PSL3':
                special=(q**3-1)*(q**3-q)*(q**3-q*q)//(q-1)
                center=math.gcd(3,q-1)
                centralizer=(q*q-1)*(q*q-q) if q%2 else q**3*(q-1)
            else:
                special=(q+1)*(q*(q*q-1))*(q*q*(q**3+1))//(q+1)
                center=math.gcd(3,q+1)
                centralizer=q*(q+1)*(q*q-1) if q%2 else q**3*(q+1)
            order=special//center;inv=special//centralizer
        else:
            order=math.factorial(q)//(2 if family=='Alt' else 1)
            # Choose moved points, then pair them recursively (2k-1)!!.
            inv=0
            for k in range(1,q//2+1):
                if family=='Alt' and k%2:continue
                pairings=math.prod(range(1,2*k,2))
                inv+=math.comb(q,2*k)*pairings
        need((order,inv,str(Fraction(inv,order)))==(r['order'],r['involutions'],r['ratio']),'exact table row')
    need(len(rows)==32,'all revised table rows')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=pathlib.Path,required=True)
    ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--gap',type=pathlib.Path)
    a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output');a.out.mkdir(parents=True)
    t=time.monotonic();study=a.study_root.resolve()
    if (HERE/'manifest.json').exists():
        for row in read(HERE/'manifest.json')['exports']:bound(HERE,row)
    m=study/'phase282_manifest.json';need(digest(m)==AUTHOR,'author freeze')
    manifest=read(m)
    for row in manifest['exports']+manifest['retained_bindings']:bound(study,row)
    ledger=read(study/'phase282_source_ledger.json');coverage=read(HERE/'clause_review.json')
    need([r['id'] for r in ledger['rows']]==[r['id'] for r in coverage['rows']],'exact 32 clause identities')
    need(len(coverage['rows'])==32 and all(r['verdict']=='ACCEPTED_AS_QUALIFIED' for r in coverage['rows']),'all clauses reviewed')
    for old,new in zip(ledger['rows'],coverage['rows']):
        need(all(new[k]==old[k] for k in ('source_clause','pdf_pages','status','proof_spans','qualification')),'literal source disposition')
    for r in ledger['proof_spans'].values():
        data=b''.join((study/r['path']).read_bytes().splitlines(keepends=True)[r['start_line']-1:r['end_line']])
        need(len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],'full written span')
    review=read(HERE/'review.json');properties(review)
    report=read(HERE/'fresh_author_replay/report.json')
    need(report['status']=='PASS' and report['primary_checked'],'actual complete fresh replay')
    need((report['source_rows'],report['finite_groups'],report['complete_flag_markings'],report['table_rows'],report['independent_GAP_rows'],report['lean_declarations'])==(32,11,18,32,20,7),'fresh dimensions')
    need(len(report['axioms'])==7 and all(set(re.findall(r'[\w.]+',ax))<={'propext','Classical.choice','Quot.sound'} for _,ax in report['axioms']),'standard axioms')
    for e in report['executions']:
        for suffix in ('stdout','stderr'):need(digest(HERE/'fresh_author_replay'/(e['label']+'.'+suffix))==e[suffix+'_sha256'],'fresh output binding')
    table_recount(read(study/'phase282_exact_table.json')['rows'])
    controls=[]
    mutations=[('false full formalization',('formal','whole_enumeration_formalized'),True),('lost unrooted contract',('scope','oriented_and_unrooted_outputs'),False),('invented timing replay',('scope','historical_timings_reproduced'),True),('invented SW original access',('scope','original_SW_chapter_obtained'),True),('enlarged nonstring recovery',('scope','general_nonstring_hypertope_theorem_reproved'),True),('invented source admission',('credit','source_admission'),1),('wrong current author',('roles','current_author'),'enumeration_review')]
    for label,(x,y),value in mutations:
        v=copy.deepcopy(review);v[x][y]=value
        try:properties(v)
        except RuntimeError:controls.append(label)
        else:raise RuntimeError('REVIEW_REJECT control accepted '+label)
    rows=read(study/'phase282_exact_table.json')['rows'];bad=copy.deepcopy(rows);bad[12]['involutions']+=1
    try:table_recount(bad)
    except RuntimeError:controls.append('changed unitary exact count')
    else:raise RuntimeError('REVIEW_REJECT changed table accepted')
    native=None
    if a.gap:
        source=(HERE/'local_cases.g').read_text()
        def run(label,code):
            path=a.out/(label+'.g');path.write_text(code)
            p=subprocess.run([str(a.gap),'-q','-T',str(path)],capture_output=True,text=True,timeout=120)
            (a.out/(label+'.stdout')).write_text(p.stdout);(a.out/(label+'.stderr')).write_text(p.stderr)
            return p
        p=run('native',source)
        need(p.returncode==0 and 'INDEPENDENT_ALL_PASS' in p.stdout and not re.search(r'Error|warning|INDEPENDENT_REJECT',p.stdout+p.stderr),'independent native cases')
        native=re.findall(r'INDEPENDENT_AFFINE (\d+) order (\d+) aut (\d+) raw (\d+) oriented (\d+) unrooted (\d+)',p.stdout)
        need(native==[('5','20','20','40','2','1'),('7','42','42','168','4','2'),('11','110','110','880','8','4')],'native result binding')
        for label,old,new in [('lost mirror divisor','nr/(2*Size(A))=expected/2','nr/Size(A)=expected/2'),('false hemi type','Order(r0*r1)=3','Order(r0*r1)=4')]:
            need(old in source,'control applicability');p=run(label.replace(' ','_'),source.replace(old,new))
            need('INDEPENDENT_REJECT' in p.stdout+p.stderr and 'INDEPENDENT_ALL_PASS' not in p.stdout,'native control '+label);controls.append(label)
    out=dict(status='PASS',author_manifest_sha256=AUTHOR,exports=48,retained_bindings=4,source_rows=32,proof_spans=12,table_rows=32,formal_declarations=7,native_cases=native,controls_rejected=controls,seconds=round(time.monotonic()-t,4),limits=['This checker binds a human semantic review; it does not mechanically verify the written proof.','GAP finite examples and author Python are validation, not all-group proof.','Primary PDFs are private retained bindings, never review exports.'])
    (a.out/'report.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
if __name__=='__main__':main()
