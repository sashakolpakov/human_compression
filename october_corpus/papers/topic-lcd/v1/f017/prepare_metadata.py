#!/usr/bin/env python3
"""Author metadata assembly; does not alter accepted input packets."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
STUDY = HERE.parent


def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def put(name, value):
    (HERE/name).write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def source_rows():
    rows = []
    def add(id, pages, target, disposition, section, common=(), retained=(), note=None):
        rows.append({'id': 'F017.'+id, 'source_physical_pages': pages,
                     'target': target, 'disposition': disposition,
                     'application_file': 'sections/'+section+'.tex',
                     'common_interfaces': list(common), 'retained_inputs': list(retained),
                     'qualification': note})
    a='00-scope'; b='01-projectors'; c='02-subsets'; d='03-borrowed'; e='04-srg'; f='05-paley'; g='06-other'
    add('Abstract.Introduction',[1,2],'LCD graph constructions, explicit projections, dimensions and row distance bounds','proved_principal_scope',a)
    add('Definitions',[2,3,4],'Code, hull, graph and reflexive/complement conventions; definitions of LCD/RLCD/CLCD','definitions_preserved',a)
    add('Result1',[3],'Massey nearest-neighbour reduction for an orthogonally split received word','proved_with_original_attribution',b)
    add('Lemma1',[3],'Full sum with orthogonal dual implies LCD','proved',b)
    add('Proposition1.1',[3,4],'Reflexive orthogonal projections, row-sum decomposition and binary support identities','proved_common_corollary',b,['ULCD.Reflexive'])
    add('Proposition1.2',[4],'Complementary projections in the two degree branches','proved_common_corollary',b,['ULCD.Complement'])
    add('Definition2.coincidence',[4],'When both RLCD and CLCD hold the two displayed dual spaces coincide','proved_common_corollary',c,['ULCD.Complement','ULCD.Reflexive'])
    add('SpectralPreliminary',[5],'Integral spectral rank lower bound; exact rank if at most one distinct eigenvalue vanishes modulo p','proved_local_polynomial_argument',b)
    add('Result2',[5],'ker A lies in im(A+I); equality exactly when A(A+I)=0','proved_common_and_local',b,['ULCD.Reflexive'])
    add('Lemma2',[5],'Compatibility of reflexive tests under complementation','corrected_literal_statement',b,[],[], 'The congruence is sufficient only after one RLCD premise; C5/F2 refutes sufficiency alone.')
    add('Proposition2.1',[5],'Reflexive orthogonality implies full duality','proved_common_corollary',b,['ULCD.Reflexive'])
    add('Proposition2.2',[5],'Complement orthogonality and possible one-dimensional defect','strengthened_and_proved',b,['ULCD.Complement'],[], 'Exact nonzero constant-line defect when both degrees vanish; integral spectrum is unnecessary.')
    add('Lemma3',[6],'LCD rank from reduced integral spectrum with multiplicities','proved_common_corollary',b,['ULCD.Rank'])
    add('SubsetDefinitions',[6],'Uniform graphs, valency, incidence spaces and alternating transversal words','definitions_and_local_cancellation',d)
    add('SubsetAction',[6],'Natural Sn pair orbits are indexed by intersection size','qualified_action_statement',c,[],[], 'Sn is edge-transitive on each nonloop relation; a complement can contain several relations and reflexive loops form a separate orbit.')
    add('Result3.k3.1',[7],'p>=5,n=5 mod p,Kneser triple spaces, dimensions and distance assertions','mixed_proved_and_retained',d,['ULCD.SubsetFamilies','ULCD.Rank'],['earlier_incidence_code_descriptions','earlier_distances'])
    add('Result3.k3.2',[7],'p=2,n=1 mod4,Kneser triple spaces and parameters','mixed_proved_and_retained',d,['ULCD.SubsetFamilies','ULCD.Rank'],['earlier_incidence_code_descriptions','earlier_distances'])
    add('Result3.k3.3',[7],'p=3,n=5 mod9,Kneser triple space W2+<j> and parameters','corrected_dimension_with_retained_distances',d,['ULCD.TernaryKneser','ULCD.SubsetFamilies'],['earlier_distances'],'Correct dimensions binom(n,2), binom(n,3)-binom(n,2); not the printed +1/-1.')
    add('Result3.k3.4',[7],'p=2,n=0 mod4,intersection-one triple graph and W1 parameters','mixed_proved_and_retained',d,['ULCD.SubsetFamilies','ULCD.Rank'],['earlier_incidence_code_descriptions','earlier_distances'])
    add('Result3.k3.5',[7],'Binary odd-n Johnson triples, exact dual spaces, dimensions and distances','corrected_and_proved',d,['ULCD.Johnson','ULCD.SimplexMin'],[], 'W2 dimension is binom(n-1,2), not binom(n,2).')
    for residue in (3,1):
        add('Result3.k2.'+str(residue),[7],f'Binary n={residue} mod4 triangular/complement parameters','mixed_corrected_and_retained' if residue==3 else 'corrected_and_proved',d,['ULCD.Johnson','ULCD.SimplexMin','ULCD.Complement'],['earlier_distances'] if residue==3 else [], 'Reflexive triangular dimension is binom(n,2)-n+1; the n3mod4 Kneser distances remain retained, while the displayed space identities are proved.')
    add('Result4.rank',[7],'Point-incidence rank over every prime field','proved_with_explicit_domain',d,[],[], 'Requires 1<=k<n; literal all-n statement is not valid at k=n.')
    add('Result4.weights',[7],'Exact binary W1 weight values and multiplicities','corrected_and_proved',d,[],[], 'Divide by coefficient-fiber size and aggregate collisions; n8,k2,weight16 has35 words.')
    add('Result4.triple_minimum',[7],'Binary point-incidence minimum binom(n-1,2) on triples','retained_quoted_result',d,[],['earlier_distances'])
    add('Result5.minimum',[7],'Minimum n-k+1 for W(k-1), n>=2k+1','binary_proved_odd_characteristic_retained',d,['ULCD.SimplexMin'],['odd_characteristic_incidence_minima'])
    add('Result5.minimum_set',[7],'Stars up to nonzero scalar are the minimum words when n>2k+1','binary_proved_odd_characteristic_retained',d,['ULCD.SimplexMin'],['odd_characteristic_incidence_minima'])
    add('Result5.dimension',[7],'General lower rank bound, binary exact binom(n-1,k-1)','binary_proved_odd_characteristic_retained',d,['ULCD.Simplex'],['odd_characteristic_incidence_minima'])
    add('Example1',[8],'Explicit projection and nearest-word decoding for binary intersection-one triples','proved_with_retained_code_distance',d,['ULCD.Reflexive'],['earlier_distances'])
    add('Example1.question',[8],'Desire for a fast explicit coset-leader/decoder algorithm','source_recorded_question_not_resolved',d)
    finite=json.loads((HERE/'finite_subset_rows.json').read_text())
    for row in finite:
        key='.'.join(str(row[x]) for x in ('n','k','r','p'))
        add('Computational.'+key,[8],f'Exact reported dualities at (n,k,r,p)={key}','proved_by_displayed_scalar_counts',c,['ULCD.Scalar','ULCD.SubsetCounts'])
    add('SubsetSpectra',[8,9],'Kneser, Johnson, Eberlein spectra and multiplicities','retained_classical_input_explicit',c,[],['association_spectra'])
    for part in (1,2,3):
        add('Proposition3.'+str(part),[9],'Scalar intersection criteria: '+{1:'reflexive',2:'complementary',3:'complement reflexive'}[part], 'proved_common_corollary',c,['ULCD.Scalar','ULCD.SubsetCounts','ULCD.Complement'],[], 'All intersection indices must be realized; our complete five-family table uses n>=2k+1.')
    for name in ('Johnson','Kneser','intersection_one'):
        add('Example2.'+name,[10],name+' common-neighbour counts and complement tests','proved_common_substitution',c,['ULCD.SubsetCounts'])
    add('Corollary1.1',[10],'Johnson reflexive and complementary classification','qualified_domain_and_completed_defect',c,['ULCD.Scalar','ULCD.Complement'],[], 'n>=2k+1,k>=2; unrestricted endpoints are not covered by printed criterion, e.g. J(n,n-1)=Kn.')
    add('Corollary1.2',[10],'Odd-graph RLCD/CLCD exclusion','corrected_and_proved',c,['ULCD.Scalar'],[], 'No RLCD for k>=2; no CLCD for k>=3, but binary Petersen k2 is CLCD. k1 is complete-graph endpoint.')
    add('Corollary1.3',[10],'RLCD implies complement orthogonality; converse fails in general','proved_with_exact_degree_condition',c,['ULCD.Scalar'])
    for npar,kpar in (('odd','odd'),('odd','even'),('even','even'),('even','odd')):
        add('Result6.'+npar+'.'+kpar,[10],f'Binary Johnson decomposition for n {npar}, k {kpar}','proved_common_corollary',d,['ULCD.Johnson'])
    for k,r in ((2,0),(3,0),(4,0),(3,1),(4,1)):
        add(f'Classification.{k}.{r}',[10,11],f'Complete prime/residue RLCD and CLCD classification for (k,r)=({k},{r})','proved_common_classification',c,['ULCD.SubsetFamilies'],[], 'n>=2k+1; common finite polynomial/residue certificate is a retained required file, not a sampled inference.')
    for part in (1,2,3):
        add('Example3.'+str(part),[11],'Exact modular spectral dimension and stated row-weight upper bound','proved_application_of_retained_spectrum',c,['ULCD.Rank'],['association_spectra'])
    add('SRGSpectrum',[11,12],'General SRG eigenspectrum/multiplicities, complements and classical parameter alternatives','proved_trace_formulas_with_retained_feasibility',e,[],['classical_SRG_parameters'])
    add('TriangularSpectrum',[12],'Triangular and complementary spectra','corrected_by_literal_complement_operator',e,[],['association_spectra'], 'Complement entries are 3-m and1 on multiplicities m-1 and m(m-3)/2.')
    add('PaleySpectrum',[12],'Paley parameters and real spectrum; integral when q is square','retained_classical_input',e,[],['classical_SRG_parameters'])
    add('Proposition4.1',[12,13],'SRG reflexive congruences and dimension','proved_with_radical_sign_correction',e,['ULCD.SRG','ULCD.Rank'],[], 'Discriminant has +4(k-mu), not the printed minus.')
    add('Proposition4.2',[12,13],'SRG complement congruences and one-dimensional exception','strengthened_and_proved',e,['ULCD.SRG','ULCD.Complement'])
    add('Proposition4.exception',[13],'Triangular example really has constant-line defect','proved_with_minor_congruence_correction',e,['ULCD.Complement'],[], 'binom(m,2) is odd for m3mod4; source stronger modulus-four assertion is not uniform.')
    for part,name in ((1,'triangular/complement'),(2,'lattice/complement'),(3,'all Paley prime powers'),(4,'81,20,1,6')):
        add('Corollary2.'+str(part),[13],name+' exact reflexive conclusions and dimensions','proved',e,['ULCD.SRG','ULCD.Rank','ULCD.Complement'],['classical_SRG_parameters'], 'Paley rank uses self-complementarity and constant-line defect, so does not assume square q.' if part==3 else None)
    add('PetersenNote',[13],'Petersen is never RLCD','proved',e,['ULCD.SRG'])
    add('SymplecticExclusion',[13,14],'Symplectic graph and complement are never RLCD, nor CLCD','proved_directly_from_retained_parameters',e,['ULCD.SRG'],['classical_SRG_parameters'])
    add('SymplecticSpectrum',[13],'Nonconstant multiplicities for symplectic graph','corrected_trace_formula',e,[],['classical_SRG_parameters'], 'Use (N-1 +/- q^m)/2, not (mu-1 +/- q^m)/2.')
    add('GeneralizedPaleyDefinition',[14],'Connection subgroup, undirectedness, regular translation action','defined_and_proved',f)
    qs=[(25,3,2),(49,4,2),(81,4,2),(81,5,2),(121,3,2),(121,4,2),(121,4,3),(121,6,2),(243,11,2),(729,4,2),(729,7,2),(729,14,2)]
    for q,h,p in qs:
        add(f'Table1.{q}.{h}.{p}',[14],f'GP({q},{h}) over F{p}: exact SRG parameters, ranks, dualities and printed distance scope','proved_with_required_complete_finite_certificate',f,['ULCD.SRG','ULCD.Complement','ULCD.Rank','ULCD.TransitiveDistance','ULCD.MinimumEnumeration'],[], 'First eight rows have sixteen exact distances and five complete adjacency-row minimum sets; last four pairs only row upper bounds. GP81,4 degree201 corrected to20.')
    add('GeneralizedPaley.neighbours',[14],'Adjacent common-neighbour count |N(1) intersect S|','proved_multiplicative_symmetry',f)
    add('GeneralizedPaley.parity',[14],'Cited general oddness of lambda-mu for SRG index h>2','retained_quoted_observation_and_checked_for_table',f,[],['generalized_Paley_prior_observation'])
    add('Section6.binary_triples',[15],'Explicit unit-vector orthogonal split for odd-n binary Johnson triples','proved_common_corollary',g,['ULCD.Johnson'])
    add('Section6.ternary_triples',[15],'Unit-vector identity and orthogonal membership for n1mod3 ternary Kneser triples','local_identity_with_retained_memberships',g,[],['ternary_Prop18_memberships'])
    add('Section6.odd_graph',[15],'Binary all-k odd-graph LCD and explicit decomposition','corrected_formula_and_uniform_proof',g,['ULCD.Simplex','ULCD.Johnson','ULCD.Projector','ULCD.SimplexMin'],[], 'Printed k2 formula omits nonzero complementary term; theorem LCD is proved, not refuted.')
    add('Conclusion.even_cube',[15],'Binary d6,8,10 cube claim','corrected_to_self_duality',g,['ULCD.Cube'],[], 'Adjacency code self-dual; complement code is full, so printed complement-duality equality is false.')
    add('Conclusion.distance_two',[15],'Ternary H2(6,2) and H2(9,2) are RLCD','proved_uniform_family',g,['ULCD.HammingCounts','ULCD.Scalar'])
    add('Conclusion.odd_alphabet',[15],'Binary H1(6,3) and H2(6,3) are RLCD','proved_uniform_family',g,['ULCD.HammingOddAlphabet'])
    add('Conclusion.further_classes',[15],'Prospective further families and cited Hamming/McLaughlin research','historical_context_and_unresolved_beyond_explicit_families',g,[],[], 'No present-day open status or new question/priority credit is inferred.')
    add('References',[15,16,17],'Complete bibliography and historical publication-status context','attributed_context_not_claimed_reproved',g)
    return rows


def main():
    source=STUDY/'sources/lcd_followup2018.pdf'
    rows=source_rows()
    put('source_contract.json', {'original_id':'F017','authors':['J. D. Key','B. G. Rodrigues'],
        'title':'LCD codes from adjacency matrices of graphs','edition':'author manuscript dated 4 August 2017',
        'physical_pages':17,'source':{'path':'sources/lcd_followup2018.pdf',**digest(source)},
        'contract':'Complete principal assertions and explicit disposition of quoted ancillary results, corrections and questions.',
        'new_original_credit':0,'new_question_credit':0,'rows':rows})
    proof=[]
    for path in sorted((HERE/'sections').glob('*.tex')):
        lines=path.read_text().splitlines(keepends=True)
        proof.append({'id':path.stem,'path':str(path.relative_to(HERE)),'first_line':1,
                      'last_line':len(lines),**digest(path),
                      'source_rows':[r['id'] for r in rows if r['application_file']==str(path.relative_to(HERE))]})
    put('proof_map.json', {'exclusive_cost_partition':False,'full_contexts':proof,
                           'all_rows_have_current_context':True})
    packet_names=['topic_LCD_umbrella_v2','topic_LCD_umbrella_independent_review',
      'topic_LCD_umbrella_root_adoption','topic_LCD_projectors_bounded_review',
      'topic_LCD_simplex_candidate','topic_LCD_simplex_independent_review',
      'topic_LCD_ternary_kneser_candidate','topic_LCD_ternary_kneser_independent_review',
      'topic_LCD_ternary_kneser_root_adoption','topic_LCD_association_candidate',
      'topic_LCD_association_bounded_review','topic_LCD_transitive_distance_candidate',
      'topic_LCD_transitive_independent_review_v2','topic_LCD_common_root_adoption']
    packets=[{'path':name+'/manifest.json',**digest(STUDY/name/'manifest.json')} for name in packet_names]
    copied=[]
    specifications=[('topic_LCD_umbrella_v2','common',['umbrella.tex','umbrella.pdf','interface_labels.json']),
      ('topic_LCD_association_candidate','certificates/association',['check_association_counts.py','counts.json']),
      ('topic_LCD_transitive_distance_candidate','certificates/paley',
       ['check_paley_codes.py','enumerate_sparse_messages.c']+
       [str(p.relative_to(STUDY/'topic_LCD_transitive_distance_candidate')) for p in sorted((STUDY/'topic_LCD_transitive_distance_candidate/finite_records').glob('*'))]),
      ('topic_LCD_L050_F017_recovery','formal',['GraphCodeProjectors.lean','formal_scope.json']),
      ('topic_LCD_transitive_distance_candidate','formal/transitive',['TransitiveCodeBounds.lean','formal_scope.json'])]
    for old,new,names in specifications:
        for name in names:
            src=STUDY/old/name; dst=HERE/new/name
            dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
            copied.append({'origin':str(src.relative_to(STUDY)),'copy':str(dst.relative_to(HERE)),**digest(src)})
    retained={
      'association_spectra':{'source_refs':['[1]','[5]','[8]','[9]','[25]'],'statement':'Kneser/Johnson/Eberlein integral eigenvalues with binomial-difference multiplicities.','prior_full_proof_reproduced':False},
      'classical_SRG_parameters':{'source_refs':['[4]','[6]'],'statement':'Parameters for triangular, lattice, Paley and symplectic graphs; classical conference feasibility. Trace multiplicity formulas are proved locally.','prior_full_proof_reproduced':False},
      'earlier_incidence_code_descriptions':{'source_refs':['[11]','[14]','[16]','[17]','[21]','[22]','[23]'],'statement':'Exactly the non-simplex incidence identities quoted in Result3 and marked retained in application section4.','prior_full_proof_reproduced':False},
      'earlier_distances':{'source_refs':['[11]','[14]','[16]','[17]','[21]','[22]','[23]'],'statement':'Exactly the Result3 distances not covered by binary simplex, plus binary W1 triple minimum in Result4. In particular ternary distance8 is retained.','prior_full_proof_reproduced':False},
      'odd_characteristic_incidence_minima':{'source_refs':['[11]'],'statement':'Result5 odd-characteristic minimum, minimum-word and dimension-lower-bound clauses.','prior_full_proof_reproduced':False},
      'ternary_Prop18_memberships':{'source_refs':['[23] Proposition18'],'statement':'For n1mod3 ternary Kneser triples: intersection-one adjacency rows belong to C0, and j belongs to C0 or its dual. Local split identity and point-vector dual membership proved separately.','prior_full_proof_reproduced':False},
      'generalized_Paley_prior_observation':{'source_refs':['[27]'],'statement':'General quoted lambda-mu oddness for strongly regular index h>2; all twelve actual rows independently certified.','prior_full_proof_reproduced':False}}
    for v in retained.values(): v['full_proof_cost']=None; v['new_primary_acquisition']=False
    put('dependencies.json', {'common':{'path':'common/umbrella.tex','pdf':'common/umbrella.pdf',
      'whole_pages':14,'full_common_paid':True,'author':'root',
      'distinct_final_review':'accepted: topic_LCD_umbrella_independent_review',
      'root_adoption':'topic_LCD_umbrella_root_adoption/manifest.json',
      'root_adoption_sha256':'bd3cbb1d290568255d5dd693ec9f1550109c2e7d1f9896ea75b0a33b1ea6dc32'},
      'accepted_prior_packets':packets,'exact_copies':copied,'retained_classical_inputs':retained,
      'new_written_bridges':['coefficient-fiber weight enumerator with exact source correction',
        'nonsquare Paley ranks from self-complementarity and exact constant-line defect',
        'uniform odd-graph A^2=I+ud and Au=0, corrected orthogonal split',
        'all source-specific table/rank/congruence substitutions and literal correction bridges'],
      'roles':{'generic_common_author':'root','current_application_author':'enumeration_volume',
        'current_application_distinct_acceptance':False,
        'prior_author_role':'enumeration_volume independently reviewed the transitive packet; did not author its mathematical theorem or enumerator'},
      'no_sibling_application_premise':True,'external_unknowns':{'full_classical_proofs':None,'historical_software':None,'source_graphics':None,'full_Lean_formalization':None}})
    put('scope.json', {'status':'AUTHOR_COMPLETE_APPLICATION_PENDING_DISTINCT_REVIEW',
      'source_rows':len(rows),'common_pages':14,'application_pages':12,
      'whole_source_principal_contract':'claimed only with explicitly retained classical/earlier-code statements and exact corrections; awaits distinct review',
      'retained_input_ids':list(retained),'new_Lean_declarations':0,'reused_partial_Lean_declarations':9,
      'formal_full_source':False,'required_programs':['certificates/association/check_association_counts.py',
        'certificates/paley/check_paley_codes.py','certificates/paley/enumerate_sparse_messages.c'],
      'required_data':['certificates/association/counts.json','certificates/paley/finite_records/'],
      'optional_validation':['check_local_bridges.py','finite_subset_rows.json'],
      'operational_scripts':['check.py','prepare_metadata.py'],
      'source_program_boundary':'The full source was read: equations, finite result tables and decoding prose occur, but no executable program listing. Historical Magma code is not supplied and its cost is unknown.',
      'measurement_policy':'Any written comparison excludes executable code on both sides; required programs/data remain mathematical premises, fully inventoried. No factor computed.',
      'new_original_credit':0,'new_question_credit':0,'ratio':None,
      'source_questions':'General further families and efficient decoding questions remain unclaimed beyond the explicit proved families.'})
    print('rows',len(rows),'copies',len(copied),'prior packets',len(packets))


if __name__=='__main__':
    main()
