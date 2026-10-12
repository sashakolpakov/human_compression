import hashlib,json,subprocess,time
from pathlib import Path
P=Path(__file__).resolve().parent
bindings={n:{'bytes':(P/n).stat().st_size,'sha256':hashlib.sha256((P/n).read_bytes()).hexdigest()} for n in ['shadow_residues.g','prior_representatives.g','run.g']}
start=time.monotonic()
r=subprocess.run(['/opt/homebrew/bin/gap','-q','-b','-T','run.g'],cwd=P,capture_output=True,text=True,timeout=120)
(P/'stdout.log').write_text(r.stdout);(P/'stderr.log').write_text(r.stderr)
passed=r.returncode==0 and not r.stderr.strip() and 'PASS_M12_MISSING_CLASS18' in r.stdout
report={'passed':passed,'seconds':time.monotonic()-start,'returncode':r.returncode,'inputs':bindings}
(P/'execution.json').write_text(json.dumps(report,indent=2)+'\n')
if not passed: raise RuntimeError(r.stderr[-1500:]+r.stdout[-1500:])
row=json.loads(next(s[7:] for s in r.stdout.splitlines() if s.startswith('RESULT|')))
(P/'result.json').write_text(json.dumps(row,indent=2)+'\n')
print(json.dumps({'passed':passed,'seconds':report['seconds'],'filters':row['filters'],'IP':row['IP'],'WIP':row['WIP'],'parabolic_orders':row['parabolic_orders'],'borel_order':row['borel_order']}))
