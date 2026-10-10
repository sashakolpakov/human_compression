"""Post-hoc coarse table comparison, deliberately not a source-label certificate.
The census and shadow reconstruction do not read this table. Refined source
subscripts and colon labels are preserved but not interpreted by this script.
"""
from pathlib import Path
import json, re, collections
ROOT=Path(__file__).resolve().parent
rows=json.loads((ROOT/'phase164_L073_table_contract.json').read_text())['rows']
witnesses=json.loads((ROOT/'phase164_m22_author/phase164_m22_shadow_data.json').read_text())['triples']
orders={'A5':60,'1':1,'2':2,'3':3,'4':4,'22':4,'S3':6,'D8':8,'Q8':8,'23':8,'D10':10,'A4':12,'D12':12,'24':16,'2× D8':16,'232':16,'322':18,'F21':21,'S4':24,'242':32,'2222':16,'2322':32,'324':36,'243':48,'22A4':48,'22D8':32,'2422':64,'24A4':192}
def sig(r):
    m=re.fullmatch(r'M(\d{3})\((.*)\)',r['label_text'])
    if not m: raise ValueError(r)
    return tuple(map(int,m[1]))+tuple(int(v.strip()[0]) for v in m[2].split(','))
by_sig=collections.defaultdict(list)
for w in witnesses:
    for s in w['signatures']: by_sig[tuple(s)].append(w['witness'])
byid={w['witness']:w for w in witnesses}
edges=[]; report=[]
for r in rows:
    candidates=by_sig[sig(r)]
    order=orders[r['Borel_text']]
    compatible=[i for i in candidates if byid[i]['borel_id'][0]==order]
    report.append(dict(r,coarse_signature=sig(r),predicted_borel_order=order,coarse_candidates=candidates,order_compatible_candidates=compatible))
    edges.append(compatible)
match={}
def augment(i,seen):
    for j in edges[i]:
        if j in seen: continue
        seen.add(j)
        if j not in match or augment(match[j],seen):
            match[j]=i;return True
    return False
unmatched=[]
for i in sorted(range(len(rows)),key=lambda i:len(edges[i])):
    if not augment(i,set()): unmatched.append(i+1)
out={'status':'coarse_posthoc_diagnostic_not_full_refined_label_match','matched':len(match),'unmatched_rows':unmatched,'rows':report}
(ROOT/'phase164_m22_coarse_comparison.json').write_text(json.dumps(out,indent=2)+'\n')
print('coarse/order bipartite matching',len(match),'of',len(rows))
for r in report:
    if not r['order_compatible_candidates']: print('NO ORDER MATCH',r['row'],r['label_text'],r['source_number'],r['Borel_text'],'actual',[byid[i]['borel_id'] for i in r['coarse_candidates']])
print('unmatched',unmatched)
