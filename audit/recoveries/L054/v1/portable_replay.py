"""Run the exact accepted join with an explicit archive-only JSON input interface."""
from pathlib import Path
import argparse,importlib.util,json,sys
sys.dont_write_bytecode=True
S='/Users/sasha/medusa/research/leemans';A=S+'/algebra/subgroup_atlas'
def need(b,m):
    if not b:raise ValueError(m)
def mapped_reader(mapping,root):
    def read(path):
        key=str(path);need(key in mapping,'explicit supplied input required; no private fallback')
        relative=mapping[key];p=(root/relative).resolve();need(p.is_relative_to(root.resolve()),'selected path remains inside extraction')
        return json.loads(p.read_text())
    return read

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--selected',required=True,type=Path);ap.add_argument('--mapping',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);x=ap.parse_args()
    mapping=json.loads(x.mapping.read_text());script=x.selected/mapping[A+'/principal_v2/audit.py']
    spec=importlib.util.spec_from_file_location('accepted_l054_audit',script);audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
    audit.P=Path(A+'/principal_v2');audit.A=Path(A);audit.read=mapped_reader(mapping,x.selected)
    result=audit.run();need(not x.out.exists(),'fresh portable join report');x.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
