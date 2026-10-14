#!/usr/bin/env python3
"""Portable L003 scientific packet checks, with optional full finite replay."""
import argparse,copy,hashlib,json,pathlib,subprocess,tempfile,time
HERE=pathlib.Path(__file__).resolve().parent

def read(p):return json.loads(p.read_text())
def require(c,m):
 if not c:raise ValueError(m)
def hashfile(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def validate(d):
 require(d['completed']==66 and not d['missing'],'finite coverage')
 require(len(d['rows'])==66 and len({r['id'] for r in d['rows']})==66,'unique finite rows')
 require(d['source_order_discrepancies']==['T5.8','T5.10'],'literal order corrections')
 for r in d['rows']:
  reg=r['actual_regularity']=='regular';require(r['actual_regularity']==r['source_regularity'],'regularity source match')
  require(r['actual_full_type_preserving_order']==r['actual_rotation_order']*(2 if reg else 1),'orientation factor')
  require(r['source_full_order_matches']==(r['source_full_order']==r['actual_full_type_preserving_order']),'honest source comparison')
  if not r['source_full_order_matches']:require(r['id'] in ('T5.8','T5.10') and r['actual_full_type_preserving_order']==2*r['source_full_order'],'exact order discrepancy')
  orders=r['all_16_Cplus_subgroup_orders'];require(len(orders)==16 and orders[-1]==r['actual_rotation_order'],'whole marked subgroup roster')
  require(r['Cplus_intersection_pairs']==256 and len(r['pair_orders'])==6,'IC+ boundary')
  flags=r['normalized_rotation_flags'];require(len(flags)==16,'all normalized rotation flags')
  for i,J,c,want in flags:
   mask=15-sum(1<<(j-1) for j in J);expected=orders[mask] if len(J)==2 else 2
   require(c==want==expected,'actual normalized flag count')
  require(len(r['actual_rank_two_residues'])==6,'all rank-two residues')
  for pair,m,seen,degrees in r['actual_rank_two_residues']:
   mask=15-sum(1<<(j-1) for j in pair)
   require(m==orders[mask] and seen==2*m and len(degrees)==2*m and set(degrees)=={2},'actual rank-two cycle')
  require(len(r['marked_residues'])==4,'all marked local groups')
  for q in r['marked_residues']:
   i=q['omitted_type'];require(q['actual_marked_local_order']==orders[15-(1<<i)],'local subgroup index')
   if q['kind']=='spherical':require(q['actual_marked_local_order']==q['literal_standard_local_order'],'spherical marked isomorphism');continue
   h=q['actual_translation_kernel_basis'];require(len(h)==2 and h[0][1]==0,'whole rank-two lattice kernel')
   m=h[0][0];a,b=h[1];require(m>0 and b>0 and 0<=a<m,'canonical kernel basis')
   require(q['actual_marked_local_order']==m*b*(3 if q['kind']=='hyper333' else 6),'translation determinant and rotation index')
   p,t=q['literal_period_parameters'];inside=t%b==0 and (p-(t//b)*a)%m==0
   if r['id']=='T8.11' and i==1:require(not inside and isinstance(q['literal_standard_local_order'],str) and m*b==84,'literal malformed-period distinction')
   else:require(inside and isinstance(q['literal_standard_local_order'],int),'literal local relation retained')
  require(bool(r['failed_inverse_relators'])!=reg,'inversion criterion')
  if reg:
   require(r['regular_full_IP_pairs']==256 and len(r['regular_normalized_flags'])==16,'full regular completion')
   require(r['regular_normalized_flags']==flags,'separate regular normalized counts')
 return True

def controls(data):
 edits=[('lost finite row',lambda d:d['rows'].pop()),('false orientation factor',lambda d:d['rows'][0].__setitem__('actual_full_type_preserving_order',1)),('collapsed rotation order',lambda d:d['rows'][0].__setitem__('actual_rotation_order',1)),('lost IC check',lambda d:d['rows'][0].__setitem__('Cplus_intersection_pairs',255)),('false flag count',lambda d:d['rows'][0]['normalized_rotation_flags'][0].__setitem__(2,999)),('disconnected residue receipt',lambda d:d['rows'][0]['actual_rank_two_residues'][0].__setitem__(2,0)),('wrong lattice determinant',lambda d:d['rows'][0]['marked_residues'][1]['actual_translation_kernel_basis'][0].__setitem__(0,1)),('false local order',lambda d:d['rows'][0]['marked_residues'][0].__setitem__('actual_marked_local_order',1)),('lost inverse relator witness',lambda d:d['rows'][0].__setitem__('failed_inverse_relators',[])),('suppressed source corrections',lambda d:d.__setitem__('source_order_discrepancies',[]))]
 out=[]
 for label,edit in edits:
  bad=copy.deepcopy(data);edit(bad)
  try:validate(bad)
  except ValueError:out.append(label)
  else:raise ValueError('accepted mutation: '+label)
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--study-root',type=pathlib.Path);ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 if (HERE/'manifest.json').exists():
  for e in read(HERE/'manifest.json')['exports']:require((HERE/e['path']).stat().st_size==e['bytes'] and hashfile(HERE/e['path'])==e['sha256'],'frozen export '+e['path'])
 data=read(HERE/'finite_results.json');validate(data);negative=controls(data)
 structural=read(HERE/'structural_columns.json');targets=read(HERE/'structural_targets.json')['targets'];sr=read(HERE/'structural_replay.json')
 def check_structural(ledger):
  require(len(ledger['rows'])==73 and len({r['id'] for r in ledger['rows']})==73,'structural row coverage')
  named={r['id']:r for r in ledger['rows'] if r['status']=='exact_named_isomorphism_proved'}
  require(set(named)=={r['id'] for r in targets}=={r['id'] for r in sr['rows']} and len(named)==29,'honest structural assertion roster')
  for r in targets:require(named[r['id']]['asserted_group']==r['target'],'exact named target including action')
  require({r['id'] for r in ledger['rows'] if r['status']=='source_order_incompatible_not_asserted'}=={'T5.8','T5.10'},'structural order corrections')
 check_structural(structural)
 for label,edit in [('invented extension identification',lambda d:next(r for r in d['rows'] if r['id']=='T3.1').__setitem__('status','exact_named_isomorphism_proved')),('field/diagonal action conflation',lambda d:next(r for r in d['rows'] if r['id']=='T8.10').__setitem__('asserted_group','PGL(2,49) x C3'))]:
  bad=copy.deepcopy(structural);edit(bad)
  try:check_structural(bad)
  except ValueError:negative.append(label)
  else:raise ValueError('accepted structural mutation '+label)
 require(sr['status']=='PASS' and sr['script_sha256']==hashfile(HERE/'structural_groups.py'),'exact structural replay program')
 for r in sr['rows']:
  q=HERE/'structural_certificates'/(r['id']+'.log');require(r['passed'] and q.stat().st_size==r['certificate_bytes'] and hashfile(q)==r['certificate_sha256'] and 'PASS_NAMED_ISOMORPHISM '+r['id'] in q.read_text(),'exact structural isomorphism receipt')
 for r in read(HERE/'migration.json')['inherited_programs']:
  q=HERE/r['destination'];require(q.stat().st_size==r['bytes'] and hashfile(q)==r['sha256'],'whole inherited program/data '+r['destination'])

 roster=read(HERE/'table_roster.json')['rows'];require(len(roster)==73 and sum(r['prior_reuse_route'] is not None for r in roster)==7,'full source table boundary')
 require({r['id'] for r in data['rows']}=={r['id'] for r in roster if r['prior_reuse_route'] is None},'separate row coverage')
 require(len(read(HERE/'source_map.json')['rows'])==117,'all source dispositions')
 for e in read(HERE/'migration.json')['complete_bodies']:require((HERE/e['destination']).stat().st_size==e['bytes'] and hashfile(HERE/e['destination'])==e['sha256'],'complete moved proof')
 for rec in read(HERE/'author_replay.json')['rows']:
  path=HERE/'certificates'/(rec['id']+'.log');require(hashfile(path)==rec['certificate_sha256'],'exact row certificate')
  require('PASS_L003_ROW '+rec['id'] in path.read_text(),'completed row')
 if a.study_root:
  q=read(HERE/'source_map.json')['source'];p=a.study_root/q['path'];require(p.stat().st_size==q['bytes'] and hashfile(p)==q['sha256'],'exact source edition')
 subprocess.run(['python3','-B','-O',str(HERE/'adapter_words.py')],check=True,stdout=(a.out/'adapter_words.json').open('wb'))
 subprocess.run(['python3','-B','-O',str(HERE/'diagram_types.py')],check=True,stdout=(a.out/'diagram_types.json').open('wb'))
 if a.programs:
  ids=[r['id'] for r in data['rows']];subprocess.run(['python3','-B','-O',str(HERE/'run_batch.py'),'--rows',*ids,'--out',str(a.out/'finite'),'--gap',a.gap,'--timeout','300'],check=True)
  subprocess.run(['python3','-B','-O',str(HERE/'collect_results.py'),'--batches',str(a.out/'finite'),'--out',str(a.out/'fresh_results.json')],check=True,stdout=(a.out/'collection.json').open('wb'))
  fresh=read(a.out/'fresh_results.json');validate(fresh)
  for old,new in zip(data['rows'],fresh['rows']):
   for k in old:
    if k not in ('receipt','stdout','stderr'):require(old[k]==new[k],'fresh complete row '+old['id']+'/'+k)
  subprocess.run(['python3','-B','-O',str(HERE/'structural_groups.py'),'--out',str(a.out/'structural'),'--gap',a.gap,'--timeout','90'],check=True)
  ns=read(a.out/'structural/report.json');require(ns['status']=='PASS' and len(ns['rows'])==29,'fresh complete structural replay')
 render=[]
 if a.render:
  from pypdf import PdfReader
  for name in ['shared_supplement','hexagonal_extensions','l121_adapter']:
   dst=a.out/name;dst.mkdir()
   for turn in (1,2):
    with (dst/f'run{turn}.stdout').open('wb') as o:subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(dst),name+'.tex'],cwd=HERE,stdout=o,stderr=subprocess.STDOUT,check=True)
   def texts(p):return [x.extract_text() for x in PdfReader(p).pages]
   require(texts(dst/(name+'.pdf'))==texts(HERE/(name+'.pdf')),'exact rendered page text '+name)
   log=(dst/(name+'.log')).read_text();require('Overfull' not in log and 'undefined' not in log.lower(),'render diagnostics '+name)
   render.append({'document':name,'pages':len(texts(dst/(name+'.pdf')))})
 report={'status':'PASS','finite_rows':66,'shared_rows':7,'source_rows':117,'exact_named_group_identifications':29,'remaining_structural_rows_explicitly_qualified':44,'source_order_corrections':['T5.8','T5.10'],'local_qualifications':13,'negative_controls':negative,'new_programs_replayed':a.programs,'unchanged_inherited_programs_reexecuted':False,'inherited_proof_sections_exact':4,'fresh_render':render,'seconds':round(time.monotonic()-start,6),'scope':'Author proof/certificate verification, not independent science acceptance or new credit.'};(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
