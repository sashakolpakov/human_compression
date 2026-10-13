from pathlib import Path,PurePosixPath
import json,hashlib,gzip,importlib.util
W=Path(__file__).resolve().parent;S=W.parents[1];R=S.parents[1]/'math_compression';stage=W/'stage01';out=W/'root_integrity01'
def need(c,s):
 if not c:raise ValueError(s)
def load(p):return json.loads(p.read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
def pin(p):b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':digest(b)}
def same(p,r):b=p.read_bytes();need(digest(b)==r['sha256'] and len(b)==r.get('bytes',len(b)),'binding '+str(p));return b
ready=load(W/'ready.json');same(W/'stage_manifest.json',ready['stage_manifest']);manifest=load(W/'stage_manifest.json')
need(len(manifest['files'])==51,'stage count')
for r in manifest['files']:
 same(stage/r['path'],r)
 if (R/r['path']).exists():need((R/r['path']).read_bytes()==(stage/r['path']).read_bytes(),'existing public change')
for key in ['proposal','scope_routes','publication_guide','install_instructions','adaptation','public_pin_audit','native_visual_review']:same(W/ready[key]['path'],ready[key])
T=stage/'audit/recoveries/L042/v1/transport.json';same(T,ready['transport']);t=load(T)
need(len(t['files'])==6712 and len(t['packets'])==441,'transport sizes')
records={(r['origin'],r['path']):r for r in t['files']};need(len(records)==6712,'distinct logical paths')
decoded={};omitted=[];restored=0
for r in t['files']:
 if r['transport'].endswith('HASH_ONLY'):omitted.append((r['origin'],r['path']));continue
 p=(R if r['transport']=='EXISTING_PUBLIC' else stage)/r['public_path'];b=p.read_bytes();need(len(b)==r['stored_bytes'] and digest(b)==r['stored_sha256'],'stored bytes')
 if r['sha256'] not in decoded:
  b=gzip.decompress(b) if r['encoding']=='gzip' else b
  need(len(b)==r['bytes'] and digest(b)==r['sha256'],'decoded bytes');decoded[r['sha256']]=b
 # Independently compare author's freshly restored tree, including all acquired files.
 p=W/'portable01/restored'/('study' if r['origin']=='study' else 'repo')/r['path'];same(p,r);restored+=1
need(len(omitted)==49 and restored==6663 and len(decoded)==4702,'logical closure')
exports=0
for pk in t['packets']:
 origin='public' if pk['origin']=='repo' else pk['origin'];key=(origin,pk['path']);r=records[key];need(r['sha256']==pk['sha256'],'packet hash');m=json.loads(decoded[r['sha256']]);need(len(m['exports'])==pk['exports'],'packet export count')
 for e in m['exports']:
  name=str(PurePosixPath(pk['path']).parent/e['path']);q=records[(origin,name)];need(q['sha256']==e['sha256'] and q['bytes']==e['bytes'],'literal export');exports+=1
need(exports==3742,'all exports')
report=load(W/'portable01/report.json');same(W/'portable01/report.json',ready['report'])
need(report['status']=='PASS_PUBLIC_L042_COMPLETE_CLOSURE','terminal complete receipt')
b=(W/'portable01/application.stdout').read_bytes();err=(W/'portable01/application.stderr').read_bytes();need(digest(b)==report['application_stdout_sha256'] and not err,'application terminal receipt')
need(report['application']['status']=='PASS_L042_PRINCIPAL' and report['application']['complete_base_matches']==18 and report['application']['subdivision_controls']==108 and report['native_pages']==4 and report['native_text_identical'],'exact application scope')
# Resolve all proposed publication hashes against its staged/public bytes.
proposal=load(W/'integration01/admission_proposal.json');npins=[0]
def walk(v):
 if isinstance(v,dict):
  if all(k in v for k in ['path','bytes','sha256']):
   paths=[stage/v['path'],R/v['path']];p=next((p for p in paths if p.is_file()),None);need(p is not None,'proposal path');same(p,v);npins[0]+=1
  for x in v.values():walk(x)
 elif isinstance(v,list):
  for x in v:walk(x)
for name in ['admission_proposal.json','scope_routes.json','manuscript_inventory.json','portable_adaptation.json']:walk(load(W/'integration01'/name))
need(npins[0]==26,'proposal public pins')
# Source article is documentary and is not silently omitted as a theorem premise.
need(('study','sources/catalogue_L042.pdf') in omitted,'documentary source')
prior=load(R/'audit/recoveries/L019/v1/transport.json')
prior_omissions={(r['origin'],r['path']) for r in prior['files'] if r['transport'].endswith('HASH_ONLY')}
new_omissions={('study',p) for p in ['sources/catalogue_L042.pdf','sources/catalogue_L042.txt','reboot_20261013/L042_recovery_work/arxiv_source.tar','reboot_20261013/L042_recovery_work/Extension_Elisa_.tex']}
need(set(omitted)==prior_omissions|new_omissions,'exact prior documentary omissions plus four fixed L042 source assets')

result={'status':'PASS_ROOT_L042_PUBLIC_TRANSPORT_INTEGRITY','stage_files':51,'logical_files':6712,'restored_files_rehashed':restored,'unique_decoded_payloads':len(decoded),'packet_exports_verified':exports,'acquired_packets':441,'documentary_omissions':len(omitted),'proposal_public_pins':npins[0],'completed_portable_report':pin(W/'portable01/report.json'),'new_mathematical_censuses_run':0,'full_prior_portable_replay_acquired':True,'whole_original_credit':0}
out.mkdir();(out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
