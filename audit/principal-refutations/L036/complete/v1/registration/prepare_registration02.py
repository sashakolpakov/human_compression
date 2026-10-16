"""Assemble the three narrative clarifications requested in root review, privately."""
from pathlib import Path
import ctypes,difflib,hashlib,json,os,shutil,subprocess,sys
W=Path(__file__).resolve().parent
Q=W/'registration_candidate02';OLD=W/'registration_candidate01'
R=Path('/Users/sasha/medusa/math_compression')
def pin(p,base):return dict(path=str(p.relative_to(base)),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def save(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def clone(src,dst):
 dst.parent.mkdir(parents=True,exist_ok=True)
 if sys.platform=='darwin':
  f=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True).clonefile
  f.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_int];f.restype=ctypes.c_int
  if f(os.fsencode(src),os.fsencode(dst),0):raise OSError(ctypes.get_errno(),str(dst))
 else:shutil.copyfile(src,dst)
 assert src.read_bytes()==dst.read_bytes()
def main():
 assert not Q.exists()
 assert pin(OLD/'manifest.json',OLD)['sha256']=='17d4e850324e3ff660319d26a54df381efcd848180c5389c5a2509e3c954bf26'
 Q.mkdir()
 for row in json.loads((OLD/'manifest.json').read_text())['exports']:
  assert pin(OLD/row['path'],OLD)==row
  if row['path'] in ['author_check.json','native_review.json'] or row['path'].startswith('native_protocol/'):continue
  clone(OLD/row['path'],Q/row['path'])
 replacements={
 'README.rst':('It does not give the corrected exact total or recover the other\neleven table rows.', 'That earlier correction established only the lower bound. The complete\nL036 treatment linked above now supplies the exact total and the other\neleven counts.'),
 'audit/completion.rst':('It does not give the corrected exact total or recover the other\neleven table rows.', 'That earlier correction established only the lower bound. The complete\nL036 treatment linked above now supplies the exact total and the other\neleven counts.'),
 'audit/protocol.tex':('For L036 the lower bound $50669>1511$ refutes the fixed Ru total without\nclaiming a corrected exact total or recovering the other eleven rows.', 'The earlier L036 correction established the lower bound $50669>1511$;\nthe complete treatment above now gives the exact total and the other\neleven counts.')}
 delta=[];narratives=[]
 for name,(before,after) in replacements.items():
  p=Q/'proposed'/name;s=p.read_text();assert s.count(before)==1;p.write_text(s.replace(before,after))
  delta.append(dict(path=name,before=before,after=after,old=pin(OLD/'proposed'/name,OLD/'proposed'),new=pin(p,Q/'proposed')))
  narratives.append(dict(path=name,before=pin(R/name,R),after=pin(p,Q/'proposed')))
  (Q/(name.replace('/','_')+'.diff')).write_text(''.join(difflib.unified_diff((R/name).read_text().splitlines(keepends=True),p.read_text().splitlines(keepends=True),fromfile=name,tofile='proposed/'+name)))
 save(Q/'narrative_changes.json',narratives)
 save(Q/'edition_delta.json',dict(predecessor=pin(OLD/'manifest.json',OLD),scope='Exactly three historical-scope paragraph clarifications and derived protocol rendering/bindings. No mathematical or counter change.',replacements=delta))
 native=Q/'native_protocol';native.mkdir()
 for k in (1,2):
  r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory',str(native),str(Q/'proposed/audit/protocol.tex')],capture_output=True,cwd=Q/'proposed/audit')
  (native/f'pass{k}.stdout').write_bytes(r.stdout);(native/f'pass{k}.stderr').write_bytes(r.stderr);r.check_returncode()
 assert 'Overfull' not in (native/'protocol.log').read_text()
 shutil.copyfile(native/'protocol.pdf',Q/'proposed/audit/protocol.pdf')
 subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r100','-dFirstPage=1','-dLastPage=2','-sOutputFile='+str(native/'page-%02d.png'),str(native/'protocol.pdf')],check=True)
 p=Q/'proposal.json';a=json.loads(p.read_text());a['proposed_paths']=sorted(str(x.relative_to(Q/'proposed')) for x in (Q/'proposed').rglob('*') if x.is_file());save(p,a)
 print(Q)
if __name__=='__main__':main()
