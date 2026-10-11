#!/usr/bin/env python3
"""Independent binding and finite-interface checks; no source texts emitted."""
import argparse
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import tempfile
from fractions import Fraction
from pathlib import Path

AUTHOR_SHA = '4737dc649c7e7229ffad462ec348870de7f4410ef8d31d51af92c0f17e8e7d49'

def need(ok, why):
    if not ok:
        raise RuntimeError(why)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def orbits(points, group, action):
    unseen = set(points)
    ans = []
    while unseen:
        x = min(unseen)
        o = {action(g, x) for g in group}
        need(o <= set(points), 'Action does not preserve the set')
        unseen -= o
        ans.append(o)
    return ans

def support_model(n):
    # E has two orbits: ordinary points and a distinguished extra point.
    # Z consists of a support S, an anchor e, and an ordinary marked point t.
    # R says e belongs to S when e is ordinary, and t belongs to S.
    # Individual proper support sublevel sets are NOT invariant under S_n.
    group = list(itertools.permutations(range(n)))
    top = (1 << n) - 1
    def mask_action(g, m):
        return sum(1 << g[i] for i in range(n) if m >> i & 1)
    def act(g, z):
        m, e, t = z
        return mask_action(g, m), (g[e] if e < n else n), g[t]
    points = [(m, e, t) for m in range(1 << n) for e in range(n+1)
              for t in range(n) if (e == n or m >> e & 1) and m >> t & 1]
    full = [z for z in points if z[0] == top]
    direct = len(orbits(full, group, act))
    terms = []
    naive = Fraction(0)
    for e in (0, n):
        stab = [g for g in group if e == n or g[e] == e]
        fiber = [z for z in points if z[1] == e]
        subtotal = 0
        for g in stab:
            fixed = [z for z in fiber if act(g, z) == z]
            subtotal += sum((-1)**(n-m.bit_count()) *
                            sum(z[0] & ~m == 0 for z in fixed)
                            for m in range(1 << n))
        term = Fraction(subtotal, len(stab))
        need(term == len(orbits([z for z in full if z[1] == e], stab, act)),
             'Stabilizer fiber count')
        terms.append(term)
        naive += Fraction(len([z for z in full if z[1] == e]), len(stab))
    need(sum(terms) == direct == 3, 'Combined exact-support formula')
    noninvariant = any(z[0] & ~1 == 0 and act(g,z)[0] & ~1 != 0
                       for z in points for g in group)
    need(noninvariant, 'Model must exercise noninvariant proper sublevel sets')
    need(naive != direct, 'Omitting stabilizer fixed-point terms must fail')
    # A nonfaithful acting group has the same orbit count; every element is doubled.
    doubled = Fraction(sum(2*len([z for z in full if act(g,z)==z]) for g in group),
                       2*len(group))
    need(doubled == direct, 'Faithfulness is not needed by Burnside')
    return {'degree': n, 'group_order':len(group), 'admissible_objects':len(points),
            'top_objects':len(full), 'base_orbits':2, 'top_orbits':direct,
            'proper_sublevel_noninvariant':True,
            'false_free_action_answer':[naive.numerator,naive.denominator],
            'nonfaithful_doubled_action_orbits':int(doubled)}

def validate_author(root):
    need(sha(root/'manifest.json') == AUTHOR_SHA, 'Different author freeze')
    manifest = json.loads((root/'manifest.json').read_text())
    for row in manifest['exports']:
        p = root/row['path']
        need(p.resolve().is_relative_to(root.resolve()), 'Escaping path')
        need(p.is_file() and p.stat().st_size == row['bytes'] and sha(p)==row['sha256'],
             'Changed author artifact: '+row['path'])
    s = json.loads((root/'scope.json').read_text())
    expected = [f'{k}.{i}' for k,n in [('L066',16),('L074',17),('L104',4)]
                for i in range(1,n+1)]
    need([r['id'] for r in s['contracts']]==expected, 'Wrong source row boundary')
    need(s['contracts'][-1]['current_status'].startswith('excluded_secondary'), 'Lost exclusions')
    need(len(s['program_inventory'])==10, 'Eight programs and two drivers required')
    return s, manifest

def replay_evidence(root, replay):
    report = json.loads((replay/'report.json').read_text())
    need(report['status']=='PASS' and report['manifest_sha256']==AUTHOR_SHA, 'Wrong replay')
    text = (replay/'j2/j2_search.log').read_text()
    ids = [int(x) for x in re.findall(r'^BOREL_COMPLETE id=(\d+) ', text, re.M)]
    need(ids == list(range(1,147)), 'Missing Borel')
    checked = {}
    # BOREL_PROGRESS is cumulative within one Borel/rank; retain its final count.
    for b,r,c in re.findall(r'^BOREL_PROGRESS id=(\d+) rank=(\d+) .* checked=(\d+) ',text,re.M):
        checked[int(b),int(r)] = int(c)
    totals = [sum(c for (b,rank),c in checked.items() if rank==r) for r in range(2,7)]
    need(totals == [644,1226,1931,271,0], 'Incomplete augmentation totals')
    stage = replay/'j2/work/research/leemans'
    done = sorted((stage/'phase5_j2_checkpoints').glob('b*_done.g'))
    need(len(done)==146, 'Missing checkpoints')
    for p in done:
        levels = json.loads(re.search(r'levels:=(\[[^\]]*\])',p.read_text())[1])
        need(not levels or levels[-1]==0, 'No empty next level')
    witness = stage/'phase5_j2_representatives.g'
    # GAP may print different generating lists for the very same subgroup.
    # Compare the actual 170 subgroup objects, rather than their printed bytes.
    template = Path(__file__).with_name('compare_witnesses.g')
    prefix = ('AUTHOR_WITNESS:='+json.dumps(str((root/'author_replay/j2/phase5_j2_representatives.g').resolve()))+';;\n'+
              'FRESH_WITNESS:='+json.dumps(str(witness.resolve()))+';;\n')
    with tempfile.TemporaryDirectory(prefix='topic-d-witness-') as td:
        script = Path(td)/'compare.g'
        script.write_text(prefix+template.read_text())
        proc = subprocess.run([shutil.which('gap'),'-q','-T',str(script)],
                              capture_output=True,text=True,timeout=60)
    need(proc.returncode==0 and 'PASS geometries=30 exact_subgroups=170 controls=2' in proc.stdout
         and 'Error' not in proc.stdout+proc.stderr, 'Witness semantic comparison failed')
    fusion = (replay/'j2/j2_fusion.log').read_text()
    rows = [[int(t) for t in v] for v in re.findall(
        r'^FUSION rank=(\d+) inner_classes=(\d+) aut_type_classes=(\d+)',fusion,re.M)]
    need(rows[:3]==[[2,8,8],[3,24,19],[4,5,3]], 'Class fusion')
    need(len(rows)==13 and all(a==b==0 for _,a,b in rows[3:]), 'Higher ranks')
    proof = json.loads((replay/'formal/report.json').read_text())
    declarations = [v for m in proof['modules'] for v in m['axioms']]
    need(len(declarations)==10 and all(set(v['axioms']) <=
        {'propext','Classical.choice','Quot.sound'} for v in declarations), 'Formal scope/axioms')
    return {'anchors':146,'augmentation_by_rank':totals,'total_candidates':sum(totals),
            'fusion':rows,'fresh_witness_sha256':sha(witness),
            'author_witness_sha256':sha(root/'author_replay/j2/phase5_j2_representatives.g'),
            'witness_semantic_comparison':{'exact_groups':170,'geometries':30,
                'controls':2,'stdout':proc.stdout.strip(),'checker_sha256':sha(template),
                'note':'Generating lists may differ; actual groups and all Borel IDs/orders agree.'},
            'lean_declarations':10,
            'render_pages':sum(x['pages'] for x in report['render']),
            'reports':{x:sha(replay/x) for x in ['report.json','small/replay.json',
                        'j2/replay.json','formal/report.json']}}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author',type=Path,required=True)
    ap.add_argument('--replay',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();need(not os.path.lexists(a.out),'Fresh output required')
    scope,manifest=validate_author(a.author)
    result={'status':'PASS','author_manifest_sha256':AUTHOR_SHA,
            'author_exports':len(manifest['exports']),'source_rows':len(scope['contracts']),
            'finite_support_models':[support_model(n) for n in [3,4]],
            'fresh_replay':replay_evidence(a.author,a.replay),
            'limits':'Finite models test interfaces; the all-parameter proof acceptance is a separate written review.',
            'new_source_credit':0,'new_question_credit':0,'ratio':None}
    a.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','out':str(a.out)}))

if __name__=='__main__':
    main()
