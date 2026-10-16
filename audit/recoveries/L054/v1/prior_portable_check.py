"""Complete L054 public transport audit and small exact application replay."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,io,json,shutil,subprocess,time
from pypdf import PdfReader
import pack_codec as codec
ROOT_SHA='01de4f62d06c9e111f7dcb4dcf91dbd570834e30272448d7968cdb2a6337e371'
AUTHOR_SHA='9e11a0c98a2a25f06a13b8a1017e72ad31733904fdd5d9cb85dcdc00d2ad77ae'
S='/Users/sasha/medusa/research/leemans';C=S+'/algebra/subgroup_atlas';PREFIX='audit/recoveries/L054/v1';PAPER='papers/recoveries/L054/v1'
need=codec.need

def jsonfile(p):return json.loads(Path(p).read_text())
def pin(p):n,h=codec.digest_file(p);return dict(path=str(p),bytes=n,sha256=h)
def equal_file(p,r):need(codec.digest_file(p)==(r['bytes'],r['sha256']),'exact file '+str(p))

class Archive:
 def __init__(self,stage,repo,t):
  self.stage=stage;self.repo=repo;self.t=t;self.objects=t['objects'];self.rows={};self.originals={}
  for r in t['logical_files']:
   key=(r['origin'],r['path']);need(key not in self.rows and r['original_path']not in self.originals,'unique logical and original paths');self.rows[key]=r;self.originals[r['original_path']]=r
   if r['origin']in ['study','public']:codec.relative(r['path'])
   else:need(r['origin']=='external'and Path(r['path']).is_absolute(),'explicit external origin')
   obj=self.objects[r['sha256']];need((obj['bytes'],obj['sha256'])==(r['bytes'],r['sha256']),'logical content identity')
  need(set(self.objects)=={r['sha256']for r in self.rows.values()},'no absent or unreferenced content')
 def record(self,original):
  need(original in self.originals,'declared logical input '+original);r=self.originals[original];return self.objects[r['sha256']]
 def content(self,original):
  r=self.record(original);need(r['kind']in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC'],'required scientific bytes cannot be premise-only')
  return b''.join(codec.decoded(r,[self.repo]if r['kind']=='EXISTING_PUBLIC'else[self.stage]))
 def load(self,original):return json.loads(self.content(original))
 def exact(self,r):
  q=self.record(r['path']);need((q['bytes'],q['sha256'])==(r['bytes'],r['sha256']),'declared bound original input')
 def extract(self,original,out):
  r=self.record(original);need(r['kind']in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC'],'selected input has actual bytes');codec.materialize(r,[self.repo]if r['kind']=='EXISTING_PUBLIC'else[self.stage],out)

def validate_metadata(ar,policy):
 t=ar.t;need(t['format']=='L054_SEGMENTED_EXACT_CONTENT_V1','known transport format')
 need(t['root_acceptance']['sha256']==ROOT_SHA and t['author_manifest']['sha256']==AUTHOR_SHA,'exact mathematical acceptance and author')
 need(policy['root']['sha256']==ROOT_SHA,'exact premise inventory authority')
 allowed={r['sha256']:r for r in policy['premises']};used={r['sha256']:r for r in t['premises']};need(len(used)==len(t['premises']),'unique premise hashes')
 for h,r in used.items():need(r==allowed.get(h),'only exact reviewed documentary/environment boundary')
 actual={h:r for h,r in ar.objects.items()if r['kind']not in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']};need(set(actual)==set(used),'all and only explicit premise objects')
 for h,r in actual.items():
  p=used[h];need(r==dict(kind=p['kind'],sha256=h,bytes=p['bytes'],exact_locator=p['exact_locator'],reason=p['reason']),'exact premise metadata')
 root=ar.load(C+'/principal_v2_root_review/manifest.json');need(root['status']=='ACCEPTED_L054_ARTICLE_MAIN_RESULTS_WITH_EXPLICIT_COMPANION_BOUNDARY','exact whole-source status')
 for r in root['exports']:ar.exact(dict(r,path=C+'/principal_v2_root_review/'+r['path']))
 deps=ar.load(C+'/principal_v2_root_review/dependencies.json');declared={r['path']:r for r in deps}
 need(len(declared)==len(deps),'unique root dependency paths')
 for r in root['exports']:declared[C+'/principal_v2_root_review/'+r['path']]=dict(r,path=C+'/principal_v2_root_review/'+r['path'])
 declared[t['root_acceptance']['path']]=t['root_acceptance'];need(set(declared)==set(ar.originals),'exact complete accepted closure, no omissions or additions')
 for r in declared.values():ar.exact(r)
 author=ar.load(C+'/principal_v2/manifest.json')
 for r in author['exports']:ar.exact(dict(r,path=C+'/principal_v2/'+r['path']))
 for r in ar.load(C+'/principal_v2/dependencies.json'):ar.exact(r)
 return dict(root_dependencies=len(deps),author_exports=len(author['exports']))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--stage',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expected-stage',required=True);ap.add_argument('--expected-transport',required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();start=time.monotonic()
 repo=a.repo.resolve();stage=a.stage.resolve()if a.stage else repo;D=stage/PREFIX
 need(a.out.is_absolute()and not a.out.exists(),'fresh absolute output');a.out.mkdir()
 need(pin(D/'manifest.json')['sha256']==a.expected_stage,'exact externally pinned stage manifest');m=jsonfile(D/'manifest.json');need(m['status']=='PRIVATE_L054_PUBLICATION_STAGE_PENDING_OPERATIONAL_REVIEW','known immutable stage')
 need(pin(D/'transport.json')['sha256']==a.expected_transport,'exact externally pinned transport');t=jsonfile(D/'transport.json')
 exports={r['path']:r for r in m['exports']};need(len(exports)==len(m['exports']),'unique stage exports')
 for r in m['exports']:codec.relative(r['path']);equal_file(codec.resolve(r['path'],[stage]),r)
 # This authenticates every complete new pack before selecting any object.
 packs={r['path']:r for r in t['packs']};need(len(packs)==len(t['packs']),'unique packs')
 for n,r in packs.items():need(exports.get(n)==r and 0<r['bytes']<=48*2**20,'bounded complete pack in exact stage manifest')
 actual_packs={str(p.relative_to(stage))for p in(D/'packs').rglob('*')if p.is_file()};need(actual_packs==set(packs),'exact physical pack inventory')
 policy=jsonfile(D/'premises.json');equal_file(D/'premises.json',t['premise_inventory']);ar=Archive(stage,repo,t);closure=validate_metadata(ar,policy)
 tracked=subprocess.run(['git','-C',str(repo),'ls-files','-z'],capture_output=True,check=True).stdout.decode().split('\0');tracked=set(tracked)
 public={r['path']:r for r in t['existing_public_files']};need(len(public)==len(t['existing_public_files']),'unique public reuse inventory')
 for n,r in public.items():need(n in tracked,'reused content is tracked public input');equal_file(codec.resolve(n,[repo]),r)
 intervals={n:[]for n in packs};public_used=set();stored=decoded=0;verified=0
 for h,r in ar.objects.items():
  need(h==r['sha256'],'object index identity')
  if r['kind']=='NEW_PACKED_EXACT_CONTENT':
   for s in r['segments']:
    need(s['path']in packs,'new content only in declared new packs');intervals[s['path']].append((s['offset'],s['offset']+s['bytes']))
   roots=[stage]
  elif r['kind']=='EXISTING_PUBLIC':
   n=r['public_path'];p=public[n];public_used.add(n);need((p['bytes'],p['sha256'])==(r['stored_bytes'],r['stored_sha256']),'exact old stored object')
   need(r['segments']==([dict(path=n,offset=0,bytes=p['bytes'])]if p['bytes']else[]),'complete existing public object');roots=[repo]
  else:continue
  codec.verify(r,roots);verified+=1;stored+=r['stored_bytes'];decoded+=r['bytes']
  if verified%5000==0:print(json.dumps(dict(verified_objects=verified,seconds=time.monotonic()-start)),flush=True)
 for n,rows in intervals.items():
  end=0
  for lo,hi in sorted(rows):need(lo==end and hi>lo,'exact nonoverlapping packed coverage');end=hi
  need(end==packs[n]['bytes'],'no unindexed pack bytes')
 need(public_used==set(public),'all declared public reuse actually used')
 # Extract only the accepted finite implication/source join inputs.
 selected=a.out/'selected';selected.mkdir();mapping={}
 names=['principal_v2/audit.py','principal_v2/scope.json','principal_v2/large_applications.json','principal_v2/claim_register.json','small_order_domain_v1/target_join01.json','article_main_results_scope_distinct_review/review.json']
 folders=['alternating_ten_structural_v1','alternating_eleven_structural_v2','mathieu_twenty_three_structural_v1','symplectic_four_five_structural_v1','symplectic_four_seven_structural_v1','symplectic_six_two_structural_v1','symmetric_ten_structural_v1']
 names += [f+'/native_assertions.json'for f in folders]
 for t0 in ar.load(C+'/principal_v2/large_applications.json'):names.append(str(Path(t0['structural_review']['path']).relative_to(C)))
 for i,n in enumerate(names):
  original=C+'/'+n;name='%02d'%i+('.py'if n.endswith('.py')else'.json');ar.extract(original,selected/name);mapping[original]=name
 mp=a.out/'mapping.json';mp.write_text(json.dumps(mapping,indent=2)+'\n')
 runs=[]
 def run(label,cmd,cwd=None):
  q=subprocess.run(cmd,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,timeout=180);(a.out/(label+'.stdout')).write_bytes(q.stdout);(a.out/(label+'.stderr')).write_bytes(q.stderr);runs.append(dict(label=label,command=cmd,returncode=q.returncode));need(q.returncode==0 and not q.stderr,'clean '+label)
 for flags,label in [([],'synthesis'),(['-O'],'synthesis_optimized')]:
  run(label,[sys.executable,'-B']+flags+[str(D/'portable_replay.py'),'--selected',str(selected),'--mapping',str(mp),'--out',str(a.out/(label+'.json'))])
  need(jsonfile(a.out/(label+'.json'))==ar.load(C+'/principal_v2/audit01.json'),'entire exact acquired finite join result')
 for name in ['principal.tex','principal.pdf','roster.tex','proof_volume.pdf','proof_volume_index.json','claim_register.json','scope.json','attribution.json','README.rst']:equal_file(stage/PAPER/name,ar.record(C+'/principal_v2/'+name))
 volume=PdfReader(stage/PAPER/'proof_volume.pdf');ms=ar.load(C+'/principal_v2/proof_collection.json')['components'];readable=jsonfile(stage/PAPER/'complete_manuscripts.json');native_inventory=jsonfile(D/'native_inputs.json')
 need(len(ms)==len(readable['manuscripts'])==len(native_inventory['manuscripts'])==41 and len(volume.pages)==readable['total_pages']==107,'41 complete prior texts and107 total pages')
 principal=PdfReader(stage/PAPER/'principal.pdf');need(len(principal.pages)==7,'seven principal pages');i=0
 for page in principal.pages:need(page.get_contents().get_data()==volume.pages[i].get_contents().get_data(),'whole principal page');i+=1
 for k,r in enumerate(ms):
  rr=readable['manuscripts'][k];ni=native_inventory['manuscripts'][k];need(ni['tex']==r['tex']and rr['title']==r['title']and rr['acceptance']==r['acceptance'],'exact acquired native title and acceptance')
  for kind in ['tex','pdf']:
   ar.exact(r[kind]);need({q:rr[kind][q]for q in ['path','bytes','sha256']}==r[kind],'exact readable origin');equal_file(codec.resolve(rr[kind]['public_path'],[stage]),r[kind])
  need(rr['adjacent_inputs']==ni['adjacent_inputs'],'all adjacent native inputs')
  for q in ni['adjacent_inputs']:ar.exact(q);equal_file(codec.resolve(q['public_path'],[stage]),q)
  for page in PdfReader(io.BytesIO(ar.content(r['pdf']['path']))).pages:need(page.get_contents().get_data()==volume.pages[i].get_contents().get_data(),'whole prior page content');i+=1
 need(i==107 and readable['prior_pages']==100 and readable['principal_pages']==7,'complete mathematical volume')
 native_pages=0
 if a.render:
  native=a.out/'native';native.mkdir();tex=stage/PAPER/'principal.tex';texbin=shutil.which('pdflatex');gs=shutil.which('gs');need(texbin and gs,'TeX and Ghostscript available')
  for j in range(2):run('tex'+str(j),[texbin,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(tex)],cwd=str(tex.parent))
  need(not any(x in(native/'principal.log').read_text()for x in ['Overfull','Underfull','Warning']),'clean rebuilt layout');pdf=PdfReader(native/'principal.pdf');need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in principal.pages],'exact fresh principal text')
  run('render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(native/'page-%02d.png'),str(native/'principal.pdf')]);pages=sorted(native.glob('page-*.png'));need(len(pages)==7,'seven new pages')
  for p in pages:need(p.read_bytes()==ar.content(C+'/principal_v2/native02/'+p.name),'exact accepted native raster')
  native_pages=len(pages)
 run('codec_controls',[sys.executable,str(D/'codec_controls.py'),'--out',str(a.out/'codec_controls')])
 run('admission_controls',[sys.executable,str(D/'portable_controls.py'),'--stage',str(stage),'--repo',str(repo),'--out',str(a.out/'admission_controls')])
 z=jsonfile(a.out/'synthesis.json')
 result=dict(status='PASS_PUBLIC_L054_ARTICLE_MAIN_RESULTS_COMPLETE_CLOSURE',stage_manifest=pin(D/'manifest.json'),transport=pin(D/'transport.json'),root_acceptance=t['root_acceptance'],logical_files=len(ar.rows),unique_content_objects=len(ar.objects),verified_payload_objects=verified,premise_objects=len(t['premises']),verified_decoded_bytes=decoded,verified_stored_bytes=stored,new_pack_files=len(packs),new_pack_bytes=sum(r['bytes']for r in packs),selected_files=len(names),selected_bytes=sum(p.stat().st_size for p in selected.rglob('*')if p.is_file()),**closure,complete_prior_manuscripts=41,complete_proof_pages=107,principal_in_volume=True,source_clauses=21,complete_groups=z['total_groups'],structural_rows=z['total_rows'],corrected_A11_labels=1,all_current_companion_tables_recovered=False,companion_socle_bound_established=False,synthesis_damages=len(z['damages']),storage_controls=jsonfile(a.out/'codec_controls/report.json'),admission_controls=jsonfile(a.out/'admission_controls/report.json'),native_pages=native_pages,seconds=time.monotonic()-start,runs=runs,new_censuses=0,new_group_calls=0,whole_original_registration_credit=0,compression_measurement=None)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='runs'}))
if __name__=='__main__':main()
