#!/usr/bin/env python3
"""Bounded binding/disposition replay; no primary extraction or scientific execution."""
import argparse,copy,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent
HELD_TOPICS={'Chamber','ChiralEnumeration','Operations'}
HELD_IDS={'L008','L028','N006'}
def require(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def semantics(docs,findings,disp,review,overview):
 ds=docs['documents'];cs=disp['comparisons'];ts=overview['topics']
 require(len(ds)==109 and sum(d['format']=='PDF'for d in ds)==107,'document roster')
 require(sum(d.get('actual_pages',0)for d in ds)==1003,'complete page boundary')
 require(len({d['topic']for d in ds})==18 and all(d['topic']!='F'for d in ds),'screened topic boundary')
 require(len([d for d in ds if d['side']=='source'])==41,'source count')
 require({d['key']for d in ds if d['format']!='PDF'}=={'N001','L108'},'authored renderings')
 require({f['source']for f in findings['findings']}==HELD_IDS,'listing sources')
 require(all('not optional validation' in f['role']or 'not a bounded optional-validation' in f['role']for f in findings['findings']),'actual listing roles')
 expected=[]
 for t in ts:
  expected.append(('whole_topic',t['topic'],t['source_ids'],t['written']))
  expected.extend(('conditional_application',t['topic'],[p['source']],p['conditional'])for p in t['pairs'])
 require(len(expected)==len(cs)==62,'comparison roster')
 for c,(kind,t,ids,value)in zip(cs,expected):
  require((c['kind'],c['topic'],c['source_ids'],c['historical_value'])==(kind,t,ids,value),'historical comparison changed')
  held=t in HELD_TOPICS if kind=='whole_topic' else ids[0]in HELD_IDS
  require(c['current_status']==('WITHHOLD_PENDING_SYMMETRIC_REMEASUREMENT'if held else'RETAIN_UNCHANGED_MANUSCRIPT_COORDINATE'),'incorrect disposition')
 require(sum(c['current_status'].startswith('RETAIN')for c in cs)==56,'retained comparisons')
 require(disp['retained_whole_topics']==16 and disp['retained_individuals']==40,'retained category counts')
 require(disp['software_inclusive_ratios']is None and disp['recovered_originals_unchanged']==43,'unknown or recovery boundary')
 require(review['findings']['old_costs_or_factors_modified']is False,'no cost mutation')
 require(all(review['scope'][k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit','new_full_scientific_reviews']),'credit/role inflation')
 require(all(d['full_graphic_cost']is None for d in ds),'unknown graphic cost')
 return True
def audit(public,study):
 docs=read(R/'documents.json');find=read(R/'listing_findings.json');disp=read(R/'comparison_dispositions.json');review=read(R/'review.json');b=read(R/'bindings.json');ov=read(public/b['overview']['path'])
 semantics(docs,find,disp,review,ov)
 bindings=[b['overview'],b['policy']]+b['measurement_specs']+b['replacement_tex_closure']+[d['file']for d in docs['documents']]
 seen=set();verified=skipped=0
 for x in bindings:
  k=(x['root'],x['path'])
  if k in seen:continue
  seen.add(k);base=public if x['root']=='public' else study
  if base is None:skipped+=1;continue
  p=base/x['path'];require(p.is_file()and p.stat().st_size==x['bytes']and sha(p)==x['sha256'],'binding '+str(p));verified+=1
 if (R/'manifest.json').exists():
  for x in read(R/'manifest.json')['exports']:
   p=R/x['path'];require(p.stat().st_size==x['bytes']and sha(p)==x['sha256'],'local export '+x['path'])
 controls=[]
 def reject(name,fn):
  z=[copy.deepcopy(x)for x in (docs,find,disp,review,ov)];fn(z)
  try:semantics(*z)
  except ValueError:controls.append(name);return
  raise ValueError('control accepted '+name)
 reject('restore held whole comparison',lambda z:z[2]['comparisons'][next(i for i,c in enumerate(z[2]['comparisons'])if c['topic']=='Chamber'and c['kind']=='whole_topic')].update(current_status='RETAIN_UNCHANGED_MANUSCRIPT_COORDINATE'))
 reject('withdraw unaffected N016',lambda z:z[2]['comparisons'][next(i for i,c in enumerate(z[2]['comparisons'])if c['source_ids']==['N016'])].update(current_status='WITHHOLD_PENDING_SYMMETRIC_REMEASUREMENT'))
 reject('change historical numerator',lambda z:z[2]['comparisons'][0]['historical_value'].update(numerator=0))
 reject('invent zero software comparison',lambda z:z[2].update(software_inclusive_ratios=0))
 reject('claim new source credit',lambda z:z[3]['scope'].update(new_source_credit=1))
 reject('delete counted companion',lambda z:z[0]['documents'].pop())
 return {'status':'PASS','binding_files_verified':verified,'private_bindings_skipped':skipped,'documents':109,'PDF_pages':1003,'tex_closure_files':len(b['replacement_tex_closure']),'whole_retained':16,'individual_retained':40,'held_topics':sorted(HELD_TOPICS),'held_individuals':sorted(HELD_IDS),'semantic_controls':controls,'source_extraction_or_scientific_rerun':False}
def main():
 p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--study-root',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args();d=audit(a.public_root,a.study_root);a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d))
if __name__=='__main__':main()
