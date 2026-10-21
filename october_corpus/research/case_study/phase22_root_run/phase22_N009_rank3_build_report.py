#!/usr/bin/env python3
"""Bind the rank-three/excess-five exhaustive run and primary type comparison."""
from pathlib import Path
import argparse,collections,gzip,hashlib,json,re
p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--output',type=Path);a=p.parse_args();b=a.directory
h=lambda path:hashlib.sha256(path.read_bytes()).hexdigest()
prefix='phase22_N009_rank3';logpath=b/(prefix+'_census.log');log=logpath.read_text();rows=json.loads((b/(prefix+'.accepted.json')).read_text())
m=re.search(r'RESULT rank=3 candidates=(\d+) ordered=(\d+) selfdual=(\d+) up_to_reversal=(\d+) actual_meets=(\d+)',log);assert m
candidates,ordered,fixed,orbits,meets=map(int,m.groups())
assert 'all-candidate full-IP cross-check agree' in log and meets==64*candidates
assert ordered==len(rows)==len({tuple(r[0]) for r in rows})
expected={(4,4):1,(4,8):8,(4,16):14,(4,32):4,(4,64):2,(4,128):2,(8,8):22,(8,16):40,(8,32):8,(8,64):4,(16,16):10,(16,32):10}
cts=collections.Counter();fts=collections.Counter()
for key,typ,cl,kinv,selfdual,facets in rows:
 assert len(typ)==2 and min(typ)>=4 and cl<=7 and 32%__import__('math').prod(kinv)==0
 t=min(tuple(typ),tuple(reversed(typ)));cts[t]+=1
 if selfdual:
  assert typ==list(reversed(typ));fts[t]+=1
 assert facets==[2*typ[0],2*typ[1]]
assert set(cts)==set(expected) and sum(fts.values())==fixed
comparison=[]
for t,count in expected.items():
 assert (cts[t]+fts[t])%2==0 and (cts[t]+fts[t])//2==count
 comparison.append(dict(type=list(t),ordered=cts[t],selfdual=fts[t],classes=count))
assert sum(expected.values())==orbits and 2*orbits==ordered+fixed
levels=[]
for depth in range(1,6):
 path=b/(prefix+'.level'+str(depth)+'.json');data=json.loads(path.read_text());assert len(data)==len({tuple(x) for x in data})
 compressed=path.with_suffix(path.suffix+'.gz');compressed.write_bytes(gzip.compress(path.read_bytes(),mtime=0))
 levels.append(dict(depth=depth,index=2**depth,kernels=len(data),path=compressed.name,sha256=h(compressed),uncompressed_sha256=h(path)))
assert levels[-1]['kernels']==candidates
km=re.search(r'KERNEL_PROFILE_CHECKS comparisons=(\d+) rejected=(\d+) directly_verified=(\d+)',log);assert km
profile,rejected,accepted=map(int,km.groups());assert accepted==ordered and rejected==candidates-ordered
report=dict(status='PASS',rank=3,excess=5,order=1024,class_bound=7,universal_order=2**38,gamma3_order=2**33,gamma3_derived_order=512,universal_gamma3_abelian=False,candidate_kernels=candidates,ordered_markings=ordered,selfdual_markings=fixed,classes_up_to_reversal=orbits,all_candidate_actual_meets=meets,kernel_profile_meets=profile,profile_rejections=rejected,source_type_comparison=comparison,levels=levels,files={n:h(b/n) for n in [prefix+'_census.g',prefix+'_census.log',prefix+'.accepted.json',prefix+'_universal.g',prefix+'_universal.log']},report_builder_sha256=h(Path(__file__)),source=dict(id='N009',target='Table5, printed p11',pdf_url='https://cdm.ucalgary.ca/article/download/62475/46803',pdf_sha256='0618a57cb5ff35c13587877818a2e77bce442cf2c561f204b6d5e5e095fa2fda'),trust_boundary=['GAP/NQ universal nilpotent quotient and exact subgroup algorithms retained','Every candidate has all 64 actual intersection checks, including profile-rejected candidates','No catalogue or source-presentation/count candidate filter','Kernel invariant lists are abelianizations, not claims that the kernels are abelian','Source comparison is by all12type aggregates, not individual presentation labels'])
out=a.output or b/(prefix+'_certificate.json');out.write_text(json.dumps(report,indent=2)+'\n');print('PASS',candidates,'kernels;',ordered,'ordered;',fixed,'selfdual;',orbits,'classes; all12source types')
