#!/usr/bin/env python3
"""Independent allocation and closure audit of the frozen Topic B text partition.

Uses the adopted PDF/parser boundary, but imports no author extraction,
allocation, graph or weight functions. Semantic reading is recorded separately.
"""
import argparse
import copy
import csv
import hashlib
import json
import unicodedata
from pathlib import Path
import pypdf

UNITS = ('whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace')
FORMS = ('NFC', 'NFKC')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_text())


def selected(pdf, spec):
    require(digest(pdf.read_bytes()) == spec['pdf_sha256'], 'PDF edition')
    pages = [p.extract_text() or '' for p in pypdf.PdfReader(pdf).pages]
    raw = '\n'.join(pages)
    require(len(pages) == spec['pages'] and digest(raw.encode()) == spec['extraction_sha256'],
            'complete PDF extraction')
    page_index = []
    at = 0
    for number, body in enumerate(pages, 1):
        expected = dict(page=number, start=at, end=at+len(body),
                        sha256=digest(body.encode()), empty_extraction=not body)
        require(expected == spec['page_bindings'][number-1], 'physical page binding')
        page_index.extend([number]*len(body) + [None])
        at += len(body)+1
    require(len(spec['included_spans']) == 1 and spec['included_spans'][0]['start'] == 0 and
            spec['included_spans'][0]['end'] == len(raw), 'complete text boundary')
    excluded = {}
    last = -1
    for row in spec['excluded_furniture']:
        a, b = row['start'], row['end']
        require(last <= a < b <= len(raw) and raw[a:b] == row['literal'], 'exact ordered furniture')
        excluded[a] = b
        last = b
    substitutions = {x['offset']:x['output'] for x in spec['glyph_substitutions']}
    require(len(substitutions) == len(spec['glyph_substitutions']), 'unique calibrated occurrence')
    for row in spec['glyph_substitutions']:
        require(ord(raw[row['offset']]) == int(row['input_codepoint'][2:],16), 'calibrated input glyph')
    body, positions, physical = [], [], []
    i = 0
    while i < len(raw):
        if i in excluded:
            body.append('\n'); positions.append(None); physical.append(None)
            i = excluded[i]
        else:
            value = substitutions.get(i, raw[i])
            require(len(value) == 1, 'adopted one-codepoint calibration')
            body.append(value); positions.append(i); physical.append(page_index[i]); i += 1
    return ''.join(body), positions, physical


def zero():
    return {f:dict.fromkeys(UNITS,0) for f in FORMS}


def sum_costs(names, costs):
    answer = zero()
    for name in set(names):
        for f in FORMS:
            for u in UNITS:
                answer[f][u] += costs[name][f][u]
    return answer


def allocate(text, spans, form):
    """Scan normalized characters and assign unit starts without regex/bisection."""
    chunks = [unicodedata.normalize(form,text[s['start']:s['end']]) for s in spans]
    normalized = unicodedata.normalize(form,text)
    require(''.join(chunks) == normalized, 'normalization across ownership boundary')
    assigned = [(char, span['node']) for chunk,span in zip(chunks,spans) for char in chunk]
    costs = {s['node']:dict.fromkeys(UNITS,0) for s in spans}
    in_token = in_alpha = False
    content_seen = False
    pending_space_owner = None
    for char, owner in assigned:
        white, alpha = char.isspace(), char.isalnum()
        if alpha and not in_alpha:
            costs[owner]['alphanumeric_units'] += 1
        in_alpha = alpha
        if white:
            if content_seen and pending_space_owner is None:
                pending_space_owner = owner
            in_token = False
            continue
        if pending_space_owner is not None:
            costs[pending_space_owner]['characters_with_collapsed_whitespace'] += 1
            costs[pending_space_owner]['utf8_bytes_with_collapsed_whitespace'] += 1
            pending_space_owner = None
        if not in_token:
            costs[owner]['whitespace_tokens'] += 1
        in_token = content_seen = True
        costs[owner]['characters_without_whitespace'] += 1
        costs[owner]['characters_with_collapsed_whitespace'] += 1
        costs[owner]['utf8_bytes_with_collapsed_whitespace'] += len(char.encode())
    return costs


def inspect(partition, weights, graph, coverage, extracted, measured):
    owners = partition['owners']
    for name in ('h.N008.L3.6', 'h.N008.T3.4'):
        require(owners[name]['category'] == 'statement', 'statement-only owner mislabeled as proof')
        matches = [s for s in partition['documents']['N008']['spans'] if s['node'] == name]
        require(len(matches) == 1 and matches[0]['category'] == 'statement',
                'statement-only span mislabeled as proof')
    require(set(partition['documents']) == set(extracted) ==
            {'N003','N008','L030','U_B','B1','B2','B3','B4'}, 'eight complete documents')
    require(partition['N001_original_pdf_cost'] is None, 'N001 remains unknown')
    costs = {name:zero() for name in owners}
    document_costs = {}
    span_count = 0
    for key, row in partition['documents'].items():
        text, positions, pages = extracted[key]
        require(digest(text.encode()) == row['text_sha256'] and len(text) == row['length'],
                'selected complete document hash')
        last = 0
        for span in row['spans']:
            a, b = span['start'], span['end']
            require(a == last and a < b <= len(text), 'gap, overlap or empty owner span')
            require(digest(text[a:b].encode()) == span['sha256'], 'owned passage hash')
            require(span['node'] in owners and owners[span['node']]['document'] == key,
                    'owner belongs to this document')
            raw_positions = [x for x in positions[a:b] if x is not None]
            require(span['raw_start'] == min(raw_positions) and span['raw_end'] == max(raw_positions)+1,
                    'raw passage endpoints')
            require(span['physical_pages'] == sorted({x for x in pages[a:b] if x is not None}),
                    'physical page correspondence')
            last = b
            span_count += 1
        require(last == len(text), 'complete document suffix')
        for form in FORMS:
            values = allocate(text,row['spans'],form)
            for owner,value in values.items():
                costs[owner][form] = value
        document_costs[key] = sum_costs([n for n,o in owners.items() if o['document']==key],costs)
        for f in FORMS:
            require(document_costs[key][f] == {u:measured['documents'][key]['calibrated_selected'][f][u] for u in UNITS},
                    'whole document metrics differ from adopted independent recount')
    require(costs == weights['owner_costs'] and document_costs == weights['document_costs'],
            'independent owner allocation differs')
    nodes = {n['id']:n for n in graph['nodes']}
    links = weights['node_interfaces']
    require(set(links) == set(nodes), 'all logical interfaces')
    for name, node in nodes.items():
        interface = links[name]
        paid = interface['owners']
        require(paid == sorted(set(paid)) and set(paid) <= set(owners), 'unique owner set')
        require(all(owners[o]['document'] == node['document'] for o in paid), 'interface document')
        missing = node['side'] in ('external','verification') or node['document']=='N001'
        require(interface['weight'] == (None if missing else sum_costs(paid,costs)), 'interface exact union or unknown')
        require(not missing or not paid, 'unknown inputs have no measured PDF owner')
        require(missing or bool(paid), 'measured node owns no text')
        require(interface['charged_as_an_additional_item'] is False and interface['full_dependency_cost'] is None,
                'node alias cannot create another charge or expanded proof total')
        for expected in [name, name+'.statement']:
            require(expected not in owners or expected in paid, 'direct owned statement/proof omitted')
        if node.get('parent'):
            statement = node['parent']+'.statement'
            require(statement not in owners or statement in paid, 'shared parent statement omitted')
            require(set(paid) <= set(links[node['parent']]['owners']), 'parent omits child passage')
    require('B1.B97' in links['B1.Reconstruction']['owners'], 'retained classification statement omitted')
    require({'h.N008.frattini_free.setup','h.N008.frattini_free.proof'} <= set(links['h.N008.T3.4']['owners']),
            'full Frattini-free setup and proof omitted')
    parents = {n:set() for n in nodes}
    for edge in graph['edges']:
        if edge['kind'] in graph['logical_edge_kinds']:
            require(edge['source'] in nodes and edge['target'] in nodes, 'edge endpoints')
            parents[edge['target']].add(edge['source'])
    def closure(targets):
        reached = set(targets)
        pending = list(targets)
        while pending:
            for prior in parents[pending.pop()]-reached:
                reached.add(prior); pending.append(prior)
        return reached
    def route(targets, record):
        names = closure(targets)
        paid = set().union(*(set(links[n]['owners']) for n in names))
        require(record['logical_nodes'] == sorted(names) and record['owners'] == sorted(paid),
                'independently reconstructed prerequisite/owner closure')
        require(record['known_extracted_text_subtotal'] == sum_costs(paid,costs), 'closure union subtotal')
        bydoc = {d:sum_costs([o for o in paid if owners[o]['document']==d],costs)
                 for d in sorted({owners[o]['document'] for o in paid})}
        require(record['by_document'] == bydoc, 'closure per-document costs')
        require(record['unknown_inputs'] == sorted(n for n in names if links[n]['weight'] is None) and
                record['expanded_dependency_cost'] is None, 'closure unknown inputs')
    require(len(coverage['rows']) == len(weights['source_contract_closures']) == 30, 'thirty paired clauses')
    for old,new in zip(coverage['rows'],weights['source_contract_closures']):
        require((old['adapter'],old['source_id']) == (new['adapter'],new['source_id']), 'exact source row')
        route([old['historical_output']],new['historical'])
        route(old['new_outputs'],new['replacement'])
    require(set(weights['new_application_closures']) == set(graph['new_application_outputs']), 'four applications')
    for name,node in graph['new_application_outputs'].items():
        route([node],weights['new_application_closures'][name])
    mapped = set().union(*(set(x['owners']) for x in links.values()))
    unmapped = [owners[n] for n in sorted(set(owners)-mapped)]
    require(partition['unmapped_owners'] == unmapped, 'unmapped text remains inventoried')
    require(all(x['category'] in ('front_matter','context','references') for x in unmapped
                if x['document'] in ('U_B','B1','B2','B3','B4')), 'new proof omitted from every interface')
    for name in ('whole_historical_pdf_cost','expanded_external_proof_cost','graphic_cost','compression_ratio'):
        require(weights[name] is None, 'unknown cost or undefined graph factor')
    require(weights['new_source_credit']==weights['new_question_credit']==0, 'no new credits')
    return dict(documents=len(extracted),spans=span_count,owners=len(owners),
                owner_metric_cells=len(owners)*10,document_metric_cells=len(extracted)*10,
                independent_closures=64,unmapped_context_owners=len(unmapped))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--study-root',type=Path,required=True)
    parser.add_argument('--public-root',type=Path,required=True)
    parser.add_argument('--packet',type=Path,required=True)
    parser.add_argument('--out',type=Path,required=True)
    args = parser.parse_args()
    require(not args.out.exists(),'fresh output directory')
    require(pypdf.__version__=='6.13.0','pinned shared PDF parser')
    args.out.mkdir(parents=True)
    study, packet = args.study_root,args.packet
    manifest=read(packet/'manifest.json')
    for row in manifest['exports']:
        raw=(packet/row['path']).read_bytes()
        require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'frozen weighted export')
    for row in read(packet/'input_bindings.json')['inputs']:
        raw=(study/row['path']).read_bytes()
        require(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'bound measurement/graph input')
    specs=read(study/'topic_B_measurement/source_input_spec.json')['sources']
    replacements=read(study/'topic_B_measurement/replacement_input_spec.json')['ours']
    public=read(study/'topic_B_measurement/publication_binding.json')['scientific_documents']
    specs=specs|replacements
    extracted={name:selected(args.public_root/public[name]['public_path'] if name in replacements
                              else study/row['path'],row) for name,row in specs.items()}
    partition,weights=read(packet/'partition.json'),read(packet/'weights.json')
    original=study/'topic_B_weighted_dag'
    require(manifest['revision_of']['path']=='topic_B_weighted_dag/manifest.json' and
            manifest['revision_of']['sha256']==digest((original/'manifest.json').read_bytes()),
            'immutable original weighted packet')
    for row in read(original/'manifest.json')['exports']:
        raw=(original/row['path']).read_bytes()
        require(len(raw)==row['bytes'] and digest(raw)==row['sha256'], 'original export changed')
    repaired=read(original/'partition.json')
    for name in ('h.N008.L3.6', 'h.N008.T3.4'):
        require(repaired['owners'][name]['category']=='named_statement_and_proof', 'original owner category')
        repaired['owners'][name]['category']='statement'
        spans=[s for s in repaired['documents']['N008']['spans'] if s['node']==name]
        require(len(spans)==1 and spans[0]['category']=='named_statement_and_proof', 'original span category')
        spans[0]['category']='statement'
    require(repaired==partition, 'revision changed more than four category cells')
    require((packet/'weights.json').read_bytes()==(original/'weights.json').read_bytes(), 'revision changed weights')
    graph=read(study/'topic_B_logical_dag_v2/logical_graph.json')
    coverage=read(study/'topic_B_logical_dag_v2/coverage.json')
    measured=read(study/'topic_B_measurement_results/independent/recount.json')
    result=inspect(partition,weights,graph,coverage,extracted,measured)
    with (packet/'owner_costs.csv').open(newline='') as stream:
        csvrows=list(csv.DictReader(stream))
    expected=[]
    for name,owner in sorted(partition['owners'].items()):
        for form in FORMS:
            expected.append(dict(owner=name,document=owner['document'],category=owner['category'],
                                 normalization=form,**{u:str(weights['owner_costs'][name][form][u]) for u in UNITS}))
    require(csvrows==expected,'all owner CSV rows')
    controls=[]
    for name in ('gap','overlap','wrong_page','wrong_weight','shared_statement','duplicate_owner',
                 'external_zero','unknown_N001_zero','drop_clause','drop_required_route','invent_factor',
                 'exercise_as_proof','statement_span_as_proof'):
        p,w=copy.deepcopy(partition),copy.deepcopy(weights)
        if name=='gap': p['documents']['U_B']['spans'][1]['start']+=1
        elif name=='overlap': p['documents']['U_B']['spans'][1]['start']-=1
        elif name=='wrong_page': p['documents']['U_B']['spans'][0]['physical_pages']=[99]
        elif name=='wrong_weight': w['owner_costs']['UB.front']['NFKC']['utf8_bytes_with_collapsed_whitespace']+=1
        elif name=='shared_statement': w['node_interfaces']['UB.Relative.choices']['owners'].remove('UB.Relative.statement')
        elif name=='duplicate_owner': w['node_interfaces']['UB.F']['owners'].append(w['node_interfaces']['UB.F']['owners'][0])
        elif name=='external_zero': w['node_interfaces']['ext.B97']['weight']=0
        elif name=='unknown_N001_zero': p['N001_original_pdf_cost']=0
        elif name=='drop_clause': w['source_contract_closures'].pop()
        elif name=='drop_required_route': w['source_contract_closures'][0]['replacement']['owners'].pop()
        elif name=='exercise_as_proof': p['owners']['h.N008.L3.6']['category']='named_statement_and_proof'
        elif name=='statement_span_as_proof':
            next(s for s in p['documents']['N008']['spans'] if s['node']=='h.N008.T3.4')['category']='named_statement_and_proof'
        else: w['compression_ratio']=2
        try: inspect(p,w,graph,coverage,extracted,measured)
        except ValueError as error: controls.append(dict(name=name,rejected=True,reason=str(error)))
        else: raise ValueError('undetected corruption '+name)
    # Private excerpts aid semantic boundary review; these must not be exported.
    for name,row in partition['documents'].items():
        text=extracted[name][0]
        excerpts=[]
        for span in row['spans']:
            passage=' '.join(text[span['start']:span['end']].split())
            excerpts.append(dict(owner=span['node'],category=span['category'],pages=span['physical_pages'],
                                 beginning=passage[:160],ending=passage[-120:]))
        (args.out/(name+'_private_boundaries.json')).write_text(json.dumps(excerpts,indent=2,ensure_ascii=False)+'\n')
    output=dict(status='PASS_INDEPENDENT_OWNER_ALLOCATION_AND_CLOSURES',**result,
                csv_rows=len(csvrows),controls=controls,author_manifest_sha256=digest((packet/'manifest.json').read_bytes()),
                logical_manifest_sha256=digest((study/'topic_B_logical_dag_v2/manifest.json').read_bytes()),
                measurement_manifest_sha256=digest((study/'topic_B_measurement_results/manifest.json').read_bytes()),
                source_parser='pypdf 6.13.0 shared with adopted measurement; no author functions imported',
                glyph_scope='Previously accepted font-aware calibration reused; exact glyph positions rechecked, not a new font/visual review.',
                semantic_review_separate=True,private_boundary_excerpts_not_for_export=True,
                label_revision={'category_cells_changed':4,'all_other_partition_data_unchanged':True,
                                'weights_byte_identical':True,'original_manifest_sha256':manifest['revision_of']['sha256']},
                N001_pdf_cost=None,compression_ratio=None,new_source_credit=0,new_question_credit=0)
    (args.out/'report.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(dict(status=output['status'],**result)))


if __name__=='__main__':
    main()
