#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction
from decimal import Decimal,localcontext
import argparse,copy,csv,hashlib,json,re,xml.etree.ElementTree as ET
import pypdf
from pypdf.generic import ContentStream
HERE=Path(__file__).resolve().parent
COLORS={'source':(98/255,108/255,118/255),'common':(66/255,107/255,154/255),'application':(112/255,165/255,154/255),'program':(189/255,135/255,78/255)}


def need(ok, message):
    if not ok:
        raise ValueError('B5_NUMERIC_CHECK_REJECT: ' + message)

def bind(protocol, roots, locations=None):
    relocated = {}
    if locations is not None:
        routing = json.loads(locations.read_text())
        need(set(routing).issubset(protocol['bindings']), 'only declared input locations')
        relocated = {key: locations.parent / value for key, value in routing.items()}
    out = {}
    for key, row in protocol['bindings'].items():
        path = relocated.get(key, roots[row['root']] / row['path'])
        b = path.read_bytes()
        need(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
             'bound input ' + key)
        out[key] = json.loads(b)
    need(out['root_adoption']['status'] == 'ADOPTED_INPUT_BOUNDARY' and
         out['root_adoption']['input_manifest_sha256'] == protocol['bindings']['author_inputs']['sha256'] and
         out['root_adoption']['distinct_review_manifest_sha256'] == protocol['bindings']['independent_input_manifest']['sha256'],
         'exact distinctly adopted input')
    return out

def exact(q, numerator, denominator):
    f = Fraction(numerator, denominator)
    with localcontext() as c:
        c.prec = 40
        dec = str(Decimal(numerator) / Decimal(denominator))
    need(q == dict(numerator=numerator, denominator=denominator,
                   reduced_numerator=f.numerator, reduced_denominator=f.denominator, decimal=dec),
         'exact integer fraction and forty-place decimal')

def expected_bars(result):
    out = []
    for topic, r in result['primary'].items():
        s, c, a, p = [r[k] for k in ['source_sum', 'common_theory', 'applications', 'printed_program_cost']]
        for name, cost, bottom in [('source', s, 0), ('common-written', c, 0),
             ('application-written', a, c), ('common-printed', c, 0),
             ('application-printed', a, c), ('program', p, c+a)]:
            out.append(('bar-' + topic + '-' + name, name.split('-')[0], cost, bottom))
    return out

def svg_boxes(data):
    boxes = {}
    for node in ET.fromstring(data).iter():
        key = node.attrib.get('id', '')
        if not key.startswith('bar-'):
            continue
        path = next((x for x in node.iter() if x.tag.endswith('path')), None)
        need(path is not None, 'actual SVG rectangle')
        v = [float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?', path.attrib['d'])]
        need(len(v) == 8, 'four actual vertices')
        boxes[key] = (min(v[::2]), max(v[::2]), min(v[1::2]), max(v[1::2]))
    return boxes

def check_svg(data, result):
    boxes = svg_boxes(data)
    bars = expected_bars(result)
    need(set(boxes) == {x[0] for x in bars}, 'all six actual SVG bars')
    first = boxes[bars[0][0]]
    scale = (first[3] - first[2]) / bars[0][2]
    for key, role, cost, bottom in bars:
        b = boxes[key]
        need(abs(b[3] - b[2] - cost * scale) < 2e-5, 'actual SVG height ' + key)
        need(abs(b[3] - (first[3] - bottom * scale)) < 2e-5, 'actual SVG baseline/stack ' + key)
    for topic in result['primary']:
        for names in [('common-written', 'application-written'),
                      ('common-printed', 'application-printed', 'program')]:
            widths = [boxes['bar-' + topic + '-' + name][:2] for name in names]
            need(all(max(abs(x-y) for x, y in zip(w, widths[0])) < 2e-5 for w in widths),
                 'actual horizontal stacking')
    return len(boxes)

def pdf_boxes(path):
    reader = pypdf.PdfReader(path)
    need(len(reader.pages) == 1, 'one complete plot page')
    rgb, points, boxes = None, [], []
    for operands, op in ContentStream(reader.pages[0].get_contents(), reader).operations:
        if op == b'rg':
            rgb = tuple(float(x) for x in operands)
        elif op == b'g':
            rgb = (float(operands[0]),) * 3
        elif op == b'm':
            points = [(float(operands[0]), float(operands[1]))]
        elif op == b'l':
            points.append((float(operands[0]), float(operands[1])))
        elif op in (b'f', b'f*', b'B', b'B*'):
            role = next((k for k, color in COLORS.items() if rgb and
                         all(abs(x-y) < 1e-7 for x, y in zip(rgb, color))), None)
            if role and len(points) in (4, 5):
                boxes.append((role, min(x for x, y in points), max(x for x, y in points),
                              min(y for x, y in points), max(y for x, y in points)))
            points = []
    need(len(boxes) == 10 and [x[0] for x in boxes[-4:]] == list(COLORS) and
         all(abs(x[4] - x[3] - 5.6) < 1e-6 for x in boxes[-4:]), 'four separate legend swatches')
    return boxes[:-4]

def check_pdf(path, result):
    got, want = pdf_boxes(path), expected_bars(result)
    need(len(got) == len(want) == 6, 'six actual PDF rectangles')
    scale = (got[0][4] - got[0][3]) / want[0][2]
    for box, (_, role, cost, bottom) in zip(got, want):
        need(box[0] == role and abs(box[4] - box[3] - cost * scale) < 2e-5,
             'actual PDF rectangle/color')
        need(abs(box[3] - got[0][3] - bottom * scale) < 2e-5, 'actual PDF baseline/stack')
    return len(got)


def arithmetic(r, d):
    need(r['topic'] == 'B' and r['original_manuscripts'] == 5 and r['additional_originals'] == 1
         and r['new_topics'] == 0, 'five actual originals in the existing topic')
    need(r['new_source_credit'] == r['new_question_credit'] == 0 and not r['full_formalization_claim'],
         'no new mathematical/formal credit')
    need(r['full_old_common_retained'] and r['full_new_common_retained'] and
         r['whole_new_programs'] == 4 and r['source_cover_retained_in_primary'], 'whole acquisition')
    need(r['program_roles'] == dict(principal_required=1, validation=2, auxiliary_example=1) and
         r['operational_drivers'] == 2 and r['new_partial_formal_declarations'] == 8,
         'actual code roles and limited formalization')
    need(all(v is None for v in r['unknown_costs'].values()), 'unknown costs stay null')
    c = d['counts']; seen = set(); main_count = cover_count = 0
    coords = {(v,n,u) for v in ['raw_untrimmed','raw_selected','calibrated_selected']
              for n in ['NFC','NFKC'] for u in ['whitespace_tokens','alphanumeric_units',
              'characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']}
    for row in r['rows']:
        v,n,u = row['variant'],row['normalization'],row['unit']; coord=(v,n,u)
        need(coord in coords and coord not in seen and row['topic']=='B','unique coordinate');seen.add(coord)
        old=next(x for x in d['old_B']['rows'] if (x['topic'],x['PDF_variant'],x['normalization'],x['unit'])==('B',v,n,u))
        vals={k:x['metrics'][v][n][u] for k,x in c['documents'].items()}
        expected=[(x['source'],x['application'],x['source_cost'],x['application_cost'],x['source_representation']) for x in old['individual']]
        expected.append(('L040','B5',vals['L040'],vals['A5'],'complete_PDF_'+v))
        common={'U_B_previous':old['common_theory'],'U_B_high_rank':vals['U_ADD']}
        printed={'previous_complete_bundle':old['printed_program_cost'],'new_complete_appendix':vals['CODE']}
        files={cat:{path:x['metrics'][n][u] for path,x in f.items()} for cat,f in c['raw_files'].items()}
        raw={'previous_complete_files':old['raw_program_alternative'],'new_complete_files':sum(files['programs'].values())}
        need(row['common_components']==common and row['printed_program_components']==printed and
             row['raw_program_components']==raw and row['new_raw_file_inventory']==files,'all full document/file components')
        s=sum(x[2] for x in expected); apps=sum(x[3] for x in expected); written=sum(common.values())+apps
        for key,val in [('source_sum',s),('common_theory',sum(common.values())),('applications',apps),
                        ('written_denominator',written),('printed_program_cost',sum(printed.values())),
                        ('raw_program_alternative',sum(raw.values())),('original_manuscripts',5)]:
            need(row[key]==val,'complete summed cost '+key)
        need(row['conditional_acquisition']==dict(full_common=sum(common.values()),full_printed_programs=sum(printed.values()),
             full_raw_programs=sum(raw.values()),printed_and_raw_are_alternatives=True),'whole common/program prepayment')
        denoms={'written':written,'including_printed_programs':written+sum(printed.values()),
                'including_raw_programs':written+sum(raw.values())}
        need(set(row['whole'])==set(denoms),'three whole-topic alternatives')
        for name,den in denoms.items():exact(row['whole'][name],s,den);main_count+=1
        need(len(row['individual'])==5,'five complete applications')
        for item,(src,app,sc,ac,rep) in zip(row['individual'],expected):
            need((item['source'],item['application'],item['source_cost'],item['application_cost'],item['source_representation'])==
                 (src,app,sc,ac,rep),'literal matched input and full application')
            exact(item['conditional'],sc,ac);main_count+=1
        body=c['source_article_only']['metrics'][v][n][u];sbody=old['source_sum']+body;sen=row['article_only_sensitivity']
        need(sen['L040_article_cost']==body and sen['source_sum']==sbody and sen['earlier_four_conditionals_unchanged'] and
             sen['all_replacement_costs_unchanged'] and sen['direct_article_extraction'],'direct cover-only sensitivity')
        need(set(sen['whole'])==set(denoms),'three article-only whole alternatives')
        for name,den in denoms.items():exact(sen['whole'][name],sbody,den);cover_count+=1
        exact(sen['L040_conditional'],body,vals['A5']);cover_count+=1
    need(seen==coords and main_count==r['main_exact_fractions']==240 and cover_count==r['cover_sensitivity_fractions']==120,
         'all thirty coordinates/360 fractions')
    need(r['primary']=={'B':next(x for x in r['rows'] if (x['variant'],x['normalization'],x['unit'])==
         ('raw_untrimmed','NFC','characters_without_whitespace'))},'full raw primary, not cover sensitivity')
    return main_count,cover_count


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True)
    ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--locations',type=Path)
    ap.add_argument('--packet',type=Path,default=HERE);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    need(not a.out.exists(),'fresh output');p=json.loads((HERE/'protocol.json').read_text())
    d=bind(p,{'study':a.study_root,'public':a.public_root},a.locations);r=json.loads((a.packet/'results.json').read_text())
    main_count,cover_count=arithmetic(r,d);actual=list(csv.DictReader((a.packet/'comparisons.csv').open()));expected=[]
    for row in r['rows']:
        entries=[('full_originals','all',key,q) for key,q in row['whole'].items()]
        entries += [('full_originals',x['source'],'conditional_application',x['conditional']) for x in row['individual']]
        entries += [('L040_article_only','all',key,q) for key,q in row['article_only_sensitivity']['whole'].items()]
        entries += [('L040_article_only','L040','conditional_application',row['article_only_sensitivity']['L040_conditional'])]
        for boundary,source,name,q in entries:
            expected.append(dict(zip(['topic','source','source_boundary','variant','normalization','unit','comparison','numerator','denominator','decimal'],
                  ['B',source,boundary,row['variant'],row['normalization'],row['unit'],name,str(q['numerator']),str(q['denominator']),q['decimal']])))
    need(actual==expected,'all360 exact CSV rows');svg=(a.packet/'whole_costs.svg').read_text()
    sg=check_svg(svg,r);pg=check_pdf(a.packet/'whole_costs.pdf',r);controls=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,TypeError,StopIteration):controls.append(name);return
        raise ValueError('accepted corrupt control '+name)
    def mutate(fn):
        x=copy.deepcopy(r);fn(x);arithmetic(x,d)
    reject('drop coordinate',lambda:mutate(lambda x:x['rows'].pop()))
    reject('duplicate coordinate',lambda:mutate(lambda x:x['rows'].append(copy.deepcopy(x['rows'][0]))))
    reject('make old common paper free',lambda:mutate(lambda x:x['rows'][0]['common_components'].update(U_B_previous=0)))
    reject('deduct new common paper overlap',lambda:mutate(lambda x:x['rows'][0]['common_components'].update(U_B_high_rank=1)))
    reject('omit previous application',lambda:mutate(lambda x:x['rows'][0]['individual'].pop(0)))
    reject('zero literal N001',lambda:mutate(lambda x:x['rows'][0]['individual'][0].update(source_cost=0)))
    reject('charge only principal finite file',lambda:mutate(lambda x:x['rows'][0]['raw_program_components'].update(new_complete_files=1)))
    reject('charge printed and raw together',lambda:mutate(lambda x:x['rows'][0]['whole']['including_printed_programs'].update(denominator=1)))
    reject('missing conditional acquisition',lambda:mutate(lambda x:x['rows'][0]['conditional_acquisition'].update(full_common=0)))
    reject('replace primary by article-only',lambda:mutate(lambda x:x.update(source_cover_retained_in_primary=False)))
    reject('token subtraction for body',lambda:mutate(lambda x:x['rows'][0]['article_only_sensitivity'].update(direct_article_extraction=False)))
    reject('alter article-only replacement denominator',lambda:mutate(lambda x:x['rows'][0]['article_only_sensitivity']['whole']['written'].update(denominator=1)))
    reject('clause count as source count',lambda:mutate(lambda x:x.update(original_manuscripts=35)))
    reject('unknown primitive catalogue cost zero',lambda:mutate(lambda x:x['unknown_costs'].update(primitive_catalogue_construction=0)))
    reject('full formalization claim',lambda:mutate(lambda x:x.update(full_formalization_claim=True)))
    reject('finite validation as uniform premise',lambda:mutate(lambda x:x['program_roles'].update(principal_required=3)))
    for name,shift in [('distorted actual bar',False),('shifted actual bar with unchanged height',True)]:
        tree=ET.fromstring(svg);node=next(x for x in tree.iter() if x.attrib.get('id')=='bar-B-application-written')
        path=next(x for x in node.iter() if x.tag.endswith('path'))
        v=[float(x) for x in re.findall(r'-?\d+(?:\.\d+)?(?:e[-+]?\d+)?',path.attrib['d'])]
        for i in ([1,3,5,7] if shift else [3,5]):v[i]+=5
        path.attrib['d']=f'M {v[0]} {v[1]} L {v[2]} {v[3]} L {v[4]} {v[5]} L {v[6]} {v[7]} z'
        reject(name,lambda:check_svg(ET.tostring(tree).decode(),r))
    pages=[p.extract_text() or '' for p in pypdf.PdfReader(a.packet/'measurement.pdf').pages];need(len(pages)==2,'two reader pages')
    text=' '.join('\n'.join(pages).split());row=r['primary']['B']
    factors=list(row['whole'].values())+[x['conditional'] for x in row['individual']]
    factors+=list(row['article_only_sensitivity']['whole'].values())+[row['article_only_sensitivity']['L040_conditional']]
    for q in factors:need(f"{float(q['decimal']):.3f}" in text,'reader exact primary/sensitivity factor')
    for phrase in ['Five originals','both entire common papers and all four complete programs','unknown costs, not zero',
                   'never token subtraction','ancillary exact primitive-rank census','Distinct review of arithmetic']:
        need(phrase in text,'reader scope '+phrase)
    report=dict(status='AUTHOR_CHECK_PASS_PENDING_DISTINCT_REVIEW',main_exact_fractions=main_count,
        cover_sensitivity_fractions=cover_count,csv_rows=len(actual),actual_svg_rectangles=sg,actual_pdf_rectangles=pg,
        semantic_controls=controls,reader_pages=2,scientific_programs_executed=False)
    a.out.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))


if __name__=='__main__':main()

