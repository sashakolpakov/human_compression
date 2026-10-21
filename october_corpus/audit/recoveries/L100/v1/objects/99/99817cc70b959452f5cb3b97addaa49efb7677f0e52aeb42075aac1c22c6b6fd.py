"""One bounded Aut/type postprocessing call on exact audited anchors 95..2."""
import argparse, collections, hashlib, importlib.util, json, sys, time
from pathlib import Path
if not __debug__: raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
G34=HERE.parent
S=G34.parents[1]
BASE=G34/'exhaustion_target_interface_v1'
BASE_SHA='f9c9220867406398e2fefa80c2946dd5a76d44469816a15defdb0ae18fde2163'
RECEIPTS=[
 ('exhaustion_target01','ba6a4d23edf478725737786fac96f7c7755ba456f0dc7e302ed9e00c2c86dc07',list(range(95,11,-1)),'PARTIAL_DEADLINE'),
 ('exhaustion_target02','10058107380afde9a818e81c50134065a1a03269c7cfb96a5e53612a0862b7b4',list(range(11,2,-1)),'PARTIAL_DEADLINE'),
 ('exhaustion_target03_anchor2','b384e440dfe2459880a7e752e6b50fb2cfc3ec2a1fdddc9ab43c676f629de073', [2],'COMPLETE_REQUEST')]
# Third receipt hash is fixed by preparation, never inferred from its contents.
IDS=list(range(95,1,-1))
ROOTS=[('exhaustion_target_review_v1','ec3321faba67fb77c7579bc23812177a1471f889bb5816f2b979a24cbbd9f96c','ACCEPTED_L100_BOUNDED_TARGET_INTERFACE_V1'),
 ('exhaustion_suffix_review_v1','3f95242847e5b799788df747ff8ef16289c929bdfefd784829d3d439d52696b7','ACCEPTED_L100_SUFFIX_TARGET_INTERFACE_V1'),
 ('exhaustion_single_review_v1','060886859d7c01dce43839fc37480913f8a5554c54665fec46c039759885aab9','ACCEPTED_L100_SINGLE_ANCHOR_INTERFACE_V1')]

def require(ok,msg):
 if not ok: raise ValueError(msg)
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),resolved=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def get_base():
 mp=BASE/'manifest.json';require(pin(mp)['sha256']==BASE_SHA,'changed acquired wrapper manifest')
 m=json.loads(mp.read_text());rows=[pin(mp)]
 for r in m['exports']:
  p=Path(r['path']);require(not p.is_absolute() and '..' not in p.parts,'unsafe acquired export')
  z=pin(BASE/p);require(all(z[k]==r[k] for k in ('bytes','sha256')),'changed acquired export');rows.append(z)
 spec=importlib.util.spec_from_file_location('accepted_target_runtime',BASE/'run_target.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
 return base,rows

def receipt_shape(d,completed,status):
 require(d['status']==status and d['completed_anchors']==completed,'wrong returned anchor boundary')
 require(d['target_census'] is True and d['equivalence']=='inner conjugacy and type permutations only','wrong search scope')
 require(d['audited_returned_rows']==d['reported_completed_rows'],'unaudited completion rows')
 require([r[0] for r in d['audited_returned_rows']]==completed,'row boundary mismatch')
 require(d['audit']['status']=='RETURNED' and d['audit']['returncode']==0,'failed returned audit')
 if status=='COMPLETE_REQUEST': require(d['execution']['status']=='RETURNED' and d['execution']['returncode']==0,'not clean completion')
 else: require(d['execution']['status']=='DEADLINE','not the acquired deadline')
 for _,levels,ranks in d['audited_returned_rows']:
  require(all(type(x) is int and x>=0 for x in levels+ranks),'bad row integer')
  require((not levels and not ranks) or (levels[-1]==0 and all(x>0 for x in levels[:-1])),'missing empty-level exhaustion')

def preflight():
 base,rows=get_base();rows+=base.preflight()
 for folder,sha,status in ROOTS: rows+=base.manifest_gate(G34/folder,sha,status)
 input_rows=[];seen=set();inventory=[]
 for folder,sha,completed,status in RECEIPTS:
  rp=G34/folder/'receipt.json';require(pin(rp)['sha256']==sha,'changed exact receipt')
  d=json.loads(rp.read_text());receipt_shape(d,completed,status);rows.append(pin(rp))
  rows+=[base.verify(r) for r in d['inputs']+d['outputs']]
  require(not (rp.parent/'target/stderr').read_bytes() and not (rp.parent/'audit/stderr').read_bytes(),'nonempty acquired stderr')
  for bid,levels,ranks in d['audited_returned_rows']:
   require(bid not in seen,'duplicate completed anchor');seen.add(bid)
   path=rp.parent/'prepared/checkpoints'/f'b{bid}_done.g';z=pin(path)
   require(any(r['path']==str(path) and r['sha256']==z['sha256'] for r in d['inputs']+d['outputs']),'unbound done checkpoint')
   rows.append(z);input_rows.append([bid,str(path),levels,ranks]);inventory.append(dict(id=bid,receipt=pin(rp),done=z,levels=levels,ranks=ranks))
 require([r[0] for r in input_rows]==IDS,'missing/out-of-order complete anchor union')
 legacy=(S/'phase7_sporadic_fuse.g').read_text();literal=legacy[legacy.index('AutoSub:=function'):legacy.index('allFinal:=[]')]
 require((HERE/'legacy_fusion_functions.g').read_text()==literal,'changed legacy fusion functions')
 for n in ('run_partial_fusion.py','fusion_witness.g','fusion_driver.g','legacy_fusion_functions.g'):
  rows.append(pin(HERE/n))
 rows.append(pin(S/'phase7_sporadic_fuse.g'))
 return base,base.unique_pins(rows),input_rows,inventory

def prepare(out):
 base,pins,rows,inventory=preflight();require(not out.exists(),'output already exists');out.mkdir(parents=True)
 scope=dict(status='PREPARED_PARTIAL_AUT_TYPE_INPUT',anchors=IDS,unpaid_anchor_ids=[1],input_family_counts=dict(sorted(collections.Counter(k for r in rows for k in r[3]).items())),target_census=False,target_postprocessing=True,cap_seconds=60,whole_original_credit=0,source_count_credit=0,bare_incidence_classification=False,actual_full_Aut_computation=True)
 base.save(out/'input_inventory.json',inventory);base.save(out/'scope.json',scope)
 q=lambda p:json.dumps(str(p))
 lines=['SizeScreen([100000,24]);;','INPUT_CATALOGUE:='+q(base.P/'input_catalogue01.g')+';;','Read('+q(base.P/'catalogue_loader_v2.g')+');;',
  'borelResult:=rec();;','INPUT_ROWS:='+json.dumps(rows)+';;','OUTPUT_DIR:='+q(out)+';;',
  'Read('+q(HERE/'legacy_fusion_functions.g')+');;','Read('+q(HERE/'fusion_witness.g')+');;','Read('+q(HERE/'fusion_driver.g')+');;', 'QUIT_GAP(0);']
 (out/'driver.g').write_text('\n'.join(lines)+'\n')
 pins += [pin(out/n) for n in ('input_inventory.json','scope.json','driver.g')]
 r=dict(status='PREPARED',inputs=base.unique_pins(pins),target_census=False,target_postprocessing=True,anchors=IDS,unpaid_anchor_ids=[1],command=[str(base.GAP),'-q','-b',str(out/'driver.g')],cap_seconds=60,whole_original_credit=0,source_count_credit=0)
 base.save(out/'receipt.json',r);return base,r

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare-only',action='store_true');ns=ap.parse_args();out=ns.out.absolute()
 base,r=prepare(out)
 if ns.prepare_only: print(json.dumps(dict(status='PREPARED_NO_POSTPROCESSING',anchors=len(IDS),target_runs=0)));return
 r['status']='ACTIVE_POSTPROCESSING';base.save(out/'receipt.json',r)
 execution=base.phase(r['command'],out/'execution',60,False);r['execution']=execution
 stdout=(out/'execution/stdout').read_text(errors='replace');stderr=(out/'execution/stderr').read_bytes()
 clean=base.clean_phase(execution,out/'execution')
 if not base.unchanged(r['inputs']): status='INVALIDATED_INPUT_CHANGE'
 elif stderr or any(line.startswith(('Error','Syntax warning','Syntax error')) for line in stdout.splitlines()):status='FAILED_POSTPROCESSING'
 elif execution['status']=='DEADLINE':status='PARTIAL_POSTPROCESSING_DEADLINE'
 elif clean and len([l for l in stdout.splitlines() if l.startswith('PASS_PARTIAL_AUT_TYPE_FUSION ')])==1 and (out/'result.g').is_file():status='COMPLETE_PARTIAL_INPUT_FUSION'
 else:status='FAILED_POSTPROCESSING'
 r.update(status=status,outputs=[pin(p) for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'receipt.json'],finished_unix=time.time())
 base.save(out/'receipt.json',r);print(json.dumps(dict(status=status,anchors=len(IDS),unpaid_anchors=[1],target_census=False)))
 if status not in ('COMPLETE_PARTIAL_INPUT_FUSION','PARTIAL_POSTPROCESSING_DEADLINE'):raise SystemExit(2)
if __name__=='__main__':main()
