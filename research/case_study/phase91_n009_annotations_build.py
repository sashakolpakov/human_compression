#!/usr/bin/env python3
"""Rebase the reviewed phase79 attribution meanings onto reviewed phase78."""
import argparse
import copy
from hashlib import sha256
import json
from pathlib import Path
import re


def digest(data):
    return sha256(data).hexdigest()


def need(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    need(not args.output.exists() and not args.output.is_symlink(), 'output exists; refusing overwrite')
    base = args.study_root.resolve()
    hashes = {
        'phase79_eleven_attribution.json':'2a2e10a04f46e894738a9978e7ca91d10f7bbeff36d41e5929d304ef83e7708e',
        'phase85_eleven_attribution_recent_audit_manifest.json':'65f54ca3d2b030f2c70b3140d40a2c0ca85ff0b68db62312c0e5d6f6f06ca542',
        'phase78_n009_integration_manuscript.md':'15dd00e3845526dc40bb0effa07652e32748958238759eae9a856d901071b801',
        'phase78_n009_integration_manifest.json':'0705f2e8a1f27cc3f60a92a4076c4edcb98b4324fb6273232db1df0e7c1ea72a',
        'phase87_n009_integration_recent_audit_manifest.json':'c1638859cbc07b1136f132e3ccec82e75026278ad38a9e931cb95d0d5bc8fef9',
    }
    for name, expected in hashes.items():
        need(digest((base/name).read_bytes()) == expected, 'changed frozen input: '+name)
    old = json.loads((base/'phase79_eleven_attribution.json').read_text())
    reviewed = json.loads((base/'phase87_n009_integration_recent_audit_manifest.json').read_text())
    need('PASS' in reviewed['status'] and not reviewed['required_corrections'], 'phase87 is not a frozen PASS')
    for b in reviewed['files']:
        need(digest((base/b['path']).read_bytes()) == b['sha256'], 'changed review evidence: '+b['path'])
    proof = base/'phase78_n009_integration_manuscript.md'
    text = proof.read_text()
    def binding(name):
        data = (base/name).read_bytes()
        return dict(path=name,sha256=digest(data),bytes=len(data))
    heads = list(re.finditer(r'^## .+$',text,re.M))
    spans = {m.group()[3:]:(m.start(),heads[i+1].start() if i+1<len(heads) else len(text)) for i,m in enumerate(heads)}
    def anchor(row,start,end,prefix=None):
        snippet=text[start:end]
        row['anchor']=dict(start_codepoint=start,end_codepoint_exclusive=end,
                           exact_prefix=prefix or snippet.split('\n',1)[0],sha256_utf8=digest(snippet.encode()))
        nl=text.find('\n',start,end)
        row['insert_after_codepoint']=nl if nl>=0 else end
        return row
    notes=[]
    for original in old['notes']:
        row=copy.deepcopy(original)
        if row['id'] in ['K03','O00','E01']:
            prefix=original['anchor']['exact_prefix'];start=text.index(prefix)
            oldtext=(base/old['manuscript']['path']).read_text()
            snippet=oldtext[original['anchor']['start_codepoint']:original['anchor']['end_codepoint_exclusive']]
            need(text[start:start+len(snippet)]==snippet,'changed inherited inline note proof: '+row['id'])
            anchor(row,start,start+len(snippet),prefix)
        elif row['id']=='INTRO':
            anchor(row,0,heads[0].start())
        else:
            if row['id']=='S24':row['id']='S25';row['label']=row['label'].replace('24.','25.',1)
            elif row['id']=='S25':row['id']='S26';row['label']=row['label'].replace('25.','26.',1)
            elif row['id']=='APPA':row['label']='Appendix A. Complete rank/excess kernel enumeration'
            anchor(row,*spans[row['label']])
        notes.append(row)
    by={r['id']:r for r in notes}
    by['INTRO'].update(summary='The original authors retain credit for all twelve corrected principal contracts. The new rank/excess theorem and complete kernel ladder share one classification proof between L035 and N009; no twelve-source factor or historical novelty is claimed.',
                       borrowed_inputs=['The twelve intake manuscripts and their original authors; exact source versions remain in the references','Standard marked-group and coset-geometry language'],
                       repository_contribution='Organizes twelve scoped contracts around shared kernel, coordinate, retained-object, geometric and finite-kernel interfaces.')
    by['S01']['summary']='The retained-input inventory remains substantive. NQ and exact GAP algorithms now support the proved finite kernel search; SmallGroups completeness is removed. N009’s quoted geometric and infinite-decomposition theorems remain explicit imports.'
    by['S01']['borrowed_inputs'] += ['NQ universal nilpotent-quotient and exact GAP algorithms; TomLib J1 subgroup data remain retained', 'N009 quoted string-IP criteria, universal geometric interpretation, finite smooth-square classification and exceptional infinite marked decomposition']
    by['S02']['summary']='Upward lifting, downward image intersections, coset transport and retained-object actions are distinct interfaces. The sole Lean sign still covers only the named K(0) implication; K(d), K(c), O0 and geometric applications remain written mathematics.'
    by['S02']['repository_contribution']='States the separate exact-kernel interfaces once, with the inherited infinite-generation repair. K(c), K(d) and O0 have individual notes.'
    by['S02']['recovered_targets'] += ['N009 Lemmas 3.1–3.2 through K(d), with the displayed quotient marking']
    by['S11']['summary']='The canonical forest quotient bounds rank excess. Q5.5 and Q5.6 turn that bound into one exhaustive kernel classification for the L035 seed and all nondegenerate N009 ranks; the geometric covering correspondence remains retained.'
    by['S11']['repository_contribution']='Combines graded support, Boolean deletion, exact parabolic restriction and kernel-profile recognition with a proved invariant index-two ladder.'
    by['S11']['recovered_targets'] += ['L035 order-256 seed for all-parameter eight-family completeness','N009 order-1024 classification, ranks three through five']
    finite=[binding(n) for n in ['phase78_n009_integration_census.g','phase78_n009_integration_finite.g','phase78_n009_integration_data.g','phase87_n009_integration_recent_audit.json','phase87_n009_integration_recent_audit_replay/phase78_n009_integration_run.json','phase87_n009_integration_recent_audit_check.json']]
    by['S13'].update(markers=list('BIRV'),summary='The bounded seed is now generated by Q5.5/Q5.6, without a SmallGroups catalogue. Its four exact word-pattern implications feed the unchanged all-parameter lift proof; bare-presentation bounds remain necessary.',
                     borrowed_inputs=['Burnside and exact GAP/NQ algorithms; no abstract-group catalogue completeness'],
                     repository_contribution='Replaces the catalogue-relative seed by the same complete rank/excess search used for N009. Historical IDs and anchored multiplicities are unnecessary for the proved word implications.',
                     recovered_targets=['L035 Theorem 1.3, all eight bare presentations and converses','N009 rank/excess census shares the same generator and exhaustion proof'],finite_evidence=finite)
    by['S16']['summary']='The earlier four-source branch retains its exact corrections and local exclusions. Its N009 exclusion is local to that branch; N009 now has a separately proved complete corrected contract in section 24. No historical novelty is claimed.'
    by['S25']['summary']='These are explicit adapters for twelve qualified principal contracts. All 27 numbered N009 items and six tables are separately accounted for; retained, corrected and unproved rows are not newly rederived theorems.'
    by['S25']['borrowed_inputs'][0]='All twelve source manuscripts, with exact authors and editions in the references'
    by['S25']['recovered_targets'].append('N009 principal nondegenerate classification and constructive statements through N7 and section 24')
    by['S25']['correction'] += ' N009 keeps the order-eight descent boundary, displayed quotient marking, three Table 4 relator repairs and four Table 6 dual-orientation corrections.'
    by['S26']['summary']='No twelve-source length factor is assigned. All necessary branches and eight complete program/data blocks remain charged. The old SmallGroups seed import is removed; geometric, infinite-decomposition, GAP/NQ and TomLib inputs remain explicit.'
    by['S26']['repository_contribution']='Accounts for actual common theorem reuse, distinct source-specific proofs and complete execution/data costs. Earlier eleven-source length bounds and later cover results are not transferred.'
    by['APPA'].update(markers=list('BIRV'),summary='This complete parameterized program generates all invariant kernels from the proved finite universal bound. It tests 539,264 actual subset intersections, including rejected candidates, for the seed and three order-1024 ranks. Source totals never filter candidates.',
                      borrowed_inputs=['GAP 4.15.1 and NQ 2.5.11 exact algorithms; no SmallGroups catalogue or saved old census'],
                      repository_contribution='One executable implements Q5.5/Q5.6 and separately compares the kernel-profile test with every actual IP meet.',
                      recovered_targets=['L035 four required order-256 type-{4,8} seed implications','N009 complete ranks three, four and five census under marked reversal'],finite_evidence=finite)
    by['REFS']['summary']='Exact twelve-source versions and retained inputs delimit the contract. Original results retain their authors’ credit. Atlas presentations define marked labels; catalogue IDs are historical labels, not a completeness input. No factor or novelty follows from a citation.'
    def new(identifier,label,markers,summary,borrowed,contribution='',targets=None,correction=None,evidence=None):
        return dict(id=identifier,label=label,markers=list(markers),summary=summary,borrowed_inputs=borrowed,
                    repository_contribution=contribution,historical_novelty='not established',recovered_targets=targets or [],
                    correction=correction,lean=[],finite_evidence=evidence or [])
    kd=new('K04','K(d): exact intersections after a quotient','BIR',
           'Equality of quotient images is equivalent to the exact kernel intersection with the set product AB. Injectivity on both ends and a kernel contained in one end give distinct useful special cases; arbitrary quotients are not assumed to preserve IP.',
           ['Elementary homomorphism, subgroup and set-product arguments','N009 quotient-intersection targets'],
           'Adds the downward image-intersection criterion to the common kernel framework, with both directions proved for arbitrary subgroups.',
           ['N009 Lemma 3.1: quotient with kernel disjoint from the end product','N009 Lemma 3.2 and central descent: kernel contained in an end with its displayed marking'])
    start=text.index('**(d) Exact intersections after a quotient.**');end=text.index('### Marked torsors and geometric recognition',start)
    notes.append(anchor(kd,start,end))
    q=new('Q55','Q5.5–Q5.6: universal rank/excess kernel classification','BIRV',
          'The written finite nilpotent bound, exact parabolic kernel restrictions and invariant hyperplane ladder exhaust ordered IP markings at every forest rank/excess. The ladder also covers nonabelian kernels; path reversal gives the source generator-set equivalence.',
          ['Burnside basis theorem, lower-central graded Lie theory and finite two-group actions','NQ universal nilpotent-quotient and exact GAP algorithms'],
          'Proves a common complete finite search used for both the earlier seed and the new classification; the bound does not depend on the computation terminating.',
          ['L035 order-256 seed via (d,k)=(3,3)','N009 order-1024 ranks via (3,5),(4,3),(5,1)'],evidence=finite)
    start=text.index('### A single finite-kernel classification for every rank and excess');end=text.index('## 12.',start)
    notes.append(anchor(q,start,end))
    row=new('S24','24. Central quotients and the complete order-1024 classification','BIRCV',
            'Gomi–Loyola–De Las Peñas retain attribution for the original classification and constructions. K(d), the shared rank/excess ladder and square model recover the corrected contract, while complete source-specific central and presentation proofs remain charged.',
            ['Gomi–Loyola–De Las Peñas (2018), all 27 numbered items and six tables in the declared contract','Quoted string-IP criteria, universal geometric interpretation, finite smooth-square classification and Theorem 5.3 infinite marked decomposition','Primary Atlas presentations as exact label definitions; no Atlas completeness or abstract-group catalogue'],
            'Shares exact quotient transport, exhaustive kernels and affine centers; independently recognizes all finite presentations and named end groups.',
            ['N009 nondegenerate classes: one rank-two, 125 rank-three, 105 rank-four and eight rank-five','N009 central quotient/lift statements, all finite examples and 107 Table 6 rows'],
            'Descent stops at C2^3; quotient markings are the displayed ones. Three Table 4 second right-hand sides and four Table 6 right-hand orientations are corrected. Binary lift choices are not automatically successful. The infinite Theorem 5.3 remains retained, not finitely proved.',finite)
    notes.append(anchor(row,*spans[row['label']]))
    for identifier,label,summary,borrowed,targets in [
        ('APPF','Appendix F. Complete source presentation and marked-label recognition',
         'The full exact program completes 214 raw presentations and 43,840 further IP meets, checks 428 marked facet isomorphisms and every finite table/example adapter. The 106 finite universal rows have exact orders; the retained infinite row is excluded from finite enumeration.',
         ['Exact complete Todd–Coxeter and marked finite-group algorithms in GAP','Literal source and named Atlas presentation words'],
         ['N009 complete finite presentations and corrected Table 4 labels','All 107 Table 6 named rows and 106 finite universal orders']),
        ('APPG','Appendix G. All named presentation and source-table data',
         'All 72 named models and 107 Table 6 rows are printed. The independent review reparsed 572 complete defining words. Names and catalogue IDs identify marked presentations; they are not candidate filters or a completeness premise.',
         ['Primary Atlas defining presentations and N009 source tables, with the explicit orientation corrections'],
         ['N009 named facet and vertex-figure identifications','Literal and corrected presentation-table adapters']),
        ('APPH','Appendix H. Complete fresh mathematical replay runner',
         'The full runner generates its own census before presentation recognition, binds GAP 4.15.1/NQ 2.5.11 and preserves input hashes. This annotation reuses the frozen independent replay; it performs no new mathematical census.',
         ['Python process/file infrastructure and the explicitly bound GAP/NQ tools'],
         ['Exact reproducible common census','Exact finite source presentation and marked-name verification'])]:
        row=new(identifier,label,'BV',summary,borrowed,targets=targets,evidence=finite)
        notes.append(anchor(row,*spans[label]))
    notes.sort(key=lambda r:(r['insert_after_codepoint'],r['id']))
    need(len(notes)==41,'unexpected note count')
    inherited=copy.deepcopy(old['evidence'])
    evidence={r['path']:r for r in inherited}
    for name in [*hashes,'phase85_eleven_attribution_recent_audit.json','phase85_eleven_attribution_recent_audit.md',
                 'phase78_n009_integration_ledger.json','phase78_n009_integration_assembly.json',
                 'phase87_n009_integration_recent_audit.json','phase87_n009_integration_recent_audit.md']:
        evidence[name]=binding(name)
    result=dict(schema='hash_bound_manuscript_attribution.v1',date='2026-10-10',
                status='author_rebase_from_phase87_reviewed_proof_pending_independent_annotation_review',
                manuscript=binding(proof.name),erratum=None,
                scope=dict(source_count=12,required_erratum_incorporated=True,predecessor_editions_immutable=True,
                           new_notes_add_proof_steps=False,one_scoped_inherited_Lean_implication=True,
                           new_Kd_ladder_N009_Lean_certificate=False,twelve_measurement=None,
                           eleven_measurement_does_not_transfer=True,priority_or_open_conjecture_claim=False),
                evidence=list(evidence.values()),selected_inputs_are_not_complete_transitive_closure=True,
                annotations_add_mathematical_proof_content=False,quantitative_factor=None,
                previously_open_conjecture_cleared=False,whole_manuscript_Lean_certificate=False,
                rebase=dict(predecessor_sidecar_sha256=hashes['phase79_eleven_attribution.json'],
                            independent_proof_review_sha256=hashes['phase87_n009_integration_recent_audit_manifest.json'],
                            old_S24_now='S25',old_S25_now='S26',new_notes=['K04','Q55','S24','APPF','APPG','APPH'],
                            changed_existing_notes=['INTRO','S01','S02','S11','S13','S16','S25','S26','APPA','REFS'],
                            SmallGroups_completeness_removed=True,catalogue_identifiers='historical labels only; not candidate-generation inputs'),notes=notes)
    with args.output.open('x',encoding='utf-8') as stream:
        json.dump(result,stream,ensure_ascii=False,indent=2);stream.write('\n')
    print(json.dumps(dict(sidecar_sha256=digest(args.output.read_bytes()),notes=len(notes)),indent=2))


if __name__=='__main__':
    main()
