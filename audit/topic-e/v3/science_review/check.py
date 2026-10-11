#!/usr/bin/env python3
"""Independent expanded-E evidence/binding check; does not automate the mathematical read."""
import argparse, copy, hashlib, json, re, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def need(b,m):
 if not b: raise ValueError('E_REVIEW_REJECT '+m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bind(root,row):
 p=root/row['path'];need(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'bytes '+str(p))
def validate(source,old,program,formal,retained,algebra):
 rows={x['id']:x for x in source['rows']}
 need(len(rows)==len(source['rows'])==56 and len(old['records'])==54,'110 dispositions')
 need(rows['L056.L4.3']['disposition']=='corrected_auxiliary' and 'q-1' in rows['L056.L4.3']['qualification'],'characteristic two')
 need('10 modulo11' in rows['L043.T1.4b']['qualification'],'residue ten')
 need('Four' in rows['L043.L5.12']['qualification'] and 'A5' in rows['L043.L5.12']['qualification'],'four nontrivial collisions')
 for k in ['L043.T8','L043.T10','L043.Table1','L043.Table2']:
  need('not_re' in rows[k]['disposition'],'ancillary boundary '+k)
 need('not_used_in_full_generality' in rows['L043.P2.6']['disposition'],'natural subfield scope')
 need('prior_accepted' in rows['L043.C6.1']['disposition'] and 'prior_accepted' in rows['L043.C6.2']['disposition'],'prior completion attribution')
 expected={'required_finite.g','exceptional_amalgams.g','exceptional_small.g','small_rotation_exclusions.g','psl2_square_bound_check.py','verify_square_witnesses.py'}
 roles={Path(x['path']).name:x['role'] for x in program['files']}
 need({k for k,v in roles.items() if v=='required finite proof'}==expected,'complete required programs')
 need(roles.get('psl2_square_witnesses.json')=='required certificate data','mandatory certificate data')
 need(sum(v=='validation only' for v in roles.values())==6 and len(roles)==13,'optional validation boundary')
 need(program['raw_and_printed_alternatives_not_additive'] and 'symmetrically' in program['measurement_policy'],'symmetric alternatives')
 need(formal['reported_declarations']==42 and formal['new_declarations']==9 and len(formal['modules'])==7,'formal inventory')
 need(len(formal['not_formalized'])==6 and not retained['full_source_Lean_coverage'],'actual partial scope')
 need(retained['external_proof_cost'] is None and retained['external_algorithm_catalogue_cost'] is None and retained['source_graphic_layout_cost'] is None,'unknown external costs')
 need(algebra['status']=='PASS' and algebra['author_imports'] is False,'independent diagnostics')
 need(sum(r['trace_triples'] for r in algebra['trace']['rows'])==316 and sum(r['extensions'] for r in algebra['trace']['rows'])==264,'trace reconstruction')
 need(algebra['trace']['zero_reversals']==24 and algebra['trace']['nonzero_nonreversals']==128,'reversal reconstruction')
 need([r['pairs'] for r in algebra['local_pairs']]==[24,48,360],'rotation pair census')
 ex={(r['p'],tuple(r['type'])):r['rows'] for r in algebra['exceptional']}
 need([r['intersection'] for r in ex[11,(3,5,3)]]==[10],'p11 actual intersection')
 need([r['intersection'] for r in ex[19,(5,3,5)]]==[3,3,6],'p19 actual intersections')
 need([r['intersection'] for r in ex[31,(5,3,4)]]==[3,3],'p31 actual intersections')
 need(set(algebra['weakenings'])=={'absolute_irreducibility_needed','nonzero_denominator_needed','pointed_minus_one_needed'},'necessary hypotheses')

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--author-dir',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--public-root',type=Path);ap.add_argument('--algebra',action='store_true');a=ap.parse_args()
 need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True);A=a.author_dir
 if (ROOT/'manifest.json').exists():
  for r in load(ROOT/'manifest.json')['exports']:bind(ROOT,r)
 binding=load(ROOT/'author_binding.json');need(sha(A/'manifest.json')==binding['frozen_author_sha256'],'author freeze')
 for r in binding['exports']:bind(A,r)
 checked=0
 if a.study_root:
  for key in ['sources','retained_primary','prior_proof_and_acceptance']:
   for r in binding['source_bindings'][key]:bind(a.study_root,r);checked+=1
 if a.public_root:
  for r in binding['source_bindings']['canonical_formal']:bind(a.public_root,r);checked+=1
 proof=load(A/'proof_map.json')
 for k,r in proof['contexts'].items():
  body=''.join((A/r['path']).read_text().splitlines(keepends=True)[r['start_line']-1:r['end_line']]).encode()
  need(len(body)==r['bytes'] and hashlib.sha256(body).hexdigest()==r['sha256'],'proof context '+k)
 pat=r'\\begin\{(theorem|lemma|proposition|corollary|proof)\}.*?\\end\{\1\}'
 envcount=0
 for r in load(A/'migration.json')['records']:
  b=[hashlib.sha256(x.group().encode()).hexdigest() for x in re.finditer(pat,(A/r['current']).read_text(),re.S)]
  need(b==r['environment_hashes'],'current complete environments');envcount+=len(b)
  if a.study_root:
   prev=[hashlib.sha256(x.group().encode()).hexdigest() for x in re.finditer(pat,(a.study_root/r['prior']).read_text(),re.S)]
   need(b==prev,'literal prior environments')
 need(envcount==32,'32 environments')
 doc=load(ROOT/'fresh_replay/report.json');need(doc['status']=='PASS' and doc['not_run']==[] and len(doc['programs_fresh'])==12,'fresh full replay')
 need(doc['source_dispositions']==56 and doc['retained_dispositions']==54 and doc['proof_contexts']==30,'fresh boundary')
 for r in doc['programs_fresh']:
  p=ROOT/'fresh_replay'/('program_'+Path(r['file']['path']).stem+'.stdout');need(sha(p)==r['stdout_sha256'],'program result')
  if r['file']['path'].endswith('.py'):need(r['assertions_enabled'] is True,'Python assertions active')
 need(all(r['rejected'] for r in doc['controls']) and len(doc['controls'])==15,'fresh author controls')
 algebra=load(ROOT/'independent_algebra_result.json')
 if a.algebra:
  p=subprocess.run([sys.executable,'-B','-O',ROOT/'independent_algebra.py','--out',a.out/'algebra.json'],capture_output=True,text=True)
  (a.out/'algebra.stdout').write_text(p.stdout);(a.out/'algebra.stderr').write_text(p.stderr)
  need(p.returncode==0,'fresh independent algebra');need(load(a.out/'algebra.json')==algebra,'fresh diagnostics exact')
 objects=[load(A/'source_map.json'),load(A/'retained_source_maps.json'),load(A/'program_scope.json'),load(A/'formal/scope.json'),load(A/'retained_inputs.json'),algebra]
 validate(*objects)
 def row(x,k):return next(r for r in x[0]['rows'] if r['id']==k)
 mutations=[
 ('hide_characteristic_two',lambda x:row(x,'L056.L4.3').update(qualification='q')),
 ('hide_residue_ten',lambda x:row(x,'L043.T1.4b').update(qualification='unchanged')),
 ('all_collision_groups_trivial',lambda x:row(x,'L043.L5.12').update(qualification='All trivial')),
 ('claim_complete_all_field_quotients',lambda x:row(x,'L043.T8').update(disposition='recovered_principal')),
 ('unqualified_subfield_intersection',lambda x:row(x,'L043.P2.6').update(disposition='recovered')),
 ('erase_prior_completion',lambda x:row(x,'L043.C6.1').update(disposition='new_answer')),
 ('demote_required_census',lambda x:next(r for r in x[2]['files'] if r['path'].endswith('exceptional_amalgams.g')).update(role='validation only')),
 ('omit_mandatory_data',lambda x:x[2]['files'].pop()),
 ('full_formal_claim',lambda x:x[4].update(full_source_Lean_coverage=True)),
 ('unknown_external_as_zero',lambda x:x[4].update(external_proof_cost=0)),
 ('wrong_p11_intersection',lambda x:x[5]['exceptional'][0]['rows'][0].update(intersection=5)),
 ('wrong_p19_zero_discriminant',lambda x:next(r for r in x[5]['exceptional'] if r['p']==19 and r['type']==[5,3,5])['rows'][-1].update(intersection=3)),
 ('reverse_nonzero_discriminant',lambda x:x[5]['trace'].update(nonzero_nonreversals=0))]
 controls=[]
 for name,f in mutations:
  obj=copy.deepcopy(objects);f(obj)
  try:validate(*obj)
  except (ValueError,KeyError,IndexError):controls.append({'name':name,'rejected':True})
  else:raise ValueError('CONTROL_ACCEPTED '+name)
 # Byte-corruption checks use the same real binding predicate, in the fresh output only.
 scratch=a.out/'mutations';scratch.mkdir();(scratch/'file').write_bytes(b'changed')
 try:bind(scratch,{'path':'file','bytes':7,'sha256':hashlib.sha256(b'original').hexdigest()})
 except ValueError:controls.append({'name':'changed_frozen_bytes','rejected':True})
 else:raise ValueError('changed bytes accepted')
 report={'status':'PASS','author_manifest':binding['frozen_author_sha256'],'author_exports':len(binding['exports']),'input_pins':checked,'reviewed_dispositions':110,'proof_contexts':len(proof['contexts']),'unchanged_environments':envcount,'fresh_author_programs':12,'fresh_author_controls':15,'independent_controls':controls,'independent_algebra_fresh':a.algebra,'review_roles_disclosed':True,'no_ratio_or_credit':True,'limitation':'This checker binds the separately recorded mathematical reading and exact diagnostics; it is not an automated proof of the classification.'}
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
