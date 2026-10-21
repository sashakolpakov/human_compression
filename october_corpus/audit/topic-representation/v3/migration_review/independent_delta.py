#!/usr/bin/env python3
import argparse,hashlib,json,re
from pathlib import Path

def need(x,s):
 if not x:raise RuntimeError(s)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def environment(s,label):
 m=re.search(r'\\begin\{theorem\}(?:\[[^]]*\])?\\label\{'+re.escape(label)+r'\}.*?\\end\{theorem\}',s,re.S);need(m is not None,'theorem found '+label);return m[0]
def verify(old,new):
 for label in ['R.PairEncoding','R.FinitePairs']:need(environment(old['volume/sections/05-pair-encoding.tex'],label)==environment(new['volume/sections/05-finite-pair-application.tex'],label),'complete local statement '+label)
 a=old['volume/sections/05-pair-encoding.tex'];b=new['volume/sections/05-pair-encoding.tex']
 # Independent inverse of the seven literal routing edits, all read in context.
 pairs=[('$C(X),K(X)$ from Section~\\ref{sec:recognition}. Correlations permute color','$C(X),K(X)$ from the common paper~\\cite{Recognition}. Correlations permute color'),('UR.FinitePairs','R.FinitePairs'),('UR.PairEncoding','R.PairEncoding'),('of Theorem~\\ref{UR.Restriction}, applied first to the labeled ordered-pair structure.','of the common theorem, applied first to the labeled ordered-pair structure.'),('For $G\\ne1$, apply Theorem~\\ref{UR.Chambers} to','For $G\\ne1$, apply the common chamber-completion theorem to'),('Theorem~\\ref{UR.Conversion} supplies a separate conclusion: any nonempty','The common cleaning theorem supplies a separate conclusion: any nonempty')]
 for x,y in pairs:need(x in b,'inverse relocation literal');b=b.replace(x,y)
 need(a==b,'entire moved section preserved, not only statements')
 need('\\input{sections/05-pair-encoding.tex}' in new['volume/umbrella.tex'],'complete common includes encoder')
 need('\\input{sections/05-pair-encoding.tex}' not in new['volume/finite-normal-pairs.tex'],'local proof replaced by exact common reference')
 need('\\input{sections/05-finite-pair-application.tex}' in new['volume/finite-normal-pairs.tex'],'local bridge included')
 for name in ['01-recognition','02-chambers','03-cleaning','06-symmetric-family','07-hexagon','09-shadows','10-free-basis','11-chamber-splitting','22-conjugate-families','23-thin-example']:
  k='volume/sections/'+name+'.tex';need(old[k]==new[k],'unchanged proof '+name)
 for name in ['20-finite-examples','21-projective','23-source-scope']:
  s=new['volume/sections/'+name+'.tex'];need('UR.FinitePairs' in s,'actual shared citation '+name)
  need('proved in the first application' not in s and 'proved in the complete first' not in s,'no sibling proof premise')
 return True

def main():
 p=argparse.ArgumentParser();p.add_argument('--author',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh report');root=a.author
 need(digest(root/'manifest.json')=='0e3911279dc5aba060b0dca1e00108134567aec58f44eae9738ce80434a8322f','frozen successor')
 current=json.loads((root/'manifest.json').read_text());previous=json.loads((root/'previous/author_manifest.json').read_text());need(digest(root/'previous/author_manifest.json')=='04985353a54cf4f7050f143c518bdf5673dc43b422518dfb5825a520a36e9f65','frozen predecessor')
 for row in current['exports']:need(digest(root/row['path'])==row['sha256'],'current artifact '+row['path'])
 oldrows={r['path']:r for r in previous['exports']};old={}
 for f in (root/'previous/volume').rglob('*.tex'):
  k=str(f.relative_to(root/'previous'));need(digest(f)==oldrows[k]['sha256'],'old TeX '+k);old[k]=f.read_text()
 new={str(f.relative_to(root)):f.read_text() for f in (root/'volume').rglob('*.tex')};verify(old,new)
 # Every old complete code, graph input and scoped formal artifact must remain identical.
 reused=[]
 for path,row in oldrows.items():
  if path.startswith(('programs/','certificate/','formal/')):
   need(digest(root/path)==row['sha256'],'required/optional/formal bytes '+path);reused.append(path)
 need(digest(root/'source_contract.json')==oldrows['source_contract.json']['sha256'],'31 complete source rows')
 controls=[]
 for name,path,before,after in [('delete proof step','volume/sections/05-pair-encoding.tex','The degrees of old vertices','The unproved degrees of old vertices'),('lose normality','volume/sections/05-finite-pair-application.tex','$H\\mathrel{\\trianglelefteq}G$','$H\\leq G$'),('wrong rank','volume/sections/05-finite-pair-application.tex','$[G:H]+3$','$[G:H]+2$'),('remove common import','volume/umbrella.tex','\\input{sections/05-pair-encoding.tex}',''),('restore sibling','volume/sections/21-projective.tex','proved in common Theorem UR.FinitePairs','proved in the first application')]:
  trial=dict(new);need(before in trial[path],'effective control');trial[path]=trial[path].replace(before,after)
  try:verify(old,trial)
  except RuntimeError:controls.append(name)
  else:raise RuntimeError('mutation survived '+name)
 report={'status':'PASS','successor_exports':len(current['exports']),'previous_tex_files':len(old),'current_tex_files':len(new),'full_encoder_exact_modulo_six_routing_replacements':True,'two_local_statements_exact':True,'unchanged_program_certificate_formal_artifacts':reused,'all31_L126_rows_preserved':True,'controls_rejected':controls,'no_new_program_formal_replay':True}
 a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print('Independent migration checks PASS')
if __name__=='__main__':main()
