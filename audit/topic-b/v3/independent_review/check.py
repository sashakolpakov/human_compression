#!/usr/bin/env python3
"""Replay the bounded independent review. Mathematical reading is not automated."""
import argparse
import copy
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from pypdf import PdfReader

HERE=Path(__file__).resolve().parent
AUTHOR_PIN='21aeba398dfda4766d3ff441032672ddde2efdac14fef8f67258c971dd827965'
SOURCES=['N001','N003','N008','L030','L040']
ROLES=['required_finite_primitive_inputs','finite_validation','finite_validation','required_only_for_auxiliary_n8_and_validation_of_branching']
DECLARATIONS={'formal-relative/ResidualGeneration.lean':(6,'61ae91456d347169c7d86ebc886ca94a71bdb7869f67ecb1712118af81dde871'),
              'formal-normalization/IrredundantNormalization.lean':(8,'07544a53f051511dedcfd3dd5d81fa2db603e315cc2832a23fde4d109b5925a9')}

def need(b,m):
    if not b:raise ValueError(m)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(base,r):
    rel=Path(r['path']);need(not rel.is_absolute() and '..' not in rel.parts,'safe relative binding')
    p=base/rel;need(p.is_file() and p.stat().st_size==r['bytes'] and digest(p)==r['sha256'],'binding '+str(p))
def manifest(base,pin=None):
    f=base/'manifest.json'
    if pin:need(digest(f)==pin,'manifest pin '+str(base))
    m=read(f);paths=[r['path'] for r in m['exports']];need(len(paths)==len(set(paths)),'unique exports')
    for r in m['exports']:bound(base,r)
    return m

def semantics(s,old,high):
    need(s['original_sources']==SOURCES and s['original_count']==5,'five source identities')
    need(len(s['source_rows'])==s['source_row_count']==65,'65 complete dispositions')
    for current,prior in zip(s['source_rows'][:30],old['rows']):
        need(current['inherited_record']==prior and current['unchanged_disposition']==prior['verdict'] and current['target']==prior['source_contract'],'unchanged corrected B contract')
    for current,prior in zip(s['source_rows'][30:],high['contracts']):
        need(current['inherited_record']==prior and current['unchanged_disposition']==prior['status'] and current['target']==prior['target'],'unchanged L040 contract')
    need(len(s['proof_contexts'])==56,'56 complete proof contexts')
    for r in s['source_rows']:
        need(r['current_proof_nodes'] and all(k in s['proof_contexts'] for k in r['current_proof_nodes']+r['current_shared_interfaces']),'actual current contexts')
    routes={r['source_reference']:set(r['current_proof_nodes']+r['current_shared_interfaces']) for r in s['source_rows']}
    need({'A.Maximum','UB.Extremal','UB.Sign','UB.F','UB.Coset'}<=routes['L040.T1.1'],'maximum-rank complete transfer')
    need({'A.Cores','A.Fracture','A.Splitting','A.Elimination','A.Exhaustion','A.FlagCompletion','UB.Laminar','U.Attachment','UB.Coset'}<=routes['L040.T1.2'],'full fracture/attachment transfer')
    need({'A.Coordinates','A.Decoration','A.FlagCompletion','UB.Laminar','U.Attachment','UB.Coset'}<=routes['L040.T6.6'],'actual prescribed-root flag transfer')
    need({'UB.Extremal','UB.Sign','UB.F'}<=routes['Corollary 2.3'],'arbitrary-family intersection requires classification')
    need([p['role'] for p in s['programs']]==ROLES and all(p['whole_file_printed'] for p in s['programs']),'whole programs and roles')
    need({r['module']:r['declarations'] for r in s['formal_evidence']}=={k:v[0] for k,v in DECLARATIONS.items()},'14 reused partial declarations')
    need(s['reused_partial_declarations']==14 and all(s[k]==0 for k in ['new_formal_declarations','new_source_credit','new_question_credit']),'no extra credit')
    need(s['compression_factor'] is None and not s['complete_formalization_claim'] and not s['unpriced_application_imports'],'scope and no factor')
    for k in ['whole_common_charged_once','all_five_complete_applications','all_four_complete_programs_visible']:need(s['boundaries'][k] is True,'complete acquisition '+k)
    for k in ['retained_external_proof_cost','source_graphics_cost','historical_software_cost','full_formalization_cost']:need(s['boundaries'][k] is None,'unknown '+k)

def audit(author,study,public):
    am=manifest(author,AUTHOR_PIN);need(len(am['exports'])==52,'52 frozen author exports')
    s=read(author/'scope.json');old=read(public/'papers/topic-b/v2/mapping_correction/source_contract_map.json');high=read(study/'corpus161_L040_recovery/scope.json')
    semantics(s,old,high)
    for r in s['inherited_inputs']:bound(study if r['root']=='study' else public,r)
    for r in s['primary_editions']:bound(study,r)
    for r in s['prior_scientific_replays']:bound(public,r)
    # Bind full distinct earlier acceptances, not merely their prose conclusions.
    priors=[]
    for path,pin in [('audit/topic-b/v2/independent_review','d224742e25167983954dc1421cbb4a09853aad47feb5ef9b84378249e6d1e6c5'),
                     ('audit/topic-b/extensions/high-rank/v1/independent_review','ed6efea4c337765c2bd8ccb4fc34582c1f54426e64ab66302ac93ce8d602a930')]:
        m=manifest(public/path,pin);priors.append({'path':path,'exports':len(m['exports']),'sha256':pin})
    for key,r in s['proof_contexts'].items():
        t=(author/r['path']).read_text();a,b=r['start_codepoint'],r['end_codepoint_exclusive']
        need(0<=a<b<=len(t) and hashlib.sha256(t[a:b].encode()).hexdigest()==r['sha256_utf8'],'complete statement/proof '+key)
    transfers=read(author/'transfer.json')
    for r in transfers['transfers']:
        bound(study,r['before']);bound(author,r['after'])
        need(((study/r['before']['path']).read_bytes()==(author/r['after']['path']).read_bytes())==r['identical_bytes'],'truthful exact transfer')
    for p,q in zip(s['programs'],high['program_inventory']):
        bound(author,p);need((p['sha256'],p['bytes'])==(q['sha256'],q['bytes']),'literal complete prior program')
    for path,(count,sha) in DECLARATIONS.items():need(digest(author/path)==sha,'same accepted formal source')
    retained_text=[]
    for row in transfers['unchanged_application_pdf_text']:
        before=PdfReader(study/row['before']['path']);after=PdfReader(author/row['after']['path'])
        need([p.extract_text() or '' for p in before.pages]==[p.extract_text() or '' for p in after.pages],'identical inherited application page text')
        retained_text.append({'name':row['name'],'pages':len(after.pages)})
    tex_inputs=re.findall(r'\\VerbatimInput\[[^\]]*\]\{([^}]+)\}',(author/'program-appendix.tex').read_text())
    need(tex_inputs==[p['path'] for p in s['programs']],'whole four-file appendix inputs')
    pieces=[]
    for p in PdfReader(author/'program-appendix.pdf').pages:
        def visit(text,cm,tm,font,size):
            if font and 'Menlo' in str(font.get('/BaseFont','')):pieces.append(text)
        p.extract_text(visitor_text=visit)
    compact=lambda t:''.join(c for c in t if not c.isspace())
    need(compact(''.join(pieces))==compact(''.join((author/p).read_text() for p in tex_inputs)),'complete visible code bytes modulo layout whitespace')
    controls=[]
    edits=[('drop source row',lambda q:q['source_rows'].pop()),
           ('endorse literal branching error',lambda q:next(r for r in q['source_rows'] if r['source_reference']=='L040.C6.5.2').update(unchanged_disposition='recovered_complete')),
           ('remove common classification',lambda q:next(r for r in q['source_rows'] if r['source_reference']=='L040.T1.1')['current_proof_nodes'].remove('UB.Extremal')),
           ('omit decorated flag premise',lambda q:next(r for r in q['source_rows'] if r['source_reference']=='L040.T6.6')['current_proof_nodes'].remove('A.Decoration')),
           ('treat IP as direct sign corollary for arbitrary family',lambda q:next(r for r in q['source_rows'] if r['source_reference']=='Corollary 2.3')['current_proof_nodes'].remove('UB.Extremal')),
           ('hide required primitive certificate',lambda q:q['programs'][0].update(role='finite_validation')),
           ('new formal credit',lambda q:q.update(new_formal_declarations=14)),
           ('claim full formalization',lambda q:q.update(complete_formalization_claim=True)),
           ('unpaid common theory',lambda q:q['boundaries'].update(whole_common_charged_once=False)),
           ('invent measured factor',lambda q:q.update(compression_factor=2)),
           ('zero retained proof cost',lambda q:q['boundaries'].update(retained_external_proof_cost=0))]
    for name,edit in edits:
        q=copy.deepcopy(s);edit(q)
        try:semantics(q,old,high)
        except ValueError:controls.append(name)
        else:raise ValueError('mutation accepted '+name)
    return dict(status='PASS',author_manifest_sha256=AUTHOR_PIN,author_exports=52,source_rows=65,proof_contexts=56,
                inherited_transfer_pairs=len(transfers['transfers']),unchanged_applications=retained_text,complete_programs=4,
                reused_partial_Lean_declarations=14,new_Lean_declarations=0,prior_acceptances=priors,semantic_controls=controls,
                mathematical_reading_verified_by_this_program=False,new_factor_evaluated=False)

def main():
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True);p.add_argument('--public-root',type=Path,required=True);p.add_argument('--author-root',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--models',action='store_true');a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output required');a.out.mkdir(parents=True)
    if (HERE/'manifest.json').exists():manifest(HERE)
    r=audit(a.author_root or a.study_root/'topic_B_unified',a.study_root,a.public_root)
    if a.models:
        cmd=[sys.executable,'-B','-O',str(HERE/'local_interfaces.py'),'--out',str(a.out/'local_interfaces.json')]
        proc=subprocess.run(cmd,capture_output=True,text=True);(a.out/'models.stdout').write_text(proc.stdout);(a.out/'models.stderr').write_text(proc.stderr)
        need(proc.returncode==0,'independent finite interface replay');r['finite_interfaces']=read(a.out/'local_interfaces.json')
    (a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
if __name__=='__main__':main()
