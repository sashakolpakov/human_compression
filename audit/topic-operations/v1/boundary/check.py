#!/usr/bin/env python3
"""Bounded input-contract checks; no scientific execution or length evaluation."""
from pathlib import Path
import argparse,copy,csv,difflib,hashlib,json,re
HERE=Path(__file__).resolve().parent
OLD_STUDY=Path('/Users/sasha/medusa/research/leemans')
OLD_PUBLIC=Path('/Users/sasha/medusa/math_compression')
FILES=['contract.json','software_inventory.json','programme_representations.json','external_data.json','retained_inputs.json','source_qualifications.json','common_correspondence.json','citation_proposals.json','evidence_map.json']
EXPECTED_DOCS={'U':21,'A.N005':18,'A.N006':8,'A.N006.nine':5,'A.N006.HN':4,'A.N007':5}
EXPECTED_MAP={'O-lem:helly':2,'O-thm:elements':3,'O-lem:parabolic-join':4,'O-thm:general-twist':21,'O-thm:twist':22,'O-lem:quotient':23,'O-prop:orbital':24,'O-lem:double':25,'M-thm:module-marking':31,'M-lem:shear':32,'M-prop:signed':33}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def walk(x):
 if isinstance(x,dict):
  yield x
  for v in x.values():yield from walk(v)
 elif isinstance(x,list):
  for v in x:yield from walk(v)
def closure(roots,edges):
 out=set(roots)
 while True:
  new=out|{e['prerequisite'] for e in edges if e['use'] in out}
  if new==out:return out
  out=new
def validate_metadata(d):
 c,s,r,e,q,co,cp=(d[n] for n in ['contract.json','software_inventory.json','programme_representations.json','external_data.json','source_qualifications.json','common_correspondence.json','citation_proposals.json'])
 need(c['original_ids']==['N005','N006','N007'],'three-original boundary')
 need(c['ratio'] is None and c['numeric_values'] is None and c['factors_permitted'] is False,'no evaluated factor')
 need(c['new_source_credit']==0 and c['new_question_credit']==0,'no new credit')
 need({x['id']:x['pages'] for x in c['written_documents']}==EXPECTED_DOCS,'whole six-document boundary')
 need({x['id']:x['pages'] for x in c['sources']}=={'N005':60,'N006':22,'N007':12},'whole source extent')
 need(c['whole_theory_once']=='U','whole common acquisition')
 need('including validation files and both required input drivers' in c['conditional_preacquisition'],'conditional complete programme acquisition')
 need(len(c['units'])==5 and c['normalizations']==['NFC','NFKC'] and len(c['variants'])==3,'30-coordinate future policy')
 need(all(x is None for x in c['unknown_costs'].values()),'unknown outside costs')
 need(r['complete_printed_unified_appendix'] is None,'no invented complete printed appendix')
 need(r['selection_rule'].endswith('Never add both representations.'),'alternative representation rule')
 need(q['counts']=={'N005':81,'N006':27,'N007':32},'preserved source scopes')
 ps=s['programs'];ds=s['required_input_drivers'];ops=s['operational_drivers'];fs=s['formal_files']
 need(len(ps)==23 and len(ds)==2 and len(ops)==5 and len(fs)==3,'full software boundary')
 ids=[x['id'] for x in ps+ds+ops+fs];need(len(ids)==len(set(ids)),'unique file identities')
 need(len({x['sha256'] for x in ps+ds})==25,'same whole program not counted twice')
 need(sum(x['logical_premise'] for x in ps)==17,'required finite premise boundary')
 need(all(x['whole_file'] for x in ps+ds+ops),'whole files retained')
 need(all(x['logical_premise'] for x in ds),'both decoders required')
 need(s['unique_partial_formal_declarations']==17 and s['new_N005_formal_declarations']==0,'partial Lean scope')
 need({x['id'] for x in ps if not x['logical_premise']}=={'P.N006.small_obstructions','P.N006.signed_markings','P.N007.diagonal_models','P.N005.presentation_identities','P.N005.literal_twist','P.N005.controls'},'exact validation roles')
 by={x['id']:x for x in ps+fs}
 for a in s['aliases_not_double_charged']:need(a['alias']['sha256']==by[a['owner']]['sha256'],'alias identity')
 total=set()
 for original,roots in s['application_roots'].items():
  actual=closure(s['executable_roots'][original],s['direct_program_edges'])
  need(actual==set(roots['programs']),'complete execution closure '+original)
  need(actual=={x['id'] for x in ps if x['original']==original},'source programme owner '+original)
  need(roots['common_documents']==['U'],'one whole common per conditional '+original)
  total.update(actual)
 need(total=={x['id'] for x in ps},'whole programme union')
 need(s['application_roots']['N006']['documents']==['A.N006','A.N006.nine','A.N006.HN'],'all N006 companions')
 need(s['application_roots']['N006']['required_decoding_drivers']==[x['id'] for x in ds],'both input drivers in closure')
 need(e['required_representation_files']==4 and e['required_representation_bytes']==21960689,'full required representation data')
 need(sum(x['bytes'] for x in e['inputs'] if x['stage_role'].startswith('required'))==e['required_representation_bytes'],'external data exact subtotal')
 need(sum(x['bytes'] for x in e['installed_files_once_by_identical_hash'])==e['installed_file_bytes_once']==2516249,'installed input subtotal')
 need(len({x['sha256'] for x in e['installed_files_once_by_identical_hash']})==16,'installed data once by actual hash')
 need(e['unknown_proof_cost'] is None and e['compact_word_discount'] is False,'external classification not zero')
 need({x['id']:x['new_common']['number'] for x in co['mapping']}==EXPECTED_MAP,'exact theorem correspondence')
 need(sum('old_N007' in x for x in co['mapping'])==6,'six earlier N007 interfaces')
 need(co['no_free_old_umbrella'] and co['final_citation_editions_pending'],'review-gated replacement')
 quot=next(x for x in co['mapping'] if x['id']=='O-lem:quotient')
 need('Initial faithful regular inputs' in quot['hypotheses'] and 'must itself be regular' in quot['hypotheses'],'quotient hypotheses explicit')
 need(len(co['local_arguments_not_replaced'])==2 and 'infinite' in co['local_arguments_not_replaced'][0]['hypothesis_and_use'],'infinite local proofs retained')
 need({x['id'] for x in co['self_contained_companions']}=={'A.N006.nine','A.N006.HN'},'sporadic local companion scope')
 need(len(cp['editions'])==2 and {x['original'] for x in cp['editions']}=={'N006','N007'},'two proposed citation editions')
 for x in cp['editions']:need(x['pdf'] is None and x['accepted'] is False and x['new_text_must_be_charged'],'no unbuilt PDF accepted')
 return {'written_documents':6,'source_originals':3,'source_records':140,'common_interfaces':11,'earlier_N007_interfaces':6,'mathematical_or_validation_files':23,'required_mathematical_files':17,'validation_files':6,'required_input_drivers':2,'operational_drivers':5,'unique_Lean_files':3,'scoped_Lean_declarations':17,'text_counts_computed':False,'ratios_computed':False}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--verify-sources',action='store_true');ap.add_argument('--verify-installed-data',action='store_true');ap.add_argument('--gap-root',type=Path,default=Path('/opt/homebrew/Cellar/gap/4.15.1'));a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'output must be fresh (including no dangling symlink)');a.out.mkdir(parents=True)
 d={n:json.loads((HERE/n).read_text()) for n in FILES};summary=validate_metadata(d)
 def remap(p):
  p=Path(p)
  if p.is_relative_to(OLD_STUDY):return a.study_root/p.relative_to(OLD_STUDY)
  if p.is_relative_to(OLD_PUBLIC):return a.public_root/p.relative_to(OLD_PUBLIC)
  if p.is_relative_to(Path('/opt/homebrew/Cellar/gap/4.15.1')):return a.gap_root/p.relative_to(Path('/opt/homebrew/Cellar/gap/4.15.1'))
  return p
 # Verify exported proposal if a frozen manifest exists; no assumption that it is HEAD.
 mf=HERE/'manifest.json';exports=0
 if mf.exists():
  for row in json.loads(mf.read_text())['exports']:
   p=HERE/row['path'];need(p.is_file() and sha(p.read_bytes())==row['sha256'] and p.stat().st_size==row['bytes'],'frozen export '+row['path']);exports+=1
 sources={x['path'] for x in d['contract.json']['sources']};installed={x['path'] for x in d['external_data.json']['installed_files_once_by_identical_hash']};seen={};skipped=[];installed_skipped=[]
 for obj in d.values():
  for row in walk(obj):
   if not isinstance(row.get('path'),str) or not Path(row['path']).is_absolute() or not re.fullmatch('[0-9a-f]{64}',str(row.get('sha256',''))):continue
   if row['path'] in seen:need(seen[row['path']]==row['sha256'],'inconsistent binding');continue
   seen[row['path']]=row['sha256']
   if row['path'] in sources and not a.verify_sources:skipped.append(row['path']);continue
   if row['path'] in installed and not a.verify_installed_data:installed_skipped.append(row['path']);continue
   p=remap(row['path']);need(p.is_file(),'missing bound file '+str(p));need(sha(p.read_bytes())==row['sha256'],'file identity '+str(p))
   if 'bytes' in row:need(p.stat().st_size==row['bytes'],'file bytes '+str(p))
   if 'span_sha256' in row:
    lines=p.read_text().splitlines(keepends=True);value=''.join(lines[row['start_line']-1:row['end_line']]);need(sha(value.encode())==row['span_sha256'],'span identity '+str(p))
 # Multiple spans of one file must all be checked, even though whole-file hashing is deduplicated.
 spans=0
 for row in walk(d['common_correspondence.json']):
  if 'span_sha256' in row:
   p=remap(row['path']);lines=p.read_text().splitlines(keepends=True);need(sha(''.join(lines[row['start_line']-1:row['end_line']]).encode())==row['span_sha256'],'individual span');spans+=1
  if 'statement_and_proof_sha256' in row:
   p=remap(row['path']);t=p.read_text();m=re.search(r'\\begin\{(lemma|theorem|proposition|corollary)\}(?:\[[^\]]*\])?\\label\{'+re.escape(row['label'])+r'\}',t);need(m is not None,'named theorem label');end=t.index(r'\end{proof}',m.end())+len(r'\end{proof}');need(sha(t[m.start():end].encode())==row['statement_and_proof_sha256'],'actual theorem/proof span');need(t.count('\n',0,m.start())+1==row['start_line'] and t.count('\n',0,end)+1==row['end_line'],'theorem line locator');spans+=1
 # Establish statement numbering from the actual ordered common TeX inputs.
 common=remap(d['common_correspondence.json']['whole_common']['path']).with_suffix('.tex');parts=[]
 for name in re.findall(r'\\input\{(sections/[^}]+)\}',common.read_text()):parts.append((common.parent/name).with_suffix('.tex').read_text())
 labels={};number=0
 for text in parts:
  for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary)\}(?:\[[^\]]*\])?\s*\\label\{([^}]+)\}',text):
   number+=1;labels[m.group(2)]=number
 # Unlabelled theorem environments must not be hidden by the label parser.
 need(sum(len(re.findall(r'\\begin\{(?:theorem|lemma|proposition|corollary)\}',t)) for t in parts)==number,'all numbered environments accounted')
 need(all(labels.get(k)==v for k,v in EXPECTED_MAP.items()),'actual common numbering')
 # Exact source contract cardinality, without changing or reproducing the records.
 for id,row in d['source_qualifications.json']['contracts'].items():
  x=json.loads(remap(row['path']).read_text());need(len(x['records' if id=='N005' else 'rows'])==d['source_qualifications.json']['counts'][id],'actual source record boundary '+id)
 patch_reports=[]
 for x in d['citation_proposals.json']['editions']:
  before=remap(x['base_tex']['path']).read_text();after=before
  for change in x['edits']:
   need(after.count(change['old'])==1,'unique citation anchor');after=after.replace(change['old'],change['new'],1)
  need(sha(after.encode())==x['proposed_tex_sha256'],'proposed complete TeX identity')
  p=Path(x['base_tex']['path']);patch=''.join(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='original/'+p.name,tofile='proposed/'+p.name));need(patch==(HERE/x['patch']).read_text(),'exact proposed patch')
  # Compare complete matched environments, not merely the captured names.
  envs=lambda t:[m.group(0) for m in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}',t,re.S)]
  need(envs(before)==envs(after),'all statements and proofs preserved')
  oldbib=re.findall(r'\\bibitem\{([^}]+)\}',before);newbib=re.findall(r'\\bibitem\{([^}]+)\}',after)
  need(newbib==(oldbib+['common'] if x['original']=='N007' else oldbib),'existing references not renumbered')
  patch_reports.append({'original':x['original'],'statement_proof_environments_unchanged':len(envs(before)),'proposed_tex_sha256':sha(after.encode()),'rendered_or_adopted':False})
 # Controls exercise changes which would misstate the proposed scientific/accounting boundary.
 controls=[]
 def bad(name,change):
  dd=copy.deepcopy(d);change(dd)
  try:validate_metadata(dd)
  except (ValueError,KeyError):controls.append({'name':name,'rejected':True});return
  raise ValueError('control accepted: '+name)
 bad('omit_HN_companion',lambda x:x['contract.json']['written_documents'].pop(4))
 bad('count_old_common_as_free',lambda x:x['common_correspondence.json'].__setitem__('no_free_old_umbrella',False))
 bad('drop_required_decoder',lambda x:x['software_inventory.json']['required_input_drivers'].pop())
 bad('drop_validation_file',lambda x:x['software_inventory.json']['programs'].pop())
 bad('misclassify_required_affine_certificate',lambda x:next(p for p in x['software_inventory.json']['programs'] if p['id']=='P.N005.affine_example').__setitem__('logical_premise',False))
 bad('remove_witness_dependency',lambda x:x['software_inventory.json']['direct_program_edges'].pop(3))
 bad('erase_quotient_hypothesis',lambda x:next(p for p in x['common_correspondence.json']['mapping'] if p['id']=='O-lem:quotient').__setitem__('hypotheses','Any invariant quotient'))
 bad('zero_outside_proof_cost',lambda x:x['contract.json']['unknown_costs'].__setitem__('outside_classical_proofs',0))
 bad('misnumber_common_interface',lambda x:x['common_correspondence.json']['mapping'][0]['new_common'].__setitem__('number',1))
 bad('invent_complete_programme_appendix',lambda x:x['programme_representations.json'].__setitem__('complete_printed_unified_appendix','programs.pdf'))
 bad('reuse_unbuilt_companion_PDF',lambda x:x['citation_proposals.json']['editions'][0].__setitem__('accepted',True))
 bad('evaluate_factor_before_review',lambda x:x['contract.json'].__setitem__('ratio',1.2))
 report={'status':'PASS','scope':'input-boundary/proposal integrity only, not independent mathematical or extraction acceptance','summary':summary,'frozen_exports_checked':exports,'bound_paths_checked':len(seen)-len(skipped)-len(installed_skipped),'primary_hashes_verified':a.verify_sources,'primary_paths_skipped':skipped,'installed_data_hashes_verified':a.verify_installed_data,'installed_paths_skipped':installed_skipped,'actual_span_checks':spans,'citation_proposals':patch_reports,'negative_controls':controls,'required_Atlas_data_rehashed':False,'external_data_scope':'Exact inherited metadata/ledger; installed-file hashes checked only when explicitly selected above. No Atlas fetch, decoding or scientific re-execution.','scientific_GAP_Python_Lean_executed':False,'text_extracted':False,'factors_evaluated':False}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':'PASS','bindings':report['bound_paths_checked'],'spans':spans,'controls':len(controls),'primary_hashes_verified':a.verify_sources}))
if __name__=='__main__':main()
