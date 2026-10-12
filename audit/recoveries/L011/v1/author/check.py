#!/usr/bin/env python3
"""Portable bound-scope, certificate and native-render replay. Not a formal proof."""
import argparse,copy,hashlib,json,re,subprocess,sys
from pathlib import Path
from pypdf import PdfReader
R=Path(__file__).resolve().parent
EXPECTED={
 'A5_control':(60,[1,3],1,15,6), 'A6':(360,[1,6,18],1,45,0),
 'A7':(2520,[1,6,28,1],1,105,0),'M11':(7920,[1,6,32,3],1,165,0),
 'M22':(443520,[1,8,178,40],1,1155,0),'M23':(10200960,[1,6,166,77,4],1,3795,0),
 'McL':(898128000,[1,4,132,65,2],1,22275,0),
 'U4_3':(3265920,[1,9,185,36,2],1,2835,0),
 'U5_2':(13685760,[2,13,145,26,2],2,3135,0)}
REQUIRED=['programs/string_search.g','programs/unitary_models.g','programs/run_certificate.g']
def need(x,m):
 if not x:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(n):return json.loads((R/n).read_text())
def texts(p):return [x.extract_text() for x in PdfReader(p).pages]
def save(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def bind(base,rows):
 for x in rows:
  p=base/x['path'];need(p.is_file(),f"missing {x['path']}");need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],f"byte binding {x['path']}")
def validate(scope,contract,inventory,report):
 need(scope['original_id']=='L011' and contract['original_id']=='L011','original identity')
 need(scope['finite_exceptions']==list(EXPECTED)[1:],'eight exact finite cases')
 need(scope['native_written_pages']==8 and [d['pages'] for d in scope['documents']]==[4,4],'whole native papers')
 need(scope['retained_positive_classification'] is True,'positive retained theorem')
 need(scope['formal_files']==[] and scope['full_formalization'] is False,'no full formal claim')
 need(scope['source_credit'] is None and scope['numerical_factor'] is None,'no registration or factor')
 need(contract['source']['sha256']=='506b2f864bf44492bc40bb3bc353d527d7d96cd9f5526cc632eb3c6b5c5a29aa' and contract['source']['pages']==6,'exact full source')
 ids=[x['id'] for x in contract['dispositions']];need(len(ids)==27 and len(set(ids))==27,'complete unique source dispositions')
 need(all('L011.finite.'+g in ids for g in EXPECTED if g!='A5_control'),'all finite source routes')
 need(contract['new_question_answer'] is False and contract['new_formalization'] is False,'bounded scope')
 need(contract['source_listing_inventory']['unknown_historical_software_cost'] is None,'historical software unknown')
 files=inventory['files'];need(len({x['path'] for x in files})==len(files),'unique whole inventory files')
 need([x['path'] for x in files if x['role']=='REQUIRED_MATHEMATICAL_PROGRAM']==REQUIRED,'entire required closure')
 need(next(x for x in files if x['path']=='optional_permutation_oracle.py')['role']=='OPTIONAL_VALIDATION','optional oracle distinct')
 need(next(x for x in files if x['path']=='check.py')['role']=='OPERATIONAL_PACKET_DRIVER','whole packet driver distinct')
 need(inventory['formal_files']==[] and inventory['required_software_inclusive_factor'] is None,'software/formal boundary')
 need(report['status']=='PASS' and report['role']=='REQUIRED_FINITE_PROOF_CERTIFICATE_FOR_EXACT_EIGHT_EXCEPTIONAL_GROUPS','proof certificate role')
 need([x['group'] for x in report['cases']]==list(EXPECTED),'complete report cases')
 for x in report['cases']:
  expected=EXPECTED[x['group']];actual=(x['order'],x['prefix_counts'],x['involution_classes'],x['involutions'],x['witnesses'])
  need(actual==expected,'finite case '+x['group'])
 need(sum(sum(x['prefix_counts']) for x in report['cases'][1:])==1209,'complete proper prefixes')
 fresh=report['fresh_permutation_orders'];need(len(fresh)==11,'eleven fresh order calculations')
 want={g:v[0] for g,v in EXPECTED.items()};want.update(unitary_model_4_3=3265920,unitary_model_5_2=13685760)
 need({x['tag']:x['order'] for x in fresh}==want and all(x['qualification']=='NO_CACHED_SIZE_OR_CHAIN' for x in fresh),'independent permutation orders')
 need(set(report['whole_program_sha256'])==set(REQUIRED),'complete program pins')
 need('random=1000' in report['stabilizer_chain_option'] and 'not excluded' in report['stabilizer_chain_option'],'verified-chain qualification')
 return True

def controls(s,c,i,r):
 cases=[]
 def add(name,which,mutate):cases.append((name,which,mutate))
 add('missing finite case',0,lambda x:x['finite_exceptions'].pop())
 add('free common paper',0,lambda x:x.update(native_written_pages=4))
 add('dropped positive theorem',0,lambda x:x.update(retained_positive_classification=False))
 add('full formal claim',0,lambda x:x.update(full_formalization=True))
 add('premature source credit',0,lambda x:x.update(source_credit=1))
 add('invented factor',0,lambda x:x.update(numerical_factor=2))
 add('truncated primary',1,lambda x:x['source'].update(pages=5))
 add('wrong primary',1,lambda x:x['source'].update(sha256='0'*64))
 add('duplicate disposition',1,lambda x:x['dispositions'].__setitem__(1,copy.deepcopy(x['dispositions'][0])))
 add('new question credit',1,lambda x:x.update(new_question_answer=True))
 add('historical software zero',1,lambda x:x['source_listing_inventory'].update(unknown_historical_software_cost=0))
 add('required computation optional',2,lambda x:x['files'][0].update(role='OPTIONAL_VALIDATION'))
 add('oracle proof premise',2,lambda x:next(y for y in x['files'] if y['path']=='optional_permutation_oracle.py').update(role='REQUIRED_MATHEMATICAL_PROGRAM'))
 add('driver missing',2,lambda x:x['files'].__setitem__(4,copy.deepcopy(x['files'][3])))
 add('software scalar',2,lambda x:x.update(required_software_inclusive_factor=1))
 add('positive control rejected',3,lambda x:x['cases'][0].update(witnesses=0))
 add('missed generating marking',3,lambda x:x['cases'][1].update(witnesses=1))
 add('truncated last prefix',3,lambda x:x['cases'][-1]['prefix_counts'].pop())
 add('missing second involution class',3,lambda x:x['cases'][-1].update(involution_classes=1))
 add('wrong ambient group order',3,lambda x:x['cases'][6].update(order=8981280))
 add('unverified chain',3,lambda x:x.update(stabilizer_chain_option='random=1'))
 add('missing unitary code',3,lambda x:x['whole_program_sha256'].pop('programs/unitary_models.g'))
 add('missing fresh model order',3,lambda x:x['fresh_permutation_orders'].pop())
 add('cached constructor order',3,lambda x:x['fresh_permutation_orders'][0].update(qualification='CACHED_SIZE'))
 passed=[]
 for name,which,mutate in cases:
  xx=copy.deepcopy([s,c,i,r]);mutate(xx[which])
  try:validate(*xx)
  except (ValueError,StopIteration,KeyError):passed.append(name)
  else:raise ValueError('control did not reject: '+name)
 return passed

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);ap.add_argument('--programs',action='store_true');ap.add_argument('--optional',action='store_true');ap.add_argument('--render',action='store_true');ap.add_argument('--study-root');ap.add_argument('--gap',default='/opt/homebrew/bin/gap');ap.add_argument('--pdflatex',default='/opt/homebrew/bin/pdflatex');a=ap.parse_args()
 out=Path(a.out).resolve();need(not out.exists(),'fresh output');out.mkdir(parents=True)
 manifest=load('manifest.json') if (R/'manifest.json').exists() else None
 if manifest:bind(R,manifest['exports'])
 s,c,i,r=map(load,['scope.json','source_contract.json','program_inventory.json','reports/finite/report.json']);validate(s,c,i,r)
 bind(R,[x for x in i['files'] if x.get('sha256')])
 for path,h in r['whole_program_sha256'].items():need(sha(R/path)==h,'program receipt '+path)
 pm=load('proof_map.json')['complete_proof_environments'];need(len(pm)==9,'nine complete proofs')
 for x in pm:
  text=(R/x['file']).read_text();lines=text.splitlines(keepends=True);block=''.join(lines[x['start_line']-1:x['end_line']]).rstrip('\n')
  need(hashlib.sha256(block.encode()).hexdigest()==x['sha256'],'complete proof span '+x['id'])
 if a.study_root:bind(Path(a.study_root),[c['source']])
 report=dict(status='PASS',author_role='enumeration_volume; no independent scientific acceptance',exports_checked=0 if not manifest else len(manifest['exports']),source_dispositions=27,complete_proof_environments=9,controls=controls(s,c,i,r),programs_replayed=False,optional_replayed=False,renders=[],source_checked=bool(a.study_root),diagnostics=[])
 if a.programs:
  p=subprocess.run([sys.executable,'-B','-O',str(R/'run.py'),'--out',str(out/'finite'),'--gap',a.gap],text=True,capture_output=True)
  (out/'finite_wrapper.stdout').write_text(p.stdout);(out/'finite_wrapper.stderr').write_text(p.stderr);need(p.returncode==0,'fresh finite replay')
  rr=json.loads((out/'finite/report.json').read_text());validate(s,c,i,rr);need(rr['whole_program_sha256']==r['whole_program_sha256'],'fresh complete program pins');report['programs_replayed']=True
 if a.optional:
  p=subprocess.run([sys.executable,'-B',str(R/'optional_permutation_oracle.py')],text=True,capture_output=True);need(p.returncode==0,'optional small oracle');oracle=json.loads(p.stdout);need(oracle==load('reports/optional_oracle.json'),'optional oracle exact result');save(out/'optional.json',oracle);report['optional_replayed']=True
 if a.render:
  build=out/'build';build.mkdir()
  for d in s['documents']:
   for passno in [1,2]:
    p=subprocess.run([a.pdflatex,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(build),d['tex']],cwd=R,text=True,capture_output=True);(build/(d['id']+f'.pass{passno}.log')).write_text(p.stdout+p.stderr);need(p.returncode==0,'native compile '+d['id'])
   log=(build/Path(d['tex']).with_suffix('.log')).read_text();bad=[line for line in log.splitlines() if 'Overfull' in line or 'undefined' in line.lower() or 'LaTeX Warning:' in line];need(not bad,'render diagnostics '+str(bad))
   pdf=build/d['pdf'];need(texts(pdf)==texts(R/d['pdf']),'exact page texts '+d['id']);need(len(texts(pdf))==d['pages'],'whole pages');report['renders'].append({'id':d['id'],'pages':d['pages'],'compiler':'pdflatex','exact_page_text':True})
 save(out/'report.json',report);print(json.dumps(report))
if __name__=='__main__':main()
