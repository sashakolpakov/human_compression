#!/usr/bin/env python3
"""Independent F fractions/boundaries; reads accepted counts, not source PDFs."""
import argparse,copy,decimal,hashlib,json,math,pathlib
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected'];FORMS=['NFC','NFKC']
PIN_INPUT='0dfc2fce16d8c532a1cdd9b8f61c1d9391c15099091e795cbba56bde30501620'
PIN_REVIEW='91ac8430736283e6719bcb3cb4e1245cb2576a38608283b4fd207c1009a0247b'
PIN_ADOPTION='f5a71b94d9fe202cd6dfdff92c7ec7002cf490092a31d3d78080e390d2e3053d'
PIN_NUMERICAL='5b484a181ae264984753bfe7c04e702dd38fad3e8ef3b532f9cb6a10dece1326'
def need(b,s):
 if not b:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def bind(p,pin):
 need(sha((p/'manifest.json').read_bytes())==pin,'accepted input manifest')
 for r in load(p/'manifest.json')['exports']:
  b=(p/r['path']).read_bytes();need(len(b)==r['bytes'] and sha(b)==r['sha256'],'accepted file binding '+r['path'])
def rational(n,d):
 need(type(n) is int and type(d) is int and n>0 and d>0,'positive integer ratio');g=math.gcd(n,d)
 with decimal.localcontext() as ctx:
  ctx.prec=60;z=decimal.Decimal(n)/decimal.Decimal(d);s=format(z,'.12f')
 return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=s)
def check(result,counts):
 need(result['source_ids']==['L014'] and result['source_records']==25,'fixed source contract')
 need(result['documents']==['L014','U_F','F1','CODE'] and result['physical_pages']==[12,4,5,4],'whole document inventory')
 need(result['coordinate_count']==30 and result['exact_fraction_count']==120 and result['combined_fractions']==90 and result['conditional_fractions']==30,'coordinate summary')
 rows=result['coordinates'];need(len(rows)==30,'coordinate list');bykey={}
 rawkeys=['complete_validation_programs','complete_operational_drivers','complete_formal_files']
 for row in rows:
  k=(row['variant'],row['normalization'],row['unit']);need(k not in bykey,'duplicate coordinate');bykey[k]=row
 need(set(bykey)=={(a,b,c) for a in VARIANTS for b in FORMS for c in UNITS},'full coordinate product')
 audits=[]
 for k,row in bykey.items():
  variant,form,unit=k;c={doc:counts['documents'][doc]['variants'][variant][form][unit] for doc in ['L014','U_F','F1','CODE']}
  raw={name:sum(v['metrics'][form][unit] for v in counts[name].values()) for name in rawkeys}
  need(c==row['costs'] and raw==row['raw_costs'],'all complete document and raw costs')
  n,u,a,code=[c[t] for t in ['L014','U_F','F1','CODE']]
  expected={'written':rational(n,u+a),'including_printed_validation':rational(n,u+a+code),'including_raw_validation':rational(n,u+a+raw['complete_validation_programs']),'conditional_application':rational(n,a)}
  need(row['comparisons']==expected,'exact complete denominators/reductions/rounded decimals')
  need(row['acquired_common']==u and row['acquired_printed_validation']==code and row['acquired_raw_validation_alternative']==raw['complete_validation_programs'],'conditional acquisition')
  audits.append(dict(variant=variant,normalization=form,unit=unit,comparisons=expected))
 primary=bykey['calibrated_selected','NFC','characters_without_whitespace'];need(result['primary']==primary,'designated primary')
 b=result['boundary']
 for key,value in {'whole_source_and_applications':True,'whole_common_once':True,'cross_topic_discount':False,'required_uniform_proof_programs':0,'complete_validation_programs':3,'separate_operational_drivers':2,'separate_Lean_files':1,'scoped_Lean_declarations':5,'retained_CP_fulltext_cost':None,'retained_external_cost':None,'source_graphics_layout_cost':None,'historical_program_cost':None,'mathematical_complexity_claim':False,'sawtooth_claim':False}.items():need(b[key]==value,'boundary '+key)
 need(b['program_representations']=='Whole printed appendix or three complete raw files; alternatives, never both.','program representation')
 need(b['conditional']=='After acquiring the whole common paper and complete declared validation package; validation is not a mathematical premise.','conditional scope')
 need(b['source_contract_qualification']=='Declared corrected principal results; not recovery of every printed auxiliary assertion.','source exclusion qualification')
 need(all(result[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']) and result['primary_material_exported'] is False,'no new credit or primary export')
 need(result['input_manifests']==dict(inputs=PIN_INPUT,input_review=PIN_REVIEW,input_adoption=PIN_ADOPTION),'input acceptance chain')
 return audits

def controls(result,counts):
 out=[]
 def reject(name,fn):
  bad=copy.deepcopy(result);fn(bad)
  try:check(bad,counts)
  except (ValueError,KeyError,IndexError) as e:out.append(dict(name=name,rejected=True,reason=str(e)));return
  raise ValueError('corruption accepted '+name)
 reject('drop a coordinate',lambda d:d['coordinates'].pop())
 reject('repeat a coordinate',lambda d:d['coordinates'].__setitem__(1,copy.deepcopy(d['coordinates'][0])))
 def denominator(d,kind,delta):
  r=d['coordinates'][0]['comparisons'][kind];r.update(rational(r['numerator'],r['denominator']+delta))
 reject('omit whole common paper',lambda d:denominator(d,'written',-d['coordinates'][0]['costs']['U_F']))
 reject('double count common paper',lambda d:denominator(d,'written',d['coordinates'][0]['costs']['U_F']))
 reject('add raw code to printed code',lambda d:denominator(d,'including_printed_validation',d['coordinates'][0]['raw_costs']['complete_validation_programs']))
 reject('omit one raw program cost',lambda d:denominator(d,'including_raw_validation',-1))
 reject('charge common paper again in conditional',lambda d:denominator(d,'conditional_application',d['coordinates'][0]['costs']['U_F']))
 reject('wrong reduced numerator',lambda d:d['coordinates'][0]['comparisons']['written'].__setitem__('reduced_numerator',0))
 reject('wrong rounded decimal',lambda d:d['coordinates'][0]['comparisons']['written'].__setitem__('decimal','0.000000000000'))
 reject('unacquired conditional common',lambda d:d['coordinates'][0].__setitem__('acquired_common',0))
 reject('unacquired validation package',lambda d:d['coordinates'][0].__setitem__('acquired_printed_validation',0))
 reject('drop raw driver inventory cost',lambda d:d['coordinates'][0]['raw_costs'].__setitem__('complete_operational_drivers',0))
 reject('different primary coordinate',lambda d:d.__setitem__('primary',copy.deepcopy(d['coordinates'][0])))
 for key,val in [('retained_CP_fulltext_cost',0),('source_graphics_layout_cost',0),('required_uniform_proof_programs',3),('complete_validation_programs',2),('separate_operational_drivers',1),('scoped_Lean_declarations',6),('sawtooth_claim',True)]:reject('boundary '+key,lambda d,key=key,val=val:d['boundary'].__setitem__(key,val))
 reject('new question credit',lambda d:d.__setitem__('new_question_credit',1))
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--inputs',type=pathlib.Path,required=True);p.add_argument('--input-review',type=pathlib.Path,required=True);p.add_argument('--input-adoption',type=pathlib.Path,required=True);p.add_argument('--result',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
 for key,pin in [('inputs',PIN_INPUT),('input_review',PIN_REVIEW),('input_adoption',PIN_ADOPTION)]:bind(getattr(a,key),pin)
 bind(a.result.parent,PIN_NUMERICAL);need(a.result.name=='measurement.json','declared numerical record')
 counts=load(a.inputs/'author_counts.json');independent=load(a.input_review/'recount.json');need(counts['documents']==independent['documents'] and all(counts[k]==independent['raw_files'][k] for k in independent['raw_files']),'accepted independent input agreement')
 result=load(a.result);audit=check(result,counts);c=controls(result,counts);r=dict(status='PASS_INDEPENDENT_NUMERICAL_REVIEW',result_sha256=sha(a.result.read_bytes()),coordinate_count=30,exact_fractions=120,combined_fractions=90,conditional_fractions=30,primary=result['primary'],independent_fractions=audit,controls=c,no_new_extraction=True)
 a.out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print('PASS',len(audit),'coordinates',len(c),'controls')
