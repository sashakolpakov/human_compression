"""Root-owned adoption and incremental tracked manifest; no historical replay."""
import sys
if sys.flags.optimize:
    raise RuntimeError('Ordinary Python required')
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime,timezone
import argparse
import importlib.util
import json
import shutil

R=Path('/Users/sasha/medusa/math_compression')
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('completion_guard',HERE/'check_L115_completion.py')
g=importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
A=R/g.AUD


def save(path,value):
    g.need(not path.exists(),'Never replace a final gate or review')
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2)+'\n')


def gates(args):
    g.need(g.git(R,'rev-parse','HEAD').decode().strip()==g.BASELINE,'Exact uncommitted predecessor')
    actual=g.verify(R,False)
    report=g.load(args.preflight_report)
    g.need(report==actual,'Exact installed preflight report')
    review=args.review.resolve()
    g.need(g.sha(review/'manifest.json')==args.review_sha,'Exact root registration review')
    m=g.load(review/'manifest.json')
    g.need(m['status']=='ACCEPTED_L115_SOURCE_COMPLETION_REGISTRATION','Distinct registration acceptance')
    for row in m['exports']:
        g.bind(review,row)
    dependencies=g.load(review/'dependencies.json')
    g.need(isinstance(dependencies,list),'Explicit root dependencies')
    parameters = g.load(A/'integration/parameters.json')
    history = parameters['old_mutable']
    # The root review may bind a predecessor file that this installation replaces.
    # Its exact retained predecessor is the authority after installation.
    for row in dependencies:
        p = Path(row['path'])
        g.need(p.is_absolute(), 'Explicit absolute root review input')
        if p.is_relative_to(R) and str(p.relative_to(R)) in history:
            name = str(p.relative_to(R))
            expected = history[name]
            g.need((row['bytes'],row['sha256']) == (expected['bytes'],expected['sha256']), 'Exact declared predecessor review input')
            g.bind(R, dict(expected, path=g.AUD+'/previous/'+name))
        elif p == R/'provenance/publication_manifest.json':
            expected = parameters['previous_publication_manifest']
            g.need((row['bytes'],row['sha256']) == (expected['bytes'],expected['sha256']), 'Exact predecessor tracked manifest')
            g.bind(R, expected)
        else:
            g.need(p.stat().st_size==row['bytes'] and g.sha(p)==row['sha256'],'Exact root review dependency')
    g.need(not (A/'registration_review').exists() and not (A/'integration_checks').exists(),'Fresh final adoption')
    for row in m['exports']+[g.pin(review/'manifest.json',review)]:
        dest=A/'registration_review'/row['path']
        dest.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(review/row['path'],dest)
    checks=A/'integration_checks'
    checks.mkdir()
    shutil.copyfile(args.preflight_report,checks/'installed_preflight.json')
    bindings=[g.pin(p,R) for folder in [A/'registration_review',checks] for p in sorted(folder.rglob('*')) if p.is_file()]
    gate=dict(status='ROOT_ACCEPTED_L115_COMPLETE_SOURCE_PUBLICATION',source_ids=['L115'],source_completion_credit=1,
              ordinary_recovery_credit=0,principal_refutation_credit=0,new_measurements=0,new_question_credit=0,new_Lean_credit=0,
              compression_factor=None,utc=datetime.now(timezone.utc).isoformat(),fully_treated_originals=98,outstanding_originals=7,
              payload_manifest=g.pin(A/'integration/payload_manifest.json',R),parameters=g.pin(A/'integration/parameters.json',R),
              candidate_manifest=g.pin(A/'registration/manifest.json',R),mathematical_acceptance_sha256=g.MATH_SHA,
              portable_acceptance_sha256=g.PORTABLE_SHA,bindings=bindings,
              scope='L115 fixed twenty-four-page article fully treated: all 70 source dispositions, corrected general classification and counting formulas, all 180 torus integers and 60 numerical rows, and all 29 diagrams representing 75 inner classes. Eight complete manuscripts retain 36 proof pages, including the unchanged four-page principal refutation. Lemma 6.1 is restricted to ranks greater than one; source domain, classification, numerical and diagram corrections and attributed classical premises remain explicit. Ordinary recoveries, principal refutations and all 53 measured IDs are unchanged.')
    save(A/'root_integration.json',gate)
    print(json.dumps(dict(status='ROOT_L115_COMPLETION_GATE_INSTALLED',fully_treated=98,outstanding=7)))


def manifest(args):
    g.need((A/'root_integration.json').is_file(),'Final root gate required')
    g.verify(R,False)
    g.need(not g.git(R,'ls-files','--others','--exclude-standard').strip(),'Stage every intended public artifact first')
    params=g.load(A/'integration/parameters.json')
    exact=g.manifest_rows(R,params)
    path=R/'provenance/publication_manifest.json'
    if args.write_manifest:
        g.need(shutil.disk_usage(R).free>=4*2**30+2*path.stat().st_size,'Preserve 4 GiB reserve')
        temp=path.with_name(path.name+'.L115-install')
        g.need(not temp.exists(),'Fresh atomic manifest temporary')
        temp.write_text(json.dumps(exact,indent=2)+'\n')
        temp.replace(path)
    g.need(g.load(path)==exact,'Exact tracked manifest with unchanged predecessor metadata')
    print(json.dumps(dict(status='PASS_L115_TRACKED_MANIFEST',tracked_artifacts=len(exact['files']),historical_files_rehashed=False)))


if __name__=='__main__':
    p=argparse.ArgumentParser()
    subs=p.add_subparsers(dest='command',required=True)
    a=subs.add_parser('gates')
    a.add_argument('--review',type=Path,required=True)
    a.add_argument('--review-sha',required=True)
    a.add_argument('--preflight-report',type=Path,required=True)
    a=subs.add_parser('manifest')
    a.add_argument('--write-manifest',action='store_true')
    args=p.parse_args()
    gates(args) if args.command=='gates' else manifest(args)
