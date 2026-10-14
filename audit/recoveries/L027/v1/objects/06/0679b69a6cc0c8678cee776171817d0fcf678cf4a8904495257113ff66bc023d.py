"""Verify exact synthesis interfaces, not the underlying mathematical proofs."""
import sys
if sys.flags.optimize: raise RuntimeError('unoptimized execution required')
import hashlib,json
from pathlib import Path

def need(b,msg):
 if not b:raise ValueError(msg)
def load(p):return json.loads(p.read_text())
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify_pin(roots,x):
 p=roots[x['namespace']]/x['path'];need(pin(p)=={k:x[k]for k in ('bytes','sha256')},'binding '+str(p));return p

def old_psl2_list():
 """Apply only the exact acquired Topic E classification to this fixed list."""
 values=[4,5,7,9,11,23,27,43,47,67,81,83];out=[]
 for q in values:
  if q in (4,5,9):r=dict(q=q,exists=False,route='acquired small boundary')
  elif q==27:r=dict(q=q,exists=False,route='q=3^3, q=3 mod4, odd prime-power degree3')
  elif q==81:
   p,d,k=3,4,40;proper=[p**e+s for e in range(1,d)for s in (-1,1)]
   need(k>2 and k%2==0 and (q-1)//2%k==0 and all(x%k for x in proper),'pointed construction hypotheses')
   r=dict(q=q,exists=True,route='acquired pointed construction',p=p,d=d,k=k,type=[40,40,40],excluded_orders=proper)
  else:
   need(q%4==3 and all(q%a for a in range(2,int(q**.5)+1)),'listed odd prime')
   sq={a*a%q for a in range(1,q)};roots=[a for a in range(q)if a*a%q==5]
   counts=[]
   for t in roots:
    inv2=pow(2,-1,q)
    counts.append([int(2 in sq and (1+t)%q in sq),int((7+5*t)*inv2%q in sq),int((3+2*t)%q in sq)])
   need(not any(any(r)for r in counts),'negative prime classification')
   r=dict(q=q,exists=False,route='acquired exceptional prime criterion',square_roots_of_five=roots,square_counts=counts)
  out.append(r)
 need([r['q']for r in out if r['exists']]==[81],'exact quoted-list correction')
 return out

def verify(P,roots,source_map=None,retained=None,scope=None):
 sm=source_map if source_map is not None else load(P/'source_map.json');rt=retained if retained is not None else load(P/'retained_inputs.json');sc=scope if scope is not None else load(P/'scope.json');cs=load(P/'components.json')
 need(sm['original']==sc['original']=='L027','original identity')
 need(sc['whole_original_credit']==sc['new_question_credit']==sc['new_Lean_credit']==sc['new_measurements']==0,'no admission/extra phase credit')
 expected=['rank_four','rank_five','even_subgroups','odd_four','rank_obstruction','odd_three','table_one','unitary_examples']
 need([c['id']for c in cs['components']]==expected,'eight actual component scopes')
 checks=0
 for c in cs['components']:
  need(c['status']=='ACCEPTED_BOUNDED_COMPONENT','component acceptance scope')
  for x in [c['author_manifest'],c['manuscript'],c['pdf']]+[y['manifest']for y in c['accepted_by']]:verify_pin(roots,x);checks+=1
  need(c['accepted_by'][0]['role']=='root_acceptance','root acceptance')
  text=verify_pin(roots,c['manuscript']).read_text();need('\\title{'+c['title']+'}'in text,'actual title')
 ids=[r['id']for r in sm['clauses']];need(len(ids)==len(set(ids))==56,'complete unique clause roster')
 numbered=['T1.1','T1.2','T1.3','L2.1','L2.2','L2.3','T5.1','T5.2','T5.3','T5.4','T5.5','T5.6','L6.1','T6.1','L6.2']
 need([r['id']for r in sm['clauses']if r['kind']=='numbered']==numbered,'all15 numbered statements')
 tables=['Table1']+[f'Table2.{i}'for i in range(1,7)]+[f'Table3.{i}'for i in range(1,15)]
 need([r['id']for r in sm['clauses']if r['kind']=='table']==tables,'all21 table row interfaces')
 known=set(expected+['topic_e','L045']+[x['id']for x in rt['records']])
 for r in sm['clauses']:
  need(all(x in known for x in r['route']),'unresolved route '+r['id'])
  need(r['source_physical_pages'] and all(type(x)is int and 1<=x<=25 for x in r['source_physical_pages']),'source page')
  need(r['route']or r['id']=='Q.unitary','unpaid source clause')
 by={r['id']:r for r in sm['clauses']};rr={r['id']:r for r in rt['records']}
 for id in ('R7','R8','R9'):
  need(rr[id]['evidence_status'].startswith('SOURCE_ATTRIBUTED_PRIOR_'),'historical computation promoted to independent census')
 need(rr['R4']['evidence_status']=='SOURCE_ATTRIBUTED_PRIOR_CLASSIFICATION','prior projective rank3 census boundary')
 need(by['S7.psu17']['route']==['unitary_examples']and by['S7.psu17']['qualification']=='No type-exhaustion claim or all-rank census.','positive examples scope')
 need(by['S7.psl2_list']['disposition']=='CORRECTED_BY_PREVIOUSLY_ACQUIRED_RESULT' and 'q81'in by['S7.psl2_list']['qualification'],'literal q81 correction')
 need(by['Q.unitary']['disposition']=='RECORDED_WITHOUT_CURRENT_STATUS_CLAIM' and by['Q.psl2']['disposition']=='ALREADY_RESOLVED_BY_ACQUIRED_PROJECT_RESULT','historical question scope')
 need(by['Table3.7']['disposition']=='PROVED_WITH_CORRECTIONS','generic affine types')
 need(by['Table2.5']['disposition']==by['Table3.10']['disposition']=='GROUPS_PROVED_PRIOR_TYPE_CLASSIFICATION_RETAINED','rank3 inherited type classifications')
 old=old_psl2_list();need(old==load(P/'psl2_context_expected.json'),'exact prior-theorem arithmetic interface')
 return dict(components=8,numbered_statements=15,table_rows=21,total_source_clauses=56,retained_inputs=len(rr),component_binding_checks=checks,quoted_psl2_values=len(old),quoted_psl2_corrections=[81],new_group_enumerations=0)
