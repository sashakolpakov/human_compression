#!/usr/bin/env python3
"""Independent SVG/data review. Uses accepted graph and reviewed owner interfaces."""
import copy
import json
from pathlib import Path
import xml.etree.ElementTree as ET

NS = '{http://www.w3.org/2000/svg}'


def need(value, reason):
    if not value:
        raise ValueError(reason)


def read(path):
    return json.loads(path.read_text())


def check_interfaces(weights, reviewed):
    actual = {name: row['owners'] for name, row in weights['node_interfaces'].items()}
    need(actual == reviewed, 'Complete independently read node interfaces')
    need(len(actual) == 119, 'All119 interfaces retained')


def check_graphs(graph, weights, drawings, svg_texts):
    node_by_id = {n['id']: n for n in graph['nodes']}
    logical = {(e['source'], e['target'], e['kind']) for e in graph['edges']
               if e['kind'] in graph['logical_edge_kinds']}
    report = {}
    for side in ['historical', 'new']:
        keep = {n for n, row in node_by_id.items() if row['side'] == side}
        while True:
            added = {a for a, b, _ in logical if b in keep}
            if added <= keep:
                break
            keep.update(added)
        edges = {e for e in logical if e[0] in keep and e[1] in keep}
        drawing = drawings[side]
        need(drawing['nodes'] == sorted(keep), 'All logical nodes on ' + side)
        shown_edges = [(e['source'], e['target'], e['kind']) for e in drawing['edges']]
        need(len(shown_edges) == len(edges) and set(shown_edges) == edges,
             'All typed prerequisite edges on ' + side)
        svg = ET.fromstring(svg_texts[side])
        groups = [e for e in svg if e.tag == NS+'g' and 'data-node' in e.attrib]
        need(len(groups) == len(keep) and {e.attrib['data-node'] for e in groups} == keep,
             'Each displayed node exactly once')
        rectangles = {}
        for group in groups:
            name = group.attrib['data-node']
            node = node_by_id[name]
            texts = group.findall(NS+'text')
            labels = [''.join(e.itertext()) for e in texts]
            cost = weights['node_interfaces'][name]['known_weight']
            expected = 'External proof: unknown' if cost is None else 'Interface text: {:,}'.format(
                cost['calibrated_selected']['NFC']['characters_without_whitespace'])
            need(labels[0] == name and ' '.join(labels[1:-1]) == node['label'] and labels[-1] == expected,
                 'Exact node identity, complete label and interface cost')
            rect = group.find(NS+'rect')
            x, y, width, height = (float(rect.attrib[k]) for k in ['x', 'y', 'width', 'height'])
            need(all(x < float(t.attrib['x']) < x+width and y < float(t.attrib['y']) < y+height
                     for t in texts), 'Text baselines remain inside boxes')
            rectangles[name] = x, y, width, height
            if node['documentary_flags']:
                need(rect.attrib['fill'] == '#fff1e9', 'Documentary qualifications stay visible')
        paths = [e for e in svg if e.tag == NS+'path' and 'data-source' in e.attrib]
        pairs = [(e.attrib['data-source'], e.attrib['data-target']) for e in paths]
        expected_pairs = [(a, b) for a, b, _ in shown_edges]
        need(pairs == expected_pairs, 'Actual SVG arrows preserve prerequisite orientation')
        for edge in paths:
            need(edge.attrib['marker-end'] == 'url(#arrow)' and 'marker-start' not in edge.attrib,
                 'Arrowhead marks the target')
            a, b = edge.attrib['data-source'], edge.attrib['data-target']
            need(rectangles[a][0] < rectangles[b][0], 'Prerequisites appear before their uses')
        need(drawing['expanded_external_proof_cost'] is None and drawing['node_count_factor'] is None,
             'No invented external cost or node-count factor')
        report[side] = {'nodes': len(keep), 'typed_edges': len(edges)}
    return report


def check_with_controls(study, packet):
    graph = read(study/'topic_Affine_logical_dag_v2/logical_graph.json')
    weights = read(packet/'weights.json')
    reviewed = read(Path(__file__).with_name('semantic_reading.json'))['owner_interface_snapshot']
    drawings = read(packet/'graphs.json')
    svgs = {side: (packet/(side+'_graph.svg')).read_text() for side in ['historical','new']}
    check_interfaces(weights, reviewed)
    counts = check_graphs(graph, weights, drawings, svgs)
    controls = []

    def rejected(name, mutator):
        w, d, s = copy.deepcopy(weights), copy.deepcopy(drawings), copy.deepcopy(svgs)
        mutator(w, d, s)
        try:
            check_interfaces(w, reviewed)
            check_graphs(graph, w, d, s)
        except ValueError as exc:
            controls.append({'name': name, 'rejected': True, 'reason': str(exc)})
            return
        raise ValueError('Accepted corruption '+name)

    rejected('omit common branch setup', lambda w,d,s:w['node_interfaces']['h.L4.5.1']['owners'].remove('h.L4.5.setup'))
    rejected('absorb local corollary into parent', lambda w,d,s:w['node_interfaces']['UA.SK']['owners'].append('UA.SK.Local'))
    rejected('omit shared complete source statement', lambda w,d,s:w['node_interfaces']['h.66.Bases']['owners'].remove('h.T5.1.statement'))
    rejected('omit whole program wrapper', lambda w,d,s:w['node_interfaces']['program.kernel64']['owners'].remove('CODE.wrapper'))
    rejected('omit unused smaller-period result from graph', lambda w,d,s:d['new']['nodes'].remove('AL.SmallerPeriods'))
    rejected('reverse prerequisite in data', lambda w,d,s:d['historical']['edges'][0].update(source=d['historical']['edges'][0]['target']))
    rejected('omit actual SVG arrow', lambda w,d,s:s.update(new=s['new'].replace('data-source=', 'removed-source=',1)))
    rejected('external proof cost claimed zero', lambda w,d,s:s.update(historical=s['historical'].replace('External proof: unknown','External proof: 0',1)))
    rejected('erase source qualification color', lambda w,d,s:s.update(historical=s['historical'].replace('#fff1e9','#ffffff',1)))
    rejected('inflate visible interface cost', lambda w,d,s:s.update(new=s['new'].replace('Interface text: 516','Interface text: 1516',1)))
    rejected('count nodes as a factor', lambda w,d,s:d['new'].update(node_count_factor=1.2))
    return {'status':'PASS_INDEPENDENT_INTERFACE_AND_SVG_DATA_CONTROLS', 'graphs':counts,
            'controls':controls, 'actual_browser_test':False,
            'scope':'Reviewed ownership-interface assignments and logical/display conservation. Physical passage correction acceptance and full arithmetic are separate.'}


if __name__ == '__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--study-root',type=Path,required=True)
    p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();need(not a.out.exists(),'Fresh output')
    result=check_with_controls(a.study_root,a.packet)
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(result['status'], result['graphs'],len(result['controls']))
