"""Manually transcribed structural labels, joined by the accepted node bijection."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,copy,json
from pathlib import Path
P=Path(__file__).resolve().parent
NAMES=dict(P='2^4:A5',F='L3(2)',A='A6',O='A5',S='2^4:S3',T='2^4:A4',Q='3^2:Q8',X='2xQ8',D='2xD8',E='3:S3')
# Each node position is a literal native-page transcription, not inferred from order.
TABLE='''2.1|7|2^4:A4|L=P/2^4 R=P/2^4
2.2|7|S4|L=S/2^2 R=A
2.3|7|3^2:4|L=A R=Q/3^2:4
2.4|7|7:3|L=F R=F
2.5|8|S4|L=S/2^2 R=F
2.6|8|Q8|L=Q R=Q
2.7|8|Q8|L=Q R=X/Q8
3.1|8|A4|L=P C=S/2^2 R=A
3.2|8|4|L=A C=D/4 R=A
3.3|8|D8|L=S/2^2 R=S/2^2 T=F
3.4|9|D8|L=S/2^2 R=S/2^2 T=A
3.5|9|3|L=F R=F T=E/3
3.6|9|S3|L=A C=S R=A
3.7|9|A4|L=P C=T/2^2 R=P
4.1|9|3|L=P C=S U=A D=A
4.2|10|2|L=A C=D/2 U=P D=P
4.3|10|2|L=F C=D/2 U=A D=A
4.4|10|2|L=P C=D/2 U=A D=A
4.5|10|2|L=A C=D/2 U=P D=P
4.6|11|2|L=F C=D/2 U=P D=A
4.7|11|2|L=F C=D/2 U=P D=P
4.8|11|3|TL=A TR=P BL=P BR=A
4.9|11|2|TL=A TR=P BL=S BR=A
4.10|12|2|TL=P TR=A BL=A BR=S
4.11|12|1|TL=F TR=F BL=O BR=O
5.1|12|1|TL=P TR=A BL=A BC=S R=P
5.2|13|1|TL=P TR=A BL=A BC=S R=P
5.3|13|1|TL=P TR=A BL=P BR=A R=P
5.4|13|1|TL=P TR=A BL=P BR=A R=P'''
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def expected():
    out={}
    for line in TABLE.splitlines():
        label,page,borel,raw=line.split('|');nodes={}
        for token in raw.split():
            pos,value=token.split('=');code,sep,kernel=value.partition('/');nodes[pos]=dict(parabolic=NAMES[code],kernel=kernel if sep else'1')
        out[label]=dict(page=int(page),borel=borel,nodes=nodes)
    return out
def join(inv,atoms,kernels):
    exp=expected();ar={r['atom']:r for r in atoms['atoms']};kr=kernels['certificates'];out=[]
    need(len(inv['routes'])==29 and {r['label']for r in inv['routes']}==set(exp),'exact 29 source rows')
    for r in sorted(inv['routes'],key=lambda x:tuple(map(int,x['label'].split('.')))):
        e=exp[r['label']];need(ar[r['borel_atom']]['name']==e['borel'],'literal Borel name');actual={};positions=[]
        for p in r['parabolics']:
            h=p['parabolic_atom'];k=p['kernel_atom'];actual[p['source_node']]=dict(parabolic=ar[h]['name'],kernel=ar[k]['name']);key=f'{h}:{k}';c=kr[key]
            positions.append(p|dict(parabolic=ar[h]['name'],kernel=ar[k]['name'],extension=c['extension'],kernel_certificate=key))
        need(actual==e['nodes'],'exact source-node group/kernel names')
        out.append(dict(label=r['label'],page=e['page'],catalogue=r['catalogue'],borel=e['borel'],borel_atom=r['borel_atom'],nodes=positions))
    need(sum(len(r['nodes'])for r in out)==99,'all 99 positions')
    special=next(r for r in out if r['label']=='2.3');right=next(x for x in special['nodes']if x['source_node']=='R');need(right['extension']=='NONSPLIT_INDEX_TWO','literal colon correction')
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--atoms',type=Path,required=True);ap.add_argument('--kernels',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output');inv=read(P/'input01/inventory.json');ar=read(a.atoms);kr=read(a.kernels);rows=join(inv,ar,kr);damages=[]
    for label,field in [('2.3','borel_atom'),('4.11','borel_atom')]:
        bad=copy.deepcopy(inv);next(r for r in bad['routes']if r['label']==label)[field]=2
        try:join(bad,ar,kr)
        except (ValueError,KeyError):damages.append(label+'-wrong-borel');continue
        raise ValueError('wrong source Borel admitted')
    bad=copy.deepcopy(inv);bad['routes'][0]['parabolics'][0]['kernel_atom']=9
    try:join(bad,ar,kr)
    except (ValueError,KeyError):damages.append('wrong-boxed-kernel')
    else:raise ValueError('wrong boxed kernel admitted')
    out=dict(status='PASS_ALL_PARABOLIC_SOURCE_NAMES',rows=rows,source='Fixed 22-page Halle preprint, physical pages 7--13; journal edition uncollated.',corrections=[dict(label='2.3',node='R',page=7,printed='3^2:Q8 = (boxed 3^2:4):2',actual='3^2:Q8 with normal index-two 3^2:4, nonsplit extension by C2',scope='Replace the outer split colon by a nonsplit extension dot, under the standard split-colon convention. No changed group, kernel, geometry or principal count.')],qualifications=['Unparenthesized boxed E4 x E4 : S3/A4 is paid as (E4 x E4):L, with the recorded action on the entire elementary abelian radical; no central direct factor or invariant vector complement is inferred.','The rank-four dotted central extensions C2.E8 are nonsplit and are retained as dotted, not silently promoted to semidirect products.'],damage_controls=damages,target_censuses=0,source_credit=0);a.out.write_text(json.dumps(out,indent=2)+'\n');print(out['status'],len(rows),len(damages))
if __name__=='__main__':main()
