import hashlib,importlib.util,json,sys
from pathlib import Path
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
W=Path(__file__).resolve().parent;G34=W.parent;out=G34/'palette_controls01';assert not out.exists();out.mkdir()
sp=importlib.util.spec_from_file_location('acquired_phase',G34/'exhaustion_target_interface_v1/run_target.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
rows=[pin(W/n)for n in ['cosets.g','palette.g','controls.g','run_controls.py']]
(out/'driver.g').write_text('CODE_DIR:='+json.dumps(str(W))+';;\nOUTPUT_DIR:='+json.dumps(str(out))+';;\nRead('+json.dumps(str(W/'controls.g'))+');;\n');rows.append(pin(out/'driver.g'))
r=dict(status='ACTIVE_SMALL_PALETTE_CONTROLS',inputs=rows,target_census=False,L100_postprocessing=False);m.save(out/'receipt.json',r)
ex=m.phase(['/opt/homebrew/bin/gap','-q','-b',str(out/'driver.g')],out/'execution',30,False);r['execution']=ex;stdout=(out/'execution/stdout').read_text()
r.update(status='PASS_SMALL_PALETTE_CONTROLS'if m.clean_phase(ex,out/'execution')and 'PASS_LITERAL_PALETTE_CONTROLS'in stdout else'FAILED_SMALL_PALETTE_CONTROLS',stdout=stdout,outputs=[pin(p)for p in out.rglob('*')if p.is_file()and p!=out/'receipt.json']);m.save(out/'receipt.json',r);print(json.dumps(r))
