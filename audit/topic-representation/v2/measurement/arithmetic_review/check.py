#!/usr/bin/env python3
"""Independent complete-cost arithmetic; no author arithmetic imports.

Accepted primitive counts are reused. No primary/font extraction, scientific
program or Lean replay is performed. Rational reduction and decimal rounding
use integer operations; actual SVG rectangles are checked against the counts.
"""
import argparse,copy,csv,hashlib,itertools,json,math,re
from pathlib import Path
import xml.etree.ElementTree as ET
PINS={'inputs':'122820fac69c94d484444a88b4318fa7ae1a588770c4378737af7d457a037af1','input_review':'d9b130046c95f625946762a4414fc294d2366e5bed3803aae783bb43967b69f3','input_adoption':'c6cd89907ac02b7384fb887e93e3d4f941dcab2f963cc9156341cbeb5b2a24c5','numbers':'8a0c2a30ac88b0d703b5082ce8a2426d8da82f27dea94558f0005a5b29d76c03'}
V=('raw_untrimmed','raw_selected','calibrated_selected');N=('NFC','NFKC')
U=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
RAW=('complete_validation_programs','complete_operational_drivers','complete_formal_files')
ORDER=('written_papers','conditional_application','including_printed_validation','including_raw_validation_alternative')
PRIMARY=('calibrated_selected','NFC','characters_without_whitespace')

def need(b,s):
    if not b:raise ValueError(s)
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rounded(n,d,places):
    q,r=divmod(n*10**places,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    a,b=divmod(q,10**places);return f'{a}.{b:0{places}d}'
def fraction(n,d):
    need(type(n)is int and type(d)is int and n>0 and d>0,'positive integer fraction');g=math.gcd(n,d);a,b=n//g,d//g
    return dict(numerator=n,denominator=d,reduced_numerator=a,reduced_denominator=b,exact_fraction=str(a) if b==1 else f'{a}/{b}',decimal=rounded(n,d,12))
def key(r):return r['variant'],r['normalization'],r['unit']
def calculate(counts):
    need(set(counts['documents'])=={'F010','U_R','R1','CODE'},'four complete documents')
    need([len(counts[k]) for k in RAW]==[2,2,2],'whole files')
    rows={};csvrows=[]
    for v,n,u in itertools.product(V,N,U):
        c={name:d['variants'][v][n][u] for name,d in counts['documents'].items()};raw={k:sum(x['metrics'][n][u] for x in counts[k].values()) for k in RAW}
        whole=c['U_R']+c['R1'];den=[whole,c['R1'],whole+c['CODE'],whole+raw[RAW[0]]]
        comps={name:fraction(c['F010'],d) for name,d in zip(ORDER,den)}
        rows[v,n,u]=dict(variant=v,normalization=n,unit=u,document_costs=c,raw_costs=raw,source_sum=c['F010'],written_denominator=whole,comparisons=comps,acquired_common=c['U_R'],acquired_printed_validation=c['CODE'],acquired_raw_validation_alternative=raw[RAW[0]])
        for name,f in comps.items():csvrows.append(dict(variant=v,normalization=n,unit=u,comparison=name,**f))
    return rows,csvrows

def verify(r,expected,counts,scope,bindings):
    rows={key(x):x for x in r['coordinates']};need(len(r['coordinates'])==len(rows)==30 and rows==expected,'all thirty full coordinate records')
    need(r['primary']==expected[PRIMARY],'fixed primary coordinate')
    need((r['coordinate_count'],r['exact_fraction_count'],r['combined_exact_fractions'],r['conditional_exact_fractions'])==(30,120,90,30),'fraction totals')
    need(tuple(r['comparison_order'])==ORDER,'declared comparisons')
    need(r['whole_common_once'] and r['whole_application'] and not r['cross_topic_discount'],'whole topic charging')
    need(r['conditional_prepaid']=='After acquiring the whole U_R and both complete validation programs; neither program is a uniform written-proof premise.','complete conditional acquisition')
    need(r['source_to_application_sequence']==[dict(source='F010',application='R1',source_pages=13,application_pages=5)],'source/application pairing')
    need(r['physical_pages']==dict(source=13,common=5,application=5,written_replacement=10,printed_validation=4,total_inputs=27),'full physical documents')
    need(r['source_contract_rows']==6 and r['accepted_proof_contexts']==13 and r['principal_contracts_unchanged']==1,'fixed principal contract')
    need(r['source_qualifications']==scope['source_qualifications'] and r['source_exclusions']==scope['exclusions'] and r['original_authors']==scope['attribution'],'exact original attribution, corrections and exclusions')
    b=r['program_boundary'];need([b[k] for k in ['complete_validation_programs','uniform_finite_proof_premises','complete_operational_drivers_separate','complete_Lean_files_separate','prior_partial_Lean_declarations','formal_generic','formal_reused_local']]==[2,0,2,2,12,8,4],'whole files and partial formal scope')
    need(not any(b[k] for k in ['full_application_formalized','drivers_added_to_comparisons','Lean_added_to_comparisons']),'no auxiliary inflation')
    need(b['primary_representation']=='Whole4-page printed appendix counted once' and b['alternative_representation']=='Both complete raw files summed per file, never added to the appendix','alternative code representations')
    need(r['raw_file_inventory']=={k:counts[k] for k in RAW},'all raw bytes inventories')
    need(all(r[k] is None for k in ['retained_external_proof_cost','historical_program_cost','graphics_and_formula_layout_cost','operational_engineering_cost','minimal_mathematical_complexity']),'unknown costs remain null')
    need(not any(r[k] for k in ['full_visible_graphical_text_claim','sawtooth_claim','primary_text_fonts_images_exported']),'bounded presentation claims')
    need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new credits')
    need(r['source_question_answer']=='Original Theorem A already answers Question2.4; no new answer.','question attribution')
    need(r['input_bindings']==bindings,'exact numerical input routing')
    utf=expected['calibrated_selected','NFC',U[-1]]['comparisons']['written_papers'];primary=expected[PRIMARY]['comparisons']['written_papers']
    need(utf['numerator']<utf['denominator'] and primary['numerator']>primary['denominator'],'unit-sensitive reversal preserved')

def chart(svg,p):
    root=ET.fromstring(svg);ns={'s':'http://www.w3.org/2000/svg'};c=p['document_costs']
    expected=[([c['F010'],c['U_R'],c['R1'],c['U_R'],c['R1'],c['CODE']],['#686868','#426b9a','#70a59a','#426b9a','#70a59a','#bd874e']),([c['U_R'],c['R1'],c['CODE']],['#426b9a','#70a59a','#bd874e'])];total=0
    for k,(values,colors) in enumerate(expected,1):
        axis=root.find(f'.//s:g[@id="axes_{k}"]',ns);need(axis is not None,'two plot axes');bars=[];bottom=None
        for g in axis.findall('s:g',ns):
            if not g.get('id','').startswith('patch_'):continue
            for path in g.findall('s:path',ns):
                nums=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?',path.get('d',''))]
                if path.get('style')=='fill: #ffffff':bottom=max(nums[1::2])
                if 'clip-path' not in path.attrib:continue
                need(len(nums)==8,'bar rectangle');bars.append((min(nums[1::2]),max(nums[1::2]),min(nums[::2]),max(nums[::2]),path.get('style')))
        need(len(bars)==len(values) and bottom is not None,'complete bars')
        scale=(bars[0][1]-bars[0][0])/values[0]
        for bar,val,col in zip(bars,values,colors):need(abs(bar[1]-bar[0]-scale*val)<0.00002 and col in bar[4],'actual rectangle height or role color')
        starts=[0,1,3] if k==1 else [0,1,2]
        need(all(abs(bars[j][1]-bottom)<0.000001 for j in starts),'zero-axis baseline')
        if k==1:
            for lower,upper in [(1,2),(3,4),(4,5)]:need(abs(bars[lower][0]-bars[upper][1])<0.000001 and bars[lower][2:4]==bars[upper][2:4],'whole common/application/validation stack')
        total+=len(bars)
    for value in [c['F010'],p['written_denominator'],p['written_denominator']+c['CODE'],c['U_R'],c['R1'],c['CODE']]:need(f'<!-- {value:,} -->' in svg,'plot count labels')
    return total

def reader(tex,r):
    p=r['primary'];c=p['document_costs'];whole=p['written_denominator']
    for value in [*c.values(),whole,whole+c['CODE'],whole+p['raw_costs'][RAW[0]],*p['raw_costs'].values(),c['F010']-whole]:need(str(value) in tex,'displayed complete counts')
    for f in p['comparisons'].values():need(rounded(f['numerator'],f['denominator'],6) in tex,'headline rounded fraction')
    for row in r['coordinates']:
        if row['variant']=='calibrated_selected' and row['normalization']=='NFC':
            for name in ORDER[:3]:
                f=row['comparisons'][name];need(rounded(f['numerator'],f['denominator'],3) in tex,'sensitivity rounding')
    for text in ['After acquiring the whole common paper and both complete validation\nprograms','Neither program is a premise of the uniform written proof.','never simultaneous charges','The UTF-8 written factor is below one','not\nstable across these units','The original Theorem A already answers Question 2.4','they do not formalize the complete application','engineering remain unknown, not zero','single application supplies no evidence of a recurring sawtooth pattern','not claim recovery of every historical auxiliary assertion']:
        need(text in tex,'reader qualification '+text)

def main():
    ap=argparse.ArgumentParser()
    for k in PINS:ap.add_argument('--'+k.replace('_','-'),type=Path,required=True)
    ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();need(not a.out.exists(),'fresh output directory')
    roots={k:getattr(a,k) for k in PINS};bound=[]
    for k,root in roots.items():
        need(sha(root/'manifest.json')==PINS[k],'manifest '+k);rows=read(root/'manifest.json')['exports']
        for row in rows:
            p=root/row['path'];need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'export '+str(p))
        bound.append(dict(role=k,path=str(root/'manifest.json'),sha256=PINS[k],exports=len(rows)))
    counts=read(a.inputs/'author_counts.json');ind=read(a.input_review/'independent_replay.json');policy=read(a.inputs/'policy.json');scope=read(a.inputs/'source_contract_boundary.json')
    need(counts['documents']==ind['documents'] and all(counts[k]==ind['raw_files'][k] for k in RAW),'accepted independent primitive counts')
    need(read(a.input_review/'review.json')['status']=='ACCEPTED_INDEPENDENT_REPRESENTATION_MEASUREMENT_INPUTS' and read(a.input_adoption/'review.json')['status']=='ROOT_ACCEPTED_REPRESENTATION_MEASUREMENT_INPUTS','distinct accepted extraction')
    need(tuple(policy['variants'])==V and tuple(policy['normalizations'])==N and tuple(policy['units'])==U,'fixed rulers')
    need(scope['row_count']==6 and len(scope['proof_spans'])==13 and scope['principal_contracts']==1 and not policy['comparison_policy']['cross_topic_deduplication'],'complete scope and topic boundary')
    need(all(x['classification']=='validation' and x['complete_original_file'] and not x['uniform_written_proof_premise'] for x in policy['program_roster']) and len(policy['program_roster'])==2,'validation boundary')
    mapping=read(a.input_adoption/'public_mapping.json');bindings=read(a.numbers/'input_bindings.json')
    need(bindings['accepted_manifest_sha256']=={k:PINS[k] for k in PINS if k!='numbers'} and bindings['published_artifacts']==mapping['artifacts'],'input manifest/mapping boundary')
    for row in mapping['artifacts']:need(sha(a.public_root/row['path'])==row['sha256'],'published scientific bytes '+row['path'])
    for k,items in bindings['accepted_metadata'].items():
        for row in items:need(sha(roots[k]/row['path'])==row['sha256'],'accepted metadata')
    expected,csvrows=calculate(counts);result=read(a.numbers/'results.json');verify(result,expected,counts,scope,bindings)
    with (a.numbers/'comparisons.csv').open(newline='') as f:actual=list(csv.DictReader(f))
    need(actual==[{k:str(v) for k,v in row.items()} for row in csvrows],'all 120 CSV fractions')
    controls=[]
    tests=[('drop_common',lambda d:d['coordinates'][0]['comparisons']['written_papers'].update(denominator=d['coordinates'][0]['document_costs']['R1'])),('drop_application',lambda d:d.update(whole_application=False)),('wrong_late_fraction',lambda d:d['coordinates'][-1]['comparisons']['including_raw_validation_alternative'].update(numerator=1)),('decimal_only_error',lambda d:d['coordinates'][3]['comparisons']['written_papers'].update(decimal='1.000000000000')),('conditional_not_prepaid',lambda d:d.update(conditional_prepaid='Only R1')),('double_charge_code',lambda d:d['coordinates'][1]['comparisons']['including_raw_validation_alternative'].update(denominator=d['coordinates'][1]['written_denominator']+d['coordinates'][1]['document_costs']['CODE']+d['coordinates'][1]['raw_costs'][RAW[0]])),('drop_validation_file',lambda d:d['raw_file_inventory'][RAW[0]].pop(next(iter(d['raw_file_inventory'][RAW[0]])))),('add_drivers_to_main',lambda d:d['program_boundary'].update(drivers_added_to_comparisons=True)),('validation_as_premise',lambda d:d['program_boundary'].update(uniform_finite_proof_premises=2)),('full_formalization',lambda d:d['program_boundary'].update(full_application_formalized=True)),('wrong_Lean_count',lambda d:d['program_boundary'].update(prior_partial_Lean_declarations=24)),('erase_correction',lambda d:d['source_qualifications'].pop()),('erase_exclusion',lambda d:d['source_exclusions'].pop()),('new_question_answer',lambda d:d.update(new_question_credit=1)),('unknown_graphics_zero',lambda d:d.update(graphics_and_formula_layout_cost=0)),('unknown_external_zero',lambda d:d.update(retained_external_proof_cost=0)),('cross_topic_discount',lambda d:d.update(cross_topic_discount=True)),('sawtooth_claim',lambda d:d.update(sawtooth_claim=True)),('omit_coordinate',lambda d:d['coordinates'].pop()),('swap_primary',lambda d:d.update(primary=d['coordinates'][0])),('omit_source_page',lambda d:d['physical_pages'].update(source=12)),('erase_UTF8_reversal',lambda d:d['coordinates'][24]['comparisons']['written_papers'].update(numerator=40000))]
    for name,change in tests:
        d=copy.deepcopy(result);change(d)
        try:verify(d,expected,counts,scope,bindings)
        except ValueError as e:controls.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('accepted control '+name)
    svg=(a.numbers/'complete_costs.svg').read_text();tex=(a.numbers/'measurement.tex').read_text();bar_count=chart(svg,result['primary']);reader(tex,result)
    # Preserve original XML comments: this mutation changes only rectangle height,
    # so it cannot pass merely because serialization discarded a value label.
    badsvg=svg.replace('L 139.857255 78.29994','L 139.857255 79.29994').replace('L 64.524955 78.29994','L 64.524955 79.29994');need(badsvg!=svg,'bar perturbation applied')
    presentation=[]
    for name,check in [('distorted_actual_height',lambda:chart(badsvg,result['primary'])),('hide_unit_reversal',lambda:reader(tex.replace('The UTF-8 written factor is below one','All written units compress'),result)),('hide_prepaid_programs',lambda:reader(tex.replace('both complete validation\nprograms','some programs'),result))]:
        try:check()
        except ValueError as e:presentation.append(dict(name=name,rejected=True,reason=str(e)))
        else:raise ValueError('accepted presentation control '+name)
    author=read(a.numbers/'author_check.json');need(author['control_count']==24 and all(x['rejected'] for x in author['controls']),'bound author controls')
    a.out.mkdir(parents=True)
    with (a.out/'fractions.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(csvrows[0]));w.writeheader();w.writerows(csvrows)
    report={'status':'PASS_INDEPENDENT_REPRESENTATION_NUMERICAL_REVIEW','input_bindings':bound,'method':'No author arithmetic imports. Accepted distinct extraction counts; gcd reduction and integer nearest-even rounding. All actual CSV fractions and SVG bar heights checked.','pdf_count_cells':120,'raw_count_cells':60,'coordinates':30,'combined_fractions':90,'conditional_fractions':30,'all_exact_fractions':120,'csv_rows_checked':120,'primary':expected[PRIMARY],'calibrated_NFC_UTF8_written':expected['calibrated_selected','NFC',U[-1]]['comparisons']['written_papers'],'controls':controls,'presentation_controls':presentation,'bar_rectangles_checked':bar_count,'bound_author_controls':24,'primary_reextraction':False,'scientific_program_or_Lean_replay':False,'public_files_edited':False,'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0}
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'status':report['status'],'fractions':120,'controls':len(controls)+len(presentation),'bars':bar_count}))
if __name__=='__main__':main()
