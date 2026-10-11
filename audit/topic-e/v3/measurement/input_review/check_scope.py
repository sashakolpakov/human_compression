#!/usr/bin/env python3
"""Independent boundary, whole-file and reader checks. No author checker import."""
from pathlib import Path
from collections import Counter
import argparse,copy,csv,hashlib,json,re
from recount import require,metric,apply_mask,own_cuts
PAGES={'L079':9,'L083':14,'L021':11,'L056':8,'L043':25,'U':20,'A1':2,'A2':1,'A3':5,'A4':2,'A5':4,'REQUIRED':20,'VALIDATION':7}
SOURCES=['L079','L083','L021','L056','L043']
WRITTEN=['U','A1','A2','A3','A4','A5']
APPS={'L083':['A1'],'L079':['A2'],'L021':['A3'],'L056':['A4'],'L043':['A5']}
ROLES={'required_finite.g':'required finite proof','exceptional_amalgams.g':'required finite proof','exceptional_small.g':'required finite proof','small_rotation_exclusions.g':'required finite proof','psl2_square_bound_check.py':'required finite proof','verify_square_witnesses.py':'required finite proof','psl2_square_witnesses.json':'required certificate data','validation.g':'validation only','pointed_models.g':'validation only','source_clause_571.g':'validation only','psl2_square_witnesses.g':'validation only','psl2_nested_witnesses.g':'validation only','psl2_intersection_check.g':'validation only'}
PRIMARY={'variant':'raw_untrimmed','normalization':'NFC','unit':'characters_without_whitespace'}
def check_boundary(d):
 p=d['policy'];s=d['software'];f=d['formal'];g=d['graphics'];a=d['aliases']
 require(p['source_ids']==SOURCES and p['original_count']==5,'five exact originals')
 require({k:v['pages']for k,v in p['documents'].items()}==PAGES,'whole thirteen documents/128 pages')
 require(p['whole_common']==['U'] and p['written_documents']==WRITTEN,'whole U and five applications')
 require(p['applications']==APPS,'source/application routing')
 require(p['primary_coordinate']==PRIMARY,'fixed raw primary')
 require(p['variants']==['raw_untrimmed','raw_selected','calibrated_selected'] and p['normalizations']==['NFC','NFKC'] and len(p['units'])==5,'all30 coordinates')
 require(p['required_printed_alternative']==['REQUIRED'] and p['optional_validation_printed_alternative']==['VALIDATION'],'separate printed alternatives')
 require({Path(x['path']).name:x['role']for x in p['programs_and_data']}==ROLES and len(p['programs_and_data'])==13,'six required, one mandatory JSON, six optional whole files')
 require(len(p['operational_drivers'])==5 and len(p['formal_files'])==7,'separate drivers/formal inventory')
 require(p['formal_declarations']==42 and p['new_formal_declarations']==9 and f['reported_declarations']==42 and f['new_declarations']==9,'partial declaration counts')
 require(sum(len(x['declarations'])for x in f['modules'])==42 and len(f['modules'])==7 and len(f['not_formalized'])==6,'partial formal boundary')
 sym=p['symmetry_policy'];require(sym['historical_software_cost']is None and sym['inclusive_software_factor']is None,'unknown historical software')
 require(sym['optional_validation'].startswith('Excluded on both sides') and 'no one-sided' in sym['optional_validation'],'symmetric optional exclusion')
 require(sym['no_cross_topic_free_premise']is True and sym['no_printed_plus_raw_double_charge']is True,'no free umbrella or double charge')
 require('whole common theory, six required programmes, mandatory JSON and retained mathematical premises' in sym['conditional'],'full conditional prepayment')
 require(all(x is None for x in p['unknown_costs'].values()),'unknown costs stay null')
 require(p['factors_permitted']is False and p['ratio']is None and p['new_source_credit']==p['new_question_credit']==0,'input-only scope')
 require(s['full_source_software_listing_present']is False and s['own_optional_listings_inside_scientific_papers']is False and s['source_pdf_pages_scanned']==67 and s['own_scientific_pages_scanned']==34,'matched listing boundary')
 require(s['historical_unprovided_executables']is None and s['matched_inclusive_software_factor']is None,'unprovided software not zero')
 require(set(g)==set(PAGES) and all(v['physical_pages']==PAGES[k] and len(v['pages'])==PAGES[k] and all(x['graphic_cost']is None for x in v['pages']) for k,v in g.items()),'all graphics inventoried/null')
 require(len(a)==19 and sum(x['occurrences']for x in a)==279,'full calibrated class/occurrence boundary')
 for x in a:
  require(len(x['input'])==len(x['output'])==1,'literal one-piece glyph proxy')
  require('font_dictionary_object' in x and x['font_identity'] and x['font_dictionary_sha256'],'actual font dictionary key')
  if x['glyph_name']=='mapsto':require(x['output']=='∣','mapsto piece not invented full arrow')
 require(p['new_source_dispositions']==56 and p['retained_source_dispositions']==54,'accepted dispositions retained')

def csv_check(packet,p,c):
 n=0
 with (packet/'document_counts.csv').open(newline='')as h:
  rows=list(csv.DictReader(h));require(len(rows)==390,'all PDF CSV cells')
 for x in rows:
  m=c['documents'][x['document']]['metrics'][x['variant']][x['normalization']]
  require(int(x['physical_pages'])==PAGES[x['document']]and int(x['count'])==m[x['unit']]and x['text_sha256']==m['normalized_text_sha256'],'PDF CSV coordinate');n+=1
 with (packet/'raw_counts.csv').open(newline='')as h:rows=list(csv.DictReader(h));require(len(rows)==250,'all raw CSV cells')
 for x in rows:
  m=c['raw_files'][x['category']][x['path']]['metrics'][x['normalization']]
  require(int(x['count'])==m[x['unit']]and x['text_sha256']==m['normalized_text_sha256'],'raw CSV coordinate');n+=1
 return n

def run(packet,root):
 load=lambda n:json.loads((packet/n).read_text());p=load('policy.json')
 d={'policy':p,'software':load('source_software_boundary.json'),'formal':load('formal_scope.json'),'graphics':load('graphics_inventory.json'),'aliases':load('glyph_aliases.json')['aliases']}
 check_boundary(d);controls=[]
 def reject(name,change):
  q=copy.deepcopy(d);change(q)
  try:check_boundary(q)
  except(ValueError,KeyError):controls.append({'control':name,'rejected':True});return
  raise ValueError('survived: '+name)
 reject('drop source',lambda q:q['policy']['source_ids'].pop())
 reject('shorten common paper',lambda q:q['policy']['documents']['U'].__setitem__('pages',19))
 reject('drop application',lambda q:q['policy']['written_documents'].pop())
 reject('wrong A1/A2 source routing',lambda q:q['policy']['applications'].__setitem__('L083',['A2']))
 reject('selected primary substitution',lambda q:q['policy']['primary_coordinate'].__setitem__('variant','calibrated_selected'))
 reject('drop required witness JSON',lambda q:q['policy']['programs_and_data'].pop())
 reject('required code relabelled optional',lambda q:q['policy']['programs_and_data'][0].__setitem__('role','validation only'))
 reject('optional appendix required',lambda q:q['policy'].__setitem__('required_printed_alternative',['REQUIRED','VALIDATION']))
 reject('driver omitted',lambda q:q['policy']['operational_drivers'].pop())
 reject('historical software set zero',lambda q:q['policy']['symmetry_policy'].__setitem__('historical_software_cost',0))
 reject('source-only validation exclusion',lambda q:q['policy']['symmetry_policy'].__setitem__('optional_validation','Excluded only from ours'))
 reject('free cross-topic common theory',lambda q:q['policy']['symmetry_policy'].__setitem__('no_cross_topic_free_premise',False))
 reject('printed and raw charged twice',lambda q:q['policy']['symmetry_policy'].__setitem__('no_printed_plus_raw_double_charge',False))
 reject('conditional data acquisition missing',lambda q:q['policy']['symmetry_policy'].__setitem__('conditional','Only common theory acquired'))
 reject('graphics unknown priced zero',lambda q:q['graphics']['L079']['pages'][0].__setitem__('graphic_cost',0))
 reject('full formal claim',lambda q:q['formal'].__setitem__('not_formalized',[]))
 reject('ratio prematurely licensed',lambda q:q['policy'].__setitem__('factors_permitted',True))
 reject('embedded source listing overlooked',lambda q:q['software'].__setitem__('full_source_software_listing_present',True))
 reject('optional code in scientific PDF overlooked',lambda q:q['software'].__setitem__('own_optional_listings_inside_scientific_papers',True))
 reject('glyph occurrence lost',lambda q:q['aliases'][0].__setitem__('occurrences',q['aliases'][0]['occurrences']-1))
 reject('semantic formula reconstruction',lambda q:q['aliases'][0].__setitem__('output','P(x)'))
 reject('BaseFont-only dictionary key',lambda q:q['aliases'][0].pop('font_dictionary_object'))
 reject('source qualification dropped',lambda q:q['policy'].__setitem__('new_source_dispositions',55))
 c=load('author_counts.json');n=csv_check(packet,p,c)
 def reject_call(name,fn):
  try:fn()
  except(ValueError,KeyError):controls.append({'control':name,'rejected':True});return
  raise ValueError('survived: '+name)
 changed=copy.deepcopy(c);changed['documents']['L043']['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']+=1
 reject_call('changed PDF count against independently recounted CSV',lambda:csv_check(packet,p,changed))
 changedraw=copy.deepcopy(c);row=p['programs_and_data'][0];changedraw['raw_files']['programs_and_data'][row['path']]['metrics']['NFKC']['whitespace_tokens']+=1
 reject_call('changed whole raw-file count',lambda:csv_check(packet,p,changedraw))
 reject_call('overlapping selection ranges',lambda:apply_mask('abcde',[(0,3),(2,4)]))
 reject_call('unverified title removal as running header',lambda:own_cuts('L079',['title\n1','Not the declared running header\nBody']))
 tex=(packet/'reader.tex').read_text()
 for k,v in p['documents'].items():
  m=c['documents'][k]['metrics']['raw_untrimmed']['NFC']['characters_without_whitespace']
  require(re.search(r'(?m)^'+re.escape(k)+r'\s*&.*?&\s*'+str(v['pages'])+r'\s*&\s*'+f'{m:,}'+r'\s*\\\\',tex),'reader exact primary row '+k)
 for phrase in ['whole 20-page common paper','all five applications','all six required finite-proof programs','mandatory JSON','Optional validation is excluded on both sides','historical software has unknown cost','They do not formalize the full','All 30 coordinates','not a compression result']:
  require(phrase in ' '.join(tex.split()),'reader boundary '+phrase)
 # Independent elementary fixture disambiguates bytes, normalization and whitespace.
 sample='e\u0301  α_2\nﬃ';m=metric(sample,'NFC');require(m['whitespace_tokens']==3 and m['alphanumeric_units']==4 and m['characters_without_whitespace']==5 and m['characters_with_collapsed_whitespace']==7 and m['utf8_bytes_with_collapsed_whitespace']==11,'independent metric fixture NFC')
 m=metric(sample,'NFKC');require(m['characters_without_whitespace']==7 and m['utf8_bytes_with_collapsed_whitespace']==11,'independent metric fixture NFKC')
 return {'status':'PASS_INDEPENDENT_SCOPE_AND_CONTROLS','controls':controls,'negative_controls':len(controls),'csv_cells':n,'reader_primary_rows':13,'ratios_evaluated':False,'mathematics_reexecuted':False,'shared_author_checker_imports':False}
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--packet',type=Path,required=True);a.add_argument('--study-root',type=Path,required=True);a.add_argument('--out',type=Path,required=True);x=a.parse_args();require(not x.out.exists(),'fresh result');r=run(x.packet,x.study_root);x.out.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
