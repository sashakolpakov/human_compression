#!/usr/bin/env python3
"""Independent exact arithmetic, CSV and actual vector geometry; no author imports."""
import argparse,copy,csv,hashlib,json,math,re
import xml.etree.ElementTree as ET
from pathlib import Path
from pypdf import PdfReader
PIN='0d548c296855637641592e539c4401895ac38c4c094eaf6f6aa8923f57e058a4'
INPUT='396355b0cc7fac4c1c0af5a18af4a148195b8abebdbd49699a10c7cfdf21cb74'
REVIEW='53338911b067231c2ae68188a22d3e630147fb82be0af814253fa040aab9237c'
def need(b,m):
    if not b:raise ValueError(m)
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def fraction(n,d):
    g=math.gcd(n,d);a,b=n//g,d//g
    return dict(numerator=n,denominator=d,reduced_numerator=a,reduced_denominator=b,exact_fraction=str(a) if b==1 else f'{a}/{b}',factor=n/d)
def inputs(packet):
    for folder,pin in [('inputs',INPUT),('input_review',REVIEW)]:
        need(sha(packet/folder/'manifest.json')==pin,'accepted input edition')
        for e in load(packet/folder/'manifest.json')['exports']:
            f=packet/folder/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'all accepted input exports')
    a=load(packet/'inputs/author_counts.json');r=load(packet/'input_review/recount.json')
    need(a['raw_files']==r['raw_files'],'all raw counts independently agree')
    for k,d in a['documents'].items():
        need(all(d[f]==r['documents'][k][f] for f in ['pages','pdf_sha256','metrics']),'all PDF counts independently agree')
    return a
def expected(a):
    rows={}
    for v in ['raw_untrimmed','raw_selected','calibrated_selected']:
        for n in ['NFC','NFKC']:
            for unit in ['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']:
                d={k:t['metrics'][v][n][unit] for k,t in a['documents'].items()};raw={k:sum(t['metrics'][n][unit] for t in vals.values()) for k,vals in a['raw_files'].items()}
                s=d['L084']+d['L095'];u=d['U']+d['TABLES'];app=d['A1']+d['A2'];code=d['CODE'];rp=raw['programs'];data=raw['required_data']
                rows[v,n,unit]=dict(variant=v,normalization=n,unit=unit,document_costs=d,source_cost=s,whole_common_cost=u,application_cost=app,written_cost=u+app,printed_program_cost=code,raw_program_cost=rp,mandatory_data_cost=data,operational_driver_cost_separate=raw['operational_drivers'],comparisons={'written_papers':fraction(s,u+app),'printed_programs_plus_mandatory_data':fraction(s,u+app+code+data),'raw_programs_plus_mandatory_data':fraction(s,u+app+rp+data)},conditional_applications={'L084':fraction(d['L084'],d['A1']),'L095':fraction(d['L095'],d['A2'])},conditional_acquisition=dict(common_proof=d['U'],common_tables=d['TABLES'],whole_common=u,printed_program_option=code,raw_program_option=rp,mandatory_raw_data=data,printed_total=u+code+data,raw_total=u+rp+data))
    return rows
def validate(d,rows):
    need(len(d['coordinates'])==30,'all coordinates')
    actual={(x['variant'],x['normalization'],x['unit']):x for x in d['coordinates']}
    need(actual==rows and d['coordinates_count']==30 and d['exact_combined_fractions']==90 and d['exact_conditional_fractions']==60,'all150 exact fractions and complete costs')
    p=rows['calibrated_selected','NFC','characters_without_whitespace'];need(d['primary']==p,'accepted calibrated primary')
    need(d['originals']==2 and d['source_ids']==['L084','L095'] and d['source_record_count']==52 and d['historical_rows']==145,'original/row accounting')
    need(d['whole_common_charged_once'] and d['complete_common_documents']==['U','TABLES'] and d['all_applications_charged'] and not d['cross_topic_discount'] and not d['sibling_application_free_premise'],'full common and local boundary')
    b=d['programme_boundary'];need(b['complete_required_programs']==6 and b['raw_program_bytes']==24255 and b['complete_printed_program_pages']==6 and b['required_data_files']==1 and b['required_data_bytes']==39150 and b['required_data_in_both_routes'] and not b['printed_program_is_data_substitute'] and b['printed_and_raw_are_alternatives'],'whole programs plus whole compulsory data')
    need(b['operational_drivers_separate']==3 and b['driver_raw_bytes']==32220 and b['generated_outputs_separate']==11 and b['generated_output_bytes']==3470182 and b['output_not_additional_enumeration_input'] and b['formal_files']==b['formal_declarations']==0,'separate driver, generated output and formal boundaries')
    need(all(v is None for v in d['unknown_costs'].values()) and len(d['unknown_costs'])==5,'unknown costs not zero')
    need(d['physical_extent']==dict(source_pages={'L084':2,'L095':15},common_proof_pages=7,common_tables_pages=5,application_pages={'L084':2,'L095':3},written_replacement_pages=17,printed_program_pages=6,all_input_pages=40),'complete source and replacement pages')
    need(not d['full_source_formalized'] and d['new_source_credit']==d['new_question_credit']==0,'no formal or question credit')
    return p
def csvs(packet,rows):
    sizes={}
    for name,n in [('overall_costs',90),('conditional_costs',60),('document_costs',210),('software_costs',120),('acquisition_costs',30)]:
        rr=list(csv.DictReader((packet/(name+'.csv')).open()));need(len(rr)==n,'complete CSV row count');seen=set()
        for r in rr:
            key=tuple(r[k] for k in ['variant','normalization','unit']);c=rows[key]
            if name=='overall_costs':label=r['comparison'];fields=c['comparisons'][label]
            elif name=='conditional_costs':
                label=r['source'];fields=c['conditional_applications'][label];need(r['application']=={'L084':'A1','L095':'A2'}[label] and r['prepaid']=='Whole U + whole TABLES + all six programs + entire source_tables.json + retained inputs','CSV prior acquisition')
            elif name=='document_costs':label=r['document'];fields={'cost':c['document_costs'][label]}
            elif name=='software_costs':label=r['role'];fields={'cost':c[label]}
            else:label='acquisition';fields=c['conditional_acquisition']
            need(key+(label,) not in seen,'no duplicate CSV cells');seen.add(key+(label,));need(all(r[k]==str(v) for k,v in fields.items()),'every CSV value')
        sizes[name]=n
    return sizes
def vectors(packet,stem,wanted):
    # Read rendered paths and visible tick labels, not the author's plot_data.
    parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True));root=ET.parse(packet/(stem+'.svg'),parser).getroot();ns={'s':'http://www.w3.org/2000/svg'};svg=[];ticks=[]
    for g in root.findall('.//s:g',ns):
        ident=g.attrib.get('id','')
        if ident.startswith('xtick_'):
            p=g.find('.//s:path',ns);comments=[e.text for e in g.iter() if e.tag is ET.Comment]
            if p is not None and comments:
                xy=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.attrib['d'])));ticks.append((xy[0],float(comments[0].strip().replace(',',''))))
        if ident.startswith('patch_'):
            p=g.find('s:path',ns)
            if p is None:continue
            nums=list(map(float,re.findall(r'-?\d+(?:\.\d+)?',p.attrib['d'])))
            if len(nums)!=8:continue
            xs,ys=nums[::2],nums[1::2];h=max(ys)-min(ys)
            if 9<h<35:svg.append((min(xs),min(ys),max(xs)-min(xs),h))
    need(len(ticks)>=3 and ticks[0][1]==0,'actual zero tick');origin=ticks[0][0];scale=(ticks[1][0]-origin)/ticks[1][1]
    need(all(abs(x-origin-v*scale)<3e-6 for x,v in ticks),'actual linear tick scale')
    page=PdfReader(packet/(stem+'.pdf')).pages[0];pdf=[];poly=[]
    for a,o in page.get_contents().operations:
        if o==b'm':poly=[tuple(map(float,a))]
        elif o==b'l':poly.append(tuple(map(float,a)))
        elif o in [b'f',b'B']:
            if len(poly)==4:
                xs,ys=zip(*poly);h=max(ys)-min(ys)
                if 9<h<35:pdf.append((min(xs),float(page.mediabox.height)-max(ys),max(xs)-min(xs),h))
            poly=[]
    count=sum(map(len,wanted));need(len(svg)==len(pdf)==count,'all actual rectangles')
    for rectangles in [svg,pdf]:
        groups={}
        for x,y,w,h in rectangles:groups.setdefault(round(y,4),[]).append((x,w))
        need(len(groups)==len(wanted),'all actual rows')
        for (_,group),target in zip(sorted(groups.items()),wanted):
            need(len(group)==len(target),'complete component row');start=0
            for (x,w),value in zip(sorted(group),target):
                need(abs((x-origin)/scale-start)<.002 and abs(w/scale-value)<.002,'actual stacked width and origin');start+=value
    need(all(all(abs(a-b)<3e-6 for a,b in zip(x,y)) for x,y in zip(sorted(svg),sorted(pdf))),'SVG/PDF agreement')
    return count
def graphs(packet,p):
    u=p['whole_common_cost'];a=p['application_cost'];m=p['mandatory_data_cost'];d=p['document_costs']
    n=vectors(packet,'costs',[[p['source_cost']],[u,a],[u,a,p['printed_program_cost'],m],[u,a,p['raw_program_cost'],m]])
    n+=vectors(packet,'documents',[[d['L084']],[d['L095']],[u],[d['A1']],[d['A2']]])
    need(n==16,'all sixteen vector rectangles');return n
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();need(not a.out.exists(),'fresh output')
    need(sha(a.packet/'manifest.json')==PIN,'reviewed numerical edition')
    for e in load(a.packet/'manifest.json')['exports']:
        f=a.packet/e['path'];need(f.stat().st_size==e['bytes'] and sha(f)==e['sha256'],'frozen numerical export')
    rows=expected(inputs(a.packet));d=load(a.packet/'results.json');primary=validate(d,rows);sizes=csvs(a.packet,rows);n=graphs(a.packet,primary)
    controls=[]
    for name,mut in [('drop common tables',lambda d:d['coordinates'][0].update(whole_common_cost=0)),('drop mandatory data',lambda d:d['coordinates'][0].update(mandatory_data_cost=0)),('printed plus raw code',lambda d:d['coordinates'][0].update(raw_program_cost=1)),('omit acquisition data',lambda d:d['coordinates'][0]['conditional_acquisition'].update(mandatory_raw_data=0)),('corrupt fraction',lambda d:d['coordinates'][0]['comparisons']['written_papers'].update(denominator=1)),('wrong raw primary',lambda d:d.update(primary=d['coordinates'][2])),('charge sibling free',lambda d:d.update(sibling_application_free_premise=True)),('cross-topic discount',lambda d:d.update(cross_topic_discount=True)),('missing mandatory file',lambda d:d['programme_boundary'].update(required_data_bytes=0)),('unknown cost zero',lambda d:d['unknown_costs'].update(historical_software=0)),('claim formal proofs',lambda d:d['programme_boundary'].update(formal_declarations=1)),('replace15pbyjournal',lambda d:d['physical_extent']['source_pages'].update(L095=12))]:
        bad=copy.deepcopy(d);mut(bad)
        try:validate(bad,rows)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('accepted corruption '+name)
    report=dict(status='PASS_DISTINCT_LOCALLY_PROJECTIVE_NUMBERS',coordinates=30,exact_fractions=150,CSV_rows=sizes,actual_SVG_rectangles=n,actual_PDF_rectangles=n,cost_bars=9,independent_controls=controls,author_modules_imported=False,primary_extraction_repeated=False,science_repeated=False,primary=primary)
    a.out.mkdir(parents=True);(a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='primary'}))
if __name__=='__main__':main()
