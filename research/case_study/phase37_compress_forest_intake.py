"""Build the three-paper intake/target ledger without assigning a length ratio."""
from pathlib import Path
import hashlib,json,re,copy
ROOT=Path(__file__).resolve().parent
MS='phase37_compress_forest_manuscript.md'
A=json.loads((ROOT/'phase36_compress_forest_intake.json').read_text())
C=json.loads((ROOT/'phase36_compress_forest_N008_intake.json').read_text())
assembly=json.loads((ROOT/'phase37_compress_forest_assembly.json').read_text())
s=(ROOT/MS).read_text()
def sha(data):return hashlib.sha256(data).hexdigest()
def bind(name):
 data=(ROOT/name).read_bytes()
 return {'path':name,'absolute_path':str(ROOT/name),'bytes':len(data),'sha256':sha(data)}
def span(text,a,b):return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(text[a:b].encode())}
# Validate every primary input and every source anchor anew.
for f in A['source_files']+C['source']['files']:
 assert bind(f['path'])['sha256']==f['sha256'],f['path']
for filename in ['phase36_compress_forest_recent_audit.json','phase36_compress_forest_N008_recent_audit.json']:
 assert bind(filename)['sha256']==assembly['assembly_inputs'][filename],filename

matches=list(re.finditer(r'\*\*Corollary ([ABC]\d+) —',s))
expected=[f'A{i}' for i in range(1,5)]+[f'B{i}' for i in range(1,9)]+[f'C{i}' for i in range(1,12)]
assert [m.group(1) for m in matches]==expected
adapters={}
for i,m in enumerate(matches):
 end=matches[i+1].start() if i+1<len(matches) else s.index('## 8. Main-result contract',m.start())
 adapters[m.group(1)]=span(s,m.start(),end)

targets=copy.deepcopy(A['targets'])
for t in targets:
 t['replacement_span']=adapters[t['adapter']]
 t['replacement_file']=MS
 t['mathematical_status']='integrated_v2_corollary_pending_new_integration_review'
 t['component_review']='two-paper manuscript independently reviewed under the declared scope'
 if t['adapter']=='A3':
  t['interpretive_note']+=' A middle explicitly requires at least two deletion components; the one-vertex diagram has none.'

c_bg={
 'C1':['Elementary','Zorn_if_infinite_extension'],
 'C2':['Elementary','Zorn_if_infinite_group'],
 'C3':['Elementary_subgroup_correspondence'],
 'C4':['Elementary','Zorn_if_infinite_group'],
 'C5':['Elementary','Zorn_if_infinite_group'],
 'C6':['Elementary'],
 'C7':['Elementary_vector_spaces'],
 'C8':['Elementary','PΦ'],
 'C9':['Elementary','PΦ'],
 'C10':['Elementary','Zorn_if_infinite_group'],
 'C11':['Elementary','Zorn_if_infinite_group_for_Frattini_containment']}
for t in C['all_numbered_items']+C['unnumbered_target_items']:
 if not t['adapter']:continue
 k=t['adapter']
 item={'adapter':k,'paper':'N008','source_reference':t.get('source_result',t.get('source_reference')),'full_source_formulation_normalized':t['full_normalized_formulation'],'source_file':C['source']['files'][1]['path'],'source_span':t['source_anchor'],'printed_pages':t['printed_pages'],'common_result':t['proof'].replace('existing Compress_A Theorem R(b)','Theorem R(b) of this integrated manuscript'),'adapter_argument':s[adapters[k]['start_codepoint']:adapters[k]['end_codepoint_exclusive']].strip(),'imported_background_transitive_closure':c_bg[k],'literal_or_scoped':t.get('scope_status','full_stated_consequence'),'mathematical_status':'integrated_v2_corollary_pending_new_integration_review','component_review':'N008 extension independently reviewed under its corrected main-result contract','replacement_file':MS,'replacement_span':adapters[k],'source_statement_reproduced_verbatim':False}
 if k=='C10':item['common_result']=item['common_result'].replace('equation6.1','equation6.7')
 if k=='C11':item['common_result']=item['common_result'].replace('equation3.3','equation6.4')
 if k=='C1':item['correction']='Finite specialization retained; unrestricted infinite converse false. E4 supplies a sufficient infinite condition and the explicit Prüfer-product counterexample is in the body.'
 if k=='C9':item['scope_note']='The printed theorem sentence omits finite; its section explicitly begins with finite p-groups. No arbitrary infinite-p-group theorem is asserted.'
 targets.append(item)
assert [t['adapter'] for t in targets]==expected
for t in targets:
 text=(ROOT/t['source_file']).read_text()
 a=t['source_span']['start_codepoint'];b=t['source_span']['end_codepoint_exclusive']
 assert sha(text[a:b].encode())==t['source_span']['sha256_utf8'],t['adapter']

sources=copy.deepcopy(A['source_versions'])
sources['N003']['publication']='Journal of Algebra258(2),641-650'
sources['N008']=copy.deepcopy(C['source'])
background=copy.deepcopy(A['retained_background'])
background += [
 {'id':'PΦ','statement':'For finite p-groups P, P/Phi(P) is an elementary abelian p-group.','reference':'N008 p174 recalled finite-p-group fact','role':'retained_unexpanded_input_for_C8_C9','direct_original_read':False},
 {'id':'Zorn','statement':'Every nonempty partially ordered set whose chains have upper bounds has a maximal element.','role':'retained_set_theoretic_input_for_explicitly_infinite_maximal_overgroup_arguments','finite_branch':'For finite groups the proof explicitly selects a proper overgroup of largest order and does not need Zorn.'},
 {'id':'Gaschütz1953','statement':C['all_numbered_items'][-1]['full_normalized_formulation'],'reference':'N008 Theorem 4.1 p175, quoting Gaschütz, Math.Z.58(1953),160-170','role':'explicit_source_quoted_background_not_rederived_not_used_by_C1_C11','direct_original_read':False,'source_span':C['all_numbered_items'][-1]['source_anchor']},
 {'id':'Archer2004','statement':'The earlier reduction, cited in N008 section4.3, of RPRI geometries that are not direct sums to primitive group actions after removing the action kernel.','reference':'C.Archer, Direct sum decomposition of geometries based on maximal subgroups, J.Geometry79(2004),12-18','role':'explicit_source_cited_prior_result_not_rederived_not_used_by_C1_C11','direct_original_read':False},
]
# De-duplicate exact file bindings while retaining access role labels from the originals.
files=[];seen=set()
for f in A['source_files']+C['source']['files']:
 if f['path'] not in seen:files.append(copy.deepcopy(f));seen.add(f['path'])
contract={'schema':'compress_A_v2_integrated_three_paper_review_v1','date':'2026-10-10','bundle':'Compress_A_v2','status':'assembled_private_candidate_not_frozen_not_measured','intake_ids':['N001','N003','N008'],'target_corollary_count':23,'warning_on_count':'Twenty-three adapter labels are a coverage inventory, not a compression factor or a count of distinct new source main theorems.','objective':'One complete mathematical manuscript with shared definitions/theorems/proofs and explicit adapters for the declared main-result contracts of three named papers.','source_versions':sources,'source_files':files,'scope_contract':{'N001':A['scope_contract']['N001'],'N003':A['scope_contract']['N003'],'N008':'All principal new geometric results, finite Theorem 2.1 with explicit infinite correction, all subsidiary numbered statements except retained Gaschütz4.1, and residue/kernel consequences; source finite-p-group context retained.','infinite_scope':'Finite rank only. E0,R(b),E1-E3 and the residue/kernel consequences allow infinite groups where stated. E4 gives a corrected relative-generation theorem; numerical mu bounds and p-group classifications are finite.','not_assumed_for_N008':'Initial flag transitivity or residual connectedness; E0 proves flag transitivity and R(b) needs no G2.','fixed_action_convention':'Typed subgroup families with their specified group actions and fixed quotient map; no unproved automorphism-lifting or orbit-count correspondence.'},'targets':targets,'retained_background':background,'complete_N008_numbered_inventory':copy.deepcopy(C['all_numbered_items']),'excluded_material':list(dict.fromkeys(A['scope_contract']['excluded']+C['excluded']+['Source historical discussion and illustrative diagrams','Archer2004 earlier primitive-group classification is retained, not a new N008 result'])),'corrections_and_qualifications':A['scope_contract']['corrections_or_clarifications']+[C['correction'],'N008 Theorem 3.8 taken in its section\'s explicitly finite-p-group context.','N003 bibliography corrected to641-650; author-manuscript target version and target hashes unchanged.'],'integration':{'shared_R_proof_count':1,'shared_E0_proof_count':1,'new_Frattini_core':'E1-E5 and equations6.1-6.7, all fully expanded in the manuscript','external_required_proof_appendices':[],'administrative_companions':'This intake and its readable ledger duplicate statements/provenance and do not carry mathematical steps absent from the manuscript.','component_audits':[bind('phase36_compress_forest_recent_audit.json'),bind('phase36_compress_forest_N008_recent_audit.json')],'new_assembly_audit_required':True},'measurement':{'three_paper_numerator_admitted':False,'manuscript_ratio':None,'reason':'The assembled integration and corrected N008 main-result contract need review; no three-paper common-rendering/body-length comparison approved. Earlier two-paper diagnostics are not transferred.','policy':'Include all mathematical body/proof appendices/dependency exposition once, same references and acknowledgment exclusions; report conditional retained inputs and rendering sensitivity.','no_previous_ratio_carried_over':True},'artifacts':[bind(MS),bind('phase37_compress_forest_assemble.py'),bind('phase37_compress_forest_assembly.json')],'integrity':{'all_source_file_hashes_verified':True,'all23source_anchor_hashes_verified':True,'all23replacement_spans_bound':True,'component_audit_hashes_verified':True,'prior_frozen_files_modified':False}}
# Remove obsolete exclusions that referred to N008 before this version added it.
contract['excluded_material']=[x for x in contract['excluded_material'] if not x.startswith('N008 and')]
for item in contract['complete_N008_numbered_inventory']:
 if item['adapter']:
  item['review_status']='constituent_extension_reviewed_PASS_new_integrated_v2_pending_review'
(ROOT/'phase37_compress_forest_intake.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')

lines=['# Compress_A_v2 — full source and dependency ledger','','10 October 2026. This ledger binds the integrated three-paper manuscript `phase37_compress_forest_manuscript.md`. It contains complete normalized source formulations, source-version locations, common results, adapters, retained inputs and statuses. Every required mathematical proof is inside the manuscript; this companion is provenance and scope bookkeeping. No three-paper numerator or ratio is admitted.','','## Contract and source versions','','The proposed intake is exactly N001, N003 and N008. There are 23 explicit adapter labels: four parts of the 1998 theorem, eight numbered 2002 results, and eleven 2005 consequences (nine numbered items plus residue/kernel conclusions). This is a coverage inventory, not a compression factor. The 2005 unrestricted infinite converse is corrected, and its quoted Gaschütz theorem remains imported.','','The finite numerical-group bounds and finite-p-group classification remain finite. Finite-rank Frattini geometry can have infinite groups and infinite coset sets. Lemma E0 supplies flag transitivity; the common R(b) induction needs no residual-connectivity assumption.','']
for paper in ['N001','N003','N008']:
 v=sources[paper]
 lines += [f"### {paper}: {v['title']}",'',f"Version: {v['version']}",'']
 locator=v.get('primary_locator',v.get('primary_urls'))
 lines += ['Primary locator(s): '+(locator if isinstance(locator,str) else '; '.join(locator)), '']
 lines += ['Reading: '+v.get('access_depth',v.get('reading',''))+'.','']
 lines += ['Reading limits: '+' '.join(v['read_limits']),'']
lines += ['## Exact source files','','| File | Bytes | SHA-256 |','|---|---:|---|']
for f in files:lines.append(f"| `{f['path']}` | {f['bytes']} | `{f['sha256']}` |")
lines += ['','The Academia challenge response is an explicitly nonprimary failed retrieval, not evidence of article contents. N001 uses the complete authored rendered body; its displayed line coordinates are not original-PDF offsets. The N003 author version and N008 published PDF are distinguished.','','## Shared proof and dependency structure','','Theorems F/P and Lemma O share forest, parity and overgroup work across the 1998/2002 branches. Theorem R(b) occurs once: it proves the 2002 rank/strong-independence result and, after the Frattini ladder and quotient, gives the 2005 coordinate classification. E0 is part of the common geometry foundation. E1/E2, E3, E4 and E5 are fully expanded new proof cost in the three-paper manuscript. No source-target theorem is imported circularly.','','## Target-by-target full formulations','']
for t in targets:
 a=t['source_span'];b=t['replacement_span']
 loc=(f"displayed L{a['displayed_lines'][0]}–L{a['displayed_lines'][-1]}, printed216" if t['paper']=='N001' else 'source pages '+','.join(map(str,t.get('printed_pages',a.get('physical_pdf_pages',[])))))
 lines += [f"### {t['adapter']} — {t['paper']} {t['source_reference']}",'',f"**Full source formulation (normalized).** {t['full_source_formulation_normalized']}",'',f"**Source and location.** `{t['source_file']}`, {loc}. Raw decoded-character interval `{a['start_codepoint']}:{a['end_codepoint_exclusive']}`, SHA-256 `{a['sha256_utf8']}`. These are scope anchors, not approved numerator spans.",'',f"**Common result / adapter.** {t['common_result']}.",'',t['adapter_argument'],'',f"**Retained inputs (transitive).** {', '.join(t['imported_background_transitive_closure'])}.",'',f"**Replacement binding.** Integrated manuscript interval `{b['start_codepoint']}:{b['end_codepoint_exclusive']}`, SHA-256 `{b['sha256_utf8']}`.",'',f"**Status.** {t['literal_or_scoped'].replace('_',' ')}. Constituent proof reviewed; assembled integration requires its own review.",'']
 if t.get('correction'):lines += ['**Correction.** '+t['correction'],'']
 if t.get('scope_note'):lines += ['**Scope note.** '+t['scope_note'],'']
 if t.get('interpretive_note'):lines += ['**Interpretation.** '+t['interpretive_note'],'']
lines += ['## Retained background and source imports','']
for b in background:
 lines += [f"### {b['id']}",'',b['statement'],'']
 if b.get('reference'):lines += ['Reference/interface: '+b['reference']+'.','']
 if b.get('role'):lines += ['Role: '+b['role'].replace('_',' ')+'.','']
 if b.get('direct_original_read') is False:lines += ['The original background work was not independently acquired/read in this assembly; the named primary-source restatement is the retained interface.','']
 if b.get('finite_branch'):lines += [b['finite_branch'],'']
 if b.get('normalization'):lines += [b['normalization'],'']
lines += ['## Complete N008 inventory and exclusions','','All 10 numbered items are accounted for: Theorem 2.1, Theorem 3.1, Proposition 3.2, Corollary 3.3, Theorem 3.4, Proposition 3.5, Lemma 3.6, Proposition 3.7, Theorem 3.8 and Theorem 4.1. The first nine have explicit corrected/scoped corollaries C1–C9; Theorem 4.1 is the quoted Gaschütz input fully stated in manuscript §1. The §4.2 residue test and §4.3 kernel assertion are C10/C11. The complete source anchors and full formulations, including the retained theorem, are in the JSON inventory.','','Excluded from main-result replacement are N003’s unnumbered small-degree exceptions/computer census, general direct-product discussion and open questions, and N008’s historical SmallGroups counts, asymptotic suggestion and cited computational algorithms. Archer 2004’s earlier primitive-group reduction is retained, not rederived as a new result. No automorphism-orbit equality of quotient/original families is assumed. The unrestricted infinite converse of N008 Theorem 2.1 is false and explicitly corrected; the theorem’s finite specialization is fully proved.','','## Review and measurement boundary','','The two-paper core and the separate N008 extension have bound independent internal reviews, which are inputs to this assembly. Their reviews do not automatically certify every integration edit. The new scope/action conventions, shared R(b) proof, equation renumbering and all 23 corollary bindings must be checked in the assembled version. All earlier frozen files remain unchanged.','','No three-paper ratio, additional numerator admission, shortest-proof claim or priority claim is made. The corrected main-result contract needs acceptance, and the complete three-paper body comparison must use a common normalization/rendering. Previously measured two-paper quantities remain separate.','']
(ROOT/'phase37_compress_forest_ledger.md').write_text('\n'.join(lines))
print(json.dumps({'targets':len(targets),'source_hashes_verified':len(files),'replacement_sha256':bind(MS)['sha256'],'all23source_and_adapter_spans_bound':True,'manuscript_ratio':None},indent=2))
