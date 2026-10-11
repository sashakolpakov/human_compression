#!/usr/bin/env python3
"""Replay L014 cyclotomic/abelian examples, negative controls, and limited Lean proofs."""
import argparse, hashlib, json, os, pathlib, re, subprocess, sys, time
ROOT=pathlib.Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError('PHASE236_REJECT '+msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--out',type=pathlib.Path,required=True)
    ap.add_argument('--gap',type=pathlib.Path,required=True)
    ap.add_argument('--lean',type=pathlib.Path,required=True)
    ap.add_argument('--packages',type=pathlib.Path,required=True)
    a=ap.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh raw output path')
    out=a.out.resolve();need(not out.exists(),'fresh resolved output path');out.mkdir(parents=True)
    def run(label,args,env=None,timeout=180):
        start=time.monotonic()
        r=subprocess.run([str(x) for x in args],cwd=out,env=env,text=True,capture_output=True,timeout=timeout)
        stdout=out/(label+'.stdout');stderr=out/(label+'.stderr')
        stdout.write_text(r.stdout);stderr.write_text(r.stderr)
        return r,dict(label=label,returncode=r.returncode,seconds=round(time.monotonic()-start,4),
            stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    models=out/'models.g'
    r,mgen=run('models',[sys.executable,'-B','-O',ROOT/'phase236_models.py','--out',models])
    need(r.returncode==0 and models.is_file(),'mixed-modulus model generation')
    parameters=json.loads(r.stdout)
    need([(x['p'],x['m']) for x in parameters]==[(3,3),(3,4),(3,6),(5,3),(5,5),(7,3),(11,3)],'fixed example coverage')
    checker=(ROOT/'phase236_finite_check.g').read_text()
    program=out/'finite.g';program.write_text(models.read_text()+checker)
    r,finite=run('finite',[a.gap,'-q','-T',program])
    need(r.returncode==0 and 'PHASE236_FINITE_PASS' in r.stdout and not re.search(r'Error|warning',r.stdout+r.stderr),'finite replay')
    need(len(re.findall(r'^CYCLOTOMIC ',r.stdout,re.M))==7,'seven cyclotomic models')
    need(len(re.findall(r'^ABELIAN ',r.stdout,re.M))==4,'four abelian models')
    rr,c1=run('control_cyclotomic',[sys.executable,'-B','-O',ROOT/'phase236_models.py','--out',out/'bad_models.g','--corrupt-cyclotomic'])
    need(rr.returncode!=0 and 'PHASE236_REJECT cyclotomic' in rr.stderr,'cyclotomic constant-coefficient rejection')
    changed=checker.replace('r1:=x*y*r2;','r1:=x*y*r0;')
    need(changed!=checker,'literal-marking mutation applied')
    altered=out/'control_literal_marking.g';altered.write_text(models.read_text()+changed)
    rr,c2=run('control_literal_marking',[a.gap,'-q','-T',altered])
    need('PHASE236_FINITE_PASS' not in rr.stdout and 'abelian marked involutions' in rr.stdout+rr.stderr,'literal source marking rejection')
    changed=checker.replace('List(ss,Order)=row.moduli','List(ss,Order)=List(row.moduli,q->Maximum(1,q/p))')
    need(changed!=checker,'source-order mutation applied')
    altered=out/'control_source_orders.g';altered.write_text(models.read_text()+changed)
    rr,c3=run('control_source_orders',[a.gap,'-q','-T',altered])
    need('PHASE236_FINITE_PASS' not in rr.stdout and 'every source generator order' in rr.stdout+rr.stderr,'source generator-order rejection')
    pins=json.loads((ROOT/'formal/dependency_manifest.json').read_text());deps=[]
    for item in pins['packages']:
        p=a.packages/item['name']
        rev=subprocess.check_output(['git','-C',p,'rev-parse','HEAD'],text=True).strip()
        need(rev==item['rev'],'dependency revision '+item['name'])
        need(subprocess.run(['git','-C',p,'diff','--quiet','HEAD','--']).returncode==0,'clean dependency '+item['name'])
        deps.append(dict(name=item['name'],revision=rev))
    version=subprocess.check_output([a.lean,'--version'],text=True).strip()
    need('version 4.32.2,' in version,'Lean version')
    formal=ROOT/'phase236_formal/OddKernelIntersection.lean';formaltext=formal.read_text()
    need(not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\s',formaltext,re.M),'proof-hole scan')
    copy=out/formal.name;copy.write_text(formaltext)
    env=dict(os.environ);env['LEAN_PATH']=os.pathsep.join(str(p/'.lake/build/lib/lean') for p in a.packages.iterdir() if (p/'.lake/build/lib/lean').is_dir())
    rr,lean=run('formal',[a.lean,'-o',out/'OddKernelIntersection.olean',copy],env)
    need(rr.returncode==0 and not re.search(r'error:|warning:|sorryAx',rr.stdout+rr.stderr),'formal compilation')
    axioms=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",rr.stdout)
    need(len(axioms)==5,'five formal declarations')
    need(all(set(re.findall(r'[\w.]+',x))<={'propext','Classical.choice','Quot.sound'} for _,x in axioms),'formal axiom boundary')
    inputs=[ROOT/'phase236_models.py',ROOT/'phase236_finite_check.g',formal,ROOT/'formal/dependency_manifest.json']
    report=dict(status='PASS',scope='L014 principal written contract with corrected literal marking; partial formal verification.',
        model_generation=mgen,finite=finite,negative_controls=[c1,c2,c3],formal=lean,
        cyclotomic_parameters=parameters,abelian_parameters=[[3,1,1],[3,1,2],[3,2,2],[5,1,2]],
        intersection_equalities_per_model=64,axiom_reports=axioms,dependencies=deps,lean_version=version,
        generated_model_sha256=sha(models),generated_program_sha256=sha(program),
        inputs={str(p.relative_to(ROOT)):sha(p) for p in inputs},
        limitations=['Finite examples do not establish the arbitrary-prime construction; its proof is written.',
          'Lean verifies the prime-index intersection step and reflection identities only.',
          'Cunningham–Pellicer Theorem1.1 is retained in the tightness converse.',
          'The literal erroneous v1 marking is corrected, not claimed as recovered.',
          'No open conjecture or numerical compression rate is claimed.'])
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',cyclotomic_examples=7,abelian_examples=4,
        semantic_negative_controls=3,lean_declarations=5,report=str(out/'report.json'))))

if __name__=='__main__':main()
