#!/usr/bin/env python3
"""Bounded independent migration and generic-criterion checks; no author imports."""
import argparse,collections,difflib,hashlib,itertools,json,math,re,subprocess
from pathlib import Path


def need(t,m):
    if not t:raise ValueError(m)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def rank(rows,p=3):
    a=[list(map(lambda x:x%p,r))for r in rows]
    if not a:return 0
    n=len(a[0]);k=0
    for j in range(n):
        i=next((i for i in range(k,len(a))if a[i][j]),None)
        if i is None:continue
        a[k],a[i]=a[i],a[k];inv=pow(a[k][j],-1,p)
        a[k]=[x*inv%p for x in a[k]]
        for i in range(len(a)):
            if i!=k and a[i][j]:
                c=a[i][j];a[i]=[(x-c*y)%p for x,y in zip(a[i],a[k])]
        k+=1
        if k==len(a):break
    return k


def mm(A,B):return tuple(tuple(sum(x*y for x,y in zip(r,c))%3 for c in zip(*B))for r in A)
def flat(A):return list(itertools.chain.from_iterable(A))
def algebra(gs):
    d=len(gs[0]);base=[tuple(tuple(int(i==j)for j in range(d))for i in range(d))];i=0
    while i<len(base):
        for g in gs:
            b=mm(base[i],g)
            if rank([flat(x)for x in base]+[flat(b)])>len(base):base.append(b)
        i+=1
    return base


def field(q):
    def add(a,b):return a^b if q==4 else(a+b)%q
    def mul(a,b):
        if q!=4:return a*b%q
        r=0
        while b:
            if b&1:r^=a
            b>>=1;a<<=1
            if a&4:a^=7
        return r
    def total(xs):
        x=0
        for y in xs:x=add(x,y)
        return x
    return mul,total


def mac(w,q,k):
    n=len(w)-1;out=[]
    for j in range(n+1):
        num=sum(c*sum((-1)**s*(q-1)**(j-s)*math.comb(i,s)*math.comb(n-i,j-s)
            for s in range(max(0,j-n+i),min(i,j)+1))for i,c in enumerate(w))
        need(num%q**k==0 and num>=0,'MacWilliams integer coefficient');out.append(num//q**k)
    return out


def math_checks():
    result=[]
    cases=[(2,[[1,0,1,1],[0,1,1,0]]),(3,[[1,0,1,1],[0,1,1,2]]),(4,[[1,2,3]]),(4,[[1,0,2],[0,1,3]])]
    for q,B in cases:
        mul,total=field(q);n=len(B[0]);k=len(B)
        words={tuple(total(mul(a,r[j])for a,r in zip(c,B))for j in range(n))for c in itertools.product(range(q),repeat=k)}
        need(len(words)==q**k,'independent literal basis')
        dual={v for v in itertools.product(range(q),repeat=n)if all(total(mul(x,y)for x,y in zip(v,r))==0 for r in B)}
        w=[sum(sum(x!=0 for x in v)==i for v in words)for i in range(n+1)]
        dw=[sum(sum(x!=0 for x in v)==i for v in dual)for i in range(n+1)]
        need(mac(w,q,k)==dw,'literal extension-field MacWilliams')
        result.append({'name':'MacWilliams direct enumeration','q':q,'n':n,'k':k,'words':len(words),'dual_words':len(dual)})
    U=((1,1),(0,1));L=((1,0),(1,1));D=((1,0),(0,2));P=((1,0),(0,0))
    need(len(algebra([U,L]))==4,'full algebra instance')
    need(len(algebra([U,D]))==3 and len(algebra([L,D]))==3,'one-sided rank-one countermodels')
    need(rank([list(mm(X,P)[0])+list(mm(X,P)[1])for X in algebra([U,D])])>=1,'rank-one present')
    cols=lambda bs:rank([list(zip(*mm(X,P)))[0]for X in bs])
    rows=lambda bs:rank([mm(P,X)[0]for X in bs])
    need((cols(algebra([U,D])),rows(algebra([U,D])))==(1,2),'missing column-span condition')
    need((cols(algebra([L,D])),rows(algebra([L,D])))==(2,1),'missing row-span condition')
    result.extend([{'name':'full algebra2x2','dimension':4},{'name':'omit column cyclicity','proper_algebra':3},{'name':'omit row cyclicity','proper_algebra':3}])
    need(len(algebra([D]))==2,'independence weakening');result.append({'name':'omit full algebra independence','proper_algebra':2})
    # C3 acts unipotently: its fixed line is the whole socle, while N=V is not semisimple.
    fixed=[v for v in itertools.product(range(3),repeat=2)if tuple(sum(v[i]*U[i][j]for i in range(2))%3 for j in range(2))==v]
    need(len(fixed)==3 and rank(fixed)==1,'nonsplit socle model')
    result.append({'name':'omit semisimplicity of N','socle_dimension':1,'N_dimension':2})
    eigenspaces=[]
    for eigenvalue in [1,2]:
        eigenspaces.append([v for v in itertools.product(range(3),repeat=2)
            if tuple(sum(v[i]*D[i][j]for i in range(2))%3 for j in range(2))==tuple(eigenvalue*x%3 for x in v)])
    need([rank(x)for x in eigenspaces]==[1,1] and rank(eigenspaces[0]+eigenspaces[1])==2,'omitted factor model')
    result.append({'name':'omit simple factor Hom spaces','C2_diagonal_factors':[1,2],'selected_factor_images_dimension':1,'socle_dimension':2})
    trivial_Hom=list(itertools.product(range(3),repeat=2))
    need(rank(trivial_Hom)==2 and rank([[1,0]])==1,'omitted basis-map model')
    result.append({'name':'omit basis-map completeness','trivial_group_dimension':2,'selected_Hom_image_dimension':1,'socle_dimension':2})
    # All permutations act on four singleton supports; the refinement bound is24 exactly.
    n=4;S=[{i}for i in range(n)];g=0
    for p in itertools.permutations(range(n)):
        if {frozenset(p[x]for x in s)for s in S}==set(map(frozenset,S)):g+=1
    need(g==math.factorial(n)==24,'refinement singleton example')
    result.append({'name':'refinement exact bound','bound':4*3*2,'actual':g})
    # Duplicated incidence vertices would add a kernel invisible on Omega.
    adj={(0,1),(1,0),(0,2),(2,0)}
    kernel=sum(p[0]==0 and {(p[x],p[y])for x,y in adj}==adj for p in itertools.permutations(range(3)))
    need(kernel==2,'duplicate-subset incidence kernel')
    result.append({'name':'omit distinct subsets','Omega_size':1,'duplicate_supports':2,'graph_automorphisms_fixing_Omega':kernel})
    allperms=list(itertools.permutations(range(3)));chosen=sum(p[0]==0 for p in allperms)
    need(len(allperms)==6 and chosen==2,'noninvariant support selection')
    result.append({'name':'omit complete invariant minimum supports','full_F3_3_Aut':len(allperms),'singleton_chosen_support_stabilizer':chosen})
    # Even binary length3: restricted representatives have first-two weight1, but S is not invariant.
    C=[(0,0,0),(1,1,0),(1,0,1),(0,1,1)];S={v for v in C if sum(v)==2 and sum(v[:2])<=1}
    need(len(S)==2 and (1,1,0)not in S and (1,0,1)in S,'minimum orbit-invariance countermodel')
    result.append({'name':'omit minimum-set invariance','restricted_minima':2,'all_minima':3})
    result.append({'name':'zero-dimensional matrix module','d':0,'independent_product_count':0,'simple':False})
    result.append({'name':'empty simplex','n':0,'V0_dimension':1,'boundary_image_dimension':0,'exact':False})
    return result


def normalized(text):return re.sub(r'\s+',' ',text).strip()


def blocks(text):
    pattern=r'\\begin\{(?:lemma|theorem|proposition|corollary)\}(?:\[[^\]]*\])?\\label\{([^}]+)\}'
    out={}
    for m in re.finditer(pattern,text):
        end=text.index(r'\end{proof}',m.end())+len(r'\end{proof}')
        out[m.group(1)]=text[m.start():end]
    return out


def braced(text,i):
    need(text[i]=='{','auxiliary group opening');depth=1;j=i+1
    while depth:
        if text[j]=='{':depth+=1
        elif text[j]=='}':depth-=1
        j+=1
    return text[i+1:j-1],j


def auxiliary_labels(text):
    result={}
    for match in re.finditer(r'\\newlabel\{ULCD\.',text):
        name,i=braced(text,match.start()+len('\\newlabel'))
        content,_=braced(text,i);value,_=braced(content,0)
        while value.startswith('{'):
            inner,end=braced(value,0)
            if end!=len(value):break
            value=inner
        result[name]=value
    return result


def migration_checks(packet,study):
    tex=(packet/'umbrella.tex').read_text();new=blocks(tex);records=[]
    for row in json.loads((packet/'migration.json').read_text())['inherited_fragments']:
        f=study/row['source'];need(sha(f)==row['sha256'],'prior source hash')
        raw=f.read_text();part=raw[raw.index(row['start']):raw.index(row['stop_excluded'])]
        for old,label in row['labels'].items():part=part.replace('{'+old+'}','{'+label+'}')
        part=part.replace('The complementary-projection theorem in the common paper yields',r'Theorem~\ref{ULCD.Complement} yields')
        part=part.replace(r'\tag{1}',r'\tag{2.1}\label{ULCD.ResidualIdentity}').replace('By (1)',r'By \eqref{ULCD.ResidualIdentity}').replace('since (1)',r'since \eqref{ULCD.ResidualIdentity}')
        part=part.replace('This invocation pays for that common theorem;\nit is not an independent derivation of it.','')
        part=part.replace('For any symmetric idempotent,\n$\\ker R=(\\im R)^\\perp$ and $V=\\im R\\oplus\\ker R$; indeed\n$x=Rx+(x-Rx)$ gives the decomposition, whose intersection is zero.\nThus both summands are LCD.',r'Lemma~\ref{ULCD.Projector} gives $\ker R=(\im R)^\perp$ and the orthogonal decomposition; both summands are LCD.')
        part=part.replace('The remaining claims in part~2 are the common projection theorem, applied',r'The remaining claims in part~2 follow from Theorem~\ref{ULCD.Complement}, applied')
        for label,oldblock in blocks(part).items():
            need(label in new,'missing inherited theorem '+label)
            need(normalized(oldblock)==normalized(new[label]),'changed inherited theorem/proof '+label)
            records.append({'label':label,'source':row['source'],'normalized_environment_sha256':hashlib.sha256(normalized(new[label]).encode()).hexdigest()})
    need(len(records)==19,'inherited environment count')
    need(len(new)==24,'complete theorem/proof environment count')
    labels=json.loads((packet/'interface_labels.json').read_text())
    need(labels['ULCD.ResidualIdentity']=='2.1','equation label parsing')
    need('d\\geq1' in new['ULCD.MatrixAlgebra'] or 'd>0' in new['ULCD.MatrixAlgebra'],'positive module dimension')
    need('an $n$-element set with $n>0$' in tex,'nonempty simplex assumption')
    for name,digest in json.loads((packet/'bindings.json').read_text())['inherited_acceptances'].items():
        need(sha(study/name/'manifest.json')==digest,'distinct prior acceptance '+name)
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--study-root',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=False)
    manifest=json.loads((a.packet/'manifest.json').read_text())
    for row in manifest['exports']:
        f=a.packet/row['path'];need(f.stat().st_size==row['bytes']and sha(f)==row['sha256'],'author export '+row['path'])
    records=migration_checks(a.packet,a.study_root)
    checks=math_checks()
    if a.render:
        for i in range(2):
            q=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory='+str(a.out),str((a.packet/'umbrella.tex').resolve())],cwd=a.out,text=True,capture_output=True)
            (a.out/f'compile{i}.log').write_text(q.stdout+q.stderr)
            need(q.returncode==0 and not any(x in q.stdout+q.stderr for x in ['Overfull','Missing character']),'new umbrella render')
        need('undefined references' not in q.stdout+q.stderr,'resolved final references')
        from pypdf import PdfReader
        old=PdfReader(a.packet/'umbrella.pdf');new=PdfReader(a.out/'umbrella.pdf')
        need(len(new.pages)==14 and [p.extract_text()for p in old.pages]==[p.extract_text()for p in new.pages],'all14 page texts')
        need(auxiliary_labels((a.out/'umbrella.aux').read_text())==json.loads((a.packet/'interface_labels.json').read_text()),'all29 fresh application interfaces')
    result={'status':'PASS','author_manifest_sha256':sha(a.packet/'manifest.json'),'inherited_environment_comparisons':records,'small_generic_models_and_controls':checks,'large_enumerations_repeated':False,'author_code_imported':False,'rendered':a.render}
    (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','inherited':len(records),'generic_checks':len(checks)}))

if __name__=='__main__':main()
