"""Reconcile fixed historical claims using independently chosen source invariants.
Accepted old shadow decisions are reused; no claim value selects a candidate.
Working author reconstruction, not yet an admission.
"""
from pathlib import Path
import argparse,json,collections,hashlib,itertools
B=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,default=B.parent)
ap.add_argument('--out',type=Path,default=B/'label_reconciliation.json');args=ap.parse_args()
S=args.study_root
read=lambda p:json.loads(p.read_text())
rows={};files={}
mm=S/'topic_D_L096_extended_candidate/mathieu_results.json'
for g in ['M11','M12']:rows[g]=[r for r in read(mm)['rows'] if r['member'].startswith(g.lower())];files[g]=mm
for g in ['M22','M23','J2','J1','HS','J3']:
 f=S/f'topic_D_L096_{g}_extension'/('shadow_results.json' if g in ['HS','J3'] else 'results.json')
 rows[g]=read(f)['rows'];files[g]=f
profiles=read(B/'transcribed_profiles.json')['profiles'];claims=read(S/'topic_D_L096_volume_v2/historical_label_claims.json')['claims']
# Parsed full bounded certificate; neither input selection nor these invariants
# consults any IP/WIP decision. The separate replay binds this record to stdout.
new_invariants={}
for r in read(B/'label_invariants.json')['records']:
 new_invariants.setdefault(r['group'],{})[r['member'],r['active_row']]=r
def panels(r):
 ans=[]
 for res in r['residues']:
  if res['residue_rank']==1:
   i=res['types'][0]-1;ans.append((r['order']//r['parabolic_orders'][i],res['panel_size']-1))
 return sorted(ans)

def candidates(p):
 hits=[]
 for r in rows[p['group']]:
  ss=[r['order']//h for h in r['parabolic_orders']]
  if sorted(ss)!=sorted(p['type_sizes']):continue
  if p['borel'] is not None and p['borel']!=r['borel_order']:continue
  if 'panel_orders' in p:
   if panels(r)!=sorted(zip(p['type_sizes'],p['panel_orders'])):continue
  ii=new_invariants.get(p['group'],{}).get((r['member'],r['active_row']),{})
  if 'source_correlation_type_swap' in p and ii.get('source_correlation_type_swap')!=p['source_correlation_type_swap']:continue
  if 'central_type_swap' in p and ii.get('central_type_swap')!=p['central_type_swap']:continue
  if 'residue_discriminator' in p and ii.get('residue_girth')!=p['residue_discriminator']['girth']:continue
  hits.append(r)
 return hits

def tag(r):return {'member':r['member'],'active_row':r['active_row'],'construction_row':r['construction_row'],'literal_input_row':r.get('literal_input_row')}
out=[];index={}
for p in profiles:
 hit=candidates(p)
 if not hit:raise ValueError(('empty source-compatible family',p['group'],p['label']))
 row={**p,'candidate_fibre':[tag(r) for r in hit],'identification':'UNIQUE_RETAINED_CLASS' if len(hit)==1 else 'ALL_MATCHING_CLASSES_PRESERVED','global_classification':'retained source completeness for HS/J3; exact accepted complete prior census for other groups, not recomputed here'}
 out.append(row);index[p['group'],p['label']]=hit
cc=[]
for c in claims:
 hit=index.get((c['group'],c['label']),[]);vals=[]
 for r in hit:
  if c['property_rank']=='full':ip,wp=r['IP'],r['WIP']
  else:
   z=next(z for z in r['by_rank'] if z['rank']==c['property_rank']);ip,wp=z['IPk'],z['WIPk']
  vals.append({'input':tag(r),'IP':ip,'WIP':wp,'agrees':ip if c['claim']=='IP' else wp and not ip})
 cc.append({**c,'candidate_decisions':vals,'status':'AWAITING_PRIMARY_NAME_BINDING' if not vals else 'CONFIRMED_ON_EVERY_COMPATIBLE_CLASS' if all(x['agrees'] for x in vals) else 'SOURCE_PROPERTY_DISCREPANCY'})
for c in cc:
 if c['status']=='AWAITING_PRIMARY_NAME_BINDING':
  if (c['group'],c['label'])!=('J1','4.1'):raise ValueError('unaccounted name')
  c['status']='ORDINAL_UNVERIFIED_CORRECTED_PROFILE_CLASSIFICATION'
  c['corrected_statement']='Among the complete two rank-four J1 classes, type-size profile {266,1463,1463,2926} has full IP, while {266,266,1463,2926} fails WIP3 and WIP4; no assertion of literal ordinal identity.'
j1=[{**tag(r),'type_sizes':sorted(r['order']//h for h in r['parabolic_orders']),'borel_order':r['borel_order'],'by_rank':r['by_rank'],'IP':r['IP'],'WIP':r['WIP']} for r in rows['J1']]
report={'status':'AUTHOR_COMPLETE_CORRECTED_PRINCIPAL_RECONCILIATION_PENDING_DISTINCT_REVIEW','profiles':out,'claims':cc,'counts':dict(collections.Counter(x['status'] for x in cc)),'J1_complete_profile_classification':j1,'literal_historical_name_equivalence':False,'no_shadow_or_census_rerun':True,'retained_files':[{'path':str(p.relative_to(S)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files.values()))]}
args.out.write_text(json.dumps(report,indent=2)+'\n')
print(report['counts'])
for c in cc:
 if c['status']=='SOURCE_PROPERTY_DISCREPANCY':print(c['group'],c['label'],c['property_rank'],c['claim'],[(v['input']['active_row'],v['IP'],v['WIP']) for v in c['candidate_decisions']])
