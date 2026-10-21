"""Literal native preprint transcription, kept distinct from computed data."""
import sys
if not __debug__:raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse,hashlib,itertools,json
from endpoint_comparison import compare_endpoints
from pathlib import Path
W=Path(__file__).resolve().parent;S=W.parents[2]
parser=argparse.ArgumentParser();parser.add_argument('--out',type=Path,required=True);args=parser.parse_args()
OUT=args.out.absolute()
if OUT.exists():raise ValueError('fresh output required')
OUT.mkdir(parents=True)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),sha256=hashlib.sha256(b).hexdigest(),bytes=len(b))
# Node syntax position:size:printed_panel_order:boxed_kernel_order.
nodes={
'2.1':'L:21:4:16 R:21:4:16','2.2':'L:210:14:4 R:56:3:1','2.3':'L:56:1:1 R:280:9:36','2.4':'L:120:7:1 R:120:7:1',
'2.5':'L:210:6:4 R:120:3:1','2.6':'L:280:8:1 R:280:8:1','2.7':'L:280:1:1 R:1260:8:8',
'3.1':'L:21:1:1 C:210:4:4 R:56:3:1','3.2':'L:56:1:1 C:1260:8:4 R:56:1:1',
'3.3':'T:120:1:1 L:210:2:4 R:210:2:4','3.4':'T:56:1:1 L:210:2:4 R:210:2:4','3.5':'T:1120:6:3 L:120:1:1 R:120:1:1',
'3.6':'L:56:3:1 C:210:2:1 R:56:3:1','3.7':'L:21:3:1 C:105:4:4 R:21:3:1',
'4.1':'L:21:1:1 C:210:1:1 U:56:3:1 D:56:3:1','4.2':'L:56:1:1 C:1260:4:2 U:21:1:1 D:21:1:1',
'4.3':'L:120:1:1 C:1260:2:2 U:56:1:1 D:56:1:1','4.4':'L:21:1:1 C:1260:2:2 U:56:1:1 D:56:1:1',
'4.5':'L:56:1:1 C:1260:2:2 U:21:1:1 D:21:1:1','4.6':'L:120:1:1 C:1260:2:2 U:21:1:1 D:56:1:1',
'4.7':'L:120:1:1 C:1260:2:2 U:21:1:1 D:21:1:1','4.8':'TL:56:3:1 TR:21:1:1 BL:21:1:1 BR:56:3:1',
'4.9':'TL:56:1:1 TR:21:2:1 BL:210:2:1 BR:56:1:1','4.10':'TL:21:2:1 TR:56:1:1 BL:56:1:1 BR:210:2:1',
'4.11':'TL:120:1:1 TR:120:1:1 BL:336:2:1 BR:336:2:1',
'5.1':'TL:21:2:1 TR:56:1:1 BL:56:1:1 BC:210:2:1 R:21:1:1',
'5.2':'TL:21:2:1 TR:56:1:1 BL:56:1:1 BC:210:2:1 R:21:1:1',
'5.3':'TL:21:1:1 TR:56:1:1 BL:21:1:1 BR:56:1:1 R:21:2:1',
'5.4':'TL:21:1:1 TR:56:1:1 BL:21:1:1 BR:56:1:1 R:21:2:1'}
# Every visible edge is listed; absent pairs are separately retained as absent.
# C-right/left/up/down records the visual opening of the printed circular symbol,
# not a claimed geometric identification. Numeric triple is ordered by endpoints.
edges={
'2.1':'L,R,single','2.2':'L,R,4/3/4','2.3':'L,R,5/4/6','2.4':'L,R,4/3/4',
'2.5':'L,R,6/3/5','2.6':'L,R,5/3/5','2.7':'L,R,9/5/10',
'3.1':'L,C,C-right C,R,Af*','3.2':'L,C,C-right C,R,C-left','3.3':'T,L,C-left T,R,C-right L,R,single',
'3.4':'T,L,C-left T,R,C-right L,R,double','3.5':'T,L,C-right T,R,C-left L,R,single',
'3.6':'L,C,6/3/5 C,R,5/3/6','3.7':'L,C,Af C,R,Af*',
'4.1':'L,C,single C,U,C-right C,D,C-right','4.2':'L,C,C-right C,U,C-left C,D,C-left',
'4.3':'L,C,double C,U,C-left C,D,C-left','4.4':'L,C,double C,U,C-left C,D,P*',
'4.5':'L,C,P C,U,C-left C,D,P*','4.6':'L,C,P C,U,C-left C,D,C-left','4.7':'L,C,P C,U,C-left C,D,C-left',
'4.8':'TL,TR,C-left TL,BL,C-up TR,BR,C-down BL,BR,C-right BL,TR,single',
'4.9':'TL,TR,C-right TL,BL,P TR,BR,C-up BL,BR,P*',
'4.10':'TL,TR,C-left TL,BL,C-up TR,BR,C-down BL,BR,P',
'4.11':'TL,TR,single TL,BL,C-down TR,BR,C-down BL,BR,single',
'5.1':'TL,TR,C-left TL,BL,C-up TR,BC,single BL,BC,5 BC,R,single',
'5.2':'TL,TR,C-left TL,BL,C-up TR,BC,5 BL,BC,5 BC,R,single',
'5.3':'TL,TR,5 TL,BL,single BL,BR,5 TL,BR,5 BL,TR,5 TR,R,C-right BR,R,C-right',
'5.4':'TL,TR,5 TL,BL,single BL,BR,single TL,BR,single BL,TR,5 TR,R,C-right BR,R,C-right'}

def gonality(label):
 if label=='double':return 4
 if label in ['P','P*','5']:return 5
 if '/'in label:return int(label.split('/')[1])
 return 3

old=json.loads((W/'diagram_inventory01.json').read_text());rows=[]
not2t={'2.2','3.2','3.5','4.2','4.11','5.1','5.2','5.3','5.4'}
for q in old['rows']:
 label=q['label'];ns=[]
 for token in nodes[label].split():
  p,s,o,k=token.split(':');ns.append(dict(position=p,type_size=int(s),printed_panel_order=int(o),printed_kernel_order=int(k)))
 es=[]
 for token in edges[label].split():
  u,v,g=token.split(',');es.append(dict(nodes=[u,v],printed_label=g,conventional_gonality=gonality(g)))
 pairs={frozenset(x['nodes']) for x in es}
 rows.append(q|dict(nodes=ns,edges=es,absent_edges=[list(p)for p in itertools.combinations([n['position']for n in ns],2)if frozenset(p)not in pairs],
                   printed_local_2T_marker=label not in not2t,status='EXACT_NATIVE_TRANSCRIPTION_NOT_CONSTRUCTION_IDENTITY'))
identity=json.loads((S/'corpus161_access_supplement_v4/L100_whole_source_reading.json').read_text())
out=dict(status='NATIVE_PREPRINT_NODE_EDGE_TRANSCRIPTION_V3',rows=rows,source=old['source'],
 documentary_identity={k:identity[k]for k in ['edition','journal_target','edition_limit','downloaded_source','derived_pdf']},
 documentary_record=pin(S/'corpus161_access_supplement_v4/L100_whole_source_reading.json'),
 superseded_working_inventory=pin(W/'diagram_inventory01.json'),
 delta='Preserves the prior local2T marker correction; restores the source3.5 horizontal single bond after distinct review and compares both ordered endpoint eccentricities for every numerical triple.',
 qualifications=['Unboxed kernel recorded as order1; abstract group structure is not inferred from this number.',
 'Printed positions are visual, not inherited construction type numbers. Every subsequent type map must be explicit.',
 'Source3.5 has a single horizontal bottom bond; v1 incorrectly omitted it. Source5.1/5.2 print panel order2 at their210-object node.',
 'No claim of textual identity with, or error in, the unobtained25-page2003 journal edition.'],
 native_inputs=[pin(W/'native'/f'high-{i:02d}.png')for i in range(1,8)],source_credit=0)
(OUT/'diagram_inventory02.json').write_text(json.dumps(out,indent=2)+'\n')
actual=json.loads((W/'literal_diagrams01/diagrams.json').read_text());joins=[]
for q in rows:
 candidates=[];ns=q['nodes'];se={frozenset(e['nodes']):e['conventional_gonality']for e in q['edges']}
 for d in actual['records']:
  if sorted(n['type_size']for n in ns)!=sorted(d['type_sizes']):continue
  ae={frozenset(p['types']):p['gonality']for p in d['pairs']}
  for perm in itertools.permutations(range(len(ns))):
   if any(n['type_size']!=d['type_sizes'][t] for n,t in zip(ns,perm)):continue
   mismatches=[]
   for n,t in zip(ns,perm):
    for k,got in [('printed_panel_order',d['panel_orders'][t]),('printed_kernel_order',d['local_action_kernels'][t]['order'])]:
     if n[k]!=got:mismatches.append(dict(kind=k,node=n['position'],printed=n[k],actual=got))
   for i,j in itertools.combinations(range(len(ns)),2):
    p=[ns[i]['position'],ns[j]['position']];printed=se.get(frozenset(p),2);got=ae[frozenset([perm[i]+1,perm[j]+1])]
    if printed!=got:mismatches.append(dict(kind='gonality',nodes=p,printed=printed,actual=got))
   endpoint_checks,endpoint_mismatches=compare_endpoints(q,d,perm);mismatches.extend(endpoint_mismatches)
   if q['printed_local_2T_marker']!=all(d['panel_two_transitive']):mismatches.append(dict(kind='local_2T_marker',printed=q['printed_local_2T_marker'],actual=all(d['panel_two_transitive'])))
   candidates.append(dict(catalogue_index=d['index'],source_node_to_catalogue_type={n['position']:t+1 for n,t in zip(ns,perm)},mismatches=mismatches,ordered_endpoint_checks=endpoint_checks))
 score=min(len(c['mismatches'])for c in candidates);best=[c for c in candidates if len(c['mismatches'])==score]
 joins.append(dict(label=q['label'],minimum_mismatches=score,candidates=best,
                   scope='Matching documented invariants only, not a general theorem that diagrams determine geometry.'))
(OUT/'diagram_comparison01.json').write_text(json.dumps(dict(status='EXPLICIT_SOURCE_DIAGRAM_COMPARISON',rows=joins,inputs=[pin(OUT/'diagram_inventory02.json'),pin(W/'literal_diagrams01/diagrams.json')],source_credit=0),indent=2)+'\n')
for x in joins:print(x['label'],sorted({y['catalogue_index']for y in x['candidates']}),x['minimum_mismatches'])
