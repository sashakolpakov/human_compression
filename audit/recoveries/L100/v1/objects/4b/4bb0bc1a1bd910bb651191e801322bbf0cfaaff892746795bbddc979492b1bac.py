"""Small set-only witness: the two displayed p4 conditions are insufficient."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import json,hashlib
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def need(v,s):
    if not v:raise ValueError(s)
def pts(x):return {i for i in range(21)if x>>i&1}
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    source=G.parent.parent/'corpus161_access_supplement_v4/primary/L100_Halle_1999_preprint.pdf'
    mp=G/'constructions_component_v1/expected/model.json';bp=G/'baer_component_v1/inputs/baer_orbits.json';gp=G/'palette_serialization_v1/derived/group_elements.json'
    m=json.loads(mp.read_text());orbs=json.loads(bp.read_text())['orbits'];raw=json.loads(gp.read_text());lines=[pts(l)for l in m['lines']]
    # Fixed explicit witnesses, not assertions extracted from a discovery count.
    pole=[1639,1945];completions=[dict(minus=[710657,1390593],p=1),dict(minus=[301704,145988],p=512)]
    answer=[]
    for r in completions:
        four=pole+r['minus'];sets=[pts(x)for x in four];point=pts(r['p']);a,b,c,d=sets
        need(len(set(four))==4 and all(x in orbs[0]for x in four),'four distinct subplanes in the same acquired PSL orbit')
        need(all(len(x)==7 and all(len(x&l)in [1,3]for l in lines)for x in sets),'literal Fano subplanes')
        need(a&c==b&d==point and len(point)==1,'exact two displayed cross intersections')
        left=a&b;right=c&d;need(len(left)==len(right)==3,'two triple intersections')
        need(left|right in lines and left&right==point,'triples collinear and their union is one full projective line')
        witnesses=[]
        for x in sets:
            maps=[g for g in raw['elements']if {g[i]-1 for i in a}==x]
            need(maps,'same fixed group orbit with explicit actual map');witnesses.append(maps[0])
        answer.append(dict(ordered_subplane_masks=four,point_mask=r['p'],central_line_mask=sum(1<<p for p in left|right),cross_intersection_sizes=[[len(u&v)for v in [c,d]]for u in [a,b]],literal_group_maps_from_first=witnesses))
    need(set(answer[0]['ordered_subplane_masks'])!=set(answer[1]['ordered_subplane_masks']),'different unordered configurations, so not merely a pole-order convention')
    r=dict(status='PASS_DISPLAYED_CONDITIONS_UNDERDETERMINE_BUTTERFLY',source_physical_page=4,scope='Only the two displayed intersection conditions are under-specified relative to the claimed uniqueness. Standard butterflies may carry a stronger conventional definition from the cited literature; no principal classification refutation is asserted.',positive_pole=pole,witnesses=answer,inputs=[pin(x)for x in [source,mp,bp,gp,Path(__file__).resolve()]])
    (P/'ambiguity01.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
if __name__=='__main__':main()
