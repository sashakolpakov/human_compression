"""Draft assembly map: accepted proof reuse, no group or measurement calculation."""
from pathlib import Path
import collections,copy,csv,difflib,hashlib,json,re,shutil
P=Path(__file__).resolve().parent;S=P.parent;PUBLIC=S.parents[1]/'math_compression'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,d):(P/n).write_text(json.dumps(d,indent=2)+'\n')
def file(p,root='study'):
 q=(S if root=='study' else PUBLIC)/p
 return dict(root=root,path=p,bytes=q.stat().st_size,sha256=sha(q))
base=S/'topic_A_L003_candidate_v2';shared=S/'topic_A_L003_shared_structures';finite=S/'topic_A_L003_structural_completion'
old=load(S/'topic_A_L003_assembly_assessment/claim_map.json');d=copy.deepcopy(old)
pr={x['id']:x for x in load(finite/'results.json')['rows']}
for r in d['rows']:
 if r['id'] in pr:
  r.update(assembly_status='STRUCTURE_ACCEPTED_DISTINCT_ROOT_REVIEW',principal_gap_after_accepted_inputs=False,structural_route='topic_A_L003_structural_completion: whole 4-page paper and full computational/data closure; root cc99fba9',current_structure=pr[r['id']]['shape'],current_source_structure_status=pr[r['id']]['status'],authorship='enumeration_review; distinct root review')
  for k in ['author_reported_structure','author_reported_status','specific_open_gate']:r.pop(k,None)
 if r['id']=='Section9_genus4_example':
  r.update(assembly_status='ISOLATED_ASSERTION_ACCEPTED_SEPARATELY',proof_route='topic_A_L003_order768: complete two-page proof and verify.g; distinct review 1fc4afb7',principal_gap_after_accepted_inputs=False)
  r.pop('specific_remaining_assertion',None)
 if r['id']=='Section3_correlations4_5':
  r.update(assembly_status='NINE_CLAUSE_CORRELATION_SUCCESSOR_ACCEPTED',principal_gap_after_accepted_inputs=False,subclauses=load(S/'topic_A_L003_correlation_reduction/source_contract.json')['rows'],accepted_author_manifest='97b87353cfaf76f960d0fbe542ad4bea4eafe124a2a985c0051414897460da97')
d['status']='AUTHOR_COMPLETE_ASSEMBLY_PENDING_DISTINCT_REVIEW';d['counts']=dict(collections.Counter(x['assembly_status'] for x in d['rows']));d['scientific_gate']='Final complete migration review; every previously pending principal proof prerequisite is accepted. Source diagram5 experimental existence remains qualified as in the source.'
d['all42_structural_assertions_accepted']=True;d['whole_original_accepted_here']=False
dump('claim_map.json',d)
with (P/'claim_map.csv').open('w',newline='') as f:
 w=csv.writer(f);w.writerow(['id','source_pages','assembly_status','principal_gap','route'])
 for r in d['rows']:w.writerow([r['id'],r['source_pages'],r['assembly_status'],r['principal_gap_after_accepted_inputs'],r.get('structural_route',r.get('proof_route','pending correlation'))])
# Bind complete whole files, retaining repeated occurrences before byte-level union.
occ=[]
def add(root,path,role,basis):
 x=file(path,root);x.update(role=role,role_basis=basis,whole_file=True);occ.append(x)
for r in load(S/'topic_A_L121_measurement_inputs/precount/raw_inventory.json')['files']:
 x=r['file'];add(x['root'],x['path'],r['role'],'unchanged accepted A9 inventory: '+r.get('scientific_role',''))
for r in load(base/'program_inventory.json')['whole_files']:add('study',r['path'],r['role'],'complete candidate v2 inventory')
for r in load(shared/'program_inventory.json')['whole_files']:add('study','topic_A_L003_shared_structures/'+r['path'],r['role'],'accepted shared structural companion')
fi=load(finite/'program_inventory.json')
for key,role in [('required_whole_mathematical_files','required mathematical program'),('required_whole_input_data','required complete mathematical input data'),('optional_validation','optional validation'),('operational_driver','operational driver')]:
 for r in fi[key]:add('study','topic_A_L003_structural_completion/'+r['path'],role,'accepted finite structural inventory: '+r.get('role',key))
# Whole saved image receipts are the input to named and recursive structural proofs.
for f in sorted((base/'certificates').glob('*.log')):add('study',str(f.relative_to(S)),'required complete accepted marked-image data','universal/geometry receipts, consumed by structural identifications; retain entire file')
for folder in [base/'structural_certificates',finite/'certificates']:
 for f in sorted(folder.glob('*.log')):add('study',str(f.relative_to(S)),'complete output receipt','retained exact witness output, separate from required algorithms')
add('study','topic_A_L003_structural_completion/obstruction_certificate.log','complete output receipt','accepted T4.8 nonsplitting obstruction')
for path,role in [('verify.g','required mathematical program'),('check.py','operational driver')]:add('study','topic_A_L003_order768/'+path,role,'accepted isolated order768/genus4 example')
# Accepted correlation diagnostics are optional, not uniform proof premises.
for path,role in [('word_checks.py','optional validation'),('check.py','operational driver')]:add('study','topic_A_L003_correlation_reduction/'+path,role,'accepted exact presentation correlation supplement')
groups={}
for r in occ:
 key=r['sha256'];g=groups.setdefault(key,dict(sha256=key,bytes=r['bytes'],occurrences=[],roles=[]));assert g['bytes']==r['bytes'];g['occurrences'].append(dict(root=r['root'],path=r['path'],role=r['role']));g['roles']=sorted(set(g['roles']+[r['role']]))
dump('whole_file_inventory.json',dict(status='DRAFT_COMPLETE_OCCURRENCE_UNION_NOT_METRIC_COUNTS',occurrences=occ,unique_contents=list(groups.values()),deduplication='Only exact complete content SHA256 equality within this enlarged topic; all occurrence roles retained. No proof or program pruning.',new_measurements=False,software_inclusive_factor=None,printed_code_boundary='Existing three code PDFs cover only old eleven-file subset; there is no complete enlarged printed code representation.'))
# A minimal application successor; unchanged mathematical environments are separately checked.
text=(base/'hexagonal_extensions.tex').read_text();oldtext=text
text=text.replace('\\date{Private mathematical draft; complete review pending}','\\date{}')
text=text.replace('longtable,hyperref}', 'longtable,array,hyperref}')
start=text.index('\\section{Structural columns: verified models and explicit limits}')
end=text.index('The required \\path{structural_groups.py}',start)
text=text[:start]+r'''\section{Structural columns and corrected extension claims}
Every one of the 73 printed group descriptions is retained in the ledger.
V denotes one of the 29 previously verified named isomorphisms. F denotes
one of the 35 complete recursive normal-subgroup, quotient and complement
certificates in the whole structural companion~\cite{finite-structures}.
S denotes one of the seven shared affine or finite structural proofs in
\cite{shared-structures}; O records a printed order incompatible with the
literal universal group. The two complete companion proofs and their
whole required programs and input data are part of this proof boundary.
An unnamed action does not remove the obligation to prove normality,
the quotient, or a stated splitting. Conversely, verifying a bracketed
extension shape does not claim it uniquely identifies all abstract groups
with those factors.

Thirty-four F rows verify the printed shape under explicit brackets.
For T4.8, the asserted split stage must instead be dotted:
\[
 \bigl((2^{5+6}.(A_5\times C_3)):S_3\bigr):S_3.
\]
The companion supplies both the corrected positive shape and the
obstruction to the printed splitting. Its perfect terminal derived
subgroup of order 120 cannot have an index-two subgroup isomorphic to
$A_5$; the complete subgroup argument is retained there.
The seven S rows have explicit normal factors and complements, including
the uniform square-family splitting for every positive parameter.
No new geometry is inferred solely from these structural descriptions.

'''+text[end:]
oldparagraph='''Source Tables 1--2 and Theorems 3.1--3.3 quote earlier classifications
and remain retained inputs. Experiments and suggested correlation
constructions around diagrams 4--5, and bounded failed searches in
Section 8, are documentary; they are not newly proved classifications
or nonexistence theorems. The source restricts its investigation to
the first three diagrams.'''
newparagraph='''Source Tables 1--2 and Theorems 3.1--3.3 quote earlier classifications
and remain retained inputs. Diagram (4)'s asserted presentation reduction
is distinguished from diagram (5)'s explicitly experimental existence
claim. The complete correlation companion~\\cite{correlations} proves inverse
presentation maps and both parameter transformations for every positive
integer parameter. For each existing regular universal fork hypertope,
its actual prescribed residues give the corresponding universal string
polytope and recover the fork marking. Its correct rank-four generator
list contains the fourth generator omitted in the source parenthesis.
For diagram (5), the exact group and conditional intersection-property
claims are proved, while the experimental flag-transitivity and existence
claim remains qualified. There is no unrestricted converse from a parity
character alone. The whole four-page companion is part of this application.
Bounded failed searches in Section 8 are documentary, not nonexistence
theorems. The source's principal finite tables concern the first three
diagrams.'''
assert oldparagraph in text;text=text.replace(oldparagraph,newparagraph)
pos=text.index('\\section{Full source boundaries and questions}')
text=text[:pos]+r'''\section{The isolated nonorientable example}
The complete separate note~\cite{order768} verifies the source's
pp.~18--19 assertion about
$\{\{4,4\}_{(4,0)},\{4,6\}_3\}$.
The literal universal group has order 768 and local orders 128 and 48.
All 256 marked subgroup intersections and the local universal maps are
checked. The vertex figure has face counts $(4,12,6)$ and a closed flag
walk of odd length nine, so it has nonorientable genus four.
The entire two-page argument and its exact finite-presentation program
are required parts of this application; the displayed permutation image
alone is not used as a universal upper bound. This is verification of an
isolated source assertion, not an answer to a subsequent open question.

'''+text[pos:]
text=text.replace('\\end{thebibliography}',r'''\bibitem{shared-structures} \emph{The seven shared group structures in the hexagonal tables},
complete accepted shared structural companion, four pages.
\bibitem{finite-structures} \emph{Checking the structural descriptions of finite
hexagonal extensions}, complete accepted structural companion, four pages.
\bibitem{order768} \emph{A locally toroidal polytope with a nonorientable vertex
figure}, complete accepted companion, two pages.
\bibitem{correlations} \emph{Correlation reductions and the exact square-torus
parameters}, complete accepted companion, four pages.
\end{thebibliography}''')
(P/'hexagonal_extensions.tex').write_text(text)
for name in ['finite_table.tex','local_corrections.tex']:shutil.copy2(base/name,P/name)
table=(base/'structural_table.tex').read_text().replace(r'p{.46\linewidth}',r'>{\raggedright\arraybackslash}p{.46\linewidth}');sr={x['id'] for x in load(shared/'scope.json')['rows']}
lines=[]
for line in table.splitlines():
 ident=line.split(' & ')[0]
 if ident in pr:
  first=line.split(' & ')[:2];label='F: corrected nonsplit stage; complete companion proof.' if ident=='T4.8' else 'F: full normal-factor and splitting certificate; explicit brackets in companion.'
  line=' & '.join(first+[label])+r'\\'
 elif ident in sr:
  first=line.split(' & ')[:2];line=' & '.join(first+['S: complete shared normal-factor and complement proof.'])+r'\\'
 lines.append(line)
(P/'structural_table.tex').write_text('\n'.join(lines)+'\n')
# No mathematical statement/proof environment was shortened in this application.
pat=r'\\begin\{(theorem|proposition|proof)\}[\s\S]*?\\end\{\1\}'
envs=lambda t:[m.group(0) for m in re.finditer(pat,t)]
assert envs(oldtext)==envs(text)
dump('application_migration.json',dict(predecessor=file('topic_A_L003_candidate_v2/hexagonal_extensions.tex'),unchanged_theorem_proof_environments=len(envs(text)),changes=['replace stale42 structural qualifications with all accepted full companion routes','retain T4.8 corrected nonsplit shape explicitly','include isolated order768 complete companion route','split pending diagram4 bridge from experimental diagram5','remove transient draft date; add precise whole companion citations'],all_original_mathematical_environments_unchanged=True,complete_companions_mandatory=True,correlation_review_pending=False))
(P/'application_changes.diff').write_text(''.join(difflib.unified_diff(oldtext.splitlines(True),text.splitlines(True),fromfile='candidate_v2/hexagonal_extensions.tex',tofile='assembly/hexagonal_extensions.tex')))
proofs=[('public','papers/topic-a/v3/umbrella.pdf','whole unchanged common',23),('study','topic_A_L003_candidate_v2/shared_supplement.pdf','whole common addition with four complete moved L121 proof bodies',14),('study','topic_A_L003_shared_structures/shared_structures.pdf','whole shared common structural companion',4),('study','topic_A_L003_candidate_v2/l121_adapter.pdf','whole replacement L121 application; old11pages historical only',1),('study','topic_A_L003_structural_completion/structural_completion.pdf','whole L003 application structural companion',4),('study','topic_A_L003_order768/order768.pdf','whole L003 application isolated-example companion',2),('study','topic_A_L003_correlation_reduction/correlation_reduction.pdf','whole L003 correlation companion; root1243885b',4)]
# Resolve literal name from frozen supplement exports.
if not (S/proofs[-1][1]).exists():
 q=next(x['path'] for x in load(S/'topic_A_L003_correlation_reduction/manifest.json')['exports'] if x['path'].endswith('.pdf'));proofs[-1]=('study','topic_A_L003_correlation_reduction/'+q,proofs[-1][2],4)
dump('written_routes.json',dict(status='DRAFT_COMPLETE_ASSEMBLY_PENDING_MIGRATION_REVIEW',whole_proofs=[dict(file=file(path,root),role=role,pages=pages) for root,path,role,pages in proofs],unchanged_eight_applications='All eight complete public A v3 applications remain unchanged and fully paid; exact current document map is bound separately.',changed_application='hexagonal_extensions.tex plus mandatory whole source-specific companions; no skipped proof body',conditional_acquisition='Full U23 + common14 + shared structures4 + full declared required program/data closure. Each application pays its own complete manuscript companions.',source_count_credit=0,ratios=None))
manifestpaths=['topic_A_L003_candidate_v2','topic_A_L003_bounded_root_adoption','topic_A_L003_shared_structures','topic_A_L003_shared_structures_root_review','topic_A_L003_structural_completion','topic_A_L003_structural_root_review','topic_A_L003_order768','topic_A_L003_order768_independent_review','topic_A_L003_order768_root_adoption','topic_A_L003_correlation_reduction','topic_A_L003_correlation_root_review','topic_A_L121_measurement_inputs']
dump('accepted_input_bindings.json',dict(inputs=[dict(file=file(x+'/manifest.json'),status='RETAINED_ACCEPTED_CHAIN') for x in manifestpaths],source=file('sources/catalogue_L003.pdf'),old_document_map=file('topic_A_L121_measurement_inputs/precount/documents.json'),whole_original_accepted=False))
print(json.dumps(dict(dispositions=len(d['rows']),status_counts=d['counts'],whole_file_occurrences=len(occ),unique_whole_contents=len(groups),unchanged_proof_environments=len(envs(text))),indent=2))
