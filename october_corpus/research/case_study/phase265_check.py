#!/usr/bin/env python3
"""Replay the L009 principal application; the separately frozen clone result is excluded."""
import argparse,hashlib,json,os,pathlib,re,subprocess,sys,time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
 if not ok:raise RuntimeError('PHASE265_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bound(row):
 p=pathlib.PurePosixPath(row['path']);need(not p.is_absolute() and '..' not in p.parts,'relative binding')
 f=ROOT/p;need(f.is_file() and f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],'binding '+str(p))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--out',type=pathlib.Path,required=True);ap.add_argument('--gap',type=pathlib.Path,required=True)
 ap.add_argument('--lean',type=pathlib.Path,required=True);ap.add_argument('--packages',type=pathlib.Path,required=True)
 ap.add_argument('--verify-primary',action='store_true');a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output');out=a.out.resolve();need(not out.exists(),'fresh resolved output');out.mkdir(parents=True)
 manifest=json.loads((ROOT/'phase265_manifest.json').read_bytes())
 for row in manifest['exports']:bound(row)
 checked=0
 for row in manifest['retained_bindings']:
  if a.verify_primary or not row['path'].startswith('sources/'):bound(row);checked+=1
 ledger=json.loads((ROOT/'phase265_source_ledger.json').read_bytes())
 need(len(ledger['rows'])==44 and len(ledger['proof_spans'])==13,'complete ledger cardinalities')
 for key,row in ledger['proof_spans'].items():
  data=b''.join((ROOT/row['path']).read_bytes().splitlines(keepends=True)[row['start_line']-1:row['end_line']])
  need(len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256'],'proof span '+key)
 need(all(all(x in ledger['proof_spans'] for x in row['proof_spans']) for row in ledger['rows']),'source ledger pointers')
 need(set(ledger['principal_clauses'])=={'L009.1.1','L009.1.2'},'principal scope')
 reports=[]
 def run(label,cmd,env=None,timeout=180):
  start=time.monotonic();p=subprocess.run([str(x) for x in cmd],cwd=out,env=env,text=True,capture_output=True,timeout=timeout)
  stdout=out/(label+'.stdout');stderr=out/(label+'.stderr');stdout.write_text(p.stdout);stderr.write_text(p.stderr)
  reports.append(dict(label=label,returncode=p.returncode,seconds=round(time.monotonic()-start,4),stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
  return p
 def gaprun(label,path,markers):
  p=run(label,[a.gap,'-q','-T',path]);flat=p.stdout.replace('\\\n','');need(p.returncode==0 and not re.search('Error|warning',p.stdout+p.stderr,re.I),label+' clean exit')
  need(all(marker in flat for marker in markers),label+' expected assertions');return p
 versiongap=run('gap_version',[a.gap,'-q','-T','-c','Print(GAPInfo.Version,\"\\n\");QUIT;'])
 need(versiongap.returncode==0 and versiongap.stdout.strip()=='4.15.1','GAP version')
 frame=gaprun('frames',ROOT/'phase265_frame_control.g',['PHASE265_FRAME_CONTROL_PASS','H5760 G466560 lines90','PHASE265_NO_SL_CONTROL_PASS'])
 exceptional=gaprun('exceptional',ROOT/'phase265_exceptional.g',['PHASE265_A7_PASS','PHASE265_UH2_PASS','PHASE265_CONTROLS_PASS'])
 residue=gaprun('unital4',ROOT/'phase265_residues.g',['PHASE265_UH4_PASS','no_duality'])
 planes=gaprun('planes',ROOT/'phase265_plane_models.g',['PHASE265_ALL_NINE_MODELS_PASS'])
 need(planes.stdout.count('PHASE265_PLANE_PASS')==9,'all nine complete finite models')
 # Three independently enforced changes to live mathematical assertions/relations.
 mutations=[('false_GL','phase265_frame_control.g','Need(not IsSubgroup(H,GLP),','Need(IsSubgroup(H,GLP),','literal GL containment fails'),
  ('altered_incidence','phase265_residues.g','if left[i] in right[j][2] then','if (left[i] in right[j][2]) <> (i=1 and j=1) then','four-regular residue'),
  ('wrong_signature','phase265_plane_models.g','Need(cs=(r-2)*(k-1),','Need(cs=(r-1)*(k-1),','same-point signature')]
 for label,name,old,new,expected in mutations:
  text=(ROOT/name).read_text();need(text.count(old)==1,label+' unique mutation');path=out/(label+'.g');path.write_text(text.replace(old,new))
  p=run(label,[a.gap,'-q','-T',path]);need('Error' in p.stdout+p.stderr and expected in p.stdout+p.stderr,label+' rejected')
 pins=json.loads((ROOT/'formal/dependency_manifest.json').read_bytes());deps=[]
 for row in pins['packages']:
  path=a.packages/row['name'];rev=subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()
  need(rev==row['rev'],'dependency revision '+row['name'])
  need(subprocess.run(['git','-C',path,'diff','--quiet','HEAD','--']).returncode==0,'clean dependency '+row['name']);deps.append(dict(name=row['name'],rev=rev))
 version=subprocess.check_output([a.lean,'--version'],text=True).strip();need('version 4.32.2,' in version,'Lean version')
 source=ROOT/'phase265_formal/DeterminantFibers.lean';text=source.read_text()
 need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',text,re.M),'formal proof-hole scan')
 env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
 target=out/'DeterminantFibers.lean';target.write_text(text)
 p=run('formal',[a.lean,'-o',out/'DeterminantFibers.olean',target],env)
 need(p.returncode==0 and not re.search(r'error:|warning:|sorryAx',p.stdout+p.stderr),'formal compilation')
 axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",p.stdout)
 need(len(axioms)==4 and all(set(re.findall(r'[\w.]+',v))<={'propext','Classical.choice','Quot.sound'} for _,v in axioms),'four standard-only reports')
 old='C.det = 1 ∧ A * C = B';need(text.count(old)==1,'formal mutation location');bad=out/'FalseDeterminant.lean';bad.write_text(text.replace(old,'C.det = 0 ∧ A * C = B'))
 p=run('false_determinant',[a.lean,bad],env);need(p.returncode!=0 and 'error:' in p.stdout+p.stderr,'false determinant target rejected')
 report=dict(status='PASS',scope='Complete corrected L009 principal contract is a written-proof claim subject to independent review; execution alone is not admission.',
  exports_checked=len(manifest['exports']),retained_bindings_checked=checked,primary_checked=a.verify_primary,source_rows=len(ledger['rows']),proof_spans=len(ledger['proof_spans']),
  lean_version=version,gap_version=versiongap.stdout.strip(),dependencies=deps,axiom_reports=axioms,executions=reports,
  models=dict(affine9=dict(frame_group=5760,affine_group=466560,lines=90,GL_contained=False),A7=dict(noncollinear_orbit=2520,nonzero_pair_orbit=210),unital2='explicit complete design isomorphism',
    unital4=dict(points=65,blocks=208,residue_vertices=120,residue_edges=240,degree=4,girth=8,diameter=6,profiles=[[1,4,12,36,44,20,3],[1,4,12,36,42,20,5]],duality=False),plane_models=9),
  controls=['false GL-containment assertion rejected','changed literal unital incidence rejected','wrong common-neighbor formula rejected','false Lean determinant conclusion rejected',
    'determinant transitivity without contained SL has four rather than48 frames','Frobenius preserves affine lines but is not affine linear','one-way incidence morphism loses triangle edges'],
  limits=['BDL2003 classification and classical full automorphism identifications retained.','All-parameter residue proof is written, with accepted norm-shell input retained.',
    'Lean verifies matrix-fiber and orbit interfaces, not the complete source classifications.','No source/question/ratio credit from author execution.','Separate cloning packet excluded.'])
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',source_rows=len(ledger['rows']),lean_declarations=4,report=str(out/'report.json'))))
if __name__=='__main__':main()
