from pathlib import Path
import csv,json,hashlib,math,argparse
from decimal import Decimal,localcontext
from itertools import product
P=Path('/Users/sasha/medusa/research/leemans/topic_B_L047_measurement_results')
AUTHOR='eaa3f62b0cea99890ed73f2816212423cde2a48dec43a8aaca756b4d6e7a9118'
def need(t,m):
 if not t: raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def key(x):return tuple(x[k] for k in ['variant','normalization','unit'])
def f(n,d):
 g=math.gcd(n,d)
 with localcontext() as ctx:
  ctx.prec=42; dec=str(Decimal(n)/Decimal(d))
 return dict(numerator=n,denominator=d,reduced_numerator=n//g,reduced_denominator=d//g,decimal=dec)
def run():
 need(sha(P/'manifest.json')==AUTHOR,'author freeze')
 m=read(P/'manifest.json')
 for x in m['exports']:
  p=P/x['path'];need(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'export '+x['path'])
 need(len(m['exports'])==len({x['path'] for x in m['exports']})==85,'85 distinct exports')
 c=read(P/'inputs/current/author_counts.json');r=read(P/'results.json');old=read(P/'prior/results.json')
 ids=['N001','N003','N008','L030','L040','L047'];apps=dict(zip(ids,['B1','B2','B3','B4','B5','B6']))
 grid=list(product(['raw_untrimmed','raw_selected','calibrated_selected'],['NFC','NFKC'],['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']))
 source={key(x):x for x in c['source_coordinates']};results={key(x):x for x in r['coordinates']};prior={key(x):x for x in old['rows']}
 need(set(source)==set(results)==set(grid) and len(r['coordinates'])==30,'grid')
 expected={};costs={};stages={};preserved=0;preserved_article=0
 for k in grid:
  v,n,u=k;s=source[k]['sources'];d={name:data['metrics'][v][n][u] for name,data in c['documents'].items()};a={i:d[apps[i]] for i in ids};x=results[k]
  common=d['U_B']+d['U_B6'];num=sum(s.values());den=common+sum(a.values());article=num-s['L040']+source[k]['L040_article_only']
  need(x['source_costs']==s and x['applications']==a and x['document_costs']==d,'complete source/document vectors')
  need(x['whole_common']==common and x['source_sum']==num and x['whole_written']==den,'full costs')
  pairs={'written':(num,den),'L040_article_whole':(article,den),'L040_article_conditional':(source[k]['L040_article_only'],a['L040'])}
  pairs.update({'conditional_'+i:(s[i],a[i]) for i in ids})
  actual={'written':x['written'],'L040_article_whole':x['article_only_sensitivity']['written'],'L040_article_conditional':x['article_only_sensitivity']['L040_conditional']}
  actual.update({'conditional_'+i:z for i,z in x['conditional'].items()})
  for label,(numi,deni) in pairs.items():
   rec=f(numi,deni);need(rec==actual[label],'exact fraction '+str(k)+label);expected[k+(label,)]=rec
  for i in ids[:-1]:need(x['conditional'][i]==prior[k]['conditional'][i],'prior unchanged');preserved+=1
  need(x['article_only_sensitivity']['L040_conditional']==prior[k]['article_only_sensitivity']['L040_conditional'],'old article conditional');preserved_article+=1
  for i,z in s.items():costs[k+(i,'source')]=z
  for i,z in d.items():
   if i!='L047':costs[k+(i,'common' if i in ['U_B','U_B6'] else 'program_alternative' if i.startswith('CODE') else 'application')]=z
  ss=0;dd=d['U_B'];seq=[dict(stage=0,acquire=['U_B'],source_written=ss,replacement_written=dd)]
  for i in ids:
   if i=='L047':
    dd+=d['U_B6'];seq.append(dict(stage=len(seq),acquire=['U_B6'],source_written=ss,replacement_written=dd))
   ss+=s[i];dd+=a[i];seq.append(dict(stage=len(seq),source=i,acquire=[apps[i]],source_written=ss,replacement_written=dd))
  need(x['acquisition']==seq,'explicit acquisition stages')
  for z in seq:stages[k+(z['stage'],)]=(z['source_written'],z['replacement_written'])
 with (P/'fractions.csv').open() as h:rows=list(csv.DictReader(h))
 need(len(rows)==270,'CSV fraction size')
 for x in rows:
  z=expected.pop(key(x)+(x['comparison'],));need(all(str(val)==x[k] for k,val in z.items()),'CSV exact fraction')
 need(not expected,'all CSV fractions unique')
 with (P/'document_costs.csv').open() as h:rows=list(csv.DictReader(h))
 for x in rows:need(costs.pop(key(x)+(x['document'],x['role']))==int(x['cost']),'CSV cost')
 need(not costs,'CSV all costs')
 with (P/'acquisition.csv').open() as h:rows=list(csv.DictReader(h))
 for x in rows:need(stages.pop(key(x)+(int(x['stage']),))==(int(x['source_written']),int(x['replacement_written'])),'CSV acquisition')
 need(not stages,'CSV all acquisition stages')
 inventory=read(P/'inputs/current/precount/raw_inventory.json')['files'];got={x['id']:x for x in r['whole_file_inventory']};expectedraw={};groupcounts={}
 for x in inventory:
  z=c['raw_files'][x['category']][x['old_path']] if x['inherited'] else c['new_raw_files'][x['id']]
  group='operational_drivers' if x['category']=='drivers' else 'partial_formal_files' if x['category']=='formal' else 'optional_validation' if x['role']=='finite_validation' else 'required_or_auxiliary_programs'
  need(got[x['id']]['file']==x['file'] and got[x['id']]['metrics']==z['metrics'] and got[x['id']]['group']==group,'raw whole file role/values')
  groupcounts[group]=groupcounts.get(group,0)+1
  for n in ['NFC','NFKC']:
   for u in grid[0:5]:
    unit=u[2];expectedraw[(x['id'],n,unit)]=z['metrics'][n][unit]
 with (P/'raw_files.csv').open() as h:rows=list(csv.DictReader(h))
 need(len(rows)==170,'raw CSV170')
 for x in rows:need(expectedraw.pop((x['id'],x['normalization'],x['unit']))==int(x['cost']),'raw CSV value')
 need(not expectedraw and len(got)==17 and sorted(groupcounts.values())==[2,2,5,8],'whole raw vector')
 for k in ['software_inclusive_factor','optional_validation_inclusive_factor','pooled_factor','collective_conditional_factor']:need(r[k] is None,'no asymmetrical scalar')
 for group,number in groupcounts.items():
  records=[x for x in got.values() if x['group']==group];z=r['whole_file_groups'][group]
  need(z['files']==number and z['literal_bytes']==sum(x['file']['bytes'] for x in records),'whole bytes')
  for n in ['NFC','NFKC']:
   for _,_,u in grid[:5]:need(z['metrics'][n][u]==sum(x['metrics'][n][u] for x in records),'raw group totals')
 primary=results[('raw_untrimmed','NFC','characters_without_whitespace')]
 need(primary==r['primary'] and primary['written']==f(144877,149071),'fixed primary')
 return {'status':'PASS','author_manifest_sha256':AUTHOR,'exports_verified':85,'exact_fractions':270,'prior_conditionals_unchanged':preserved,'prior_article_conditionals_unchanged':preserved_article,'raw_cells':170,'primary':primary['written'],'L047_conditional':primary['conditional']['L047'],'method':'Direct independent integer arithmetic from previously adopted input vectors; no author arithmetic or presentation imports. Fresh author replay separately checks graphics and rendering.','scope':'Numerical comparison only; inherited mathematical and extraction reviews retained.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();p=Path(a.out);need(not p.exists(),'fresh output');r=run();p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
