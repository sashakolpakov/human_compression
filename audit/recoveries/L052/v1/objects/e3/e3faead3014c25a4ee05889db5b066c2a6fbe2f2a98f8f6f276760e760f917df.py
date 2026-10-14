from pathlib import Path
import json,hashlib,shutil
S=Path('/Users/sasha/medusa/research/leemans');A=S/'corpus106_L052_finite_v1';W=S/'reboot_20261013/L052_work';D=W/'historical_preflight_exact01';D.mkdir(exist_ok=True);m={x['path']:x for x in json.loads((A/'author_preflight_manifest.json').read_text())['exports']};out=[]
def save(name,b,route):
 x=m[name];h=hashlib.sha256(b).hexdigest();print(name,len(b),h,h==x['sha256'])
 if h==x['sha256']:
  (D/name).write_bytes(b);out.append({'path':name,'bytes':len(b),'sha256':h,'literal_reconstruction':route});return True
 return False
save('finite.tex',(W/'finite.tex').read_bytes(),'Exact original retained work file')
save('check.py',(W/'finite_stage01/author_wrapper_before_native_repair.py').read_bytes(),'Exact retained historical wrapper')
t=(A/'README.rst').read_text();save('README.rst',t.split('\nAuthor validation ran')[0].encode(),'Remove the final appended author validation paragraph, retaining prior newline')
d=json.loads((A/'development.json').read_text());del d['preflight03'];save('development.json',(json.dumps(d,indent=2)+'\n').encode(),'Remove final preflight03 key')
d=json.loads((A/'finite_source_map.json').read_text());del d['Table1_polytope_route'];save('finite_source_map.json',(json.dumps(d,indent=2)+'\n').encode(),'Remove final Table1_polytope_route key')
t=(A/'literal.py').read_text();a=t.index("        entry={'id':");b=t.index('        result.append(entry)',a)+len('        result.append(entry)');s=t[:a]+"        result.append({'id':row['id'],'rotation_order':len(ss[-1]),'subset_pairs':256})"+t[b:];save('literal.py',s.encode(),'Replace added entry/poset_tests block by original inline result.append literal')
(D/'reconstruction.json').write_text(json.dumps({'status':'EXACT_HASH_CHECKED_HISTORICAL_FILES','files':out,'accepted_final_packet_unmodified':True},indent=2)+'\n')
