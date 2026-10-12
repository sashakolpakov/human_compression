#!/usr/bin/env python3
"""Portable L050 assembly replay. Large enumerations are retained, never repeated."""
import argparse,copy,hashlib,importlib.util,json,re,shutil,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
def need(ok,message):
 if not ok:raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def save(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def run(cmd,cwd=None):
 r=subprocess.run([str(x)for x in cmd],cwd=cwd,capture_output=True,text=True)
 need(r.returncode==0,'command failed: '+str(cmd)+'\n'+r.stdout[-1000:]+r.stderr[-1000:]);return r
def exports(path):
 m=load(path);rows=m.get('exports',m.get('files'));need(isinstance(rows,list),'manifest shape')
 for r in rows:
  p=path.parent/r.get('path',r.get('file'));need(p.is_file(),'missing retained export '+str(p))
  need(sha(p)==r['sha256'],'retained export hash '+str(p))
  if 'bytes'in r:need(p.stat().st_size==r['bytes'],'retained export length')
 return len(rows)

def scope_check(obj):
 need(obj['original_id']=='L050' and obj['pages']==11,'whole exact source')
 rows={r['id']:r for r in obj['records']}
 need(len(rows)==54 and obj['record_count']==54,'all54 source rows')
 need(not any('PENDING'in r['disposition']for r in rows.values()),'unresolved author bridge')
 exact={'P2group':'PROVED','P2groupS':'PROVED','P5dual8':'DISPROVED_CORRECT_DISTANCE6','P5dualirred':'DISPROVED','GraphUniqueness':'UNRESOLVED','QuestionReverse':'DISPROVED'}
 for k,v in exact.items():need(rows[k]['disposition']==v,'source qualification '+k)
 need(obj['new_admission_credit']==obj['question_credit']==0 and not obj['full_formalization'],'scope inflation')
 for row in rows.values():
  need(row['proof_files'],'missing current proof')
  for name in row['proof_files']:need(sha(HERE/name)==row['proof_file_hashes'][name],'current proof binding')
 return len(rows)

def inventory_check(obj):
 required={'programs/check_local_bridges.py','programs/steiner_construction.py','inputs/group120/check.py','inputs/common_scalar/check_association_counts.py','inputs/enumerations/method/enumerate_ternary.c','inputs/module105/enumerate_sparse_messages.c','inputs/module120/verify_modules.g','inputs/module176/certificate.py','inputs/module253/certificate.py'}
 rows={r['path']:r for r in obj['whole_executable_files']}
 need(required<=rows.keys(),'missing whole required program')
 for name in required:need('REQUIRED'in rows[name]['role'],'required program mislabeled')
 for r in list(rows.values())+obj['literal_data_and_retained_outputs']:
  p=HERE/r['path'];need(p.stat().st_size==r['bytes']and sha(p)==r['sha256'],'whole program/data integrity '+r['path'])
 source=obj['source_software'];need(source['length']is None and not source['whole_program_available'],'unknown source software must remain unknown')
 need(source['embedded_executable_listings']is False,'changed source listing boundary')
 return len(rows)

def bindings():
 out={};d=load(HERE/'dependencies.json')
 need(d['common_full_cost_required']and d['no_large_enumeration_repeat'],'complete common/computational boundary')
 for r in d['packages']:
  p=HERE/r['copied_manifest'];need(sha(p)==r['author_manifest_sha256'],'retained author edition')
  out[r['id']]=exports(p)
  if 'acceptance_copied_manifest'in r:
   q=HERE/r['acceptance_copied_manifest'];need(sha(q)==r['acceptance_manifest_sha256'],'distinct acceptance edition');exports(q)
  else:raise ValueError('missing distinct retained acceptance '+r['id'])
  for f in r['files']:need(sha(HERE/f['path'])==f['sha256'],'retained route binding')
 scope_check(load(HERE/'source_map.json'));inventory_check(load(HERE/'program_inventory.json'))
 pcs=load(HERE/'proof_contexts.json')
 for r in pcs['contexts']:
  text=''.join((HERE/r['path']).read_text().splitlines(True)[r['start_line']-1:r['end_line']])
  need(hashlib.sha256(text.encode()).hexdigest()==r['sha256'],'exact proof context')
 f=load(HERE/'formal_scope.json');need(f['new_Lean_declarations']==0 and f['total_reused_declarations']==9,'actual formal scope')
 for name,r in f['files'].items():
  p=HERE/'formal'/name;need(sha(p)==r['sha256'],'formal source')
  need(re.findall(r'#print axioms (\w+)',p.read_text())==r['declarations'],'actual declaration inventory')
 return dict(retained_exports=out,source_rows=54,proof_contexts=len(pcs['contexts']),formal_declarations=9)

def distributions():
 sys.path.insert(0,str(HERE/'programs'))
 import check_local_bridges as bridge
 receipt=load(HERE/'inputs/enumerations/receipt.json');out={}
 for name,r in receipt['results'].items():
  p=HERE/'inputs/enumerations'/(name+'.json');obj=load(p)
  need(sha(p)==r['enumeration_sha256'],'complete enumeration receipt')
  need(sha(HERE/'inputs/enumerations/bases'/(name+'.txt'))==r['basis_sha256'],'complete basis receipt')
  dual=bridge.mac(obj['weight_counts'],r['n'],r['k'])
  actual=(next(i for i in range(1,r['n']+1)if obj['weight_counts'][i]),obj['weight_counts'][r['d']],next(i for i in range(1,r['n']+1)if dual[i]),dual[r['dual_d']])
  need(actual==(r['d'],r['minimum_words'],r['dual_d'],r['dual_minimum_words']),'complete distribution transfer')
  out[name]=list(actual)
 for name,k,dualcount in [('K',15,2100),('N',16,1260)]:
  obj=load(HERE/'inputs/module120/author_replay'/(name+'_enumeration.json'));v=obj['weight_counts'];dual=bridge.mac(v,120,k)
  need(not any(v[1:48])and v[48]==1260 and not any(dual[1:4])and dual[4]==dualcount,'socle complete distribution')
  out[name]=[48,1260,4,dualcount]
 table=load(HERE/'inputs/module105/source_tables.json')
 for key,name in [('C','105_adjacency'),('D','105_differences')]:
  v=load(HERE/'inputs/enumerations'/(name+'.json'))['weight_counts']
  need({str(i):c for i,c in enumerate(v)if c}==table[key],'entire historical weight table')
 return out

def controls(out):
 rejected=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,FileNotFoundError):rejected.append(name)
  else:raise ValueError('control survived '+name)
 base=load(HERE/'source_map.json')
 for key,new in [('P5dual8','PROVED'),('GraphUniqueness','PROVED'),('P2groupS','PENDING_BOUNDED_GROUP_BRIDGE')]:
  q=copy.deepcopy(base);next(r for r in q['records']if r['id']==key)['disposition']=new
  reject('changed source qualification '+key,lambda q=q:scope_check(q))
 q=load(HERE/'program_inventory.json');q['whole_executable_files']=[r for r in q['whole_executable_files']if r['path']!='inputs/enumerations/method/enumerate_ternary.c']
 reject('dropped whole retained enumerator',lambda:inventory_check(q))
 q=load(HERE/'program_inventory.json');q['source_software']['length']=0
 reject('unknown historical software changed to zero',lambda:inventory_check(q))
 q=load(HERE/'program_inventory.json');q['whole_executable_files'][0]['sha256']='0'*64
 reject('changed required file bytes',lambda:inventory_check(q))
 # Re-evaluate the actual local mathematics under five independently named corruptions.
 text=(HERE/'programs/check_local_bridges.py').read_text()
 edits=[('wrong characteristic17 rank','17:155','17:175','all exceptional ranks'),('missing characteristic11 exception','7:119,11:99','7:119','complete exceptional primes'),('wrong difference dimension','len(S)==20','len(S)==21','difference code is incidence augmentation'),('wrong difference dual multiplicity','20,30,112,43680','20,30,112,33600','dual minimum'),('false LCD converse','rank(B4,3)==4','rank(B4,3)==2','LCD converse counterexample')]
 for i,(name,old,new,error)in enumerate(edits):
  need(text.count(old)==1,'unique semantic mutation')
  d=out/('mutation'+str(i));d.mkdir();(d/'check_local_bridges.py').write_text(text.replace(old,new));shutil.copyfile(HERE/'programs/steiner_construction.py',d/'steiner_construction.py')
  r=subprocess.run([sys.executable,'-B','-O',str(d/'check_local_bridges.py'),'--enumerations',str(HERE/'inputs/enumerations'),'--out',str(d/'result')],capture_output=True,text=True)
  need(r.returncode!=0 and error in r.stderr,'semantic control must fail at its intended mathematical guard '+name);rejected.append(name)
 return rejected

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--study-root',type=Path);ap.add_argument('--render',action='store_true');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args()
 need(not a.out.exists(),'fresh output required');a.out.mkdir(parents=True);t=time.monotonic()
 if (HERE/'manifest.json').exists():exports(HERE/'manifest.json')
 report=bindings()
 if a.study_root:
  src=load(HERE/'source_map.json');need(sha(a.study_root/src['source_pdf'])==src['source_sha256'],'exact eleven-page primary')
 r=run([sys.executable,'-B','-O',HERE/'assemble.py','--out',a.out/'migration'])
 for row in load(HERE/'migration.json')['rows']:
  name=row['destination'];need((a.out/'migration'/name).read_bytes()==(HERE/name).read_bytes(),'exact scientific migration '+name)
 report['exact_migrated_sections']=len(load(HERE/'migration.json')['rows'])
 run([sys.executable,'-B','-O',HERE/'programs/check_local_bridges.py','--enumerations',HERE/'inputs/enumerations','--out',a.out/'bridges'])
 report['new_local_bridges']=load(a.out/'bridges/report.json')
 run([sys.executable,'-B','-O',HERE/'inputs/group120/check.py','--out',a.out/'group120'])
 report['actual_group120_bridge']=load(a.out/'group120/report.json')
 report['complete_distribution_transfers']=distributions()
 report['controls_rejected']=controls(a.out)
 if a.render:
  from pypdf import PdfReader
  d=a.out/'render';d.mkdir();shutil.copyfile(HERE/'application.tex',d/'application.tex');shutil.copytree(HERE/'sections',d/'sections')
  for i in range(2):
   r=run([a.pdflatex,'-halt-on-error','-interaction=nonstopmode','application.tex'],cwd=d);(d/('render'+str(i)+'.log')).write_text(r.stdout)
  log=(d/'application.log').read_text();need(not any(s in log for s in ['Overfull','Undefined control sequence','LaTeX Warning: Reference','LaTeX Warning: Citation','Missing character']),'clean mathematical render')
  pdf=PdfReader(d/'application.pdf');text=[p.extract_text()or''for p in pdf.pages]
  if (HERE/'application.pdf').exists():need(text==[p.extract_text()or''for p in PdfReader(HERE/'application.pdf').pages],'exact final page text')
  report['rendered_pages']=len(text);report['page_text_sha256']=[hashlib.sha256(x.encode()).hexdigest()for x in text]
 report.update(status='PASS',large_exhaustive_enumerations_repeated=False,new_source_credit=0,elapsed_seconds=round(time.monotonic()-t,3))
 save(a.out/'report.json',report);print(json.dumps({k:v for k,v in report.items()if k not in ['new_local_bridges','actual_group120_bridge','page_text_sha256']},indent=2))
if __name__=='__main__':main()
