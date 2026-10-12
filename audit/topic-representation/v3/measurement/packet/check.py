"""Bounded numerical/control checker; exact accepted counts only."""
import copy,csv,json
from calculate import need,calculate,validate,COMPARE,ROLES,sha,read
from presentation import records,graph

def validate_against_inputs(r,expected):
 validate(r);need(r==expected,'exact accepted input vectors and complete metadata')
def controls(r):
 cases=[]
 def case(name,change):
  z=copy.deepcopy(r);change(z)
  try:validate_against_inputs(z,r)
  except (ValueError,KeyError,StopIteration):cases.append(name)
  else:raise ValueError('mutation accepted: '+name)
 case('omit complete common from denominator',lambda z:z['coordinates'][0]['comparisons']['written'].__setitem__('denominator',z['coordinates'][0]['totals']['applications']))
 case('omit R1 after shared proof relocation',lambda z:z['coordinates'][0]['costs'].__setitem__('R1',0))
 case('wrong source/application route',lambda z:z['coordinates'][0]['comparisons'].__setitem__('conditional_F010',z['coordinates'][0]['comparisons']['conditional_L126']))
 case('switch inherited primary to raw',lambda z:z.__setitem__('primary_coordinate',['raw_untrimmed','NFC','characters_without_whitespace']))
 case('lose a sensitivity',lambda z:z['coordinates'].pop())
 case('change accepted source count coherently',lambda z:z['coordinates'][0]['costs'].__setitem__('F010',z['coordinates'][0]['costs']['F010']+1))
 case('invent software factor',lambda z:z['scope'].__setitem__('software_inclusive_factor',1))
 case('treat source software unknown as zero',lambda z:z['scope'].__setitem__('source_software_cost',0))
 case('omit required graph JSON',lambda z:z['acquisition']['L126_required_software'].pop())
 case('make optional checks required',lambda z:z['scope'].__setitem__('optional_validation_required_for_conditional',True))
 case('restore sibling application premise',lambda z:z['scope'].__setitem__('no_sibling_application_dependency',False))
 case('claim whole formal proof',lambda z:z['scope'].__setitem__('full_source_formalized',True))
 case('claim whole-topic compression',lambda z:z['interpretation'].__setitem__('whole_topic','Achieved compression.'))
 case('drop complete raw program file',lambda z:z['raw_file_inventory']['files'].pop(0))
 case('give new source credit',lambda z:z.__setitem__('new_source_credit',1))
 return cases

def check(root,expected=None):
 expected=calculate(root)if expected is None else expected;r=read(root/'results.json');validate_against_inputs(r,expected)
 with(root/'costs.csv').open(newline='')as f:rows=list(csv.reader(f));need(rows[1:]==[[str(x)for x in row]for row in records(r)],'all330 PDF/role CSV rows')
 with(root/'fractions.csv').open(newline='')as f:fr=list(csv.reader(f));wanted=[]
 for x in r['coordinates']:
  for k in COMPARE:wanted.append([str(q)for q in[x['variant'],x['normalization'],x['unit'],k]+list(x['comparisons'][k].values())])
 need(fr[1:]==wanted,'all90 exact fraction CSV rows')
 with(root/'raw_files.csv').open(newline='')as f:rr=list(csv.DictReader(f))
 a=read(root/'inputs/input_author_counts.json');wanted=[]
 for x in r['raw_file_inventory']['files']:
  for form in ['NFC','NFKC']:
   for unit in __import__('calculate').UNITS:wanted.append(dict(file=x['key'],role=x['role'],whole_bytes=str(x['bytes']),sha256=x['sha256'],normalization=form,unit=unit,cost=str(a['raw_files'][x['key']]['metrics'][form][unit])))
 need(rr==wanted,'all170 whole-file CSV rows')
 need(read(root/'acquisition.json')==r['acquisition'],'complete acquisition costs')
 need(read(root/'document_graph.json')==graph(r),'graph associations')
 return {'coordinates':30,'written_fractions':30,'conditional_fractions':60,'cost_CSV_rows':len(rows)-1,'fraction_CSV_rows':len(fr)-1,'raw_CSV_rows':len(rr),'semantic_controls':controls(r)}
