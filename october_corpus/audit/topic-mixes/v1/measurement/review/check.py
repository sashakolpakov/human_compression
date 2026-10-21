#!/usr/bin/env python3
"""Distinct arithmetic and rendered-vector review. Imports no author's modules."""
from pathlib import Path
import argparse, copy, csv, hashlib, json, math, re
import xml.etree.ElementTree as ET
from pypdf import PdfReader

PINS = {
    'packet': '280555bfa0f45388bea391b35ef92c44bdaf9f0b22af79fca6dff469a733b7d0',
    'inputs': '3f02f43dd6e0037cfded61d4b3096b69a8412eeba669ec5714ea1190a24990a8',
    'input_review': '77597436ddeeadc12ae94c20aa1355b52d51251a48d894192afebb5491775010',
}
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
ORDER = ['written_papers', 'conditional_application', 'including_printed_programs',
         'including_raw_programs_alternative']

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
                exact_fraction=str(n//g) if d//g == 1 else f'{n//g}/{d//g}',
                decimal=f'{q//10**12}.{q%10**12:012d}')

def derive(counts):
    rows = []
    for v in VARIANTS:
        for n in FORMS:
            for unit in UNITS:
                d = {k: x['metrics'][v][n][unit] for k, x in counts['documents'].items()}
                raw = {g: sum(x['metrics'][n][unit] for x in files.values())
                       for g, files in counts['raw_files'].items()}
                local = d['A1'] + d['A2']
                written = d['U'] + local
                code = d['CODE1'] + d['CODE2']
                den = [written, local, written + code, written + raw['programs']]
                rows.append(dict(variant=v, normalization=n, unit=unit, document_costs=d,
                                 raw_costs=raw, source_cost=d['F005'], common_cost=d['U'],
                                 application_cost=local, written_denominator=written,
                                 printed_program_cost=code,
                                 comparisons={k: fraction(d['F005'], x) for k, x in zip(ORDER, den)}))
    return rows

def validate(result, rows, counts, policy, science):
    need(result['coordinates'] == rows, 'all 30 sums and 120 exact fractions')
    need(result['primary'] == rows[2], 'fixed raw NFC nonspace primary')
    for key, value in dict(coordinate_count=30, exact_fraction_count=120,
                           combined_exact_fractions=90, conditional_exact_fractions=30,
                           comparison_order=ORDER, source_id='F005', original_manuscripts=1,
                           source_contract_rows=35, unanswered_final_problems=3,
                           whole_common_once=True, whole_application_including_exception=True,
                           raw_and_printed_alternatives=True).items():
        need(result[key] == value, 'complete boundary ' + key)
    for key in ['cross_topic_discount', 'overlap_discount', 'whole_source_formalized',
                'finite_tests_as_uniform_proof', 'all_drivers_and_Lean_charged_in_factors',
                'sawtooth_claim', 'minimal_proof_complexity_claim', 'historical_priority_claim',
                'source_text_fonts_images_exported']:
        need(result[key] is False, 'scope limit ' + key)
    need(result['new_scientific_credit'] == result['new_question_credit'] == 0, 'no numerical mathematical credit')
    need(result['document_pages'] == dict(F005=21, U=5, A1=8, A2=4, CODE1=4, CODE2=3), 'all 45 pages')
    need(result['raw_file_inventory'] == counts['raw_files'], 'all seven whole raw files')
    need([len(counts['raw_files'][k]) for k in ['programs','drivers','formal']] == [3,3,1], 'whole program inventory')
    need(result['program_boundary'] == dict(required_finite_certificates=1, bounded_validations=2,
                                          separate_drivers=3, separate_Lean_files=1,
                                          partial_Lean_declarations=2), 'actual program roles')
    need(result['conditional_prepaid'] == 'The whole common paper U and all three complete mathematical programs are already acquired; A1 and A2 together form the one complete application.', 'whole acquisition')
    need(result['unknown_costs'] == {k: None for k in ['full_graphics','historical_software',
        'retained_external_proofs','full_formalization','runtime','operational_engineering']}, 'unknowns remain unknown')
    for key in ['retained_inputs','accepted_literal_counterexample_targets',
                'accepted_qualified_counterexample_targets','unresolved_literal_correspondence']:
        need(result[key] == science[key], 'accepted scientific scope ' + key)
    need(result['source_exclusions'] == policy['corrected_source_scope'], 'unchanged source scope')

def actual_vectors(svg_path, pdf_path, primary):
    # Infer scales from actual rendered tick marks and labels, not the author's geometry JSON.
    parser = ET.XMLParser(target=ET.TreeBuilder(insert_comments=True))
    root = ET.fromstring(svg_path.read_text(), parser=parser)
    ns = {'s': 'http://www.w3.org/2000/svg'}
    d = primary['document_costs']
    expected = [dict(), dict()]
    expected[0]['cost-source'] = (d['F005'], 0)
    for col, keys in [(1, ['U','A1','A2']), (2, ['U','A1','A2','CODE1','CODE2'])]:
        base = 0
        for key in keys:
            expected[0][f'cost-total-{col}-{key}'] = (d[key], base)
            base += d[key]
    for key in ['U','A1','A2','CODE1','CODE2']:
        expected[1]['cost-component-' + key] = (d[key], 0)
    boxes = {}
    for index in [1,2]:
        ax = next(g for g in root.findall('.//s:g',ns) if g.get('id') == f'axes_{index}')
        ticks = []
        actual = set()
        for g in ax.findall('.//s:g',ns):
            name = g.get('id','')
            if name.startswith('ytick_'):
                path = g.find('.//s:path',ns)
                comments = [e.text for e in g.iter() if e.tag is ET.Comment]
                if path is not None and comments:
                    xy = list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))))
                    ticks.append((xy[1], float(comments[0].strip().replace(',',''))))
            if name.startswith('cost-'):
                actual.add(name)
                path = g.find('s:path',ns)
                need(path is not None and not re.search('[CQAST]',path.get('d'),re.I), 'rectangular cost path')
                nums = list(map(float,re.findall(r'-?\d+(?:\.\d+)?',path.get('d'))))
                need(len(nums) == 8, 'four rectangle vertices')
                xs,ys = nums[::2],nums[1::2]
                need(len(set(xs)) == len(set(ys)) == 2, 'rectangle corner coordinates')
                need(len(set(zip(xs,ys))) == 4 and name not in boxes, 'unique four corners')
                boxes[name] = (min(xs),min(ys),max(xs)-min(xs),max(ys)-min(ys))
        need(actual == set(expected[index-1]), 'complete rendered document ownership')
        need(len(ticks) >= 3 and ticks[0][1] == 0, 'actual axis starts at zero')
        origin = ticks[0][0]
        scale = (origin-ticks[1][0])/ticks[1][1]
        need(scale > 0 and all(abs(y-(origin-v*scale)) < 3e-6 for y,v in ticks), 'actual linear ticks')
        for name,(value,base) in expected[index-1].items():
            x,y,w,h = boxes[name]
            need(abs(h/scale-value) < .002 and abs((origin-y-h)/scale-base) < .002, 'actual cost height and stacking')
    need(len(boxes) == 14, 'fourteen complete rectangles')
    pdf = PdfReader(pdf_path)
    need(len(pdf.pages) == 1, 'one graph page')
    page = pdf.pages[0]
    rectangles,poly = [],[]
    for args,op in page.get_contents().operations:
        if op == b'm': poly = [tuple(map(float,args))]
        elif op == b'l': poly.append(tuple(map(float,args)))
        elif op in [b'f',b'B',b'f*',b'B*']:
            if len(poly) == 4:
                xs,ys = zip(*poly)
                if len(set(xs)) == len(set(ys)) == 2 and len(set(poly)) == 4:
                    rectangles.append((min(xs),float(page.mediabox.height)-max(ys),max(xs)-min(xs),max(ys)-min(ys)))
            poly = []
        elif op in [b'S',b's',b'n']: poly=[]
    for box in boxes.values():
        need(sum(all(abs(x-y) < 3e-6 for x,y in zip(box,r)) for r in rectangles) == 1, 'actual PDF equals SVG bar')
    return len(boxes)

def main():
    ap = argparse.ArgumentParser()
    for name in ['packet','inputs','input-review','out']:
        ap.add_argument('--'+name,type=Path,required=True)
    a = ap.parse_args()
    need(not a.out.exists(), 'fresh output')
    exports = {k:bind(getattr(a,k),pin) for k,pin in PINS.items()}
    accepted = read(a.input_review/'review.json')
    need(accepted['status'] == 'ROOT_ACCEPTED_UNCHANGED_COMPLETE_F005_MEASUREMENT_INPUTS'
         and accepted['factors_now_permitted_for_exact_reviewed_inputs'] is True, 'distinct input acceptance')
    counts = read(a.input_review/'independent_counts.json')
    author_counts = read(a.inputs/'author_counts.json')
    need(all(counts[k] == author_counts[k] for k in ['documents','raw_files']), 'all independent counts agree')
    policy = read(a.inputs/'policy.json')
    science = read(a.inputs/'source_boundary.json')['topic_Mix_F005_root_review/review.json']
    protocol = read(a.packet/'protocol.json')
    before = read(a.packet/'protocol_before_input_acceptance.json')
    delta = dict(protocol, status=before['status'], input_acceptance=None, evaluation_authorized=False)
    need(delta == before and protocol['primary'] == [VARIANTS[0],FORMS[0],UNITS[2]], 'preselected protocol unchanged')
    rows = derive(counts)
    result = read(a.packet/'results.json')
    validate(result,rows,counts,policy,science)
    csv_rows = list(csv.DictReader((a.packet/'comparisons.csv').open()))
    wanted = [{k:str(v) for k,v in dict(variant=r['variant'],normalization=r['normalization'],
              unit=r['unit'],comparison=c,**r['comparisons'][c]).items()} for r in rows for c in ORDER]
    need(csv_rows == wanted, 'all 120 exact CSV rows')
    n = actual_vectors(a.packet/'complete_costs.svg',a.packet/'complete_costs.pdf',rows[2])
    controls=[]
    for name,mut in [
        ('free common',lambda d:d['coordinates'][0].update(common_cost=0)),
        ('free exceptional proof',lambda d:d['coordinates'][0]['document_costs'].update(A2=0)),
        ('missing exceptional code',lambda d:d['coordinates'][0]['document_costs'].update(CODE2=0)),
        ('both code alternatives added',lambda d:d['coordinates'][0]['comparisons']['including_raw_programs_alternative'].update(denominator=1)),
        ('free conditional acquisition',lambda d:d.update(conditional_prepaid='none')),
        ('wrong exact reduction',lambda d:d['coordinates'][0]['comparisons']['written_papers'].update(reduced_denominator=1)),
        ('wrong rounding',lambda d:d['coordinates'][0]['comparisons']['written_papers'].update(decimal='1.0')),
        ('changed primary',lambda d:d.update(primary=d['coordinates'][0])),
        ('cross topic discount',lambda d:d.update(cross_topic_discount=True)),
        ('unknown becomes zero',lambda d:d['unknown_costs'].update(full_graphics=0)),
        ('source rows become originals',lambda d:d.update(original_manuscripts=35)),
        ('claim all questions solved',lambda d:d.update(unanswered_final_problems=0)),
        ('claim full Lean',lambda d:d.update(whole_source_formalized=True)),
        ('omit complete program',lambda d:d['raw_file_inventory']['programs'].pop(next(iter(d['raw_file_inventory']['programs'])))),
    ]:
        bad=copy.deepcopy(result); mut(bad)
        try: validate(bad,rows,counts,policy,science)
        except (ValueError,KeyError): controls.append(name)
        else: raise ValueError('accepted corruption '+name)
    a.out.mkdir(parents=True)
    # An actual vector distortion must be rejected, independently of manifest hashes.
    svg=(a.packet/'complete_costs.svg').read_text()
    root=ET.fromstring(svg, parser=ET.XMLParser(target=ET.TreeBuilder(insert_comments=True)))
    group=next(e for e in root.iter() if e.get('id')=='cost-source')
    path=next(e for e in group if e.tag.endswith('path'))
    old=path.get('d'); hit=list(re.finditer(r'-?\d+(?:\.\d+)?',old))[1]
    replacement=old[:hit.start()]+str(float(hit.group())+8)+old[hit.end():]
    path.set('d',replacement)
    corrupt=a.out/'corrupt.svg';corrupt.write_text(ET.tostring(root,encoding='unicode'))
    try: actual_vectors(corrupt,a.packet/'complete_costs.pdf',rows[2])
    except (ValueError,KeyError): controls.append('actual distorted SVG source bar')
    else: raise ValueError('accepted corrupted actual graph')
    corrupt.unlink()
    p=rows[2];c=p['document_costs'];raw=p['raw_costs']
    acquisition=dict(source_cost=c['F005'],whole_common_cost=c['U'],whole_local_cost=c['A1']+c['A2'],
                     printed_upfront=c['U']+c['CODE1']+c['CODE2'],raw_upfront=c['U']+raw['programs'],
                     printed_raw_alternatives=True,retained_cost=None,prior_correction_free=False)
    report=dict(status='PASS_DISTINCT_F005_NUMERICAL_REVIEW',exports=exports,coordinates=30,
                exact_fractions=120,CSV_rows=120,actual_SVG_rectangles=n,actual_PDF_rectangles=n,
                independent_controls=controls,arithmetic='integer gcd and exact ties-to-even decimal division',
                graph_scale='inferred from actual SVG tick positions and numeric labels',
                author_modules_imported=False,extraction_repeated=False,science_repeated=False,
                primary=p,conditional_acquisition=acquisition)
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    (a.out/'independent_results.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ['primary','independent_controls']}))

if __name__ == '__main__': main()
