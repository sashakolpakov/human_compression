#!/usr/bin/env python3
"""Rebase the reviewed ten-source attribution onto the reviewed extension."""
import argparse
import copy
from hashlib import sha256
import json
from pathlib import Path
import re


def digest(data):
    return sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study-root', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.is_symlink():
        raise ValueError('output exists; refusing overwrite')
    base = args.study_root
    oldpath = base/'phase61_ten_source_attribution.json'
    old = json.loads(oldpath.read_text())
    if digest(oldpath.read_bytes()) != '81b5a0606a1e20824260cfe37c6785e7cf5c33efc56af11a7ab70b9cdeb8fa54':
        raise ValueError('changed reviewed predecessor sidecar')
    proofpath = base/'phase65_petrial_integration_manuscript.md'
    if digest(proofpath.read_bytes()) != '6d302a2e7c696c916de97d2deef409c3053879999539be99a3fe72c9506205a1':
        raise ValueError('changed reviewed manuscript')
    text = proofpath.read_text()

    def binding(name):
        data = (base/name).read_bytes()
        return {'path':name, 'sha256':digest(data), 'bytes':len(data)}

    headings = list(re.finditer(r'^## .+$', text, re.M))
    spans = {m.group(0)[3:]:(m.start(),headings[i+1].start() if i+1<len(headings) else len(text)) for i,m in enumerate(headings)}

    def anchor(row, start, end, prefix=None):
        snippet = text[start:end]
        row['anchor'] = {'start_codepoint':start, 'end_codepoint_exclusive':end,
                         'exact_prefix':prefix or snippet.split('\n',1)[0], 'sha256_utf8':digest(snippet.encode())}
        first_newline = text.find('\n',start,end)
        row['insert_after_codepoint'] = first_newline if first_newline>=0 else end
        return row

    notes = []
    for source in old['notes']:
        row = copy.deepcopy(source)
        if row['id']=='E01':
            continue
        if row['id']=='INTRO':
            anchor(row,0,headings[0].start())
        else:
            if row['id']=='S23': row['id']='S24';row['label']=row['label'].replace('23.','24.',1)
            elif row['id']=='S24': row['id']='S25';row['label']=row['label'].replace('24.','25.',1)
            anchor(row,*spans[row['label']])
        notes.append(row)
    byid = {r['id']:r for r in notes}
    intro = byid['INTRO']
    intro['summary']='The intake authors retain credit for their results. This exposition joins eleven corrected principal contracts; no eleven-source factor, historical novelty or newly solved open conjecture is claimed.'
    intro['borrowed_inputs'][0]='The eleven intake manuscripts and their original authors; see exact-version references'
    intro['repository_contribution']='Organizes the eleven scoped contracts around shared kernel, coordinate, retained-object and geometric interfaces.'
    s2=byid['S02']
    s2['summary']='Distinct lifting, coset-transport and retained-object interfaces serve the adapters. Lean covers only the named K(0) lifting implication; K(c), O0 and their applications remain written mathematics. The infinite converse has a corrected hypothesis.'
    s2['repository_contribution']='States the separate exact-kernel interfaces once and makes the infinite-scope repair explicit. K(c) and O0 receive their own notes below.'
    s18=byid['S18']
    s18['summary']='Typed Helly remains separate from subgroup IP. The retained-object theorem now proves faithfulness for the actual endpoint action after its encoding, surjection and simple-graph hypotheses are checked.'
    s18['repository_contribution']='Shares O0 for the connected galleries and K(c) for the endpoint action kernel; the double-cover geometry and typed-Helly proof remain necessary.'
    s24=byid['S24']
    s24['summary']='These are the explicit source corollaries for all eleven principal contracts. Source corrections and retained inputs govern the arrows; corrected assertions and unproved ledger rows are not literal recovered theorems.'
    s24['borrowed_inputs'][0]='All eleven source manuscripts, with exact authors and editions in the references'
    s24['recovered_targets'].append('L108 Theorem 1 and valid Lemmas 3.1–3.2 conclusions via P1/P2; Lemma 3.2(ii) corrected')
    s24['correction']='The earlier corrected scopes remain. L108 unconditional embedding is replaced by the exact action kernel; its geometric length/order equality is not recovered literally.'
    s25=byid['S25']
    s25['summary']='No eleven-source numerical ratio is assigned. Every necessary branch and all five programs remain charged; no open-conjecture or historical-novelty credit is claimed.'
    s25['repository_contribution']='Makes shared proof cost, necessary distinct branches, corrected contracts and excluded targets explicit, including the full Petrial branch.'
    byid['REFS']['summary']='The exact eleven source versions delimit the contracts. Original results retain their authors’ credit; bibliographic presence grants neither numerical compression nor historical novelty.'

    def newnote(identifier,label,markers,summary,borrowed,contribution='',targets=None,correction=None,evidence=None):
        return {'id':identifier,'label':label,'markers':list(markers),'summary':summary,
                'borrowed_inputs':borrowed,'repository_contribution':contribution,'historical_novelty':'not established',
                'recovered_targets':targets or [],'correction':correction,'lean':[],'finite_evidence':evidence or []}

    kcstart=text.index('**(c) Retained-object operations and the faithful image.**')
    ostart=text.index('**Lemma O0 (chamber galleries and residue stabilizers).**')
    # End exactly at the independently bound O0 paragraph, not its next heading.
    priorattr=json.loads((base/'phase65_petrial_integration_attribution.json').read_text())
    osp=next(r['span'] for r in priorattr['entries'] if r['kind']=='integration_argument' and r['item'].startswith('O0'))
    oend=osp['end_codepoint_exclusive']
    kc=newnote('K03','K(c): retained objects and the faithful image','BIR',
       'The actual subset encoding and an equivariant forgetting map identify the exact action kernel. This same proof is applied to typed cosets, endpoint halving and Petrials; it is not a homomorphism between changed markings.',
       ['Elementary permutation actions, subgroup cores, first isomorphism and orbit–stabilizer facts',
        'Archer–Cara–Krempa coset-action kernel and Bonheure–Buekenhout–Leemans Petrial targets'],
       'Proves a common retained-object interface, including the infinite-group panel-index argument; checks the concrete encoding and surjection in each application.',
       ['N008 faithful coset-image calculation in section 2', 'N013 endpoint geometry faithfulness in section 18', 'L108 exact kernel and thin-case full action in section 23'])
    notes.append(anchor(kc,kcstart,ostart))
    oo=newnote('O00','O0: chamber galleries and residue stabilizers','BIR',
       'For thin residually connected geometries of finite rank, the gallery proof gives free chamber actions; a chamber-transitive subgroup is then the full regular group with the stated residue stabilizers. Object sets and groups may be infinite.',
       ['Standard chamber-gallery and thin-geometry arguments; elementary involution and group-action facts'],
       'Prints the shared gallery proof once and uses it in coset recognition, endpoint connectedness and Petrial recovery.',
       ['O1.1 coset recognition and full automorphism group', 'N013 connected endpoint truncations', 'L108 residue generators, thin action and obstruction'])
    notes.append(anchor(oo,ostart,oend))
    pevidence=[binding('phase65_petrial_integration_check.py'),binding('phase70_petrial_integration_recent_audit.json'),binding('phase70_petrial_integration_recent_audit_controls.json')]
    pet=newnote('S23','23. Set-valued Petrials: the exact kernel and thin-case recovery','BIRCV',
       'The original Petrial operation and principal conclusions retain Bonheure–Buekenhout–Leemans attribution. K(c)/O0 plus the two-case residue argument recover the valid conclusions, including infinite cases; two unconditional auxiliary assertions are corrected.',
       ['Bonheure–Buekenhout–Leemans (2001), L108: set-valued Petrial definition, Theorem 1 and Lemmas 3.1–3.2',
        'Conventional map/Petrie-walk definition and elementary dihedral normal forms'],
       'Integrates the previously reviewed corrected proof through the shared kernel and gallery interfaces. It proves residual connectivity, both obstruction branches, thin-case faithfulness and distinct old face shadows for biduality.',
       ['L108 Theorem 1 and thin-only obstruction', 'L108 Lemma 3.1 walk adapter and Lemma 3.2(i) connectivity', 'L108 Lemma 3.2(iii),(iv) thin-case biduality and full automorphism group'],
       'Lemma 3.2(ii) is replaced by ker(rho)=core_G(<a>); the complete-tripartite example disproves unconditional embedding. The C2×S3 example disproves unconditional geometric-length=step-order. Neither is counted as literal recovery.',
       pevidence)
    notes.append(anchor(pet,*spans[pet['label']]))
    app=newnote('APPE','Appendix E. Complete Petrial operation and kernel controls','BV',
       'The complete Python program checks seven explicit geometries using literal chamber flips and deduplicated vertex–edge sets. Its independent replay checks the counterexamples and thin-case recoveries; it is neither exhaustive nor a proof of the infinite theorem.',
       ['L108 geometric operation and the explicitly described test geometries', 'Python standard-library arithmetic and container operations'],
       targets=['Two direct counterexample controls', 'Finite exact kernel and thin-case biduality controls'],evidence=pevidence)
    notes.append(anchor(app,*spans[app['label']]))
    sentence="Recognition lemma O1.1 supplies the content needed from N013's quoted Theorem 2.2."
    start=text.index(sentence)
    er=newnote('E01','Incorporated reference correction after O4.1','C',
       'This manuscript already incorporates the approved reference correction to N013’s quoted Theorem 2.2. The ten-source predecessor and its separate erratum remain unchanged.',[],
       correction='The formerly ambiguous internal O2.2 reference is corrected in this new manuscript; no additional erratum or proof step is inserted here.')
    notes.append(anchor(er,start,start+len(sentence),sentence))
    notes.sort(key=lambda r:(r['insert_after_codepoint'],r['id']))
    inherited = [e for e in old['evidence'] if e['path']!='phase45_ten_source_errata.json']
    names=['phase61_ten_source_attribution.json','phase62_attribution_recent_audit.json',
           'phase65_petrial_integration_manifest.json','phase65_petrial_integration_attribution.json',
           'phase65_petrial_integration_ledger.json','phase70_petrial_integration_recent_audit.md',
           'phase70_petrial_integration_recent_audit.json','phase70_petrial_integration_recent_audit_manifest.json',
           'phase76_eleven_source_root_audit.json','phase77_eleven_wrapper_recent_audit.md']
    sidecar={
      'schema':'hash_bound_manuscript_attribution.v1','date':'2026-10-10',
      'status':'author_mapping_from_reviewed_extension_pending_independent_semantic_review',
      'manuscript':binding(proofpath.name),'erratum':None,
      'scope':{'source_count':11,'required_erratum_incorporated':True,'old_ten_source_edition_immutable':True,
               'new_notes_add_proof_steps':False,'new_Kc_O0_Petrial_Lean_certificate':False,
               'one_scoped_inherited_Lean_implication':True,'eleven_measurement':None,'priority_or_open_conjecture_claim':False},
      'evidence':inherited+[binding(n) for n in names],
      'selected_inputs_are_not_complete_transitive_closure':True,'annotations_add_mathematical_proof_content':False,
      'quantitative_factor':None,'previously_open_conjecture_cleared':False,'whole_manuscript_Lean_certificate':False,
      'rebase':{'predecessor_sidecar_sha256':digest(oldpath.read_bytes()),
                'old_S23_now':'S24','old_S24_now':'S25','new_notes':['K03','O00','S23','APPE'],
                'E01':'corrected source sentence; no appended obsolete erratum'},
      'notes':notes}
    args.output.write_text(json.dumps(sidecar,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'sidecar_sha256':digest(args.output.read_bytes()),'notes':len(notes)},indent=2))


if __name__=='__main__':
    main()
