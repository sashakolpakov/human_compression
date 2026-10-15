import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,collections,hashlib,json,re
from pathlib import Path
P=Path(__file__).resolve().parent;G=P.parent
def need(v,s):
    if not v:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def pin(p):
    b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def extract(text):
    begin='  members := [';end='  new_comparison_count :='
    need(text.count(begin)==text.count(end)==1,'unique exact whole-member field')
    content=text.split(begin,1)[1].split(end,1)[0].strip();need(content.endswith('],'),'exact whole-member array delimiter');content=content[:-2].strip()
    pattern=re.compile(r'rec\(\s*generator_images\s*:=\s*\[[0-9\s(),]*\],\s*rank\s*:=\s*([2-5]),\s*source\s*:=\s*\[\s*(\d+)\s*,\s*(\d+)\s*\],\s*target\s*:=\s*\[\s*(\d+)\s*,\s*(\d+)\s*\],\s*type_permutation\s*:=\s*[0-9\s(),]*\)')
    rows=[];last=0
    for m in pattern.finditer(content):
        need(content[last:m.start()].strip() in ['',','],'complete literal record coverage')
        r,a,b,c,d=map(int,m.groups());rows.append(dict(rank=r,representative=[a,b],member=[c,d]));last=m.end()
    need(not content[last:].strip(),'no unparsed trailing record')
    need(len(rows)==145 and len({tuple(r['member'])for r in rows})==145,'exact145 distinct acquired family members')
    need(collections.Counter(r['rank']for r in rows)=={2:21,3:25,4:63,5:36},'complete acquired rank partition')
    return rows
def join(rows,inventory,comparison,models):
    counts=collections.Counter(tuple(r['representative'])for r in rows);bylabel={r['label']:r for r in inventory};result=[]
    need(len(counts)==29 and len(bylabel)==29,'all29 classes')
    used=set()
    for r in comparison:
        ids={q['catalogue_index']for q in r['candidates']};need(len(ids)==1,'accepted unique numerical source join');i=ids.pop();m=models[i];source=tuple(m['source'])
        need(source in counts and source not in used,'one exact class per source row');used.add(source)
        members=[v['member']for v in rows if tuple(v['representative'])==source]
        need(all(v['rank']==m['rank']for v in rows if tuple(v['representative'])==source),'actual family rank')
        expected=bylabel[r['label']]['printed_G_conjugacy_fusion_multiplicity'];actual=counts[source]
        result.append(dict(label=r['label'],catalogue_index=i,representative=list(source),members=members,printed=expected,actual=actual,match=actual==expected))
    need(used==set(counts),'all acquired classes joined');need(all(r['match']for r in result),'literal printed multiplicities all match')
    return result
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output')
    inputs=[G/'incremental_target02/result.g',G/'source_join_component_v2/diagram_inventory02.json',G/'source_join_component_v2/diagram_comparison01.json']+[G/f'palette_serialization_v1/derived/model{i}.json'for i in range(1,30)]
    before=[pin(p)for p in inputs];rows=extract(inputs[0].read_text());result=join(rows,read(inputs[1])['rows'],read(inputs[2])['rows'],{i:read(inputs[i+2])for i in range(1,30)})
    need(before==[pin(p)for p in inputs],'unchanged exact inputs');a.out.mkdir(parents=True);report=dict(status='PASS_ALL29_SOURCE_FUSION_MULTIPLICITIES',rows=result,inputs=before,acquired_family_members=145,equivalence='Inner-conjugacy/type families fused by actual full Aut(G)/type; inherited exact enumeration convention.',target_runs=0,new_group_comparisons=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k not in ['rows','inputs']}))
if __name__=='__main__':main()
