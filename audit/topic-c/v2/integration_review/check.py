#!/usr/bin/env python3
"""Read-only Topic C integration audit; corruptions occur only in a fresh copy."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists() and not args.out.is_symlink(), 'fresh output required')
    out = args.out.resolve()
    out.mkdir(parents=True)
    repo = args.repo.resolve()
    publication = 'audit/topic-c/v2/'
    base = 'papers/topic-c/v2/'
    admission = json.loads((repo/publication/'admission.json').read_text())
    need(digest(repo/publication/'admission.json') ==
         'c2245e1f12e58af5834fbea8d3ab58ccbab2b3a0215534a7fe8c143b0b6dbcf9',
         'Different admission edition')
    checked = []
    for private, public, expected in [
            ('topic_C_volume', base,
             'f4113a6161f717f076e0d11158460fef6f12650f5214baa59a16283853fa8f94'),
            ('topic_C_independent_review', publication+'independent_review/',
             '69c225137fcbaf718bcec96060ec3629c17beec0a09cee924fd910cd401f36aa')]:
        need(digest(repo/public/'manifest.json') == expected, 'Public freeze changed')
        manifest = json.loads((args.study/private/'manifest.json').read_text())
        for row in manifest['exports'] + [{'path':'manifest.json'}]:
            name = row['path']
            need((args.study/private/name).read_bytes() == (repo/public/name).read_bytes(),
                 'Copy differs from accepted private artifact: '+name)
        checked.append({'private':private,'public':public,'files':len(manifest['exports'])+1,
                        'manifest_sha256':expected,'all_byte_identical':True})

    baseline = subprocess.check_output(['git','rev-parse','e03c569'],cwd=repo,text=True).strip()
    old = subprocess.check_output(['git','show',baseline+':scripts/verify_snapshot.py'],cwd=repo,text=True)
    current = (repo/'scripts/verify_snapshot.py').read_text()
    functions = lambda text: {n.name:ast.dump(n,include_attributes=False)
                              for n in ast.parse(text).body if isinstance(n,ast.FunctionDef)}
    before, after = functions(old), functions(current)
    unchanged = sorted(n for n in before if n != 'main' and before[n] == after.get(n))
    need(set(unchanged) == set(before)-{'main'}, 'An earlier verifier function changed')
    need(set(after)-set(before) == {'check_topic_c_proofs'}, 'Unexpected verifier addition')
    verifier = load_module(repo/'scripts/verify_snapshot.py','topic_c_publication_verifier')
    need(verifier.check_topic_c_proofs() == (40,16), 'New verifier does not pass')
    catalogue = json.loads((repo/'papers/catalogue.json').read_text())
    entries = [r for r in catalogue['new_editions'] if r['topic']=='C']
    need(entries == admission['catalogue_entries'], 'Catalogue/admission mismatch')
    builder = load_module(repo/'scripts/build_papers.py','topic_c_publication_builder')
    routes=[]
    for row in entries:
        bundle = builder.source_bundle(row,root=repo)
        need(set(bundle) == {row['tex'],*row['tex_inputs']}, 'Incomplete TeX bundle')
        routes.append({'id':row['id'],'files':sorted(bundle),'complete':True})
    fresh = json.loads((repo/publication/'catalogue_replay.json').read_text())
    need(fresh['status']=='PASS_CURRENT_CATALOGUE_ROUTES_RENDERED' and
         fresh['scientific_pages']==27 and len(fresh['scientific_documents'])==5,
         'Catalogue render boundary changed')
    for row,report in zip(entries,fresh['scientific_documents']):
        need(row['id']==report['id'] and row['physical_pages']==report['pages'] and
             report['all_page_text_identical'] and
             digest(repo/row['pdf'])==report['source_pdf_sha256'] and
             not report['builder_report']['diagnostics'], 'Catalogue render mismatch')
        need(digest(repo/row['tex'])==report['builder_report']['tex_sha256'],
             'Rendered a different main source')
        need([r['path'] for r in report['builder_report']['tex_inputs']]==row['tex_inputs'],
             'Rendered a different input set')
        for source in report['builder_report']['tex_inputs']:
            need(digest(repo/source['path'])==source['sha256'], 'Rendered a different input')

    # All mutations below are isolated from the public and frozen private files.
    stage = out/'stage'
    files = {r['path'] for r in admission['artifacts']} | {
        publication+'admission.json','papers/catalogue.json','scripts/verify_snapshot.py'}
    for name in files:
        dest=stage/name
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(repo/name,dest)
    test = load_module(stage/'scripts/verify_snapshot.py','topic_c_staged_verifier')
    need(test.check_topic_c_proofs()==(40,16),'Staged positive control failed')
    controls=[]
    def semantic(name,path,mutate):
        original=test.load
        def altered(p):
            value=original(p)
            if str(p)==path:
                value=copy.deepcopy(value)
                mutate(value)
            return value
        test.load=altered
        try:
            test.check_topic_c_proofs()
        except (ValueError,RuntimeError,FileNotFoundError) as error:
            controls.append({'case':name,'mode':'semantic record mutation in staged verifier',
                             'status':'REJECTED','reason':str(error)})
        else:
            raise RuntimeError('Accepted corruption: '+name)
        finally:
            test.load=original
    ad=publication+'admission.json'
    semantic('claim end-to-end Lean coverage',ad,lambda d:d.update(end_to_end_source_formalization=True))
    semantic('turn unknown L108 cost into zero',ad,lambda d:d.update(original_L108_pdf_cost=0))
    semantic('invent source credit',ad,lambda d:d.update(new_source_credit=1))
    semantic('omit required census program',ad,lambda d:d['required_mathematical_programs'].pop())
    semantic('omit umbrella TeX input','papers/catalogue.json',
             lambda d:next(r for r in d['new_editions'] if r['id']=='topic-c/v2/umbrella')['tex_inputs'].pop())
    semantic('promote excluded auxiliary',base+'scope.json',
             lambda d:next(r for r in d['source_result_rows'] if r['id']=='N14').update(coverage='recovered'))
    semantic('inject nonstandard Lean axiom',publication+'root_replay/formal.json',
             lambda d:d['modules'][2]['axioms'][0].update(axioms=['Unproved.theorem']))
    semantic('replace census by reading source list',publication+'independent_review/replay/janko/phase150_module_C_j1_replay.json',
             lambda d:d.update(source_geometry_list_read=True))
    for name,path,mutation in [
        ('alter Lean proof bytes',base+'formal/SemidirectRecognition.lean',lambda b:b+b'\n'),
        ('truncate required census',base+'programs/phase40_compress_operations_exhaustive.g',lambda b:b[:-20]),
        ('alter required appendix PDF',base+'required-programs.pdf',lambda b:b[:-1])]:
        target=stage/path;old_bytes=target.read_bytes();target.write_bytes(mutation(old_bytes))
        try:
            test.check_topic_c_proofs()
        except (ValueError,RuntimeError,FileNotFoundError) as error:
            controls.append({'case':name,'mode':'real staged byte corruption',
                             'status':'REJECTED','reason':str(error)})
        else:
            raise RuntimeError('Accepted byte corruption: '+name)
        finally:
            target.write_bytes(old_bytes)
    need(test.check_topic_c_proofs()==(40,16),'Final restored positive control failed')
    report={'status':'PASS_BOUNDED_PUBLICATION_INTEGRATION_REVIEW',
            'admission_sha256':digest(repo/publication/'admission.json'),
            'exact_private_copies':checked,'admission_artifacts':len(admission['artifacts']),
            'baseline_commit':baseline,'old_non_main_verifier_functions_unchanged':unchanged,
            'new_verifier_result':[40,16],'catalogue_routes':routes,
            'catalogue_render_report_sha256':digest(repo/publication/'catalogue_replay.json'),
            'root_catalogue_replay_checked_not_repeated':True,
            'negative_controls':controls,'fresh_Lean_or_Janko_rerun_in_this_integration_check':False,
            'mathematical_acceptance':'Previously frozen independent mathematical review retained byte for byte.',
            'ratio':None,'new_source_credit':0,'new_question_credit':0}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':report['status'],'byte_identical_export_counts':[r['files'] for r in checked],
                      'old_non_main_functions':len(unchanged),'controls':len(controls)}))


if __name__=='__main__':
    main()
