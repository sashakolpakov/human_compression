"""One bounded literal-coset/palette postprocessing call. No subgroup census."""
import argparse,hashlib,importlib.util,json,sys,time
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;G34=HERE.parent;S=G34.parents[1];PREV=G34/'incremental_fusion_interface_v2';TARGET=G34/'incremental_target02'
PREV_SHA='d999f917fabb9389589e71b1e1311b2943a943fde042c98e8c3defd222cbd533'
RESULT_RECEIPT='185dd6f7857c5cfbfa3932928c77e906213c32cfc8e03bedd1149788c418c207'
PKG=Path('/opt/homebrew/Cellar/gap/4.15.1/lib/gap/pkg');NAUTY=PKG/'grape/bin/aarch64-apple-darwin25-default64-kv10/dreadnaut'
def need(x,s):
 if not x:raise ValueError(s)
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),resolved=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def shape(r):
 need(r['status']=='COMPLETE_INCREMENTAL_FUSION'and r['old_member_count']==103 and r['new_member_count']==42 and r['total_input_members']==145,'exact acquired complete family input')
 need(r['old_anchors']==list(range(95,1,-1))and r['new_anchor']==[1]and r['execution']['status']=='RETURNED'and r['execution']['returncode']==0,'all95 complete input anchors')
def preflight():
 need(pin(PREV/'manifest.json')['sha256']==PREV_SHA,'exact acquired caller');rows=[pin(PREV/'manifest.json')]
 for r in json.loads((PREV/'manifest.json').read_text())['exports']:
  q=Path(r['path']);need(not q.is_absolute()and'..'not in q.parts,'safe acquired export');z=pin(PREV/q);need(all(z[k]==r[k]for k in ['bytes','sha256']),'changed acquired export');rows.append(z)
 sp=importlib.util.spec_from_file_location('accepted_incremental_preflight',PREV/'run_incremental.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);base,old,newrow=m.preflight();rows+=old
 rows+=base.manifest_gate(G34/'incremental_fusion_review_v2','512d574566754cbb13a2c07975bb48949401aa5e34bfa3f466f8c032a223a281','ACCEPTED_L100_INCREMENTAL_AUT_TYPE_FUSION_V2')
 rp=TARGET/'receipt.json';need(pin(rp)['sha256']==RESULT_RECEIPT,'exact complete fusion receipt');r=json.loads(rp.read_text());shape(r);rows.append(pin(rp));rows +=[base.verify(x)for x in r['inputs']+r['outputs']]
 need(not(TARGET/'execution/stderr').read_bytes(),'clean complete fusion stderr');z=pin(TARGET/'result.g');need(any(q['path']==z['path']and q['sha256']==z['sha256']for q in r['outputs']),'bound actual complete representatives');rows.append(z)
 for n in ['run_palette.py','driver_body.g','cosets.g','palette.g']:rows.append(pin(HERE/n))
 for package,files in [('grape',['init.g','PackageInfo.g','lib/grape.g','lib/smallestimage.g']),('json',['init.g','read.g','PackageInfo.g','gap/json.gi','gap/json.gd','bin/aarch64-apple-darwin25-default64-kv10/json.so'])]:
  rows +=[pin(PKG/package/n)for n in files]
 rows.append(pin(NAUTY))
 for n in ['phase188_gadget_check.g','phase188_F010_independent_review.md','phase188_review.json','phase197_recognizable_representations.md','topic_Representation_root_adoption/manifest.json']:
  rows.append(pin(S/n))
 return base,base.unique_pins(rows)
def prepare(out):
 base,rows=preflight();need(not out.exists(),'fresh output');out.mkdir(parents=True);q=lambda x:json.dumps(str(x))
 lines=['LoadPackage("grape");;LoadPackage("json");;SizeScreen([100000,24]);;', 'GRAPE_RANDOM:=false;;GRAPE_NAUTY:=true;;GRAPE_DREADNAUT_EXE:='+q(NAUTY)+';;',
 'INPUT_CATALOGUE:='+q(base.P/'input_catalogue01.g')+';;','Read('+q(base.P/'catalogue_loader_v2.g')+');;',
 'Read('+q(TARGET/'result.g')+');;','OUTPUT_DIR:='+q(out)+';;','Read('+q(HERE/'cosets.g')+');;','Read('+q(HERE/'palette.g')+');;','Read('+q(HERE/'driver_body.g')+');;']
 (out/'driver.g').write_text('\n'.join(lines)+'\n');rows.append(pin(out/'driver.g'))
 r=dict(status='PREPARED_LITERAL_PALETTE',inputs=base.unique_pins(rows),command=[str(base.GAP),'-q','-b',str(out/'driver.g')],cap_seconds=60,target_census=False,target_postprocessing=True,source_credit=0,whole_original_credit=0)
 base.save(out/'receipt.json',r);return base,r
def main():
 a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--prepare-only',action='store_true');ns=a.parse_args();out=ns.out.absolute();base,r=prepare(out)
 if ns.prepare_only:print('PREPARED_LITERAL_PALETTE_NO_EXECUTION');return
 try:
  r['status']='ACTIVE_PALETTE_POSTPROCESSING';base.save(out/'receipt.json',r);ex=base.phase(r['command'],out/'execution',60,False);r['execution']=ex;text=(out/'execution/stdout').read_text(errors='replace');err=(out/'execution/stderr').read_bytes()
  if not base.unchanged(r['inputs']):status='INVALIDATED_INPUT_CHANGE'
  elif err or any(x.startswith(('Error','Syntax warning','Syntax error'))for x in text.splitlines()):status='FAILED_PALETTE_POSTPROCESSING'
  elif ex['status']=='DEADLINE':status='PARTIAL_PALETTE_DEADLINE'
  elif base.clean_phase(ex,out/'execution')and text.count('PASS_COMPLETE_LITERAL_PALETTE ')==1 and(out/'result.json').is_file():status='COMPLETE_LITERAL_PALETTE'
  else:status='FAILED_PALETTE_POSTPROCESSING'
  r.update(status=status,outputs=[pin(p)for p in sorted(out.rglob('*'))if p.is_file()and p!=out/'receipt.json'],finished_unix=time.time());base.save(out/'receipt.json',r);print(json.dumps(dict(status=status)))
  if status not in ['COMPLETE_LITERAL_PALETTE','PARTIAL_PALETTE_DEADLINE']:raise SystemExit(2)
 except Exception as e:
  r.update(status='FAILED_INTERFACE',error=repr(e),outputs=[pin(p)for p in sorted(out.rglob('*'))if p.is_file()and p!=out/'receipt.json']);base.save(out/'receipt.json',r);raise
if __name__=='__main__':main()
