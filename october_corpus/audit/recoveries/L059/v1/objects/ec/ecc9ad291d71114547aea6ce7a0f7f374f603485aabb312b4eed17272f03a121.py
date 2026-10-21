"""Verify the immutable census register and reproduce its 39 table totals.

This audit checks retained computational certificates and their provenance.
It does not relaunch the complete subgroup census or claim Lean verification.
"""
from pathlib import Path
import argparse,collections,hashlib,json,os,re,subprocess,sys
if sys.flags.optimize:raise RuntimeError('optimized Python is unsupported')
def need(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('--sources',type=Path,required=True)
 parser.add_argument('--replay',type=Path,required=True)
 parser.add_argument('--replay-inputs',action='store_true')
 parser.add_argument('--replay-named',action='store_true')
 parser.add_argument('--gap',default='/opt/homebrew/bin/gap')
 a=parser.parse_args();H=Path(__file__).resolve().parent;W=a.sources.resolve()
 a.replay.mkdir(exist_ok=False)
 deps=json.loads((H/'dependencies.json').read_text())
 for x in deps:
  p=Path(x['path']);need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'dependency '+str(p))
 rows=json.loads((H/'census_register.json').read_text())
 need(len({(r['family'],r['graph']) for r in rows})==len(rows)==1950,'unique source inputs')
 totals={};old_tokens=0;retry_count=0;reversals=[]
 for r in rows:
  p=W/r['witness'];need(sha(p)==r['witness_sha256'],'witness '+r['graph'])
  s=p.read_text()
  maximum=re.findall(r'maxcode := \[(.*?)\]',s,re.S)
  normal=re.findall(r'normcode := \[(.*?)\]',s,re.S)
  mc=[];nc=[]
  for raw in maximum:
   parts=re.findall(r'"(2T|M|X)"',raw)
   need(len(parts)==4 and re.sub(r'\s+','',raw)==','.join('"'+t+'"' for t in parts),'Max syntax')
   mc.append(''.join(parts))
  for raw in normal:
   parts=re.findall('true|false',raw)
   need(len(parts)==4 and re.sub(r'\s+','',raw)==','.join(parts),'Norm syntax')
   nc.append(''.join('Y' if t=='true' else 'N' for t in parts))
  need(len(mc)==len(nc)==r['markings'] and r['markings']>0,'positive row count '+r['graph'])
  need(dict(collections.Counter(mc))==r['max'] and dict(collections.Counter(nc))==r['norm'],'stored row summary')
  if 'receipt' in r:
   receipt=json.loads((W/r['receipt']).read_text())
   need(receipt['status']=='PASS' and receipt['returncode']==0,'terminal receipt')
   for suffix in ['stdout','stderr']:
    need(sha(W/r[suffix])==receipt[suffix+'_sha256'],'terminal stream hash')
   need(not (W/r['stderr']).read_text().strip(),'terminal stderr')
   need(sha(W/r['worker'])==r['worker_sha256']==receipt['script_sha256'],'actual worker')
   need(receipt['witness_sha256']==r['witness_sha256'],'receipt witness')
   if 'basis' in r:need(sha(W/r['basis'])==receipt['basis_sha256'],'extension basis')
   if 'prior_capped_receipt' in r:
    old=W/r['prior_capped_receipt'];d=json.loads(old.read_text())
    need(d['status']=='TIME_LIMIT_NO_CONCLUSION' and sha(old)==receipt['prior_capped_receipt_sha256'],'preserved cap')
    retry_count+=1
  else:
   token=re.fullmatch(r'COMPLETE '+re.escape(r['graph'])+r' (\d+) (\d+)\n',(W/r['done']).read_text())
   need(token is not None and int(token[1])==r['markings'],'old per-graph completion')
   need(sha(W/r['worker'])==r['worker_sha256'],'old producer');old_tokens+=1
  if r['reverse_parts_for_table']:
   need(r['family']=='quartic' and r['graph']=='128_055','unexpected part reversal')
   mc=[''.join([t[1],t[0],t[3],t[2]]) for t in [re.findall('2T|M|X',code) for code in mc]]
   nc=[''.join([t[0],t[2],t[1],t[3]]) for t in nc]
   reversals.append(r['graph'])
  if r['family'] not in totals:totals[r['family']]={'graphs':0,'markings':0,'max':collections.Counter(),'norm':collections.Counter()}
  t=totals[r['family']];t['graphs']+=1;t['markings']+=r['markings'];t['max'].update(mc);t['norm'].update(nc)
 expected={'quartic':(397,1643),'symmetric':(714,1082),'semisymmetric':(43,102),'subdivision':(796,1427)}
 for k,v in expected.items():need((totals[k]['graphs'],totals[k]['markings'])==v,'family scope '+k)
 need(retry_count==2 and reversals==['128_055'],'explicit corrections')
 c=json.loads((W/'cubic_scopes_summary.json').read_text());q=json.loads((W/'quartic_census_scope_corrected_summary.json').read_text())
 need(totals['symmetric']['max']==c['source_symmetric_max'] and totals['symmetric']['norm']==c['source_symmetric_norm'],'16 printed cubic cells')
 source_max={'2TXX2T':11,'2TXXM':1,'X2TXX':26,'2TXMM':1,'2TXXX':19,'XX2T2T':1,'XXMM':17,'2T2TMM':5,'X2T2TX':11,'2T2TXX':38,'XXXX':1503,'2T2T2T2T':10}
 source_norm={'YNNN':466,'NNYN':4,'YNNY':525,'NYNN':4,'NNYY':3,'NYNY':3,'YYNN':2,'YYYY':1,'YNYN':2,'NNNN':365,'NNNY':268}
 need(totals['quartic']['max']==source_max and totals['quartic']['norm']==source_norm,'23 printed quartic cells')
 # The three named historical entries are identified using the separately
 # acquired set equality and a unique invariant pair, not invariants alone.
 named=[]
 for file in ['c4_table_20080505.html.json','c4_table_20141228.html.json','c4_table.html.json']:
  table=json.loads((W/file).read_text())
  selected=[r for r in table if r['n']<=150 and r['bipartite'] and r['tr'] in ['DT','SS'] and r['vertex_stabilizer']<200]
  need(len(selected)==397,'historical corrected set')
  ids=[]
  for n,order in [(8,1152),(10,240),(110,1320)]:
   match=[r for r in selected if (r['n'],r['aut_order'])==(n,order)]
   need(len(match)==1,'unique named invariant pair');ids.append({'n':n,'aut_order':order,'index':match[0]['i']})
  named.append({'edition':file,'entries':ids})
 env=os.environ.copy();env.pop('PYTHONOPTIMIZE',None)
 commands=[]
 if a.replay_inputs:commands.append(('primary_inputs',[sys.executable,str(H/'verify_cubic_sources.py'),'--sources',str(W),'--output',str(a.replay.resolve()/'primary_inputs.json')],W,120,'PASS_PRIMARY_CUBIC_SOURCES_839_REUSE_261'))
 if a.replay_named:commands.append(('named_groups',[a.gap,'-q','-b','-T','named_examples_check.g'],W,180,'PASS_MATHIEU_MARKED_ISOMORPHISM_AND_STRUCTURES'))
 for name,command,cwd,timeout,token in commands:
  run=subprocess.run(command,cwd=cwd,env=env,text=True,capture_output=True,timeout=timeout)
  (a.replay/(name+'.stdout')).write_text(run.stdout);(a.replay/(name+'.stderr')).write_text(run.stderr)
  need(run.returncode==0 and not run.stderr.strip() and token in run.stdout.splitlines(),'bounded replay '+name)
 report={'status':'PASS_PRINCIPAL_CERTIFICATE_INTEGRITY_AND_39_TABLE_CELLS','dependencies':len(deps),'graphs':len(rows),'faithful_markings':sum(r['markings'] for r in rows),'totals':totals,'old_per_graph_completion_tokens':old_tokens,'preserved_caps_with_separate_successful_retries':retry_count,'part_reversals':reversals,'named_historical_entries':named,'bounded_replays':[x[0] for x in commands],'new_Lean_claim':False,'full_census_relaunched':False}
 (a.replay/'report.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
 print('PASS:1950 graphs;4254 markings;39 printed table cells;all declared dependencies and actual worker receipts')
if __name__=='__main__':main()
