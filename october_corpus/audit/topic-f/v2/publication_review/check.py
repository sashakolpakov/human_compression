#!/usr/bin/env python3
"""Read-only publication integration checks; no mathematical replay."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

BASELINE = 'e2893c59d4c50fd79a59bf17250e107d16a5cddf'
HERE = Path(__file__).resolve().parent
ADMISSION = 'audit/topic-f/v2/admission.json'
SCOPE = 'papers/topic-f/v2/scope.json'


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(root, path):
    return json.loads((root/path).read_text())


def functions(text):
    return {n.name: n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef)}


def same_ast(a, b):
    return ast.dump(a, include_attributes=False) == ast.dump(b, include_attributes=False)


def main_calls(node):
    return [n.func.id for n in ast.walk(node)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id.startswith('check_')]


def audit(root, study=None):
    bound = load(HERE, 'bindings.json')
    for row in bound['public']:
        data = (root/row['path']).read_bytes()
        need(len(data) == row['bytes'] and digest(data) == row['sha256'],
             'changed publication candidate: '+row['path'])
    before = subprocess.check_output(['git', 'show', BASELINE+':scripts/verify_snapshot.py'], cwd=root, text=True)
    after = (root/'scripts/verify_snapshot.py').read_text()
    old, new = functions(before), functions(after)
    prior = [name for name in old if name != 'main']
    need(all(name in new and same_ast(old[name], new[name]) for name in prior),
         'an older verifier function changed')
    need(set(new)-set(old) == {'check_topic_f_proofs'}, 'unexpected verifier additions')
    old_calls, new_calls = main_calls(old['main']), main_calls(new['main'])
    need([n for n in new_calls if n != 'check_topic_f_proofs'] == old_calls
         and new_calls.count('check_topic_f_proofs') == 1, 'changed prior checker order')
    spec = importlib.util.spec_from_file_location('topic_f_public_verifier', root/'scripts/verify_snapshot.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = root
    need(module.check_topic_f_proofs() == (25, 5), 'F direct checker did not pass')
    need(module.check_catalogue() == (10, 34), 'catalogue check changed')
    admission = load(root, ADMISSION)
    packets = [('papers/topic-f/v2', 'topic_F_volume', 49),
               ('audit/topic-f/v2/independent_review', 'topic_F_independent_review', 31),
               ('audit/topic-f/v2/root_adoption', 'topic_F_root_adoption', 3)]
    exact_copies = []
    for public, private, count in packets:
        manifest = load(root, public+'/manifest.json')
        need(len(manifest['exports']) == count, 'packet export count')
        for row in manifest['exports']:
            data = (root/public/row['path']).read_bytes()
            need(digest(data) == row['sha256'] and len(data) == row['bytes'], 'copy integrity')
        if study is not None:
            for path in [r['path'] for r in manifest['exports']] + ['manifest.json']:
                need((root/public/path).read_bytes() == (study/private/path).read_bytes(),
                     'public copy differs from private frozen packet')
        exact_copies.append({'public': public, 'exports': count, 'manifest_in_addition': True,
                             'private_comparison': study is not None})
    old_catalogue = json.loads(subprocess.check_output(
        ['git', 'show', BASELINE+':papers/catalogue.json'], cwd=root, text=True))
    catalogue = load(root, 'papers/catalogue.json')
    need(catalogue['papers'] == old_catalogue['papers'] and
         catalogue['new_editions'][:-2] == old_catalogue['new_editions'] and
         {k:v for k,v in catalogue['current_topic_editions'].items() if k != 'F'} ==
         old_catalogue['current_topic_editions'], 'earlier catalogue records changed')
    links = []
    for filename in ['papers/topic-f/v2/PUBLICATION.rst', 'audit/completion.rst', 'README.rst']:
        text = (root/filename).read_text()
        if filename == 'README.rst':
            text = text.split('Odd kernels and cyclotomic polyhedra\n',1)[1].split('Papers and verification\n',1)[0]
        for target in re.findall(r'<([^>]+)>`_', text):
            if '://' in target:
                continue
            resolved = ((root/filename).parent / target.split('#')[0]).resolve()
            need(resolved.is_relative_to(root.resolve()) and resolved.exists(), 'broken public reader link')
            links.append({'document':filename, 'target':target})
    changed = subprocess.check_output(['git', 'diff', '--name-only', BASELINE], cwd=root, text=True).splitlines()
    f_paths = [p for p in changed if '/topic-f/v2/' in p]
    need(not any(Path(p).suffix in {'.md','.olean','.png','.jpg'} or '/sources/' in p for p in f_paths),
         'private primary, Markdown or build artifact added')
    # These controls override a JSON object in memory after real byte integrity
    # succeeds. They isolate semantic guards; they do not rewrite public files.
    original_load = module.load
    controls = []
    def control(name, path, transform):
        obj = original_load(path)
        transform(obj)
        module.load = lambda wanted: copy.deepcopy(obj) if wanted == path else original_load(wanted)
        try:
            module.check_topic_f_proofs()
        except (ValueError, KeyError, IndexError) as exc:
            controls.append({'name':name,'rejected':True,'reason':str(exc)})
        else:
            raise ValueError('semantic mutation accepted: '+name)
        finally:
            module.load = original_load
    for key, value in [('status','UNREVIEWED'),('source_rows',26),('proof_spans',15),
                       ('scientific_pages',10),('complete_validation_pages',3),
                       ('required_mathematical_programs',3),('separate_operational_drivers',1),
                       ('fresh_lean_declarations',10),('new_lean_declarations',5),
                       ('end_to_end_source_formalization',True),('project_total_preserved',28),
                       ('canonical_complete_contract_count_at_this_admission',24),
                       ('remaining_contracts_for_canonical_topic_editions',[]),
                       ('compression_ratio',2),('retained_CP_full_proof_cost',0),
                       ('source_graphics_cost',0),('new_question_credit',1)]:
        control('admission '+key, ADMISSION, lambda d,k=key,v=value:d.__setitem__(k,v))
    control('source marking correction erased', SCOPE,
            lambda d:next(r for r in d['contracts'] if r['id']=='L014.T1.2.defect').__setitem__('status','recovered'))
    control('excluded census claimed', SCOPE,
            lambda d:next(r for r in d['contracts'] if r['id']=='excluded.census').__setitem__('status','recovered'))
    control('retained proof claimed internal', SCOPE,
            lambda d:d['retained_remote_primary'].__setitem__('not_reproved',False))
    control('finite examples promoted to uniform proof', SCOPE,
            lambda d:d['validation_boundary'].__setitem__('uniform_written_proof_depends_on_finite_results',True))
    control('whole common paper omitted', SCOPE,
            lambda d:d['cost_boundary'].__setitem__('full_common_paper_charged_once',False))
    control('independent acceptance removed','audit/topic-f/v2/independent_review/review.json',
            lambda d:d.__setitem__('status','PENDING'))
    control('catalogue TeX input dropped','papers/catalogue.json',
            lambda d:next(r for r in d['new_editions'] if r['id']=='topic-f/v2/umbrella')['tex_inputs'].pop())
    control('new formal declarations invented','papers/topic-f/v2/formal/scope.json',
            lambda d:d.__setitem__('new_declarations',5))
    control('nonstandard Lean axiom inserted','audit/topic-f/v2/independent_review/fresh_replay/formal/report.json',
            lambda d:d['modules'][0]['axioms'][0]['axioms'].append('sorryAx'))
    whitespace = load(HERE, 'whitespace_exceptions.json')
    for row in whitespace['frozen_exceptions']:
        need(digest((root/row['path']).read_bytes()) == row['sha256'], 'changed frozen whitespace exception')
    excludes = [':(exclude)'+r['path'] for r in whitespace['frozen_exceptions']]
    proc = subprocess.run(['git','diff',BASELINE,'--check','--','.']+excludes,
                          cwd=root,text=True,capture_output=True)
    need(proc.returncode == 0, 'whitespace error outside exact frozen exceptions: '+proc.stdout)
    return {'status':'PASS','baseline':BASELINE,'admission_sha256':digest((root/ADMISSION).read_bytes()),
            'admission_artifacts':len(admission['artifacts']),'exact_frozen_copies':exact_copies,
            'prior_nonmain_functions_ast_unchanged':len(prior),'prior_main_checker_order_unchanged':True,
            'new_checker_return':[25,5],'catalogue_return':[10,34],'prior_catalogue_unchanged':True,
            'public_links':links,'new_F_paths':len(f_paths),'no_private_source_or_build_exports':True,
            'semantic_controls':controls,'whitespace_exceptions_preserved':whitespace,
            'scope':'Bounded publication integration only. Reuses accepted independent mathematical, primary, program and formal review; no new proof, GAP, Lean, source extraction or render run.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,required=True)
    p.add_argument('--study',type=Path)
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'fresh output required')
    result=audit(a.repository.resolve(),a.study.resolve() if a.study else None)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':result['status'],'semantic_controls':len(result['semantic_controls']),
                      'prior_nonmain_functions':result['prior_nonmain_functions_ast_unchanged']}))


if __name__=='__main__':
    main()
