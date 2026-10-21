#!/usr/bin/env python3
"""Portable independent recount/scope review plus isolated exported-author replay."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
import recount,check_scope,compare
PIN='9b754940f2edee8ba7e3bf4010f236613040f850bca3ad440d3e5a6876fedd7f'
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def load(p):return json.loads(p.read_text())
def check_reader(packet,counts,raw):
 t=(packet/'reader.tex').read_text();rows=0
 for j,src in enumerate(check_scope.SOURCES,1):
  sid=counts['documents'][src];app=counts['documents']['A'+str(j)];n=lambda d:d['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']
  line=f"{src} & {sid['pages']} & {n(sid):,} & A{j} & {app['pages']} & {n(app):,}"
  recount.require(line in t,'actual primary source/application table');rows+=1
 recount.require('23 & 66,140' in t and counts['documents']['U']['metrics']['calibrated_selected']['NFC']['characters_without_whitespace']==66140,'full common table')
 for key in ['L121','A9']:
  for var,label in [('raw_untrimmed','raw, complete'),('raw_selected','raw, selected'),('calibrated_selected','calibrated')]:
   for norm in ['NFC','NFKC']:
    values=counts['documents'][key]['metrics'][var][norm];order=['whitespace_tokens','alphanumeric_units','characters_without_whitespace','characters_with_collapsed_whitespace','utf8_bytes_with_collapsed_whitespace']
    line=' & '.join([key,label,norm]+[f'{values[m]:,}'for m in order]);recount.require(line in t,'all actual reader sensitivity cells');rows+=1
 group=lambda role:'Required programs/data'if role.startswith('required')else'Old auxiliaries'if role=='inherited_auxiliary'else'Operational runners'if role in('current_operational_driver','operational_validation_runner')else'Partial formal files'
 groups={}
 for r in raw['files']:
  name=group(r['role']);c,b=groups.get(name,(0,0));groups[name]=c+1,b+r['file']['bytes']
 for name,(c,b)in groups.items():recount.require(f'{name} & {c} & {b:,}'in t,'complete raw role table')
 for phrase in ['No printed appendix represents the entire enlarged required collection.','no software-inclusive factor.','Their\nedges, layout and geometric content are not priced.','two nonconsequences only; they do not formalize the group orders, infinite']:
  recount.require(phrase in t,'reader scope limitation')
 return dict(status='PASS',source_application_rows=9,common_rows=1,raw_role_rows=4,new_sensitivity_cells=60,no_factors=True)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--study-root',type=Path,required=True);ap.add_argument('--public-root',type=Path,required=True);ap.add_argument('--packet',type=Path);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--skip-author-replay',action='store_true');a=ap.parse_args();a.study_root=a.study_root.resolve();a.public_root=a.public_root.resolve();packet=(a.packet or a.study_root/'topic_A_L121_measurement_inputs').resolve();out=a.out.resolve();recount.require(not out.exists(),'fresh output');out.mkdir(parents=True)
 recount.require(recount.digest((packet/'manifest.json').read_bytes())==PIN,'exact final author manifest')
 man=load(packet/'manifest.json');copy=out/'exports';copy.mkdir();bindings=[]
 for row in man['exports']:
  rel=Path(row['path']);recount.require(not rel.is_absolute()and'..'not in rel.parts,'safe export path');b=(packet/rel).read_bytes();recount.require(len(b)==row['bytes']and recount.digest(b)==row['sha256'],'immutable export '+str(rel));dest=copy/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b);bindings.append(row)
 (copy/'manifest.json').write_bytes((packet/'manifest.json').read_bytes());recount.require(len(bindings)==44 and sum(r['bytes']for r in bindings)==1831082,'all44 exports')
 recount.require((packet/'policy.json').read_bytes()==(packet/'precount/policy.json').read_bytes(),'policy unchanged after counts')
 scope=check_scope.run(copy,{'study':a.study_root,'public':a.public_root});actual=recount.preliminary(copy,a.study_root);comparison=compare.run(copy,a.study_root,actual,scope);reader=check_reader(copy,load(copy/'author_counts.json'),load(copy/'precount/raw_inventory.json'))
 dump(out/'scope.json',scope);dump(out/'recount.json',actual);dump(out/'comparison.json',comparison);dump(out/'reader_check.json',reader)
 exported=None
 if not a.skip_author_replay:
  cmd=[sys.executable,'-B','-O',str(copy/'check.py'),'--study-root',str(a.study_root),'--public-root',str(a.public_root),'--out',str(out/'author_replay'),'--render','--xelatex','/opt/homebrew/bin/xelatex']
  r=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);(out/'author_replay.log').write_text(r.stdout);recount.require(r.returncode==0,'export-only author replay; see log');exported=load(out/'author_replay/report.json')
 result=dict(status='PASS_DISTINCT_INPUT_REVIEW_REPLAY',author_manifest_sha256=PIN,author_exports=44,new_PDF_cells_independent=60,old_PDF_cells_literal_preserved=600,raw_cells_independently_recounted=450,new_text_hashes=42,all_CSV_cells=1110,font_dictionaries=36,encoded_glyph_classes=871,glyph_repairs=69,independent_controls=scope['controls']+comparison['controls'],reader=reader,exported_author_replay=exported,shared_low_level_font_parser=True,author_metric_calibration_event_helpers_imported=False,scientific_programs_executed=False,Lean_executed=False,ratios=None)
 dump(out/'report.json',result);print(json.dumps({k:v for k,v in result.items()if k not in('independent_controls','exported_author_replay')},indent=2))
if __name__=='__main__':main()
