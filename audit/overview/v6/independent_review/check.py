#!/usr/bin/env python3
"""Distinct current overview check; reuses pinned earlier root vector parser."""
from pathlib import Path
import argparse, copy, csv, hashlib, importlib.util, json, math
from pypdf import PdfReader
PIN = 'be15a2ef573f2694fa72eb9b9df77f7644937fbfc16aa6f1842013965dfa4a84'
VECTOR_PIN = 'eba42a6b2b3621aebe0cc5d9875bae33157b103ca369bf3e3335e2a55bffba5c'
AUTHOR = '7eb6e66ff1fdd291624a52ef86f2d54906c8a723aad6f9e6f99fbf9593782330'
REVIEW = '9e3d09defb11e1a289ea63308608724d7aabea2154777b2d240419c455d73316'
def need(ok,msg):
    if not ok: raise ValueError(msg)
def load(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ratio(n,d):
    g=math.gcd(n,d); q,r=divmod(n*10**12,d)
    if 2*r>d or (2*r==d and q%2):q+=1
    return dict(numerator=n,denominator=d,exact_fraction=str(n//g) if d==g else f'{n//g}/{d//g}',decimal=f'{q//10**12}.{q%10**12:012d}')
def prior_checker(public):
    p=public/'audit/overview/v3/independent_review/check.py';need(sha(p)==VECTOR_PIN,'pinned prior independent vector parser')
    s=importlib.util.spec_from_file_location('overview37_prior_vectors',p);q=importlib.util.module_from_spec(s);s.loader.exec_module(q);return q
def bindings(packet,public):
    routes={'previous_results':'audit/overview/v5/packet/results.json','previous_manifest':'audit/overview/v5/packet/manifest.json','previous_admission':'audit/overview/v5/admission.json','previous_review':'audit/overview/v5/independent_review/review.json',
      'RankContraction_results':'audit/topic-rank-contraction/v1/measurement/packet/results.json','RankContraction_manifest':'audit/topic-rank-contraction/v1/measurement/packet/manifest.json','RankContraction_protocol':'audit/topic-rank-contraction/v1/measurement/packet/protocol.json',
      'RankContraction_review':'audit/topic-rank-contraction/v1/measurement/independent_review/review.json','RankContraction_review_manifest':'audit/topic-rank-contraction/v1/measurement/independent_review/manifest.json'}
    p=load(packet/'protocol.json');need(set(p['bindings'])==set(routes),'all nine numerical inputs')
    for name,route in routes.items():
        row=p['bindings'][name];f=packet/row['local'];need(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'] and f.read_bytes()==(public/route).read_bytes(),'exact public input '+name)
    need(p['bindings']['RankContraction_manifest']['sha256']==AUTHOR and p['bindings']['RankContraction_review_manifest']['sha256']==REVIEW,'accepted numerical editions')
    return len(routes)
def arithmetic(data,public):
    prior=load(public/'audit/overview/v5/packet/results.json')
    need(data['topics'][:-1]==prior['topics'],'all fourteen complete earlier topic objects unchanged')
    need(data['topic_count']==len(data['topics'])==15 and data['original_manuscript_count']==37,'fifteen topics37 originals')
    need(data['registry_manuscripts']==161 and data['pooled_factor'] is None and not data['cross_topic_deduplication'] and not data['all_registry_manuscripts_completed'],'no pooled or whole corpus completion claim')
    need(data['pending_numerical_acceptance']==[] and data['pending_overview_review'] and data['currently_published_measured_originals']==36 and data['proposed_measured_originals']==37 and data['recovery_status_not_derived_from_measurement'],'preserved author stage')
    need(all(data[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no credit from overview')
    b=public/'audit/topic-rank-contraction/v1/measurement';p=load(b/'packet/results.json')['primary'];review=load(b/'independent_review/review.json')
    need(sha(b/'independent_review/manifest.json')==REVIEW and review['author_manifest_sha256']==AUTHOR and review['status']=='ROOT_ACCEPTED_COMPLETE_L037_NUMBERS','distinct numerical acceptance')
    t=data['topics'][-1];d=p['document_costs'];s,u,a,c=(d[k] for k in ['L037','U','A1','CODE']);raw=p['raw_program_cost']
    need(t['topic']=='RankContraction' and t['source_count']==1 and t['source_ids']==['L037'],'one new original')
    need(t['common_components']=={'whole_local_theory':u} and t['application_components']=={'RC1':{'complete_application_including_references':a}},'complete common and application')
    need((t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['printed_program_cost'],t['raw_program_alternative'])==(s,u,a,u+a,c,raw),'whole input amounts')
    need(t['conditional_prepaid']==dict(full_common=u,full_declared_printed_programs=c,total=u+c) and t['conditional_raw_alternative_prepaid']==dict(full_common=u,full_declared_raw_programs=raw,total=u+raw),'complete alternative acquisition')
    need(t['separate_raw_inventory']==dict(programs=raw,drivers=p['driver_cost_separate'],formal=p['formal_file_cost_separate']),'complete separate raw inventories')
    need(t['representation']=='raw_untrimmed_pdf' and t['normalization']=='NFC' and t['unit']=='characters_without_whitespace' and not t['old_Topic_B_common_free_premise'],'primary representation')
    need((t['entire_source_pages'],t['entire_common_pages'],t['entire_application_pages'],t['entire_program_pages'])==(6,[3],5,1),'entire page boundary')
    need(t['pairs']==[dict(source='L037',application='RC1',source_cost=s,application_cost=a,source_representation='complete_PDF_raw_untrimmed',conditional=ratio(s,a))],'complete new source/application')
    need('Conjecture5.1 remains open' in t['scientific_boundary'] and 'not a uniform contraction premise' in t['program_roles'],'question and computational limits')
    ids=[];count=0
    for t in data['topics']:
        need(t['common_theory']==sum(t['common_components'].values()) and t['source_sum']==sum(q['source_cost'] for q in t['pairs']) and t['applications_sum']==sum(q['application_cost'] for q in t['pairs']) and t['written_denominator']==t['common_theory']+t['applications_sum'],'every complete sum')
        for k,cost in [('written',0),('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:
            need(t[k]==(None if cost is None else ratio(t['source_sum'],t['written_denominator']+cost)),'exact combined comparison');count+=cost is not None
        if t.get('including_optional_validation') is not None:
            f=t['including_optional_validation'];need(f==ratio(f['numerator'],f['denominator']),'optional exact fraction');count+=1
        for q in t['pairs']:
            need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'exact individual fraction');count+=1;ids.append(q['source'])
        need(all(t[k] is None for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']),'unknowns stay null')
    need(len(ids)==len(set(ids))==37 and set(ids)=={q['source'] for t in prior['topics'] for q in t['pairs']}|{'L037'} and count==81,'37 originals81fractions')
    return count
def graphs(packet,data,old):
    n=0
    for stem in ['whole_topics','conditional_1','conditional_2']:
        bars=old.expected_bars(data,stem);svg=old.svg_rects((packet/(stem+'.svg')).read_bytes());ns=old.svg_costs(svg,bars);pdf,h=old.pdf_rects(packet/(stem+'.pdf'));need(old.pdf_costs(pdf,h,svg,bars,stem=='whole_topics')==ns,'actual vector bars');n+=ns
    need(n==147,'all147 actual cost rectangles');return n
def csv_check(packet,data):
    def strs(d):return {k:'' if v is None else str(v) for k,v in d.items()}
    rows=list(csv.DictReader((packet/'topics.csv').open()));apps=list(csv.DictReader((packet/'applications.csv').open()));need(len(rows)==15 and len(apps)==37,'52complete CSV rows')
    for row,t in zip(rows,data['topics']):
        expected=dict(topic=t['topic'],title=t['title'],originals=t['source_count'],representation=t['representation'],sources=t['source_sum'],common=t['common_theory'],applications=t['applications_sum'],written=t['written_denominator'],written_factor=t['written']['decimal'],printed_programs=t['printed_program_cost'],printed_factor=None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],raw_programs=t['raw_program_alternative'],raw_factor=None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],numerical_status=t.get('numerical_status','unchanged_admitted'))
        need(row==strs(expected),'every topic CSV cell')
    for row,(t,p) in zip(apps,[(t,p) for t in data['topics'] for p in t['pairs']]):
        op=t['topic']=='Operations';expected=dict(topic=t['topic'],title=t['title'],source=p['source'],application=p['application'],source_cost=p['source_cost'],application_cost=p['application_cost'],conditional_exact=p['conditional']['exact_fraction'],conditional_factor=p['conditional']['decimal'],full_common_prepaid=t['common_theory'],full_program_or_software_prepaid=t['raw_program_alternative'] if op else t['printed_program_cost'],acquisition_representation='whole_raw_software_and_external_data' if op else 'whole_printed_programs',source_representation=p['source_representation'])
        need(row==strs(expected),'every application CSV cell')
def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,required=True);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'bound author overview edition')
    for r in load(a.packet/'manifest.json')['exports']:
        f=a.packet/r['path'];need(f.stat().st_size==r['bytes'] and sha(f)==r['sha256'],'complete exports')
    nb=bindings(a.packet,a.public_root);d=load(a.packet/'results.json');nf=arithmetic(d,a.public_root);old=prior_checker(a.public_root);ng=graphs(a.packet,d,old);csv_check(a.packet,d)
    pages=PdfReader(a.packet/'summary.pdf').pages;need(len(pages)==6,'six pages');text='\n'.join(p.extract_text() or '' for p in pages);need(all(p['source'] in text for t in d['topics'] for p in t['pairs']),'all37 source labels')
    controls=[]
    for name,mut in [('alter earlier topic',lambda d:d['topics'][0].update(common_theory=0)),('omit whole common',lambda d:d['topics'][-1]['common_components'].clear()),('omit reference page',lambda d:d['topics'][-1].update(entire_application_pages=4)),('both code alternatives added',lambda d:d['topics'][-1].update(raw_program_alternative=5426)),('free old B theory',lambda d:d['topics'][-1].update(old_Topic_B_common_free_premise=True)),('incomplete acquisition',lambda d:d['topics'][-1]['conditional_prepaid'].update(total=6937)),('unknown external cost zero',lambda d:d['topics'][-1].update(external_proof_cost=0)),('claim conjecture solved',lambda d:d['topics'][-1].update(scientific_boundary='all solved')),('round exact fraction',lambda d:d['topics'][-1]['written'].update(exact_fraction='0.888')),('pooled estimate',lambda d:d.update(pooled_factor=1)),('free cross-topic theory',lambda d:d.update(cross_topic_deduplication=True))]:
        bad=copy.deepcopy(d);mut(bad)
        try:arithmetic(bad,a.public_root)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted mutation '+name)
    bars=old.expected_bars(d,'whole_topics');sv=old.svg_rects((a.packet/'whole_topics.svg').read_bytes());bad=copy.deepcopy(sv);key='bar-RankContraction-common-whole_local_theory';x,y,w,h=bad[key];bad[key]=(x,y,w+1,h)
    try:old.svg_costs(bad,bars)
    except ValueError:controls.append('distorted new SVG common')
    else:raise ValueError('accepted SVG mutation')
    pdf,H=old.pdf_rects(a.packet/'whole_topics.pdf');bad=copy.deepcopy(pdf);role,x,y,w,h=bad[-4];bad[-4]=(role,x,y,w+1,h)
    try:old.pdf_costs(bad,H,sv,bars,True)
    except ValueError:controls.append('distorted new PDF application')
    else:raise ValueError('accepted PDF mutation')
    report=dict(status='PASS_DISTINCT_OVERVIEW37',author_manifest_sha256=PIN,input_bindings=nb,topics=15,distinct_originals=37,exact_comparisons=nf,actual_SVG_bars=ng,actual_PDF_bars=ng,CSV_rows=52,reader_pages=6,controls_rejected=controls,author_implementation_imported=False,prior_independent_vector_parser_reused=True,primary_reextraction=False,new_mathematical_credit=0)
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
