#!/usr/bin/env python3
"""Independent integer/gcd derivation from accepted input cells; no author imports."""
import argparse,hashlib,json,math,pathlib
VARIANTS=('raw_untrimmed','raw_selected','calibrated_selected')
FORMS=('NFC','NFKC')
UNITS=('whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace')
PRIMARY=('calibrated_selected','NFC','characters_without_whitespace')

def need(v,s):
    if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text())
def fraction(a,b):
    need(isinstance(a,int)and isinstance(b,int)and a>0 and b>0,'positive integral costs');g=math.gcd(a,b)
    scaled,remainder=divmod(a*10**12,b)
    if 2*remainder>b or (2*remainder==b and scaled%2):scaled+=1
    decimal=f'{scaled//10**12}.{scaled%10**12:012d}'
    return dict(numerator=a,denominator=b,reduced_numerator=a//g,reduced_denominator=b//g,decimal_12=decimal)
def derive(study):
    pins={'topic_Representation_L126_measurement_inputs_v2/manifest.json':'4c61d955ddc8178c759e7943cde62deefb3c6696878a54d095146e207e5c8b29','topic_Representation_L126_measurement_independent_review/manifest.json':'3c103ab2a8991bbbd532e572b5fead2940783de74bcb71d480263d102be6f8f1','topic_Representation_L126_measurement_input_root_adoption/manifest.json':'6455c8cb576814818bd563dcb12d776aeff829fbebfad19d90686f7736334a1e'}
    for path,want in pins.items():
        p=study/path;need(sha(p.read_bytes())==want,'accepted pin '+path)
        for row in read(p)['exports']:
            data=(p.parent/row['path']).read_bytes();need(len(data)==row['bytes']and sha(data)==row['sha256'],'accepted export '+row['path'])
    # Use this reviewer's prior independently recounted cells, equal to the
    # distinctly adopted author input, rather than any numerical author helper.
    prior=read(study/'topic_Representation_L126_measurement_independent_review/independent_counts.json')
    input=read(study/'topic_Representation_L126_measurement_inputs_v2/author_counts.json')
    need(prior['documents']==input['documents']and prior['raw_files']==input['raw_files'],'both accepted recounts agree')
    coordinates=[]
    for variant in VARIANTS:
        for form in FORMS:
            for unit in UNITS:
                d={k:x['variants'][variant][form][unit]for k,x in prior['documents'].items()}
                complete=d['U_R']+d['R1']+d['R2'];source=d['F010']+d['L126']
                coordinates.append(dict(variant=variant,normalization=form,unit=unit,documents=d,whole_written=fraction(source,complete),conditional={'F010':fraction(d['F010'],d['R1']),'L126':fraction(d['L126'],d['R2'])},software_inclusive_factor=None,pooled_factor=None))
    raw=[]
    for form in FORMS:
        for unit in UNITS:
            groups={}
            for x in prior['raw_files'].values():groups[x['role']]=groups.get(x['role'],0)+x['metrics'][form][unit]
            raw.append(dict(normalization=form,unit=unit,whole_role_counts=groups))
    main=next(x for x in coordinates if(x['variant'],x['normalization'],x['unit'])==PRIMARY)
    return dict(status='INDEPENDENT_DERIVATION_READY_FOR_DISTINCT_AUTHOR_PACKET_REVIEW',accepted_input_manifests=pins,policy_coordinates=30,whole_written_fractions=30,conditional_fractions=60,primary_coordinate=dict(zip(['variant','normalization','unit'],PRIMARY)),coordinates=coordinates,primary=main,raw_inventory=raw,acquisition={'F010':{'complete_written_prepaid':['U_R'],'required_software_prepaid':[],'retained_classical_proofs':'explicit scientific premises; full cost unknown'},'L126':{'complete_written_prepaid':['U_R'],'required_software_prepaid':['certificate/check.py','certificate/graph.json'],'optional_programs_prepaid':False,'retained_classical_proofs':'explicit scientific premises; full cost unknown'}},whole_program_bytes={'required_certificate':8030,'mandatory_graph_json':19326,'nine_optional_programs':35601,'two_current_drivers':16622,'four_partial_Lean_files':15931},unknown_software_inclusive_factor=None,new_source_credit=0,new_question_credit=0)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=pathlib.Path,required=True);p.add_argument('--out',type=pathlib.Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output');r=derive(a.study_root);a.out.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n');print(json.dumps({'status':r['status'],'policy_coordinates':30,'fractions':90,'primary':r['primary']}))
