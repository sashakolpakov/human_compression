import sys
if sys.flags.optimize:raise RuntimeError('Normal Python required')
from pathlib import Path
import json,ast,hashlib,gzip,re
from pypdf import PdfReader
R=Path('/Users/sasha/medusa/math_compression');W=Path(__file__).resolve().parent;P=W.parent/'N010_publication_work'
def load(p):return json.loads(p.read_text())
old=(R/'audit/science84/v1/previous/scripts/verify_snapshot.py').read_text();new=(R/'scripts/verify_snapshot.py').read_text()
def main(t):return ast.dump(next(n for n in ast.parse(t).body if isinstance(n,ast.FunctionDef)and n.name=='main'),include_attributes=False)
expected=old.replace('    science83_history = check_previous_science83()',"    science84_history = check_previous_science84()\n    science83_history = science84_history['previous']").replace('    science72 = check_science83()','    science72 = check_science84()').replace("print('PASS: exact science82 history preserved; L052 corrected hypertope recovery adds one original.')","print('PASS: exact science83 history preserved; N010 attributed survey disposition adds one original.')")
assert main(expected)==main(new)
a=load(R/'audit/recoveries/N010/v1/admission.json');texts=[];pages=[]
for m in a['new_native_manuscripts']:
 pp=PdfReader(R/m['pdf']['path']).pages;assert len(pp)==m['physical_pages'];texts.extend(p.extract_text()for p in pp);pages.append(len(pp))
assert pages==[11,4,3,2,2] and texts==[p.extract_text()for p in PdfReader(R/a['complete_reading_volume']['path']).pages]
t0=load(P/'stage01/audit/recoveries/N010/v1/transport.json');t1=load(R/'audit/recoveries/N010/v1/transport.json');assert len(t0['files'])==len(t1['files'])==5962
changed=[]
for x,y in zip(t0['files'],t1['files']):
 for k in ['origin','path','bytes','sha256']:assert x.get(k)==y.get(k)
 if x!=y:
  assert x['transport']=='EXISTING_PUBLIC'and y['transport']=='NEW_FROZEN_FILE'and y['public_path'].endswith('.bin');b=(R/y['public_path']).read_bytes();assert len(b)==y['bytes']and hashlib.sha256(b).hexdigest()==y['sha256'];changed.append(y['path'])
assert len(changed)==6
links=[]
for doc in ['README.rst','audit/completion.rst']:
 text=(R/doc).read_text()
 for ref in re.findall(r'<([^>]*recoveries/(?:N010|L052)/v1/PUBLICATION\.rst)>',text):
  target=(R/doc).parent/ref;assert target.is_file();links.append([doc,ref])
assert len(links)==4
for n in ['protocol1.stderr','protocol2.stderr']:assert not(R/'audit/science84/v1'/n).read_bytes()
log=(R/'audit/science84/v1/protocol2.stdout').read_text();assert 'Overfull'not in log and 'LaTeX Warning:'not in log
report=dict(status='PASS_ADDITIONAL_REGISTRATION_INTERFACES',exact_main_ast=True,native_component_pages=pages,complete_volume_is_exact_concatenation=True,storage_changes=changed,all_5962_logical_identities_unchanged=True,current_guide_links=links,native_log_clean=True)
(W/'additional_report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
