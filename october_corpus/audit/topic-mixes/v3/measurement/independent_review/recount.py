#!/usr/bin/env python3
"""Independent numerical review from accepted inputs; no author calculation import."""
import argparse
import csv
import hashlib
import importlib.util
import itertools
import json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

MANIFEST = '1ee537a6b90e83f6d812570a4b900928724d3f8f0bf2e20f684b54522fe9cf1d'
SOURCES = ['F005','L016','F007']
COMMON = ['U','U1','U2']
APPS = {'F005':['A1','A2'],'L016':['A3'],'F007':['A4','A5']}
VARIANTS = ['raw_untrimmed','raw_selected','calibrated_selected']
NORMS = ['NFC','NFKC']
UNITS = ['whitespace_tokens','alphanumeric_units','characters_without_whitespace',
         'characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']


def need(t,m):
    if not t:
        raise RuntimeError(m)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return json.loads(p.read_text())


def fraction(a,b):
    f=Fraction(a,b)
    with localcontext() as ctx:
        ctx.prec=60
        decimal=format(Decimal(a)/Decimal(b),'.12f')
    return dict(source_cost=a,replacement_cost=b,numerator=f.numerator,
                denominator=f.denominator,exact_fraction=str(f),decimal=decimal)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--packet',type=Path,required=True)
    ap.add_argument('--study',type=Path)
    ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();p=args.packet
    need(not args.out.exists(),'fresh review output')
    need(sha(p/'manifest.json')==MANIFEST,'reviewed frozen edition')
    manifests=[p/'manifest.json']+[p/'inputs'/x/'manifest.json' for x in ['input','input_review','input_adoption']]
    checked=0
    for m in manifests:
        for row in read(m)['exports']:
            q=m.parent/row['path']
            need(len(q.read_bytes())==row['bytes'] and sha(q)==row['sha256'],'frozen export '+str(q))
            checked+=1
    old=read(p/'inputs/input/retained_counts.json')
    new=read(p/'inputs/input/author_counts.json')
    need(new['retained_accepted_inputs']==old,'retained inputs')
    docs=dict(old['documents'])
    need(set(docs).isdisjoint(new['documents']),'document identities')
    docs.update(new['documents'])
    reviewed=read(p/'inputs/input_review/recount.json')
    for key,row in new['documents'].items():
        need(row['metrics']==reviewed['new_metrics'][key],'reviewed new counts')
    raw={}
    groups={}
    required={'topic_Mix_F005_recovery/check_coprime.g','topic_Mix_L016_recovery/base_certificate.g'}
    for group in ['programs','drivers','formal']:
        a=old['raw_files'][group];b=new['raw_files'][group]
        need(set(a).isdisjoint(b),'raw duplicates')
        for path,row in {**a,**b}.items():
            raw[path]=row
            groups[path]=('required_finite_certificate' if path in required else 'optional_validation') if group=='programs' else ('operational_driver' if group=='drivers' else 'partial_formal_evidence')
            if args.study:
                q=args.study/path
                need(sha(q)==row['sha256'] and len(q.read_bytes())==row['bytes'],'complete raw file')
    r=read(p/'results.json')
    need(r['source_ids']==SOURCES and r['common_documents']==COMMON and r['application_documents']==APPS,'full boundary')
    need(r['primary_coordinate']=='raw_untrimmed/NFC/characters_without_whitespace','primary chosen in advance')
    need(r['source_cells_unchanged']==450 and r['raw_cells_unchanged']==170,'all accepted cells')
    need(r['source_pages']==62 and r['whole_common_pages']==13 and r['inventory_pages']==114,'page inventory')
    expected_pdf=[];expected_fractions=[];expected_whole=[]
    expected_coordinates={}
    for v,n,u in itertools.product(VARIANTS,NORMS,UNITS):
        key='/'.join([v,n,u]);cost={k:d['metrics'][v][n][u] for k,d in docs.items()}
        source=sum(cost[s] for s in SOURCES);common=sum(cost[s] for s in COMMON)
        apps={s:sum(cost[a] for a in APPS[s]) for s in SOURCES}
        c=r['coordinates'][key]
        need(c['document_costs']==cost,'full PDF metric vector '+key)
        need((c['source_sum'],c['whole_common'],c['application_sum'],c['whole_written'])==(source,common,sum(apps.values()),common+sum(apps.values())),'whole arithmetic '+key)
        need(c['application_bundles']==apps,'both companion papers charged')
        expected_coordinates[key]=(cost,source,common,apps)
        for label,num,den in [('whole_topic',source,common+sum(apps.values()))]+[(s,cost[s],apps[s]) for s in SOURCES]:
            f=fraction(num,den)
            observed=c['written'] if label=='whole_topic' else c['conditional'][label]
            need(observed==f,'exact fraction '+key+label)
            expected_fractions.append(dict(coordinate=key,comparison=label,**f))
        for d,val in cost.items():
            expected_pdf.append(dict(coordinate=key,document=d,cost=val,physical_pages=docs[d]['pages']))
        for group in set(groups.values()):
            total=sum(row['metrics'][n][u] for path,row in raw.items() if groups[path]==group)
            need(c['separate_inventory'][group]==total,'separate whole-program inventory')
        for field in ['software_inclusive_factor','original_software_cost','full_optional_printed_representation']:
            need(c['separate_inventory'][field] is None,'unknown is not zero')
    for path,row in raw.items():
        for n,u in itertools.product(NORMS,UNITS):
            expected_whole.append(dict(path=path,role=groups[path],literal_bytes=row['bytes'],sha256=row['sha256'],normalization=n,unit=u,cost=row['metrics'][n][u]))
    for name,rows in [('fractions.csv',expected_fractions),('document_costs.csv',expected_pdf),('whole_files.csv',expected_whole)]:
        actual=list(csv.DictReader((p/name).open()))
        normalize=lambda row:tuple(sorted((k,str(v))for k,v in row.items()))
        need(sorted(map(normalize,actual))==sorted(map(normalize,rows)),'all CSV rows '+name)
    primary=r['coordinates'][r['primary_coordinate']]
    need(r['primary']==primary,'primary identity')
    src=0;ours=primary['whole_common'];acq=list(csv.DictReader((p/'acquisition.csv').open()))
    for i,row in enumerate(acq):
        if i:
            s=SOURCES[i-1];src+=primary['document_costs'][s];ours+=primary['application_bundles'][s]
        need((int(row['source_written']),int(row['replacement_written']))==(src,ours),'acquisition accumulation')
        need(row['whole_common_paid']=='True' and row['required_certificates_prepaid']=='True','prepaid premises')
    need(len(acq)==4,'all acquisition rows')
    for field in ['software_inclusive_factors','optional_validation_inclusive_factors','historical_source_software_cost']:
        need(r[field] is None,'no invented software comparison')
    for field in ['new_source_credit','new_question_credit','new_formal_credit']:
        need(r[field]==0,'no arithmetic science credit')
    need(r['full_source_formalized'] is False and r['sawtooth_claim'] is False,'bounded claims')
    need(r['required_printed_coverage']['REQ']==sorted(required),'actual two-file printed coverage')
    tex=(p/'evidence/required_program.tex').read_text()
    need('{check_coprime.g}'in tex and '{base_certificate.g}'in tex,'both actual TeX inclusions')
    need(r['full_required_only_printed_representation']=='REQ','required-only appendix')
    # Shared low-level parser only; independent proportions from the input counts.
    helper=Path(__file__).with_name('geometry_parser.py')
    spec=importlib.util.spec_from_file_location('geometry_parser',helper)
    geom=importlib.util.module_from_spec(spec);spec.loader.exec_module(geom)
    rect=geom.svg_rectangles((p/'costs.svg').read_bytes())
    need(len(rect)==16,'exact SVG bar count')
    x,y,w,h=rect['bar-whole-source'];cursor=x
    for d in COMMON+sum(APPS.values(),[]):
        bx,by,bw,bh=rect['bar-whole-'+d]
        need(abs(bx-cursor)<0.00001,'stack has no omitted or overlapping cost')
        need(abs(bw/w-primary['document_costs'][d]/primary['source_sum'])<0.0000001,'whole bar proportion '+d)
        cursor+=bw
    local_scale=None
    for s in SOURCES:
        sx,sy,sw,sh=rect['bar-source-'+s];ax,ay,aw,ah=rect['bar-application-'+s]
        need(abs(sx-x)<1e-6 and abs(ax-x)<1e-6,'common zero axis')
        scale=sw/primary['document_costs'][s]
        if local_scale is None:local_scale=scale
        need(abs(scale-local_scale)<1e-9 and abs(aw/local_scale-primary['application_bundles'][s])<0.01,'local bar scales')
    ux,uy,uw,uh=rect['bar-acquire-common']
    need(abs(ux-x)<1e-6 and abs(uw/local_scale-primary['whole_common'])<0.01,'full common acquisition bar')
    pdf,H=geom.pdf_rectangles(p/'costs.pdf')
    # All sixteen parsed data rectangles must match; the parser omits legend swatches.
    geom.compare_pdf(pdf,H,rect,0)
    report={'status':'PASS_INDEPENDENT_ARITHMETIC_AND_GRAPH_REVIEW',
      'reviewed_manifest_sha256':MANIFEST,'frozen_exports_checked':checked,
      'PDF_cells':450,'raw_cells':170,'coordinates':30,'exact_fractions':120,
      'CSV_rows':[len(expected_fractions),len(expected_pdf),len(expected_whole),len(acq)],
      'whole_files':len(raw),'raw_files_rehashed':bool(args.study),'SVG_bars':len(rect),'PDF_bars':len(rect),
      'primary_whole':primary['written'],'primary_individual':primary['conditional'],
      'software_inclusive_factor':None,'shared_helper':'SVG/PDF rectangle parser; no author arithmetic or chart-value metadata used.',
      'limits':['Accepted input extraction and mathematical recovery reused, not re-adjudicated.','Direct reader visual inspection is recorded separately.']}
    args.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':
    main()
