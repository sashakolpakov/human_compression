"""Portable complete L115 closure and literal certificate acquisition."""
import sys
if sys.flags.optimize:raise RuntimeError('ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import argparse,csv,io,json,subprocess,time
from pypdf import PdfReader
import pack_codec as codec
from prior_transport_reader import Archive
import portable_replay
PREFIX='audit/principal-refutations/L115/complete/v1';PAPER='papers/corrections/L115/v1'
S='/Users/sasha/medusa/research/leemans';Z=S+'/geometry/suzuki_subgroups';A=Z+'/principal_v2';ROOT=Z+'/principal_root_review'
ROOT_SHA='1f7e2e6b2954d60b7af9c5a1a16261a78065d87b2a0828547afcf97a86b91fb3'
AUTHOR_SHA='8c15732e2041adc45ba02f88119c6823673e33272ae2c5526ab3d7dbe83cacf9'
need=codec.need

def load(p):return json.loads(p.read_text())
def pin(p):n,h=codec.digest_file(p);return dict(path=str(p),bytes=n,sha256=h)
def equal(p,r):need(codec.digest_file(p)==(r['bytes'],r['sha256']),'exact stored file '+str(p))

def metadata(ar,policy):
    t=ar.t;need(t['format']=='L115_COMPLETION_EXACT_CONTENT_V1','exact transport format')
    need(t['root_acceptance']['sha256']==ROOT_SHA and t['author_manifest']['sha256']==AUTHOR_SHA,'exact source acceptance')
    need(policy['root']==t['root_acceptance'],'premise authority')
    premises={r['sha256']:r for r in policy['premises']}
    need(len(premises)==len(policy['premises'])and t['premises']==policy['premises'],'exact premise list')
    actual={h:r for h,r in ar.objects.items()if r['kind']not in ['NEW_PACKED_EXACT_CONTENT','EXISTING_PUBLIC']}
    need(actual==premises,'all and only explicit documentary and environment objects')
    for r in actual.values():need(r['kind']in ['ORIGINAL_SOURCE_DOCUMENTARY_PREMISE','PINNED_ENVIRONMENT_OR_LIBRARY_PREMISE'],'known premise meaning')
    root=ar.load(ROOT+'/manifest.json');need(root['status']=='ACCEPTED_L115_COMPLETE_CORRECTED_SOURCE_TREATMENT','whole-source status')
    deps=ar.load(ROOT+'/dependencies.json');declared={r['path']:r for r in deps}
    need(len(declared)==len(deps),'unique root dependencies')
    for r in root['exports']:declared[ROOT+'/'+r['path']]=dict(r,path=ROOT+'/'+r['path'])
    declared[ROOT+'/manifest.json']=t['root_acceptance'];need(set(declared)==set(ar.originals),'exact accepted closure with no omitted paths')
    for r in declared.values():ar.exact(r)
    author=ar.load(A+'/manifest.json')
    for r in author['exports']:ar.exact(dict(r,path=A+'/'+r['path']))
    for r in ar.load(A+'/dependencies.json'):ar.exact(r)
    gates=ar.load(A+'/gates.json')
    need(set(gates)=={'preliminaries','scalar_subspaces','normalizer_families','subfield_families','arithmetic','diagram_labels','diagrams'},'all seven proof components')
    for g in gates.values():
        ar.exact(g['manifest']);m=ar.load(g['manifest']['path']);need(m['status']==g['status'],'exact accepted gate')
        for r in m['exports']:ar.exact(dict(r,path=str(Path(g['manifest']['path']).parent/r['path'])))
    return dict(root_dependencies=len(deps),author_exports=len(author['exports']),proof_gates=len(gates))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--stage',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--expected-stage',required=True);ap.add_argument('--expected-transport',required=True);ap.add_argument('--render',action='store_true');a=ap.parse_args();start=time.monotonic()
    repo=a.repo.resolve();stage=a.stage.resolve()if a.stage else repo;d=stage/PREFIX
    need(a.out.is_absolute()and not a.out.exists(),'fresh absolute output');a.out.mkdir()
    need(pin(d/'manifest.json')['sha256']==a.expected_stage,'externally pinned stage')
    need(pin(d/'transport.json')['sha256']==a.expected_transport,'externally pinned transport')
    m=load(d/'manifest.json');need(m['status']=='PRIVATE_L115_COMPLETION_STAGE_PENDING_OPERATIONAL_REVIEW','exact stage status')
    exports={r['path']:r for r in m['exports']};need(len(exports)==len(m['exports']),'unique exports')
    for r in m['exports']:
        codec.relative(r['path']);need(not r['path'].lower().endswith('.md'),'no new public Markdown path');equal(codec.resolve(r['path'],[stage]),r)
    for r in load(d/'reused_tools.json'):equal(d/r['path'],r)
    t=load(d/'transport.json');ar=Archive(stage,repo,t);closure=metadata(ar,load(d/'premises.json'))
    packs={r['path']:r for r in t['packs']};need(len(packs)==len(t['packs']),'unique new packs')
    for n,r in packs.items():need(exports.get(n)==r and 0<r['bytes']<=48*2**20,'bounded complete new pack')
    need({str(p.relative_to(stage))for p in(d/'packs').rglob('*')if p.is_file()}==set(packs),'exact new pack domain')
    public={r['path']:r for r in t['existing_public_files']};need(len(public)==len(t['existing_public_files']),'unique reused physical files')
    for n,r in public.items():equal(codec.resolve(n,[repo]),r)
    intervals={n:[]for n in packs};used=set();verified=stored=decoded=0
    for h,r in ar.objects.items():
        need(h==r['sha256'],'object key')
        if r['kind']=='NEW_PACKED_EXACT_CONTENT':
            roots=[stage]
            for seg in r['segments']:
                need(seg['path']in packs,'new segment in declared pack');intervals[seg['path']].append((seg['offset'],seg['offset']+seg['bytes']))
        elif r['kind']=='EXISTING_PUBLIC':
            roots=[repo]
            for seg in r['segments']:
                need(seg['path']in public and seg['offset']+seg['bytes']<=public[seg['path']]['bytes'],'reused segment within exact public file');used.add(seg['path'])
        else:continue
        codec.verify(r,roots);verified+=1;stored+=r['stored_bytes'];decoded+=r['bytes']
    for name,ranges in intervals.items():
        end=0
        for lo,hi in sorted(ranges):need(lo==end and hi>lo,'new packs have no holes or overlaps');end=hi
        need(end==packs[name]['bytes'],'every new pack byte indexed')
    need(used==set(public),'no unused public declarations')
    readable=load(stage/PAPER/'readable_sources.json')
    for name,r in readable.items():ar.exact(r);equal(stage/PAPER/name,r)
    imports=ar.load(A+'/proof_imports.json')
    for row in imports:
        for k in ['tex','pdf']:ar.exact(row[k]);need(readable['proofs/'+row['name']+'/proof.'+k]==row[k],'complete exact proof import')
    manuscripts=load(stage/PAPER/'manuscripts.json');need(len(manuscripts['manuscripts'])==8 and manuscripts['complete_pages']==36,'eight whole proof manuscripts')
    total=0
    for item in manuscripts['manuscripts']:
        need(len(PdfReader(stage/PAPER/item['pdf']).pages)==item['pages'],'exact native proof page count');total+=item['pages']
    need(total==36,'total complete proof pages')
    replay=portable_replay.replay(ar,a.out)
    with(stage/PAPER/'table12_comparison.csv').open(newline='')as f:rows=list(csv.DictReader(f))
    need(rows==[{k:str(v)for k,v in r.items()}for r in ar.load(A+'/table12_comparison.json')],'all readable CSV values')
    rebuilt=0
    if a.render:
        native=a.out/'native';native.mkdir()
        for item in manuscripts['manuscripts']:
            folder=native/item['name'];folder.mkdir();tex=stage/PAPER/item['tex']
            for turn in range(2):
                cmd=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(folder),str(tex)]
                q=subprocess.run(cmd,cwd=tex.parent,stdin=subprocess.DEVNULL,capture_output=True,timeout=60)
                (folder/f'compile{turn}.stdout').write_bytes(q.stdout);(folder/f'compile{turn}.stderr').write_bytes(q.stderr);need(q.returncode==0,'clean exact TeX rebuild')
            pdf=PdfReader(folder/(tex.stem+'.pdf'));old=PdfReader(stage/PAPER/item['pdf'])
            need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in old.pages],'complete native page text preserved');rebuilt+=len(pdf.pages)
    q=subprocess.run([sys.executable,'-B',str(d/'codec_controls.py'),'--out',str(a.out/'codec_controls')],capture_output=True,timeout=30)
    (a.out/'codec.stdout').write_bytes(q.stdout);(a.out/'codec.stderr').write_bytes(q.stderr);need(q.returncode==0 and not q.stderr,'unchanged codec controls')
    result=dict(status='PASS_PUBLIC_L115_COMPLETE_CORRECTED_SOURCE_TREATMENT',stage_manifest=pin(d/'manifest.json'),transport=pin(d/'transport.json'),root_acceptance=t['root_acceptance'],logical_files=len(ar.originals),unique_content_objects=len(ar.objects),verified_payload_objects=verified,premise_objects=len(t['premises']),verified_decoded_bytes=decoded,verified_stored_bytes=stored,new_pack_files=len(packs),new_pack_bytes=sum(r['bytes']for r in packs.values()),reused_public_files=len(public),complete_manuscripts=8,complete_proof_pages=36,rebuilt_pages=rebuilt,mathematical_replay=replay,codec_controls=load(a.out/'codec_controls/report.json'),**closure,ordinary_recovery_delta=0,principal_refutation_delta=0,proposed_completed_original_delta=1,registration_credit=0,measurement=None,new_Lean=0,new_conjectures=0,seconds=time.monotonic()-start)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
