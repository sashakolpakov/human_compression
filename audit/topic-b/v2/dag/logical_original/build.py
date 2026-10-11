#!/usr/bin/env python3
"""Build the unweighted, paired Topic B proof graph from bound editions.

Only span hashes and locators are exported. Primary text stays at --sources-root.
Node/edge choices are mathematical authorship and require independent review.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

COMMIT = '769322e67042671b404917b7a6249e1a5de4ef18'
PINS = {
 'papers/topic-b/v2/manifest.json':'9029bb003c3b419bb9aa3b2edeefca473b2143b25cc6b30dab0c9dfd663e02c0',
 'papers/topic-b/v2/mapping_correction/manifest.json':'2f958b2991b71c983efa09984629045f4c1b748b1eddd29b8555b4b868f15750',
 'audit/topic-b/v2/independent_review/manifest.json':'d224742e25167983954dc1421cbb4a09853aad47feb5ef9b84378249e6d1e6c5'}
SOURCE = {
 'N001': ('sources/phase16_N001_browser_record.txt',None),
 'N003': ('sources/phase10_N003_extracted.txt','sources/network_independent_generators.pdf'),
 'N008': ('sources/phase16_frattini_geometries.txt','sources/phase16_frattini_geometries.pdf'),
 'L030': ('sources/kneser_revised.txt','sources/kneser_revised.pdf')}
TEX = {'U1':'umbrella-sections/01-cosets.tex','U2':'umbrella-sections/02-relative.tex',
       'U3':'umbrella-sections/03-forest.tex','U4':'umbrella-sections/04-overgroups.tex',
       'B1':'inductively-minimal-geometries.tex','B2':'maximal-symmetric-markings.tex',
       'B3':'frattini-coordinate-geometries.tex','B4':'disjoint-subset-geometries.tex'}
LOGICAL = ['proof_use','definition_use','hypothesis_use','proof_assembly','retained_input_use']


def need(ok,msg):
 if not ok: raise ValueError(msg)


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--sources-root',required=True,type=Path)
 ap.add_argument('--public-root',required=True,type=Path);ap.add_argument('--out',required=True,type=Path)
 a=ap.parse_args();need(not a.out.exists() and not a.out.is_symlink(),'fresh output directory')
 roots={'research':a.sources_root.resolve(),'public':a.public_root.resolve()};inputs={};nodes={};edges=[]
 def sha(b):return hashlib.sha256(b).hexdigest()
 def binding(space,path):
  p=roots[space]/path;b=p.read_bytes();r=dict(namespace=space,path=path,bytes=len(b),sha256=sha(b));inputs[(space,path)]=r;return r
 def read(space,path):binding(space,path);return (roots[space]/path).read_text()
 def loc(space,path,first,last,label=None):
  text=read(space,path);lines=text.splitlines(keepends=True)
  need(1<=first<=last<=len(lines),f'line range {path}:{first}-{last}')
  start=sum(map(len,lines[:first-1]));end=sum(map(len,lines[:last]));span=text[start:end]
  out=dict(namespace=space,path=path,first_line=first,last_line=last,start_codepoint=start,
           end_codepoint_exclusive=end,sha256_utf8=sha(span.encode()),scope=label or 'exact proof or statement locator; not a disjoint cost span')
  if space=='research':
   pre=''.join(lines[:first]);suffix=''.join(lines[:last]);pages=[]
   for data in [pre,suffix]:
    hits=list(re.finditer(r'(?:--- PDF PAGE |\[\[PDF PAGE |^PAGE )(\d+)',data,re.M))
    pages.append(int(hits[-1].group(1)) if hits else 1)
   out['physical_pdf_pages']=list(range(pages[0],pages[1]+1))
  return out
 def sl(doc,first,last):
  path=SOURCE[doc][0]
  if doc!='N001':return loc('research',path,first,last)
  text=read('research',path);lines=text.splitlines(keepends=True)
  indices={int(m.group(1)):i+1 for i,line in enumerate(lines) if (m:=re.match(r'L(\d+):',line))}
  r=loc('research',path,indices[first],indices[last],'authored browser display lines; not PDF-extracted text')
  r.pop('physical_pdf_pages',None);r['browser_display_lines']=[first,last];r['original_pdf_available']=False;return r
 def nl(doc,first,last):return loc('public','papers/topic-b/v2/'+TEX[doc],first,last)
 def add(id,doc,side,label,category,locations=(),parent=None,flags=(),scope=None):
  need(id not in nodes,'duplicate node '+id)
  r=dict(id=id,document=doc,side=side,label=label,category=category,locators=list(locations),
         cost=None,cost_status='unknown retained cost' if side=='external' else 'unweighted; exclusive calibrated partition not assigned',
         documentary_flags=list(flags))
  if parent:r['parent']=parent
  if scope:r['scope']=scope
  nodes[id]=r;return id
 def edge(src,dst,why,kind='proof_use',where=None):
  need(src in nodes and dst in nodes,'unknown endpoint '+src+' -> '+dst)
  need(not any(e['source']==src and e['target']==dst and e['kind']==kind for e in edges),'duplicate edge')
  edges.append(dict(source=src,target=dst,kind=kind,evidence=why,
                    target_evidence=where or nodes[dst]['locators'],necessity_claim=False))
 def deps(dst,srcs,why='Used in the displayed proof.',kind='proof_use'):
  for s in srcs:edge(s,dst,why,kind)
 def h(doc,id,label,first,last,cat='named_result',parent=None,flags=()):
  return add('h.'+doc+'.'+id,doc,'historical',label,cat,[sl(doc,first,last)],parent,flags)
 def n(doc,id,label,first,last,cat='proof_branch',parent=None):
  return add(id,'U_B' if doc.startswith('U') else doc,'new',label,cat,[nl(doc,first,last)],parent)

 for path,expected in PINS.items():need(binding('public',path)['sha256']==expected,'frozen pin '+path)
 contract=json.loads(read('public','papers/topic-b/v2/mapping_correction/source_contract_map.json'))
 author_map=json.loads(read('public','papers/topic-b/v2/proof_map.json'))
 previous=json.loads(read('research','phase141_module_B_review.json'))
 old={r['adapter']:r for r in previous['source_contracts']}
 for r in contract['rows']:need(all(r[k]==v for k,v in old[r['adapter']].items()),'old clause '+r['adapter'])
 for row in json.loads(read('public','papers/topic-b/v2/manifest.json'))['exports']:
  b=binding('public','papers/topic-b/v2/'+row['path']);need(b['sha256']==row['sha256'],'bound public proof')
 source_bindings={}
 for doc,(txt,pdf) in SOURCE.items():
  source_bindings[doc]={'documentary_text':binding('research',txt),'primary_pdf':binding('research',pdf) if pdf else None,
                        'pdf_cost':None,'representation':'authored browser rendering' if doc=='N001' else 'exact bound primary PDF and pre-existing extraction'}

 # Classical statements are separately named; unknown outside costs are not zero.
 external=[
 ('B97','Inductively minimal-pair classification and uniqueness',[sl('N001',193,194),nl('B1',17,17)]),
 ('DirectSum','Direct-sum theorem for disconnected diagram residues',[sl('N001',203,207)]),
 ('SymmetricMaximal','Maximal overgroups of two-block symmetric subgroups, as cited to Liebeck–Praeger–Saxl',[sl('N001',209,210)]),
 ('Ends','A finite connected graph has an end',[sl('N001',191,191)]),
 ('W1','Whiston independent-family bound and extremal-generation implication',[sl('N003',81,83),nl('B2',13,13)]),
 ('W2','Whiston omission-subgroup trichotomy for n >= 7',[sl('N003',109,124),nl('B2',15,15)]),
 ('CFSG','Classification input retained through the Whiston argument',[sl('N003',237,241),nl('B2',15,16)]),
 ('Cayley','Cayley labelled-tree count',[sl('N003',164,189),nl('B2',16,16)]),
 ('AutSn','All automorphisms of S_n are inner for n >= 7',[nl('B2',16,16),nl('B2',75,75)]),
 ('CosetRecognition','Classical coset-geometry recognition and residue coordinates',[sl('N003',243,266),sl('N008',60,94)]),
 ('PrimitiveStabilizer','A transitive coset action is primitive iff its stabilizer is maximal',[sl('N008',89,94),nl('U1',68,82)]),
 ('BH','Buekenhout–Hermand/Tits product-intersection flag criterion',[sl('N003',267,281)]),
 ('SubgroupCorrespondence','Quotient subgroup correspondence and maximal intervals',[sl('N008',156,159),nl('B3',18,18)]),
 ('HistoricalQuotient','Previously published normal-Borel coset quotient proposition',[sl('N008',194,198)]),
 ('HistoricalProduct','Previously cited rank-two coset-product criterion',[sl('N008',208,221)]),
 ('FinitePFrattini','Finite p-group Frattini quotient is elementary abelian',[sl('N008',222,224),nl('B3',73,73)]),
 ('Zorn','Zorn lemma',[nl('B3',20,22)]),
 ('LinearAlgebra','Elementary dimension, basis and quotient linear algebra',[sl('N008',225,228),sl('N008',249,254),nl('B3',73,82)]),
 ('RealSpectral','Real symmetric spectral theorem and orthogonal eigenbases',[nl('B4',85,102)])]
 for name,label,locations in external:add('ext.'+name,None,'external',label,'retained_input',locations)
 edge('ext.CFSG','ext.W2','Both source and new statement retain this dependence.','retained_input_use')

 # N001: browser documentary units, retaining the theorem's four distinct clauses.
 for row in [
 ('Definitions','Finite diagram, action and primitivity definitions',182,193,'definition'),
 ('L1','Lemma 1 and following classification/uniqueness recall',193,194,'retained_statement'),
 ('L2','At most two components after deleting a diagram vertex',196,198,'named_result'),
 ('T1','Four-part property theorem (statement)',198,199,'named_result'),
 ('L3','Panel two-transitivity',200,200,'named_result'),
 ('L4','Rank-two geometric intersection property',200,202,'named_result'),
 ('Residues','Disconnected residues and their component groups',203,205,'proof_setup'),
 ('L5','Direct product of residue component groups',205,208,'named_result'),
 ('C1','Quasi-primitivity and the middle criterion',208,210,'named_result'),
 ('C2','Even rank implies primitivity',210,210,'named_result'),
 ('L6','Residual weak primitivity',211,214,'named_result'),
 ('L7','Residual primitivity iff complete diagram',214,216,'named_result')]:h('N001',*row)
 for suffix,label in [('a','RWPRI, panel two-transitivity and geometric IP'),('b','Even-rank primitivity'),('c','Quasi-primitivity and middle criterion'),('d','Residual primitivity and complete diagram')]:
  h('N001','T1.'+suffix,label,198,199,'result_clause','h.N001.T1')
 deps('h.N001.L1',['ext.B97'],'The source explicitly recalls the earlier classification and uniqueness.','retained_input_use')
 deps('h.N001.L2',['h.N001.L1'],'Uses the one-or-two maximal-clique condition at a vertex.')
 for target in ['L3','L4']:deps('h.N001.'+target,['h.N001.Definitions','h.N001.L1'],'Uses the residue definition and thin/classified connected residues.')
 deps('h.N001.Residues',['h.N001.Definitions','ext.DirectSum','h.N001.L1'],'The source invokes the direct-sum theorem and identifies connected truncations.')
 deps('h.N001.L5',['h.N001.Residues','ext.DirectSum'],'Induction on diagram components; source proof uses the cited direct-sum interpretation.')
 deps('h.N001.C1',['h.N001.L1','h.N001.L2','h.N001.L5','ext.SymmetricMaximal'],'Uses end stabilizers, the two component sizes, and the cited symmetric subgroup classification.')
 deps('h.N001.C2',['h.N001.C1'],'Two equal component sizes are impossible when the rank is even.')
 deps('h.N001.L6',['h.N001.L1','h.N001.L5','ext.Ends','ext.SymmetricMaximal'],'Choose an end in a component and a maximal point stabilizer, then multiply by the other factors.')
 deps('h.N001.L7',['h.N001.C1','h.N001.L1'],'Complete diagrams give point stabilizers; a shortest noncomplete path gives an odd-rank nonprimitive residue.')
 for suff,srcs in {'a':['L3','L4','L6'],'b':['C2'],'c':['C1'],'d':['L7']}.items():
  deps('h.N001.T1.'+suff,['h.N001.'+x for x in srcs],'The final source paragraph assembles precisely these clauses.')
  edge('h.N001.T1.'+suff,'h.N001.T1','Four clauses form the theorem.','proof_assembly')
 nodes['h.N001.C1']['documentary_flags']=['The ambiguous phrase this is the case is resolved by the accepted contract as failure of PRI, not QPRI alone.']

 # N003: printed named results and the substantive branches of the two long proofs.
 for row in [
 ('Definitions','Independent and relatively independent families',29,47,'definition'),
 ('T1.1','Normal-quotient bounds',50,74,'named_result'),
 ('W1Recall','Whiston bound as printed',81,86,'retained_statement'),
 ('T2.1','Two extremal tree-marking families',87,163,'named_result'),
 ('T2.1.converse','Both tree families generate irredundantly',100,107,'proof_branch'),
 ('T2.1.blocks','Excluding two-point imprimitivity blocks',109,128,'proof_branch'),
 ('T2.1.tree','Constructing the omission-orbit tree',129,140,'proof_branch'),
 ('T2.1.types','Local supports give ordinary or twisted transpositions',141,163,'proof_branch'),
 ('C2.2','Three distinct counting conventions',164,189,'named_result'),
 ('C2.3','Strong independence',190,211,'named_result'),
 ('C2.4','Maximal relative rank forces trivial Borel',215,228,'named_result'),
 ('Coset','G1–G4, residues and the BH criterion',243,289,'definition'),
 ('T3.1','Rank bounds and residual generation',290,308,'named_result'),
 ('T3.2','Geometry–marking bijection',310,361,'named_result'),
 ('T3.2.unique','Recovering generators up to conjugation and inversion',313,320,'proof_branch'),
 ('T3.2.ordinary','Ordinary trees satisfy BH and residual maximality',322,347,'proof_branch'),
 ('T3.2.sign','Parity markings satisfy BH and residual maximality',348,361,'proof_branch'),
 ('C3.3','Maximum-rank coset geometries are RWPRI',362,364,'named_result')]:
  parent='h.N003.T2.1' if row[0].startswith('T2.1.') else 'h.N003.T3.2' if row[0].startswith('T3.2.') else None
  h('N003',*row,parent=parent)
 nodes['h.N003.W1Recall']['documentary_flags']=['The printed iff includes an incorrect converse. Only the bound and maximum-size-implies-generation direction are retained.']
 deps('h.N003.T1.1',['h.N003.Definitions'],'The proof removes quotient words and, in the abelian case, uses conjugation-module independence.','definition_use')
 deps('h.N003.W1Recall',['ext.W1'],'Authoritative retained input is the qualified implication, not the false printed converse.','retained_input_use')
 deps('h.N003.T2.1.converse',['h.N003.Definitions'],'Edge deletion and the parity homomorphism witness irredundancy.','definition_use')
 deps('h.N003.T2.1.blocks',['h.N003.T1.1','ext.W1','ext.W2'],'Omission trichotomy plus the normal-kernel bounds excludes the imprimitive option.')
 deps('h.N003.T2.1.tree',['h.N003.T2.1.blocks'],'All but possibly one omission group is intransitive; crossing edges cannot form a cycle.')
 deps('h.N003.T2.1.types',['h.N003.T2.1.tree'],'The unique tree paths restrict local supports and force the distinguished transposition.')
 for part in ['converse','blocks','tree','types']:edge('h.N003.T2.1.'+part,'h.N003.T2.1','The complete forward and converse branches establish the classification.','proof_assembly')
 deps('h.N003.C2.2',['h.N003.T2.1','ext.Cayley'],'Uses ordinary/distinguished trees and contracted trees modulo inversion.')
 deps('h.N003.C2.3',['h.N003.T2.1'],'The proof computes forest component stabilizers and their even subgroups.')
 deps('h.N003.C2.4',['ext.W1','h.N003.T2.1','h.N003.C2.3'],'Classified omissions and a pendant point stabilizer force B into every omission; their intersection is trivial.')
 edge('ext.SymmetricMaximal','h.N003.C2.4','The proof uses the two-block maximality fact for its tree-cut Young subgroups. This fact is used inline here; the earlier classification citation is not repeated.','retained_input_use')
 deps('h.N003.Coset',['ext.CosetRecognition','ext.BH'],'The source cites the coset equivalence and the product-intersection reformulation.','retained_input_use')
 edge('ext.PrimitiveStabilizer','h.N003.Coset','Condition G4 identifies primitive coset actions with maximal stabilizers.','retained_input_use')
 deps('h.N003.T3.1',['h.N003.Coset','h.N003.Definitions'],'Panel choices are independent; maximal successive intersections give generation by induction.')
 deps('h.N003.T3.2.unique',['h.N003.T3.1','h.N003.C2.4','h.N003.T2.1'],'Classifies the chosen panel elements and their allowed inversions.')
 deps('h.N003.T3.2.ordinary',['h.N003.C2.3','h.N003.Coset'],'Uses common forest components for BH and a pendant edge for maximality.')
 deps('h.N003.T3.2.sign',['h.N003.T3.2.ordinary','h.N003.C2.3'],'Even subgroups and an odd common element adapt the BH and maximality arguments.')
 for part in ['unique','ordinary','sign']:edge('h.N003.T3.2.'+part,'h.N003.T3.2','Existence and uniqueness branches establish the source correspondence.','proof_assembly')
 deps('h.N003.C3.3',['h.N003.T3.1','h.N003.C2.4','ext.W1','h.N003.T3.2'],'These four dependencies are named in the printed proof.')
 nodes['h.N003.C3.3']['documentary_flags']=['Printed as an immediate consequence; the new B2.MaxRank supplies an explicit arbitrary-parabolic argument. This graph records the printed use, not a minimal sufficient proof.']

 # N008: preserve the unrestricted printed assertion as a flagged source node.
 for row in [
 ('Definitions','Coset, relative generation and Frattini definitions',60,109,'definition'),
 ('Nongeneration','Printed setwise nongeneration assertion',104,109,'unnumbered_assertion'),
 ('T2.1','Relative generating-set quotient equivalence',110,131,'named_result'),
 ('RelativeRecall','Recall of the Cameron–Cara generation theorem',132,144,'retained_statement'),
 ('T3.1','Frattini containment in every type stabilizer',154,190,'named_result'),
 ('T3.1.ladder','Maximal-intersection chain and first failure',166,182,'proof_branch'),
 ('T3.1.propagation','Upward propagation using distinct intersections',183,190,'proof_branch'),
 ('P3.2','Normal-Borel quotient preserves the pregeometry',194,198,'retained_statement'),
 ('C3.3','Quotient by the Frattini subgroup',199,201,'named_result'),
 ('T3.4','Frattini-free realization',202,205,'named_result'),
 ('DirectSum','Direct sums and their residues',207,220,'definition'),
 ('P3.5','Rank-two direct sum iff the subgroup product is all G',221,221,'retained_statement'),
 ('L3.6','Maximal-subspace dimension lemma',223,228,'named_result'),
 ('P3.7','Finite p-group RWPRI iff RPRI',229,246,'named_result'),
 ('T3.8','Finite p-group direct-sum classification',247,254,'named_result'),
 ('Test4.2','Necessary residue Frattini test',280,295,'unnumbered_result'),
 ('Core4.3','Faithful core quotient',300,305,'unnumbered_result')]:
  h('N008',*row,parent='h.N008.T3.1' if row[0].startswith('T3.1.') else None)
 for id in ['Nongeneration','T2.1']:nodes['h.N008.'+id]['documentary_flags']=['Unrestricted infinite setwise nongeneration is false; the preserved contract includes the stated correction and counterexample.']
 nodes['h.N008.Definitions']['locators']=[sl('N008',60,103),sl('N008',105,107)]
 nodes['h.N008.T3.1.ladder']['documentary_flags']=['The printed argument uses setwise nongeneration for an infinite group. B3.Ladder proves the required relative finite-generation condition before this step; the geometric conclusion is preserved.']
 nodes['h.N008.L3.6']['documentary_flags']=['The source calls the dimension proof an easy exercise; B3 supplies the calculation.']
 edge('ext.PrimitiveStabilizer','h.N008.Definitions','Section 1.3 explicitly translates primitive action into maximality.','retained_input_use')
 deps('h.N008.Nongeneration',['h.N008.Definitions'],'This is the literal assertion made after the definitions.','definition_use')
 deps('h.N008.T2.1',['h.N008.Nongeneration'],'The converse and deletion tests use the flagged setwise nongeneration assertion.')
 deps('h.N008.RelativeRecall',['h.N003.T3.1'],'The source explicitly recalls Cameron–Cara, citation [4], in section 2.3.','retained_input_use')
 deps('h.N008.T3.1.ladder',['h.N008.Definitions','h.N008.Nongeneration'],'Residual maximality supplies a finite chain; the terminal contradiction invokes the flagged assertion.')
 deps('h.N008.T3.1.propagation',['h.N008.Definitions'],'Normality, maximality and distinct indexed intersections prove the upward step.','definition_use')
 deps('h.N008.T3.1',['h.N008.T3.1.ladder','h.N008.T3.1.propagation'],'Both branches prove the containment theorem.','proof_assembly')
 deps('h.N008.P3.2',['ext.HistoricalQuotient'],'Explicit earlier proposition [2], with its original proof retained.','retained_input_use')
 deps('h.N008.C3.3',['h.N008.T3.1','h.N008.P3.2'],'Apply the normal-Borel quotient to Phi(G).')
 deps('h.N008.T3.4',['h.N008.C3.3','ext.SubgroupCorrespondence'],'The quotient is Frattini free by the maximal-subgroup correspondence.')
 deps('h.N008.P3.5',['h.N008.DirectSum','ext.HistoricalProduct'],'The source cites [1] for the well-known product criterion.','retained_input_use')
 deps('h.N008.L3.6',['ext.LinearAlgebra'],'Source explicitly leaves the finite-vector-space dimension exercise.','retained_input_use')
 deps('h.N008.P3.7',['h.N008.T3.1','h.N008.P3.2','ext.FinitePFrattini','h.N008.L3.6'],'Reduce to an elementary abelian quotient and propagate maximality by the dimension lemma.')
 deps('h.N008.T3.8',['h.N008.T3.1','h.N008.P3.7','ext.FinitePFrattini','ext.LinearAlgebra','h.N008.P3.5'],'Every type subgroup is a hyperplane; dimension gives complete cross-incidence.')
 deps('h.N008.Test4.2',['h.N008.T3.1','h.N008.Definitions'],'Apply containment to each actual residue; no sufficiency assertion.')
 deps('h.N008.Core4.3',['h.N008.T3.1','h.N008.P3.2'],'The largest normal subgroup of the Borel contains Phi(G) and can be removed.')

 # L030: the revised institutional edition, not a silently substituted journal text.
 for row in [
 ('Construction1.1','Disjoint-subset incidence system',36,45,'definition'),
 ('Definitions','Graph, incidence and diagram conventions',88,241,'definition'),
 ('T1.2','Main geometry, automorphism and parameter theorem',47,61,'named_result'),
 ('C1.3','Locally Kneser link graphs',72,73,'named_result'),
 ('C1.4','Transitivity on maximal cliques',78,79,'named_result'),
 ('L2.1','Odd-cycle length bound',102,117,'named_result'),
 ('L2.2','Even and odd paths',118,137,'named_result'),
 ('L3.1','Bipartite diameter',242,256,'named_result'),
 ('L3.2','Rank-two gonality',257,263,'named_result'),
 ('L3.3','Connectedness of the bipartite double',264,266,'named_result'),
 ('L4.1','Every maximal flag is a chamber',271,274,'named_result'),
 ('L4.2','Symmetric-group flag transitivity',275,277,'named_result'),
 ('L4.3','Residual connectedness by induction',278,288,'named_result'),
 ('L4.4','Panel count and printed order',289,301,'named_result'),
 ('C4.5','Printed thickness conclusion',304,305,'named_result'),
 ('L4.6','All rank-two residues',306,309,'named_result'),
 ('L4.7','Typed automorphism groups',310,314,'named_result'),
 ('C4.8','Geometric rank-two intersection criterion',323,328,'named_result'),
 ('C5.1','The displayed locally Desargues example',349,351,'named_result')]:h('L030',*row)
 nodes['h.L030.Definitions']['locators']=[sl('L030',88,101),sl('L030',138,241)]
 for suff,label in [('existence','Existence and residual properties'),('groups','Automorphism assertions'),('parameters','Diagram and numerical parameters')]:h('L030','T1.2.'+suff,label,47,61,'result_clause','h.L030.T1.2')
 nodes['h.L030.C1.3']['locators'].append(sl('L030',346,348))
 nodes['h.L030.C1.4']['locators'].append(sl('L030',74,79))
 for id in ['L4.4','T1.2.parameters']:nodes['h.L030.'+id]['documentary_flags']=['Printed order is corrected to binom(n-k,k)-1 in the fixed contract; the source proof counts binom(n-k,k) panel elements.']
 for id in ['C4.5','T1.2.existence']:nodes['h.L030.'+id]['documentary_flags']=['The k=1, n=3 boundary is thin, as explicitly corrected in the accepted contract.']
 nodes['h.L030.L4.7']['documentary_flags']=['The printed upper-bound sentence is not expanded. The new proof reconstructs the action and separately proves the uncolored graph group.']
 nodes['h.L030.C5.1']['documentary_flags']=['Only the displayed 63-vertex example is corrected to S7 x S3. No impossibility claim about a different graph in the literal existential statement.']
 deps('h.L030.L2.1',['h.L030.Definitions'],'Uses disjoint-set walks and two-step overlap bounds.','definition_use')
 deps('h.L030.L2.2',['h.L030.Definitions'],'Explicitly partitions differing set elements to construct paths.','definition_use')
 deps('h.L030.L3.1',['h.L030.L2.1','h.L030.L2.2'],'Both lemmas are named for the upper and lower diameter bounds.')
 deps('h.L030.L3.2',['h.L030.Definitions'],'Displays the six- and four-cycles in the bipartite double.','definition_use')
 deps('h.L030.L3.3',['h.L030.L2.1'],'The printed proof invokes odd cycles in the Kneser graph.')
 for id in ['L4.1','L4.2','L4.4','L4.6']:deps('h.L030.'+id,['h.L030.Construction1.1'],'Uses disjoint k-subsets on the displayed ground set.','definition_use')
 deps('h.L030.L4.3',['h.L030.L3.3','h.L030.L4.2','h.L030.Construction1.1'],'The source uses connected rank-two truncations and flag-transitive induction on residues.')
 deps('h.L030.C4.5',['h.L030.L4.4'],'Literal source inference, subject to the already recorded thin-boundary correction.')
 deps('h.L030.L4.7',['h.L030.L4.2','h.L030.Construction1.1'],'The source uses its symmetric-group action and symmetry in the types; upper bound is asserted.')
 for suff,src in {'existence':['L4.1','L4.2','L4.3','C4.5'],'groups':['L4.7'],'parameters':['L4.4','L4.6','L3.1','L3.2']}.items():
  deps('h.L030.T1.2.'+suff,['h.L030.'+x for x in src],'Section 4 explicitly assembles the preceding lemmas into the main theorem.')
  edge('h.L030.T1.2.'+suff,'h.L030.T1.2','These clauses form the main statement.','proof_assembly')
 deps('h.L030.C1.3',['h.L030.Construction1.1','h.L030.T1.2.groups','h.L030.T1.2.existence'],'The printed proof uses the common residue model and transitivity.')
 deps('h.L030.C1.4',['h.L030.L4.1','h.L030.L4.2'],'Maximal cliques are chambers and the action is transitive on chambers.')
 deps('h.L030.C4.8',['h.L030.L4.6','h.L030.L3.1','h.L030.L3.2'],'Rank-two residues, gonality and diameter give the printed criterion.')
 deps('h.L030.C5.1',['h.L030.C1.3','h.L030.T1.2.groups','h.L030.Construction1.1'],'Specializes the displayed construction; the fixed contract corrects its full group.')

 # New proof parent units. Fine branches below replace broad parent edges.
 for row in author_map['nodes']:
  doc=next((k for k,v in TEX.items() if v==row['file']),None);need(doc,'new node file')
  first,last=row['start_line'],min(row['end_line'],len((roots['public']/('papers/topic-b/v2/'+row['file'])).read_text().splitlines()))
  if row['id']=='B4.TypedAut':first,last=63,69
  if row['id']=='B4.Aut':first,last=70,104
  if row['id']=='B3.Coordinates':first,last=68,80
  if row['id']=='B3.Frattini':first,last=52,64
  n(doc,row['id'],row['id']+' complete statement and proof',first,last,'named_result')
 # Human labels are exact mathematical descriptions rather than identifiers alone.
 labels={'UB.Coset':'Coset recognition and residue coordinates','UB.Flags':'Residual primitivity gives flag transitivity',
 'UB.Relative':'Generation from residual maximality','UB.Generation':'Geometric rank and generation interface',
 'UB.F':'Weighted forests, intersections and flag completion','UB.Overgroups':'Overgroups of a two-block stabilizer',
 'B1.Profile':'Properties of the unit-weight tree geometry','B1.Reconstruction':'Recognizing the tree from its diagram',
 'B1.Source':'All four inductively minimal conclusions','B2.RelativeBound':'Normal-quotient independent-family bound',
 'B2.Sign':'The parity-twisted subgroup formula','B2.Blocks':'Excluding two-point imprimitivity blocks',
 'B2.Extremal':'Recognizing every extremal marking','B2.Count':'The three generating-set counts',
 'B2.MaxRank':'Recognizing all maximum-rank geometries','B2.Source':'The full symmetric-group contract',
 'B3.Quotient':'Exact coset transport through a normal quotient','B3.Maximal':'Relative finite generation gives maximal overgroups',
 'B3.Transport':'Relative generating families through the Frattini quotient','B3.Ladder':'Normal containment through a maximal chain',
 'B3.Frattini':'Frattini containment and faithful quotient','B3.Coordinates':'Finite p-group coordinate classification',
 'B3.Source':'The complete corrected Frattini contract','B4.Star':'Weighted-star geometry and all residues',
 'B4.Distance':'Exact distances, diameter and gonality','B4.Johnson':'Recovering points from the Johnson graph',
 'B4.TypedAut':'Recovering the common action across types','B4.Aut':'Recovering types from the uncolored graph',
 'B4.Source':'The corrected disjoint-subset contract'}
 for id,label in labels.items():nodes[id]['label']=label
 # Definitions and hypothesis checks remain actual prerequisites in the graph.
 for doc,id,label,first,last in [
 ('U1','UB.Incidence','Finite types, action, flags and residues',2,11),
 ('U1','UB.CosetData','Cosets, Borel and conditions G1–G3',13,27),
 ('U1','UB.Primitivity','Primitive actions and maximal residual stabilizers',68,82),
 ('U1','UB.Independence','Finite relative families and numerical invariants',99,108),
  ('U3','UB.ForestData','Finite tree and positive finite blocks',2,5),
  ('U4','UB.TwoBlockData','Arbitrary finite two-block stabilizer and its size cases',2,4),
 ('B1','B1.Conventions','Positive finite rank, connected diagram and property definitions',12,15),
 ('B2','B2.Hypotheses','Separate Whiston inputs and n >= 7 range',12,16),
 ('B3','B3.Hypotheses','Finite rank versus finite p-group scope',49,50),
 ('B4','B4.StarData','Positive central weight and exact source parameter substitution',12,20)]:n(doc,id,label,first,last,'definition')
 branches=[
 ('U1','UB.Coset.flags','Common representatives and exact residues',35,44,'UB.Coset'),
 ('U1','UB.Coset.connected','Connected coset graphs equal subgroup generation',46,56,'UB.Coset'),
 ('U1','UB.Coset.converse','Firm flag transitivity yields G1–G3',58,65,'UB.Coset'),
 ('U2','UB.Relative.choices','Existence and independence of panel choices',16,16,'UB.Relative'),
 ('U2','UB.Relative.induction','Maximality induction and resulting intersections',18,18,'UB.Relative'),
 ('U3','UB.F.intersections','Unique paths and transposition generation',24,24,'UB.F'),
 ('U3','UB.F.flags','Laminar Boolean atoms complete every partial flag',26,26,'UB.F'),
 ('U3','UB.F.geometry','Distinct intersections, generation and residue products',28,28,'UB.F'),
 ('U4','UB.Overgroups.interval','Cross-block transpositions classify the subgroup interval',6,6,'UB.Overgroups'),
 ('U4','UB.Overgroups.balance','At most one balanced weighted cut',8,8,'UB.Overgroups'),
 ('B1','B1.Profile.local','Panels, rank-two residues and the line graph',31,31,'B1.Profile'),
 ('B1','B1.Profile.residual','Inductive minimality and a primitive leaf in each residue',33,33,'B1.Profile'),
 ('B1','B1.Profile.middle','Balanced cuts give exactly the middle criterion',35,35,'B1.Profile'),
 ('B1','B1.Profile.star','Residual primitivity iff the tree is a star',37,37,'B1.Profile'),
 ('B2','B2.Extremal.omissions','Apply W1/W2 and exclude the imprimitive case',53,53,'B2.Extremal'),
 ('B2','B2.Extremal.tree','Orbit-crossing edges form a tree',55,55,'B2.Extremal'),
 ('B2','B2.Extremal.local','Forest intersections force the local generator types',57,57,'B2.Extremal'),
 ('B2','B2.Extremal.borel','A fixed point rules out the balanced-cut enlargement',59,59,'B2.Extremal'),
 ('B2','B2.MaxRank.ordinary','Ordinary marking satisfies all coset conditions',69,69,'B2.MaxRank'),
 ('B2','B2.MaxRank.sign','Weighted edge contraction, parity adjustment and primitive residues',71,73,'B2.MaxRank'),
 ('B2','B2.MaxRank.unique','Panel orders determine choices up to inversion',75,75,'B2.MaxRank'),
 ('B2','B2.MaxRank.general','Arbitrary parabolics at maximum rank coincide with marking parabolics',77,84,'B2.MaxRank'),
 ('B3','B3.Nongeneration','Setwise nongeneration under the maximal-overgroup hypothesis',24,27,None),
 ('B3','B3.Ladder.finite','The maximal chain proves relative finite generation',40,40,'B3.Ladder'),
 ('B3','B3.Ladder.propagation','First failure propagates upwards through distinct intersections',42,48,'B3.Ladder'),
 ('B3','B3.Frattini.containment','Verify every hypothesis of the normal-chain theorem',60,60,'B3.Frattini'),
 ('B3','B3.Frattini.core','Identify the entire action kernel',62,62,'B3.Frattini'),
 ('B3','B3.Frattini.free','The faithful Frattini quotient and indexed-family correspondence',64,64,'B3.Frattini'),
 ('B3','B3.InfiniteCorrection','The Prüfer-group counterexample and the exact correction',66,66,None),
 ('B3','B3.Coordinates.basis','Elementary abelian quotient and relative basis',73,73,'B3.Coordinates'),
 ('B3','B3.Coordinates.geometry','Coordinate cosets, RPRI and chamber regularity',75,75,'B3.Coordinates'),
 ('B3','B3.Coordinates.count','Converse and count of indexed hyperplane families',77,80,'B3.Coordinates'),
 ('B3','B3.Product','Rank-two direct sum via subgroup products',82,82,None),
 ('B3','B3.Subspace','Maximal-subspace dimension calculation',82,82,None),
 ('B3','B3.ResidueTest','Apply the normal-chain theorem to each residue',84,87,None),
 ('B4','B4.Star.residues','Positive weights, residue complements and exact panels',27,27,'B4.Star'),
 ('B4','B4.Star.links','Tensor product, links and chamber transitivity',29,29,'B4.Star'),
 ('B4','B4.Distance.walks','Exact replacement bounds and realizing paths',40,44,'B4.Distance'),
 ('B4','B4.Distance.gonality','Common-neighbor counts and shortest cycles',46,51,'B4.Distance'),
 ('B4','B4.Diagram','Diagram orders and geometric IP criterion',53,53,None),
 ('B4','B4.TypedAut.points','Reconstruct Johnson adjacency in each type',65,65,'B4.TypedAut'),
 ('B4','B4.TypedAut.synchronization','Disjointness neighborhoods force equal point permutations',67,69,'B4.TypedAut'),
 ('B4','B4.Spectrum','The subset-indicator filtration gives the Kneser eigenvalues',73,89,None),
 ('B4','B4.TypeEigenspace','N > rk identifies the least eigenspace exactly',91,94,None),
 ('B4','B4.Aut.independent','The least-eigenvalue bound and its equality case',98,102,'B4.Aut'),
 ('B4','B4.Desargues','Identify the displayed 63-vertex graph and its full group',104,104,None)]
 for doc,id,label,first,last,parent in branches:n(doc,id,label,first,last,'proof_branch',parent)
 # Refine the mixed sentence into nonoverlapping semantic locators; costs are still unset.
 for id,start,end in [('B3.Product','Two subsidiary assertions','If \\(U,W'),('B3.Subspace','If \\(U,W',None)]:
  L=nodes[id]['locators'][0];s=(roots['public']/L['path']).read_text();chunk=s[L['start_codepoint']:L['end_codepoint_exclusive']]
  offset=chunk.index(start);stop=chunk.index(end) if end else len(chunk)
  L['start_codepoint']+=offset;L['end_codepoint_exclusive']=L['start_codepoint']+(stop-offset)
  L['sha256_utf8']=sha(s[L['start_codepoint']:L['end_codepoint_exclusive']].encode())
 for row in branches:
  if row[5]:edge(row[1],row[5],'This substantive proof branch is part of the complete result.','proof_assembly')

 # Exact new prerequisite chains. Fine branches carry the actual hypotheses.
 deps('UB.CosetData',['UB.Incidence'],'Fixes the finite typed incidence conventions.','definition_use')
 deps('UB.Primitivity',['ext.PrimitiveStabilizer'],'The text explicitly uses the elementary invariant-partition/subgroup-interval equivalence, including induced actions.','retained_input_use')
 deps('B1.Conventions',['UB.Primitivity'],'Ordinary and residual primitivity have the common paper conventions.','definition_use')
 for id in ['UB.Coset.flags','UB.Coset.connected','UB.Coset.converse']:deps(id,['UB.CosetData'],'Uses precisely the displayed cosets and G1–G3.','definition_use')
 edge('UB.Coset.flags','UB.Coset.connected','Residues are identified before applying the graph criterion.')
 edge('UB.Coset.connected','UB.Coset.converse','The reverse implication reuses the connectedness criterion.')
 deps('UB.Flags',['UB.Incidence','UB.Primitivity'],'Finite rank and transitive primitive types allow the chamber-matching induction.','hypothesis_use')
 deps('UB.Relative.choices',['UB.CosetData','UB.Independence'],'Distinct intersections give a choice in each panel; off-diagonal membership proves independence.','definition_use')
 deps('UB.Relative.induction',['UB.Relative.choices','UB.Primitivity'],'The chosen element escapes the maximal lower intersection; induction derives equality.')
 deps('UB.Generation',['UB.Flags','UB.Coset','UB.Relative','UB.Independence'],'The theorem explicitly verifies all subgroup hypotheses from the geometric action.')
 for id in ['UB.F.intersections','UB.F.flags','UB.F.geometry']:deps(id,['UB.ForestData'],'Finite positive blocks and unique tree paths are the stated hypotheses.','hypothesis_use')
 deps('UB.F.geometry',['UB.F.intersections','UB.F.flags','UB.Coset'],'Apply the coset criterion after proving all three conditions and the residue factors.')
 deps('UB.Overgroups.interval',['UB.TwoBlockData'],'Uses arbitrary finite nonempty disjoint blocks, without a tree hypothesis.','definition_use')
 deps('UB.Overgroups.balance',['UB.ForestData'],'Positive weights make every proper half-subtree lighter.','hypothesis_use')
 for id in ['B1.Profile.local','B1.Profile.residual']:deps(id,['UB.F','B1.Conventions'],'Specializes every block to one point and applies the exact residue formula.')
 edge('UB.Overgroups','B1.Profile.residual','The leaf point stabilizer is the unbalanced two-block case, or the explicit two-point exception.')
 deps('B1.Profile.middle',['UB.Overgroups','B1.Profile.local','B1.Conventions'],'The line-graph component sizes translate balanced cuts into a middle.')
 deps('B1.Profile.star',['UB.F','UB.Overgroups','B1.Profile.local'],'A nonstar contains the three-edge path with a nonprimitive balanced cut.')
 deps('B1.Reconstruction',['B1.Profile','ext.B97'],'Clique reconstruction gives the tree; retained uniqueness identifies the original pair.')
 deps('B1.Source',['B1.Profile','B1.Reconstruction','UB.Overgroups'],'Tree parity supplies the even-rank clause; the other three follow from the full profile.')
 deps('B2.RelativeBound',['UB.Independence'],'The argument works with the declared finite numerical invariants.','definition_use')
 deps('B2.Sign',['UB.F'],'The parity-kernel calculation uses the proved forest-generated subgroups and intersections.')
 deps('B2.Blocks',['B2.RelativeBound','ext.W1'],'The normal elementary abelian block kernel is bounded twice after extremal equality.')
 deps('B2.Extremal.omissions',['ext.W1','ext.W2','B2.Blocks','B2.Hypotheses'],'Check n >= 7, generation, and the imprimitive exceptional range.')
 deps('B2.Extremal.tree',['B2.Extremal.omissions'],'Each selected edge crosses its own omission orbit and lies inside the others.')
 deps('B2.Extremal.local',['B2.Extremal.tree','UB.F'],'Intersect the actual tree cut stabilizers to reduce to one- and two-edge groups.')
 deps('B2.Extremal.borel',['B2.Extremal.local','UB.F','B2.Sign','UB.Overgroups'],'A pendant fixed point rules out a half interchange; the full marking intersection is trivial.')
 deps('B2.Count',['B2.Extremal','ext.Cayley'],'The classification and canonical edge switches justify the bijections before applying Cayley.')
 deps('B2.MaxRank.ordinary',['UB.F','B2.Sign','UB.Primitivity','UB.Overgroups'],'The forest completes flags and its leaf point stabilizer is maximal by the two-block interval.')
 deps('B2.MaxRank.sign',['UB.F','B2.Sign','B2.Extremal','UB.Primitivity'],'Contract the distinguished edge to a block of weight two; the common odd element adjusts parity.')
 deps('B2.MaxRank.unique',['UB.Generation','B2.Extremal','ext.AutSn'],'Panel orders are two or three; the specified-action equivalence uses innerness.')
 deps('B2.MaxRank.general',['UB.Coset','ext.W1','B2.Extremal','UB.Overgroups','B2.MaxRank.ordinary','B2.MaxRank.sign'],'Without assuming G4, firmness gives choices and G2 determines parabolics after the sole balanced-cut possibility is eliminated.')
 deps('B2.Source',['B2.Extremal','B2.Count','B2.MaxRank','B2.RelativeBound','UB.Generation','B2.Sign','UB.F'],'Assembles exactly the eight fixed numbered results and all counting conventions.')
 deps('B3.Quotient',['ext.SubgroupCorrespondence'],'Inverse images of typed cosets give the full incidence and subgroup-interval correspondence.','retained_input_use')
 deps('B3.Maximal',['ext.Zorn'],'A finite relative generating family prevents a chain of proper overgroups from exhausting G.','retained_input_use')
 deps('B3.Transport',['B3.Nongeneration'],'The equivalence is applied to the full generating subgroup and each deletion subgroup.')
 edge('B3.Maximal','B3.Transport','Supplies the sufficient relative-finite-generation application after the theorem; it is not a necessary condition in the abstract maximal-overgroup statement.','hypothesis_use')
 deps('B3.Ladder.finite',['B3.Maximal'],'Maximal-chain witnesses give a finite relative generating family, so proper H_i have maximal overgroups.')
 deps('B3.Ladder.propagation',['B3.Ladder.finite','UB.CosetData'],'Normality and maximality propagate the first failure; distinct intersections exclude equality at an intermediate endpoint.')
 deps('B3.Frattini.containment',['UB.Flags','UB.Coset','UB.Primitivity','B3.Ladder','B3.Quotient','B3.Hypotheses'],'All assumptions of the chain theorem are verified, including finite rank and actual residue maximality.')
 deps('B3.Frattini.core',['B3.Quotient'],'The intersection of parabolic cores is exactly the action kernel.')
 deps('B3.Frattini.free',['B3.Frattini.containment','ext.SubgroupCorrespondence'],'Maximal subgroups of the quotient have trivial intersection; quotient/pullback concern indexed families.')
 deps('B3.InfiniteCorrection',['B3.Transport','B3.Maximal','B3.Ladder'],'The Prüfer-group witness distinguishes the unrestricted false converse from the valid geometric theorem.')
 deps('B3.Coordinates.basis',['B3.Frattini','UB.Generation','ext.FinitePFrattini','ext.LinearAlgebra'],'First quotient by Phi(P), then use relative generation and independence to obtain an actual basis.')
 deps('B3.Coordinates.geometry',['B3.Coordinates.basis','B3.Quotient'],'Coordinate cosets directly give every incidence, primitive residue and chamber action.')
 deps('B3.Coordinates.count',['B3.Coordinates.geometry','ext.LinearAlgebra'],'Independent functionals give the converse and the indexed-family count.')
 deps('B3.Product',['UB.CosetData'],'The elementary coset intersection formula proves the pair-product criterion.','definition_use')
 deps('B3.Subspace',['ext.LinearAlgebra'],'The one-dimensional quotient computes the missing hyperplane dimension.','retained_input_use')
 deps('B3.ResidueTest',['UB.Flags','UB.Coset','B3.Ladder'],'Check the same hypotheses inside the actual residue, whose common subgroup is B.')
 deps('B3.Source',['B3.Frattini','B3.Coordinates','B3.Transport','B3.InfiniteCorrection','B3.Product','B3.Subspace','B3.ResidueTest'],'Each source clause and the exact infinite-group correction is accounted for.')
 deps('B4.StarData',['UB.ForestData'],'The source substitution gives central block size n-2k > 0.','hypothesis_use')
 deps('B4.Star.residues',['UB.F','B4.StarData'],'All weighted-forest hypotheses are checked before the specialization and panel calculation.')
 deps('B4.Star.links',['B4.Star.residues'],'The same disjoint-subset model identifies links and maximal cliques.')
 deps('B4.Distance.walks',['B4.StarData'],'The rank-two ambient n=2k+s has s positive.','hypothesis_use')
 deps('B4.Distance.gonality',['B4.Distance.walks'],'Use the exact odd closed-walk length and explicit common-neighbor calculation.')
 deps('B4.Diagram',['B4.Star','B4.Distance'],'No residue is a digon; panel size minus one gives the diagram order.')
 deps('B4.TypedAut.points',['B4.Distance.gonality','B4.Johnson','B4.StarData'],'The common-neighbor coefficient identifies Johnson adjacency, and N > rk >= 2k checks the Johnson lemma hypothesis.')
 deps('B4.TypedAut.synchronization',['B4.TypedAut.points','B4.StarData'],'Distinct disjointness neighborhoods force one common point action; type permutations split.')
 deps('B4.Spectrum',['B4.StarData','ext.RealSpectral'],'Inclusion–exclusion on subset indicators derives the complete eigenvalue list; the symmetric spectral theorem gives diagonalization.')
 deps('B4.TypeEigenspace',['B4.Spectrum','B4.StarData'],'N > rk makes the tensor-product least eigenspace exactly the type-constant vectors.')
 deps('B4.Aut.independent',['B4.TypeEigenspace','B4.TypedAut','ext.RealSpectral'],'The independent-set bound and equality case force every graph automorphism to permute types.')
 deps('B4.Desargues',['B4.Star','B4.Aut'],'Complementation identifies the classical 10_3 link and the proved full graph group specializes.')
 deps('B4.Source',['B4.Star','B4.Distance','B4.Diagram','B4.TypedAut','B4.Aut','B4.Desargues'],'Assembles existence, parameters, links and the already recorded corrections.')

 # Explicit source provenance is not a logical premise of a proof written anew.
 for src,dst,why in [
 ('h.N003.T3.1','UB.Relative','The shared maximality induction re-proves Cameron–Cara’s displayed argument.'),
 ('h.N003.C2.3','UB.F','The weighted theorem extends the historical unweighted forest intersection argument.'),
 ('h.N003.T3.2.ordinary','UB.F','Historical flag completion is replaced by the full laminar-atom argument.'),
 ('h.N003.T1.1','B2.RelativeBound','The normal-quotient proof is reworked explicitly, with attribution.'),
 ('h.N003.T2.1','B2.Extremal','The historical recognition is reconstructed using shared forest intersections.'),
 ('h.N008.T3.1','B3.Ladder','The normal-chain argument is reworked and its infinite-group step supplied.'),
 ('h.N008.P3.2','B3.Quotient','The known quotient correspondence is proved locally.'),
 ('h.N008.T3.8','B3.Coordinates','The old classification is derived from the shared relative-generation basis.'),
 ('h.L030.Construction1.1','B4.Star','The source construction is identified with the weighted star.'),
 ('h.L030.L2.2','B4.Distance','The replacement-path idea is retained and its bounds proved exactly.'),
 ('h.L030.L4.7','B4.TypedAut','The new local proof supplies the explicit reconstruction absent from the short source upper-bound assertion.')]:edge(src,dst,why,'attribution_identity')

 # Formal evidence and finite diagnostics are deliberately outside proof closure.
 lean_path='papers/topic-b/v2/formal/ResidualGeneration.lean';lean=read('public',lean_path);ls=lean.splitlines()
 reports=json.loads(read('public','papers/topic-b/v2/formal/scope.json'))['reported_declarations']
 for name in reports:
  short=name.split('.')[-1];start=next(i+1 for i,x in enumerate(ls) if re.match(r'theorem '+short+r'\b',x))
  end=next((i+1 for i in range(start,len(ls)) if re.match(r'(?:theorem |end |#print)',ls[i])),len(ls)+1)-1
  id='formal.'+short
  add(id,'Lean','verification',short,'formal_component',[loc('public',lean_path,start,end)],scope='Exactly the subgroup theorem in formal/scope.json; imports trust compiled dependencies, standard axioms only.')
  edge('UB.Relative',id,'This is separately checked component evidence; no geometry/application formalization is implied.','formalized_component')
 add('validation.controls','Validation','verification','Finite missing-hypothesis countermodels and compilation controls','validation',
     [loc('public','papers/topic-b/v2/check.py',1,len(read('public','papers/topic-b/v2/check.py').splitlines()))],
     scope='No required mathematical enumeration and no logical-premise cost; replay infrastructure is not an omitted written argument.')
 edge('UB.Relative','validation.controls','Finite controls test the actual subgroup hypotheses.','validation_evidence')

 historical={
 'A1':'h.N001.T1.a','A2':'h.N001.T1.b','A3':'h.N001.T1.c','A4':'h.N001.T1.d',
 'B1':'h.N003.T1.1','B2':'h.N003.T2.1','B3':'h.N003.C2.2','B4':'h.N003.C2.3','B5':'h.N003.C2.4','B6':'h.N003.T3.1','B7':'h.N003.T3.2','B8':'h.N003.C3.3',
 'C1':'h.N008.T2.1','C2':'h.N008.T3.1','C3':'h.N008.P3.2','C4':'h.N008.C3.3','C5':'h.N008.T3.4','C6':'h.N008.P3.5','C7':'h.N008.L3.6','C8':'h.N008.P3.7','C9':'h.N008.T3.8','C10':'h.N008.Test4.2','C11':'h.N008.Core4.3',
 'D1':'h.L030.T1.2.existence','D2':'h.L030.T1.2.groups','D3':'h.L030.T1.2.parameters','D4':'h.L030.C1.3','D5':'h.L030.C1.4','D6':'h.L030.C4.8','D7':'h.L030.C5.1'}
 specific={
 'A1':['B1.Source'],'A2':['B1.Source'],'A3':['B1.Source'],'A4':['B1.Source'],
 'B1':['B2.RelativeBound'],'B2':['B2.Extremal','B2.Sign','UB.F'],'B3':['B2.Count'],'B4':['B2.Sign','UB.F'],'B5':['B2.Extremal.borel'],'B6':['UB.Generation'],'B7':['B2.MaxRank'],'B8':['B2.MaxRank.general'],
 'C1':['B3.Transport','B3.InfiniteCorrection'],'C2':['B3.Frattini.containment'],'C3':['B3.Quotient'],'C4':['B3.Frattini'],'C5':['B3.Frattini.free'],'C6':['B3.Product'],'C7':['B3.Subspace'],'C8':['B3.Coordinates'],'C9':['B3.Coordinates'],'C10':['B3.ResidueTest'],'C11':['B3.Frattini.core'],
 'D1':['B4.Star'],'D2':['B4.TypedAut','B4.Aut'],'D3':['B4.Diagram'],'D4':['B4.Star.links'],'D5':['B4.Star.links'],'D6':['B4.Diagram'],'D7':['B4.Desargues']}
 def closure(targets):
  found=set(targets);pending=list(targets)
  for x in pending:
   for e in edges:
    if e['target']==x and e['kind'] in LOGICAL and e['source'] not in found:
     found.add(e['source']);pending.append(e['source'])
  return sorted(found)
 coverage=[]
 for row in contract['rows']:
  key=row['adapter'];need(key in historical and key in specific,'matched row '+key)
  coverage.append(dict(adapter=key,source_id=row['source_id'],source_reference=row['source_reference'],
    preserved_contract=row['source_contract'],source_span=row['source_span'],
    historical_output=historical[key],new_outputs=specific[key],
    accepted_owner_nodes=row['new_tex_nodes'],accepted_owner_spans=row['new_tex_spans'],
    historical_closure=closure([historical[key]]),new_closure=closure(specific[key]),
    statement_match='same fixed clause, including its recorded corrections and qualifications',
    cost=None))
 # Complete applications include extra locally proved implications as written;
 # per-clause routes are not substitutions for full-document accounting.
 outgroups={'B1':'B1.Source','B2':'B2.Source','B3':'B3.Source','B4':'B4.Source'}
 checks=dict(nodes=len(nodes),edges=len(edges),nodes_by_side=dict(Counter(n['side'] for n in nodes.values())),
             nodes_by_category=dict(Counter(n['category'] for n in nodes.values())),
             edges_by_kind=dict(Counter(e['kind'] for e in edges)),source_clauses=len(coverage))
 # Bind the fixed but not yet independently adopted measurement candidate only.
 candidate='topic_B_measurement/manifest.json'
 if (roots['research']/candidate).exists():
  measurement_candidate=binding('research',candidate)
  need(measurement_candidate['sha256']=='644bcb427db39ac60f244c1cfe807b884f78691fe8c606de0dc9bead00f9ce99','measurement candidate pin')
 else:measurement_candidate=None
 graph=dict(schema='topic_b_paired_logical_graph_v1',status='AUTHOR_CANDIDATE_PENDING_INDEPENDENT_LOGICAL_REVIEW',
  scope='Exactly four accepted source contracts and their thirty fixed clauses; documentary historical routes and actual complete new proof routes.',
  public_proof_edition_commit=COMMIT,source_order=list(SOURCE),applications={'B1':'N001','B2':'N003','B3':'N008','B4':'L030'},
  document_titles={'N001':'Some properties of inductively minimal geometries',
   'N003':'Independent generating sets and geometries for symmetric groups',
   'N008':'Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries',
   'L030':'An infinite family of incidence geometries whose incidence graphs are locally X (revised institutional edition)',
   'U_B':'Forest coordinates and relative generation','B1':'Inductively minimal geometries and their tree coordinates',
   'B2':'Extremal symmetric-group markings and their geometries','B3':'Frattini quotients and primitive coordinate geometries',
   'B4':'Disjoint-subset geometries and their full graph automorphisms'},
  edge_orientation='prerequisite -> use',logical_edge_kinds=LOGICAL,
  nonlogical_edge_kinds=['attribution_identity','formalized_component','validation_evidence'],
  source_bindings=source_bindings,immutable_inputs=sorted(inputs.values(),key=lambda r:(r['namespace'],r['path'])),
  nodes=list(nodes.values()),edges=edges,checks=checks,
  graph_granularity='Named results and substantive proof branches; definitions, retained statements and external inputs remain distinguished. Parent and child locators can overlap and are not additive costs.',
  node_count_policy='Descriptive category counts only. Historical and new granularity differ; no node-count factor or judgement of research quality.',
  measurement=dict(weights_assigned=False,exclusive_partition_assigned=False,external_costs_unknown=True,measurement_candidate=measurement_candidate,
   policy='Await independent adoption and exact calibrated span partition. Full manuscripts remain the denominator; graph closures are explanatory, not whole-paper costs.',
   N001='Authored-browser locators are documentary evidence only; they are not an invented PDF or replacement PDF numerator.'),
  new_application_outputs=outgroups,new_output_closures={k:closure([v]) for k,v in outgroups.items()},
  required_mathematical_programs=[],new_source_credit=0,new_question_credit=0,compression_ratio=None,
  limits=['The historical arrows record identifiable printed uses and do not certify every original inference. Flags preserve previously recorded corrections and unexpanded printed steps.',
          'No original N001 PDF is available; its diagram/formula browser rendering can be damaged.',
          'No fresh whole-primary reading of retained B97, Whiston, CFSG or older classification proofs is claimed.',
          'No blanket recovery of all auxiliary statements: small-degree N003 exceptions, N008 Gaschuetz/Archer classifications and source suggestions are excluded as in the accepted contracts.',
          'All mathematical text is already present in the admitted complete papers; this packet changes only dependency metadata.',
          'Formal components are verification evidence and not new dependencies that price the same written proof twice.'])
 protocol=dict(schema='topic_b_logical_protocol_v1',status='AUTHOR_BOUNDARY_PENDING_INDEPENDENT_REVIEW',
  scope=graph['scope'],orientation=graph['edge_orientation'],logical_edge_kinds=LOGICAL,
  source_representation=source_bindings,new_paper_root='papers/topic-b/v2',authoritative_map='papers/topic-b/v2/mapping_correction/source_contract_map.json',
  source_text_exported=False,graph_weights=False,raw_node_ratio=False,
  locator_rule='Unicode codepoint half-open spans in the exact bound text edition, with inclusive physical text-file lines. Browser display lines and PDF page locators are separate fields.',
  overlap_rule='These are semantic locators, not an exclusive partition. Parent/branch overlap must never be added as cost.',
  retained_rule='External inputs have unknown cost, never zero; source recalls and local proofs of the same classical fact are distinguished.',
  closure_rule='Traverse only logical_edge_kinds. Attribution and formal/control evidence never enter mathematical prerequisite closure.',
  historical_rule='An edge is a documentary use in the printed source, not a assertion of proof minimality or a certification of an unexpanded/flagged inference.',
  full_contract_rule='Every fixed clause retains its complete source contract and accepted new-owner span references; finer outputs can narrow a displayed route but never the admitted manuscript coverage.')
 a.out.mkdir(parents=True)
 gaps={'N001':{'original_pdf':'unavailable; browser rendering is documentary evidence only','retained_input':'B97 classification and uniqueness','mathematical_contract':'all four accepted clauses preserved'},
       'N003':{'retained_inputs':['W1','W2 with stated CFSG dependence','Cayley','Aut(S_n) inner for n >= 7'],
               'not_targeted':['small-degree exceptional cases in the source remarks','the direct-product and classification-free questions'],
               'mathematical_contract':'all eight accepted numbered clauses preserved, including the three counting conventions'},
       'N008':{'retained_inputs':['finite p-group Frattini quotient','subgroup correspondence','Zorn','elementary linear algebra'],
               'not_targeted':['Gaschuetz structure theorem cited as Theorem 4.1','older Archer classification cited in section 4.3','source population statistics'],
               'mathematical_contract':'all eleven accepted clauses preserved; the infinite generating-set converse is corrected and the infinite geometric theorem is not narrowed'},
       'L030':{'edition':'exact revised institutional PDF, not silently the journal edition',
               'retained_inputs':['elementary real symmetric spectral theorem'],
               'mathematical_contract':'all seven accepted clauses preserved, including three recorded corrections; the graph does not refute the existence of a different locally Desargues graph'},
       'all':{'independent_graph_review':'pending','weights_and_partition':'not assigned','retained_external_and_image_costs':'unknown, not zero','required_mathematical_programs':[]}}
 for name,obj in [('logical_graph.json',graph),('coverage.json',dict(schema='topic_b_thirty_clause_coverage_v1',rows=coverage,scope_gaps=gaps)),('protocol.json',protocol)]:
  (a.out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(checks))


if __name__=='__main__':main()
