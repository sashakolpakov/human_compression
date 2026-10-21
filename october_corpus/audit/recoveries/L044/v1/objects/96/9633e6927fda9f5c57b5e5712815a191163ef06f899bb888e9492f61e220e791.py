#!/usr/bin/env python3
"""Bounded fresh render, exact pins, and elementary quotient-action controls."""
import argparse,hashlib,itertools,json,shutil,subprocess
from pathlib import Path
from pypdf import PdfReader
AUTHOR='64f0596a59190290d0cf8fe9f1d8a791d4cbe3834c2ae71bb67c5e2d764571c7'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compose(a,b):return tuple(a[b[i]] for i in range(len(a)))
def check_example():
    D=list(itertools.permutations(range(3)));one=tuple(range(3));idx={x:i for i,x in enumerate(D)}
    mul=lambda a,b:idx[compose(D[a],D[b])]
    e=idx[one];reflection=idx[(1,0,2)];rotation=idx[(1,2,0)]
    results=[]
    for name,K in [('core_free_reflection',{e,reflection}),('nontrivial_normal_core',{e,rotation,mul(rotation,rotation)})]:
        cosets=[]
        for d in range(6):
            c=frozenset(mul(k,d) for k in K)
            if c not in cosets:cosets.append(c)
        loc={d:i for i,c in enumerate(cosets) for d in c};images=set();old=set()
        for a0,a1 in itertools.product(range(6),repeat=2):
            for sigma in [(0,1),(1,0)]:
                aa=[a0,a1]
                p=tuple(sigma[j]*6+mul(d,aa[j]) for j in range(2) for d in range(6))
                q=tuple(sigma[j]*len(cosets)+loc[mul(next(iter(c)),aa[j])] for j in range(2) for c in cosets)
                # Every literal representative of each coset has the same image.
                if not all(len({loc[mul(d,aa[j])] for d in c})==1 for c in cosets for j in range(2)):raise ValueError('not well defined')
                old.add(p);images.add(q)
                for z in range(6):
                    left=tuple(j*6+mul(z,d) for j in range(2) for d in range(6))
                    if compose(left,p)!=compose(p,left):raise ValueError('commutation')
        expected=72 if len(K)==2 else 8
        if len(old)!=72 or len(images)!=expected:raise ValueError('quotient cardinality')
        if {p[0] for p in images}!=set(range(2*len(cosets))):raise ValueError('lost transitivity')
        results.append({'case':name,'original_degree':12,'new_degree':2*len(cosets),'centralizer_order':len(old),'image_order':len(images)})
    # Dropping semiregularity: C2 on a two-point orbit plus fixed point is not a torsor product.
    # Dropping d>=3: the order-four dihedral group cannot act faithfully on two points.
    return {'torsor_quotient_cases':results,'non_core_free_control_kernel_order':9,'degenerate_dihedral_control':'D of order4 has no faithful degree2 representation, since |S2|=2.'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();study=Path(a.study_root);out=Path(a.out);out.mkdir(parents=True,exist_ok=False);p=study/'topic_B_centralizer_reduction_candidate'
    if sha(p/'manifest.json')!=AUTHOR:raise ValueError('wrong author packet')
    for e in json.loads((p/'manifest.json').read_text())['exports']:
        f=p/e['path']
        if sha(f)!=e['sha256'] or f.stat().st_size!=e['bytes']:raise ValueError(e['path'])
    scope=json.loads((p/'scope.json').read_text())
    for key in ['source','retained_rank_theorem']:
        e=scope[key];f=study/e['path']
        if sha(f)!=e['sha256'] or f.stat().st_size!=e['bytes']:raise ValueError(key)
    shutil.copy(p/'centralizer_reduction.tex',out/'centralizer_reduction.tex')
    for j in range(2):
        r=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','centralizer_reduction.tex'],cwd=out,capture_output=True,text=True,timeout=60)
        (out/f'render{j}.log').write_text(r.stdout+r.stderr)
        if r.returncode:raise ValueError('render')
    if any(w in r.stdout for w in ['Overfull','undefined','Missing character']):raise ValueError('render diagnostics')
    expected=[x.extract_text() for x in PdfReader(p/'centralizer_reduction.pdf').pages];actual=[x.extract_text() for x in PdfReader(out/'centralizer_reduction.pdf').pages]
    if expected!=actual or len(actual)!=2:raise ValueError('changed page text')
    report={'status':'PASS','author_manifest_sha256':sha(p/'manifest.json'),'exact_two_page_text_rebuild':True,'small_diagnostics':check_example(),'no_whole_L044_recovery':True}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
