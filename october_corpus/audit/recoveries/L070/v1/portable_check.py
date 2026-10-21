"""Complete L070 public transport audit and small exact application replay."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,hashlib,io,json,shutil,subprocess,time
from pypdf import PdfReader
import pack_codec as codec
ROOT_SHA='4720efe6602ba25047dc7546c67734850fcf95485d839f280e7a4fdfbf6688da'
AUTHOR_SHA='faee5e2bbe75c54772634bc92c8c26c2f704bca78c8c0e8e207d66e71da0ae34'
S='/Users/sasha/medusa/research/leemans';C=S+'/geometry/chiral_atlases';PREFIX='audit/recoveries/L070/v1';PAPER='papers/recoveries/L070/v1'
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
 t=ar.t;need(t['format']=='L070_SEGMENTED_EXACT_CONTENT_V1','known transport format')
 need(t['root_acceptance']['sha256']==ROOT_SHA and t['author_manifest']['sha256']==AUTHOR_SHA,'exact mathematical acceptance and author')
 need(policy['root']['sha256']==ROOT_SHA,'exact premise inventory authority')
 allowed={r['sha256']:r for r in policy['premises']};used={r['sha256']:r for r in t['premises']};need(len(used)==len(t['premises']),'unique premise hashes')
 for h,r in used.items():need(r==allowed.get(h),'only exact reviewed documentary/environment boundary')
 actual={h:r for h,r in ar.objects.items()if r['kind']not in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']};need(set(actual)==set(used),'all and only explicit premise objects')
 for h,r in actual.items():
  p=used[h];need(r==dict(kind=p['kind'],sha256=h,bytes=p['bytes'],exact_locator=p['exact_locator'],reason=p['reason']),'exact premise metadata')
 root=ar.load(C+'/principal_root_review/manifest.json');need(root['status']=='ACCEPTED_COMPLETE_CORRECTED_L070_SOURCE_DISPOSITION','exact whole-source status')
 for r in root['exports']:ar.exact(dict(r,path=C+'/principal_root_review/'+r['path']))
 deps=ar.load(C+'/principal_root_review/dependencies.json');declared={r['path']:r for r in deps}
 need(len(declared)==len(deps),'unique root dependency paths')
 for r in root['exports']:declared[C+'/principal_root_review/'+r['path']]=dict(r,path=C+'/principal_root_review/'+r['path'])
 declared[t['root_acceptance']['path']]=t['root_acceptance'];need(set(declared)==set(ar.originals),'exact complete accepted closure, no omissions or additions')
 for r in declared.values():ar.exact(r)
 author=ar.load(C+'/principal_v1/manifest.json')
 for r in author['exports']:ar.exact(dict(r,path=C+'/principal_v1/'+r['path']))
 for r in ar.load(C+'/principal_v1/dependencies.json'):ar.exact(r)
 return dict(root_dependencies=len(deps),author_exports=len(author['exports']))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--stage',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expected-stage',required=True);ap.add_argument('--expected-transport',required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();start=time.monotonic()
 repo=a.repo.resolve();stage=a.stage.resolve()if a.stage else repo;D=stage/PREFIX
 need(a.out.is_absolute()and not a.out.exists(),'fresh absolute output');a.out.mkdir()
 need(pin(D/'manifest.json')['sha256']==a.expected_stage,'exact externally pinned stage manifest');m=jsonfile(D/'manifest.json');need(m['status']=='PRIVATE_L070_PUBLICATION_STAGE_PENDING_OPERATIONAL_REVIEW','known immutable stage')
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
 # The exact accepted closure authorizes the premises; selected science cannot
 # use their unavailable bytes. No private-path fallback exists.
 selected=a.out/'selected/study';SC=selected/'geometry/chiral_atlases';local=SC/'principal_v1'
 names=['principal_v1/verify.py','principal_v1/vertex_figures.py','principal_v1/check.py','regular_application_v1/application.json','chiral_application_v2/application.json','chiral_application_v2/aut_columns.json','chiral_application_v2/domain.json','small_entries_v1/data01.json','small_entries_v1/expected_classes.json']+['small_entries_v1/groups01/entry_%02d.json'%i for i in[32,33,44,39]]
 for n in names:ar.extract(C+'/'+n,SC/n)
 runs=[]
 def run(label,cmd,cwd=None):
  q=subprocess.run(cmd,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,timeout=180);(a.out/(label+'.stdout')).write_bytes(q.stdout);(a.out/(label+'.stderr')).write_bytes(q.stderr);runs.append(dict(label=label,command=cmd,returncode=q.returncode));need(q.returncode==0 and not q.stderr,'clean '+label)
 for script,name in [('verify.py','synthesis'),('vertex_figures.py','vertex_figures')]:
  run(name,[sys.executable,str(local/script),'--out',str(a.out/(name+'.json'))]);got=jsonfile(a.out/(name+'.json'));want=ar.load(C+'/principal_v1/'+name+'.json')
  if name=='vertex_figures':
   for r in got['inputs']:
    path=Path(r['path']);need(path.is_relative_to(selected),'actual selected input path');original=S+'/'+str(path.relative_to(selected));ar.exact(dict(r,path=original));r['path']=original
  need(got==want,'entire exact accepted '+name+' output')
 for script in ['check.py','verify.py','vertex_figures.py']:
  q=subprocess.run([sys.executable,'-O',str(local/script)],capture_output=True,timeout=10);need(q.returncode!=0 and b'ordinary Python required'in q.stderr,'actual unchanged optimization guard')
 comps=ar.load(C+'/principal_v1/components.json')
 for c in comps:ar.exact(c['manifest']);need(ar.load(c['manifest']['path'])['status']==c['status'],'exact acquired component status')
 ledger=ar.load(C+'/principal_v1/source_ledger.json');need(len(ledger['rows'])==46 and len({x['id']for x in ledger['rows']})==46 and ledger['source_sections']==list(range(1,8))and ledger['source_tables']==list(range(1,8)),'complete fixed-source ledger')
 for public_name,original_name in [('principal.tex','principal.tex'),('principal.pdf','native/principal.pdf'),('complete_proofs.pdf','complete_proofs.pdf'),('source_ledger.json','source_ledger.json')]:equal_file(stage/PAPER/public_name,ar.record(C+'/principal_v1/'+original_name))
 ms=ar.load(C+'/principal_v1/complete_manuscripts.json');volume=PdfReader(io.BytesIO(ar.content(C+'/principal_v1/complete_proofs.pdf')));need(len(ms['manuscripts'])==16 and len(volume.pages)==ms['pages']==41,'16whole manuscripts41pages including principal')
 readable=jsonfile(stage/PAPER/'complete_manuscripts.json');need(len(readable['manuscripts'])==16,'all readable manuscripts');native_inventory=jsonfile(D/'native_inputs.json');need(len(native_inventory['manuscripts'])==16,'all native input rows');i=0
 for k,r in enumerate(ms['manuscripts']):
  rr=readable['manuscripts'][k];ni=native_inventory['manuscripts'][k];need(ni['tex']==r['tex'],'exact native main input')
  need(all(rr[key]==r[key]for key in ['title','pages','first_volume_page','last_volume_page']),'exact readable title and page interval')
  for key in ['tex','pdf']:
   ar.exact(r[key]);need({x:rr[key][x]for x in ['path','bytes','sha256']}==r[key],'exact readable manuscript origin');equal_file(codec.resolve(rr[key]['public_path'],[stage]),r[key])
  need(rr['adjacent_inputs']==ni['adjacent_inputs'],'complete adjacent inputs')
  for q in ni['adjacent_inputs']:ar.exact(q);equal_file(codec.resolve(q['public_path'],[stage]),q)
  pdf=PdfReader(io.BytesIO(ar.content(r['pdf']['path'])));need(len(pdf.pages)==r['pages']and r['first_volume_page']==i+1,'complete native interval')
  for page in pdf.pages:need(page.get_contents().get_data()==volume.pages[i].get_contents().get_data(),'exact whole native page content');i+=1
  need(r['last_volume_page']==i,'exact native interval end')
 native_pages=0
 if a.render:
  native=a.out/'native';native.mkdir();tex=stage/PAPER/'principal.tex';need(tex.read_bytes()==ar.content(C+'/principal_v1/principal.tex'),'exact standalone principal input')
  texbin=shutil.which('pdflatex');gs=shutil.which('gs');need(texbin and gs,'TeX and Ghostscript available')
  for j in range(2):run('tex'+str(j),[texbin,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(tex)],cwd=str(tex.parent))
  need('Overfull'not in(native/'principal.log').read_text(),'clean rebuilt layout');pdf=PdfReader(native/'principal.pdf');old=PdfReader(io.BytesIO(ar.content(C+'/principal_v1/native/principal.pdf')));need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in old.pages],'exact fresh principal text')
  run('render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'principal.pdf')]);pages=sorted(native.glob('page-*.png'));need(len(pages)==4,'four new principal pages')
  for p in pages:need(p.read_bytes()==ar.content(C+'/principal_v1/native/'+p.name),'exact accepted native raster')
  native_pages=len(pages)
 run('codec_controls',[sys.executable,str(D/'codec_controls.py'),'--out',str(a.out/'codec_controls')])
 run('admission_controls',[sys.executable,str(D/'portable_controls.py'),'--stage',str(stage),'--repo',str(repo),'--out',str(a.out/'admission_controls')])
 z=jsonfile(a.out/'synthesis.json');v=jsonfile(a.out/'vertex_figures.json')
 result=dict(status='PASS_PUBLIC_L070_COMPLETE_CLOSURE',stage_manifest=pin(D/'manifest.json'),transport=pin(D/'transport.json'),root_acceptance=t['root_acceptance'],logical_files=len(ar.rows),unique_content_objects=len(ar.objects),verified_payload_objects=verified,premise_objects=len(t['premises']),verified_decoded_bytes=decoded,verified_stored_bytes=stored,new_pack_files=len(packs),new_pack_bytes=sum(r['bytes']for r in packs.values()),selected_files=len(names),selected_bytes=sum(p.stat().st_size for p in selected.rglob('*')if p.is_file()),**closure,complete_manuscripts=16,complete_proof_pages=41,principal_in_volume=True,source_clauses=46,regular=z['regular'],oriented_chiral=z['oriented_chiral'],first_atlas=56,source_groups=79,source_occurrences=88,vertex_figure_edges=sum(r['edges_checked']for r in v['results']),synthesis_damages=6,map_damages=4,optimization_guards=3,storage_controls=jsonfile(a.out/'codec_controls/report.json'),admission_controls=jsonfile(a.out/'admission_controls/report.json'),native_pages=native_pages,seconds=time.monotonic()-start,runs=runs,new_censuses=0,new_group_calls=0,whole_original_registration_credit=0)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='runs'}))
if __name__=='__main__':main()
