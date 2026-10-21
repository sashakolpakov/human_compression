"""Bind N008 primary/version, all numbered items, and extension proof interface.
No source content is modified and no source/replacement length ratio is computed.
"""
from pathlib import Path
import hashlib,json,re
ROOT=Path(__file__).resolve().parent
PDF='sources/phase16_frattini_geometries.pdf'
TXT='sources/phase16_frattini_geometries.txt'
EXT='phase36_compress_forest_N008_extension.md'
EXPECTED={PDF:'cfbd53bc367ecaea644214eb0f64fc5db0c20d63096fdc239cf5d61c3f72c5c9',TXT:'056823e93c4da84e0fb8f9425ebb2a1f27efc78b7ce6bb18a69b09c0b102f128'}
def digest(data): return hashlib.sha256(data).hexdigest()
def bind(name):
 data=(ROOT/name).read_bytes()
 h=digest(data)
 if name in EXPECTED: assert h==EXPECTED[name],name
 return {'path':name,'absolute_path':str(ROOT/name),'sha256':h,'bytes':len(data)}
s=(ROOT/TXT).read_text()
def span(a,b):
 return {'start_codepoint':a,'end_codepoint_exclusive':b,'sha256_utf8':digest(s[a:b].encode())}
found=list(re.finditer(r'^(Theorem|Proposition|Corollary|Lemma) (\d+\.\d+)\.',s,re.M))
assert len(found)==10
records=[
 ('Theorem 2.1',[171,172],'C1','For B<=G and Phi=Phi(G), a family (s_i) is an independent generating family of G relative to B iff (Phi s_i) is an independent generating family of G/Phi relative to BPhi/Phi.','finite_group_specialization_and_explicit_infinite_correction','E1,E4','Elementary finite group theory; Zorn for relative finite-generation infinite extension'),
 ('Theorem 3.1',[173],'C2','A firm RWPRI coset geometry satisfies Phi(G)<=H_i for every type i, including infinite G.','full_finite_rank_geometric_scope','E0,E1,E2','Zorn for infinite groups; elementary subgroup theory'),
 ('Proposition 3.2',[174],'C3','If N is normal in G and N<=H_i for every type of a coset pregeometry, that pregeometry is isomorphic to the coset pregeometry (G/N,(H_i/N)).','full_statement_reproved_though_quoted_in_source','E3','Subgroup correspondence'),
 ('Corollary 3.3',[174],'C4','A firm RWPRI coset geometry (G,(H_i)) is isomorphic to (G/Phi(G),(H_i/Phi(G))).','full_finite_rank_geometric_scope','E0,E2,E3','Zorn for infinite groups; subgroup correspondence'),
 ('Theorem 3.4',[174],'C5','Every firm RWPRI geometry is isomorphic to a firm RWPRI geometry for a Frattini-free group.','full_finite_rank_geometric_scope','E0,E2,E3 and maximal-subgroup correspondence','Zorn for infinite groups; subgroup correspondence'),
 ('Proposition 3.5',[174],'C6','A rank-two coset pregeometry (G,(H_1,H_2)) is a direct sum iff H_1 H_2=G.','full_statement_reproved_though_quoted_in_source','Exact coset-product proof after E5','Elementary group theory'),
 ('Lemma 3.6',[174],'C7','For proper U,W<F_p^k with W not contained in U, if U is maximal and U intersect W is maximal in U, then W is maximal in F_p^k.','full_statement','Dimension proof after E5','Elementary vector spaces'),
 ('Proposition 3.7',[174,175],'C8','A firm coset geometry of a finite p-group is RWPRI iff it is RPRI.','full_stated_finite_scope','E0,E2,E3,E5 and existing Compress_A Theorem R(b)','Finite-p-group Frattini quotient is elementary abelian; elementary vector spaces'),
 ('Theorem 3.8',[175],'C9','A firm RWPRI coset geometry of a p-group is a direct sum of primitive rank-one geometries. The source section fixes finite p-groups, although this theorem sentence omits the word finite.','finite_p_group_context_explicit','E0,E2,E3,E5 and existing Compress_A Theorem R(b)','Finite-p-group Frattini quotient is elementary abelian; elementary vector spaces'),
 ('Theorem 4.1',[175],None,'A finite Frattini-free F with socle S=A times D (abelian and nonabelian simple factors respectively) has F=A semidirect K, K<=Aut(S)=Aut(A) times Aut(D), D=Inn(S)<=K, and K acts semisimply on A; the intersection of maximal K-invariant subgroups of A is trivial.','retained_source_quoted_Gaschütz_1953_theorem_not_rederived','No use in extension E0-E5','Gaschütz, Math.Z.58(1953),160-170; original not independently read in this extension')]
items=[]
for i,(name,pages,adapter,form,status,proof,bg) in enumerate(records):
 m=found[i]
 assert name==m.group(1)+' '+m.group(2),(name,m.group())
 end=found[i+1].start() if i+1<len(found) else s.index('4.1.1. Frattini free groups',m.start())
 items.append({'source_result':name,'printed_pages':pages,'source_anchor':span(m.start(),end),'source_anchor_role':'statement_and_context_block_not_length_selection','full_normalized_formulation':form,'adapter':adapter,'scope_status':status,'proof':proof,'retained_background':bg,'review_status':'new_assembled_extension_pending_independent_review' if adapter else 'declared_retained_background'})
extra=[]
for ref,start,end,adapter,form in [
 ('Section4.2','4.2. The Φ-test for a residue','4.2.1. How to compute','C10','For every residue at a flag of type J, Phi(H_J)<=H_J intersect H_i for every remaining type i; this is necessary, not sufficient.'),
 ('Section4.3','4.3. Other reduction in some cases','Acknowledgement.','C11','The largest normal subgroup of G contained in B is core_G(B)=intersection_i core_G(H_i); quotienting yields the faithful coset action, and for firm RWPRI geometries this kernel contains Phi(G). The separately cited Archer2004 classification at the end of this section is retained, not newly proved.')]:
 a=s.index(start);b=s.index(end,a)
 extra.append({'source_reference':ref,'printed_pages':[176],'source_anchor':span(a,b),'adapter':adapter,'full_normalized_formulation':form,'proof':'E2,E3, equation6.1' if adapter=='C10' else 'E2,E3, equation3.3','review_status':'pending_independent_review'})
body={'schema':'compress_A_N008_extension_review_v1','date':'2026-10-10','status':'separate_candidate_extension_not_admitted_to_reviewed_intake','source':{'id':'N008','title':'Using the Frattini Subgroup and Independent Generating Sets to Study RWPRI Geometries','authors':['Claude Archer','Philippe Cara','Jan Krempa'],'year':2005,'publication':'Beiträge zur Algebra und Geometrie46(1),169-177','primary_urls':['https://ftp.gwdg.de/pub/EMIS/journals/BAG/vol.46/no.1/b46h1car.pdf','https://emis.muni.cz/journals/BAG/vol.46/no.1/b46h1car.pdf'],'version':'Complete nine-page published primary PDF; two prior mirror responses identical','files':[bind(PDF),bind(TXT)],'reading':'Complete extraction pages1-9 (printed169-177), all statements/proofs/discussions/references read during this extension','read_limits':['No newly regenerated PDF extraction or independent visual formula-layout reconstruction.','Gaschütz1953, Archer2004 and Eick algorithm originals were not acquired or independently rechecked.']},'all_numbered_items':items,'unnumbered_target_items':extra,'candidate_scoped_corollary_count':11,'numbered_items_count':10,'numbered_items_reproved_or_corrected':9,'numbered_items_retained':1,'reused_core':{'file':'phase36_compress_forest_manuscript.md','theorem':'R(b)','interface':'H_J=<B,s_i:i not in J>; strong relative independence','new_application':'Frattini containment makes P/B elementary abelian; the existing generating equality then gives a coordinate basis and every p-group parabolic.','first_manuscript_modified_for_extension':False},'necessary_new_proof':['E0: finite-rank RWPRI implies flag transitivity','E1/E2: relative maximal-overgroup existence and normal-subgroup ladder','E3: exact coset-kernel transport','E4: Frattini transport of relative generators with valid infinite hypothesis and counterexample to unrestricted converse','E5: short coordinate specialization using R(b), not an imported p-group geometry classification'],'retained_inputs_for_new_results':['Elementary subgroup correspondence','Finite-p-group Frattini quotient is elementary abelian','Elementary vector-space theory','Zorn lemma for the explicitly infinite claims'],'source_imports_not_rederived':['Theorem4.1 quoted Gaschütz1953 structure of finite Frattini-free groups','Section4.3 cited Archer2004 primitive-group reduction'],'excluded':['Historical SmallGroups counts and asymptotic suggestion','Computing-Frattini algorithm implementations or runtime claims','Automorphism-orbit equality between G families and G/Phi families','Unrestricted infinite converse of Theorem2.1','Unrestricted infinite-p-group extension of Theorem3.8'],'correction':{'source':'Theorem2.1 and preceding simultaneous nongenerator assertion','counterexample':'G=C_(p^infinity) times C2, Phi(G)=C_(p^infinity) times1, B=1; the second-factor generator generates G/Phi(G) but not G.','proved_scope':'finite G, or every proper overgroup of B contained in a maximal subgroup (in particular G finitely generated relative to B)'} ,'measurement':{'ratio':None,'admitted_as_third_manuscript':False,'reason':'Independent extension proof/source scope review and final corrected main-result contract pending. New proof costs must be charged; no theorem count is a length ratio.'},'extension_file':bind(EXT),'structural_checks':{'complete_numbered_inventory':len(items)==10,'every_recovered_numbered_item_has_adapter':all(t['adapter'] for t in items if not t['scope_status'].startswith('retained')),'two_explicit_unnumbered_consequences':len(extra)==2,'source_hashes_verified':True}}
assert len(items)==10 and len(extra)==2
text=(ROOT/EXT).read_text()
assert re.findall(r'\*\*C(\d+) —',text)==[str(i) for i in range(1,12)]
assert text.count('\\[')==text.count('\\]') and text.count('\\(')==text.count('\\)')
(ROOT/'phase36_compress_forest_N008_intake.json').write_text(json.dumps(body,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'source_hashes_verified':True,'complete_numbered_inventory':len(items),'retained_numbered_background':1,'explicit_scoped_corollaries':11,'extension_sha256':body['extension_file']['sha256'],'ratio':None},indent=2))
