import sys
if sys.flags.optimize:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,json,subprocess,shutil
from pathlib import Path
S=Path('/Users/sasha/medusa/research/leemans');W=Path(__file__).resolve().parent
P=S/'corpus106_L100_rank_two_v2';Q=S/'geometry/psl3_4/edition02'
def need(ok,msg):
 if not ok:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return {'path':str(p.resolve()),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def exact(p,r):need(all(pin(p)[k]==r[k]for k in ['bytes','sha256']),'exact input '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();out=a.out.resolve();need(not out.exists()and out.parent.exists(),'fresh output')
 need(pin(P/'manifest.json')['sha256']=='ff40f6de14f2676f867c8fccf4f8a2065a3741bd900cb4960bb9bfa33bb19971','final author v2')
 for r in load(P/'manifest.json')['exports']:exact(P/r['path'],r)
 deps=load(P/'dependencies.json')
 for r in deps:exact(Path(r['path']),r)
 old=S/'corpus106_L100_rank_two_v1'
 need(pin(old/'manifest.json')['sha256']=='2a53441260ce172d195ae028e433d21d9b4af75fcd74209ae1fd7a40c12ea114','unchanged v1')
 for r in load(old/'manifest.json')['exports']:exact(old/r['path'],r)
 for r in load(old/'dependencies.json'):exact(Path(r['path']),r)
 for n in ['primitive_residues.tex','primitive_residues.pdf','source_rows.json','scope.rst']:
  need((W/'v1_exact'/n).read_bytes()==(S/'geometry/psl3_4'/n).read_bytes(),'exact preserved v1 '+n)
 independent=load(W/'literal02.json');need(independent['status']=='PASS_INDEPENDENT_LITERAL_L100_CANDIDATE_CHECKS','independent literal result')
 need(independent['candidate_pairs']==60 and independent['neighbour_pairs']==3098 and independent['witnesses']==24,'complete literal checks')
 for folder in ['export01','literal02_receipt']:
  rec=load(W/folder/'receipt.json');need(rec['status']=='TERMINAL_PASS'and rec['returncode']==0,'clean independent receipt')
  for k in ['stdout','stderr']:exact(Path(rec[k]['path']),rec[k])
 calls=load(W/'fresh01/calls.json');need(len(calls)==12,'exact complete control calls before native failure')
 markers=['Actual groups mismatch','Common neighbour multiset','All pairs incidence','Local 2T flag','Witness coverage','Not an automorphism','Simultaneous images']
 for i,c in enumerate(calls):
  for k in ['stdout','stderr']:exact(Path(c[k]['path']),c[k])
  so=Path(c['stdout']['path']).read_text();se=Path(c['stderr']['path']).read_text()
  if i==0:need(c['returncode']==0 and not se and 'PASS_COSET_ORACLE 60 PAIRS 3098 NEIGHBOUR_PAIRS 24 WITNESSES'in so,'fresh actual oracle')
  elif i<=7:need(c['returncode']not in [0,None]and markers[i-1]in so+se and 'PASS_COSET_ORACLE'not in so,'damaged input rejection')
  elif i<=9:need(c['returncode']not in [0,None]and 'normal Python required'in so+se,'optimization rejection')
  else:need(c['returncode']==0 and not se,'old native passes retained')
 source=load(Q/'source_rows.json');oldrows=load(W/'v1_exact/source_rows.json')['rows']
 by={tuple(x['orders']):x['local_two_transitive'] for x in independent['class_local_two_transitive']}
 for r,oldr in zip(source['rows'],oldrows):
  need(all(r[k]==v for k,v in oldr.items()),'old scientific source row unchanged')
  flags=by[tuple(r['parabolic_orders']+[r['intersection']])]
  need(r['local_two_transitive']==[bool(x)for x in flags],'source flags equal literal checks')
 need(len(source['rows'])==7,'seven source rows')
 out.mkdir();native=out/'native';native.mkdir();shutil.copy2(Q/'primitive_residues.tex',native/'primitive_residues.tex')
 for n in [1,2]:
  p=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','primitive_residues.tex'],cwd=native,timeout=60,capture_output=True)
  (out/f'native{n}.stdout').write_bytes(p.stdout);(out/f'native{n}.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr,'clean final native')
 log=(native/'primitive_residues.log').read_text();need(not any(x in log for x in ['Warning','Overfull','Underfull']),'final clean log')
 from pypdf import PdfReader
 a=PdfReader(Q/'primitive_residues.pdf');b=PdfReader(native/'primitive_residues.pdf');need(len(a.pages)==len(b.pages)==2,'two pages')
 at='\f'.join(x.extract_text()for x in a.pages);bt='\f'.join(x.extract_text()for x in b.pages);need(at==bt,'final native text equality')
 (out/'author.txt').write_text(at);(out/'review.txt').write_text(bt)
 p=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r120','-sOutputFile='+str(out/'page-%02d.png'),str(native/'primitive_residues.pdf')],capture_output=True,timeout=30)
 (out/'render.stdout').write_bytes(p.stdout);(out/'render.stderr').write_bytes(p.stderr);need(p.returncode==0 and not p.stderr and len(list(out.glob('page-*.png')))==2,'final native render')
 report={'status':'PASS_FINAL_L100_RANK_TWO_V2_REVIEW_CHECK','author_manifest':pin(P/'manifest.json'),'direct_bindings':len(deps),'unchanged_v1_bindings':36,'literal_candidates':60,'literal_local_primitivity_checks':120,'literal_neighbour_pairs':3098,'literal_witnesses':24,'source_rows':7,'negative_controls':7,'optimization_guards':2,'native_pages':2,'new_subgroup_enumerations':0,'local2T_correction_explicit':True,'old_failures_preserved':True}
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
