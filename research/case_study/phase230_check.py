#!/usr/bin/env python3
"""Replay the two finite principal classifications and the abstract Lean interface."""
import argparse, hashlib, json, os, pathlib, re, shutil, subprocess, time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok: raise RuntimeError('PHASE230_REJECT '+msg)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--gap',type=pathlib.Path,required=True)
    ap.add_argument('--lean',type=pathlib.Path,required=True)
    ap.add_argument('--packages',type=pathlib.Path,required=True)
    a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output path')
    out=a.out.resolve(); need(not out.exists(),'fresh resolved output path');out.mkdir(parents=True)
    def run(label,args,env=None,timeout=180):
        start=time.monotonic()
        r=subprocess.run([str(x) for x in args],text=True,capture_output=True,timeout=timeout,env=env,cwd=out)
        (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
        return r,dict(label=label,returncode=r.returncode,seconds=round(time.monotonic()-start,4),
                      stdout_sha256=sha(out/(label+'.stdout')),stderr_sha256=sha(out/(label+'.stderr')))
    src=ROOT/'phase230_finite_check.g'; text=src.read_text()
    copied=out/src.name;copied.write_text(text)
    r,finite=run('finite',[a.gap,'-q','-T',copied])
    need(r.returncode==0 and 'PHASE230_FINITE_PASS' in r.stdout and 'Error,' not in r.stderr+r.stdout,'finite replay')
    need(len(re.findall(r'^ROW \d+ ORDER',r.stdout,re.M))==10,'all ten amalgams')
    need(len(re.findall(r'^RANK3 ',r.stdout,re.M))==2,'both local group censuses')
    # A wrong facet Petrie relation must fail the exact universal order.
    altered=text.replace('U:=F/rel;', 'if n=8 then Add(rel,x[1]*x[2]*x[3]); fi; U:=F/rel;')
    need(altered!=text,'relator mutation was applied')
    p=out/'control_wrong_petrie.g';p.write_text(altered)
    rr,c1=run('control_wrong_petrie',[a.gap,'-q','-T',p])
    need('PHASE230_FINITE_PASS' not in rr.stdout and 'fp universal order' in rr.stderr+rr.stdout,'Petrie control rejection')
    # Keep the correctly computed group, but destroy the marking independence.
    altered=text.replace('good:=ForAll(rr', 'if n=10 then rr[4]:=rr[1]; fi; good:=ForAll(rr')
    need(altered!=text,'marking mutation was applied')
    p=out/'control_dependent_marking.g';p.write_text(altered)
    rr,c2=run('control_dependent_marking',[a.gap,'-q','-T',p])
    need('PHASE230_FINITE_PASS' not in rr.stdout and 'rank-four intersection property' in rr.stderr+rr.stdout,'marking control rejection')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text());checked=[]
    for item in pins['packages']:
        p=a.packages/item['name']
        rev=subprocess.check_output(['git','-C',p,'rev-parse','HEAD'],text=True).strip()
        need(rev==item['rev'],'dependency revision '+item['name'])
        need(subprocess.run(['git','-C',p,'diff','--quiet','HEAD','--']).returncode==0,'clean source '+item['name'])
        checked.append(dict(name=item['name'],revision=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip()
    need('version 4.32.2,' in version,'Lean version')
    source=ROOT/'phase230_formal/DihedralFacetObstruction.lean';formaltext=source.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',formaltext,re.M),'formal proof hole')
    copy=out/source.name;copy.write_text(formaltext)
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    rr,formal=run('formal',[a.lean,'-o',out/'DihedralFacetObstruction.olean',copy],env)
    need(rr.returncode==0 and not re.search(r'error:|warning:|sorryAx',rr.stdout+rr.stderr),'formal compilation')
    axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",rr.stdout)
    need(len(axioms)==5,'five formal interface reports')
    need(all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in axioms),'formal axiom boundary')
    report=dict(status='PASS',scope='Two principal classification contracts; partial Lean verification.',
      finite=finite,negative_controls=[c1,c2],formal=formal,axiom_reports=axioms,
      dependencies=checked,lean_version=version,
      inputs={str(p.relative_to(ROOT)):sha(p) for p in [src,source,ROOT/'formal/dependency_manifest.json']},
      limitations=['Dickson subgroup types and classical structural facts are retained inputs.',
                  'GAP finite-presentation algorithms are trusted for exact universal orders.',
                  'Lean verifies the abstract facet-normalizer obstruction, not the matrix or census applications.',
                  'L079 PΣL2(25) seventeen-case census and Conjecture11 are outside this contract.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',universal_presentations=10,local_marking_classes=6,
                         semantic_negative_controls=2,lean_declarations=5,report=str(out/'report.json'))))
if __name__=='__main__':main()
