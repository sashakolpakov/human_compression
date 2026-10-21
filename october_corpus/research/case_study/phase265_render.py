#!/usr/bin/env python3
"""Render the umbrella and its complete application; no page-based compression statistic."""
import argparse,hashlib,json,re,shutil,subprocess
from pathlib import Path
import pypdf
ROOT=Path(__file__).resolve().parent
FILES=['phase265_flag_relations.md','phase265_triangle_application.md']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,s):
 if not ok:raise RuntimeError(s)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 need(not a.out.exists() and not a.out.is_symlink(),'fresh directory required');a.out.mkdir(parents=True);out=a.out.resolve()
 config=json.loads((ROOT/'phase265_render_config.json').read_text());report={}
 for name in FILES:
  source=ROOT/name;before=sha(source);d=out/source.stem;d.mkdir();(d/'paper.md').write_text(source.read_text());(d/'header.tex').write_text(config['header'])
  cmd=[shutil.which('pandoc'),'paper.md','--from='+config['reader'],'--standalone','--pdf-engine=xelatex','--include-in-header=header.tex','-o','paper.pdf']
  for var in config['variables']:cmd.extend(['-V',var])
  r=subprocess.run(cmd,cwd=d,text=True,capture_output=True,timeout=120);(d/'render.stdout').write_text(r.stdout);(d/'render.stderr').write_text(r.stderr)
  need(r.returncode==0,'render failed '+name+': '+r.stderr)
  diagnostics=[z for z in r.stderr.splitlines() if re.search(r'Warning|Overfull|Missing character|Missing glyph',z,re.I)]
  pdf=pypdf.PdfReader(d/'paper.pdf');(d/'extraction.txt').write_text('\n'.join(p.extract_text() or '' for p in pdf.pages))
  need(len(pdf.pages)>0,'empty PDF')
  raster=[shutil.which('gs'),'-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r95','-sOutputFile=page-%02d.png','paper.pdf']
  r=subprocess.run(raster,cwd=d,text=True,capture_output=True,timeout=120);need(r.returncode==0,'raster failed')
  need(sha(source)==before,'source changed')
  report[name]={'source_sha256':before,'pages':len(pdf.pages),'pdf_sha256':sha(d/'paper.pdf'),'diagnostics':diagnostics,'command':cmd}
 (out/'report.json').write_text(json.dumps({'status':'rendered_visual_inspection_separate','papers':report,'ratio':None},indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
