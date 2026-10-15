"""Single bounded anchor1 continuation from exactly completed levels1..4."""
import argparse,hashlib,importlib.util,json,shutil,sys,time,re
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
G34=HERE.parent
OLD=G34/'exhaustion_single_interface_v1'
OLD_SHA='5c89f00440bed0ac7995aee436d3999982c07e52297e50a4ecdcd6fd6b047d09'
PRIOR=G34/'exhaustion_target04_anchor1'
PRIOR_SHA='d9c6a840e621857170a4fc28c8c8a82f41981dafbddf7d94566136d5a3d7a6a4'
COUNTS=[4,30,196,334]
CAP=300

def require(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 p=Path(p).absolute();b=p.read_bytes();return dict(path=str(p),resolved=str(p.resolve()),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def load_base():
 mp=OLD/'manifest.json';require(pin(mp)['sha256']==OLD_SHA,'changed accepted singleton wrapper');m=json.loads(mp.read_text());pins=[pin(mp)]
 for r in m['exports']:
  p=Path(r['path']);require(not p.is_absolute() and '..' not in p.parts,'unsafe predecessor export');a=pin(OLD/p);require(all(a[k]==r[k] for k in ['bytes','sha256']),'changed predecessor export');pins.append(a)
 sys.path.insert(0,str(OLD));sp=importlib.util.spec_from_file_location('accepted_singleton',OLD/'run_target.py');base=importlib.util.module_from_spec(sp);sp.loader.exec_module(base);base.IDS=[1]
 return base,pins

def prior_shape(d,stdout):
 require(d['status']=='PARTIAL_DEADLINE' and d['requested_anchors']==[1] and d['completed_anchors']==[] and d['unpaid_anchors']==[1],'wrong prior boundary')
 require(d['execution']['status']=='DEADLINE' and d['audit']['status']=='RETURNED' and d['audit']['returncode']==0,'prior process boundary')
 require(d['reported_completed_rows']==d['audited_returned_rows']==[],'prior incorrectly claims completion')
 lines=[l for l in stdout.splitlines() if l.startswith('BOREL_LEVEL')]
 expected=[f'BOREL_LEVEL id=1 rank={r} classes={c} full_group={6 if r==4 else 0}' for r,c in enumerate(COUNTS,1)]
 require(lines==expected,'wrong completed level markers')
 require('BOREL_COMPLETE' not in stdout and 'L100_REQUESTED_ANCHORS_COMPLETE' not in stdout,'prior false terminal')
 require(not (PRIOR/'prepared/checkpoints/b1_r5.g').exists() and not (PRIOR/'prepared/checkpoints/b1_done.g').exists(),'unexpected later checkpoint')

def preflight():
 base,pins=load_base();pins+=base.preflight()
 pins+=base.manifest_gate(G34/'exhaustion_single_review_v1','060886859d7c01dce43839fc37480913f8a5554c54665fec46c039759885aab9','ACCEPTED_L100_SINGLE_ANCHOR_INTERFACE_V1')
 rp=PRIOR/'receipt.json';require(pin(rp)['sha256']==PRIOR_SHA,'changed exact partial execution');d=json.loads(rp.read_text());prior_shape(d,(PRIOR/'target/stdout').read_text());pins.append(pin(rp))
 pins+=[base.verify(r) for r in d['inputs']+d['outputs']]
 require(not (PRIOR/'target/stderr').read_bytes() and not (PRIOR/'audit/stderr').read_bytes(),'prior stderr')
 for r in range(2,5):
  p=PRIOR/f'prepared/checkpoints/b1_r{r}.g';z=pin(p);require(any(e['path']==str(p) and e['sha256']==z['sha256'] for e in d['outputs']),'unbound completed level');pins.append(z)
 sp=importlib.util.spec_from_file_location('literal_resume_delta',HERE/'prepare_delta.py');delta=importlib.util.module_from_spec(sp);sp.loader.exec_module(delta)
 require((HERE/'resume_borel.g').read_text()==delta.derive((base.P/'legacy_functions.g').read_text()),'nonliteral search-loop delta')
 for n in ['run_level_resume.py','prepare_delta.py','resume_borel.g','validate_resume.g']:pins.append(pin(HERE/n))
 return base,base.unique_pins(pins)

def prepare(out):
 base,pins=preflight();require(not out.exists(),'output already exists');out.mkdir(parents=True);cp=out/'checkpoints';cp.mkdir()
 for r in range(2,5):shutil.copyfile(PRIOR/f'prepared/checkpoints/b1_r{r}.g',cp/f'b1_r{r}.g')
 q=lambda x:json.dumps(str(x))
 setup='INPUT_CATALOGUE:='+q(base.P/'input_catalogue01.g')+';;\nRead('+q(base.P/'catalogue_loader_v2.g')+');;'
 lines=['SizeScreen([100000,24]);;',setup,'OUTPUT_DIR:='+q(cp)+';;','Read('+q(base.P/'legacy_functions.g')+');;',
  'Read('+q(HERE/'validate_resume.g')+');;','Read('+q(HERE/'resume_borel.g')+');;',
  'borelCheckpoint:=rec();;RESUME_CHECKPOINTS:=[];;']
 for r in range(2,5):lines+=['Read('+q(cp/f'b1_r{r}.g')+');;Add(RESUME_CHECKPOINTS,borelCheckpoint);;']
 lines+=['RESUME_STATE:=ValidateLevelResume(1,RESUME_CHECKPOINTS,'+str(COUNTS)+');;',
  'if RESUME_STATE=fail or REQUIRE_2T<>false then Error("invalid completed-level resume");fi;',
  'RunBorelFromLevel(1,RESUME_STATE);;','Print("L100_REQUESTED_ANCHORS_COMPLETE\\n");','QUIT_GAP(0);']
 (out/'driver.g').write_text('\n'.join(lines)+'\n')
 pins += [pin(out/'driver.g')]+[pin(p) for p in sorted(cp.iterdir())]
 r=dict(status='PREPARED_LEVEL_CONTINUATION',target_census=True,requested_anchors=[1],completed_anchors=[],unpaid_anchors=[1],reused_complete_levels=COUNTS,restarted_level=5,restarted_candidate=1,unpaid_prior_candidate_prefix={'through':130,'accepted_count':27,'saved_tuples':False,'credit':0},target_cap_seconds=CAP,audit_cap_seconds=20,inputs=base.unique_pins(pins),prior_receipt=pin(PRIOR/'receipt.json'),whole_original_credit=0,source_count_credit=0)
 base.save(out/'receipt.json',r);return base,r,setup

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);ap.add_argument('--prepare-only',action='store_true');ns=ap.parse_args();out=ns.out.absolute()
 base,r,setup=prepare(out)
 if ns.prepare_only:print('PREPARED_LEVEL_CONTINUATION_NO_TARGET');return
 r['status']='ACTIVE_TARGET';base.save(out/'receipt.json',r)
 execution=base.phase([str(base.GAP),'-q','-b',str(out/'driver.g')],out/'target',CAP,True);r['execution']=execution
 stdout=(out/'target/stdout').read_text(errors='replace');stderr=(out/'target/stderr').read_bytes();rows=base.completed_rows(stdout,[1]);r['reported_completed_rows']=rows
 cpins=base.checkpoint_files(out/'checkpoints',rows);ad=base.audit_driver(out,out/'checkpoints',rows,setup);r['inputs']=base.unique_pins(r['inputs']+cpins+[pin(ad)])
 ar=base.phase([str(base.GAP),'-q','-b',str(ad)],out/'audit',20,False);r['audit']=ar
 audited=[];astr=(out/'audit/stdout').read_text(errors='replace')
 for l in astr.splitlines():
  if l.startswith('AUDITED '):audited.append(json.loads(l[len('AUDITED '):]))
 auditok=base.clean_phase(ar,out/'audit') and 'PASS_RETURNED_ANCHOR_AUDIT' in astr and audited==rows
 r.update(audited_returned_rows=audited,status=base.classify(execution,stderr.decode(errors='replace'),stdout,rows,[1],auditok,base.unchanged(r['inputs'])),completed_anchors=[x[0] for x in rows] if auditok else [],finished_unix=time.time())
 r['unpaid_anchors']=[i for i in [1] if i not in r['completed_anchors']]
 r['outputs']=[pin(p) for p in sorted(out.rglob('*')) if p.is_file() and p!=out/'receipt.json'];base.save(out/'receipt.json',r)
 print(json.dumps(dict(status=r['status'],completed=r['completed_anchors'],unpaid=r['unpaid_anchors'])))
 if r['status'] not in ('COMPLETE_REQUEST','PARTIAL_DEADLINE'):raise SystemExit(2)
if __name__=='__main__':main()
