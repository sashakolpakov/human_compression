"""Small independent set oracle; no complete Baer scan or catalogue search."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,itertools,json
from pathlib import Path
import certificate as c
P=Path(__file__).resolve().parent;G=P.parent
def points(mask):return {i for i in range(21)if mask>>i&1}
def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);x=a.parse_args();out=x.out.resolve();c.need(not out.exists()and out.parent.is_dir(),'fresh output')
    m=c.read(G/'constructions_component_v1/expected/model.json');lines=m['lines'];sets={l:points(l)for l in lines}
    F={label for v,label in zip(m['coordinate_points'],m['coordinate_to_retained'])if all(e in[0,1]for e in v)}
    c.need(len(F)==7 and all(len(F&L)in[1,3]for L in sets.values()),'embedded coordinate Fano plane')
    geometry=c.Geometry([sum(1<<i for i in F)],lines);pairs=geometry.objects[2];pair_sets={p:points(p)for p in pairs}
    checks=0
    for i,(l1,l2)in enumerate(geometry.objects[1]):
        u,v=sets[l1],sets[l2]
        c.need(bool(geometry.adj[0,1][0]>>i&1)==(F&(u|v)==u&v),'Baer-line-pair set oracle');checks+=1
        for j,p in enumerate(pairs):
            pp=pair_sets[p];line=next(L for L in sets.values()if pp<=L)
            answer=not((u|v)&pp)and bool(u&v&line)
            c.need(bool(geometry.adj[1,2][i]>>j&1)==answer,'line-pair/point-pair set oracle');checks+=1
    for j,p in enumerate(pairs):
        pp=pair_sets[p];line=next(L for L in sets.values()if pp<=L)
        c.need(bool(geometry.adj[0,2][0]>>j&1)==(not(F&pp)and len(F&line)==3),'Baer-point-pair set oracle');checks+=1
    actions=0
    for g in m['retained_generators']:
        for pair in geometry.objects[1]:
            got=c.action(1,pair,g);expected=tuple(sorted(sum(1<<g[p]for p in sets[l])for l in pair))
            c.need(got==expected and all(set(g[p]for p in sets[l])in sets.values()for l in pair),'literal induced line-pair action');actions+=1
    # Every single point replacement destroys the seven-point Fano subset.
    # This is a direct finite fact checked here, not presumed as a theorem.
    damaged=valid_replacements=0
    for p in F:
        for q in set(range(21))-F:
            B=F-{p}|{q};valid=all(len(B&L)in[1,3]for L in sets.values())
            valid_replacements+=valid;damaged+=1
    c.need(valid_replacements==0,'single-point replacement destroys this literal Fano plane')
    out.mkdir();report=dict(status='PASS_BAER_SOURCE_INCIDENCE_SMALL_SET_CONTROLS',set_comparisons=checks,line_pair_action_comparisons=actions,damaged_fano_subsets=damaged,
                            complete_baer_enumerations=0,catalogue_searches=0,source_credit=0)
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
