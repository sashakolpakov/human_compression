#!/usr/bin/env python3
"""Author semantic mutation and no-clobber controls for the label-eight collector."""
import argparse,hashlib,importlib.util,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
COLLECTOR_SHA='f9d8b925b982484635e717cefde854e2999bb5d6d02cef569af28da53de5f12c'

def require(ok,message):
    if not ok:raise ValueError(message)

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output-dir',type=Path,required=True)
    args=parser.parse_args();out=args.output_dir.absolute();require(not out.exists() and not out.is_symlink(),'Fresh control directory required');out.mkdir(parents=True)
    source=BASE/'phase161_label_eight_collector.py';require(sha(source)==COLLECTOR_SHA,'Frozen collector changed')
    spec=importlib.util.spec_from_file_location('checked_label_eight_collector',source);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    reports=[]
    for name in ['omitted_left_tail','omitted_edge_commutator','omitted_triple_commutator','collapsed_edge_square','unsupported_power','nontriangular_power']:
        C=module.Collector(14);p=C.position
        if name=='omitted_left_tail':C.rules[p['x',1],p['r',0]]=(p['r',0],p['x',1],p['y',0],p['w',0])
        elif name=='omitted_edge_commutator':C.rules[p['x',1],p['x',0]]=(p['x',0],p['x',1])
        elif name=='omitted_triple_commutator':C.rules[p['y',0],p['r',1]]=(p['r',1],p['y',0])
        elif name=='collapsed_edge_square':C.rules[p['x',0],p['x',0]]=()
        elif name=='unsupported_power':C.rules[p['x',0],p['x',0]]=(p['w',12],)
        else:C.rules[p['x',0],p['x',0]]=(p['x',0],)
        expected=('Rule creates unsupported coordinates' if name=='unsupported_power' else 'Power rule is not triangular' if name=='nontriangular_power' else 'Critical pair failed')
        try:C.verify_rules();C.critical_pairs()
        except ValueError as error:
            require(expected in str(error),'Wrong failure for '+name);reports.append({'case':name,'rejected':True,'diagnostic':str(error)})
        else:raise ValueError('Mutation accepted: '+name)
    def reject(name,target):
        run=subprocess.run([sys.executable,'-B','-O',str(source),'--report',str(target)],capture_output=True,text=True,timeout=10)
        require(run.returncode!=0 and 'Fresh report required' in run.stderr,'No-clobber control failed: '+name)
        reports.append({'case':name,'exit_code':run.returncode,'stderr':run.stderr})
    regular=out/'regular';regular.write_bytes(b'keep file\n');digest=sha(regular);reject('occupied_regular',regular);require(sha(regular)==digest,'Regular output changed')
    directory=out/'directory';directory.mkdir();marker=directory/'marker';marker.write_bytes(b'keep directory\n');mdigest=sha(marker);reject('occupied_directory',directory);require(list(directory.iterdir())==[marker] and sha(marker)==mdigest,'Directory output changed')
    live=out/'live';live.symlink_to(regular);reject('live_symlink',live);require(live.is_symlink() and live.readlink()==regular and sha(regular)==digest,'Live link changed')
    missing=out/'missing';dangling=out/'dangling';dangling.symlink_to(missing);reject('dangling_symlink',dangling);require(dangling.is_symlink() and dangling.readlink()==missing and not missing.exists(),'Dangling link changed')
    require(sha(source)==COLLECTOR_SHA,'Collector changed during controls')
    result={'status':'PASS','controls':reports,'control_count':len(reports),'collector_sha256':COLLECTOR_SHA,'control_source_sha256':sha(Path(__file__)),'author_controls_not_independent_review':True}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','controls':len(reports)},indent=2))
if __name__=='__main__':main()
