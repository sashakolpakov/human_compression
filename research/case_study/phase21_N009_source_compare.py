#!/usr/bin/env python3
"""Compare a complete rank-four kernel census to N009's primary type counts.
No group enumeration is performed here. The input is the exact GAP result.
"""
import argparse, collections, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--accepted',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args()
rows=json.loads(a.accepted.read_text())
assert len(rows)==199 and len({tuple(r[0]) for r in rows})==199
expected={(4,4,4):4,(4,4,8):10,(4,4,16):4,(4,4,32):2,
 (4,8,4):14,(4,8,8):24,(4,8,16):10,(4,16,4):4,
 (4,16,8):12,(4,32,4):3,(8,4,8):4,(8,4,16):4,(8,8,8):10}
ordered=collections.Counter();fixed=collections.Counter()
for kernel,typ,cl,kt,selfdual,facets in rows:
    assert len(typ)==3 and min(typ)>=4 and cl<=5
    assert len(facets)==2 and all(1024%f==0 for f in facets)
    assert selfdual in (True,False)
    t=min(tuple(typ),tuple(reversed(typ)))
    ordered[t]+=1
    if selfdual:
        assert typ==list(reversed(typ)) and facets==list(reversed(facets))
        fixed[t]+=1
assert set(ordered)==set(expected)
comparison=[]
for t,count in expected.items():
    assert (ordered[t]+fixed[t])%2==0
    actual=(ordered[t]+fixed[t])//2
    assert actual==count,(t,actual,count)
    comparison.append(dict(type=list(t),ordered=ordered[t],reversal_fixed=fixed[t],up_to_reversal=actual,source_count=count))
special=[r for r in rows if r[1]==[4,4,4] and r[5]==[128,64]]
assert len(special)==2
assert sum(fixed.values())==11 and sum(expected.values())==105
out={'status':'PASS','source':'N009 Table6 printed pp14–17; Theorem5.5 printed p20',
 'source_pdf_sha256':'0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda',
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'accepted_sha256':hashlib.sha256(a.accepted.read_bytes()).hexdigest(),
 'ordered_markings':len(rows),'reversal_fixed':sum(fixed.values()),'up_to_reversal':sum(expected.values()),
 'type_comparison':comparison,'theorem55_oriented_markings':special,
 'scope':'Exact arithmetic/source comparison of the supplied complete GAP census. The normal-kernel enumeration and IP are verified separately; source facet labels and all raw presentation tables are not compared here.'}
a.output.write_text(json.dumps(out,indent=2)+'\n')
print('PASS all 13 canonical type counts; 199 ordered, 11 reversal-fixed, 105 classes; exactly two oriented Theorem5.5 markings.')
