"""Assemble the exact N012 principal wrapper from accepted components."""
from pathlib import Path
import difflib
import hashlib
import json
import shutil
import sys

if sys.flags.optimize:
    raise RuntimeError('No optimization')
S=Path('/Users/sasha/medusa/research/leemans')
W=S/'reboot_20261013/N012_principal_work'
P=S/'corpus106_N012_principal_v1'
P.mkdir(exist_ok=False)
W.mkdir(exist_ok=True)

def need(x,msg):
    if not x: raise ValueError(msg)
def pin(p,base=S):
    b=p.read_bytes()
    return dict(path=str(p.relative_to(base)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def write(p,obj): p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

paths=set(); packets={}; checked=0
def add(p):
    global checked
    p=p.resolve();need(p.is_relative_to(S),'Non-study dependency '+str(p));need(p.is_file(),'Missing '+str(p))
    if p in paths:return
    paths.add(p)
    if p.suffix!='.json':return
    d=json.loads(p.read_text())
    if not isinstance(d,dict):return
    if p.name=='manifest.json' and 'exports' in d:
        packets[str(p.relative_to(S))]=len(d['exports'])
        for row in d['exports']:
            q=p.parent/row['path'];need(q.resolve().is_relative_to(p.parent.resolve()),'Escaping export')
            v=pin(q);need(v['sha256']==row['sha256'] and v['bytes']==row.get('bytes',v['bytes']),'Changed export '+str(q))
            checked+=1;add(q)
    bindings=d.get('bindings',[])
    if not isinstance(bindings,list):return
    for row in bindings:
        q=S/row['path'];v=pin(q)
        need(v['sha256']==row['sha256'] and v['bytes']==row.get('bytes',v['bytes']),'Changed binding '+str(q))
        checked+=1;add(q)

seeds=['corpus106_N011_recovery','corpus106_N011_root_review',
 'corpus106_N012_integral_v1','corpus106_N012_integral_independent_review','corpus106_N012_integral_root_adoption',
 'corpus106_N012_central_quotients_v1','corpus106_N012_central_quotients_independent_review','corpus106_N012_central_quotients_root_adoption',
 'corpus106_N012_finite_H_v2','corpus106_N012_finite_H_independent_review','corpus106_N012_finite_H_root_adoption',
 'corpus106_N012_quotient_completion_v1','corpus106_N012_quotient_completion_independent_review','corpus106_N012_quotient_completion_root_adoption',
 'corpus106_N012_source_contract_work']
for name in seeds:add(S/name/'manifest.json')

shutil.copyfile(S/'reboot_20261013/N012_source_recovery.tex',P/'source_recovery.tex')
for n in ('principal_ledger.json','dependency_routes.json','contract_audit.rst'):
    shutil.copyfile(S/'corpus106_N012_source_contract_work'/n,P/('historical_'+n))
old=json.loads((S/'corpus106_N012_source_contract_work/principal_ledger.json').read_text())
routes=[]
for row in old['principal_claims']:
    x=dict(row);x['historical_status']=x['status'];x['status']=('CORRECTED_PRINCIPAL_ROUTE_ACCEPTED_COMPONENTS' if x['source_label']=='Corollary 4.2.1' else 'COMPLETE_ROUTE_ACCEPTED_COMPONENTS')
    x['historical_route']=x['route']
    x['route']=[s.replace('its distinct review is pending.', 'its distinct review and root adoption are acquired.').replace('distinct review pending.', 'distinct review and root adoption acquired.') for s in x['route']]
    routes.append(x)
write(P/'claim_routes.json',dict(rows=routes,classification_tables=old['classification_tables'],
    historical_ledger=pin(S/'corpus106_N012_source_contract_work/manifest.json'),
    closing_author=pin(S/'corpus106_N012_quotient_completion_v1/manifest.json'),
    closing_review=pin(S/'corpus106_N012_quotient_completion_independent_review/manifest.json'),
    closing_adoption=pin(S/'corpus106_N012_quotient_completion_root_adoption/manifest.json'),
    historical_status_supersession='The frozen ledger predates Q acceptance. This wrapper acquires its exact distinct review and root adoption; no old packet is edited.',
    whole_original_credit=0))

original=S/'corpus106_N012_finite_H_v2/finite_H.tex'
old_text=original.read_text()
before='Its order $4p$ and the distinctness of the\nthree involutions persist.'
after='The product $AC$ retains order $4p$, while the dihedral subgroup\n$\\langle A,C\\rangle$ retains order $8p$. The three involutions remain\ndistinct.'
need(old_text.count(before)==1,'Exact finite-H editorial target')
edited=old_text.replace(before,after)
(P/'finite_H_clarified.tex').write_text(edited)
diff=''.join(difflib.unified_diff(old_text.splitlines(keepends=True),edited.splitlines(keepends=True),
      fromfile='corpus106_N012_finite_H_v2/finite_H.tex',tofile='corpus106_N012_principal_v1/finite_H_clarified.tex'))
(P/'finite_H_editorial.diff').write_text(diff)
write(P/'editorial_delta.json',dict(original=pin(original),copy=pin(P/'finite_H_clarified.tex',P),
    old=before,new=after,delta_file='finite_H_editorial.diff',
    reason='Remove the ambiguous pronoun in the scalar-quotient proof: the product AC has order 4p and its dihedral subgroup has order 8p.',
    mathematical_change=False,frozen_author_modified=False,product_order='4p',dihedral_order='8p'))

write(P/'source.json',dict(id='N012',author='Irina Alexandrovna Markovskaya',supervisor='Yakov Nifantievich Nuzhin',
    title=old['source']['title'],year=2025,pages=80,edition='Fixed supplied thesis edition',
    pdf=pin(S/'sources/phase22_markovskaya_thesis.pdf'),text=pin(S/'sources/phase22_markovskaya_thesis.txt')))
write(P/'scope.json',dict(status='AUTHOR_COMPLETE_CORRECTED_PRINCIPAL_RECOVERY_PENDING_WHOLE_REVIEW',
    originals=['N012'],principal_labels=[r['source_label'] for r in routes],principal_claims=12,
    classification_tables=2,table_rows=12,dimension_domain='n>=2',
    determinant_sign_field_domain='odd prime powers q',quotient_definition='H_n(q)/Z(SL_n(q))',
    corrected_numbered_claim='Corollary 4.2.1: structural clause split by parity of e=(q-1)/gcd(n,q-1); existence and type preserved.',
    centre_cases={'e_even':'H/Z1=PSL; Q=PSL×C2','e_odd':'H/Z1=Q=PSL semidirect C2 embedded in PGL'},
    small_exceptions={'GL_polytope':'q in {2,3},n>=5','PGL2_polytope':'q!=2','Q2':'q!=9','Q3':'all excluded'},
    supporting_lemmas_not_all_reproved=True,external_classifications_retained=True,
    whole_original_credit=0,proposed_principal_recovery_credit=1,new_question_credit=0,new_Lean_credit=0,
    new_measurements=0,compression_factor=None,software_factor=None,public_registration=False))
write(P/'provenance.json',dict(wrapper_author='publication_recovery',
    component_authors={'integral':'f003_resume','finite_H_and_centre_and_Q':'root','N011':'rewrite_termination'},
    independent_review_chains={'integral':'publication_recovery; root integration','centre':'publication_recovery; root integration',
      'finite_H_v2':'publication_recovery; root integration','Q':'f003_resume; root integration','N011':'root distinct review'},
    wrapper_role='The wrapper author wrote the source contract audit and reviewed prior components but did not author their mathematical arguments. Root must review this new whole-source assembly and the explicit editorial delta.',
    original_priority='The principal source results and matrices remain attributed to Markovskaya and the collaborators explicitly credited on source pp6–8.',
    earlier_project_reuse='Phase22 detected the degree-four witness defect; N011 contains the acquired finite common and application proofs.',
    novelty_claim=False,source_is_new_intake=False))

proofs=[]
for key,folder,stem in [('I','corpus106_N012_integral_v1','integral_groups'),('U','corpus106_N011_recovery','root_parameters'),
 ('L','corpus106_N011_recovery','linear_classification'),('Z','corpus106_N012_central_quotients_v1','central_quotients'),
 ('H','corpus106_N012_finite_H_v2','finite_H'),('Q','corpus106_N012_quotient_completion_v1','quotients_and_classification')]:
    from pypdf import PdfReader
    proofs.append(dict(key=key,tex=pin(S/folder/(stem+'.tex')),pdf=pin(S/folder/(stem+'.pdf')),pages=len(PdfReader(S/folder/(stem+'.pdf')).pages)))
write(P/'manuscripts.json',dict(assembly='source_recovery.pdf',acquired_complete=proofs,
    editorial_copy='finite_H_clarified.pdf',editorial_original_retained=True,
    integral_premise_substitution='I replaces L\'s formerly external integral-generation input without changing any frozen L bytes.',
    required_proof_order=['explicit external inputs','I and U','L','Z','H','Q','whole assembly'],measurement=None))

primary=[]
for p in sorted(paths):
    rel=str(p.relative_to(S)); name=p.name
    if rel.startswith('sources/') or 'source_page_' in name or (p.suffix=='.png' and (name.startswith('source') or '/source_native' in rel)):
        primary.append(rel)
write(P/'dependencies.json',dict(bindings=[pin(p)for p in sorted(paths)],acquired_packets=packets,
    primary_files_hash_only=primary,
    complete_external_proof_costs=None,complete_external_software_costs=None,
    retained_inputs=['Specified simple-linear admissibility classification','Sjerve–Cherkassoff PGL2 theorem',
                     'Conder–Oliveros intersection criterion','String C-group and regular-polytope correspondence'],
    existing_finite_evidence='All literal integral and finite-H arithmetic programs, expected outputs and distinct replay records are acquired unchanged; no new census is required.'))
write(P/'collection_report.json',dict(status='PASS_ACQUIRED_CLOSURE',acquired_packets=len(packets),
    acquired_files=len(paths),verified_export_and_dependency_records=checked,primary_hash_only_files=len(primary),all_frozen_packets_unchanged=True))
(P/'README.rst').write_text('N012: complete corrected principal recovery\n==========================================\n\n'
 'Read source_recovery.pdf and all six complete companion papers named in manuscripts.json.\n'
 'All twelve principal claims and both six-row source tables have explicit routes.\n'
 'Corollary 4.2.1 has a corrected structural clause; its polytope existence and type survive.\n'
 'Q means H/Z(SL), not H/Z(H). The historical contract audit is retained unchanged;\n'
 'claim_routes.json adds the subsequent closing-component acceptance and adoption.\n'
 'finite_H_clarified.tex changes only the ambiguous order sentence, as recorded in the exact diff.\n'
 'The original finite_H_v2 proof and all accepted source/component/review packets are unchanged.\n'
 'This candidate grants no public admission, conjecture, Lean or numerical compression credit.\n')
print(json.dumps(dict(status='ASSEMBLED_NOT_YET_FROZEN',path=str(P),files=len(paths),packets=len(packets),records=checked)))
