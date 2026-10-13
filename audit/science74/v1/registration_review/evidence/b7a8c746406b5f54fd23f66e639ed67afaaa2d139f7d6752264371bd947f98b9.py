from pathlib import Path
import hashlib,json,shutil,datetime,subprocess
S=Path('/Users/sasha/medusa/research/leemans');R=S.parents[1]/'math_compression';W=S/'reboot_20261013/F006_publication_work';T=W/'stage01';AUD='audit/science74/v1';review=S/'reboot_20261013/F006_registration_distinct'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):
 p=T/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(v if isinstance(v,bytes)else(json.dumps(v,indent=2)+'\n').encode())
def pin(p,base):return dict(path=str(p.relative_to(base)),bytes=p.stat().st_size,sha256=digest(p))
m=json.loads((review/'manifest.json').read_text());write(AUD+'/registration_review/manifest.json',(review/'manifest.json').read_bytes())
for r in m['exports']:
 p=review/r['path'];assert digest(p)==r['sha256']and p.stat().st_size==r['bytes'];write(AUD+'/registration_review/'+r['path'],p.read_bytes())
mapping={}
for r in json.loads((review/'dependencies.json').read_text())['bindings']:
 p=S/r['path'];assert digest(p)==r['sha256']and p.stat().st_size==r['bytes']
 prefix='reboot_20261013/F006_publication_work/review_repo01/'
 if r['path'].startswith(prefix):
  n=r['path'][len(prefix):];base=T if (T/n).is_file()else R;assert digest(base/n)==r['sha256'];mapping[r['path']]=pin(base/n,base)
 else:
  n=AUD+'/registration_review/evidence/'+r['sha256']+p.suffix;write(n,p.read_bytes());mapping[r['path']]=pin(T/n,T)
write(AUD+'/registration_review/public_mapping.json',mapping)
exclude={'audit/protocol.aux','audit/protocol.log','audit/protocol.out','audit/pass1.log','audit/pass2.log'}
def selected(p):
 n=str(p.relative_to(T));return p.is_file()and n not in exclude and not n.startswith('audit/protocol-page-')
rows=[pin(p,T)for p in sorted(T.rglob('*'))if selected(p)]
assert not any(r['path'].endswith('.md')for r in rows)
write(AUD+'/root_integration.json',dict(status='ROOT_ACCEPTED_SCIENCE74_PUBLICATION',source_ids=['F006'],whole_original_credit=1,scope='Full Dn rank spectrum and all connected source table cells; literal disconnected I2/H3/E7 and Lemma19 corrections, retained classifications and computational premises remain explicit.',root_review='Complete mathematical assembly and acquired components, distinct whole review, separate exact-warning assessment, complete public restoration review and final independent registration review read and adopted. New/common scientific pages and final protocol changed pages1/3 directly viewed.',bindings=rows,new_question_credit=0,new_Lean_declarations=0,new_measurements=0,compression_factor=None,utc=datetime.datetime.now(datetime.timezone.utc).isoformat()))
# Prior public worktree must still be the clean reviewed baseline.
assert subprocess.check_output(['git','-C',str(R),'rev-parse','HEAD'],text=True).strip()=='e3901a93c5551e526f4703a06bec8c8f4ae1a2f9'
assert not subprocess.check_output(['git','-C',str(R),'status','--porcelain'],text=True).strip()
rows.append(pin(T/AUD/'root_integration.json',T))
for r in rows:
 p=T/r['path'];q=R/r['path'];q.parent.mkdir(parents=True,exist_ok=True)
 if q.exists():q.unlink()
 shutil.copyfile(p,q)
(W/'integration01/installed_paths.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(dict(status='INSTALLED_REVIEWED_SCIENCE74',files=len(rows),source_id='F006',full_snapshot_required=True)))
