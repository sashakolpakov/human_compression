#!/usr/bin/env python3
"""Additive response to the independent edge review; original packet immutable."""
from pathlib import Path
import collections,copy,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
def need(x,m):
    if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(p):
    b=(ROOT/p).read_bytes();return {'path':p,'bytes':len(b),'sha256':sha(b)}
old=ROOT/'topic_A_logical_dag/logical_graph.json'
need(sha(old.read_bytes())=='a3e848e7e6bb75f292404780b78aa4a8114ca336358d8471bbd8f9d734782d6f','original graph hash')
g=json.loads(old.read_text());idx={n['id']:n for n in g['nodes']}
g['status']='AUTHOR_REVISED_IN_RESPONSE_TO_INDEPENDENT_EDGE_REVIEW'
g['schema']='topic_A_logical_dependency_graph_v3'
idx['h.MagmaN009']['label']='Historical GAP presentation, order, isomorphism and IP computations'
idx['h.MagmaN009']['deprecated_id_note']='Stable legacy ID contains a mistaken Magma label; the source explicitly uses GAP. No Magma input is asserted for N009.'
idx['h.MagmaN009']['locators']=[{'primary_pdf':'sources/phase17_gomi_loyola2018.pdf','physical_pages':[8,9,10,11,12,13,14],'scope':'GAP computations explicitly named in the rank-three and universal-presentation procedures.'}]
idx['A5.collection']['label']='The eight complete bare source presentations'
idx['A5.collection']['category']='presentation_data'
idx['N009.Table2']['category']='imported_table_data'
idx['N009.Table2']['documentary_validity']='Imported order-512 Atlas definitions. Neither the source lift theorem nor GAP generation is asserted to prove these imported records.'
removed=[];edges=[]
for e in g['edges']:
    if ((e['target']=='N009.Table2' and e['source'] in ('N009.T3.8','h.MagmaN009')) or
        (e['source']=='A6.centers' and e['target']=='A6.exceptional')):
        removed.append(e);continue
    if e['source']=='A5.collection':
        e['kind']='definition_use'
        e['evidence']='The case proof uses the specified bare presentation relations; the displayed table is data and does not itself prove commutator collection identities.'
    edges.append(e)
g['edges']=edges
def edge(a,b,kind,evidence,locators=None):
    need(not any((e['source'],e['target'],e['kind'])==(a,b,kind) for e in g['edges']),'duplicate edge')
    g['edges'].append({'source':a,'target':b,'kind':kind,'evidence':evidence,
                      'target_evidence':locators or copy.deepcopy(idx[b]['locators']),'necessity_claim':False})
for a,b,evidence in [
 ('N009.Table2','N009.Table3','Physical pp9–10, Example3.9 ClassIII: the four order512 input presentations in Table2 are lifted by the three relation assignments in Table3.'),
 ('N009.L2.2','N009.Table3','Physical p8 explicitly requires the rank-three intersection criterion; pp9–10 describe the GAP checks for Table3.'),
 ('N009.Table3','N009.Table4','Physical pp9–10: Table4 summarizes the ClassIII outputs of Table3.'),
 ('N009.E3.9','N009.Table4','Physical p9, Example3.9 ClassII: the two square-map lifts supply the ClassII rows in Table4.'),
 ('N009.L2.5','N009.Table5','Physical p9 restricts the possible rank-three types using Lemma2.5; p11 gives the resulting type census.'),
 ('N009.L2.2','N009.Table5','Physical p8 explicitly prescribes testing the rank-three intersection condition before accepting lifted groups.')]:
    edge(a,b,'historical_documented_use',evidence)
edge('ext.polytope','N009.T4.2','historical_documented_use',
     'Source physical p12, Theorem4.2, explicitly attributes the geometric universal-cover statement to Abstract Regular Polytopes, p97.')
edge('ext.polytope','A6.examples','retained_input_use',
     'Section3.2 explicitly retains the regular-polytope correspondence and universal geometric interpretation; these facts are not certified by merely finite group computations.')

# The decomposition is a retained theorem, distinct from the center calculation.
path='topic_A_volume/order-1024-markings.tex';text=(ROOT/path).read_text()
a=text.index('For the sole infinite row');b=text.index('\\textbf{Proposition N6',a)
loc={'path':path,'first_line':text[:a].count('\n')+1,'last_line':text[:b].count('\n')+1,
     'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':sha(text[a:b].encode()),
     'scope':'Complete retained marked decomposition (N6), not the preceding center formulas.'}
for e in g['edges']:
    if e['source']=='ext.exceptionalUniversal' and e['target']=='A6.exceptional':
        e['kind']='retained_input_use';e['evidence']='The exact infinite universal and its marked decomposition are retained in display (N6). The center-formula proof is not needed for the parity/kernel argument.'
        e['target_evidence']=[loc]+e['target_evidence']
oldloc=idx['A6.centers']['locators'][0]
oldloc['end_codepoint_exclusive']=a;oldloc['last_line']=text[:a].count('\n')+1
oldloc['sha256_utf8']=sha(text[oldloc['start_codepoint']:a].encode())
idx['A6.exceptional']['locators'].insert(0,loc)

# Bind the already reviewed attribution-only current edition without rewriting
# any older evidence string or mutating its archived file.
final='topic_A_volume_A6_attribution/order-1024-markings.tex';newtext=(ROOT/final).read_text()
for node in g['nodes']:
    if node['document']!='A6':continue
    for l in node['locators']:
        if l.get('path')!=path or 'start_codepoint' not in l:continue
        snippet=text[l['start_codepoint']:l['end_codepoint_exclusive']]
        at=newtext.find(snippet);need(at>=0,'A6 mathematical evidence changed')
        l.update(path=final,start_codepoint=at,end_codepoint_exclusive=at+len(snippet),
                 first_line=newtext[:at].count('\n')+1,last_line=newtext[:at+len(snippet)].count('\n')+1)
for e in g['edges']:
    for l in e.get('target_evidence',[]):
        if l.get('path')!=path or 'start_codepoint' not in l:continue
        snippet=text[l['start_codepoint']:l['end_codepoint_exclusive']]
        at=newtext.find(snippet);need(at>=0,'A6 edge evidence changed')
        l.update(path=final,start_codepoint=at,end_codepoint_exclusive=at+len(snippet),
                 first_line=newtext[:at].count('\n')+1,last_line=newtext[:at+len(snippet)].count('\n')+1)
for p in [final,'topic_A_volume_A6_attribution/order-1024-markings.pdf',
          'topic_A_volume_A6_attribution/manifest.json','topic_A_logical_dag/manifest.json']:
    if not any(x['path']==p for x in g['immutable_inputs']):g['immutable_inputs'].append(binding(p))
kinds={'proof_use','retained_input_use','retained_algorithm_use','computational_use','branch_membership','output_assembly','definition_use'}
inc=collections.defaultdict(set)
for e in g['edges']:
    if e['kind'] in kinds:inc[e['target']].add(e['source'])
def closure(start):
    found={start};todo=[start]
    while todo:
        for x in inc[todo.pop()]-found:found.add(x);todo.append(x)
    return sorted(found)
g['new_output_closures']={n:closure(n) for n in g['new_main_outputs']}
g['revision']={'original_graph_sha256':sha(old.read_bytes()),
 'public_proof_edition_commit':'6641c356b39ea9ca650542a41869b7811fdfc0ff',
 'status':'Precise independent-review requests applied; final independent acceptance pending.',
 'mathematical_papers_changed':False,'original_packet_preserved':True,
 'changes':['GAP attribution corrected with stable deprecated ID.',
 'Imported Atlas Table2 distinguished from derived lift tables; explicit data and criterion dependencies added.',
 'Retained polytope universality charged to historical Theorem4.2 and current universal examples.',
 'A5.collection identified as eight presentation data records; definition-use edges remain prerequisites.',
 'Center formulas detached from exceptional parity argument; exact retained decomposition bound separately.',
 'Current A6 attribution-only edition bound; mathematical evidence snippets unchanged.']}
g['checks'].update(nodes=len(g['nodes']),edges=len(g['edges']),
 node_categories=dict(collections.Counter(n['category'] for n in g['nodes'])),
 edge_categories=dict(collections.Counter(e['kind'] for e in g['edges'])))
g['revision']['supersedes_metadata_only']='topic_A_logical_dag_v2/manifest.json'
(HERE/'logical_graph.json').write_text(json.dumps(g,ensure_ascii=False,indent=2)+'\n')
(HERE/'delta.json').write_text(json.dumps({'original':binding('topic_A_logical_dag/logical_graph.json'),
 'removed_edges':removed,'changes':g['revision'],'nodes':len(g['nodes']),'edges':len(g['edges'])},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'nodes':len(g['nodes']),'edges':len(g['edges']),'graph_sha256':sha((HERE/'logical_graph.json').read_bytes())}))
