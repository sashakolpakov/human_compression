#!/usr/bin/env python3
"""Author exact full-text ownership over the adopted calibrated PDF extraction.

Primary extracted text stays in memory. No ratios, graph admission, or source credit.
"""
from pathlib import Path
import bisect,collections,copy,csv,hashlib,importlib.util,json,re,unicodedata

HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(x,m):
    if not x:raise ValueError(m)
def read(p):return json.loads((ROOT/p).read_text())
def bind(p):
    b=(ROOT/p).read_bytes();return dict(path=p,sha256=sha(b),bytes=len(b))
LOGICAL_MANIFEST='5b85fbb96bceb570f9458819c75cfca62c5707c094a239ef16e061640517e523'
need(bind('topic_A_logical_dag/manifest.json')['sha256']==LOGICAL_MANIFEST,'frozen logical graph')
LOGICAL_GRAPH='topic_A_logical_dag_v3/logical_graph.json'
need(bind(LOGICAL_GRAPH)['sha256']=='190f6fa26ab13627a25201c7a70bb0309826a2f34369af8765627ff059fe7dd4','reviewed corrective graph')
graph=read(LOGICAL_GRAPH)
ss=read('topic_A_measurement/source_input_spec.json')
REPLACEMENT_SPEC='topic_A_numerical_audit/final_replacement_input_spec_private.json'
need(bind(REPLACEMENT_SPEC)['sha256']=='9b4de0a1e44942728d38a24d7c908a9aa84e92d57e76ce5f1b02505eb87ba5ba','final A6 boundary')
rs=read(REPLACEMENT_SPEC)
spec=ss['sources']|rs['ours']
im=importlib.util.spec_from_file_location('measure',ROOT/'topic_A_measurement/extract_inputs.py')
measure=importlib.util.module_from_spec(im);im.loader.exec_module(measure)
extracted={k:measure.document(ROOT,k,v) for k,v in spec.items()}
texts={k:v[2] for k,v in extracted.items()}
parts={};owners={}
F='front_matter';C='context';D='definitions';R='retained_statement';N='named_statement_and_proof'
B='substantive_proof_branch';S='statement';P='unnumbered_proof';T='table_or_mathematical_data';Q='question';REF='references'
def A(anchor,id,kind,label=None):return anchor,id,kind,label or id
def doc(k,rows):
    text=texts[k];cuts=[];at=-1
    for anchor,id,kind,label in rows:
        if anchor is None:pos=0
        else:
            pat=r'\s+'.join(re.escape(x) for x in anchor.split())
            m=re.search(pat,text[at+1:]);pos=at+1+m.start() if m else -1
        need(pos>=0,(k,'missing anchor',anchor));need(pos>at,(k,'cut order',anchor))
        cuts.append((pos,id,kind,label));at=pos
    need(cuts[0][0]==0,'full start')
    spans=[]
    for i,(a,id,kind,label) in enumerate(cuts):
        b=cuts[i+1][0] if i+1<len(cuts) else len(text)
        spans.append(dict(start=a,end=b,node=id,category=kind,label=label,sha256=sha(text[a:b].encode())))
        if id not in owners:owners[id]=dict(id=id,document=k,label=label,category=kind)
        else:need(owners[id]['document']==k,('cross-document owner',id))
    parts[k]=spans

# The actual common paper. Statements and substantive branches are paid once;
# named theorem aggregates are reconstructed below from these exclusive leaves.
doc('U_A',[
A(None,'UA.front',F),A('1 Introduction','UA.intro',C),A('2 Markings, images and kernels','UA.defs',D),
A('All subgroup products below','UA.retained.initial',R),
A('Lemma UA.K0 (','UA.K0',N),A('Theorem UA.K (','UA.K',N),
A('The next result concerns','UA.quotient.motivation',C),A('Theorem UA.Q (','UA.Q',N),
A('3 Deletion maps and supported extensions','UA.deletion.defs',D),A('Proposition UA.D (','UA.D',N),
A('We now assemble extensions','UA.SK.motivation',C),A('Theorem UA.SK (','UA.SK',S),
A('Proof. The compatibility equations','UA.SK.tuples',B),A('We first prove, by induction','UA.SK.isolation',B),
A('The kernel of','UA.SK.generation',B),A('The image equality','UA.SK.profiles',B),
A('The coordinate products in','UA.SK.intersections',B),
A('Corollary UA.SK.Local (','UA.SK.Local',N),A('Corollary UA.SK.Delete (','UA.SK.Delete',N),
A('Corollary UA.SK.Central (','UA.SK.Central',N),A('Corollary UA.SK.Separator (','UA.SK.Separator',N),
A('Proposition UA.Fiber (','UA.Fiber',N),
A('4 Recognition of presentations','UA.recognition.defs',D),A('Theorem UA.Normal (','UA.Normal',N),
A('Corollary UA.RecognizeQuotient.','UA.RecognizeQuotient',N),
A('Theorem UA.Recognition (','UA.Recognition',N),A('Proposition UA.Mix (','UA.Mix',N),
A('5 Coordinate kernels and incidence geometries','UA.geometry.defs',D),
A('Proposition UA.Geometry (','UA.Geometry',N),
A('5.1 Helly transfer','UA.Helly.defs',D),A('Theorem UA.SK.Helly (','UA.SK.Helly',N),
A('Corollary UA.SK.Geometry.','UA.SK.Geometry',N),
A('A sufficient alternative','UA.SK.Geometry.scope',P),A('6 Frattini coordinates','UA.frattini.heading',C),
A('Theorem UA.Phi (','UA.Phi',N),A('7 The canonical quotient','UA.forest.context',C),
A('Lemma UA.Lift (','UA.Lift',N),A('Lemma UA.Support (','UA.Support',N),
A('Theorem UA.Forest (','UA.Forest',S),A('Proof. IP gives irredundancy.','UA.Forest.frattini',B),
A('If they satisfy a nonzero','UA.Forest.edge_independence',B),A('Bilinearity makes','UA.Forest.coordinates',B),
A('8 Finite quotients of prescribed excess order','UA.finite.context',C),
A('Theorem UA.Nilpotent (','UA.Nilpotent',S),
A('Proof. The degree-one part','UA.Nilpotent.finiteness',B),
A('Let 𝐺 satisfy item 1.','UA.Nilpotent.bijection',B),
A('An isomorphism preserving','UA.Nilpotent.equivalence',B),
A('Theorem UA.Ladder (','UA.Ladder',N),A('Lemma UA.Order (','UA.Order',N),
A('Corollary UA.Search (','UA.Search',N),A('The last corollary is a finite classification procedure','UA.Search.algorithm',P),
A('9 Affine square groups','UA.affine.defs',D),A('Proposition UA.Affine (','UA.Affine',N),
A('The normal form also fixes','UA.affine.conventions',D),A('Proposition UA.Square (','UA.Square',N),
A('Lemma UA.SquareRecognition (','UA.SquareRecognition',S),
A('Proof. Its two adjacent dihedral','UA.SquareRecognition.orientation',B),
A('The kernel contains no nonidentity torsion.','UA.SquareRecognition.translation',B),
A('Under ℤ2 = ℤ[𝑖]','UA.SquareRecognition.lattice',B),
A('Proposition UA.SquareDecomposition (','UA.SquareDecomposition',N),
A('10 Changing the orders on selected pairs','UA.edge.heading',C),A('Theorem UA.Edge (','UA.Edge',N),
A('11 Amalgams and primary torsion','UA.amalgam.retained',R),A('Theorem UA.Amalgam (','UA.Amalgam',S),
A('Proof. The free-product universal property','UA.Amalgam.universal',B),
A('The torsion assertion for subgroups','UA.Amalgam.torsion',B),
A('If the common subgroup is proper','UA.Amalgam.infinite',B),
A('The simultaneous fiber product','UA.amalgam.scope',C),
A('12 Retained inputs, applications and attribution','UA.attribution',C),A('References','UA.references',REF)])

doc('A1',[
A(None,'A1.front',F),A('1 Markings and the source theorem','A1.defs',D),
A('We retain the regular-polytope','A1.retained',R),A('Theorem 1 (','A1.statement',S),
A('This is Theorem 1.2','A1.source_scope',C),A('2 The base and its local quotients','A1.base',P),
A('For the consecutive pair','A1.locals',P),A('3 Construction and proof','A1.construct',P),
A('For |𝑗 −ℓ| > 1','A1.string',P),A('The exact order formula','A1.order',P),
A('4 The necessary order bound','A1.bound.context',C),A('Proposition 2.','A1.bound',N),
A('For a group of order','A1.bound.consequence',P),A('5 Source coverage and retained work','A1.scope',C),
A('References','A1.references',REF)])

doc('A2',[
A(None,'A2.front',F),A('1 Marked groups and geometric scope','A2.s1',D),
A('2 Affine seeds and the source presentation','A2.seed.inputs',R),
A('For 𝛿 ≥ 0','A2.parity',P),A('Take 𝑛 ≥ 10','A2.presentation',D),
A('Theorem 1 (','A2.statement',S),A('Proof. The three pair supports','A2.locals',B),
A('All relators of 𝑃 hold','A2.recognition',B),A('Its order formula gives','A2.geometry',B),
A('The quotient description','A2.structure',P),A('3 Attribution and exact boundary','A2.scope',C),
A('References','A2.references',REF)])

doc('A3',[
A(None,'A3.front',F),A('1 Marked groups and geometric inputs','A3.defs',D),
A('We retain the regular-polytope correspondence','A3.retained.polytope',R),
A('A deletion keeps','A3.defs.FAP',D),A('Write 𝐻𝑛','A3.seeds',P),
A('2 One construction for every sequence','A3.path',P),
A('Theorem 1 (','A3.T5.1',S),A('Proof. Take the path','A3.T5.1.string',B),
A('All deletions exist.','A3.T5.1.FAP',B),A('For flatness assume','A3.T5.1.flatness',B),
A('The group is also precisely','A3.mix_identification',P),
A('3 Recognizing the complete universal presentation','A3.universal.defs',D),
A('Lemma 2.','A3.normalization',N),A('Theorem 3 (','A3.T5.3',S),
A('Proof. Let 𝐻 denote','A3.T5.3.normal',B),A('Kill all the','A3.T5.3.base',B),
A('Finally every defining relator','A3.T5.3.universal',B),A('In the smallest diagonal square group','A3.correction.square',C),
A('4 Two branches and the full alternating automorphism group','A3.assembly.retained',R),
A('Theorem 4 (','A3.T6.1',S),A('Proof. Take the tree','A3.T6.1.local',B),
A('The deletions onto','A3.T6.1.joint',B),A('The common group has order','A3.T6.1.order',B),
A('The co-','A3.assembly.scope',C),A('5 Free extensions and two-primary torsion','A3.torsion.context',D),
A('We retain three geometric identifications','A3.extension_inputs',R),A('Theorem 5 (','A3.T7',S),
A('Proof. For the regular extension','A3.T7.proof',B),
A('6 Coverage and attribution','A3.scope',C),A('References','A3.references',REF)])

doc('A4',[
A(None,'A4.front',F),A('1 The fixed path group','A4.defs',D),A('For 𝑑 ≥ 2','A4.s1',P),
A('2 The two principal source conclusions','A4.principal.heading',C),A('Theorem 1 (','A4.s2',N),
A('The proof of UA.Forest is a complete part','A4.main.scope',C),
A('3 The auxiliary kernel in the source','A4.s3',P),
A('4 Attribution and scope','A4.scope',C),A('References','A4.references',REF)])

doc('A5',[
A(None,'A5.front',F),A('1 The source results and common inputs','A5.context',C),
A('We use the marking conventions','A5.defs',D),A('The reusable results used below','A5.inputs',R),
A('2 Existence for every stated type','A5.exist',N),
A('3 Cyclic cores and the eight high-type families','A5.core.context',C),
A('The retained cyclic core theorem','A5.core.retained',R),A('Theorem H.Core (','A5.core',N),
A('Hereafter','A5.models',P),A('3.1 Completeness and bare presentation recognition','A5.collection',T),
A('Theorem H.Classification (','A5.classification.statement',S),
A('Proof, first branch.','A5.case3',B),A('Second branch.','A5.case4',B),
A('The bounded seed for the third branch.','A5.seed',T),A('Third-branch lifts.','A5.case5',B),
A('It remains to recognize','A5.bare',B),A('The preceding theorem proves','A5.classification.scope',C),
A('4 Computation, attribution and formal scope','A5.scope',C),A('References','A5.references',REF)])

doc('A6',[
A(None,'A6.front',F),A('1 Markings, scope and the main census','A6.def',D),
A('Theorem 1 (','A6.census.statement',S),A('We use the common paper','A6.inputs',R),
A('2 Central descent and complete binary lifts','A6.central.context',C),
A('The specifically retained prior results','A6.retained',R),
A('2.1 Preliminary adapters','A6.adapters',P),A('2.2 A safe central quotient','A6.central.defs',D),
A('Lemma N2 (','A6.central',N),A('Theorem N3 (','A6.descent',N),
A('This proves source Corollary 3.3','A6.descent.correction',C),
A('Theorem N4 (','A6.lifts',N),A('3 Exhaustive bounded classification','A6.census',P),
A('3.1 Every printed rank-three presentation','A6.rank3',P),
A('3.2 Universal presentations','A6.examples',P),
A('3.3 Square-lattice centers','A6.centers',P),A('For the sole infinite row','A6.exceptional.retained',R),A('Proposition N6 (','A6.exceptional',N),
A('A All marked facet pairs','A6.table6',T),A('B Proof obligations and attribution','A6.scope',C),
A('References','A6.references',REF)])
doc('code',[A(None,'code.appendix','required_computation','All four full programs and their complete appendix wrapper')])

# Documentary historical units: these boundaries describe the printed exposition,
# not an assertion that every printed argument is correct or minimally dependent.
doc('L032',[
A(None,'L032.front',F),A('1 Introduction','L032.intro',C),
A('Problem 1.1','L032.problem',Q),A('The number of pairwise','L032.intro',C),
A('Theorem 1.2 For','L032.T1.2',S),A('The paper is organized','L032.organization',C),
A('2 Background deﬁnitions','L032.defs',D),
*[A('Proposition 2.'+str(i)+' ',f'L032.P2.{i}',R if i<6 else N) for i in range(1,7)],
A('3 Proof of Theorem 1.2','L032.proof',P),A('References','L032.references',REF)])

doc('L034',[
A(None,'L034.front',F),A('1 Introduction','L034.intro',C),A('2 Background results','L034.defs',D),
A('Proposition 2.1 [','L034.P2.1',R),A('The following proposition gives','L034.square.context',C),
A('Proposition 2.2 For','L034.P2.2',R),A('In Proposition 2.2','L034.square.context',C),
A('2.2 Regular hypertopes','L034.geometry.context',C),A('Deﬁnition 2.3 An','L034.D2.3',D),
*[A('Proposition 2.'+str(i)+' ',f'L034.P2.{i}',R) for i in range(4,12)],
A('3 Main Result','L034.main.heading',C),A('Lemma 3.1 Let','L034.L3.1',N),
A('Theorem 3.2 For','L034.T3.2',S),A('Proof. Let L1','L034.proof.setup',P),
A('Claim 1 :','L034.C1',B),A('Claim 2:','L034.C2',B),A('Claim 3 :','L034.C3',B),
A('Conjecture 3.3 For','L034.Q3.3',Q),A('References','L034.references',REF)])

doc('L035',[
A(None,'L035.front',F),A('1 Introduction','L035.intro',C),A('Problem 1.1 Characterize','L035.problem',Q),
A('Conder [6] showed','L035.intro',C),A('Theorem 1.2 For','L035.T1.2',S),
A('Cunningham and Pellicer [8]','L035.classification.context',C),
A('To state the next result','L035.presentations',T),A('Theorem 1.3 For','L035.T1.3',S),
A('Let n < 10.','L035.small_cases',R),A('2 Background results','L035.defs',D),
*[A('Proposition 2.'+str(i)+' ',f'L035.P2.{i}',R) for i in range(1,7)],
A('Theorem 2.7 [','L035.T2.7',R),A('Remark 2.8 A','L035.R2.8',N),
A('Proposition 2.9 [','L035.P2.9',R),A('3 Proof of Theorem 1.2','L035.exist',P),
A('Corollary 3.1 The','L035.C3.1',N),A('4 Proof of Theorem 1.3','L035.classification.heading',C),
A('Lemma 4.1 Let','L035.L4.1',N),A('Lemma 4.2 Let','L035.L4.2',N),
A('Proof of Theorem 1.3(1):','L035.proof1',B),A('Proof of Theorem 1.3(2):','L035.proof2',B),
A('Proof of Theorem 1.3(3):','L035.proof3',B),A('References','L035.references',REF)])

doc('F013',[
A(None,'F013.front',F),A('1.Introduction','F013.intro',C),A('Theorem 1.1.','F013.main',S),
A('These two theorems prove','F013.main.context',C),A('2.Basic Notions','F013.definitions',D),
A('3.The smallest regular polytopes','F013.Conder',R),A('4.String C-group','F013.Frattini_defs',D),
A('Theorem 4.1.Let','F013.Burnside',R),A('Next we study the implications','F013.ABC',D),
A('Theorem 4.2.Let','F013.4.2_statement',S),A('Proof.The first part','F013.4.2a',B),
A('We proceed with the second part','F013.4.2b',B),
A('For the third part of the theorem','F013.4.2c',B),
A('For the fourth part of the theorem','F013.4.2d',B),
A('For the final part of the theorem','F013.4.2e',B),
A('In conclusion,','F013.questions',Q),A('Acknowledgment.','F013.acknowledgment',C),
A('References','F013.references',REF)])

doc('F016',[
A(None,'F016.front',F),A('1.Introduction','F016.intro',C),A('2.Basic Notions','F016.defs',D),
A('3.The F AP','F016.FAP.defs',D),A('Lemma 3.1.Let','F016.L3.1',N),
A('Lemma 3.2.Let','F016.L3.2',N),A('The flat amalgamation property can','F016.mix',R),A('Theorem 3.3.Let','F016.T3.3',R),
A('4.Toroidal polyhedra','F016.square.context',C),A('Lemma 4.1.The','F016.L4.1',N),
A('5.Regular polytopes','F016.regular.context',C),A('Theorem 5.1.Let','F016.T5.1',N),
A('Remark 5.2.The','F016.R5.2',N),A('Now let us determine a presentation','F016.presentation.context',C),
A('Theorem 5.3.The','F016.T5.3',N),A('6.Alternating semiregular','F016.alternating.inputs',R),
A('Theorem 6.1.Let','F016.T6.1',N),A('Remark 6.2.The','F016.R6.2',N),
A('7.Polytopes with infinite','F016.infinite.inputs1',R),A('Theorem 7.1.Let','F016.T7.1',N),
A('A similar theorem also holds','F016.infinite.inputs2',R),A('Theorem 7.2.Let','F016.T7.2',N),A('Note that Theorem 7.2 is','F016.infinite.scope',C),A('There also is an analogue','F016.infinite.inputs3',R),A('Theorem 7.3.Let','F016.T7.3',N),
A('8.Power polytopes','F016.power',P),A('Acknowledgment.','F016.acknowledgment',C),
A('References','F016.references',REF)])

doc('N009',[
A(None,'N009.front',F),A('1. Introduction','N009.intro',C),A('2. Preliminaries','N009.defs',D),
A('Deﬁnition 2.1 (','N009.D2.1',D),
*[A('Lemma 2.'+str(i)+'.',f'N009.L2.{i}',R) for i in range(2,6)],
A('Deﬁnition 2.6.','N009.D2.6',D),A('Theorem 2.7.','N009.T2.7',R),
A('Lemma 2.8. Let','N009.L2.8',N),A('3. Rank three','N009.rank3.context',C),
A('Lemma 3.1 ([','N009.L3.1',R),A('Lemma 3.2. Let','N009.L3.2',N),
A('Corollary 3.3. Let','N009.C3.3',N),A('Lemma 3.4. Let','N009.L3.4',N),
A('Lemma 3.5. Let','N009.L3.5',N),A('Theorem 3.6. Let','N009.T3.6',N),
A('Corollary 3.7. For','N009.C3.7',N),A('Suppose we want to enumerate','N009.lift.proof',P),
A('Theorem 3.8. Let','N009.T3.8',S),A('Note that a group','N009.lift.warning',C),
A('Class of Γ Type of Γ','N009.Table1',T),A('We now use the method','N009.census.context',C),
A('Example 3.9. Suppose','N009.E3.9',N),
A('Γ R1(s0,s1,s2) R2(s0,s1,s2)','N009.Table2',T),
A('Γ τ =R1','N009.Table3',T),A('Γ Class of Γ Additional','N009.Table4',T),
A('Enumeration for other types','N009.census.context',C),A('Type Count','N009.Table5',T),
A('4. Rank at least four','N009.rank4.context',C),A('Deﬁnition 4.1. Let','N009.D4.1',D),
A('Theorem 4.2 ([','N009.T4.2',R),A('It then follows from the above discussion','N009.universal.algorithm',P),A('Example 4.3.','N009.E4.3',N),
A('Example 4.4.','N009.E4.4',N),A('Example 4.5.','N009.E4.5',N),
A('We summarize the results for each type','N009.table6.context',C),
A('Type Γ′ Γ′′','N009.Table6',T),A('5. ClassC(','N009.exceptional.context',C),
A('Lemma 5.1 ([','N009.L5.1',R),A('Lemma 5.2. Let','N009.L5.2',N),
A('Theorem 5.3 ([','N009.T5.3',R),A('It follows from above','N009.L5.4.proof',P),A('Lemma 5.4. Let','N009.L5.4',S),A('It follows immediately from Lemma 5.4','N009.exceptional.proof',P),
A('Theorem 5.5. There','N009.T5.5',S),A('6. Concluding','N009.conclusion',C),
A('References','N009.references',REF)])

from accounting import (FORMS,METRICS,atomic,total,add_weights,page_locations,
                        build_weights,validate_links)

# Statements of a theorem with branch children are separate charged leaves.
# The displayed theorem is a set-valued rollup, never a second cost item.
children=collections.defaultdict(set)
for n in graph['nodes']:
    if n.get('parent'):children[n['parent']].add(n['id'])
children['UA.SquareRecognition'].add('UA.SquareRecognition.orientation')
children['UA.Amalgam'].add('UA.Amalgam.universal')
children['A3.T6.1'].update(['A3.T6.1.local','A3.T6.1.order'])
children['A3.T7'].add('A3.T7.proof')
rename={n:n+'.own_text' for n in children if n in owners}
for n,new in rename.items():
    owners[new]=owners.pop(n);owners[new]['id']=new
    owners[new]['logical_statement_owner']=n
for spans in parts.values():
    for s in spans:s['node']=rename.get(s['node'],s['node'])

docs={}
for k,text in texts.items():
    positions=page_locations(extracted[k][0],spec[k],parts[k])
    need(len(positions)==len(text),'raw-to-selected coordinate map '+k)
    need(''.join('\n' if i is None else extracted[k][0][i] for i in positions)==extracted[k][1],
         'raw-to-selected text identity '+k)
    docs[k]={'title':graph['document_titles'].get(k,'Complete four-program computational appendix'),'pdf':spec[k]['path'],'pdf_sha256':spec[k]['pdf_sha256'],'pages':spec[k]['pages'],
             'selected_calibrated_codepoints':len(text),'selected_calibrated_sha256':sha(text.encode()),
             'span_count':len(parts[k]),'spans':parts[k]}
weights,totals=build_weights(texts,spec,parts,owners)
root_totals=read('topic_A_measurement_root_review/recount.json')['documents']
root_a6=read('topic_A_A6_final_recount_root/recount.json')
# Older root input audit remains immutable; A6 is independently recounted below.
for k in texts:
    for form in FORMS:
        expected=(root_a6['document'] if k=='A6' else root_totals[k])['metrics'][form]['calibrated_selected']
        need(totals[k][form]=={m:expected[m] for m in METRICS},'accepted root recount '+k+form)

node_index={n['id']:n for n in graph['nodes']}
for id,owner in owners.items():
    logical=owner.get('logical_statement_owner',id)
    if logical in node_index:owner['label']=node_index[logical]['label']
extra={
 'A1.main':['A1.statement'],'A1.bound':['A1.bound.consequence'],
 'A2.s2':['A2.seed.inputs','A2.presentation','A2.statement'],
 'A2.main':['A2.seed.inputs','A2.presentation','A2.statement'],
 'A2.recognition':['A2.presentation'],
 'L034.T3.2':['L034.proof.setup'],
 'N009.Table6':['N009.universal.algorithm'],
 'A3.T5.3':['A3.universal.defs'],
 'A3.T6.1':['A3.assembly.retained'],
 'A5.core':['A5.core.retained'],
 'A5.main':['A5.classification.statement'],
 'A6.main':['A6.census.statement'],
 'A6.central':['A6.central.defs'],
 'A6.exceptional':['A6.exceptional.retained'],
 'L035.T1.3':['L035.presentations'],
 'F016.T3.3':['F016.mix'],
 'F016.T7.1':['F016.infinite.inputs1'],
 'F016.T7.2':['F016.infinite.inputs2'],
 'F016.T7.3':['F016.infinite.inputs3'],
 'N009.T3.8':['N009.lift.proof'],
 'N009.L5.4':['N009.L5.4.proof'],
 'N009.T5.5':['N009.exceptional.proof']}
def paid(n,seen=None):
    seen=set() if seen is None else seen
    need(n not in seen,'rollup cycle '+n);seen=seen|{n}
    out={rename.get(n,n)}&set(owners)
    out.update(extra.get(n,[]))
    for child in children[n]:out.update(paid(child,seen))
    if n.startswith('code.'):out={'code.appendix'}
    need(out<=set(owners),'unknown mapped owner '+n)
    return out
links={}
for n in graph['nodes']:
    id=n['id'];ids=sorted(paid(id));external=n['category']=='external'
    links[id]={'owners':ids,'weight':None if external or not ids else add_weights([weights[i] for i in ids]),
      'full_dependency_cost':None,'charged_as_an_additional_item':False,
      'scope':('Unknown external proof cost.' if external else
               'Shared full appendix representation; union owner IDs before summing.' if id.startswith('code.') else
               'Inclusive text ownership rollup; branch and parent costs must never be added.' if children[id] else
               'Direct printed text, including the stated hypotheses and proof where present.' if ids else
               'Logical output alias; its cost is obtained from the documented dependency closure.')}
validate_links(graph,owners,links)

# The original mathematical edge set is preserved. Cost links above add no
# theorem implication. Local context is not silently counted as free: the full
# document totals and exact context ledger accompany every closure subtotal.
incoming=collections.defaultdict(set)
logical_kinds={'proof_use','retained_input_use','retained_algorithm_use','computational_use',
 'branch_membership','output_assembly','historical_documented_use','historical_asserted_use',
 'definition_use','declared_retained_translation'}
for e in graph['edges']:
    if e['kind'] in logical_kinds:incoming[e['target']].add(e['source'])
def closure(starts):
    found=set(starts);todo=list(starts)
    while todo:
        for n in incoming[todo.pop()]-found:found.add(n);todo.append(n)
    return found
def closure_row(starts):
    logical=closure(starts);ids=sorted(set().union(*(set(links[n]['owners']) for n in logical)))
    unknown=sorted(n for n in logical if node_index[n]['category']=='external')
    used=sorted({owners[i]['document'] for i in ids})
    omitted=sorted(i for i,x in owners.items() if x['document'] in used and i not in ids)
    return {'starting_nodes':sorted(starts),'logical_nodes':sorted(logical),'unique_owner_ids':ids,
      'known_owned_text_subtotal':add_weights([weights[i] for i in ids]),
      'unknown_external_nodes':unknown,'complete_dependency_cost':None,
      'documentary_qualifications':[{ 'node':n,'qualification':node_index[n]['documentary_validity']} for n in sorted(logical) if node_index[n].get('documentary_validity')],
      'other_document_text_not_in_this_graph_closure':omitted,
      'scope':'Documentary proof-unit closure, not an independently proved minimal or complete dependency cost. '
              'Every omitted text owner remains paid in the full-document totals. No scalar proof-compression factor.'}
closures={n['id']:closure_row([n['id']]) for n in graph['nodes'] if n['category']!='external'}
coverage=read('topic_A_logical_dag/coverage.json')
contract_closures={row['id']:closure_row(row['new_nodes']) for row in coverage['rows']}
category_totals={}
for k in docs:
    cats=sorted({x['category'] for x in owners.values() if x['document']==k})
    category_totals[k]={c:add_weights([weights[i] for i,x in owners.items() if x['document']==k and x['category']==c]) for c in cats}

partition={'schema':'topic_A_exclusive_calibrated_text_partition_v1',
 'status':'AUTHOR_FROZEN_PENDING_INDEPENDENT_OWNERSHIP_REVIEW','documents':docs,'owners':owners,
 'convention':'Every selected calibrated codepoint has exactly one owner. Named units contain their printed '
              'statement and proof, with immediately attached connective prose unless separated explicitly. '
              'Tables begin at their data headers, not only at captions. An owner may have disjoint spans. '
              'Section context, introductions, references, retained statements and complete program wrapper text remain charged.',
 'coordinate':'Half-open Unicode-codepoint intervals in calibrated selected pypdf text; exact raw positions and physical pages supplied.',
 'primary_text_redistributed':False}
result={'schema':'topic_A_weighted_ownership_v1','status':'AUTHOR_FROZEN_PENDING_INDEPENDENT_OWNERSHIP_REVIEW',
 'normalizations':list(FORMS),'metrics':list(METRICS),'metric_allocation':
 'Normalize the full document and each span, require concatenation equality, then assign each token, '
 'alphanumeric run and collapsed whitespace run to the owner of its first codepoint. Each nonspace '
 'codepoint and its UTF-8 bytes belong to its unique span. These are additive global allocations, not '
 'independently trimmed substring lengths.',
 'document_totals':totals,'owner_weights':weights,'category_totals':category_totals,
 'logical_node_cost_interfaces':links,'logical_closures':closures,'contract_closures':contract_closures,
 'program_representation':{'charged':'code.appendix','required_raw_files':rs['required_programs'],
   'raw_file_metrics_are_alternative_not_additional':True,'shared_across_A5_A6_charged_once':True},
 'unknown_costs':{'retained_external_proofs':None,'unextracted_scientific_raster_labels':None,
   'diagram_structure':None,'note':'Extracted text coordinates do not assign zero to omitted nontext mathematics. '
   'L035 pages 9,10,12,22 include scientific raster labels, and page 22 has clipping; this limitation is retained.'},
 'whole_document_total_is_authoritative':True,
 'granularity_counts':{'logical_nodes_by_category':dict(collections.Counter(n['category'] for n in graph['nodes'])),
  'ownership_leaves_by_category':dict(collections.Counter(n['category'] for n in owners.values())),
  'count_comparison':'Different granularities; neither number is a count of comparable proofs or a compression ratio.'},'raw_node_count_ratio':None,'proof_count_ratio':None,
 'new_source_credit':0,'new_question_credit':0,'self_admission':False}

for row in rs['required_programs']:
    b=(ROOT/row['path']).read_bytes()
    need(sha(b)==row['sha256'] and len(b)==row['bytes'],'full program binding')
    need(re.sub(r'\s+','',b.decode()) in re.sub(r'\s+','',texts['code']),'full code inclusion')
inputs=['topic_A_logical_dag/manifest.json','topic_A_logical_dag/logical_graph.json',
 'topic_A_logical_dag/coverage.json','topic_A_weighted_dag/manifest.json','topic_A_logical_dag_v3/manifest.json',LOGICAL_GRAPH,
 'topic_A_numerical_audit/manifest.json',
 'topic_A_logical_independent_review/manifest.json','topic_A_logical_independent_review/review.json',
 'topic_A_measurement/source_input_spec.json',REPLACEMENT_SPEC,
 'topic_A_measurement/extract_inputs.py','topic_A_measurement_root_review/manifest.json',
 'topic_A_measurement_root_review/recount.json','topic_A_A6_final_recount_root/manifest.json',
 'topic_A_A6_final_recount_root/recount.json','topic_A_volume_A6_attribution/manifest.json']
bindings={'status':'AUTHOR_FROZEN_PENDING_INDEPENDENT_OWNERSHIP_REVIEW','inputs':[bind(p) for p in inputs],
 'pdf_inputs':[bind(v['path']) for v in spec.values()],
 'logical_packet_preserved':True,'A6_overlay':{'attribution_only':True,'mathematical_graph_unchanged':True,
 'prior_pdf_sha256':'4c38f7abf8b5e41148b3937b4e6f3f499e09313d247153327e750c51f83d4e8f',
 'current_pdf_sha256':spec['A6']['pdf_sha256']},
 'public_proof_edition_commit':'6641c356b39ea9ca650542a41869b7811fdfc0ff','ratio':None}
for name,value in [('partition.json',partition),('weights.json',result),('input_bindings.json',bindings)]:
    (HERE/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
with (HERE/'owner_costs.csv').open('w',newline='') as file:
    fields=['owner','document','category','label','physical_pages']+[f+'_'+m for f in FORMS for m in METRICS]
    writer=csv.DictWriter(file,fieldnames=fields);writer.writeheader()
    for id,owner in sorted(owners.items()):
        pages=sorted(set().union(*(set(s['physical_pages']) for s in parts[owner['document']] if s['node']==id)))
        row={'owner':id,'document':owner['document'],'category':owner['category'],'label':owner['label'],
             'physical_pages':','.join(map(str,pages))}
        row.update({f+'_'+m:weights[id][f][m] for f in FORMS for m in METRICS});writer.writerow(row)
print(json.dumps({'documents':len(docs),'spans':sum(len(x) for x in parts.values()),'owners':len(owners),
                  'logical_nodes':len(links),'metric_cells':len(docs)*10,
                  'A6_NFC_nonspace':totals['A6']['NFC']['characters_without_whitespace'],
                  'status':'AUTHOR_FROZEN_PENDING_INDEPENDENT_OWNERSHIP_REVIEW'}))

