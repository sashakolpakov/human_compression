#!/usr/bin/env python3
"""Parse literal supplementary permutations and the FINAL active geo selection.
No Magma evaluation, source-label inference, or geometry-property inference.
"""
import argparse,hashlib,json,re,tarfile
from pathlib import Path
ARCHIVE_SHA='073cffc1946a6797ef0575ac26d21a88ac3fad24d6f32c3dd30311d254ec9613'
def digest(b):return hashlib.sha256(b).hexdigest()
def parse(raw,name):
    s=re.sub(r'/\*.*?\*/','',raw.decode(),flags=re.S)
    s=re.sub(r'//[^\n]*','',s)
    chunks=re.split(r'Append\s*\(\s*~geo\s*,\s*geosub\s*\)\s*;',s)
    rank=int(name.split('.rk')[1]);rows=[]
    for c in chunks[:-1]:
        groups=re.findall(r'\bh\s*:=\s*sub\s*<\s*g\s*\|\s*(.*?)>\s*;',c,re.S)
        if len(groups)!=rank:raise ValueError((name,'wrong parabolic count',len(groups)))
        row=[]
        for g in groups:
            g=re.sub(r'Id\s*\(\s*\$\s*\)', '()', g)  # literal identity only
            if not re.fullmatch(r'[0-9(),\s]+',g):raise ValueError((name,'nonliteral generator'))
            ps=[re.sub(r'\s+','',p) for p in re.split(r'\)\s*,\s*\(',g.strip())]
            # Splitting consumes the two boundary parentheses.
            for k in range(len(ps)):
                if k:ps[k]='('+ps[k]
                if k<len(ps)-1:ps[k]+=')'
                if not re.fullmatch(r'(?:\((?:[0-9]+(?:,[0-9]+)*)?\))+',ps[k]):raise ValueError(ps[k])
            row.append(ps)
        rows.append(row)
    tail=chunks[-1]
    selected=list(range(1,len(rows)+1))
    assignments=re.findall(r'\bgeo\s*:=\s*\[(.*?)\]\s*;',tail,re.S)
    if assignments:
        if len(assignments)!=1:raise ValueError((name,'unexpected multiple selections'))
        a=assignments[0].strip()
        m=re.fullmatch(r'geo\[i\]\s*:\s*i\s+in\s*\[([0-9,\s]+)\]',a)
        if m:selected=[int(x) for x in m[1].split(',')]
        else:
            if not re.fullmatch(r'\s*geo\[\d+\](?:\s*,\s*geo\[\d+\])*\s*',a):raise ValueError((name,'unsupported selection',a))
            selected=[int(x) for x in re.findall(r'geo\[(\d+)\]',a)]
    if any(not 1<=i<=len(rows) for i in selected) or len(set(selected))!=len(selected):raise ValueError('selection indices')
    meta={'member':name,'bytes':len(raw),'sha256':digest(raw),'rank':rank,'construction_rows':len(rows),'active_rows':len(selected),'active_to_construction':selected,'published_labels':None}
    return meta,[rows[i-1] for i in selected]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--archive',required=True);ap.add_argument('--out',required=True);ap.add_argument('--members',nargs='+',default=['m11.rk3','m11.rk4']);a=ap.parse_args()
    archive=Path(a.archive);raw=archive.read_bytes()
    if digest(raw)!=ARCHIVE_SHA:raise ValueError('wrong archive')
    out=Path(a.out);out.mkdir(parents=True,exist_ok=True);inventory=[];selected={}
    with tarfile.open(archive) as tf:
        for member in tf.getmembers():
            if not member.isfile() or '.rk' not in member.name:continue
            meta,rows=parse(tf.extractfile(member).read(),member.name);inventory.append(meta)
            if member.name in a.members:selected[member.name]={'metadata':meta,'rows':rows}
    if set(selected)!=set(a.members):raise ValueError('missing requested member')
    (out/'archive_inventory.json').write_text(json.dumps({'archive_sha256':ARCHIVE_SHA,'members':inventory},indent=2)+'\n')
    (out/'selected_inputs.json').write_text(json.dumps(selected,indent=2)+'\n')
    code='L096Inputs:=[\n'
    for name,part in selected.items():
        for active,row in enumerate(part['rows'],1):
            group=name.split('.')[0];order={'m11':7920,'m12':95040,'j1':175560,'j2':604800,'m22':443520,'m23':10200960,'hs':44352000,'j3':50232960}[group]
            code+=f'rec(member:="{name}",active:={active},construction:={part["metadata"]["active_to_construction"][active-1]},expected_order:={order},parabolic_generators:=['
            code+=','.join('['+','.join(g)+']' for g in row)+']),\n'
    code=code.rstrip(',\n')+'\n];;\n';(out/'inputs.g').write_text(code)
    print(json.dumps({k:len(v['rows']) for k,v in selected.items()}))
if __name__=='__main__':main()
