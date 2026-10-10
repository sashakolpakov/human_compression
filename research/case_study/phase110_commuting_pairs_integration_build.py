#!/usr/bin/env python3
"""Build a fresh complete manuscript and contract map; no overwrite is allowed."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
P = 'phase110_commuting_pairs_integration_'
BASE = 'phase78_n009_integration_manuscript.md'
BASE_SHA = '15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801'
LEDGER = 'phase78_n009_integration_ledger.json'
LEDGER_SHA = 'd1b08624baee1c2bf4a53dacc23d12643e6ee901a680fe039aa61a4899733367'
SOURCE_SHA = '788654bc5d015b72ad65819a848d78645a2e69fe940f44908b5d6452410fd134'

def need(ok, message):
    if not ok:
        raise RuntimeError(message)

def hs(text):
    return hashlib.sha256(text.encode()).hexdigest()

def binding(name):
    b = (ROOT/name).read_bytes()
    return dict(path=name,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

ITEMS = [
 ('Theorem 1.1',[1,4,5,6],True,'25.2','25.3','The exact symmetric floor formula for N=2n or 2n+1, n>1, with the N=6 value five.','full_principal'),
 ('Theorem 1.2',[2,7,8],True,'25.2','25.3','The exact alternating floor formula for N=2n or 2n+1, n>1, with the N=6 value one.','full_principal'),
 ('Proposition 3.1',[3],False,'25.1',None,'C_S_N(rho)=(C2 wreath S_k) times S_(N-2k) for an involution with k transpositions.','proved'),
 ('Lemma 3.2',[4],False,'25.2',None,'Ordered commuting distinct nonidentity involution conjugacy classes number sum(lambda(k)(n-k+1))-2n.','proved'),
 ('Lemma 3.3',[5],False,'25.2',None,'Reversal pairs the unequal-cycle ordered classes and fixes each equal-cycle ordered class.','valid_statement_repaired_proof'),
 ('Remark 3.4',[5],False,'25.2','25.4','The endpoint-pair reversal interpretation only; no inference that a completed triple is self-dual.','scoped_nonprincipal_remark'),
 ('Definition 3.5',[7],False,'25.3',None,'C-group IP and string commutation convention, already given in the shared manuscript.','definition'),
 ('Theorem 3.6',[7],True,'25.3',None,'Exactly two regular polyhedra with group S6 up to isomorphism and duality, of types {6,5} and {6,6}.','full_principal_computational'),
 ('Remark 3.7',[7],False,'25.4',None,'Historical attribution of the earlier computer classification to Leemans-Vauthier.','historical_attribution_not_new_result'),
 ('Proposition 4.1',[7],False,'25.1',None,'Alternating centralizer is the even subgroup of the symmetric centralizer, of order 2^(k-1) k! (N-2k)!.','proved'),
 ('Lemma 4.2',[8],False,'25.2',None,'Exact ordered-even S_(2n)-orbit formula mu(n).','proved'),
 ('Lemma 4.3',[8],False,'25.3',None,'A6 has exactly one unordered commuting-involution-pair orbit under its full automorphism group.','proved_computational'),
 ('Theorem 4.4',[9],True,'25.3','25.4','No abstract regular polyhedron has full automorphism group A6; regular scope of the source section retained.','full_principal_regular_scope'),
 ('Table 1',[2],False,'25.4',None,'All fourteen printed numerical rows including degrees below four and exceptional degree six.','proved_and_checked'),
 ('Equation (2)',[6],False,'25.3',None,'All five printed S6 endpoint representatives form a complete irredundant Aut(S6)-orbit list; exactly (2b),(2d) extend.','proved_computational'),
 ('Even/odd degree observation',[3],False,'25.2',None,'The same permutation-conjugacy counts occur in degrees 2n and 2n+1; ambient automorphism equivalence has its six-point exception.','proved')
]

def build():
    old = (ROOT/BASE).read_text()
    need(hs(old) == BASE_SHA,'Frozen predecessor mismatch')
    need(binding(LEDGER)['sha256'] == LEDGER_SHA,'Frozen predecessor ledger mismatch')
    s = old
    edits = []
    def replace(a,b,label):
        nonlocal s
        need(s.count(a) == 1,'Nonunique assembly anchor: '+label)
        s = s.replace(a,b)
        edits.append(dict(id=label,old_sha256=hs(a),new_sha256=hs(b)))
    replace('L035, F013, F016, L088, N013, N016, L108 and N009.',
            'L035, F013, F016, L088, N013, N016, L108, N009 and L066.','intake')
    replace('The full forest recognition, cyclic-core classification, model presentations,',
            'The finite-action extension of that same core formula classifies a permutation action by its orbit stabilizers, supplies its centralizer and normalizer twists, and turns evenness into a character equation. A configuration and its extension are enumerated by an orbit and then a stabilizer orbit. This gives the all-degree commuting-pair formulas, the complete exceptional polyhedron census, and the finite-image justification also used in the J1 residue census.\n\nThe full forest recognition, cyclic-core classification, model presentations,','intro_shared_action')
    core = (ROOT/(P+'core.md')).read_text()
    branch = (ROOT/(P+'branch.md')).read_text()
    replace('**Lemma O0 (chamber galleries and residue stabilizers).**',
            core+'\n**Lemma O0 (chamber galleries and residue stabilizers).**','K_e')
    replace('## 25. Every source result as an explicit corollary',
            branch+'\n## 26. Every source result as an explicit corollary','full_L066_branch')
    extra = '''**Corollary CP — L066 full principal contract.** For every n>1 the exact counts in its Theorems 1.1 and 1.2 are (CPI7) and (CPI9), except that degree six has five symmetric and one alternating class. Up to isomorphism and duality the only regular polyhedra with group S₆ have types {6,5} and {6,6}; none has group A₆.

*Proof.* Apply K(e) to the marked Klein four action; §§25.1–25.2 give the exact reversible adapter to the source floor sums. The retained ambient automorphism theorem identifies the nonexceptional equivalence. Apply K(e)'s invariant-fiber theorem to the complete Appendix I automorphism census and then the shared marked recognition to every survivor. Section 25.3 proves its exhaustiveness and verifies both source and polyhedron representatives. All necessary exceptional computation, as well as the optional arithmetic controls, is printed in Appendices I–K. ∎

'''
    replace('## 26. Shared proof, retained costs and source boundaries',
            extra+'## 27. Shared proof, retained costs and source boundaries','new_corollary')
    replace('A future common measurement must count all prose, code and mathematical data, charge wrappers/outputs consistently and declare every retained background.',
            'A future common measurement must count all prose, code and mathematical data, charge wrappers/outputs consistently and declare every retained background. The current L066 extension adds K(e), the complete §25 adapters, Appendix I finite census, Appendix J optional controls and Appendix K full new runner; all are charged. The predecessor twelve-source measurement is not a measurement of this enlarged text.','new_cost')
    replace('N009 is a new candidate intake with the complete corrected contract in §24; its addition awaits independent review of this assembly.',
            'N009 has its complete corrected contract in §24. Its predecessor assembly passed phase87 review; that review is inherited, while this L066 extension still awaits its own independent review.','old_status_boundary')
    appendices = ''
    for letter,title,name,lang in [
        ('I','Complete commuting-pair and polyhedron census','finite.g','gap'),
        ('J','Complete optional arithmetic and coordinate controls','formula.py','python'),
        ('K','Complete fresh commuting-pair replay runner','run.py','python')]:
        code = (ROOT/(P+name)).read_text()
        appendices += '## Appendix '+letter+'. '+title+'\n\nThe entire executable is charged; predecessor programs A–H remain unchanged.\n\n```'+lang+'\n'+code+'```\n\n'
    replace('## References and exact source versions',
            appendices+'## References and exact source versions','full_new_programs')
    s += '''
[KL13] A. Kiefer and D. Leemans, *On pairs of commuting involutions in Sym(n) and Alt(n)*, Communications in Algebra **41**(12) (2013), 4408–4418, DOI [10.1080/00927872.2012.701360](https://doi.org/10.1080/00927872.2012.701360). Contract: [nine-page author PDF](https://math.uni.lu/kiefer/Publications/Involutions.pdf), SHA256 `788654bc5d015b72ad65819a848d78645a2e69fe940f44908b5d6452410fd134`. Journal metadata was read from the archived institutional record; publisher full text was not compared. The source cites Suzuki, *Group Theory I* (1982), and Wilson, *The Finite Simple Groups* (2009), for standard permutation-group background. Their general automorphism theorems are retained in the precise nonexceptional form stated in §25.2; those books were not newly read for this extension. The source attributes an earlier computer polyhedron classification to D. Leemans and L. Vauthier, *An atlas of abstract regular polytopes for small groups*, Aequationes Mathematicae **72** (2006), 313–320. That older classification is not used as a proof input here.
'''
    ledger = copy.deepcopy(json.loads((ROOT/LEDGER).read_text()))
    prior = []
    for row in ledger['contracts']:
        span = row['integrated_proof_span']
        chunk = old[span['start_codepoint']:span['end_codepoint_exclusive']]
        need(hs(chunk) == span['sha256_utf8'],'Prior contract hash')
        need(s.count(chunk) == 1,'Prior contract absent or duplicated: '+row['integration_id'])
        a = s.index(chunk)
        row['previous_replacement_file'] = BASE
        row['previous_integration_proof_span'] = span
        row['replacement_file'] = P+'manuscript.md'
        row['integrated_proof_span'] = dict(start_codepoint=a,end_codepoint_exclusive=a+len(chunk),sha256_utf8=hs(chunk))
        prior.append(dict(id=row['integration_id'],sha256=hs(chunk)))
    for index,(name,pages,principal,section,second,target,status) in enumerate(ITEMS,1):
        start = s.index('### '+section+'.')
        last = second or section
        last_start = s.index('### '+last+'.')
        match = re.search(r'^##[#]? ',s[last_start+1:],re.M)
        end = last_start+1+match.start()
        ledger['contracts'].append(dict(integration_id='L066.'+str(index),paper='L066',source_reference=name,
            source_pdf='sources/catalogue_L066.pdf',source_pdf_sha256=SOURCE_SHA,printed_pages=pages,
            principal=principal,full_source_formulation_normalized=target,literal_or_scoped=status,
            replacement_file=P+'manuscript.md',integrated_proof_span=dict(start_codepoint=start,end_codepoint_exclusive=end,sha256_utf8=hs(s[start:end])),
            common_result=['K(c)','K(e)','CPI1–CPI12'],
            integration_status='author_assembled_pending_independent_review',full_dependency_closure_certified=False))
    ledger.update(schema='thirteen_source_commuting_pair_extension_contract_v1',
        candidate_source_ids=ledger['candidate_source_ids']+['L066'],source_count_admitted=0,ratio=None,
        status='author_assembly_pending_independent_review',manuscript=dict(path=P+'manuscript.md',sha256=hs(s)),
        new_source_complete_numbered_items=13,new_source_complete_tables=1,
        new_fresh_source_reading='Complete nine-page L066 author PDF text and all nine rendered pages, including bibliography',
        new_dependency_delta='Nonexceptional ambient automorphism theorem retained; centralizers proved via K(e); complete exceptional enumeration is new charged code, not retained classification')
    ledger['retained_background']['L066'] = [
        dict(id='L066-aut',statement='Aut(S_N) and Aut(A_N) are induced by S_N conjugation for N>=4,N!=6'),
        dict(id='L066-algorithms',statement='GAP exact finite-group, automorphism, orbit and subgroup algorithms'),
        dict(id='L066-polytope',statement='Existing marked string-C-group/regular-polytope correspondence; reversal is duality')]
    ledger['source_versions']['L066'] = dict(authors=['Ann Kiefer','Dimitri Leemans'],year=2013,
        title='On pairs of commuting involutions in Sym(n) and Alt(n)',edition='nine-page author PDF, undated within PDF; journal metadata 2013',
        primary_pdf='sources/catalogue_L066.pdf',sha256=SOURCE_SHA,publisher_fulltext_compared=False)
    ledger['common_core'].append(dict(id='Ke',statement='Orbit-stabilizer multiplicities, core kernel, centralizer/normalizer, sign character and invariant-fiber orbits',actual_users=['L066 all four principal results','L088 finite-image local subset enumeration and invariant extensions']))
    def section(text,n):
        return re.search(r'^## '+str(n)+r'\. .*?(?=^## |\Z)',text,re.M|re.S)[0]
    preserved = []
    for n in range(1,27):
        oldsec = section(old,n)
        if n != 2 and n < 25:
            need(oldsec == section(s,n),'Changed old whole section '+str(n))
            preserved.append(dict(section=n,sha256=hs(oldsec)))
    oldblocks = re.findall(r'^```(gap|python)\n(.*?)^```',old,re.M|re.S)
    blocks = re.findall(r'^```(gap|python)\n(.*?)^```',s,re.M|re.S)
    need(len(oldblocks) == 8 and len(blocks) == 11 and blocks[:8] == oldblocks,'Program continuity')
    assembly = dict(status='author_assembled_pending_independent_review',base=binding(BASE),
        base_ledger=binding(LEDGER),manuscript=dict(path=P+'manuscript.md',sha256=hs(s),bytes=len(s.encode())),
        edits=edits,all_120_prior_source_adapters_byte_identical=prior,hash_preserved_sections=preserved,
        code_appendices=[dict(language=lang,sha256=hs(code),bytes=len(code.encode())) for lang,code in blocks],
        old_eight_programs_byte_identical=True,contract_rows=len(ledger['contracts']),new_source_numbered_items=13,
        new_source_principal_results=4,new_source_table_rows=14,source_count_admitted=0,ratio=None)
    return {P+'manuscript.md':s,P+'ledger.json':json.dumps(ledger,indent=2,ensure_ascii=False)+'\n',
            P+'assembly.json':json.dumps(assembly,indent=2)+'\n'}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output_dir.exists(),'Refusing existing assembly directory')
    products = build()
    args.output_dir.mkdir(parents=True)
    for name,text in products.items():
        (args.output_dir/name).write_text(text)
    print(json.dumps(dict(status='BUILT',outputs=[dict(path=name,sha256=hs(text),bytes=len(text.encode())) for name,text in products.items()])))

if __name__ == '__main__':
    main()
