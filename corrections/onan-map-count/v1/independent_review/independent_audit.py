"""Independent integer evaluation and class-constant/source comparisons."""
import sys
if sys.flags.optimize:raise RuntimeError('Optimized Python is not accepted')
from pathlib import Path
from itertools import combinations_with_replacement
from collections import Counter
from html import unescape
from math import lcm
import hashlib,json,re,subprocess,os
from pypdf import PdfReader
S=Path('/Users/sasha/medusa/research/leemans');A=S/'corpus106_L046_maximal_bounds_v1'
W=S/'reboot_20261013/L046_maximal_bounds_distinct'
def need(value,message):
    if not value:raise ValueError(message)
def pin(path):
    b=path.read_bytes();return dict(absolute_path=str(path),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
bindings=[]
need(pin(A/'manifest.json')['sha256']=='d7e826cec742417d68173aa748de3b6b44b6a348d63cd6fc85394ff5bd279919','author manifest')
bindings.append(pin(A/'manifest.json'))
for item in json.loads((A/'manifest.json').read_text())['exports']:
    r=pin(A/item['path']);need(all(r[k]==item[k]for k in ['bytes','sha256']),'export hash');bindings.append(r)
for item in json.loads((A/'dependencies.json').read_text())['bindings']:
    r=pin(Path(item['absolute_path']));need(all(r[k]==item[k]for k in ['bytes','sha256']),'dependency hash');bindings.append(r)

# Independent parser: retain integer degree/vectors, then use one common
# denominator, not the author's Fraction summation implementation.
tables={};active=None;maxes=None
for line in (W/'replay01/maximal_vectors.g.stdout').read_text().splitlines():
    t=line.split()
    if not t:continue
    if t[0]=='TABLE':
        need(active is None,'open table');active=t[1];tables[active]=dict(order=int(t[2]),nt=int(t[3]),nc=int(t[4]),rows=[])
    elif t[0]=='TYPES':tables[active]['types']=list(map(int,t[1:]))
    elif t[0]=='VECTOR':tables[active]['rows'].append(list(map(int,t[1:])))
    elif t[0]=='ENDTABLE':need(t[1]==active,'bad close');active=None
    elif t[0]=='MAXCLASSES':maxes=t[1:]
    else:need(line=='COMPLETE EXACT ORDER VECTORS','unexpected record')
need(active is None and maxes is not None,'incomplete table')
for name,t in tables.items():
    need(len(t['rows'])==t['nc'] and len(t['types'])==t['nt'],'table dimensions')
    need(sum(v[0]**2 for v in t['rows'])==t['order'],'character degree squares')
    need(sum(v[0]==1 and sum(v[1:])==t['order'] for v in t['rows'])==1,'trivial character class partition')
    need(all(len(v)==1+t['nt'] for v in t['rows']),'row dimensions')
    t['denominator']=lcm(*(v[0]for v in t['rows']))
def count(name,p,q):
    t=tables[name]
    if p not in t['types'] or q not in t['types']:return 0
    cols=[1+t['types'].index(x)for x in [2,p,q]];d=t['denominator']
    numerator=sum((d//v[0])*v[cols[0]]*v[cols[1]]*v[cols[2]]for v in t['rows'])
    quotient,remainder=divmod(numerator,d*t['order'])
    need(remainder==0 and quotient>=0,'nonintegral or negative count');return quotient

# Compare every available p,q>2 with an independently structured GAP
# computation summing class multiplication constants times target-class size.
lines=[x for x in (W/'class_constants.stdout').read_text().splitlines() if x.strip()];need(lines[-1]=='COMPLETE DISTINCT CLASS CONSTANT COUNTS','class constants incomplete')
constant_keys=set()
for line in lines[:-1]:
    tag,name,p,q,n=line.split();need(tag=='COUNT','constant record');p,q,n=map(int,[p,q,n])
    key=(name,p,q);need(key not in constant_keys,'duplicate constant record');constant_keys.add(key)
    need(count(name,p,q)==n,'independent class constant mismatch')
expected={(name,p,q)for name,t in tables.items()for p,q in combinations_with_replacement([s for s in t['types']if s>2],2)}
need(constant_keys==expected,'constant count coverage')

# Literal primary Atlas list: thirteen distinct subgroup-class rows, with
# multiplicity retained even when the abstract isomorphism type repeats.
html=(A/'primary_atlas_ON.html').read_text(errors='replace')
part=html.split('<H3>Maximal subgroups of O\'N</H3>')[1].split('</TABLE>')[0]
atlas=[]
for row in re.findall(r'<TR>(.*?)</TR>',part,re.S|re.I):
    cells=re.findall(r'<TD[^>]*>(.*?)(?=<TD|</TR>|$)',row,re.S|re.I)
    if len(cells)<3:continue
    plain=[unescape(re.sub('<[^>]*>','',c)).replace('\n',' ').strip() for c in cells]
    atlas.append(dict(type=plain[0],order=int(re.sub(r'\s','',plain[1])),index=int(re.sub(r'\s','',plain[2]))))
need(len(atlas)==13,'primary maximal list coverage')
need(len(maxes)==13,'stored maximal list coverage')
for x,name in zip(atlas,maxes):
    need(x['order']==tables[name]['order'],'primary/stored order mismatch')
    need(x['order']*x['index']==tables['ON']['order'],'primary index mismatch')

G=tables['ON']['order'];aut=2*G;P=[s for s in tables['ON']['types']if s>2]
ledger=[]
for p,q in combinations_with_replacement(P,2):
    total=count('ON',p,q);bad=sum((G//tables[m]['order'])*count(m,p,q)for m in maxes)
    d,r=divmod(total-bad,aut);lower=max(0,d+(r!=0));upper=total//aut
    ledger.append(dict(p=p,q=q,all_pairs=total,maximal_upper_bad=bad,lower=lower,upper=upper))
old=json.loads((A/'bounds.json').read_text())
need(len(ledger)==len(old['rows'])==136,'ledger coverage')
for new,record in zip(ledger,old['rows']):need(all(new[k]==record[k]for k in new),'independent interval mismatch')
need(sum(x['lower']for x in ledger)==798370,'independent total')
need(sum(x['lower']==x['upper']for x in ledger)==20,'exact cell count')
special=next(x for x in ledger if(x['p'],x['q'])==(20,31))
need(special['all_pairs']==8403431565957120 and special['maximal_upper_bad']==0 and special['lower']==special['upper']==9118,'special cell')
with31=[n for n in maxes if 31 in tables[n]['types']]
need(with31==['L2(31)','ONM8'] and all(20 not in tables[n]['types']for n in with31),'order incompatibility')

# Read the original printed table, rather than only the author's extracted JSON.
pdf=PdfReader(S/'sources/catalogue_L046.pdf');text=pdf.pages[10].extract_text()
source={};started=False
for line in text.splitlines():
    tokens=line.split()
    if tokens==list(map(str,P)):started=True;continue
    if not started:continue
    if not tokens or not all(t.isdigit()for t in tokens):continue
    p=int(tokens[0]);need(p in P and len(tokens)==1+len(P)-P.index(p),'source row shape')
    for q,value in zip(P[P.index(p):],tokens[1:]):source[p,q]=int(value)
need(len(source)==136 and sum(source.values())==796772,'literal source total')
need(source[20,31]==7246,'literal printed special cell')
disagreements=[dict(p=x['p'],q=x['q'],source=source[x['p'],x['q']],lower=x['lower'],upper=x['upper'])for x in ledger if not x['lower']<=source[x['p'],x['q']]<=x['upper']]
need(disagreements==[dict(p=20,q=31,source=7246,lower=9118,upper=9118)],'literal interval discrepancies')
need({(x['p'],x['q'])for x in ledger if x['lower']>0}=={key for key,val in source.items()if val>0},'positive type identities')

native=W/'replay01/native'
for path,filename,first,last in [(native/'maximal_bounds.pdf',native/'page-%d.png',None,None),(S/'sources/catalogue_L046.pdf',W/'source-%d.png',3,5),(S/'sources/catalogue_L046.pdf',W/'source-table-%d.png',11,11)]:
    cmd=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105',f'-sOutputFile={filename}']
    if first is not None:cmd.extend([f'-dFirstPage={first}',f'-dLastPage={last}'])
    cmd.append(str(path));r=subprocess.run(cmd,capture_output=True,timeout=30);need(r.returncode==0,'raster failure')
probe=W/'rejected_optimized_output';env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
r=subprocess.run([sys.executable,'-O',str(A/'check.py'),'--out',str(probe)],capture_output=True,timeout=10,env=env)
(W/'optimization.stdout').write_bytes(r.stdout);(W/'optimization.stderr').write_bytes(r.stderr)
need(r.returncode!=0 and not probe.exists(),'optimized mode accepted')
result=dict(status='PASS_DISTINCT_INTEGER_CLASS_CONSTANT_AND_SOURCE_AUDIT',author_and_dependency_pins=bindings,tables=len(tables),class_constant_cells=len(constant_keys),primary_maximal_classes=atlas,maximal_table_names=maxes,integer_intervals=ledger,lower_total=sum(x['lower']for x in ledger),source_total=sum(source.values()),positive_types=sum(x['lower'] > 0 for x in ledger),exact_types=sum(x['lower']==x['upper']for x in ledger),source_discrepancies=disagreements,optimized_rejected_before_output=True,whole_original_credit=0,new_question_credit=0,new_measurement_credit=0,new_Lean_declarations=0)
(W/'independent_report.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k]for k in ['status','tables','class_constant_cells','lower_total','source_total','positive_types','exact_types']}))
