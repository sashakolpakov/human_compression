"""Fresh finite control; output must be outside this immutable packet."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def require(test, message):
    if not test:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    require(__debug__, 'optimized Python is forbidden')
    parser = argparse.ArgumentParser()
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--render', action='store_true')
    args = parser.parse_args()
    base = Path(__file__).resolve().parent
    out = args.output.resolve()
    require(out != base and base not in out.parents, 'external output required')
    out.mkdir(parents=True, exist_ok=False)
    manifest = json.loads((base/'manifest.json').read_text())
    for rec in manifest['exports']:
        path = base/rec['path']
        require(path.stat().st_size == rec['bytes'] and digest(path) == rec['sha256'],
                'damaged export: '+str(path))
    deps = json.loads((base/'dependencies.json').read_text())
    for rec in deps['bindings']:
        path = args.study/rec['path']
        require(path.stat().st_size == rec['bytes'] and digest(path) == rec['sha256'],
                'damaged dependency: '+str(path))
    scope = json.loads((base/'scope.json').read_text())
    for key in ['parabolic_names','full_F004_census','q5_census',
                'whole_original_credit','new_conjecture_claim','lean_claim',
                'compression_measurement']:
        require(scope[key] is False or scope[key] == 0, 'scope inflation: '+key)
    spec = importlib.util.spec_from_file_location('literal_parser', base/'extract_records.py')
    extractor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(extractor)
    controls = 0
    for raw, marker in [('[]','MISSING'),('M [1]; M [2]','M'),('M [Read("x")]','M')]:
        try:
            extractor.literal(raw,marker)
        except ValueError:
            controls += 1
        else:
            raise RuntimeError('damaged literal accepted')
    gap = shutil.which('gap')
    require(gap is not None, 'GAP unavailable')
    runs = []

    def run(name, text, marker):
        driver = out/(name+'.g')
        driver.write_text(text)
        done = subprocess.run([gap,'-q','-b',str(driver)], capture_output=True,
                              text=True, timeout=90, stdin=subprocess.DEVNULL)
        (out/(name+'.stdout')).write_text(done.stdout)
        (out/(name+'.stderr')).write_text(done.stderr)
        require(done.returncode == 0 and done.stderr == '' and
                done.stdout.count(marker) == 1, 'GAP failure: '+name)
        runs.append({'name':name,'returncode':done.returncode,
                     'stdout_sha256':digest(out/(name+'.stdout')),
                     'stderr_empty':True,'terminal_marker':marker})
        return done.stdout

    model = base/'q3_model.g'
    run('model',f'''Read("{model}");;
    B:=Group(GeneratorsOfGroup(PrimitiveGroup(351,7)));;
    iso:=IsomorphismGroups(B,G);;
    if iso=fail or not IsBijective(iso) then Error("standard model identity");fi;
    if Size(AutomorphismGroup(B))<>expectedAutOrder then Error("full Aut order");fi;
    if not IsNormal(A,G) or Size(A)/Size(Centralizer(A,G))<>expectedAutOrder then Error("compatible action");fi;
    Print("MODEL_CONTROL_COMPLETE\\n");QUIT;
    ''','MODEL_CONTROL_COMPLETE')
    for name, engine, opts, marker in [
        ('prefix','enumerate_rank4.g','', 'COMPLETE_EXHAUSTION'),
        ('ends','enumerate_ends_v2.g','computeOddRankBound:=true;;', 'COMPLETE_ENDS_EXHAUSTION')]:
        raw = run(name,f'modelFile:="{model}";;{opts}\nRead("{base/engine}");\n',marker)
        ranks = [4,5,6] if name == 'ends' else list(range(4,23))
        records = ''.join('freshMarks[%d]:=%s;;\n' %
                    (rank,extractor.literal(raw,f'COMPLETE_TUPLES_RANK_{rank} ')) for rank in ranks)
        (out/(name+'_records.g')).write_text('freshMarks:=[];;\n'+records)
        if name == 'ends':
            require('subgroup_classes 84 max_elementary_order 8 rank_bound 6' in ' '.join(raw.split()),
                    'unexpected Sylow control')
    run('compare',f'''Read("{model}");;Read("{base/'q3_ends_records.g'}");;retained:=recordedMarks;;
    for file in ["{out/'prefix_records.g'}","{out/'ends_records.g'}"] do
      Read(file);;
      for r in [4..6] do
        if Length(freshMarks[r])<>Length(retained[r]) then Error("orbit count");fi;
        for t in retained[r] do
          if Number(freshMarks[r],u->RepresentativeAction(A,t,u,OnTuples)<>fail)<>1 then Error("orbit equality");fi;
        od;
      od;
    od;
    Print("EXACT_ORBIT_COMPARISON_COMPLETE\\n");QUIT;
    ''','EXACT_ORBIT_COMPARISON_COMPLETE')
    raw = run('validate',f'modelFile:="{model}";;recordsFile:="{base/"q3_ends_records.g"}";;checksFile:="{base/"checks.g"}";;\nRead("{base/"validate_records_v2.g"}");\n',
              'COMPLETE_RECORD_VALIDATION')
    require('VALIDATED_TOTAL 2 SUBSET_PAIRS 512' in raw, 'wrong finite control')
    native = None
    if args.render:
        shutil.copy2(base/'ends_enumeration.tex',out/'ends_enumeration.tex')
        env = dict(os.environ)
        env.pop('PYTHONOPTIMIZE',None)
        for index in [1,2]:
            done = subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',
                                   'ends_enumeration.tex'],cwd=out,capture_output=True,text=True,
                                  timeout=45,env=env)
            (out/f'native{index}.stdout').write_text(done.stdout)
            (out/f'native{index}.stderr').write_text(done.stderr)
            require(done.returncode == 0,'native build')
        from pypdf import PdfReader
        reader = PdfReader(out/'ends_enumeration.pdf')
        native = {'pages':len(reader.pages),'pdf_sha256':digest(out/'ends_enumeration.pdf'),
                  'direct_view_required':True}
    report = {'status':'PASSED','exports':len(manifest['exports']),
              'bindings':len(deps['bindings']),'runs':runs,'literal_negative_controls':controls,
              'scope_controls':7,'full_subset_pairs':512,'native':native,
              'whole_original_credit':0,'q5_census':False}
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
