#!/usr/bin/env python3
"""Exclusive text ownership for Topic B; logical semantics await independent review."""
import argparse,collections,csv,hashlib,importlib.util,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
from accounting import need,sha,build_weights,page_locations,add_weights

F='front_matter';C='context';D='definitions';R='retained_statement';N='named_statement_and_proof'
P='unnumbered_proof';B='substantive_proof_branch';S='statement';REF='references';Q='question_or_excluded_result'
def A(anchor,name,kind,label=None):return (anchor,name,kind,label or name)

def boundaries():
    return {
 'U_B':[
 A(None,'UB.front',F),A('1 Introduction','UB.intro',C),
 A('2 Flags, parabolics and coset coordinates','UB.Incidence',D),
 A('For subgroups','UB.CosetData',D),A('Proposition UB.Coset (','UB.Coset.statement',S),
 A('Proof. Under','UB.Coset.flags',B),A('For completeness, a coset incidence graph','UB.Coset.connected',B),
 A('Conversely, flag transitivity','UB.Coset.converse',B),A('An action is primitive','UB.Primitivity',D),
 A('Lemma UB.Flags (','UB.Flags',N),A('For 𝐵 ≤ 𝐺','UB.Independence',D),
 A('3 Relative generation from residual maximality','UB.relative.setup',D),
 A('Theorem UB.Relative (','UB.Relative.statement',S),A('Proof. Distinctness','UB.Relative.choices',B),
 A('Prove (2) by downward induction','UB.Relative.induction',B),
 A('Theorem UB.Generation (','UB.Generation',N),
 A('4 Weighted forests and complete flags','UB.ForestData',D),A('Theorem UB.F (','UB.F.statement',S),
 A('Proof. A permutation belongs','UB.F.intersections',B),A('The coset','UB.F.flags',B),
 A('Repeated use of (1)','UB.F.geometry',B),A('For unit blocks','UB.F.unit',P),
 A('5 Overgroups of a two-block stabilizer','UB.overgroups.heading',C),
 A('Lemma UB.Overgroups (','UB.Overgroups.statement',S),
 A('Proof. The case','UB.Overgroups.interval',B),A('If an edge bisects','UB.Overgroups.balance',B),
 A('Use and attribution','UB.attribution',C),A('References','UB.references',REF)],
 'B1':[
 A(None,'B1.front',F),A('1 Introduction','B1.intro',C),
 A('2 Retained classification and conventions','B1.Conventions',D),A('B97 (foundational classification)','B1.B97',R),
 A('3 The unit-weight property profile','B1.profile.heading',C),
 A('Proposition B1.Profile (','B1.Profile.statement',S),A('Proof. The unit-weight','B1.Profile.local',B),
 A('Each connected remaining edge set','B1.Profile.residual',B),A('Lemma UB.Overgroups gives','B1.Profile.middle',B),
 A('Every nontrivial subtree of a star','B1.Profile.star',B),
 A('4 Reconstructing the tree from the diagram','B1.reconstruction.heading',C),
 A('Lemma B1.Reconstruction (','B1.Reconstruction',N),
 A('5 All four property conclusions','B1.source.heading',C),A('Corollary B1.Source (','B1.Source',N),
 A('References and retained inputs','B1.references',REF)],
 'B2':[
 A(None,'B2.front',F),A('1 Introduction','B2.intro',C),
 A('2 Hypotheses, retained classification inputs and quotient bounds','B2.Hypotheses',R),
 A('Proposition B2.RelativeBound (','B2.RelativeBound',N),
 A('3 Tree markings and the parity construction','B2.sign.heading',C),A('Theorem B2.Sign (','B2.Sign',N),
 A('4 The extremal converse and its three counts','B2.extremal.heading',C),A('Lemma B2.Blocks (','B2.Blocks',N),
 A('Theorem B2.Extremal (','B2.Extremal.statement',S),A('Proof. By W1','B2.Extremal.omissions',B),
 A('For each 𝑖 > 1','B2.Extremal.tree',B),A('Deleting','B2.Extremal.local',B),
 A('Now suppose the original family','B2.Extremal.borel',B),A('Corollary B2.Count (','B2.Count',N),
 A('5 Recognizing every maximum-rank geometry','B2.maxrank.heading',C),
 A('Theorem B2.MaxRank (','B2.MaxRank.statement',S),A('Proof of existence.','B2.MaxRank.ordinary',B),
 A('For a sign-kernel marking','B2.MaxRank.sign',B),
 A('Proof of uniqueness in the RWPRI case.','B2.MaxRank.unique',B),
 A('Proof for firm, residually connected','B2.MaxRank.general',B),
 A('6 The full source contract','B2.source.heading',C),A('Corollary B2.Source (','B2.Source',N),
 A('References and retained inputs','B2.references',REF)],
 'B3':[
 A(None,'B3.front',F),A('1 Introduction','B3.intro',C),
 A('2 Relative generation and removal of normal kernels','B3.quotient.heading',C),
 A('Proposition B3.Quotient (','B3.Quotient',N),
 A('3 The normal Frattini ladder','B3.ladder.heading',C),A('Lemma B3.Maximal (','B3.Maximal',N),
 A('Define Φ','B3.Nongeneration',P),A('Theorem B3.Transport (','B3.Transport',N),
 A('The maximal-overgroup hypothesis holds','B3.correction.preview',C),
 A('Theorem B3.Ladder (','B3.Ladder.statement',S),A('Proof. Choose','B3.Ladder.finite',B),
 A('Suppose 𝑁 ≰ 𝐵','B3.Ladder.propagation',B),
 A('4 The complete geometry and coordinate classification','B3.Hypotheses',D),
 A('Theorem B3.Frattini.','B3.Frattini.statement',S),
 A('Proof. By UB.Flags','B3.Frattini.containment',B),A('An element acts trivially','B3.Frattini.core',B),
 A('The quotient','B3.Frattini.free',P),A('For relative generating families','B3.InfiniteCorrection',P),
 A('Theorem B3.Coordinates.','B3.Coordinates.statement',S),A('Proof. B3.Frattini','B3.Coordinates.basis',B),
 A('The cosets','B3.Coordinates.geometry',B),A('Conversely every family','B3.Coordinates.count',P),
 A('Two subsidiary assertions','B3.Product',P),A('If 𝑈, 𝑊','B3.Subspace',P),
 A('Finally, every residue','B3.ResidueTest',P),
 A('5 The admitted source statements','B3.source.heading',C),A('Corollary B3.Source (','B3.Source',N),
 A('References and retained inputs','B3.references',REF)],
 'B4':[
 A(None,'B4.front',F),A('1 Introduction','B4.intro',C),
 A('2 The weighted-star construction','B4.StarData',D),A('Theorem B4.Star (','B4.Star.statement',S),
 A('Proof. All positive-weight','B4.Star.residues',B),A('Equation ( 1) is the tensor-product','B4.Star.links',B),
 A('Here ⊗ denotes','B4.distance.setup',D),A('Proposition B4.Distance (','B4.Distance.statement',S),
 A('Proof. If','B4.Distance.walks',B),A('The number of common neighbors','B4.Distance.gonality',B),
 A('It follows that the Buekenhout diagram','B4.Diagram',P),
 A('3 Recovering the permutation action','B4.typed.heading',C),A('Lemma B4.Johnson.','B4.Johnson',N),
 A('Proposition B4.TypedAut.','B4.TypedAut.statement',S),A('Proof. Within one type','B4.TypedAut.points',B),
 A('These permutations are all equal.','B4.TypedAut.synchronization',B),
 A('4 Recovering the types from the uncolored graph','B4.uncolored.motivation',C),
 A('Let 𝒱','B4.Spectrum',P),A('The graph adjacency matrix','B4.TypeEigenspace',P),
 A('Theorem B4.Aut (','B4.Aut.statement',S),A('Proof. The graph has','B4.Aut.independent',B),
 A('For 𝑘 = 2','B4.Desargues',P),
 A('5 The corrected source conclusions','B4.source.heading',C),A('Corollary B4.Source (','B4.Source',N),
 A('References and retained inputs','B4.references',REF)],
 'N003':[
 A(None,'h.N003.front',F),A('1 Independent generating sets','h.N003.Definitions',D),
 A('The ﬁrst result is not','h.N003.quotient.attribution',C),A('Theorem 1.1','h.N003.T1.1',N),
 A('It follows that, if','h.N003.direct_product_question',Q),
 A('2 Symmetric groups','h.N003.W1Recall',R),A('We are interested in the structure','h.N003.tree.defs',D),
 A('Theorem 2.1','h.N003.T2.1.statement',S),A('Proof We prove the converse ﬁrst.','h.N003.T2.1.converse',B),
 A('We now turn to the forward implication.','h.N003.T2.1.blocks',B),
 A('We construct a graph','h.N003.T2.1.tree',B),A('Next, we claim that','h.N003.T2.1.types',B),
 A('Corollary 2.2','h.N003.C2.2',N),A('Corollary 2.3','h.N003.C2.3',N),A('Corollary 2.4','h.N003.C2.4',N),
 A('Remark It is possible','h.N003.small_cases',Q),A('We end this section with a question.','h.N003.CFSG_question',Q),
 A('3 Geometries','h.N003.Coset',D),A('Theorem 3.1','h.N003.T3.1',N),
 A('The converse is not true.','h.N003.geometry.transition',C),A('Theorem 3.2','h.N003.T3.2.statement',S),
 A('Proof We have seen','h.N003.T3.2.unique',B),A('Conversely, let','h.N003.T3.2.converse_setup',D),
 A('Let T be a tree','h.N003.T3.2.ordinary',B),A('Now let S∗','h.N003.T3.2.sign',B),
 A('Corollary 3.3','h.N003.C3.3',N),A('Remark The diagram','h.N003.diagram_remark',Q),
 A('Remark Theorem 3.2','h.N003.small_geometry_remark',Q),A('References','h.N003.references',REF)],
 'N008':[
 A(None,'h.N008.front',F),A('1. Geometries','h.N008.Definitions',D),
 A('2. Independent generating sets','h.N008.Definitions',D),
 A('2.2. Independent generating sets and the Frattini subgroup','h.N008.frattini.defs',D),
 A('Hence','h.N008.Nongeneration',S),A('Theorem 2.1.','h.N008.T2.1',N),
 A('2.3. Independent generating sets and','h.N008.RelativeRecall',R),
 A('A natural question','h.N008.motivation',C),A('3. New applications','h.N008.containment.setup',D),
 A('Theorem 3.1.','h.N008.T3.1.statement',S),A('Proof. For','h.N008.T3.1.ladder',B),
 A('It remains to prove statement (1).','h.N008.T3.1.propagation',B),
 A('A geometry where all stabilizers','h.N008.P3.2',R),
 A('From Theorem 3.1 we now conclude','h.N008.C3.3',N),
 A('The groups of the form','h.N008.frattini_free.setup',D),A('Theorem 3.4.','h.N008.T3.4',N),
 A('3.2. Firm','h.N008.DirectSum',D),A('Proposition 3.5.','h.N008.P3.5',R),
 A('3.2.2. Firm','h.N008.pgroup.input',R),A('Lemma 3.6.','h.N008.L3.6',N),
 A('Proposition 3.7.','h.N008.P3.7',N),A('Theorem 3.8.','h.N008.T3.8',N),
 A('4. Implications','h.N008.frattini_free.proof',P),
 A('The following theorem describes','h.N008.gaschutz.setup',R),A('Theorem 4.1.','h.N008.gaschutz',R),
 A('4.1.1. Frattini free groups are scarce','h.N008.smallgroup_statistics',Q),
 A('4.2. The Φ-test for a residue','h.N008.Test4.2',P),
 A('4.2.1. How to compute','h.N008.computation_note',Q),
 A('4.3. Other reduction in some cases','h.N008.Core4.3',P),
 A('In some cases K is a larger subgroup','h.N008.archer_recall',R),
 A('Acknowledgement.','h.N008.acknowledgement',C),A('References','h.N008.references',REF)],
 'L030':[
 A(None,'h.L030.front',F),A('1. Introduction','h.L030.intro',C),
 A('Construction 1.1.','h.L030.Construction1.1',D),
 A('These geometries have several nice properties','h.L030.theorem.transition',C),
 A('Theorem 1.2.','h.L030.T1.2.existence',S),A('Its automorphism groups','h.L030.T1.2.groups',S),
 A('The Buekenhout diagram of','h.L030.T1.2.parameters',S),
 A('We want to highlight','h.L030.localgraph.context',C),A('Corollary 1.3.','h.L030.C1.3',N),
 A('Corollary 1.4.','h.L030.C1.4',S),A('We believe that','h.L030.organization',C),
 A('2. Preliminaries','h.L030.Definitions',D),
 A('Lemma 2.1.','h.L030.L2.1',N),A('Lemma 2.2.','h.L030.L2.2',N),
 A('2.2. Incidence','h.L030.Definitions',D),
 A('3. The neighborhood geometry','h.L030.double.setup',D),
 A('Lemma 3.1.','h.L030.L3.1',N),A('Lemma 3.2.','h.L030.L3.2',N),A('Lemma 3.3.','h.L030.L3.3',N),
 A('4. Proof of Theorem 1.2','h.L030.family.heading',C),
 A('Lemma 4.1.','h.L030.L4.1',N),A('Lemma 4.2.','h.L030.L4.2',N),A('Lemma 4.3.','h.L030.L4.3',N),
 A('Lemma 4.4.','h.L030.L4.4',N),A('Corollary 4.5.','h.L030.C4.5',S),
 A('Lemma 4.6.','h.L030.L4.6',N),A('Lemma 4.7.','h.L030.L4.7',N),
 A('Theorem 1.2 is a summary','h.L030.T1.2.assembly',P),
 A('We highlight that','h.L030.IP.context',C),A('Corollary 4.8.','h.L030.C4.8',N),
 A('Observe that when','h.L030.diagram.remark',Q),
 A('5. Connection with locally X graphs','h.L030.applications.context',C),
 A('Proof of Corollary 1.3.','h.L030.C1.3',N),A('Corollary 5.1.','h.L030.C5.1',N),
 A('It would be interesting','h.L030.future_and_literature',Q),
 A('Acknowledgements','h.L030.acknowledgements',C),A('References','h.L030.references',REF)],
    }

def interfaces(graph,owners,owner_costs):
    """Explicit semantic owner interfaces, separate from disjoint cost leaves."""
    nodes={n['id']:n for n in graph['nodes']};children=collections.defaultdict(list)
    for n in graph['nodes']:
        if n.get('parent'):children[n['parent']].append(n['id'])
    supplements={
      'UB.Relative':['UB.relative.setup'],
      'UB.F':['UB.F.unit'],
      'UB.TwoBlockData':['UB.Overgroups.statement'],
      'B1.Reconstruction':['B1.B97'],
      'B4.Distance':['B4.distance.setup'],
      'h.N003.T2.1':['h.N003.tree.defs'],
      'h.N003.T3.2':['h.N003.T3.2.converse_setup'],
      'h.N008.Definitions':['h.N008.frattini.defs'],
      'h.N008.T3.1':['h.N008.containment.setup'],
      'h.N008.T3.4':['h.N008.frattini_free.setup','h.N008.frattini_free.proof'],
      'h.N008.P3.7':['h.N008.pgroup.input'],
      'h.N008.T3.8':['h.N008.pgroup.input'],
      'h.L030.T1.2':['h.L030.T1.2.assembly'],
      'h.L030.L3.1':['h.L030.double.setup'],
      'h.L030.L3.2':['h.L030.double.setup'],
      'h.L030.L3.3':['h.L030.double.setup'],
    }
    result={}
    def link(name):
        if name in result:return result[name]
        n=nodes[name]
        paid=set(supplements.get(name,[]))
        if name in owners:paid.add(name)
        if name+'.statement' in owners:paid.add(name+'.statement')
        if n.get('parent') and n['parent']+'.statement' in owners:
            paid.add(n['parent']+'.statement')
        for child in children[name]:paid.update(link(child)['owners'])
        need(paid<=owners.keys(),'all owner references exist')
        need(all(owners[x]['document']==n['document'] for x in paid),'interface stays in its own document')
        unknown=n['side'] in ['external','verification'] or n['document']=='N001'
        need(not unknown or not paid,'unknown or verification node is not silently assigned measured PDF cost')
        reason=('missing N001 original PDF' if n['document']=='N001' else
                'expanded retained proof cost is unknown' if n['side']=='external' else
                'separate validation evidence; no scientific PDF cost' if n['side']=='verification' else
                'union of exclusively owned passages, including the shared full parent statement where a branch uses one; parent/child displays can overlap')
        need(unknown or bool(paid),'unmapped measured logical node: '+name)
        result[name]=dict(owners=sorted(paid),weight=None if unknown else add_weights([owner_costs[x] for x in sorted(paid)]),
            cost_status=reason,charged_as_an_additional_item=False,full_dependency_cost=None)
        return result[name]
    for name in nodes:link(name)
    return result

def closure_cost(names,graph,links,owner_costs,owners):
    nodes={n['id']:n for n in graph['nodes']}
    paid=sorted({o for name in names for o in links[name]['owners']})
    unknown=[name for name in names if links[name]['weight'] is None]
    return dict(logical_nodes=sorted(names),owners=paid,known_extracted_text_subtotal=add_weights([owner_costs[x] for x in paid]),
        by_document={key:add_weights([owner_costs[x] for x in paid if owners[x]['document']==key]) for key in sorted({owners[x]['document'] for x in paid})},
        unknown_inputs=sorted(unknown),expanded_dependency_cost=None,
        scope='Selected documentary prerequisite union, not a minimal proof or a complete-paper denominator. Omitted context and all full-paper text remain charged in the accepted overall comparison.')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    root=a.study_root.resolve();need(not a.out.exists(),'fresh output');a.out.mkdir(parents=True)
    graph=json.loads((root/'topic_B_logical_dag_v2/logical_graph.json').read_text())
    need(sha((root/'topic_B_logical_dag_v2/manifest.json').read_bytes())=='a825b42e248e2d4fe9a853ff0baefb40c7590642eca8b028e0d6471333e5bf4b','frozen corrected logical author packet')
    need(sha((root/'topic_B_logical_independent_review/manifest.json').read_bytes())=='5d848fc049ee84bacd7b38332ce413ffd378228af7f1d568a26448c9935b980f','independent logical acceptance')
    need(sha((root/'topic_B_measurement_results/manifest.json').read_bytes())=='c61503c52b1e0136b0eb70ebe7993c63dc635933e6ae0bf9a50d7c164d211609','fixed numerical edition')
    spec=importlib.util.spec_from_file_location('bmeasure',root/'topic_B_measurement/extract_inputs.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    bindings=json.loads((root/'topic_B_measurement/source_input_spec.json').read_text())['sources']|json.loads((root/'topic_B_measurement/replacement_input_spec.json').read_text())['ours']
    extracted={k:m.document(root,k,v) for k,v in bindings.items()};texts={k:v[2] for k,v in extracted.items()}
    rows=boundaries();parts={};owners={}
    for key,blocks in rows.items():
        text=texts[key];cuts=[];at=-1
        for anchor,name,kind,label in blocks:
            if anchor is None:pos=0
            else:
                match=re.search(r'\s+'.join(re.escape(x) for x in anchor.split()),text[at+1:]);pos=at+1+match.start() if match else -1
            need(pos>at,(key,'missing or out-of-order anchor',anchor));cuts.append((pos,name,kind,label));at=pos
        spans=[]
        for i,(start,name,kind,label) in enumerate(cuts):
            end=cuts[i+1][0] if i+1<len(cuts) else len(text)
            spans.append(dict(start=start,end=end,node=name,category=kind,label=label,sha256=sha(text[start:end].encode())))
            if name in owners:need(owners[name]['document']==key,'same owner document')
            owners[name]=dict(id=name,document=key,label=label,category=kind)
        page_locations(extracted[key][0],bindings[key],spans);parts[key]=spans
    need(set(parts)==set(bindings),'all eight available documents owned')
    owner_costs,doc_costs=build_weights(texts,bindings,parts,owners)
    measured=json.loads((root/'topic_B_measurement_results/independent/recount.json').read_text())
    for k,d in doc_costs.items():
        for form,values in d.items():
            for unit,value in values.items():need(value==measured['documents'][k]['calibrated_selected'][form][unit],'accepted whole-document conservation')
    links=interfaces(graph,owners,owner_costs)
    coverage=json.loads((root/'topic_B_logical_dag_v2/coverage.json').read_text())
    clauses=[dict(adapter=row['adapter'],source_id=row['source_id'],historical=closure_cost(row['historical_closure'],graph,links,owner_costs,owners),
         replacement=closure_cost(row['new_closure'],graph,links,owner_costs,owners)) for row in coverage['rows']]
    apps={k:closure_cost(v,graph,links,owner_costs,owners) for k,v in graph['new_output_closures'].items()}
    mapped={x for row in links.values() for x in row['owners']}
    partition=dict(status='AUTHOR_EXCLUSIVE_OWNERSHIP_PENDING_INDEPENDENT_REVIEW',text_representation='calibrated_selected before NFC/NFKC normalization',
        documents={k:dict(text_sha256=sha(texts[k].encode()),length=len(texts[k]),pdf_sha256=bindings[k]['pdf_sha256'],spans=parts[k]) for k in parts},
        owners=owners,unmapped_owners=[owners[k] for k in sorted(set(owners)-mapped)],
        boundary='Every selected character has exactly one owner. Context, references and excluded source claims remain fully charged; no primary text is exported.',
        N001_original_pdf_cost=None)
    weights=dict(status='AUTHOR_WEIGHTS_OVER_ACCEPTED_LOGIC_PENDING_INDEPENDENT_OWNERSHIP_REVIEW',owner_costs=owner_costs,document_costs=doc_costs,
        node_interfaces=links,source_contract_closures=clauses,new_application_closures=apps,
        primary_coordinate=['NFC','characters_without_whitespace'],all_units=list(next(iter(doc_costs.values()))['NFC']),
        scope='These explanatory costs do not replace the accepted complete-document comparison. No node-count factor is defined.',
        whole_historical_pdf_cost=None,expanded_external_proof_cost=None,graphic_cost=None,compression_ratio=None,new_source_credit=0,new_question_credit=0)
    (a.out/'partition.json').write_text(json.dumps(partition,indent=2)+'\n')
    (a.out/'weights.json').write_text(json.dumps(weights,indent=2)+'\n')
    with (a.out/'owner_costs.csv').open('w',newline='') as stream:
        writer=csv.writer(stream);writer.writerow(['owner','document','category','normalization']+list(weights['all_units']))
        for name in sorted(owners):
            for form in ['NFC','NFKC']:writer.writerow([name,owners[name]['document'],owners[name]['category'],form]+[owner_costs[name][form][m] for m in weights['all_units']])
    input_paths=['topic_B_logical_dag_v2/manifest.json','topic_B_logical_dag_v2/logical_graph.json','topic_B_logical_dag_v2/coverage.json',
      'topic_B_logical_independent_review/manifest.json','topic_B_logical_independent_review/review.json',
      'topic_B_measurement/manifest.json','topic_B_measurement/protocol.json','topic_B_measurement/source_input_spec.json',
      'topic_B_measurement/replacement_input_spec.json','topic_B_measurement/extract_inputs.py',
      'topic_B_measurement_results/manifest.json','topic_B_measurement_results/independent/recount.json',
      'topic_B_measurement_results/independent/manifest.json','topic_B_measurement_results/independent/review.json',
      'topic_B_arithmetic_independent_review/manifest.json','topic_A_weighted_dag_v2/accounting.py']
    inventory=dict(status='AUTHOR_BOUNDARY_PENDING_OWNERSHIP_REVIEW',inputs=[dict(path=n,bytes=(root/n).stat().st_size,sha256=sha((root/n).read_bytes())) for n in input_paths],
       primary_text_exported=False,logical_packet_independently_accepted=True,
       measurement_boundary='The separately accepted complete PDF costs, furniture rules and eight one-codepoint glyph substitutions are unchanged.',
       allocation_rule='Normalize each owned chunk under NFC or NFKC and require concatenation to equal whole-document normalization. Each complete whitespace/alphanumeric token belongs to the owner of its first character. Each nonspace codepoint belongs to its unique owner; each internal collapsed whitespace run belongs to its first owner. Leading/trailing whitespace is uncharged in the collapsed metrics.',
       reuse='The exact allocator from accepted Topic A weighted v2 is reused through build_weights; no old topic cost is imported or shared across topics.',
       known_pdf_documents=list(parts),missing_source_pdf='N001',node_count_ratio=None,
       logical_rule='The graph remains a separate frozen packet. A parent interface is a union of owner IDs, not another additive proof. Only graph logical edge kinds enter prerequisite closure.')
    (a.out/'input_bindings.json').write_text(json.dumps(inventory,indent=2)+'\n')
    print(json.dumps(dict(documents=len(parts),spans=sum(map(len,parts.values())),owners=len(owners),interfaces=len(links),clauses=len(clauses))))
if __name__=='__main__':main()
