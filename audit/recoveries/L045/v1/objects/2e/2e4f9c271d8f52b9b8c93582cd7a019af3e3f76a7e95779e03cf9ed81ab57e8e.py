"""Independent brute permutations, without the author's reflection parametrization."""
import sys
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
import itertools,json
def need(b,s):
    if not b:raise ValueError(s)
rows=[]
for n in (8,9):
    labels=list(range(n))if n%2 else list(range(1,n));x=list(range(n));t=list(range(n))
    for a,b in zip(labels,labels[1:]+labels[:1]):x[a]=b
    for a,b in [(0,1),(2,5)if n%2 else (2,3)]:t[a]=b;t[b]=a
    xi=[x.index(i)for i in range(n)];all_count=0;inverting=[];bad=[]
    for h in itertools.permutations(range(n)):
        all_count+=1
        if all(h[x[i]]==xi[h[i]]for i in range(n)):
            inverting.append(h)
            if all(h[t[i]]==t[h[i]]for i in range(n)):bad.append(h)
    need(len(inverting)==len(labels) and not bad,'literal inverting permutations')
    rows.append({'degree':n,'all_permutations':all_count,'inverters':len(inverting),'also_fix_t':len(bad)})
print(json.dumps({'status':'PASS_INDEPENDENT_FULL_PERMUTATIONS','rows':rows},indent=2))
