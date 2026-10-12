"""Independent integer/gcd derivation from adopted inputs. No author arithmetic imports."""
import json,math
from decimal import Decimal,localcontext
from pathlib import Path
SOURCES=['L032','L034','F016','F013','L035','N009','L128','L012','L121']
PAIRS=dict(zip(SOURCES,['A'+str(i)for i in range(1,10)]))
VARIANTS=['raw_untrimmed','raw_selected','calibrated_selected']
NORMS=['NFC','NFKC']
UNITS=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
PRIMARY='calibrated_selected/NFC/characters_without_whitespace'
def need(x,s):
 if not x:raise ValueError('A9_DISTINCT: '+s)
def ratio(a,b):
 g=math.gcd(a,b)
 with localcontext()as ctx:
  ctx.prec=60;q=Decimal(a)/Decimal(b)
  return {'source_cost':a,'replacement_cost':b,'numerator':a//g,'denominator':b//g,'decimal':format(q,'.12f'),'display_six':format(q,'.6f')}
def derive(input_file,roster_file):
 c=json.loads(Path(input_file).read_text());roster=json.loads(Path(roster_file).read_text())['files'];coordinates={}
 for v in VARIANTS:
  for n in NORMS:
   for unit in UNITS:
    key='/'.join([v,n,unit]);d={k:x['metrics'][v][n][unit]for k,x in c['documents'].items()};s=sum(d[k]for k in SOURCES);apps=sum(d[k]for k in PAIRS.values());u=d['U'];f={src:ratio(d[src],d[app])for src,app in PAIRS.items()};coordinates[key]={'document_costs':d,'source_sum':s,'whole_common':u,'application_sum':apps,'whole_written':u+apps,'written':ratio(s,u+apps),'conditional':f}
 raw=[];groups={}
 for row in roster:
  rid=row['id'];r=c['raw_files_measured'][rid];need(r['file']['sha256']==row['file']['sha256']and r['file']['bytes']==row['file']['bytes']and r['role']==row['role'],'exact adopted raw identity')
  group=('required_program_or_data'if row['mathematical_premise']else'inherited_auxiliary'if row['role']=='inherited_auxiliary'else'operational_runners'if row['role']in('current_operational_driver','operational_validation_runner')else'partial_formal_files')
  if group not in groups:groups[group]={'files':0,'literal_bytes':0,'metrics':{n:{m:0 for m in UNITS}for n in NORMS}}
  g=groups[group];g['files']+=1;g['literal_bytes']+=row['file']['bytes']
  for n in NORMS:
   for m in UNITS:g['metrics'][n][m]+=r['metrics'][n][m]
  raw.append({'id':rid,'group':group,'file':row['file'],'role':row['role'],'metrics':r['metrics']})
 p=coordinates[PRIMARY];stages=[];s=0;ours=p['whole_common']
 for i in range(10):
  if i:s+=p['document_costs'][SOURCES[i-1]];ours+=p['document_costs'][PAIRS[SOURCES[i-1]]]
  stages.append({'stage':i,'source_written':s,'replacement_written':ours})
 return {'primary_coordinate':PRIMARY,'coordinates':coordinates,'primary':p,'groups':groups,'raw_files':raw,'stages':stages}
if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('--input',type=Path,required=True);a.add_argument('--roster',type=Path,required=True);a.add_argument('--out',type=Path,required=True);q=a.parse_args();need(not q.out.exists(),'fresh output');r=derive(q.input,q.roster);q.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'whole':r['primary']['written'],'L121':r['primary']['conditional']['L121']}))
