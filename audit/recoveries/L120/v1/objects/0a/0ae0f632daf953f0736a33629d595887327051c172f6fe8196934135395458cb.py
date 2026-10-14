"""Exact interfaces for the completed fixed-edition survey; no new census."""
import sys
if sys.flags.optimize:
    raise RuntimeError('unoptimized execution required')
from pathlib import Path
from fractions import Fraction
import json,re,hashlib,math,collections
from diagrams import graph,validate
from verify_diagrams import conjugacy
from read_figure import extract,literal

def need(b,message):
    if not b:raise ValueError(message)
def load(p):return json.loads(p.read_text())
def integer(x):return type(x)is int and x>=0

def formula(N,even):
    n=N//2;lam=lambda k:(k+2)**2//4
    def psi(k):return sum(l//2+1 for l in range(max(0,2*k-n)))
    if even:
        mu=Fraction(-2*(n//2))
        for k in range(2,n+1,2):
            gamma=Fraction(k*k,8)+Fraction(3*k,4)+1;delta=Fraction(k*k,8)+Fraction(k,4)
            mu+=gamma*((n-k+2)//2)+delta*((n-k+1)//2)
        ans=(mu+sum(lam(k)-psi(k)-1 for k in range(2,n+1,2)))/2
    else:ans=-Fraction(3*n,2)+sum(lam(k)*(Fraction(n-k,2)+1)for k in range(1,n+1))-Fraction(sum(psi(k)for k in range(n//2+1,n+1)),2)
    need(ans.denominator==1,'integer orbit formula');return int(ans)

def direct(N,even):
    total=0
    for t in range(N//4+1):
        for x in range(N//2+1):
            for y in range(x,(N-4*t-2*x)//2+1):
                for z in range((N-4*t-2*x-2*y)//2+1):
                    if t==0 and sum(a>0 for a in (x,y,z))<2:continue
                    if even and not(x%2==y%2==z%2):continue
                    total+=1
    return total

def permorder(p):
    seen=set();order=1
    for v in range(len(p)):
        if v in seen:continue
        w=v;n=0
        while w not in seen:seen.add(w);n+=1;w=p[w]
        order=math.lcm(order,n)
    return order

def check_marking(marks,n,typ):
    need(all(len(g)==n and all(type(v)is int for v in g)and sorted(g)==list(range(1,n+1)) for g in marks),'literal permutation')
    a=[[v-1 for v in g]for g in marks]
    need(all(permorder(g)==2 for g in a),'nonidentity involutions')
    for i,g in enumerate(a):
        for h in a[i+2:]:need(all(g[h[v]]==h[g[v]]for v in range(n)),'string relations')
    need([permorder([h[g[v]]for v in range(n)])for g,h in zip(a,a[1:])]==typ,'literal adjacent type')

def source_check(P,raw,tables,clauses,figure):
    text=raw.decode();need(hashlib.sha256(raw).hexdigest()==tables['primary_tex_sha256'],'exact source edition')
    clean=re.sub(r'(?m)(?<!\\)%.*$','',text)
    labels=[];section=0;tn=0;counters=collections.Counter()
    for m in re.finditer(r'\\section(?:\*)?\{|\\begin\{(theorem|corollary|problem|conjecture)\}',clean):
        if m.group(1)is None:section+=1;tn=0
        elif m.group(1)=='theorem':tn+=1;labels.append(f'Theorem {section}.{tn}')
        else:k=m.group(1);counters[k]+=1;labels.append(k.capitalize()+' '+str(counters[k]))
    need(labels==[r['label']for r in clauses['clauses']],'exact complete ordered50 source labels')
    blocks=re.findall(r'\\begin\{table\}(.*?)\\end\{table\}',text,re.S)
    need(len(blocks)==6,'all source tables')
    def number(s):
        s=s.strip().replace(',','');need(bool(re.fullmatch(r'[0-9]+',s)),'source integer');return int(s)
    for t,b in zip(tables['tables'],blocks):
        need(hashlib.sha256(b.encode()).hexdigest()==t['source_block_sha256'],'literal source table block')
        i=t['table'];actual=[]
        if i in (1,3):
            g='S'if i==1 else'A';ranks=range(3,14 if i==1 else 9)
            for line in b.splitlines():
                m=re.fullmatch(r'\$'+g+r'_(?:\{(\d+)\}|(\d+))\$&(.*?)\\\\',line.strip())
                if m:
                    vals=[number(s)for s in m[3].split('&')];need(len(vals)==len(ranks),'source columns');n=int(m[1]or m[2]);actual.append(dict(group=g+str(n),degree=n,rank_counts=dict(zip(map(str,ranks),vals))))
        elif i==2:
            for line in b.splitlines():
                m=re.fullmatch(r'([\d,]+)\s*&\s*(\d+)\s*&\s*(\d+)\\\\',line.strip())
                if m:actual.append(dict(degrees=list(map(int,m[1].split(','))),symmetric=int(m[2]),alternating=int(m[3])))
        elif i==5:
            for line in b.splitlines():
                if not line.strip().startswith('$')or'Order'in line:continue
                v=line.strip().removesuffix('\\\\').split('&')
                if len(v)!=5:continue
                g=v[0].strip().strip('$').replace('\\prime',"'").replace('{','').replace('}','').replace('_','').replace('^','').replace(' ','')
                actual.append(dict(group=g,source_order=number(v[1]),rank_counts=dict(zip(('3','4','5'),[None if z.strip()=='Unknown'else number(z)for z in v[2:]]))))
        else:continue # exact block hash plus independently checked individual interfaces below
        need(actual==t['rows'],'all literal source rows')
    matrices=extract(text);need(len(matrices)==18,'all literal source matrices')
    for matrix,row in zip(matrices,figure['records']):
        marks,edges=literal(matrix,row['n']);need(hashlib.sha256(matrix.encode()).hexdigest()==row['source_matrix_sha256'],'source matrix bytes')
        need([list(g)for g in marks]==row['marks']and[list(e)for e in edges]==row['edges'],'all literal source edges')
    return dict(named_labels=50,tables=6,diagrams=18)

def verify(P,S,scope=None,clauses=None,figure=None,source_tex=None):
    scope=load(P/'survey_table_scope09.json')if scope is None else scope
    clauses=load(P/'named_clause_register03.json')if clauses is None else clauses
    figure=load(P/'survey_figure_records01.json')if figure is None else figure
    tables=load(P/'survey_tables03.json');base=load(P/'survey_table_comparison03.json');finite=load(P/'finite_numeric_interfaces.json');smap=load(P/'source_map.json')
    labels=[r['label']for r in clauses['clauses']]
    need(len(labels)==50 and len(set(labels))==50,'complete distinct50 clause labels')
    need(collections.Counter(r['label'].split()[0]for r in clauses['clauses'])=={'Theorem':31,'Corollary':1,'Problem':15,'Conjecture':3},'exact named kinds')
    need(all(r.get('disposition')and r.get('route')and r.get('qualification')for r in clauses['clauses']),'every exact disposition')
    retained={'Theorem 3.1','Theorem 4.6','Theorem 5.1','Theorem 5.4','Theorem 5.6','Theorem 11.1','Theorem 11.2'}
    need(set(smap['retained_assertions'])==retained,'seven exact retained assertions')
    assertions={x for x in labels if x.startswith(('Theorem','Corollary'))};need(set(smap['acquired_or_corrected_assertions'])==assertions-retained,'25 acquired/corrected assertions')
    need(all(v==0 for v in smap['credit'].values()),'no author whole/question/formal/measurement credit')
    expected={(t['table'],r['group'],int(k)):v for t in tables['tables']if t['table']in(1,3,5)for r in t['rows']for k,v in r['rank_counts'].items()}
    old={(t['table'],r['group'],int(k)):v['verified_value']for t in base['numeric_tables']if t['table']in(1,3,5)for r in t['rows']for k,v in r['dispositions'].items()}
    need(len(expected)==221,'221 original numeric cells')
    new={}
    for g,x in finite.items():
        actual=load(S/x['input']['path']);need(actual['rows']==x['rows'],'exact accepted finite receipt')
        for r in x['rows']:
            need(integer(r['with_duality']),'integer exact count')
            if g!='S6':need(r['ordered']+r['self_dual']==2*r['with_duality'],'exact duality arithmetic')
            new[(g,r['rank'])]=r['with_duality']
        if g=='S6':
            for r in x['rows']:
                n=r['point_classes'];a=[v-1 for v in r['outer_permutation']];b=[v-1 for v in r['reversal_permutation']]
                need(sorted(a)==sorted(b)==list(range(n))and all(a[a[v]]==b[b[v]]==v for v in range(n)),'literal full-Aut and duality involutions')
                unseen=set(range(n));orbits=0
                while unseen:
                    q=[min(unseen)];o=set(q)
                    for v in q:
                        for w in (a[v],b[v]):
                            if w not in o:o.add(w);q.append(w)
                    unseen-=o;orbits+=1
                need(orbits==r['with_duality'],'actual S6 full fusion')
    ext={r['group']:r for r in load(P/'external_census_interfaces.json')['claims']}
    seen=set();counts=collections.Counter()
    for r in scope['rows']:
        key=(r['table'],r['group'],r['rank']);need(key in expected and key not in seen,'exact unique source cell');seen.add(key);need(r['source_value']==expected[key],'source value retained')
        d=r['disposition'];counts[d]+=1
        if d=='retained_independent_published_classification':
            g=r['group'].replace("'",'');need(g in ext and r['project_census_verified']is False,'independent retained classification')
            value=ext[g]['rank_counts'].get(str(r['rank']),0);need(r['published_value']==value,'exact published retained cell')
            need(r['source_value']is None or value==r['source_value'],'retained source comparison')
        else:
            need(d=='acquired_project_result'and r['group']not in ('Ru','Suz',"O'N"),'no self-premise or silently promoted retained cell')
            value=new.get((r['group'],r['rank']),old[key]);need(value is not None and value==r['comparison_value']==r['source_value'],'actual acquired cell comparison')
    need(seen==set(expected) and counts=={'acquired_project_result':212,'retained_independent_published_classification':9},'exact212/9 cell partition')
    controls=0
    for N in range(1,51):
        for even in (False,True):need(formula(N,even)==direct(N,even),'literal orbit count control');controls+=1
    for row in tables['tables'][1]['rows']:
        for n in row['degrees']:
            actual=(5,1)if n==6 else(formula(n,False),formula(n,True));need(actual==(row['symmetric'],row['alternating']),'exact Table2 formula/fusion row')
    interfaces=load(P/'table_interfaces01.json');need(len(interfaces['table4'])==2 and len(interfaces['table6'])==4,'both individual table interfaces')
    for row in interfaces['table4_literal_controls']:check_marking(row['marks'],row['degree'],row['type'])
    for row in interfaces['table6']:
        need(row['matching_acquired_tuples'],'no empty finite interface')
        for t in row['matching_acquired_tuples']:check_marking(t['marks'],t['degree'],row['printed_type'])
    need(len(figure['records'])==18,'18 diagram families')
    acquired=load(S/'corpus106_L042_principal_v1/source_figure_records.json')
    need(figure['records']==acquired['records'],'all literal figure families identical to acquired full classification')
    for row in figure['records']:
        model,_=graph(row['k'],row['family'],row['n']);conjugacy(row['marks'],model,row['to_model'])
    source=None
    if source_tex is not None:source=source_check(P,source_tex.read_bytes(),tables,clauses,figure)
    return dict(status='PASS_COMPLETE_L120_SOURCE_INTERFACES',clauses=50,assertions=32,retained_assertions=7,acquired_or_corrected_assertions=25,questions=18,rank_count_cells=221,project_cells=212,retained_cells=9,source_only_cells=0,formula_controls=controls,table2_rows=14,table4_families=2,table4_literal_controls=22,table6_rows=4,figure1_models=18,source_replay=source,new_census=False,new_question_credit=0,whole_original_credit=0)
