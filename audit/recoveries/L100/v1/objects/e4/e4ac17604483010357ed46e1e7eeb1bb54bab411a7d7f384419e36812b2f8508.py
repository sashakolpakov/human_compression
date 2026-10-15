import hashlib,importlib.util,json,sys
from pathlib import Path
if not __debug__:raise SystemExit('optimized execution forbidden')
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;G34=W.parent;P=G34/'incremental_fusion_interface_v1';out=G34/'aut_reuse_probe01'
sp=importlib.util.spec_from_file_location('accepted_incremental_probe_input',P/'run_incremental.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
base,pins,row=m.preflight();assert not out.exists();out.mkdir()
pins +=[m.pin(W/n)for n in ['run_probe.py','initialization.g','inspection.rst']]
pins.append(m.pin(Path('/opt/homebrew/Cellar/gap/4.15.1/share/gap/lib/morpheus.gi')))
(out/'driver.g').write_text('OUTPUT_DIR:='+json.dumps(str(out))+';;\nRead('+json.dumps(str(W/'initialization.g'))+');;\n');pins.append(m.pin(out/'driver.g'))
r=dict(status='ACTIVE_INITIALIZER_ONLY',inputs=base.unique_pins(pins),command=[str(base.GAP),'-q','-b',str(out/'driver.g')],cap_seconds=20,root_instruction='Read full inspection and initialization; changed one20s initializer-only diagnostic authorized',target_census=False,target_postprocessing=False,independent_order_check=False)
base.save(out/'receipt.json',r);ex=base.phase(r['command'],out/'execution',20,False);text=(out/'execution/stdout').read_text();r['execution']=ex
if not base.unchanged(r['inputs']):status='INVALIDATED_INPUT_CHANGE'
elif(ex['status']=='DEADLINE'):status='INITIALIZER_DEADLINE'
elif base.clean_phase(ex,out/'execution')and 'PASS_SAVED_AUT_INITIALIZATION'in text:status='PASS_SAVED_AUT_INITIALIZATION'
else:status='FAILED_INITIALIZER'
r.update(status=status,outputs=[m.pin(p)for p in sorted(out.rglob('*'))if p.is_file()and p.name!='receipt.json'],stdout=text);base.save(out/'receipt.json',r);print(json.dumps(dict(status=status,execution=ex,stdout=text)))
