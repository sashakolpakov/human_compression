#!/usr/bin/env python3
"""Assemble a new private Petrial extension; never overwrite an output."""
from pathlib import Path
import copy
import hashlib
import json
import re

P = Path(__file__).resolve().parent
SHA = lambda b: hashlib.sha256(b).hexdigest()
BASE_SHA = 'f7d66e2b0b67da95e1d345fd47cd9e86c03a4309ca38ab9c8b18dd58a0f475fa'
BASE = 'phase45_ten_source_manuscript.md'
OUT = 'phase65_petrial_integration_manuscript.md'


def binding(name):
    data = (P / name).read_bytes()
    return {'path': name, 'sha256': SHA(data), 'bytes': len(data)}


def main():
    outputs = [OUT, 'phase65_petrial_integration_ledger.json',
               'phase65_petrial_integration_assembly.json']
    for name in outputs:
        if (P / name).exists():
            raise FileExistsError(name)
    base = (P / BASE).read_text()
    assert SHA(base.encode()) == BASE_SHA
    text = base
    edits = []

    def replace(old, new, reason):
        nonlocal text
        assert text.count(old) == 1, (reason, text.count(old))
        edits.append({'reason': reason, 'old_sha256': SHA(old.encode()),
                      'new_sha256': SHA(new.encode()),
                      'old_codepoints': len(old), 'new_codepoints': len(new)})
        text = text.replace(old, new)

    def between(start, end, new, reason):
        a = text.index(start)
        b = text.index(end, a)
        replace(text[a:b], new, reason)

    replace('L035, F013, F016, L088, N013 and N016.',
            'L035, F013, F016, L088, N013, N016 and L108.', 'intake extension')
    old = "N013's rank-three exception and N016's nonidentity-power wording. L108's\nPetrial paper remains outside the intake because its set-valued operation can\nlose faithfulness. No open conjecture, new priority claim, or Lean verification\nof the complete geometry is asserted."
    new = "N013's rank-three exception and N016's nonidentity-power wording. L108's\nPetrial operation is now handled with its exact action kernel: the source's\nunconditional embedding is corrected, while its principal obstruction and\nvalid numbered structural conclusions are proved in Section 23. No open\nconjecture, new priority claim, or Lean verification of the complete geometry\nis asserted."
    replace(old, new, 'corrected Petrial scope in introduction')
    needle = 'The full forest recognition, cyclic-core classification, model presentations,'
    replace(needle, "A further operation keeps actual subsets of retained objects rather than\nlabelled copies of walks. The common retained-object theorem identifies its\nexact permutation kernel and also supplies the old coset-core identity and\nthe endpoint operation's faithfulness. Thin Petrials still require their own\nresidue-cycle and face-shadow proofs; a general matrix change is not a\nsubstitute for these hypotheses.\n\n" + needle, 'new shared idea, with actual distinct cost')
    replace('**Theorem K (intersection transport and exact coset transport).**',
            '**Theorem K (intersection transport, exact coset transport and retained-object operations).**',
            'general interface title')
    core = (P / 'phase65_petrial_integration_core.md').read_text().rstrip()
    replace('### Marked torsors and geometric recognition',
            core + '\n\n### Marked torsors and geometric recognition', 'proved common kernel/gallery interface')
    old = 'The chamber graph is connected because the markers generate G. A type-preserving automorphism fixing one chamber fixes its unique neighbour across each panel, and consequently every chamber. Thus the full automorphism group acts freely on chambers, and the already regular G-action is the full group.'
    replace(old, 'Lemma O0 now identifies the already regular G-action with the full type-preserving automorphism group.',
            'recognition uses shared chamber lemma')
    old = 'Moreover the kernel of the action on all typed cosets is'
    replace(old, 'Applying K(c) with X=Y the typed coset objects gives the kernel',
            'coset-core identity specializes shared operation theorem')
    old = 'It is the largest normal subgroup of \\(G\\) contained in \\(B\\); transport through that kernel yields the faithful action.'
    replace(old, 'It is the core from (Kc2); K(b) transports through it to the faithful action.',
            'remove duplicate core explanation')
    start = 'Here is the connectivity fact being used. The chamber graph'
    end = '\n\nFor a connected graph Q'
    replacement = ('Lemma O0 supplies connected chamber galleries in every residue. Restricting a gallery to any set of at least two types shows that its truncation is connected, since successive complete incidence subgraphs overlap. Apply this inside the residue at F; chamber extension supplies an edge. The edge-shadow hypothesis says Q_F is the induced graph on its common vertices.')
    between(start, end, replacement, 'endpoint connectivity uses common gallery lemma')
    old = 'The action is faithful: fixing new objects fixes old vertices and higher objects, and simplicity then fixes every edge. '
    replace(old, '', 'faithfulness moved to exact common-kernel application')
    old = 'Its color-preserving subgroup therefore has index two and is transitive on the selected chambers, with the same faithfulness proof. ∎'
    new = ('Its color-preserving subgroup therefore has index two and is transitive on the selected chambers.\n\n'
           'For faithfulness apply K(c) to this actual acting group, retaining X consisting of old vertices and all old higher objects. A new vertex is encoded by its old vertex and its color; (x,C_x) is encoded by x and the two old-vertex subsets of C_x. These data determine the component, because the double-cover graph is fixed. Forgetting the color or component maps onto X: when Q is nonbipartite all lifts lie in C, while in the bipartite case C has one lift of every old vertex and one compatible component of every connected Q_x. Thus the encoding and surjection hypotheses hold. An element fixing X fixes every old edge by simplicity, so acts trivially on Γ and is the identity. K(c) therefore proves faithfulness. ∎')
    replace(old, new, 'endpoint exact encoding/surjection membership check')
    erratum = json.loads((P / 'phase45_ten_source_errata.json').read_text())
    for row in erratum['changes']:
        replace(row['old'], row['new'], 'incorporate approved source-reference erratum')
    branch = (P / 'phase65_petrial_integration_branch.md').read_text().rstrip()
    replace('## 23. Every source result as an explicit corollary',
            branch + '\n\n## 24. Every source result as an explicit corollary', 'complete new Petrial branch')
    z3 = '''**Corollary Z3 — L108's corrected principal contract.** A thin regular residually connected rank-three geometry with thin Petrial has a commuting pair in its diagram. Its Petrial is residually connected; under thinness it has the same full regular automorphism group and its second Petrial recovers the original geometry. The map walk is the usual Petrie walk. Unconditionally the natural action has kernel core_G(⟨a⟩), rather than necessarily being an embedding.

*Proof.* Lemma P1 supplies residual connectivity and the exact kernel through K(c). Theorem P2 proves the obstruction, faithfulness and biduality without finite-group assumptions. The explicit three-step walk in §23.1 proves source Lemma 3.1. Section 23.3 proves why the unconditional source inclusion and length/order equality cannot be counted as literal rederivations. These are Theorem 1 and the valid numbered conclusions of Lemma 3.2, with its part (ii) expressly corrected. ∎

'''
    replace('## 24. Shared proof, retained costs and source boundaries',
            z3 + '## 25. Shared proof, retained costs and source boundaries', 'explicit new corollary and section sequence')
    old = 'The necessary finite programs are printed in full in Appendices A–D.'
    replace(old, 'The necessary finite programs are printed in full in Appendices A–D. The optional Petrial controls are also fully charged in Appendix E; their finite output is not a substitute for the uniform proof.',
            'full fifth program cost disclosed')
    start = 'L108 remains excluded: its Petrial objects'
    end = "Ens's full\ntoroidal classification"
    a = text.index(start)
    b = text.index(end, a)
    replace(text[a:b], "L108's set-valued operation is included with the exact K(c) kernel and the corrected §23 contract; its former exclusion in the ten-source assembly remains part of that earlier frozen record. The current branch uses no atlas or map classification. ", 'remove obsolete exclusion without erasing historical boundary')
    replace('The new integration reading\nlog distinguishes complete component proofs from inherited primary\nreadings.',
            'L108 uses the complete seven-page authored browser rendering corresponding to its 2001 publication, without a primary PDF. This extension freshly read that complete text and the complete phase25 proof, checker, contract and independent review; it inherits unchanged earlier source readings.',
            'precise new source reading scope')
    marker = '\n## References and exact source versions'
    if marker not in text:
        marker = '\n## References and source versions'
    if marker not in text:
        marker = '\n## References'
    code = (P / 'phase65_petrial_integration_check.py').read_text()
    appendix = '''
## Appendix E. Complete Petrial operation and kernel controls

This standard-library program constructs the geometry and its actual set-valued Petrial from explicit permutations. It checks all finite incidence/residue conditions, both branches of the face-stabilizer split, the exact action kernel against the intersection of conjugates, the central-involution criterion and thin-case bidual shadows. The two source boundaries and every general theorem already have full proofs in §23. The program is a strengthened, fully charged version of the phase25 checker; its seven examples are not a census.

```python
''' + code.rstrip('\n') + '\n```\n'
    replace(marker, appendix + marker, 'complete fifth executable appendix')
    text += '''

[BBL01] D. Bonheure, F. Buekenhout and D. Leemans, *On the Petrials of thin rank 3 geometries*, Journal of Geometry **71** (2001), 19–25, DOI 10.1007/s00022-001-8548-2. Target version: complete seven-page authored rendering hosted at the coauthor-linked Academia article; primary PDF unavailable. The source operation and targets are attributed to this work. Its unconditional embedding and length/order assertions are corrected in §23, without a historical-priority claim.

The new retained-object interface K(c) and its coset/endpoint/Petrial applications are explicit integration arguments; no claim of historical originality is made for the elementary ingredients. The two-branch corrected Petrial proof was developed and independently reviewed in the earlier phase25 component and is reproved here using the common interface. The phase45 reference erratum is incorporated in this new manuscript: the citation after O4.1 is to N013's quoted Theorem 2.2. No frozen predecessor is altered.
'''
    assert re.findall(r'^## (\d+)\.', text, re.M) == [str(i) for i in range(1, 26)]
    tags = re.findall(r'\\tag\{([^}]+)\}', text)
    assert len(tags) == len(set(tags))
    assert len(re.findall(r'```gap\n', text)) == 4
    assert len(re.findall(r'```python\n', text)) == 1
    assert (re.findall(r'```python\n(.*?)\n```', text, re.S)[0] + '\n').encode() == code.encode()

    oldledger = json.loads((P / 'phase45_ten_source_adapter_map.json').read_text())
    ledger = copy.deepcopy(oldledger)
    ledger.update(schema='eleven_source_Petrial_extension_contract_v1',
                  status='author_complete_pending_independent_extension_review',
                  source_count_admitted=False, ratio=None)
    ledger['candidate_source_ids'].append('L108')
    ledger['excluded'] = [x for x in ledger['excluded'] if not x.startswith('L108')]
    ledger['source_versions']['L108'] = json.loads((P / 'phase25_L108_intake.json').read_text())['source']
    unchanged_contracts = []
    corrected_contracts = []
    for row in ledger['contracts']:
        span = row['integrated_proof_span']
        snippet = base[span['start_codepoint']:span['end_codepoint_exclusive']]
        assert SHA(snippet.encode()) == span['sha256_utf8']
        replacement = snippet
        for change in erratum['changes']:
            replacement = replacement.replace(change['old'], change['new'])
        assert text.count(replacement) == 1, row['integration_id']
        a = text.index(replacement)
        row['previous_integration_proof_span'] = span
        row['previous_replacement_file'] = row['replacement_file']
        row['replacement_file'] = OUT
        row['integrated_proof_span'] = {'start_codepoint': a, 'end_codepoint_exclusive': a+len(replacement),
                                        'sha256_utf8': SHA(replacement.encode())}
        row['extension_status'] = 'pending_independent_review; previous_ten_source_contract_review_retained'
        (unchanged_contracts if replacement == snippet else corrected_contracts).append(row['integration_id'])

    intake = json.loads((P / 'phase25_L108_intake.json').read_text())
    target_rows = intake['numbered_statements'] + intake['other_scope_records'][:2]
    a = text.index(branch)
    pspan = {'start_codepoint': a, 'end_codepoint_exclusive': a+len(branch),
             'sha256_utf8': SHA(branch.encode())}
    primary = (P / intake['source_asset']['path']).read_text()
    assert SHA(primary.encode()) == intake['source_asset']['sha256']
    line_ranges = {'Theorem 1':(8,9), 'Lemma 3.1':(20,24),
                   'Lemma 3.2(i)':(25,28), 'Lemma 3.2(ii)':(25,28),
                   'Lemma 3.2(iii)':(25,30), 'Lemma 3.2(iv)':(25,31),
                   'Unnumbered converse boundary':(9,9),
                   'Unnumbered geometric length/order assertion':(25,25)}
    for i, target in enumerate(target_rows, 1):
        l0,l1 = line_ranges[target['id']]
        ss = primary.index(f'L{l0}:')
        ee = primary.index(f'L{l1+1}:')
        normalized = target.get('exact_target', target.get('adapter'))
        if i == 7:
            normalized = 'A linear diagram does not imply that the Petrial is thin.'
        if i == 8:
            normalized = 'The geometric Petrie length equals the order of the chamber-step element cab.'
        ledger['contracts'].append({
            'integration_id': f'PET.{i}', 'paper': 'L108', 'source_reference':target['id'],
            'full_source_formulation_normalized':normalized,
            'principal_source_result':i == 1,
            'source_statement_reproduced_verbatim':False,
            'source_file':intake['source_asset']['path'],
            'source_span':{'start_codepoint':ss,'end_codepoint_exclusive':ee,'sha256_utf8':SHA(primary[ss:ee].encode()),'displayed_lines':[l0,l1]},
            'previous_component_status':target['status'],
            'integration_status':'author_proved_corrected_contract_pending_independent_review',
            'literal_or_scoped': 'corrected_not_literal' if i in [4,8] else 'stated_scope_with_thin_only_strengthening_for_Theorem1',
            'common_result':['K(c)','O0','P1','P2'],
            'replacement_file':OUT,'integrated_proof_span':pspan,
            'selected_imported_inputs':['elementary group actions','conventional map/Petrie-walk definition'],
            'new_substantial_classification_input':False,
            'infinite_group_scope':True,
            'finite_controls_are_uniform_proof':False,
            'historical_priority_claim':False})
    ledger['source_versions']['L108']['reading'] = 'Fresh complete saved seven-page primary authored rendering read in phase65; original PDF not acquired.'
    ledger['fresh_integration_reading'] = {
        'complete':['sources/phase25_L108_rendered_primary.txt','phase25_L108_reduction.md','phase25_L108_intake.json','phase25_L108_rank_audit.md','phase25_L108_check.py'],
        'new_complete_proof':['phase65_petrial_integration_core.md','phase65_petrial_integration_branch.md'],
        'selected_fresh_earlier_sections':[1,2,18,19,23,24],
        'inherited_unchanged':'Approved ten-source source/proof contracts; no new full reading of all ten primary papers claimed',
        'not_claimed':['L108 primary PDF reading','retained older classifications newly reproved','historical priority search']}
    ledger['common_core'].extend([
        {'id':'Kc','statement':'Injective equivariant encoding from retained objects, with a surjective forgetting map, preserves exactly the retained-object action kernel; this is the intersection of stabilizer cores. Thin chamber-transitive outputs give the full faithful image and a panel-index test.',
         'proof_to_include':'Complete elementary proof and all application-specific encoding/surjectivity conditions in this manuscript',
         'actual_users':['N008 action core','N013 endpoint faithfulness','L108 exact kernel and thin-case faithfulness']},
        {'id':'O0','statement':'Chamber galleries, free automorphism action for thin geometries, and exact residue-stabilizer generation.',
         'proof_to_include':'Finite-rank induction and gallery words, allowing infinite groups',
         'actual_users':['O1 geometric recognition','O3 endpoint connectivity','L108 original stabilizers and thin output']}])
    ledger['necessary_distinct_branches'].append('Petrial two-case residue obstruction and injectivity of old face shadows')
    ledger['integration_proof_changes'] = edits
    ledger['component_bindings'] += [binding(n) for n in ['phase45_ten_source_manuscript.md','phase45_ten_source_errata.json','phase52_ten_source_recent_audit.json','phase25_L108_reduction.md','phase25_L108_intake.json','phase25_L108_rank_audit.md']]
    ledger['manuscript'] = {'path': OUT, 'sha256': SHA(text.encode()), 'bytes':len(text.encode())}

    def sections(body):
        matches=list(re.finditer(r'^## (\d+)\. ',body,re.M)); out={}
        for i,m in enumerate(matches):
            end=matches[i+1].start() if i+1<len(matches) else body.index('## Appendix A.',m.start())
            out[int(m.group(1))]=body[m.start():end]
        return out
    os,ns=sections(base),sections(text)
    unmodified=[i for i in range(1,23) if os[i]==ns[i]]
    assert all(i in unmodified for i in list(range(1,2))+list(range(3,18))+[20,21,22])
    programs=[]
    for lang in ['gap','python']:
        for block in re.findall('```'+lang+r'\n(.*?)\n```',text,re.S):
            programs.append({'language':lang,'bytes':len((block+'\n').encode()),'sha256':SHA((block+'\n').encode())})
    assembly={'status':'author_complete_pending_independent_extension_review',
              'base':binding(BASE),'approved_reference_erratum':binding('phase45_ten_source_errata.json'),
              'manuscript':ledger['manuscript'],'edits':edits,
              'hash_preserved_sections':{str(i):SHA(os[i].encode()) for i in unmodified},
              'earlier_contract_spans_byte_unchanged':unchanged_contracts,
              'earlier_contract_spans_only_approved_erratum_applied':corrected_contracts,
              'old_contract_count':79,'new_contract_count':len(ledger['contracts']),
              'source_count_admitted':False,'ratio':None,
              'code_appendices':programs,
              'new_raw_utf8_byte_delta':len(text.encode())-len(base.encode()),
              'new_raw_byte_delta_is_not_a_compression_metric':True,
              'source_PDF_available_for_new_L108':False,
              'all_old_four_GAP_programs_unchanged':re.findall(r'```gap\n(.*?)\n```',base,re.S)==re.findall(r'```gap\n(.*?)\n```',text,re.S),
              'new_source_claims_corrected_not_imported':True,
              'new_proofs_allow_infinite_groups':True}
    payloads={OUT:text,'phase65_petrial_integration_ledger.json':json.dumps(ledger,indent=2,ensure_ascii=False)+'\n',
              'phase65_petrial_integration_assembly.json':json.dumps(assembly,indent=2,ensure_ascii=False)+'\n'}
    for name,body in payloads.items():
        with (P/name).open('x',encoding='utf-8') as stream:stream.write(body)
    print(json.dumps({'manuscript_sha256':SHA(text.encode()),'bytes':len(text.encode()),'contracts':len(ledger['contracts']),
                      'unchanged_sections':unmodified,'old_contract_spans_unchanged':len(unchanged_contracts),
                      'approved_erratum_only_spans':len(corrected_contracts),'new_code_appendices':programs},indent=2))


if __name__=='__main__':
    main()
