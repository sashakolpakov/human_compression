#!/usr/bin/env python3
"""Author checks use exact input integers, not rounded reader decimals."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,json,csv,copy,re,xml.etree.ElementTree as ET
import pypdf
from pypdf.generic import ContentStream
HERE=Path(__file__).resolve().parent
COLORS={'source':(98/255,108/255,118/255),'common':(66/255,107/255,154/255),'application':(112/255,165/255,154/255),'program':(189/255,135/255,78/255)}
def need(ok,m):
 if not ok:raise ValueError('ADDITIONAL_NUMERIC_CHECK: '+m)
def arithmetic(result,counts):
 need(result['original_manuscripts']==2 and result['source_ids']==['F015','L028'] and result['independent_topics']==2,'exact two-original boundary')
 need(result['new_source_credit']==result['new_question_credit']==0 and not result['full_formalization_claim'],'no new credit')
 need(all(x is None for x in result['unknown_costs'].values()),'unknown costs remain null')
 ids={'Matching':['F015','U_M','M1','M_CODE'],'ChiralEnumeration':['L028','U_CE','CE1','CE_CODE']};seen=set();number=0
 for row in result['rows']:
  t,v,n,u=row['topic'],row['variant'],row['normalization'],row['unit'];coord=(t,v,n,u);need(coord not in seen,'one row per coordinate');seen.add(coord)
  nums=[counts['documents'][k]['metrics'][v][n][u] for k in ids[t]];s,common,app,printed=nums
  raw={cat:sum(x['metrics'][n][u] for x in files.values() if x['topic']==t) for cat,files in counts['raw_files'].items()}
  need(row['document_costs']==dict(zip(['source','common','application','program'],nums)) and row['raw_costs']==raw,'all complete components')
  need(row['written_denominator']==common+app,'whole common theory paid')
  a=row['conditional_acquisition'];need(a['whole_common_cost']==common and a['whole_printed_program_cost']==printed and a['whole_raw_program_cost']==raw['complete_programs'] and a['printed_and_raw_are_alternatives'],'whole acquisition before conditional comparison')
  denoms={'written':common+app,'including_printed_programs':common+app+printed,'including_raw_programs':common+app+raw['complete_programs'],'conditional_application':app};need(set(row['comparisons'])==set(denoms),'four complete comparisons')
  for name,denom in denoms.items():
   q=row['comparisons'][name];f=Fraction(s,denom)
   with localcontext() as c:c.prec=40;dec=str(Decimal(s)/Decimal(denom))
   need(q==dict(numerator=s,denominator=denom,reduced_numerator=f.numerator,reduced_denominator=f.denominator,decimal=dec),'exact whole fraction '+name);number+=1
 need(len(seen)==60 and number==240,'all coordinates')
 for t,row in result['primary'].items():need(row==next(x for x in result['rows'] if (x['topic'],x['variant'],x['normalization'],x['unit'])==(t,'calibrated_selected','NFC','characters_without_whitespace')),'primary points to exact row')
 return number

def svg_heights(data):
 out={};root=ET.fromstring(data)
 for node in root.iter():
  key=node.attrib.get('id','')
  if not key.startswith('bar-'):continue
  path=next((n for n in node.iter() if n.tag.endswith('path')),None);need(path is not None,'actual plotted path')
  values=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?',path.attrib['d'])];need(len(values)==8,'actual four-vertex rectangle');ys=values[1::2];out[key]=max(ys)-min(ys)
 return out

def expected_bars(r):
 out=[]
 for t,row in r['primary'].items():
  d=row['document_costs']
  for name,cost in [('source',d['source']),('common-written',d['common']),('application-written',d['application']),('common-printed',d['common']),('application-printed',d['application']),('program',d['program'])]:out.append(('bar-'+t+'-'+name,cost,name.split('-')[0]))
 return out

def check_svg(data,r):
 h=svg_heights(data);bars=expected_bars(r);need(set(h)=={x[0] for x in bars},'all twelve real bars')
 scale=h[bars[0][0]]/bars[0][1]
 for key,cost,_ in bars:need(abs(h[key]-cost*scale)<2e-5,'actual SVG height '+key)
 return len(h)

def pdf_heights(path):
 r=pypdf.PdfReader(path);need(len(r.pages)==1,'one complete plot page');rgb=None;points=[];out=[]
 for operands,op in ContentStream(r.pages[0].get_contents(),r).operations:
  if op==b'rg':rgb=tuple(float(x) for x in operands)
  elif op==b'g':rgb=(float(operands[0]),)*3
  elif op==b'm':points=[(float(operands[0]),float(operands[1]))]
  elif op==b'l':points.append((float(operands[0]),float(operands[1])))
  elif op in (b'f',b'f*',b'B',b'B*'):
   role=next((k for k,c in COLORS.items() if rgb and all(abs(x-y)<1e-7 for x,y in zip(rgb,c))),None)
   if role and len(points) in (4,5):out.append((role,max(y for x,y in points)-min(y for x,y in points)))
   points=[]
 need(len(out)==16 and all(abs(h-5.6)<1e-6 for _,h in out[-4:]) and [x[0] for x in out[-4:]]==list(COLORS),'four separate legend swatches')
 return out[:-4]

def check_pdf(path,r):
 got=pdf_heights(path);expected=expected_bars(r);need(len(got)==len(expected)==12,'all twelve actual PDF rectangles');scale=got[0][1]/expected[0][1]
 for (role,height),(_,cost,want) in zip(got,expected):need(role==want and abs(height-cost*scale)<2e-5,'actual PDF rectangle/color')
 return len(got)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--packet',type=Path,default=HERE);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh report')
 p=json.loads((HERE/'protocol.json').read_text());counts=json.loads((a.study_root/p['bindings']['counts']['path']).read_text());r=json.loads((a.packet/'results.json').read_text());number=arithmetic(r,counts)
 csvrows=list(csv.DictReader((a.packet/'comparisons.csv').open()));expect=[]
 for row in r['rows']:
  for name,q in row['comparisons'].items():expect.append(dict(zip(['topic','source','variant','normalization','unit','comparison','numerator','denominator','decimal'],[row['topic'],row['source_id'],row['variant'],row['normalization'],row['unit'],name,str(q['numerator']),str(q['denominator']),q['decimal']])))
 need(csvrows==expect,'240 exact CSV comparisons');svg=(a.packet/'whole_costs.svg').read_text();sg=check_svg(svg,r);pg=check_pdf(a.packet/'whole_costs.pdf',r)
 controls=[]
 def reject(name,fn):
  try:fn()
  except (ValueError,KeyError,TypeError,StopIteration):controls.append(name);return
  raise ValueError('accepted corrupt control '+name)
 def mutate(fn):
  x=copy.deepcopy(r);fn(x);arithmetic(x,counts)
 reject('drop coordinate',lambda:mutate(lambda x:x['rows'].pop()))
 reject('duplicate coordinate',lambda:mutate(lambda x:x['rows'].append(copy.deepcopy(x['rows'][0]))))
 reject('common theory made free',lambda:mutate(lambda x:x['rows'][0]['document_costs'].update(common=0)))
 reject('truncate program charge',lambda:mutate(lambda x:x['rows'][0]['document_costs'].update(program=1)))
 reject('raw software omitted',lambda:mutate(lambda x:x['rows'][0]['raw_costs'].update(complete_programs=0)))
 reject('printed and raw charged together',lambda:mutate(lambda x:x['rows'][0]['comparisons']['including_printed_programs'].update(denominator=999)))
 reject('conditional cost pays no complete acquisition',lambda:mutate(lambda x:x['rows'][0]['conditional_acquisition'].update(whole_common_cost=0)))
 reject('rounded decimal changed',lambda:mutate(lambda x:x['rows'][0]['comparisons']['written'].update(decimal='2')))
 reject('source count uses clause count',lambda:mutate(lambda x:x.update(original_manuscripts=64)))
 reject('external proof cost zero',lambda:mutate(lambda x:x['unknown_costs'].update(retained_external=0)))
 reject('full formalization inferred',lambda:mutate(lambda x:x.update(full_formalization_claim=True)))
 root=ET.fromstring(svg);target=next(x for x in root.iter() if x.attrib.get('id')=='bar-Matching-common-written');path=next(x for x in target.iter() if x.tag.endswith('path'));v=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?',path.attrib['d'])];v[3]+=5;v[5]+=5;path.attrib['d']=f'M {v[0]} {v[1]} L {v[2]} {v[3]} L {v[4]} {v[5]} L {v[6]} {v[7]} z';reject('distorted actual bar',lambda:check_svg(ET.tostring(root).decode(),r))
 text='\n'.join(x.extract_text() or '' for x in pypdf.PdfReader(a.packet/'measurement.pdf').pages);need(len(pypdf.PdfReader(a.packet/'measurement.pdf').pages)==2,'two reader pages')
 for row in r['primary'].values():
  for q in row['comparisons'].values():need(f"{float(q['decimal']):.3f}" in text,'reader factor')
 report=dict(status='AUTHOR_CHECK_PASS_PENDING_DISTINCT_REVIEW',exact_fractions=number,csv_rows=len(csvrows),actual_svg_rectangles=sg,actual_pdf_rectangles=pg,semantic_controls=controls,reader_pages=2,scientific_programs_executed=False)
 a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
