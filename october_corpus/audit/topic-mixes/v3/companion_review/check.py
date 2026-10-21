#!/usr/bin/env python3
"""Independent optional finite models for the written F007 repair; no root imports."""
import argparse, hashlib, json, subprocess, tempfile
from collections import deque
from pathlib import Path

def require(test, message):
    if not test: raise RuntimeError(message)
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def components(r, colors):
    left=set(range(len(r[0]))); out=[]
    while left:
        seed=min(left); found={seed}; todo=[seed]
        while todo:
            x=todo.pop()
            for c in colors:
                y=r[c][x]
                if y not in found: found.add(y); todo.append(y)
        left-=found; out.append(sorted(found))
    return out

def properties(r):
    n=len(r[0]); simple=all(len({x,*[s[x] for s in r]})==4 for x in range(n))
    invol=all(s[s[x]]==x for s in r for x in range(n))
    commute=all(r[0][r[2][x]]==r[2][r[0][x]] for x in range(n))
    connected=len(components(r,range(3)))==1
    return dict(simple=simple,involutions=invol,distant_commutation=commute,connected=connected)

def automorphisms(r):
    n=len(r[0]); autos=[]
    for image in range(n):
        f={0:image}; q=deque([0]); good=True
        while q and good:
            x=q.popleft()
            for s in r:
                y=s[x]; z=s[f[x]]
                if y in f:
                    if f[y]!=z: good=False; break
                else: f[y]=z; q.append(y)
        if good and len(f)==n and len(set(f.values()))==n: autos.append([f[i] for i in range(n)])
    return autos

def model(p, extra, c_kind, version):
    elems=[(j,e,z) for j in range(p) for e in range(2) for z in range(1+extra)]
    def mul(x,y): return ((x[0]+(-1 if x[1] else 1)*y[0])%p,x[1]^y[1],x[2]^y[2])
    a=(0,1,0); b=(p-1,1,0); h=(p//2,0,0)
    c={'h':h,'ha':mul(h,a),'external':(0,0,1)}[c_kind]
    d={'P':h,'T':mul(h,b),'printedT':mul(h,a)}[version]
    flags=[(g,i) for g in elems for i in range(2)]; index={x:i for i,x in enumerate(flags)}
    r=[[],[],[]]
    for g,i in flags:
        r[0].append(index[mul(g,b if i else a),i]); r[1].append(index[g,1-i]); r[2].append(index[mul(g,d if i else c),i])
    return r,elems,(a,b,c,d)

def finite_checks():
    rows=[]
    for p in (2,4,6,8,10):
        for ck in ('h','ha','external'):
            if p==2 and ck=='ha': continue
            extra=int(ck=='external')
            for version in ('P','T','printedT'):
                r,H,marks=model(p,extra,ck,version); props=properties(r)
                if version=='printedT':
                    require(not all(props.values()),'Printed formula unexpectedly valid')
                    require((not props['simple']) if p==2 else (not props['distant_commutation']),'Wrong literal failure mechanism')
                    row=dict(p=p,base=ck,version=version,flags=len(r[0]),properties=props)
                else:
                    require(all(props.values()),'Corrected construction invalid')
                    autos=automorphisms(r); expected=len(H)*(2 if ((version=='P' and ck=='h') or (version=='T' and ck=='ha')) else 1)
                    require(len(autos)==expected,'Automorphism exception mismatch')
                    faces=[components(r,[c for c in range(3) if c!=i]) for i in range(3)]
                    ids=[{v:j for j,F in enumerate(f) for v in F} for f in faces]
                    for x in range(1,len(r[0]),2): require(all(z[x]==z[r[2][x]] for z in ids),'White pair not chain-equivalent')
                    row=dict(p=p,base=ck,version=version,flags=len(r[0]),automorphisms=len(autos),predicted=expected,properties=props)
                rows.append(row)
    # Independent V4 coordinate model, with elements as ordered bits.
    elements=[(i,j) for i in range(2) for j in range(2)]
    flags=[(x,i) for x in elements for i in range(2)]; ix={x:i for i,x in enumerate(flags)}
    x=(1,0);y=(0,1);xy=(1,1)
    def add(a,b): return tuple(i^j for i,j in zip(a,b))
    def four(a,b,c,d):
        return [[ix[add(g,b if i else a),i] for g,i in flags], [ix[g,1-i] for g,i in flags], [ix[add(g,d if i else c),i] for g,i in flags]]
    r=four(x,y,y,xy); require(all(properties(r).values()),'Eight-flag graph invalid')
    aut=automorphisms(r); require(len(aut)==4,'Eight-flag group not V4')
    f=[components(r,[c for c in range(3) if c!=i]) for i in range(3)]
    require(list(map(len,f))==[1,2,1],'Face counts')
    word=lambda q:r[1][r[0][r[1][q]]]
    require(all((word(q)==r[2][q])==(q%2==0) for q in range(8)),'Layer distinguishing word')
    rp=four(y,x,xy,y); switch=[q^1 for q in range(8)]
    require(all(switch[r[c][q]]==rp[c][switch[q]] for c in range(3) for q in range(8)),'Layer-swap isomorphism')
    require(len(automorphisms(four(x,y,y,x)))==8,'Excluded duplicate case not regular')
    # Meaningful wrong-assumption controls: the fixed validators must reject them.
    controls=[]
    def reject(name,fn):
        try: fn()
        except RuntimeError: controls.append(name); return
        raise RuntimeError('Control accepted: '+name)
    for p in (2,4):
        bad,_,_=model(p,0,'h','printedT')
        reject('printed torus p='+str(p),lambda bad=bad:require(all(properties(bad).values()),'not a maniplex'))
    bad=four(x,y,y,y)
    reject('equal white marks',lambda:require(all(properties(bad).values()),'not simple'))
    reject('eight-flag example regular',lambda:require(len(aut)==8,'wrong symmetry type'))
    regular,_,_=model(4,0,'h','P')
    reject('omit projective regular exception',lambda:require(len(automorphisms(regular))==8,'wrong symmetry order'))
    reject('unexchanged degenerate base is simple',lambda:require(len({x,y,y})==3,'repeated base marks'))
    return dict(status='PASS',construction_cases=len(rows),rows=rows,eight_flag=dict(flags=8,automorphisms=4,face_counts=[1,2,1],chain_class_sizes=[4,4],layer_swap_isomorphism=True),rejected_controls=controls,scope='Optional finite diagnostics; the all-group and infinite statements are proved in rank_three.tex, not inferred from these cases.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--source',type=Path);args=p.parse_args()
    root=Path(__file__).resolve().parent; args.out.mkdir(parents=True,exist_ok=True)
    if (root/'manifest.json').exists():
        m=json.loads((root/'manifest.json').read_text())
        for x in m['exports']: require(digest(root/x['path'])==x['sha256'],'changed '+x['path'])
    if args.source: require(digest(args.source)=='b6d437c2a53357d98c2d8b446795c410f9dfc27f7421226183914cb8d5be82c1','Wrong source edition')
    result=finite_checks()
    if args.render:
        from pypdf import PdfReader
        with tempfile.TemporaryDirectory(prefix='f007-rank-three-') as tmp:
            d=Path(tmp);(d/'rank_three.tex').write_bytes((root/'rank_three.tex').read_bytes())
            for i in range(2):
                q=subprocess.run(['/opt/homebrew/bin/xelatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','rank_three.tex'],cwd=d,capture_output=True,text=True)
                require(q.returncode==0,'XeLaTeX failure '+q.stdout[-2000:])
            log=(d/'rank_three.log').read_text();require(not any(s in log for s in ('Overfull','Missing character','LaTeX Warning')),'Render diagnostics')
            old=PdfReader(root/'rank_three.pdf');new=PdfReader(d/'rank_three.pdf')
            require([x.extract_text() for x in old.pages]==[x.extract_text() for x in new.pages],'Rendered page text changed')
            result['render']={'pages':len(new.pages),'exact_page_text':True,'diagnostics':[]}
    (args.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
