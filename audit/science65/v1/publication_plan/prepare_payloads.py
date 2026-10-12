"""Exact L096 dependency transport; no source assets or public mutations."""
from pathlib import Path
import argparse,collections,hashlib,json
HERE=Path(__file__).resolve().parent
AUDIT='audit/recoveries/L096/v1';NATIVE='papers/recoveries/L096/v1'
PINS={'corpus106_L096_recovery':'9cde30b9e57f4678f6014e69995ecb2fc8bb011de333bc1fcb4226a71c00c449',
      'corpus106_L096_complete_root_review':'3fe44ce8a5fd34f119fd6a37edee74900097cb68c8d65e6b1b3d670c550bfa24'}
def need(x,m):
    if not x:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def pin(p,n):return dict(path=n,bytes=p.stat().st_size,sha256=sha(p))
def main(a):
    need(not(HERE/'manifest.json').exists(),'frozen proposal')
    files={};public={};packets={};seen=set()
    def add(r):
        n=r['path'];need(not Path(n).is_absolute() and '..' not in Path(n).parts,'safe logical path')
        clean={k:r[k] for k in ['path','bytes','sha256']}
        for base,target in [(a.study,files),(a.repo,public)]:
            p=base/n
            if p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']:
                need(n not in target or target[n]==clean,'consistent logical binding');target[n]=clean;return
        raise ValueError('unresolved exact dependency '+n)
    def walk(x):
        if isinstance(x,dict):
            if {'path','bytes','sha256'}<=x.keys():add(x)
            for v in x.values():walk(v)
        elif isinstance(x,list):
            for v in x:walk(v)
    for directory,h in PINS.items():
        p=a.study/directory/'manifest.json';need(sha(p)==h,'current acceptance pin');add(pin(p,directory+'/manifest.json'))
    dep=load(a.study/'corpus106_L096_recovery/dependencies.json')
    walk(dep);walk(load(a.study/'corpus106_L096_recovery/whole_program_inventory.json')['all_occurrences'])
    while True:
        todo=[n for n in files if Path(n).name=='manifest.json' and n not in seen]
        if not todo:break
        for n in todo:
            seen.add(n);m=load(a.study/n)
            if not isinstance(m,dict) or 'exports' not in m:continue
            entries=[]
            for r in m['exports']:
                x=dict(r,path=str(Path(n).parent/r['path']));add(x);entries.append(x['path'])
            packets[n]=dict(study_manifest=n,sha256=files[n]['sha256'],exports=len(entries),logical_exports=entries)
    idx=collections.defaultdict(list)
    for r in load(a.repo/'provenance/publication_manifest.json')['files']:
        if 'sha256' in r and not r['file'].endswith('.md'):idx[r['sha256']].append(r['file'])
    def score(n):return ('publication_plan' in n or '/previous/' in n,len(n),n)
    # Native current routes are fixed even when identical content also occurs in
    # inherited packets. Other logical occurrences share one exact public body.
    routes={};content={}
    order=sorted(files,key=lambda n:(not n.startswith('corpus106_L096_recovery/'),not n.startswith('corpus106_L096_complete_root_review/'),n))
    for n in order:
        r=files[n];suffix=Path(n).suffix
        need(not any(x in Path(n).parts for x in ['sources','private_source','private_auxiliary','fonts','rasters']),'no primary asset export '+n)
        if n.startswith('corpus106_L096_recovery/'):
            tail=n.split('/',1)[1]
            dest=NATIVE+'/'+tail if suffix in ['.tex','.pdf'] else AUDIT+'/author/'+tail
            kind='COPY_FROZEN'
        elif n.startswith('corpus106_L096_complete_root_review/'):
            dest=AUDIT+'/root_review/'+n.split('/',1)[1];kind='COPY_FROZEN'
        elif r['sha256'] in idx:
            dest=sorted(idx[r['sha256']],key=score)[0];kind='EXISTING_PUBLIC'
            need(pin(a.repo/dest,n)==r,'actual reused public content')
        elif r['sha256'] in content:
            dest,kind=content[r['sha256']]
        else:
            dest=AUDIT+'/retained/'+n
            if dest.endswith('.md'):dest=dest[:-3]+'.txt'
            kind='COPY_FROZEN'
        content.setdefault(r['sha256'],(dest,kind))
        routes[n]=dict(study_path=n,public_path=dest,bytes=r['bytes'],sha256=r['sha256'],transport=kind,
                       extension_only_conversion=n.endswith('.md'),whole_file=True)
    for n,p in packets.items():p['manifest']=dict(path=routes[n]['public_path'],bytes=routes[n]['bytes'],sha256=routes[n]['sha256'])
    unique={}
    for r in routes.values():
        n=r['public_path'];need(n not in unique or all(unique[n][k]==r[k] for k in ['bytes','sha256']),'one destination one content');unique[n]=r
    plan=dict(status='PRIVATE_EXACT_COMPLETE_DEPENDENCY_TRANSPORT',current_pins=PINS,files=list(routes.values()),packets=list(packets.values()),public_dependencies=list(public.values()),
              unique_public_files=len(unique),new_public_files=sum(r['transport']=='COPY_FROZEN' for r in unique.values()),
              new_public_bytes=sum(r['bytes'] for r in unique.values() if r['transport']=='COPY_FROZEN'),
              reused_existing_public_files=sum(r['transport']=='EXISTING_PUBLIC' for r in unique.values()),
              source_assets_exported=False,manifest_bytes_unchanged=True,
              external_GAP_inputs=[{k:v for k,v in c.items() if k in ['imported_group_data','trust_boundary']} for c in dep['all_prior_mathematical_components']['retained_complete_censuses']])
    (HERE/'copy_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({k:plan[k] for k in ['unique_public_files','new_public_files','new_public_bytes','reused_existing_public_files']}))
    print('logical',len(files),'packets',len(packets),'markdown aliases',sum(n.endswith('.md') for n in files))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study',type=Path,required=True);p.add_argument('--repo',type=Path,required=True);main(p.parse_args())
