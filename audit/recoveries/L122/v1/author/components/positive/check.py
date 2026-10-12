#!/usr/bin/env python3
"""Portable replay of explicit finite witnesses and bounded source dispositions."""
import argparse,copy,hashlib,json,re,shutil,subprocess,time
from pathlib import Path
from pypdf import PdfReader
R=Path(__file__).resolve().parent
EXPECTED={'Sz8':[29120,14,2080,20,7],'PSL2_8':[504,14,36,9,7],'PSL2_27':[9828,28,351,12,14],'PSL2_64':[262080,130,2016,60,65],'PSL2_125':[976500,62,15750,60,31],'PSL2_512':[134217216,1026,130816,504,513]}
FRESH=[y for v in EXPECTED.values() for y in [v[0],v[3],v[0]]]
PROGRAMS=['programs/verify_examples.g','data/seeds.g']
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((R/n).read_text())
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def binding(base,items):
 for x in items:
  p=base/x['path'];need(p.is_file() and sha(p)==x['sha256'] and p.stat().st_size==x['bytes'],'binding '+x['path'])
def texts(p):return [x.extract_text() for x in PdfReader(p).pages]
def parse(stdout):
 need('L122_FINITE_EXAMPLES_PASS' in stdout and not any(x in stdout for x in ['Error,','Syntax error','break loop']),'actual GAP completion')
 cases={m.group(1):list(map(int,m.groups()[1:])) for m in re.finditer(r'^EXAMPLE\|([^|]+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)\|(\d+)$',stdout,re.M)}
 fresh=[int(m.group(2)) for m in re.finditer(r'^FRESH\|(\d+)\|(\d+)\|NO_CACHED_SIZE_OR_CHAIN$',stdout,re.M)]
 need(cases==EXPECTED,'all six exact examples');need(fresh==FRESH,'all eighteen uncached orders')
 need(stdout.count('ABSOLUTE|20|20|60|20|0')==1,'whole absolute subgeometry')
 return {'cases':cases,'fresh_orders':fresh,'absolute':{'objects':20,'orbit':20,'edges':60,'chambers':20,'unextendable_edges':0}}
def validate(s,c,i,r,o):
 need(s['original_id']=='L122' and c['original_id']=='L122','fixed original')
 need(s['finite_cases']==list(EXPECTED),'all six finite cases')
 need([x['pages'] for x in s['documents']]==[4,4] and s['native_written_pages']==8,'whole common and application')
 need(s['complete_original_recovery_claim'] is False and c['complete_original_recovery_claim'] is False,'no incomplete-as-whole credit')
 need(s['unresolved_principal_obligations']==c['unresolved_principal_obligations']==['L122.Lemma1_bare_existence'],'literal principal obligation preserved')
 need(o['status']=='UNRESOLVED_LITERAL_GENERAL_PRINCIPAL_ASSERTION' and o['source_credit'] is None,'remaining obligation not relabeled')
 need(s['source_credit'] is None and s['numerical_factor'] is None and s['new_question_answer'] is False,'no source/factor/question credit')
 need(s['full_formalization'] is False and s['formal_files']==[],'no formal claim')
 need(c['source']['sha256']=='6df5e83ab3fef9f5374375ef9fa0b39cce4969258422772da46f75b479158418' and c['source']['pages']==6,'whole exact source')
 rows=c['dispositions'];ids=[x['id'] for x in rows];need(len(ids)==36 and len(set(ids))==36,'all unique source dispositions')
 row=next(x for x in rows if x['id']=='L122.Lemma1_bare_existence');need(row['status']=='UNRESOLVED_PRINCIPAL_OBLIGATION','bare lemma not silently closed')
 for name in ['duality_reset','triality_reset']:need(next(x for x in rows if x['id']=='L122.'+name)['status']=='REFUTED_LITERAL_NORMALIZATION','exact reset correction')
 need(c['source_listing_inventory']['unknown_historical_software_cost'] is None and c['source_listing_inventory']['executable_listings']==[],'historical software boundary')
 files=i['files'];need(len(files)==4 and len({x['path'] for x in files})==4,'four complete executable/data roles')
 need({x['path']:x['role'] for x in files}=={'programs/verify_examples.g':'REQUIRED_MATHEMATICAL_PROGRAM','data/seeds.g':'REQUIRED_MARKING_AND_FIELD_DATA','optional_small_oracle.py':'OPTIONAL_VALIDATION','check.py':'OPERATIONAL_PACKET_DRIVER'},'required/optional roles')
 need(i['software_inclusive_factor'] is None and i['formal_files']==[],'no software scalar or formal claims')
 need(r['status']=='PASS' and r['role']=='REQUIRED_FINITE_PROOF_PREMISES_FOR_SIX_EXPLICIT_MARKINGS','finite receipt role')
 need(r['cases']==EXPECTED and r['fresh_orders']==FRESH,'complete finite receipt')
 need(r['absolute']=={'objects':20,'orbit':20,'edges':60,'chambers':20,'unextendable_edges':0},'all absolute claims')
 need(r['source_historical_markings_identified'] is False,'no historical marking identification')
 need(r['sigma_orders']==[3]*6 and r['outer_cases']==['Sz8','PSL2_27','PSL2_64','PSL2_125','PSL2_512'],'actual triality and outer scope')
 need(set(r['whole_program_sha256'])==set(PROGRAMS),'complete finite input pins')
 return True

def controls(s,c,i,r,o):
 cases=[]
 def add(name,k,f):cases.append((name,k,f))
 add('missing largest finite case',0,lambda x:x['finite_cases'].pop())
 add('free common paper',0,lambda x:x.update(native_written_pages=4))
 add('premature whole original recovery',0,lambda x:x.update(complete_original_recovery_claim=True))
 add('dropped principal obligation',0,lambda x:x.update(unresolved_principal_obligations=[]))
 add('source credit from partial work',0,lambda x:x.update(source_credit=1))
 add('invented compression factor',0,lambda x:x.update(numerical_factor=2))
 add('full formalization',0,lambda x:x.update(full_formalization=True))
 add('truncated primary',1,lambda x:x['source'].update(pages=5))
 add('wrong primary bytes',1,lambda x:x['source'].update(sha256='0'*64))
 add('duplicate source disposition',1,lambda x:x['dispositions'].__setitem__(0,copy.deepcopy(x['dispositions'][1])))
 add('proof gap called false theorem',1,lambda x:next(y for y in x['dispositions'] if y['id']=='L122.Lemma1_bare_existence').update(status='REFUTED'))
 add('triality reset left uncorrected',1,lambda x:next(y for y in x['dispositions'] if y['id']=='L122.triality_reset').update(status='PROVED'))
 add('historical software treated as zero',1,lambda x:x['source_listing_inventory'].update(unknown_historical_software_cost=0))
 add('required program made optional',2,lambda x:x['files'][0].update(role='OPTIONAL_VALIDATION'))
 add('marking data omitted',2,lambda x:x['files'].pop(1))
 add('optional oracle made premise',2,lambda x:x['files'][2].update(role='REQUIRED_MATHEMATICAL_PROGRAM'))
 add('software factor',2,lambda x:x.update(software_inclusive_factor=1))
 add('wrong finite reduced group',3,lambda x:x['cases']['Sz8'].__setitem__(3,10))
 add('cached order substituted',3,lambda x:x['fresh_orders'].pop())
 add('absolute edge omitted',3,lambda x:x['absolute'].update(edges=59))
 add('historical marking identity asserted',3,lambda x:x.update(source_historical_markings_identified=True))
 add('order-nine instead of triality',3,lambda x:x['sigma_orders'].__setitem__(0,9))
 add('inner outer distinction dropped',3,lambda x:x.update(outer_cases=[]))
 add('unresolved gap made ancillary',4,lambda x:x.update(status='ANCILLARY_EXCLUDED'))
 passed=[]
 for name,k,f in cases:
  xx=copy.deepcopy([s,c,i,r,o]);f(xx[k])
  try:validate(*xx)
  except (ValueError,KeyError,StopIteration):passed.append(name)
  else:raise ValueError('control failed: '+name)
 return passed

def run_gap(base,gap,out):
 start=time.monotonic();proc=subprocess.run([gap,'-q','-b','-T','programs/verify_examples.g'],cwd=base,capture_output=True,text=True)
 (out/'stdout.txt').write_text(proc.stdout);(out/'stderr.txt').write_text(proc.stderr)
 need(proc.returncode==0 and not proc.stderr.strip(),'GAP runtime')
 ans=parse(proc.stdout.replace('\r',''));ans['seconds']=round(time.monotonic()-start,3);return ans

def finite_controls(out,gap):
 tests=[('identity involution seed','data/seeds.g','\nTrialitySeeds.sz8:=IdentityMat(4,GF(8));;\n','three distinct involutions'),('wrong field polynomial','data/seeds.g','\nTrialityFieldPolynomials.q512[1]:=0;;\n','literal field defining polynomial'),('identity instead of triality','programs/verify_examples.g',None,'Suzuki field automorphism')]
 results=[]
 for number,(name,path,append,expected) in enumerate(tests):
  d=out/str(number);d.mkdir(parents=True)
  for rel in PROGRAMS:
   target=d/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(R/rel,target)
  p=d/path
  if append:p.write_text(p.read_text()+append)
  else:p.write_text(p.read_text().replace(' Need(IsBijective(sigma) and Order(sigma)=3,"Suzuki field automorphism");',' sigma:=IdentityMapping(g);\n Need(IsBijective(sigma) and Order(sigma)=3,"Suzuki field automorphism");'))
  proc=subprocess.run([gap,'-q','-b','-T','programs/verify_examples.g'],cwd=d,capture_output=True,text=True);combined=proc.stdout+proc.stderr;(d/'output.txt').write_text(combined)
  need('L122_FINITE_EXAMPLES_PASS' not in combined and expected in combined,'actual finite negative control '+name);results.append(name)
 return results

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--optional',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--study-root');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args()
 out=Path(a.out).resolve();need(not out.exists(),'fresh output path');out.mkdir(parents=True)
 if (R/'manifest.json').exists():binding(R,load('manifest.json')['exports'])
 s,c,i,r,o=map(load,['scope.json','source_contract.json','program_inventory.json','reports/finite/report.json','remaining_obligation.json']);validate(s,c,i,r,o)
 binding(R,[x for x in i['files'] if 'sha256' in x]);binding(R,i['evidence_outputs'])
 for p,h in r['whole_program_sha256'].items():need(sha(R/p)==h,'receipt program '+p)
 need(parse((R/'reports/finite/stdout.txt').read_text().replace('\r',''))=={k:r[k] for k in ['cases','fresh_orders','absolute']},'literal finite output')
 pm=load('proof_map.json');need(len(pm['complete_environments'])==6,'six complete written theorem/proof environments')
 for x in pm['complete_environments']:
  b=''.join((R/x['file']).read_text().splitlines(keepends=True)[x['start_line']-1:x['end_line']]).rstrip('\n');need(hashlib.sha256(b.encode()).hexdigest()==x['sha256'],'complete proof span '+x['id'])
 if a.study_root:
  S=Path(a.study_root);binding(S,[c['source']]);binding(S,[x for x in load('dependencies.json')['items'] if x.get('path')])
 report={'status':'PASS','role':'AUTHOR_REPLAY_NOT_DISTINCT_MATHEMATICAL_REVIEW','scope':'Six finite examples, written corrections and one explicit unresolved principal obligation; no whole-original credit.','source_dispositions':36,'whole_native_pages':8,'complete_environments':6,'controls':controls(s,c,i,r,o),'program_run':None,'optional_run':None,'render':[],'diagnostics':[]}
 if a.programs:
  d=out/'finite';d.mkdir();report['program_run']=run_gap(R,a.gap,d);report['finite_negative_controls']=finite_controls(out/'finite_controls',a.gap)
 if a.optional:
  proc=subprocess.run(['python3',str(R/'optional_small_oracle.py')],capture_output=True,text=True);need(proc.returncode==0,'optional coordinate oracle');report['optional_run']=json.loads(proc.stdout)
 if a.render:
  b=out/'render';b.mkdir()
  for doc in s['documents']:
   tex=R/doc['tex'];stem=tex.stem
   for j in range(2):
    p=subprocess.run([a.pdflatex,'-halt-on-error','-interaction=nonstopmode','-output-directory',str(b),str(tex)],cwd=R,capture_output=True,text=True);(b/(stem+str(j)+'.stdout')).write_text(p.stdout+p.stderr);need(p.returncode==0,'native render '+stem)
   log=(b/(stem+'.log')).read_text();bad=[line for line in log.splitlines() if 'Overfull' in line or 'LaTeX Warning' in line];need(not bad,'render diagnostics '+str(bad))
   need(len(texts(b/(stem+'.pdf')))==doc['pages'] and texts(b/(stem+'.pdf'))==texts(R/doc['path']),'exact page texts '+stem);report['render'].append({'path':doc['path'],'pages':doc['pages'],'page_texts_exact':True})
 save(out/'report.json',report);print(json.dumps({'status':'PASS','source_dispositions':36,'whole_pages':8,'finite_cases':len(EXPECTED),'controls':len(report['controls']),'programs':a.programs,'render':a.render}))
if __name__=='__main__':main()
