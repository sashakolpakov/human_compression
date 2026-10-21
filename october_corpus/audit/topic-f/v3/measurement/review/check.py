#!/usr/bin/env python3
"""Distinct symmetric expanded F arithmetic and vector review; no author modules imported.

The generic integer division and SVG/PDF rectangle methods are adapted from
the previously reviewed root F005 checker, with new two-source expectations.
"""
from pathlib import Path
import argparse, copy, csv, hashlib, json, math, re
import xml.etree.ElementTree as ET
from pypdf import PdfReader

def need(value, message):
    if not value:
        raise ValueError(message)

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def bind(path, pin):
    need(sha(path / 'manifest.json') == pin, 'frozen manifest')
    names = set()
    for item in read(path / 'manifest.json')['exports']:
        rel = Path(item['path'])
        need(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in names, 'unique safe export')
        names.add(str(rel))
        f = path / rel
        need(f.stat().st_size == item['bytes'] and sha(f) == item['sha256'], 'frozen export ' + str(rel))
    return len(names)

def fraction(n, d):
    g = math.gcd(n, d)
    q, r = divmod(n * 10**12, d)
    if 2*r > d or (2*r == d and q % 2):
        q += 1
    return dict(numerator=n, denominator=d, reduced_numerator=n//g, reduced_denominator=d//g,
                decimal=f'{q//10**12}.{q%10**12:012d}')


PINS = {'packet': '3a24e6ba85542b0cde991b56a40a93cb0e7ed540abd33d0b69b899b5e8f30527',
        'inputs': '4835714ae78f8069a7b53f6181b770a2b40286eadf8a2c53cc652b96c4ccea0a',
        'input_review': 'caf7bb421e325234f2565bece89032d44ee8781c5aea18b09c4ac4bc3fae99c5'}
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
ORDER = ['written', 'conditional_L014', 'conditional_L007']


def derive(counts):
    rows = []
    for v in VARIANTS:
        for f in FORMS:
            for u in UNITS:
                c = {k: counts['documents'][k]['metrics'][v][f][u]
                     for k in ['L014', 'L007', 'U', 'A1', 'A2', 'CODE']}
                raw = {kind: sum(r['metrics'][f][u] for r in files.values())
                       for kind, files in counts['raw_files'].items()}
                source = c['L014'] + c['L007']
                local = c['A1'] + c['A2']
                written = c['U'] + local
                numerators = [source, c['L014'], c['L007']]
                denominators = [written, c['A1'], c['A2']]
                rows.append(dict(variant=v, normalization=f, unit=u, costs=c, raw_costs=raw,
                    totals=dict(source=source, common=c['U'], applications=local, written=written),
                    comparisons={key: fraction(n,d) for key,n,d in zip(ORDER,numerators,denominators)},
                    optional_validation_inventory=dict(printed=c['CODE'], raw_alternative=raw['programs'],
                        representations_alternative=True, source_software_cost=None,
                        symmetric_software_inclusive_factor=None, used_as_uniform_proof_premise=False),
                    conditional_acquisition=dict(whole_common=['U'], common_cost=c['U'],
                        local_application_costs={'L014':c['A1'], 'L007':c['A2']},
                        unknown_retained_costs_remain=True, optional_validation_required=False)))
    return rows


def validate(result, rows, policy, scope):
    need(result['coordinates'] == rows and result['primary'] == rows[2], 'all90 exact fractions and full totals')
    need(result['source_ids'] == ['L014','L007'] and result['source_dispositions'] == 63 and
         result['whole_documents'] == ['L014','L007','U','A1','A2','CODE'] and
         result['physical_pages'] == [12,22,7,5,6,9], 'two originals and all61physical pages')
    need((result['coordinate_count'],result['exact_fraction_count'],result['combined_fractions'],
          result['conditional_fractions']) == (30,90,30,60), 'all fixed coordinates')
    need(result['raw_inventory'] == {k:policy[k] for k in ['programs','operational_drivers','formal_files']},
         'whole9program/4driver/3formal inventories')
    b = result['boundary']
    need(b['source_corrections'] == scope and b['unknown_costs'] == policy['unknown_costs'] and
         all(x is None for x in b['unknown_costs'].values()), 'unchanged corrected scope and unknowns')
    need(b['written_documents'] == ['U','A1','A2'] and b['application_map'] == {'L014':'A1','L007':'A2'},
         'complete source application pairing')
    for k,v in dict(whole_programs=9,programs_bytes=25501,validation_programs=9,uniform_finite_premise_programs=0,
                    separate_drivers=4,separate_driver_bytes=33222,formal_files=3,separate_formal_bytes=9398,
                    formal_declarations=12,reused_declarations=9,new_generic_declarations=3,
                    old_L014_selected_headline=25115,new_L014_raw_primary=25574).items():
        need(b[k] == v, 'actual boundary '+k)
    for k in ['whole_common_once','printed_and_raw_alternatives','no_source_specific_Lean_instance',
              'no_cross_topic_discount','no_free_inherited_common',
              'conditional_prepays_whole_common_and_actual_retained_premises','previous_one_source_edition_preserved']:
        need(b[k] is True, 'complete acquisition '+k)
    need(b['source_validation_software_cost'] is None and b['symmetric_software_inclusive_factor'] is None and
         b['optional_validation_required_for_conditional'] is False, 'symmetric optional validation policy')
    change = result['policy_correction']
    need(change['public_commit'] == 'eddda09725a0738bb5dc77489cb06d6221736714' and
         change['previous_manifest_sha256'] == '855ea109031cf316640f2f2d8263d50227a4ca2c98d65b745c8d8bb8b0869bcb' and
         change['removed_asymmetric_fractions'] == 60 and change['all_document_and_raw_costs_unchanged'] and
         change['all_written_and_conditional_fractions_unchanged'] and
         change['embedded_optional_validation_listings_found'] is False and change['manuscript_cuts_made'] is False,
         'unchanged costs and correct scope of policy correction')
    need(not b['full_source_formalized'] and not result['primary_material_exported'] and
         all(result[k] == 0 for k in ['new_source_credit','new_question_credit','new_formal_credit']), 'no new mathematical credit')


def actual_vectors(svg, pdf, primary):
    root = ET.fromstring(svg.read_text(), parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    ns = {'s':'http://www.w3.org/2000/svg'}
    c,raw = primary['costs'],primary['raw_costs']
    expected = []
    for panel,bars in [
        ('written', [[('L014',c['L014']),('L007',c['L007'])],[(k,c[k]) for k in ['U','A1','A2']]]),
        ('validation', [[('CODE',c['CODE'])], [('programs',raw['programs'])]]),
        ('conditional', [[(k,c[k])] for k in ['L014','A1','L007','A2']])]:
        result = {}
        for i,parts in enumerate(bars):
            bottom = 0
            for key,value in parts:
                result[f'cost-{panel}-{i}-{key}'] = (value,bottom)
                bottom += value
        expected.append(result)
    boxes = {}
    for index,wanted in enumerate(expected,1):
        axes = next(g for g in root.findall('.//s:g',ns) if g.get('id') == f'axes_{index}')
        ticks,seen = [],set()
        for g in axes.findall('.//s:g',ns):
            name = g.get('id','')
            if name.startswith('ytick_'):
                path = g.find('.//s:path',ns)
                comments = [e.text for e in g.iter() if e.tag is ET.Comment]
                if path is not None and comments:
                    xy = list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))))
                    ticks.append((xy[1],float(comments[0].strip().replace(',',''))))
            if name.startswith('cost-'):
                seen.add(name)
                path = g.find('s:path',ns)
                need(path is not None and not re.search('[CQAST]',path.get('d'),re.I), 'straight cost rectangle')
                numbers = list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))))
                need(len(numbers) == 8, 'four actual vertices')
                xs,ys = numbers[::2],numbers[1::2]
                need(len(set(xs)) == len(set(ys)) == 2 and len(set(zip(xs,ys))) == 4 and name not in boxes,
                     'unique rectangular bar')
                boxes[name] = (min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
        need(seen == set(wanted), 'all document components owned in actual graph')
        need(len(ticks) >= 3 and ticks[0][1] == 0, 'actual zero baseline')
        origin = ticks[0][0]; scale = (origin-ticks[1][0])/ticks[1][1]
        need(scale > 0 and all(abs(y-(origin-v*scale)) < 3e-6 for y,v in ticks), 'actual linear tick scale')
        for name,(value,bottom) in wanted.items():
            x,y,w,h = boxes[name]
            need(abs(h/scale-value) < .002 and abs((origin-y-h)/scale-bottom) < .002,
                 'actual bar amount and stacked baseline')
    need(len(boxes) == 11, '11 complete manuscript and validation cost components')
    doc = PdfReader(pdf); need(len(doc.pages) == 1, 'one chart page'); page=doc.pages[0]
    rectangles,poly = [],[]
    for args,op in page.get_contents().operations:
        if op == b'm': poly=[tuple(map(float,args))]
        elif op == b'l': poly.append(tuple(map(float,args)))
        elif op in [b'f',b'B',b'f*',b'B*']:
            if len(poly) == 4:
                xs,ys=zip(*poly)
                if len(set(xs)) == len(set(ys)) == 2 and len(set(poly)) == 4:
                    rectangles.append((min(xs),float(page.mediabox.height)-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
            poly=[]
        elif op in [b'S',b's',b'n']: poly=[]
    for box in boxes.values():
        need(sum(all(abs(a-b)<3e-6 for a,b in zip(box,rect)) for rect in rectangles) == 1,
             'one exact PDF rectangle per SVG cost component')
    return len(boxes)


def acquisition_graph(packet, primary):
    graph = read(packet/'document_graph.json')
    nodes = {r['id']:r for r in graph['nodes']}
    need(len(nodes)==len(graph['nodes'])==7 and set(nodes)=={'L014','L007','U','A1','A2','programs','retained'},
         'all whole-document acquisition nodes')
    for k in ['L014','L007','U','A1','A2']:
        need(nodes[k]['cost']==primary['costs'][k], 'node text cost')
    need(nodes['retained']['cost'] is None and nodes['programs']['printed_cost']==primary['costs']['CODE'] and
         nodes['programs']['raw_alternative_cost']==primary['raw_costs']['programs'], 'complete alternative programs and unknown premise')
    edges={(r['source'],r['target'],r['kind']) for r in graph['edges']}
    want={('U',a,'proof_input') for a in ['A1','A2']} | {('retained',a,'retained_input') for a in ['U','A1','A2']} | {
          ('L014','A1','source_correspondence'),('L007','A2','source_correspondence')} | {
          ('programs',a,'validation_association') for a in ['A1','A2']}
    need(edges==want and len(graph['edges'])==9 and 'not a theorem dependency DAG' in graph['scope'],
         'explicit logical/validation/source roles; no theorem DAG claim')
    svg=ET.fromstring((packet/'document_graph.svg').read_text())
    actual={e.get('id') for e in svg.iter() if e.get('id','').startswith(('node-','edge-'))}
    need(actual=={'node-'+k for k in nodes}|{'edge-'+a+'-'+b for a,b,_ in want}, 'actual graph nodes and edges')
    return len(nodes),len(edges)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['packet','inputs','input-review','out']:
        ap.add_argument('--'+key,type=Path,required=True)
    a=ap.parse_args()
    need(not a.out.exists(), 'fresh output directory')
    exports={k:bind(getattr(a,k),pin) for k,pin in PINS.items()}
    counts=read(a.input_review/'independent_counts.json')
    authored=read(a.inputs/'author_counts.json')
    need(counts['documents']==authored['documents'] and counts['raw_files']==authored['raw_files'], 'accepted full input agreement')
    need(read(a.input_review/'review.json')['factors_now_permitted_for_exact_reviewed_inputs'] is True,
         'distinct input acceptance')
    policy=read(a.inputs/'policy.json'); scope=read(a.inputs/'source_boundary.json')
    rows=derive(counts); result=read(a.packet/'results.json'); validate(result,rows,policy,scope)
    csv_rows=list(csv.DictReader((a.packet/'fractions.csv').open()))
    wanted=[{k:str(v) for k,v in dict(variant=r['variant'],normalization=r['normalization'],unit=r['unit'],
                                    comparison=key,**r['comparisons'][key]).items()} for r in rows for key in ORDER]
    need(csv_rows==wanted, 'all90 exact CSV comparisons')
    bars=actual_vectors(a.packet/'costs.svg',a.packet/'costs.pdf',rows[2])
    graph_nodes,graph_edges=acquisition_graph(a.packet,rows[2])
    controls=[]
    for name,change in [
        ('free_common',lambda r:r['coordinates'][0]['costs'].__setitem__('U',0)),
        ('free_L014_application',lambda r:r['coordinates'][0]['costs'].__setitem__('A1',0)),
        ('free_L007_application',lambda r:r['coordinates'][0]['costs'].__setitem__('A2',0)),
        ('wrong_reduced_fraction',lambda r:r['coordinates'][0]['comparisons']['written'].__setitem__('reduced_numerator',0)),
        ('wrong_rounding',lambda r:r['coordinates'][0]['comparisons']['written'].__setitem__('decimal','1.0')),
        ('omit_raw_program',lambda r:r['raw_inventory']['programs'].pop()),
        ('conditional_validation_wrongly_required',lambda r:r['coordinates'][0]['conditional_acquisition'].__setitem__('optional_validation_required',True)),
        ('invent_symmetric_program_ratio',lambda r:r['coordinates'][0]['optional_validation_inventory'].__setitem__('symmetric_software_inclusive_factor',1.07)),
        ('unknown_source_software_as_zero',lambda r:r['coordinates'][0]['optional_validation_inventory'].__setitem__('source_software_cost',0)),
        ('unknown_retained_proof_as_zero',lambda r:r['boundary']['unknown_costs'].__setitem__('full_retained_CP_proof',0)),
        ('source_rows_as_originals',lambda r:r['source_ids'].extend(['extra']*61)),
        ('claim_complete_Lean',lambda r:r['boundary'].__setitem__('full_source_formalized',True)),
        ('claim_new_question',lambda r:r.__setitem__('new_question_credit',1)),
        ('change_primary',lambda r:r.__setitem__('primary',r['coordinates'][0]))]:
        bad=copy.deepcopy(result);change(bad)
        try:validate(bad,rows,policy,scope)
        except (ValueError,KeyError):controls.append(name)
        else:raise ValueError('invalid result accepted '+name)
    a.out.mkdir(parents=True)
    root=ET.fromstring((a.packet/'costs.svg').read_text(),parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    group=next(e for e in root.iter() if e.get('id')=='cost-written-0-L014')
    path=next(e for e in group if e.tag.endswith('path')); old=path.get('d')
    hit=list(re.finditer(r'-?\d+(?:\.\d+)?',old))[1]
    path.set('d',old[:hit.start()]+str(float(hit.group())+8)+old[hit.end():])
    damaged=a.out/'damaged.svg';damaged.write_text(ET.tostring(root,encoding='unicode'))
    try:actual_vectors(damaged,a.packet/'costs.pdf',rows[2])
    except (ValueError,KeyError):controls.append('actual_distorted_bar')
    else:raise ValueError('actual graph distortion accepted')
    damaged.unlink()
    report=dict(status='PASS_DISTINCT_SYMMETRIC_EXPANDED_F_NUMBERS',exports=exports,coordinates=30,exact_fractions=90,
                CSV_rows=90,actual_SVG_bars=bars,actual_PDF_bars=bars,acquisition_nodes=graph_nodes,
                acquisition_edges=graph_edges,independent_controls=controls,primary=rows[2],
                arithmetic='integer gcd and exact ties-to-even division',
                vector_scale='actual rendered SVG numeric tick positions, matched to actual PDF rectangles',
                author_modules_imported=False,source_extraction_repeated=False,science_repeated=False,
                new_original_credit=0,new_question_credit=0,new_formal_credit=0)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (a.out/'independent_results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['primary','independent_controls']}))


if __name__=='__main__':main()
