import itertools,json,sys
if not __debug__:raise SystemExit('normal Python required')
from pathlib import Path
x=[sum(1<<i for i in pair)for pair in itertools.combinations(range(5),2)]
if x==sorted(x)or len(x)!=len(set(x))or sorted(x)!=sorted(set(x)):raise ValueError('literal combination/mask order control')
r=dict(status='PASS_DISTINCT_COMBINATION_AND_MASK_ORDERS',masks=x,ascending_masks=sorted(x),original_order_differs=True,duplicate_free=True)
p=Path(__file__).with_name('ordering_control_report.json')
if p.exists():raise ValueError('fresh report')
p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
