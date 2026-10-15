"""Independent finite closure, all-marking intersections and positive flag complex."""
import sys
if sys.flags.optimize:raise RuntimeError('normal Python required')
sys.dont_write_bytecode=True
from pathlib import Path
import hashlib,json,math,itertools
W=Path(__file__).resolve().parent
def need(v,m):
    if not v:raise ValueError(m)
def pin(p):
    p=p.resolve();b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def compose(a,b):return tuple(b[a[i]]for i in range(len(a)))
def closure(gens,n):
    identity=tuple(range(n));items=[identity];seen={identity}
    for x in items:
        for y in gens:
            z=compose(x,y)
            if z not in seen:seen.add(z);items.append(z)
    return seen
def order(p):
    seen=set();lengths=[]
    for x in range(len(p)):
        if x in seen:continue
        y=x;k=0
        while y not in seen:seen.add(y);y=p[y];k+=1
        lengths.append(k)
    return math.lcm(*lengths)
def cosets(group,sub):
    pending=set(group);out=[];index={}
    while pending:
        g=min(pending);c=frozenset(compose(h,g)for h in sub)
        need(c<=pending,'exact partition')
        for h in c:index[h]=len(out)
        out.append(c);pending.difference_update(c)
    return out,index
def flag_audit(sub):
    group=sub[15];data=[cosets(group,sub[15^(1<<i)])for i in range(4)]
    objects=[x[0]for x in data];indices=[x[1]for x in data]
    orbit={tuple(indices[i][g]for i in range(4))for g in group}
    adjacency={(i,j):[{y for y,b in enumerate(objects[j])if a&b}for a in objects[i]]for i in range(4)for j in range(i+1,4)}
    all_flags={};counts={};first_extra=None
    for mask in range(16):
        types=[i for i in range(4)if mask>>i&1];flags={()}
        for pos,i in enumerate(types):
            extended=set()
            for flag in flags:
                allowed=set(range(len(objects[i])))
                for j,x in zip(types[:pos],flag):allowed.intersection_update(adjacency[j,i][x])
                extended.update(flag+(x,)for x in allowed)
            flags=extended
        projected={tuple(c[i]for i in types)for c in orbit}
        need(projected<=flags,'actual orbit flags')
        if flags!=projected and first_extra is None:first_extra=dict(types=types,flag=list(min(flags-projected)),actual=len(flags),orbit=len(projected))
        all_flags[mask]=flags;counts[str(mask)]=len(flags)
    if first_extra is None:
        for missing in range(4):
            counts_panel={}
            for chamber in all_flags[15]:
                panel=chamber[:missing]+chamber[missing+1:]
                counts_panel[panel]=counts_panel.get(panel,0)+1
            need(set(counts_panel.values())=={2},'every panel is thin')
    return dict(object_counts=list(map(len,objects)),chamber_orbit=len(orbit),actual_chambers=len(all_flags[15]),flag_counts=counts,first_nonorbit_flag=first_extra)
def main():
    source=W/'fresh01/quotients.json';paths=[source,Path(__file__),Path(sys.executable)];inputs=[pin(p)for p in paths]
    rows=json.loads(source.read_text());need(len(rows)==23,'complete roster');results=[];positive=None;incidence=None
    expected_matrix=[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]]
    for row in rows:
        gens=[tuple(x-1 for x in p)for p in row['permutations']];n=len(gens[0])
        need(all(sorted(g)==list(range(n))for g in gens),'permutations')
        need([order(g)for g in gens]==[2]*4,'involutions')
        need([[order(compose(a,b))for b in gens]for a in gens]==expected_matrix,'matrix')
        sub={mask:closure([g for i,g in enumerate(gens)if mask>>i&1],n)for mask in range(16)}
        need(len(sub[15])==row['order'],'order')
        failures=[[i,j,len(sub[i]&sub[j]),len(sub[i&j])]for i in range(16)for j in range(16)if sub[i]&sub[j]!=sub[i&j]]
        r=dict(node=row['node'],order=row['order'],local_orders=[len(sub[15^(1<<i)])for i in range(4)],intersection_failures=failures)
        if not failures:
            r['actual_flags']=flag_audit(sub)
            if r['actual_flags']['first_nonorbit_flag']is None:need(positive is None,'unique positive');positive=r
            else:need(incidence is None,'unique incidence-only failure');incidence=r
        results.append(r)
    need(sum(bool(r['intersection_failures'])for r in results)==21,'21IP exclusions')
    need(sum(r['order']==3840 for r in results)==11 and all(r['intersection_failures']for r in results if r['order']==3840),'eleven3840 exclusions')
    need(positive['order']==1920 and positive['local_orders']==[60]*4 and positive['actual_flags']['object_counts']==[32]*4 and positive['actual_flags']['actual_chambers']==1920,'literal positive')
    need(incidence['order']==960,'960 extra actual flags')
    need([pin(p)for p in paths]==inputs,'stable inputs')
    out=W/'independent01';need(not out.exists(),'fresh');out.mkdir()
    report=dict(status='PASS_INDEPENDENT_COMPLETE_SQUARE_MARKINGS',inputs=inputs,rows=results,positive=positive,incidence_only_failure=incidence,author_helpers_imported=False,normal_quotient_searches=0,whole_original_credit=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status=report['status'],markings=len(results),positive_chambers=positive['actual_flags']['actual_chambers'],incidence_failure=incidence['actual_flags']['first_nonorbit_flag'])))
if __name__=='__main__':main()
