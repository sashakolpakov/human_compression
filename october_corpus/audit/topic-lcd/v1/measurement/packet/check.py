"""Complete integer/CSV boundary checks and targeted semantic mutations."""
import copy,csv,json
from calculate import need,calculate,validate,read,row,ROLES
from presentation import records,fraction_records,raw_records,occurrence_records,graph

def validate_against_inputs(r,expected):
 validate(r);need(r==expected,'exact accepted vectors and complete scope')
def controls(r):
 cases=[]
 def case(name,change):
  z=copy.deepcopy(r);change(z)
  try:validate_against_inputs(z,r)
  except (ValueError,KeyError,StopIteration):cases.append(name)
  else:raise ValueError('mutation accepted: '+name)
 case('omit whole common from denominator',lambda z:z['coordinates'][0]['comparisons']['written'].__setitem__('denominator',z['coordinates'][0]['totals']['applications']))
 case('omit complete L050 application',lambda z:z['coordinates'][0]['costs'].__setitem__('A_L050',0))
 case('swap conditional source/application routes',lambda z:z['coordinates'][0]['comparisons'].__setitem__('conditional_L050',z['coordinates'][0]['comparisons']['conditional_F017']))
 case('change fixed primary to raw',lambda z:z.__setitem__('primary_coordinate',['raw_untrimmed','NFC','characters_without_whitespace']))
 case('drop one sensitivity',lambda z:z['coordinates'].pop())
 def coherent(z):
  old=z['coordinates'][0];cost=old['costs'].copy();cost['L050']+=1;z['coordinates'][0]=row(old['variant'],old['normalization'],old['unit'],cost,old['raw_costs'])
 case('coherent arithmetic from altered accepted count',coherent)
 case('invent software-inclusive factor',lambda z:z['scope'].__setitem__('software_inclusive_factor',1))
 case('unknown historical software becomes zero',lambda z:z['scope'].__setitem__('source_software_cost',0))
 case('omit required whole file from acquisition',lambda z:z['acquisition']['required_whole_content_sha256'].pop())
 case('make optional validation required',lambda z:z['scope'].__setitem__('optional_validation_required_for_conditional',True))
 case('introduce sibling application premise',lambda z:z['scope'].__setitem__('no_sibling_application_dependency',False))
 case('claim full formalization',lambda z:z['scope'].__setitem__('full_source_formalized',True))
 case('double-count reused nine declarations',lambda z:z['scope'].__setitem__('unique_partial_Lean_declarations',18))
 case('describe primary expansion as compression',lambda z:z['interpretation'].__setitem__('whole_topic','Achieved whole-topic compression.'))
 case('drop complete raw program',lambda z:z['raw_file_inventory']['files'].pop())
 case('drop duplicate occurrence disclosure',lambda z:z['raw_file_inventory']['occurrence_bindings'].pop())
 case('relabel required data as optional',lambda z:next(x for x in z['raw_file_inventory']['files']if x['role']=='required_data').__setitem__('role','optional_validation'))
 case('invent printed code manuscript',lambda z:z['scope'].__setitem__('printed_CODE_document_present',True))
 case('omit common stage cost',lambda z:z['acquisition']['complete_written_stages'].__setitem__(0,0))
 case('give new original credit',lambda z:z.__setitem__('new_source_credit',1))
 case('convert external proofs unknown to zero',lambda z:z['unknown_costs'].__setitem__('full_external_proofs',0))
 return cases

def csvcheck(root,name,expected):
 with(root/name).open(newline='')as f:rows=list(csv.reader(f))
 need(rows[1:]==[[str(x)for x in row]for row in expected],'complete CSV '+name)
 return len(rows)-1

def check(root,expected=None):
 expected=calculate(root)if expected is None else expected;r=read(root/'results.json');validate_against_inputs(r,expected)
 csvrows={
  'costs':csvcheck(root,'costs.csv',records(r)),
  'fractions':csvcheck(root,'fractions.csv',fraction_records(r)),
  'raw_files':csvcheck(root,'raw_files.csv',raw_records(r)),
  'raw_occurrences':csvcheck(root,'raw_occurrences.csv',occurrence_records(r)),
  'acquisition':csvcheck(root,'acquisition.csv',[[x['variant'],x['normalization'],x['unit'],stage,cost]for x in r['coordinates']for stage,cost in zip(['whole_common','common_and_L050','common_and_both_apps'],x['acquisition']['common_then_L050_then_F017'])])}
 need(csvrows=={'costs':390,'fractions':90,'raw_files':1020,'raw_occurrences':127,'acquisition':90},'all CSV row scopes')
 need(read(root/'acquisition.json')==r['acquisition'],'complete acquisition records')
 need(read(root/'document_graph.json')==graph(r),'declared document associations')
 return dict(coordinates=30,written_fractions=30,conditional_fractions=60,accepted_PDF_cells=150,accepted_raw_cells=1020,CSV_rows=csvrows,semantic_controls=controls(r))
