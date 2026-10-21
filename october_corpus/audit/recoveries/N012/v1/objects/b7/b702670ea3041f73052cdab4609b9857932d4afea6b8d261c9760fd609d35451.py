"""Replay the N012 assembly boundary, exact evidence and native texts."""
from pathlib import Path
import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

if sys.flags.optimize:
    raise RuntimeError('Run without Python optimization')

def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def verify(base,row):
    p=(base/row['path']).resolve()
    need(p.is_relative_to(base.resolve()),'Path escapes '+row['path'])
    need(p.is_file(),'Missing '+str(p))
    need(sha(p)==row['sha256'],'Digest mismatch '+str(p))
    need(p.stat().st_size==row.get('bytes',p.stat().st_size),'Size mismatch '+str(p))
    return p

LABELS={'Theorem 2.2.1','Theorem 3.2.1','Theorem 3.2.2','Theorem 3.3.1',
 'Corollary 3.3.1','Theorem 4.2.1','Theorem 4.2.2','Corollary 4.2.1',
 'Corollary 4.2.2','Corollary 4.2.3','Theorem 4.3.1','Corollary 4.3.1'}
def boundary(scope,routes,delta):
    need(scope['originals']==['N012'],'Fixed original')
    need(scope['dimension_domain']=='n>=2','Dimension domain')
    need(scope['determinant_sign_field_domain']=='odd prime powers q','Odd field domain')
    need(scope['quotient_definition']=='H_n(q)/Z(SL_n(q))','Actual source quotient')
    need(scope['principal_claims']==12 and set(scope['principal_labels'])==LABELS,'Principal scope')
    need(len(routes['rows'])==12 and {r['source_label'] for r in routes['rows']}==LABELS,'Complete unique routes')
    need(scope['classification_tables']==2 and scope['table_rows']==12,'Both complete tables')
    need(len(routes['classification_tables'])==2 and all(len(t['rows'])==6 for t in routes['classification_tables']),'Table routes')
    need(scope['centre_cases']=={'e_even':'H/Z1=PSL; Q=PSL×C2','e_odd':'H/Z1=Q=PSL semidirect C2 embedded in PGL'},'Corrected centre cases')
    need(scope['small_exceptions']=={'GL_polytope':'q in {2,3},n>=5','PGL2_polytope':'q!=2','Q2':'q!=9','Q3':'all excluded'},'Exact negative cases')
    need(scope['corrected_numbered_claim'].startswith('Corollary 4.2.1:'),'Numbered correction retained')
    for r in routes['rows']:
        expected='CORRECTED_PRINCIPAL_ROUTE_ACCEPTED_COMPONENTS' if r['source_label']=='Corollary 4.2.1' else 'COMPLETE_ROUTE_ACCEPTED_COMPONENTS'
        need(r['status']==expected,'Current accepted route '+r['source_label'])
        need(not any('pending' in s.lower() for s in r['route']),'No current pending route')
    need(routes['closing_review']['path']=='corpus106_N012_quotient_completion_independent_review/manifest.json','Closing review required')
    need(routes['closing_review']['sha256']=='5dfe6a77b792e06a0274e9bdef67e52850a28dee728ab8f34ceecdbe089b5432','Accepted closing edition')
    need(routes['closing_adoption']['sha256']=='37ce8b90466ccfd6562cf287cff4c1b73aa11eceb94d37bb4180c65b370d11a2','Closing root adoption required')
    need(delta['product_order']=='4p' and delta['dihedral_order']=='8p','Product versus subgroup order')
    need(delta['mathematical_change'] is False and delta['frozen_author_modified'] is False,'Editorial boundary')
    need(scope['whole_original_credit']==0 and scope['proposed_principal_recovery_credit']==1,'No premature admission')
    need(scope['new_question_credit']==0 and scope['new_Lean_credit']==0,'No question/formal credit')
    need(scope['new_measurements']==0 and scope['compression_factor'] is None and scope['software_factor'] is None,'No measurements')
    need(scope['public_registration'] is False,'No public registration by this packet')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true')
    args=ap.parse_args();P=Path(__file__).resolve().parent;S=(args.study or P.parent).resolve();O=args.out.resolve()
    need(not O.exists(),'Fresh output directory required');O.mkdir(parents=True)
    exports=read(P/'manifest.json')['exports']
    for x in exports:verify(P,x)
    dep=read(P/'dependencies.json')
    for x in dep['bindings']:verify(S,x)
    for name,count in dep['acquired_packets'].items():
        mp=S/name;ms=read(mp);need(len(ms['exports'])==count,'Acquired packet cardinality')
        for x in ms['exports']:verify(mp.parent,x)
    scope=read(P/'scope.json');routes=read(P/'claim_routes.json');delta=read(P/'editorial_delta.json')
    boundary(scope,routes,delta)
    for k in ['historical_ledger','closing_author','closing_review','closing_adoption']:verify(S,routes[k])
    source=read(P/'source.json');verify(S,source['pdf']);verify(S,source['text'])
    observed={(('Theorem' if k=='Теорема' else 'Corollary')+' '+v) for k,v in re.findall(r'(Теорема|Следствие)\s+(\d+\.\d+\.\d+)',(S/source['text']['path']).read_text())}
    need(observed==LABELS,'Exact fixed-source label census')
    original=verify(S,delta['original']).read_text();edited=verify(P,delta['copy']).read_text()
    need(original.count(delta['old'])==1,'Unique editorial target')
    need(edited==original.replace(delta['old'],delta['new']),'Exact sole editorial change')
    expected=''.join(difflib.unified_diff(original.splitlines(keepends=True),edited.splitlines(keepends=True),fromfile='corpus106_N012_finite_H_v2/finite_H.tex',tofile='corpus106_N012_principal_v1/finite_H_clarified.tex'))
    need((P/delta['delta_file']).read_text()==expected,'Exact editorial diff')
    bad=[]
    mutations=[
      ('wrong_original',lambda s,r,d:s.update(originals=['N011'])),
      ('n1_domain',lambda s,r,d:s.update(dimension_domain='n>=1')),
      ('even_fields',lambda s,r,d:s.update(determinant_sign_field_domain='all prime powers q')),
      ('wrong_quotient',lambda s,r,d:s.update(quotient_definition='H_n(q)/Z(H_n(q))')),
      ('missing_claim',lambda s,r,d:r['rows'].pop()),
      ('lost_table_row',lambda s,r,d:r['classification_tables'][0]['rows'].pop()),
      ('uncorrected_centre',lambda s,r,d:s['centre_cases'].update(e_even='H/Z1=PSL semidirect C2')),
      ('q9_positive',lambda s,r,d:s['small_exceptions'].update(Q2='all q')),
      ('missing_Q_review',lambda s,r,d:r['closing_review'].update(sha256='0'*64)),
      ('wrong_dihedral_order',lambda s,r,d:d.update(dihedral_order='4p')),
      ('premature_admission',lambda s,r,d:s.update(whole_original_credit=1)),
      ('question_credit',lambda s,r,d:s.update(new_question_credit=1)),
      ('unjustified_ratio',lambda s,r,d:s.update(compression_factor=12)),
      ('pending_route',lambda s,r,d:r['rows'][0].update(status='PENDING'))]
    for name,fn in mutations:
        s,r,d=copy.deepcopy((scope,routes,delta));fn(s,r,d)
        try:boundary(s,r,d)
        except (ValueError,KeyError):bad.append(name)
        else:raise ValueError('Malformed control accepted: '+name)
    native=[]
    if args.render:
        from pypdf import PdfReader
        env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None)
        for row in read(P/'native.json')['manuscripts']:
            stem=row['stem'];N=O/stem;N.mkdir();shutil.copyfile(P/(stem+'.tex'),N/(stem+'.tex'))
            for k in [1,2]:
                with (N/f'pass{k}.log').open('wb') as f:
                    subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=N,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
            log=(N/(stem+'.log')).read_text();need('Warning' not in log and 'Overfull' not in log,'Native warnings')
            pdf=PdfReader(N/(stem+'.pdf'));need(len(pdf.pages)==row['pages'],'Page count')
            hashes=[hashlib.sha256(x.extract_text().encode()).hexdigest() for x in pdf.pages]
            need(hashes==row['page_text_sha256'],'Native text changed')
            subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r90',f'-sOutputFile={N}/page-%d.png',str(N/(stem+'.pdf'))],env=env,check=True)
            native.append(dict(stem=stem,pages=row['pages'],page_text_sha256=hashes))
    report=dict(status='PASS_N012_COMPLETE_PRINCIPAL_ASSEMBLY',author_exports=len(exports),external_bindings=len(dep['bindings']),
                acquired_packets=len(dep['acquired_packets']),acquired_exports=sum(dep['acquired_packets'].values()),
                principal_claims=12,table_rows=12,negative_controls=bad,exact_editorial_diff=True,
                historical_pending_status_superseded_by_accepted_Q=True,native=native,
                new_numerical_searches=0,whole_original_credit=0,mathematical_review_replaced_by_checks=False)
    (O/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
