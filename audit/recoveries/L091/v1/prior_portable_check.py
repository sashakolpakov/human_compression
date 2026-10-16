"""L091 exact public transport and unchanged occurrence-join replay.

Reuses the accepted segmented codec and the earlier Archive reader.
It does not restore the full dependency tree or execute an old search.
"""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,copy,hashlib,importlib.util,io,json,shutil,subprocess,time
from pypdf import PdfReader
import pack_codec as codec
from prior_transport_reader import Archive

ROOT_SHA='3ac722a21723c2a712bfb0f98b3490880a86e74fbcdb0ba26f46cd62fb6b8131'
AUTHOR_SHA='03c2195c86a7b491cf2783c8968cd1fa59d8e83e3163dfd2b57b0f789a788f8f'
S='/Users/sasha/medusa/research/leemans'
H=S+'/geometry/higman_sims'
A=H+'/principal_synthesis_v1'
PREFIX='audit/recoveries/L091/v1'
PAPER='papers/recoveries/L091/v1'
need=codec.need
def load(p):return json.loads(Path(p).read_text())
def pin(p):n,h=codec.digest_file(p);return dict(path=str(p),bytes=n,sha256=h)
def equal_file(p,r):need(codec.digest_file(p)==(r['bytes'],r['sha256']),'exact file '+str(p))


def metadata(ar,policy):
 t=ar.t
 need(t['format']=='L091_SEGMENTED_EXACT_CONTENT_V1','exact L091 transport format')
 need(t['root_acceptance']['sha256']==ROOT_SHA and t['author_manifest']['sha256']==AUTHOR_SHA,'accepted whole-source root and author')
 need(policy['root']==t['root_acceptance'],'exact premise authority')
 allowed={r['sha256']:r for r in policy['premises']}
 used={r['sha256']:r for r in t['premises']}
 need(len(allowed)==len(policy['premises']) and len(used)==len(t['premises']),'unique exact premises')
 actual={h:r for h,r in ar.objects.items() if r['kind'] not in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']}
 need(set(actual)==set(used)==set(allowed),'all and only exact listed premises')
 for h,r in actual.items():
  p=allowed[h];need(used[h]==p,'unchanged exact premise record')
  need(r==dict(kind=p['kind'],sha256=h,bytes=p['bytes'],exact_locator=p['exact_locator'],reason=p['reason']),'literal premise identity')
 root=ar.load(H+'/principal_root_review/manifest.json')
 need(root['status']=='ACCEPTED_COMPLETE_CORRECTED_L091_SOURCE_DISPOSITION','accepted complete source disposition')
 rows=ar.load(H+'/principal_root_review/dependencies.json')
 declared={r['path']:r for r in rows}
 need(len(rows)==len(declared),'unique accepted dependency paths')
 for r in root['exports']:declared[H+'/principal_root_review/'+r['path']]=dict(r,path=H+'/principal_root_review/'+r['path'])
 declared[t['root_acceptance']['path']]=t['root_acceptance']
 need(set(declared)==set(ar.originals),'exact complete root closure')
 for r in declared.values():ar.exact(r)
 author=ar.load(A+'/manifest.json')
 for r in author['exports']:ar.exact(dict(r,path=A+'/'+r['path']))
 for r in ar.load(A+'/dependencies.json'):ar.exact(r)
 return dict(root_dependencies=len(rows),author_exports=len(author['exports']))


def selected_names(ar):
 names=['principal_synthesis_v1/'+n for n in ['verify.py','source_catalogue.json','corrections.json','claims.json','gates.json','proof_registry.json']]
 names+=['supplement_source_audit_v1/full_diagram_transcription.json','source_coordinates_v1/joins.json',
 'local_structure_atoms_v1/source_joins.json','local_structure_compound_v1/source_joins.json',
 'parabolic_structure_frozen01/source_join/source_joins.json','local_structure_atoms_v1/corrections.json',
 'local_structure_compound_v1/corrections.json','parabolic_structure_frozen01/source_join/corrections.json',
 'source_flags_component_v1/claims.json','table_one_join_component_v1/result01.json','j3_table_join_v1/source_join.json']
 for r in ar.load(A+'/source_catalogue.json')['full_group_batches']:
  names.append(r['proof']+'/manifest.json')
  extra=r['proof']+'/expected_groups.json'
  if H+'/'+extra in ar.originals:names.append(extra)
 need(len(names)==31 and len(set(names))==31,'all exact 31 join inputs, including optional original group tables')
 return names


def manuscript_checks(ar,stage,native_inventory,stream_inventory):
 paper=stage/PAPER
 author=ar.load(A+'/manifest.json')
 for r in author['exports']:
  n=r['path']
  if n.endswith(('.tex','.pdf')):
   equal_file(paper/n,ar.record(A+'/'+n))
 for n in ['claims.json','source_catalogue.json','corrections.json','disposition.rst']:
  equal_file(paper/n,ar.record(A+'/'+n))
 need(len(native_inventory['native'])==28,'all TeX entry points')
 expected_mains={A+'/synthesis.tex',A+'/complete.tex'}|{A+'/'+r['copied_tex'] for r in ar.load(A+'/proof_registry.json')}
 need({r['main']['path'] for r in native_inventory['native']}==expected_mains,'every exact native entry point once')
 for n in native_inventory['native']:
  ar.exact(n['main']);equal_file(paper/n['relative_to_author'],n['main'])
  for r in n['adjacent_inputs']:
   ar.exact(r);equal_file(paper/r['relative_to_author'],r)
 registry=ar.load(A+'/proof_registry.json')
 volume=PdfReader(paper/'complete.pdf')
 synthesis=PdfReader(paper/'synthesis.pdf')
 need(len(registry)==26 and len(volume.pages)==78 and len(synthesis.pages)==11,'complete accepted proof volume')
 need(len(stream_inventory['rows'])==66 and stream_inventory['pages']==78,'all imported proof pages')
 at=12;seen=0
 for r in registry:
  for j,page in enumerate(PdfReader(paper/r['copied_pdf']).pages):
   original=page.get_contents().get_data()
   matches=[(key,obj.get_object()) for key,obj in volume.pages[at]['/Resources']['/XObject'].items()
            if obj.get_object().get('/Subtype')=='/Form' and obj.get_object().get_data()==original]
   need(len(matches)==1,'exact imported accepted mathematical page stream')
   expected=dict(chapter=r['id'],chapter_page=j+1,volume_page=at+1,form=matches[0][0],
                 stream_bytes=len(original),stream_sha256=hashlib.sha256(original).hexdigest())
   need(stream_inventory['rows'][seen]==expected,'literal page-stream inventory')
   at+=1;seen+=1
 need(at==78 and seen==66,'no omitted accepted proof pages')
 return dict(synthesis_pages=11,unchanged_chapter_pages=66,complete_volume_pages=78,native_entry_points=28)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=Path);ap.add_argument('--stage',type=Path)
 ap.add_argument('--out',required=True,type=Path);ap.add_argument('--expected-stage',required=True)
 ap.add_argument('--expected-transport',required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args()
 start=time.monotonic();repo=a.repo.resolve();stage=a.stage.resolve() if a.stage else repo;d=stage/PREFIX
 need(a.out.is_absolute() and not a.out.exists(),'fresh absolute replay output');a.out.mkdir()
 need(pin(d/'manifest.json')['sha256']==a.expected_stage,'externally pinned stage')
 manifest=load(d/'manifest.json');need(manifest['status']=='PRIVATE_L091_PUBLICATION_STAGE_PENDING_OPERATIONAL_REVIEW','known stage status')
 need(pin(d/'transport.json')['sha256']==a.expected_transport,'externally pinned transport')
 exports={r['path']:r for r in manifest['exports']};need(len(exports)==len(manifest['exports']),'unique stage exports')
 for r in exports.values():equal_file(codec.resolve(r['path'],[stage]),r)
 t=load(d/'transport.json');policy=load(d/'premises.json');equal_file(d/'premises.json',t['premise_inventory'])
 ar=Archive(stage,repo,t);closure=metadata(ar,policy)
 packs={r['path']:r for r in t['packs']};need(len(packs)==len(t['packs']),'unique new packs')
 for n,r in packs.items():need(exports.get(n)==r and 0<r['bytes']<=48*2**20,'exact bounded new pack')
 need({str(p.relative_to(stage)) for p in (d/'packs').rglob('*') if p.is_file()}==set(packs),'complete physical pack inventory')
 tracked=set(subprocess.run(['git','-C',str(repo),'ls-files','-z'],check=True,capture_output=True).stdout.decode().split('\0'))
 old={r['path']:r for r in t['existing_public_files']};need(len(old)==len(t['existing_public_files']),'unique reused public files')
 for n,r in old.items():need(n in tracked,'reused content is tracked');equal_file(codec.resolve(n,[repo]),r)
 intervals={n:[] for n in packs};used=set();verified=0;decoded=stored=0
 for h,r in ar.objects.items():
  need(h==r['sha256'],'object index hash')
  if r['kind']=='NEW_PACKED_EXACT_CONTENT':
   for s in r['segments']:
    need(s['path'] in packs,'new stream only in declared packs');intervals[s['path']].append((s['offset'],s['offset']+s['bytes']))
   roots=[stage]
  elif r['kind']=='EXISTING_PUBLIC':
   for s in r['segments']:
    need(s['path'] in old,'public segment file declared');need(s['offset']+s['bytes']<=old[s['path']]['bytes'],'public segment within exact whole file');used.add(s['path'])
   roots=[repo]
  else:continue
  codec.verify(r,roots);verified+=1;decoded+=r['bytes'];stored+=r['stored_bytes']
  if verified%5000==0:print(json.dumps(dict(verified_objects=verified,seconds=time.monotonic()-start)),flush=True)
 for n,spans in intervals.items():
  end=0
  for lo,hi in sorted(spans):need(lo==end and hi>lo,'nonoverlapping complete new packed coverage');end=hi
  need(end==packs[n]['bytes'],'no unindexed new pack bytes')
 need(used==set(old),'no unused public file declarations')
 native_inventory=load(d/'selected_inputs.json');names=selected_names(ar)
 need([r['relative_to_H'] for r in native_inventory['selected']]==names,'exact selected replay inputs')
 selected=a.out/'selected/study/geometry/higman_sims'
 for r,n in zip(native_inventory['selected'],names):ar.exact(r);need(r['path']==H+'/'+n,'selected original path');ar.extract(r['path'],selected/n)
 spec=importlib.util.spec_from_file_location('accepted_L091_join',selected/'principal_synthesis_v1/verify.py')
 module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 p=selected/'principal_synthesis_v1'
 args=[load(p/n) for n in ['source_catalogue.json','corrections.json','claims.json','gates.json','proof_registry.json']]
 join=module.ledger_check(*args);damages=module.controls(*args)
 accepted=ar.load(ar.load(H+'/principal_root_review/review.json')['fresh_validation']['report']['path'])
 need(join==accepted['join'] and damages==accepted['damage_controls'],'entire unchanged accepted occurrence join and controls')
 proof=manuscript_checks(ar,stage,native_inventory,load(d/'native_streams.json'))
 runs=[]
 def run(label,cmd,cwd=None,timeout=90):
  q=subprocess.run(cmd,cwd=cwd,stdin=subprocess.DEVNULL,capture_output=True,timeout=timeout)
  (a.out/(label+'.stdout')).write_bytes(q.stdout);(a.out/(label+'.stderr')).write_bytes(q.stderr)
  runs.append(dict(label=label,command=cmd,returncode=q.returncode));need(q.returncode==0 and not q.stderr,'clean '+label)
 native_pages=0
 if a.render:
  native=a.out/'native';native.mkdir();paper=stage/PAPER
  texbin=shutil.which('pdflatex');gs=shutil.which('gs');need(texbin and gs,'TeX and Ghostscript available')
  for stem in ['synthesis','complete']:
   for k in range(3):run(stem+'_tex'+str(k),[texbin,'-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),stem+'.tex'],cwd=paper)
   log=(native/(stem+'.log')).read_text();need('Overfull' not in log and 'undefined references' not in log and 'Rerun to' not in log,'clean fresh native layout')
   new=PdfReader(native/(stem+'.pdf'));oldpdf=PdfReader(paper/(stem+'.pdf'))
   need([x.extract_text() for x in new.pages]==[x.extract_text() for x in oldpdf.pages],'exact fresh accepted document text')
  run('render',[gs,'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-sOutputFile='+str(native/'page%02d.png'),str(native/'synthesis.pdf')])
  pages=sorted(native.glob('page*.png'));need(len(pages)==11,'eleven new synthesis pages')
  for q in pages:need(q.read_bytes()==ar.content(H+'/principal_synthesis_author01/native/'+q.name),'exact directly viewed accepted raster')
  native_pages=11
 run('codec_controls',[sys.executable,str(d/'codec_controls.py'),'--out',str(a.out/'codec_controls')])
 run('admission_controls',[sys.executable,str(d/'portable_controls.py'),'--stage',str(stage),'--repo',str(repo),'--out',str(a.out/'admission_controls')],timeout=180)
 # The transport wrapper's ordinary-Python guard is actually executed.
 q=subprocess.run([sys.executable,'-O',str(d/'portable_check.py')],capture_output=True,timeout=10)
 need(q.returncode!=0 and b'ordinary Python required' in q.stderr,'portable ordinary-Python guard')
 result=dict(status='PASS_PUBLIC_L091_COMPLETE_CLOSURE',stage_manifest=pin(d/'manifest.json'),transport=pin(d/'transport.json'),
             root_acceptance=t['root_acceptance'],logical_files=len(ar.rows),unique_content_objects=len(ar.objects),
             verified_payload_objects=verified,premise_objects=len(t['premises']),verified_decoded_bytes=decoded,
             verified_stored_bytes=stored,new_pack_files=len(packs),new_pack_bytes=sum(r['bytes'] for r in packs.values()),
             selected_files=len(names),selected_bytes=sum(r['bytes'] for r in native_inventory['selected']),
             join=join,join_damage_controls=damages,**closure,**proof,native_pages=native_pages,
             codec_controls=load(a.out/'codec_controls/report.json'),admission_controls=load(a.out/'admission_controls/report.json'),optimization_guards=1,
             new_scientific_targets=0,whole_original_registration_credit=0,new_question_credit=0,new_Lean=0,
             mathematical_compression_measurement=None,seconds=time.monotonic()-start,runs=runs)
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k not in ['runs','join_damage_controls']}),flush=True)


if __name__=='__main__':main()
