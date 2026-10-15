"""One60s incremental Aut/type call:42new families, preserved old103/completeAut."""
import argparse,hashlib,importlib.util,json,sys,time
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;G34=HERE.parent;OLD=G34/'postprocess_interface_v1';OUTOLD=G34/'postprocess_target01';NEW=G34/'exhaustion_target05_level_resume'
OLD_SHA='49d27feb144a22d650c233b60606549cb54c195b05ae45c4bcdfa0327acf646f'
OLD_RECEIPT='cf30b8c7a8f58719618bd714cc0aa23099d4cd9fd47d3b5b6cd5418b86342b51'
NEW_RECEIPT='063cdf3625e72b2e0d075c54c7b059159c88cea333a4a9ccda855ce006be5d14'
def require(v,s):
 if not v:raise ValueError(s)
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),resolved=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load_prior():
 require(pin(OLD/'manifest.json')['sha256']==OLD_SHA,'old author manifest');rows=[pin(OLD/'manifest.json')]
 for r in json.loads((OLD/'manifest.json').read_text())['exports']:
  q=Path(r['path']);require(not q.is_absolute() and '..'not in q.parts,'safe old export');z=pin(OLD/q);require(all(z[k]==r[k]for k in ['bytes','sha256']),'changed old export');rows.append(z)
 sp=importlib.util.spec_from_file_location('acquired_partial_fusion',OLD/'run_partial_fusion.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m,rows

def receipt_shapes(old,new):
 require(old['status']=='COMPLETE_PARTIAL_INPUT_FUSION' and old['anchors']==list(range(95,1,-1)),'old complete partial input boundary')
 require(old['execution']['status']=='RETURNED' and old['execution']['returncode']==0,'old clean execution')
 require(new['status']=='COMPLETE_REQUEST' and new['requested_anchors']==new['completed_anchors']==[1] and new['unpaid_anchors']==[],'new complete singleton boundary')
 require(new['execution']['status']=='RETURNED' and new['execution']['returncode']==0 and new['audit']['status']=='RETURNED' and new['audit']['returncode']==0,'new clean execution/audit')
 require(new['reported_completed_rows']==new['audited_returned_rows'] and len(new['audited_returned_rows'])==1,'new audited row')
 row=new['audited_returned_rows'][0];require(row==[1,[4,30,196,334,36,0],[4]*6+[5]*36],'new exact actual rank inventory')

def preflight():
 m,pins=load_prior();base,more,oldrows,inv=m.preflight();pins+=more
 pins+=base.manifest_gate(G34/'postprocess_review_v1','2aec2b0183913fc9da8f24b46003311d1f06b60cb0278b517a0bf2538185bb96','ACCEPTED_L100_PARTIAL_AUT_TYPE_FUSION_V1')
 pins+=base.manifest_gate(G34/'level_resume_review_v1','15d74eb84763ff459cda0f12521f00687770ee2b3291b3fe937e236333af3295','ACCEPTED_L100_COMPLETE_LEVEL_CONTINUATION_V1')
 data=[]
 for folder,sha in [(OUTOLD,OLD_RECEIPT),(NEW,NEW_RECEIPT)]:
  rp=folder/'receipt.json';require(pin(rp)['sha256']==sha,'changed exact terminal receipt');d=json.loads(rp.read_text());data.append(d);pins.append(pin(rp));pins +=[base.verify(r)for r in d['inputs']+d['outputs']]
 receipt_shapes(*data)
 require(not(OUTOLD/'execution/stderr').read_bytes()and not(NEW/'target/stderr').read_bytes()and not(NEW/'audit/stderr').read_bytes(),'clean acquired stderr')
 files=[OUTOLD/'result.g',OUTOLD/'automorphisms.g',NEW/'checkpoints/b1_done.g']
 for f,rec in zip(files,[data[0],data[0],data[1]]):
  z=pin(f);require(any(r['path']==str(f)and r['sha256']==z['sha256']for r in rec['outputs']),'bound actual artifact');pins.append(z)
 for n in ['run_incremental.py','incremental.g']:pins.append(pin(HERE/n))
 row=data[1]['audited_returned_rows'][0];newrow=[1,str(files[2]),row[1],row[2]]
 return base,base.unique_pins(pins),newrow

def prepare(out):
 base,pins,row=preflight();require(not out.exists(),'fresh output');out.mkdir(parents=True);q=lambda x:json.dumps(str(x))
 lines=['SizeScreen([100000,24]);;','INPUT_CATALOGUE:='+q(base.P/'input_catalogue01.g')+';;','Read('+q(base.P/'catalogue_loader_v2.g')+');;',
 'Read('+q(OUTOLD/'result.g')+');;','Read('+q(OUTOLD/'automorphisms.g')+');;',
 'Read('+q(OLD/'legacy_fusion_functions.g')+');;','Read('+q(OLD/'fusion_witness.g')+');;',
 'borelResult:=rec();;','NEW_ROW:='+json.dumps(row)+';;','OUTPUT_DIR:='+q(out)+';;','Read('+q(HERE/'incremental.g')+');;','QUIT_GAP(0);']
 (out/'driver.g').write_text('\n'.join(lines)+'\n');pins.append(pin(out/'driver.g'))
 r=dict(status='PREPARED_INCREMENTAL_FUSION',inputs=base.unique_pins(pins),command=[str(base.GAP),'-q','-b',str(out/'driver.g')],cap_seconds=60,old_member_count=103,new_member_count=42,total_input_members=145,old_anchors=list(range(95,1,-1)),new_anchor=[1],full_Aut_recomputed=False,old_members_reclassified=False,target_census=False,target_postprocessing=True,source_count_credit=0,whole_original_credit=0)
 base.save(out/'receipt.json',r);return base,r

def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--prepare-only',action='store_true');ns=a.parse_args();out=ns.out.absolute();base,r=prepare(out)
 if ns.prepare_only:print('PREPARED_INCREMENTAL_FUSION_NO_TARGET');return
 try:
  r['status']='ACTIVE_POSTPROCESSING';base.save(out/'receipt.json',r);ex=base.phase(r['command'],out/'execution',60,False);r['execution']=ex
  text=(out/'execution/stdout').read_text(errors='replace');err=(out/'execution/stderr').read_bytes()
  if not base.unchanged(r['inputs']):status='INVALIDATED_INPUT_CHANGE'
  elif err or any(l.startswith(('Error','Syntax warning','Syntax error'))for l in text.splitlines()):status='FAILED_POSTPROCESSING'
  elif ex['status']=='DEADLINE':status='PARTIAL_POSTPROCESSING_DEADLINE'
  elif base.clean_phase(ex,out/'execution')and len([l for l in text.splitlines()if l.startswith('PASS_INCREMENTAL_AUT_TYPE_FUSION ')])==1 and(out/'result.g').is_file():status='COMPLETE_INCREMENTAL_FUSION'
  else:status='FAILED_POSTPROCESSING'
  r.update(status=status,outputs=[pin(p)for p in sorted(out.rglob('*'))if p.is_file()and p!=out/'receipt.json'],finished_unix=time.time());base.save(out/'receipt.json',r);print(json.dumps(dict(status=status,total_input_members=145)))
  if status not in ['COMPLETE_INCREMENTAL_FUSION','PARTIAL_POSTPROCESSING_DEADLINE']:raise SystemExit(2)
 except Exception as exc:
  r.update(status='FAILED_INTERFACE',error=repr(exc),finished_unix=time.time());r['outputs']=[pin(p)for p in sorted(out.rglob('*'))if p.is_file()and p!=out/'receipt.json'];base.save(out/'receipt.json',r);raise
if __name__=='__main__':main()
