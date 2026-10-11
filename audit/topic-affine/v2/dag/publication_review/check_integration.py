#!/usr/bin/env python3
"""Review publication wiring without re-extracting sources or rerunning proofs.

Controls alter parsed records in memory. All disk-byte checks remain enabled;
no public file is edited. This is separate from science and cost acceptance.
"""
import argparse, ast, copy, hashlib, importlib.util, json, re, subprocess
from pathlib import Path

BASE = 'eff467a870c7f19d851928158ffd424bf03390c6'
PREFIX = 'audit/topic-affine/v2/dag/'
CANDIDATE_SHA = '27d36f43b16a0d23b3dbedad7a883f0d2fa4ffff2a01bfd9db5d7f9655418c7b'
EXACT_LATER = {PREFIX+'root_publication_acceptance.json',
               PREFIX+'root_publication_replay.json',
               'provenance/publication_manifest.json'}

def need(value, message):
    if not value:
        raise ValueError(message)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(p):
    return json.loads(p.read_text())

def check_change_set(changed, bound, later):
    need(bound <= changed, 'candidate missing from baseline change set')
    need(changed <= bound | later, 'unreviewed tracked change: '+str(sorted(changed-bound-later)))

def checked_files(repo, candidate, review_manifest=None):
    bound = {r['path'] for r in candidate['files']}
    need(len(bound) == len(candidate['files']) == 128, '128 unique candidate files')
    for row in candidate['files']:
        p = repo/row['path']
        need(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'changed candidate '+row['path'])
    later = set(EXACT_LATER)
    if review_manifest is not None:
        need(review_manifest['status'] == 'FROZEN_ACCEPTED_BOUNDED_AFFINE_PUBLICATION_REVIEW', 'unaccepted future review manifest')
        exports = review_manifest['exports']
        for row in exports:
            name = row['path']
            need(not Path(name).is_absolute() and '..' not in Path(name).parts, 'unsafe future export')
            p = repo/PREFIX/'publication_review'/name
            need(p.stat().st_size == row['bytes'] and sha(p) == row['sha256'], 'changed future review export '+name)
            later.add(PREFIX+'publication_review/'+name)
        later.add(PREFIX+'publication_review/manifest.json')
    changed = set(subprocess.check_output(['git','diff','--name-only',BASE,'--'], cwd=repo, text=True).splitlines())
    check_change_set(changed,bound,later)
    return {'candidate_files':len(bound), 'tracked_changes':len(changed), 'allowed_exact_later_paths':sorted(later), 'prefix_wildcards':False}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--repo', type=Path, required=True); ap.add_argument('--study', type=Path, required=True); ap.add_argument('--out', type=Path, required=True); a=ap.parse_args()
    need(not a.out.exists(), 'fresh output required')
    repo,study=a.repo,a.study; candidate_path=study/'topic_Affine_dag_publication_candidate/candidate.json'
    need(sha(candidate_path)==CANDIDATE_SHA, 'candidate pin')
    candidate=load(candidate_path)
    future_path=repo/PREFIX/'publication_review/manifest.json'; future=None
    if future_path.exists():
        own=Path(__file__).parent/'manifest.json'
        need(own.exists() and sha(own)==sha(future_path), 'future review must be this exact frozen review')
        future=load(future_path)
    publication_boundary=checked_files(repo,candidate,future)
    script=repo/'scripts/verify_snapshot.py'
    old=subprocess.check_output(['git','show',BASE+':scripts/verify_snapshot.py'],cwd=repo,text=True)
    new=script.read_text(); old_ast,new_ast=ast.parse(old),ast.parse(new)
    defs=lambda tree:{n.name:n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
    before,after=defs(old_ast),defs(new_ast)
    prior=load(study/'topic_Affine_dag_publication_candidate/prior_guard_asts.json')
    unchanged=[]
    for name,node in before.items():
        if name=='main': continue
        actual=ast.dump(node,include_attributes=False)
        need(name in after and actual==ast.dump(after[name],include_attributes=False)==prior[name], 'prior guard changed '+name)
        unchanged.append(name)
    need(len(unchanged)==len(prior)==34 and set(after)-set(before)=={'check_affine_dag'}, 'guard inventory')
    other=lambda tree:[ast.dump(n,include_attributes=False) for n in tree.body if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))]
    need(other(old_ast)==other(new_ast), 'top-level configuration changed')
    calls=lambda n:[x.func.id for x in ast.walk(n) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id.startswith('check_')]
    old_calls,new_calls=calls(before['main']),calls(after['main'])
    need([x for x in new_calls if x!='check_affine_dag']==old_calls and new_calls.count('check_affine_dag')==1, 'old main checks changed')
    mapping=load(repo/PREFIX/'publication_mapping.json'); admission=load(repo/PREFIX/'admission.json')
    copies=[]; exports=0
    for folder,pin in admission['packet_manifests'].items():
        public=PREFIX+folder
        private=[k for k,v in mapping['private_prefixes'].items() if v==public]
        need(len(private)==1, 'unique archive route '+folder)
        p,q=study/private[0],repo/public
        need(sha(p/'manifest.json')==sha(q/'manifest.json')==pin, 'exact copied manifest '+folder)
        manifest=load(p/'manifest.json')
        for r in manifest['exports']:
            x,y=p/r['path'],q/r['path']
            need(x.read_bytes()==y.read_bytes() and sha(y)==r['sha256'] and y.stat().st_size==r['bytes'], 'exact copied export '+str(y))
            exports+=1
        copies.append({'private':private[0],'public':public,'manifest_sha256':pin,'exports':len(manifest['exports'])})
    need(exports==110 and len(copies)==7, 'archive totals')
    for r in admission['artifacts']:
        p=repo/r['path']; need(sha(p)==r['sha256'] and p.stat().st_size==r['bytes'], 'admission binding '+r['path'])
    need(len(admission['artifacts'])==123, 'admission artifact count')
    graph=load(repo/PREFIX/'logical/logical_graph.json')
    for r in mapping['graph_inputs']:
        public=repo/r['public_path']; original=(repo if r['namespace']=='public' else study)/r['path']
        need(public.read_bytes()==original.read_bytes() and sha(public)==r['sha256'], 'exact public graph input route')
    need(len(mapping['graph_inputs'])==44 and len(mapping['separate_primary_inputs'])==6, 'public/private source boundary')
    # These sources are deliberately not opened: this review checks relocation,
    # while fresh primary extraction retains its explicit separate prerequisite.
    need(all(r['namespace']=='research' and r['path'].startswith('sources/') and 'public_path' not in r for r in mapping['separate_primary_inputs']), 'primary material redistributed')
    spec=importlib.util.spec_from_file_location('affine_publication_guard_review',script); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    positive=m.check_affine_dag(); need(positive==(120,222), 'new guard result')
    prior_results={name:getattr(m,name)() for name in ['check_affine_proofs','check_affine_measurement']}
    original_load=m.load; controls=[]
    def control(name,target,change):
        def changed(path):
            data=original_load(path)
            if str(path)==target:
                data=copy.deepcopy(data);change(data)
            return data
        m.load=changed
        try:
            m.check_affine_dag()
        except ValueError as exc:
            controls.append({'name':name,'rejected':True,'reason':str(exc),'mechanism':'Parsed-record mutation in memory, all actual disk-byte guards left enabled.'})
        else:
            raise ValueError('accepted mutation '+name)
        finally:
            m.load=original_load
    control('changed_artifact',PREFIX+'admission.json',lambda d:d['artifacts'][0].update(sha256='0'*64))
    control('wrong_current_cost_pin',PREFIX+'admission.json',lambda d:d['packet_manifests'].update(costs=d['packet_manifests']['costs_previous']))
    control('lost_deletion_prerequisite',PREFIX+'logical/logical_graph.json',lambda d:d.update(edges=[e for e in d['edges'] if (e['source'],e['target'])!=('UA.D','UA.SK.Delete')]))
    control('wrong_public_mapping',PREFIX+'publication_mapping.json',lambda d:d['graph_inputs'][0].update(public_path='README.rst'))
    def bad_locator(d):
        loc=next(s for n in d['nodes'] for s in n['locators'] if s['namespace']=='public');loc['start_codepoint']+=1
    control('changed_current_proof_locator',PREFIX+'logical/logical_graph.json',bad_locator)
    def wrong_owner(d):
        d['owner_costs']['h.front']['calibrated_selected']['NFC']['characters_without_whitespace']+=1
    control('changed_one_owner_cell',PREFIX+'costs/weights.json',wrong_owner)
    def gap(d):
        next(iter(d['documents'].values()))['variants']['calibrated_selected']['spans'][0]['start']+=1
    control('gap_in_passage_partition',PREFIX+'costs/partition.json',gap)
    def duplicate(d):
        entry=next(v for v in d['node_interfaces'].values() if v['owners']);entry['owners'].append(entry['owners'][0])
    control('duplicate_shared_owner',PREFIX+'costs/weights.json',duplicate)
    control('unknown_external_as_zero',PREFIX+'costs/weights.json',lambda d:d['node_interfaces']['ext.Lucchini'].update(known_weight=0))
    def wrong_route(d):
        next(iter(d['individual_node_closures'].values()))['raw_program_alternative_subtotal']['calibrated_selected']['NFC']['characters_without_whitespace']+=1
    control('incorrect_raw_alternative',PREFIX+'costs/weights.json',wrong_route)
    control('omit_whole_program',PREFIX+'costs/weights.json',lambda d:d['raw_program_alternative'].pop('program.kernel64'))
    control('omit_whole_common_context',PREFIX+'costs/acquisition.json',lambda d:d['stages'][0]['complete_owner_ids'].pop())
    control('omit_whole_application_context',PREFIX+'costs/acquisition.json',lambda d:d['stages'][2]['complete_owner_ids'].pop())
    control('changed_full_factor',PREFIX+'admission.json',lambda d:d['primary']['comparisons']['written_papers'].update(factor=2))
    control('invented_graphics_cost',PREFIX+'admission.json',lambda d:d.update(graphic_cost=0))
    control('invented_full_formalization',PREFIX+'admission.json',lambda d:d.update(source_specific_full_formalization=True))
    control('invented_source_credit',PREFIX+'admission.json',lambda d:d.update(new_source_credit=1))
    need(m.check_affine_dag()==positive, 'unmodified guard no longer passes')
    boundary_controls=[]
    candidate_paths={r['path'] for r in candidate['files']}
    for extra in [PREFIX+'unreviewed_extra.json', PREFIX+'publication_review/not_declared.json', 'papers/topic-affine/v2/umbrella.tex']:
        try:
            check_change_set(candidate_paths|{extra},candidate_paths,EXACT_LATER)
        except ValueError as exc:
            boundary_controls.append({'unexpected_path':extra,'rejected':True,'reason':str(exc)})
        else:
            raise ValueError('accepted unrestricted addition '+extra)
    hrefs=[]
    for name in ['README.rst',PREFIX+'README.rst']:
        for href in re.findall(r'<([^<>]+)>`_', (repo/name).read_text()):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href): continue
            target=href.split('#')[0]
            if not target: continue
            need(((repo/name).parent/target).exists(), 'broken relative link '+name+' '+target)
            hrefs.append({'document':name,'target':target})
    reader_bindings=load(repo/PREFIX/'costs/reader_input_bindings.json')['files']
    for path,pin in reader_bindings.items():
        folder,rest=path.split('/',1);need(sha(repo/mapping['private_prefixes'][folder]/rest)==pin, 'operative reader input route')
    protocol=(repo/'audit/protocol.tex').read_text()
    need('\\mathcal P(t)=\\bigcup_{v\\in D(t)}P(v)' in protocol and
         'W_{\\rm known}(t)=\\sum_{p\\in\\mathcal P(t),\\,c(p)\\text{ known}}c(p)' in protocol,
         'protocol must union passage owners before summing')
    need('several' in protocol.lower() and 'count some passages twice' in protocol and
         'unknown proof' in protocol and 'charges shared' in protocol, 'missing protocol qualifications')
    report={'status':'PASS_BOUNDED_INDEPENDENT_AFFINE_DAG_PUBLICATION_INTEGRATION','baseline':BASE,'candidate_sha256':CANDIDATE_SHA,'publication_boundary':publication_boundary,'prior_nonmain_guards_unchanged':unchanged,'prior_main_calls_preserved':True,'prior_check_results':prior_results,'new_check_result':positive,'copied_archives':copies,'exact_frozen_exports':exports,'admission_artifacts':123,'public_graph_input_routes':44,'separate_primary_inputs':6,'negative_controls':controls,'boundary_controls':boundary_controls,'local_links':hrefs,'reader_input_routes':reader_bindings,'protocol_owner_union_verified':True,'source_reextraction_performed':False,'GAP_or_Lean_replay_performed':False,'public_files_edited':False,'mathematical_and_cost_acceptance':'Reuses distinct accepted scientific/root cost reviews; this report checks root-authored publication wiring only.'}
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'prior_guards':len(unchanged),'archives':len(copies),'exports':exports,'controls':len(controls),'links':len(hrefs),'result':positive}))

if __name__=='__main__':
    main()
