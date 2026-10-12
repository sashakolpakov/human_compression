#!/usr/bin/env python3
"""Exact bounded certificate; complete prior word enumeration is retained, not rerun."""
from pathlib import Path
import argparse,collections,copy,hashlib,importlib.util,json,math,subprocess,time
HERE=Path(__file__).resolve().parent

def need(x,message):
    if not x: raise ValueError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def basis_file(path):
    lines=path.read_text().splitlines();n,k=map(int,lines[0].split());rows=[list(map(int,r)) for r in lines[1:]]
    need(n==120 and len(rows)==k and all(len(r)==n and set(r)<={0,1,2}for r in rows),'basis format')
    return rows

def rref(rows):
    a=[list(r)for r in rows];i=0
    for j in range(len(a[0])):
        h=next((h for h in range(i,len(a))if a[h][j]%3),None)
        if h is None:continue
        a[i],a[h]=a[h],a[i];a[i]=[(x*pow(a[i][j],-1,3))%3 for x in a[i]]
        for h in range(len(a)):
            if h!=i and a[h][j]:
                c=a[h][j];a[h]=[(x-c*y)%3 for x,y in zip(a[h],a[i])]
        i+=1
        if i==len(a):break
    return a[:i]
def member(x,basis):
    y=list(x)
    for r in basis:
        j=next(i for i,v in enumerate(r)if v);c=y[j]
        y=[(a-c*b)%3 for a,b in zip(y,r)]
    return not any(y)
def word_action(x,g):
    out=[0]*len(x)
    for i,v in enumerate(x):out[g[i]]=v
    return tuple(out)
def orbit(seed,gens,limit):
    seen={tuple(seed)};todo=collections.deque(seen)
    while todo:
        x=todo.popleft()
        for g in gens:
            y=word_action(x,g)
            if y not in seen:
                seen.add(y);need(len(seen)<=limit,'orbit exceeds retained total');todo.append(y)
    return seen

def refine(adj,colors):
    # Partition refinement, with the original color retained in every signature.
    while True:
        sig=[(colors[v],tuple(sorted(collections.Counter(colors[w]for w in adj[v]).items())))for v in range(len(adj))]
        labels={x:i for i,x in enumerate(sorted(set(sig)))};new=[labels[x]for x in sig]
        if len(set(new))==len(set(colors)):return new
        colors=new

def upper_bound(A,expected):
    adj=[[j for j,v in enumerate(r)if v]for r in A];colors=[0]*len(A);chain=[]
    while True:
        colors=refine(adj,colors);cells=collections.defaultdict(list)
        for v,c in enumerate(colors):cells[c].append(v)
        choices=[s for s in cells.values()if len(s)>1]
        if not choices:break
        cell=min(choices,key=lambda s:(len(s),s));chain.append([cell[0],len(cell)]);colors[cell[0]]=max(colors)+1
    need(chain==expected,'actual graph refinement chain');need(len(set(colors))==120,'discrete final partition')
    return math.prod(n for _,n in chain)
def group_order(gens,upper):
    identity=bytes(range(120));seen={identity};todo=collections.deque([identity]);tables=[bytes(g)+bytes(range(120,256))for g in gens]
    while todo:
        p=todo.popleft()
        for table in tables:
            q=p.translate(table)
            if q not in seen:
                seen.add(q);need(len(seen)<=upper,'group exceeds refinement upper bound');todo.append(q)
    need(len(seen)==upper,'generated group falls short of full upper bound');return len(seen)
def graph_action(A,gens):
    for g in gens:
        need(len(g)==120 and set(g)==set(range(120)),'literal generator permutation')
        need(all(A[g[i]][g[j]]==A[i][j]for i in range(120)for j in range(120)),'literal graph action')
def seed_check(seed,S):
    need(len(seed)==120 and set(seed)<={0,1,2}and sum(x!=0 for x in seed)==30,'seed weight/field')
    need(member(seed,S),'seed lies in actual difference code')
def supports_check(A,words,d):
    supports=sorted({tuple(i for i,v in enumerate(w)if v)for w in words})
    need(len(words)==d['minimum_words']and len(supports)==d['minimum_supports'],'minimum orbit/support cardinalities')
    need(all(sum(x!=0 for x in w)==30 for w in words),'minimum orbit weights')
    need(all(tuple(-v%3 for v in w)in words for w in words),'opposite minimum words')
    incidence=[[int(i in s)for s in supports]for i in range(120)]
    need(all(sum(r)==d['support_gram_diagonal']for r in incidence),'diagonal support incidence')
    counts=collections.defaultdict(collections.Counter)
    for i in range(120):
        for j in range(i):
            t=sum(x*y for x,y in zip(incidence[i],incidence[j]));counts[str(A[i][j])][str(t)]+=1
            need(A[i][j]==int(t!=4),'canonical graph recovery from actual minimum supports')
    need({k:dict(v)for k,v in counts.items()}==d['support_gram_pair_counts'],'complete pair-incidence table')
    return supports,{k:dict(v)for k,v in counts.items()}
def retained_count(row,k):
    need(row['length']==120 and row['basis_rows']==k and row['coefficient_vectors']==3**k,'whole retained enumeration range')
    wc=row['weight_counts'];need(len(wc)==121 and sum(wc)==3**k and wc[0]==1 and all(x==0 for x in wc[1:30])and wc[30]==112,'retained complete minimum count')

def inspect(d,A,gens,C,S,counts):
    need(len(C)==21 and len(S)==20,'actual code dimensions')
    need(rref(A)==C,'C is actual adjacency row code')
    need(rref([[(x-y)%3 for x,y in zip(r,A[0])]for r in A[1:]])==S,'S is actual difference row code')
    for k,row in counts.items():retained_count(row,k)
    graph_action(A,gens)
    for g in gens:
        need(all(member(word_action(r,g),C)for r in C),'C action')
        need(all(member(word_action(r,g),S)for r in S),'S action')
    # Direct finite checks of the displayed projector identities, independent of minimum counts.
    J=[[1]*120 for _ in range(120)];E=[[(1-x)%3 for x in r]for r in A]
    need(rref(E)==C,'projector image equals C')
    need(all(E[i][j]==E[j][i]for i in range(120)for j in range(120)),'projector symmetric')
    need(all(sum(E[i][h]*E[h][j]for h in range(120))%3==E[i][j]for i in range(120)for j in range(120)),'projector idempotent')
    seed_check(d['seed'],S);words=orbit(d['seed'],gens,d['minimum_words']);supports,pairs=supports_check(A,words,d)
    bound=upper_bound(A,d['graph_refinement_chain']);need(bound==d['group_order']==80640,'claimed graph upper bound')
    lower=group_order(gens,bound)
    return {'status':'PASS','actual_code_dimensions':[len(C),len(S)],'graph_order':120,'graph_valency':77,'symmetric_projector_image_C':True,'minimum_words_in_S':len(words),'minimum_supports':len(supports),'support_pair_incidence':pairs,'graph_refinement_chain_zero_based':d['graph_refinement_chain'],'full_graph_upper_bound':bound,'explicit_subgroup_order':lower,'Aut_C_equals_Aut_S_equals_Aut_graph':True,'exhaustive_word_enumeration_repeated':False,'graph_isomorphism_backend_used':False,'new_formal_declarations':0}

def controls(A,gens,C,S,d,counts):
    out=[]
    def reject(name,fn):
        try:fn()
        except ValueError:out.append(name);return
        raise ValueError('Unrejected mutation: '+name)
    bad=copy.deepcopy(counts[20]);bad['coefficient_vectors']-=1;reject('incomplete retained enumeration',lambda:retained_count(bad,20))
    bad=copy.deepcopy(counts[20]);bad['weight_counts'][30]=110;bad['weight_counts'][33]+=2;reject('wrong retained minimum multiplicity',lambda:retained_count(bad,20))
    wrong=[1]+[0]*119;reject('nonmember seed',lambda:seed_check(wrong,S))
    bad=copy.deepcopy(gens);bad[0][0]=bad[0][1];reject('nonpermutation generator',lambda:graph_action(A,bad))
    wrong=list(range(120));wrong[0],wrong[1]=wrong[1],wrong[0];reject('permutation not preserving graph',lambda:graph_action(A,[wrong]))
    reject('proper subgroup lower bound',lambda:group_order([list(range(120))],80640))
    bad=copy.deepcopy(d['graph_refinement_chain']);bad[1][1]-=1;reject('altered stabilizer cell bound',lambda:upper_bound(A,bad))
    words=orbit(d['seed'],gens,112);badwords=set(words);badwords.pop();reject('incomplete minimum orbit',lambda:supports_check(A,badwords,d))
    complement=[[int(i!=j)-v for j,v in enumerate(r)]for i,r in enumerate(A)];reject('wrong graph complement identification',lambda:supports_check(complement,words,d))
    reject('confusing graph code with difference code',lambda:need(len(C)==20 and rref(C)==S,'distinct C/S spaces'))
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
    if (HERE/'manifest.json').exists():
        for r in load(HERE/'manifest.json')['exports']:
            q=HERE/r['path'];need(q.stat().st_size==r['bytes']and sha(q)==r['sha256'],'frozen export '+r['path'])
    bindings=load(HERE/'retained_bindings.json')
    for r in bindings:
        q=HERE/r['path'];need(q.stat().st_size==r['bytes']and sha(q)==r['sha256'],'retained file '+r['path'])
        if a.study_root:
            q=a.study_root/r['origin'];need(q.stat().st_size==r['bytes']and sha(q)==r['sha256'],'original retained file '+r['origin'])
    if a.study_root:
        primary=load(HERE/'source_map.json')['source'];q=a.study_root/primary['path'];need(q.stat().st_size==primary['bytes']and sha(q)==primary['sha256'],'exact primary edition')
    em=load(HERE/'retained/enumeration_manifest.json');emap={r['path']:r for r in em['exports']}
    for name in ['120_adjacency','120_differences']:
        for suffix,key in [('.json',name+'.json'),('.txt','bases/'+name+'.txt')]:
            need(sha(HERE/'retained'/ (name+suffix))==emap[key]['sha256'],'exact retained count/basis provenance')
    modulemap={r['path']:r for r in load(HERE/'retained/module_manifest.json')['exports']}
    need(sha(HERE/'retained/module_data.json')==modulemap['module_data.json']['sha256'],'literal retained permutation group')
    need(sha(HERE/'retained/steiner_construction.py')==modulemap['steiner_construction.py']['sha256'],'whole retained constructor')
    root_review=load(HERE/'retained/module_root_review.json');need(root_review['author_manifest_sha256']==sha(HERE/'retained/module_manifest.json'),'distinct root group review edition')
    rootmap={r['path']:r for r in load(HERE/'retained/module_root_manifest.json')['exports']};need(rootmap['review.json']['sha256']==sha(HERE/'retained/module_root_review.json'),'frozen distinct group review')
    methodmap={r['path']:r for r in load(HERE/'retained/enumeration_method_review_manifest.json')['exports']};need(methodmap['review.json']['sha256']==sha(HERE/'retained/enumeration_method_review.json'),'frozen method review')
    receipt=load(HERE/'retained/enumeration_receipt.json');need(receipt['method_review_sha256']==sha(HERE/'retained/enumeration_method_review_manifest.json'),'retained receipt method pin')
    need(emap['receipt.json']['sha256']==sha(HERE/'retained/enumeration_receipt.json'),'completed count receipt')
    spec=importlib.util.spec_from_file_location('retained_steiner',HERE/'retained/steiner_construction.py');constructor=importlib.util.module_from_spec(spec);spec.loader.exec_module(constructor)
    blocks,_=constructor.steiner_blocks();heptads=[b for b in blocks if b&3==0];need(len(heptads)==120,'actual deleted-heptad set')
    need({(x&y).bit_count()for i,x in enumerate(heptads)for y in heptads[:i]}=={1,3},'actual heptad intersection classes')
    A=[[int(i!=j and (x&y).bit_count()==3)for j,y in enumerate(heptads)]for i,x in enumerate(heptads)];constructor.srg_check(A,(120,77,52,44))
    C=basis_file(HERE/'retained/120_adjacency.txt');S=basis_file(HERE/'retained/120_differences.txt');gens=[[v-1 for v in g]for g in load(HERE/'retained/module_data.json')['full_generators']];d=load(HERE/'certificate_data.json');counts={21:load(HERE/'retained/120_adjacency.json'),20:load(HERE/'retained/120_differences.json')}
    report=inspect(d,A,gens,C,S,counts);report['controls_rejected']=controls(A,gens,C,S,d,counts);report['retained_bindings_checked']=len(bindings)
    if a.render:
        import shutil
        from pypdf import PdfReader
        work=a.out/'render';work.mkdir();shutil.copy2(HERE/'proof.tex',work/'proof.tex')
        for _ in range(2):
            r=subprocess.run([a.xelatex,'-halt-on-error','-interaction=nonstopmode','proof.tex'],cwd=work,capture_output=True,text=True);need(r.returncode==0,'TeX render')
        log=(work/'proof.log').read_text();need(not any(s in log for s in ['Overfull','LaTeX Warning:','Undefined control sequence']),'clean TeX diagnostics')
        text=lambda p:'\n'.join(x.extract_text()or'' for x in PdfReader(p).pages)
        need(text(work/'proof.pdf')==text(HERE/'proof.pdf'),'exact fresh PDF page text');report['rendered_pages']=len(PdfReader(work/'proof.pdf').pages)
    report['elapsed_seconds']=round(time.monotonic()-start,3);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
