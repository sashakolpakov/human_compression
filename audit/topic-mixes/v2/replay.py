#!/usr/bin/env python3
"""Public-path adapter; never executes scientific programs or extracts source PDFs."""
from pathlib import Path
import argparse,json,subprocess,sys

def main():
 p=argparse.ArgumentParser();p.add_argument('--repo',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',type=Path,default=Path('/opt/homebrew/bin/xelatex'));a=p.parse_args()
 if a.out.exists():raise ValueError('Fresh output directory required')
 a.out.mkdir(parents=True);a.out=a.out.resolve();repo=a.repo.resolve();base=repo/'audit/topic-mixes/v2'
 locations=json.loads((base/'public_locations.json').read_text());study=a.out/'accepted_inputs';study.mkdir()
 for name,rel in locations['numerical_study_aliases'].items():
  target=repo/rel
  if not target.is_dir():raise ValueError('Missing public packet '+rel)
  (study/name).symlink_to(target,target_is_directory=True)
 cmd=[sys.executable,'-B','-O',str(base/'measurement/review/check.py'),'--study',str(study),'--out',str(a.out/'distinct_numbers.json')]
 proc=subprocess.run(cmd,capture_output=True,text=True);(a.out/'distinct.log').write_text(proc.stdout+proc.stderr)
 if proc.returncode:raise ValueError('Distinct public numerical replay failed: '+proc.stdout+proc.stderr)
 result=json.loads((a.out/'distinct_numbers.json').read_text())
 if a.render:
  cmd=[sys.executable,'-B','-O',str(base/'measurement/packet/run.py'),'--inputs',str(base/'measurement/inputs'),'--prior-inputs',str(repo/'audit/topic-mixes/v1/measurement/inputs'),'--input-review',str(base/'measurement/input_review'),'--out',str(a.out/'rendered'),'--xelatex',str(a.xelatex)]
  proc=subprocess.run(cmd,capture_output=True,text=True);(a.out/'render.log').write_text(proc.stdout+proc.stderr)
  if proc.returncode:raise ValueError('Exact reader/render replay failed: '+proc.stdout+proc.stderr)
  result['exact_author_reader_replay']=json.loads((a.out/'rendered/report.json').read_text())
 result['adapter_scope']='Public path routing only. No scientific GAP/Lean or source-PDF extraction; exact previous scientific acceptances are reused.'
 (a.out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='exact_author_reader_replay'},indent=2))
if __name__=='__main__':main()
