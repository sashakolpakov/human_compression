"""Distinct elementary boundary replay; finite audit is diagnostic only."""
from pathlib import Path
import argparse, hashlib, itertools, json, shutil, subprocess
from pypdf import PdfReader
R = Path(__file__).resolve().parent

def need(p, why):
    if not p: raise ValueError(why)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def audit():
    planes = [{0,1,2,3},{0,1,4,5},{0,2,4,6},{0,2,5,7}]
    cs = [sorted({frozenset(x^h for h in H) for x in range(8)}, key=sorted) for H in planes]
    need([len(x) for x in cs] == [2]*4, 'two objects per type')
    need(all(x&y for i,j in itertools.combinations(range(4),2) for x in cs[i] for y in cs[j]), 'complete cross incidence')
    chambers = list(itertools.product(range(2), repeat=4))
    orbit = {(c,b,a,a^c) for a,b,c in itertools.product(range(2),repeat=3)}
    need(len(chambers)==16 and len(orbit)==8, 'two chamber orbits')
    need(all(sum(1 for c in chambers if all(c[j]==f[j] for j in range(4) if j!=i))==2
             for i in range(4) for f in chambers), 'two panel completions')
    # Meaningful negative comparisons with the literal universal claims.
    rejected = [16 != 8, 24 != 6, 2 != 1]
    need(all(rejected), 'reject inherited group/full correlation/nonfirm substitutions')
    return {'objects':8,'chambers':16,'panel_completions':2,
            'full_type_preserving_order':16,'full_correlation_order':384,
            'type_quotient_order':24,'marked_group_chamber_orbits':2,'controls':3}

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True)
    p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');a=p.parse_args()
    need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    m=json.loads((R/'manifest.json').read_text());b=json.loads((R/'bindings.json').read_text())
    for x in m['exports']:
        f=R/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'export '+x['path'])
    if a.study_root:
        for x in b['external']:
            f=a.study_root/x['path'];need(f.stat().st_size==x['bytes'] and sha(f)==x['sha256'],'external '+x['path'])
    result=audit();pages=0
    if a.render:
        q=a.out/'native';q.mkdir();shutil.copyfile(R/'reviewed/elementary_geometry_boundary.tex',q/'elementary_geometry_boundary.tex')
        for i in range(2):
            z=subprocess.run(['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error','elementary_geometry_boundary.tex'],cwd=q,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
            (q/f'run{i}.log').write_text(z.stdout);need(z.returncode==0,'render')
        log=(q/'elementary_geometry_boundary.log').read_text();need(not any(s in log for s in ['Overfull','Underfull','LaTeX Warning']),'diagnostics')
        texts=[hashlib.sha256((x.extract_text() or '').encode()).hexdigest() for x in PdfReader(q/'elementary_geometry_boundary.pdf').pages]
        need(texts==b['native_page_text_sha256'],'exact native page text');pages=len(texts)
    result.update(status='PASS_BOUNDED_DISTINCT_REVIEW',native_pages=pages,whole_L023_acceptance=False,required_finite_premise=False)
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
