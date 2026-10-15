"""Create the immutable author preparation component, never execute a target."""
import hashlib,json,pathlib,shutil
if not __debug__:raise SystemExit('optimized execution forbidden')
HERE=pathlib.Path(__file__).resolve().parent
def row(p,base):
    b=p.read_bytes();return dict(path=str(p.relative_to(base)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def main():
    dest=HERE.parent/'exhaustion_component_v1';dest.mkdir(exist_ok=False)
    for p in sorted(HERE.rglob('*')):
        if not p.is_file() or '__pycache__' in p.parts or p.suffix in ('.aux','.out') or p.name=='draft_manifest.json':continue
        q=dest/p.relative_to(HERE);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    shutil.copyfile(HERE.parents[2]/'phase4_geometry_checks.g',dest/'accepted_verify.g')
    (dest/'author_scope.json').write_text(json.dumps(dict(
      status='AUTHOR_COMPLETE_BROAD_PRIMITIVE_PREPARATION_COMPONENT_AWAITING_DISTINCT_REVIEW',
      target_runs=0,whole_original_credit=0,
      positive_scope=['General RWPRI panel-recognition and maximal-augmentation adaptation without local2T',
                      'Exact unchanged seven legacy functions and general verifier',
                      'Complete retained95-class/367-inclusion input and fixed named model map',
                      'Seven tiny all-family controls and a preparation-only target draft'],
      excluded=['Target traversal/exhaustion','Aut/type fusion','Bare incidence isomorphism counts',
                'Whole L100 recovery','Production receipt wrapper','New Lean or measurement'],
      executable_entry='check.py --study S --out NEW_ABSOLUTE --render',
      source_priorities='Exact source and all retained classifications stay explicitly attributed.',
      historical_failure='loader_execution01: Group([]) usage failure; corrected in separate loader_v2, original retained.'),indent=2)+'\n')
    exports=[row(p,dest) for p in sorted(dest.rglob('*')) if p.is_file()]
    manifest=dict(status='AUTHOR_COMPLETE_L100_BROAD_PRIMITIVE_PREPARATION_V1_AWAITING_DISTINCT_REVIEW',exports=exports,
      export_count=len(exports),dependency_file='dependencies.json',target_runs=0,new_source_credit=0)
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(packet=str(dest),manifest=row(dest/'manifest.json',dest),exports=len(exports)),indent=2))
if __name__=='__main__':main()
