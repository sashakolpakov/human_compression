#!/usr/bin/env python3
"""Parse only explicit permutation/subgroup/list data; never execute source Magma."""
import argparse,hashlib,json,re,tarfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def perms(body,n=100):
    if re.search(r'[^\d\s(),]',body): raise ValueError('Unexpected generator syntax')
    ans=[];depth=0;start=0
    for i,c in enumerate(body+','):
        if c=='(': depth+=1
        if c==')': depth-=1
        if depth<0: raise ValueError('Unbalanced parentheses')
        if c==',' and depth==0:
            p=list(range(1,n+1));text=body[start:i].strip();start=i+1
            if not text: raise ValueError('Empty generator')
            covered=set()
            for cyc in re.findall(r'\(([^()]*)\)',text):
                pts=[int(x) for x in cyc.split(',') if x.strip()]
                if len(set(pts))!=len(pts) or covered.intersection(pts) or any(x<1 or x>n for x in pts):raise ValueError('Invalid cycle')
                covered.update(pts)
                for a,b in zip(pts,pts[1:]+pts[:1]):p[a-1]=b
            if sorted(p)!=list(range(1,n+1)): raise ValueError('Not permutation')
            ans.append(p)
    if depth:raise ValueError('Unbalanced parentheses')
    return ans

def parse(s):
    out=[];current=[];ambient=None;h=None;sel=None
    for stmt in s.split(';'):
        stmt=stmt.strip()
        if not stmt:continue
        m=re.fullmatch(r'(g|h)\s*:=\s*sub<(?:Sym\(100\)|g)\|(.*)>',stmt,re.S)
        if m:
            p=perms(m[2])
            if m[1]=='g':ambient=p
            else:h=p
        elif re.fullmatch(r'G\s*:=\s*g',stmt):pass
        elif re.fullmatch(r'geo\s*:=\s*\[\]',stmt):out=[]
        elif re.fullmatch(r'geosub\s*:=\s*\[\]',stmt):current=[]
        elif stmt=='Append(~geosub,h)':current.append(h)
        elif stmt=='Append(~geo,geosub)':out.append(list(current))
        elif re.fullmatch(r'geo\s*:=\s*\[\s*geo\[\d+\](?:\s*,\s*geo\[\d+\])*\s*\]',stmt):
            sel=[int(x) for x in re.findall(r'geo\[(\d+)\]',stmt)]
        else:raise ValueError('Unsupported statement: '+stmt[:100])
    return dict(ambient_generators=ambient,raw_geometries=out,selected_indices=sel or list(range(1,len(out)+1)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True,type=Path);a=ap.parse_args()
    out={'source_url':'https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S1461157000001133/resource/name/S1461157000001133sup002.tar','archive_sha256':hashlib.sha256(a.archive.read_bytes()).hexdigest(),'files':{}}
    with tarfile.open(a.archive) as t:
        for name in ['j2.rk3','j2.rk4']:
            b=t.extractfile(name).read();entry=parse(b.decode());entry['sha256']=hashlib.sha256(b).hexdigest();out['files'][name]=entry
    p=ROOT/'phase4_j2_source_data.json';p.write_text(json.dumps(out,separators=(',',':'))+'\n')
    with (ROOT/'phase4_j2_parsed.g').open('w') as f:
        f.write('# Generated only from validated permutation arrays, not Magma execution.\n')
        f.write('sourceData:=[];;\n')
        for name,entry in out['files'].items():
            def gp(gens):return 'Group(['+','.join('PermList('+json.dumps(p)+')' for p in gens)+'])'
            f.write('Add(sourceData,rec(name:="'+name+'",G:='+gp(entry['ambient_generators'])+',selected:='+str(entry['selected_indices'])+',geos:=[')
            f.write(','.join('['+','.join(gp(gens) for gens in geo)+']' for geo in entry['raw_geometries']))
            f.write(']));;\n')
    print(json.dumps({k:{'raw':len(v['raw_geometries']),'selected':len(v['selected_indices']),'sha256':v['sha256']} for k,v in out['files'].items()},indent=2))
if __name__=='__main__':main()
