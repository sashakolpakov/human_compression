from pathlib import Path
import subprocess,json,time,hashlib,sys
w=Path(__file__).resolve().parent
for i in [int(x) for x in sys.argv[1:]]:
 out=w/('case%02d'%i)
 if out.exists():raise RuntimeError('existing case receipt')
 out.mkdir();driver=out/'driver.g';driver.write_text('CaseNumber:='+str(i)+';Read("check_case.g");\n')
 t=time.monotonic()
 try:
  r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b',str(driver)],cwd=w,capture_output=True,timeout=60)
  (out/'stdout').write_bytes(r.stdout);(out/'stderr').write_bytes(r.stderr)
  status='PASS' if not r.stderr and (b'PASS_CASE' in r.stdout or b'REJECT_NONPROPER_END' in r.stdout) else 'FAILED_NO_CERTIFICATE'
  rec=dict(case=i,status=status,returncode=r.returncode,seconds=time.monotonic()-t)
 except subprocess.TimeoutExpired as e:
  (out/'stdout').write_bytes(e.stdout or b'');(out/'stderr').write_bytes(e.stderr or b'');rec=dict(case=i,status='TIMEOUT_NO_CERTIFICATE',seconds=time.monotonic()-t)
 rec['inputs']=[dict(path=n,sha256=hashlib.sha256((w/n).read_bytes()).hexdigest())for n in ['point_input.g','case_input.g','check_case.g']]
 (out/'receipt.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec),flush=True)
