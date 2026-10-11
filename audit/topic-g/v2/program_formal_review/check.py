#!/usr/bin/env python3
"""Read-only audit of the exact Topic G program/formal replay and its limits."""
import argparse, copy, hashlib, json, re
from pathlib import Path
PIN='9d1c68991e23e4b4618472c0c85b500ab208c9c579634f5b635748d8fe843992'
LABELS={'phase265_exceptional.g':'exceptional','phase265_residues.g':'deleted_pencil',
 'phase186_witt_derived_check.g':'witt','phase182_mathieu_fibers.g':'mathieu_fibers',
 'phase186_witt_validate.py':'witt_validation','phase186_witt_lean_generate.py':'witt_formal_generation',
 'phase265_frame_control.g':'frame_control','phase265_plane_models.g':'plane_models',
 'phase186_hermitian_labels.g':'hermitian_labels','phase182_deleted_line_check.py':'deleted_line',
 'phase182_inversive_geometry_check.py':'inversive','hermitian_unital_check.g':'literal_unitals',
 'phase199_path_length.py':'path_length'}
ROLES=dict.fromkeys(list(LABELS)[:4],'required mathematical computation')
ROLES.update({'phase186_witt_validate.py':'required witness verification','phase186_witt_lean_generate.py':'required certificate bridge'})
ROLES.update(dict.fromkeys(list(LABELS)[6:],'validation'))
def need(ok,s):
 if not ok: raise ValueError(s)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def audit(packet,replay,report=None,formal=None,inventory=None):
 report=read(replay/'report.json') if report is None else report
 formal=read(packet/'formal/scope.json') if formal is None else formal
 inventory=read(packet/'program_inventory.json') if inventory is None else inventory
 need(report['status']=='PASS' and report['distinct_formal_reports']==40,'complete successful 40-report replay')
 need({Path(r['path']).name:r['role'] for r in inventory['programs']}==ROLES and len(inventory['programs'])==13,'whole 4+2+7 program roles')
 need({r['label'] for r in report['program_replays']}==set(LABELS.values()) and len(report['program_replays'])==13,'all thirteen executions, no duplicate substitute')
 need(len(formal['modules'])==6 and sum(r['reports'] for r in formal['modules'])==40,'six formal modules, forty printed declarations')
 need({r['module'] for r in report['formal_replays']}=={Path(r['path']).name for r in formal['modules']} and len(report['formal_replays'])==6,'all six executions')
 expected={}
 for row in inventory['programs']+formal['modules']:
  p=packet/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'unchanged code '+row['path']);expected[row['path']]=row['sha256']
 need(report['program_inputs']==expected,'no skipped or substituted source')
 for row in report['program_replays']+report['formal_replays']:
  p=replay/(row['label']+'.log');need(row['status']=='PASS' and row['returncode']==0 and sha(p)==row['log_sha256'],'successful bound log')
  text=p.read_text();need('Error,' not in text and 'error:' not in text,'no silent program/formal error')
 declarations=[]
 for row in formal['modules']:
  text=(packet/row['path']).read_text();names=re.findall(r'^#print axioms\s+(\w+)',text,re.M)
  need(names==row['declarations'] and len(names)==row['reports'],'actual source declaration list')
  need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'no forbidden proof shortcut')
  logs=re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",(replay/(Path(row['path']).stem+'.log')).read_text())
  need([name.rsplit('.',1)[-1] for name,ax in logs]==names,'actual fully qualified declarations, not count alone')
  for name,ax in logs:
   axioms=[x.strip() for x in ax.split(',') if x.strip()];need(set(axioms)<={'propext','Classical.choice','Quot.sound'},'nonstandard axiom')
   declarations.append(dict(name=name,axioms=axioms,module=row['path']))
 need(len({r['name'] for r in declarations})==40,'forty distinct declarations')
 pins=read(replay/'formal_pins.json');wanted=read(packet/'formal/dependency_manifest.json')
 need('version 4.32.2' in pins['lean'] and {r['name']:r['revision'] for r in pins['packages']}=={r['name']:r['rev'] for r in wanted['packages']},'exact nine package revisions and Lean version')
 need((replay/'Generated.lean').read_bytes()==(packet/'formal/WittDerivedPlanes.lean').read_bytes(),'actual native-witness to compiled table bridge')
 need(len(report['controls'])==8 and all(r['status']=='REJECTED' for r in report['controls']),'eight rejected mathematical controls')
 for row in report['controls']:
  if 'log_sha256' in row:need(sha(replay/(row['label']+'.log'))==row['log_sha256'],'control log binding')
 for name in ['wrong_coordinate_incidence','swapped_point_images','alter_biplane_difference_set','replace_singleton_by_pair']:
  text=(replay/(name+'.log')).read_text();need('Tactic `decide` proved that the proposition' in text and 'is false' in text,'formal corruption is false mathematics, not import failure')
 w=read(replay/'phase186_witt_witness.json');need([c['v'] for c in w['cases']]==[11,12,22,23,24],'five actual Witt models')
 return dict(status='PASS_INDEPENDENT_G_PROGRAM_FORMAL_REPLAY_AUDIT',programs=13,roles=dict(mathematical=4,witness_or_certificate=2,validation=7),formal_modules=6,formal_declarations=declarations,mathematical_controls=8,pinned_packages=9,software={k:w[k] for k in ['gap_version','design_version','grape_version']},regenerated_finite_Lean_source_equal=True)
def main():
 p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--replay',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh report')
 need(sha(a.packet/'manifest.json')==PIN,'exact author freeze')
 manifest=read(a.packet/'manifest.json');need(len(manifest['exports'])==105,'105 whole exports')
 for row in manifest['exports']:
  n=Path(row['path']);need(not n.is_absolute() and '..' not in n.parts,'safe export path');q=a.packet/n;need(q.stat().st_size==row['bytes'] and sha(q)==row['sha256'],'frozen export '+str(n))
 result=audit(a.packet,a.replay);controls=[]
 for case in ['omit_program','duplicate_program','omit_formal_module','wrong_declaration_name','promote_sample_to_premise','inflate_formal_count']:
  r=read(a.replay/'report.json');f=read(a.packet/'formal/scope.json');i=read(a.packet/'program_inventory.json')
  if case=='omit_program':r['program_replays'].pop()
  elif case=='duplicate_program':r['program_replays'][-1]=copy.deepcopy(r['program_replays'][0])
  elif case=='omit_formal_module':r['formal_replays'].pop()
  elif case=='wrong_declaration_name':f['modules'][0]['declarations'][0]='a_different_theorem'
  elif case=='promote_sample_to_premise':i['programs'][-1]['role']='required mathematical computation'
  else:r['distinct_formal_reports']=41
  try:audit(a.packet,a.replay,r,f,i)
  except ValueError as e:controls.append(dict(control=case,status='REJECTED',reason=str(e)))
  else:raise ValueError('accepted changed evidence '+case)
 result.update(author_manifest_sha256=PIN,exports_checked=105,independent_evidence_controls=controls,scope='Bound programs, actual statements and replay interfaces only. Whole written/source mathematics reviewed separately; sample cases do not prove uniform claims.')
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','programs','formal_modules','exports_checked']}))
if __name__=='__main__':main()
