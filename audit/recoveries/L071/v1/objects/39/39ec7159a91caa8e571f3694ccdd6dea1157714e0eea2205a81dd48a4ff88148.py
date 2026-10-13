"""Distinct receipt and complete literal assembly audit; no census is rerun."""
from pathlib import Path
import ast, hashlib, json, re
S = Path('/Users/sasha/medusa/research/leemans')
P = S / 'corpus106_L071_remaining_censuses_v1'
W = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def path(p): return Path(p) if Path(p).is_absolute() else S / p
def pin(row, base=S):
    p = base / row['path']
    assert sha(p) == row['sha256'], str(p)
    if 'bytes' in row: assert p.stat().st_size == row['bytes']
def literal(raw, marker):
    assert raw.count(marker) == 1
    start = raw.index('[', raw.index(marker) + len(marker)); depth=0
    for pos in range(start,len(raw)):
        if raw[pos] == '[': depth += 1
        elif raw[pos] == ']': depth -= 1
        if depth == 0:
            text=raw[start:pos+1]
            assert re.fullmatch(r'[\s\d,()\[\]]+',text)
            return text
    raise AssertionError('unclosed literal')
def tuple_count(text, rank):
    depth=0; count=0; positions=[]; begin=None
    for i,c in enumerate(text):
        if c=='[':
            depth+=1
            if depth==2: begin=i+1
        elif c==']':
            if depth==2:
                row=text[begin:i]; level=0; entries=1 if row.strip() else 0
                for d in row:
                    if d=='(':level+=1
                    elif d==')':level-=1
                    elif d==',' and level==0:entries+=1
                    assert level>=0
                assert level==0 and entries==rank
                positions.append(re.sub(r'\s','',row));count+=1
            depth-=1
        assert depth in (0,1,2)
    assert depth==0 and len(set(positions))==count
    return count
def receipt(p):
    r=json.loads(p.read_text())
    assert r['status']=='EXITED' and r['returncode']==0 and r['complete_marker'] is True and r['unchanged'] is True
    for q in r['pins']:pin(q)
    assert (p.parent/'stderr.log').read_bytes()==b''
    return r
manifest=json.loads((P/'manifest.json').read_text())
assert sha(P/'manifest.json')=='9bd0e3d2ddeecd513ac195eae2bf3db5d2fb3f68eba03747b75e44ecd91e3ee0'
for q in manifest['exports']:pin(q,P)
deps=json.loads((P/'dependencies.json').read_text())
for q in deps['bindings']:pin(q)
queue=json.loads((P/'queue.json').read_text())['models']
execution=json.loads((P/'executions.json').read_text())['models']
assert len(queue)==len(execution)==20
expected_bench={'A5':(3,1,2),'PGammaL2_9':(21,3,12),'S7':(81,7,44),'PSL2_25':(30,4,17),'PSigmaU3_3':(60,2,31),'PGL2_27':(190,6,98),'M12':(67,7,37),'J1':(300,0,150),'A9':(84,10,47),'S9':(352,12,182)}
expected_spor={'M11':{},'M12':{3:40,4:27},'J1':{3:296,4:4},'M22':{},'J2':{3:261,4:31},'M23':{},'HS':{3:465,4:111,5:4},'M24':{3:946,4:310,5:4},'McL':{},'He':{3:2292,4:145},'J3':{3:584,4:2},'Tits':{3:468,4:57}}
names={'M11':'m11','M12':'m12','J1':'j1','M22':'m22','J2':'j2','M23':'m23','HS':'hs','M24':'m24','McL':'mcl','Tits':'ti','He':'he','J3':'j3'}
rows=[]; source_rows=[]
for model,x in zip(queue,execution):
    name=model['name']; assert name==x['name']
    D=path(x['census_receipt']['path']).parent;V=path(x['validation_receipt']['path']).parent
    cr=receipt(D/'report.json');vr=receipt(V/'report.json');limit=model['order'].bit_length()-1
    assert cr['name']==vr['name']==name and vr['rank_limit']==x['rank_limit']==limit
    assert sha(V/'model.g')==model['model_sha256']
    raw=(D/'stdout.log').read_text();valid=(V/'stdout.log').read_text()
    assert raw.count('COMPLETE_EXHAUSTION')==valid.count('COMPLETE_REMAINING_MODEL_VALIDATION')==1
    h=re.search(r'MODEL (\w+) ORDER (\d+) AUT_ORDER (\d+)',raw);assert h[1]==name and int(h[2])==model['order']
    ranks=list(map(int,re.findall(r'COMPLETE_TUPLES_RANK_(\d+) ',raw)))
    assert ranks==list(range(1,limit+1))
    summary=[tuple(map(int,m)) for m in re.findall(r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)',raw)]
    assert [r[0] for r in summary]==ranks
    assembled='recordedMarks:=[];;\n'; byrank={}; types={}
    for rank,ordered,selfdual,dual,con,cons,cond in summary:
        text=literal(raw,f'COMPLETE_TUPLES_RANK_{rank} ')
        assert tuple_count(text,rank)==ordered
        assert ordered+selfdual==2*dual and con+cons==2*cond
        assert 0<=selfdual<=ordered and 0<=cons<=con<=ordered
        assembled+=f'recordedMarks[{rank}]:='+text+';;\n'
        byrank[rank]=ordered
        tv=ast.literal_eval(literal(valid,f'VERIFIED_TYPE_COUNTS {rank} '))
        assert all(len(typ)==rank-1 and all(a>=2 for a in typ) and count>0 for typ,count in tv)
        assert sum(count for typ,count in tv)==ordered
        assert sum(count for typ,count in tv if all(a>2 for a in typ))==con
        types[rank]=tv
    assert assembled+'reportedCounts:='+json.dumps([r[1] for r in summary])+';;\n'==(V/'records.g').read_text()
    total=sum(byrank.values());assert total==vr['recorded_tuples']==x['ordered_classes']
    assert re.findall(r'VALIDATED_MODEL (\w+) TUPLES (\d+) RANK_LIMIT (\d+)',valid)==[(name,str(total),str(limit))]
    csd=tuple(sum(r[j] for r in summary) for j in (1,2,3))
    if name in expected_bench:assert csd==expected_bench[name]
    if name in expected_spor:assert {r:c for r,c in byrank.items() if c}==expected_spor[name]
    rows.append(dict(name=name,rank_limit=limit,ordered=total,self_dual=csd[1],duality=csd[2],rank_counts=byrank,types=types,census_sha256=sha(D/'report.json'),validation_sha256=sha(V/'report.json'),literal_reconstruction_byte_exact=True,all_pins_valid=True,stderr_empty=True))
    if name in names:
        C=S/'reboot_20261013/L071_source_comparison01'/name
        assert (C/'records.g').read_text()==assembled
        src=S/'reboot_20261013/L071_census_preparation/source_sporpolys/sporpolys'/(names[name]+'.gap')
        statements=[a.strip() for a in src.read_text().split(';;') if a.strip()]
        assert statements[:2]==['gens := []',names[name]+' := []']
        gens=[];tuples=[]
        for statement in statements[2:]:
            if statement.startswith('Add(gens,'):
                m=re.fullmatch(r'Add\(gens,([\s\d,()]+)\)',statement);assert m;gens.append(m[1])
            else:
                m=re.fullmatch(r'Add\('+names[name]+r',\[(gens\[\d+\](?:,gens\[\d+\])*)\]\)',statement);assert m
                indices=list(map(int,re.findall(r'gens\[(\d+)\]',m[1])));assert all(1<=i<=len(gens) for i in indices);tuples.append(indices)
        code='sourceGens:=['+','.join(gens)+'];;\nsourceTuples:=['+','.join('['+','.join(f'sourceGens[{i}]' for i in t)+']' for t in tuples)+'];;\n'
        assert code==(C/'source.g').read_text()
        assert len(tuples)==total
        out=(C/'stdout.log').read_text()
        matched=[tuple(map(int,m)) for m in re.findall(r'SOURCE_MATCH\s+(\d+)\s+LEAF\s+\[\s*(\d+)\s*,\s*(\d+)\s*\]\s+TRANSPORTER',out)]
        assert [m[0] for m in matched]==list(range(1,total+1))
        assert {m[1:] for m in matched}=={(r,i) for r,count in byrank.items() for i in range(1,count+1)}
        assert all(len(tuples[i-1])==r for i,r,j in matched)
        source_rows.append(dict(name=name,generators=len(gens),source_markings=total,all_target_leaf_coordinates_covered=True,source_literal_reconstructed_byte_exact=True,source_sha256=sha(src)))
assert sum(r['ordered'] for r in rows)==6868
assert sum(r['source_markings'] for r in source_rows)==6047
assert {r['name'] for r in rows if r['ordered']==0}=={'M11','M22','M23','McL'}
report=dict(status='PASS_DISTINCT_COMPLETE_ASSEMBLY_AUDIT',author_manifest_sha256=sha(P/'manifest.json'),author_exports_checked=len(manifest['exports']),external_bindings_checked=len(deps['bindings']),groups=20,all_ordered_tuples=6868,source_groups=12,source_tuples=6047,rows=rows,source_rows=source_rows,whole_original_credit=0,no_group_census_or_full_IP_execution_repeated=True)
(W/'check_report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('rows','source_rows')}))
