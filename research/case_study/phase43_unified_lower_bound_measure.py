#!/usr/bin/env python3
"""Measure the conservative six-source/full-seven-source PDF-extraction lower bound.
Only writes to a NEW private output directory; does not copy source texts/PDFs.
Exact source hashes, body/exclusion spans and full replacement are fixed by the
bound protocol. This checks length/render integrity, not mathematical truth.
"""
from __future__ import annotations
import argparse, collections, hashlib, importlib.util, io, json, logging, os
from pathlib import Path
import platform, re, shutil, subprocess, sys, unicodedata
HERE=Path(__file__).resolve().parent
PROTOCOL_NAME='phase43_unified_lower_bound_protocol.json'
PROTOCOL_SHA256='8c6459c1ed938f3bc8979579775b66f4b12af317029887e542e7338776dae4c0'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read_bound(path,expected):
 b=path.read_bytes()
 if sha(b)!=expected:raise ValueError(f'Hash mismatch: {path}')
 return b
def write_json(path,obj):
 with path.open('x',encoding='utf-8') as f:json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n')
def program_info(name):
 located=shutil.which(name)
 if not located:raise RuntimeError(f'Missing executable: {name}')
 path=Path(located).absolute();binary=path.resolve()
 v=subprocess.run([str(path),'--version'],capture_output=True,text=True,check=True)
 return {'path':str(path),'binary_realpath':str(binary),'sha256':sha(binary.read_bytes()),'first_line':v.stdout.splitlines()[0],'version_output':v.stdout.strip()}
def ast_info(node):
 counts=collections.Counter();codes=[];tables=[]
 def visit(n):
  if isinstance(n,dict):
   typ=n.get('t');counts[typ]+=1
   if typ=='Math':counts['inline_math' if n['c'][0]['t']=='InlineMath' else 'display_math']+=1
   if typ=='Str':counts['qed_marks']+=n['c'].count('∎')
   if typ=='CodeBlock':codes.append(n['c'][1])
   if typ=='Table':tables.append(n)
   for v in n.values():visit(v)
  elif isinstance(n,list):
   for v in n:visit(v)
 visit(node)
 return {'inline_math':counts['inline_math'],'display_math':counts['display_math'],'qed_marks':counts['qed_marks'],'tables':counts['Table'],'images':counts['Image'],'figures':counts['Figure'],'code_blocks':len(codes),'code_sha256':[sha(x.encode()) for x in codes],'code_lines':[len(x.splitlines()) for x in codes]},codes
def extract(reader):
 stream=io.StringIO();handler=logging.StreamHandler(stream);logger=logging.getLogger('pypdf');logger.addHandler(handler)
 try:pages=[page.extract_text() or '' for page in reader.pages]
 finally:logger.removeHandler(handler)
 return '\n'.join(pages),pages,stream.getvalue().splitlines()
def extract_primary(path,pypdf):
 stream=io.StringIO();handler=logging.StreamHandler(stream);logger=logging.getLogger('pypdf');old=logger.propagate;logger.propagate=False;logger.addHandler(handler)
 try:
  reader=pypdf.PdfReader(path);text,pages,_=extract(reader)
 finally:logger.removeHandler(handler);logger.propagate=old
 return text,pages,stream.getvalue().splitlines()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--input-root',type=Path,default=HERE);ap.add_argument('--protocol',type=Path,default=HERE/PROTOCOL_NAME);ap.add_argument('--output-dir',type=Path,required=True);ap.add_argument('--allow-toolchain-drift',action='store_true');ap.add_argument('--rasterize',action='store_true',help='Produce all-page PNGs with Ghostscript for a separate human visual review')
 args=ap.parse_args();root=args.input_root.resolve();out=args.output_dir.expanduser().absolute()
 if os.path.lexists(out):raise FileExistsError(f'Refusing existing output directory: {out}')
 p=json.loads(read_bound(args.protocol,PROTOCOL_SHA256));h=p['measurement_helper'];read_bound(root/h['path'],h['sha256'])
 spec=importlib.util.spec_from_file_location('bound_measurement',root/h['path']);m=importlib.util.module_from_spec(spec);sys.dont_write_bytecode=True;spec.loader.exec_module(m)
 import pypdf
 programs={name:program_info(name) for name in ['pandoc','xelatex']+(['gs'] if args.rasterize else [])};drift={}
 for name in ['pandoc','xelatex']:
  if programs[name]['first_line']!=p['expected_toolchain'][name+'_first_line']:drift[name]=programs[name]['first_line']
 if pypdf.__version__!=p['expected_toolchain']['pypdf']:drift['pypdf']=pypdf.__version__
 if drift and not args.allow_toolchain_drift:raise RuntimeError('Toolchain drift: '+json.dumps(drift))
 for b in p['contract_bindings']+p['external_costs']:read_bound(root/b['path'],b['sha256'])
 docs={};bodies={}
 for key in p['source_keys']:
  s=p['documents'][key];read_bound(root/s['pdf_path'],s['pdf_sha256']);text,pages,warnings=extract_primary(root/s['pdf_path'],pypdf)
  if s.get('extraction_format')=='N003_legacy_markers':text=''.join(f'\n--- PDF PAGE {i+1} ---\n'+q+'\n' for i,q in enumerate(pages))
  if s.get('extraction_format')=='N008_legacy_markers':text='\n\n'.join(f'[[PDF PAGE {i+1}; PRINTED {169+i}]]\n'+q for i,q in enumerate(pages))
  if sha(text.encode())!=s['extraction_sha256']:raise ValueError('Fresh primary extraction differs: '+key)
  if len(pages)!=s['pages']:raise ValueError('Primary page count differs: '+key)
  if warnings!=s['expected_extraction_warnings']:raise ValueError('Primary extraction warnings differ: '+key)
  for page,ps in zip(pages,s['page_spans']):
   if sha(page.encode())!=ps['sha256_utf8']:raise ValueError('Page extraction hash differs: '+key)
  body,ex=m.body_text(text,s);bodies[key]=body
  docs[key]={'pdf_path':s['pdf_path'],'pdf_sha256':s['pdf_sha256'],'pdf_bytes':s['pdf_bytes'],'pdf_pages':len(pages),'body_pages':s['body_pages'],'fresh_extraction_sha256':sha(text.encode()),'extraction_warnings':warnings,'selected_body':s['body'],'exclusions':ex,'cleaned_body_sha256':sha(body.encode()),'metrics':{f:m.metrics(body,f) for f in p['forms']},'nonwhitespace_control_codepoints':sorted({ord(c) for c in body if ord(c)<32 and not c.isspace()})}
 s=p['documents']['Compress_Unified'];text=read_bound(root/s['path'],s['sha256']).decode();body,_=m.body_text(text,s);out.mkdir(parents=False);(out/'replacement.md').write_text(body);(out/'qed.tex').write_text(p['render']['header'])
 if sha(p['render']['header'].encode())!=p['render']['header_sha256']:raise ValueError('Header hash mismatch')
 cmds=[]
 def run(label,argv):
  r=subprocess.run(argv,cwd=out,capture_output=True,text=True);(out/(label+'.stdout.txt')).write_text(r.stdout);(out/(label+'.stderr.txt')).write_text(r.stderr);cmds.append({'label':label,'argv':argv,'cwd':str(out),'returncode':r.returncode})
  if r.returncode:raise RuntimeError(f'{label} failed; inspect {out}')
  return r
 pandoc=programs['pandoc']['path'];readeropt='--from='+p['render']['reader']
 run('ast',[pandoc,'replacement.md',readeropt,'--to=json','--output=ast.json']);ast=ast_info(json.loads((out/'ast.json').read_text()));ai,codes=ast
 if ai!=p['expected_rendering']['ast']:raise ValueError('AST differs from full-body rendering contract')
 raw_code=re.findall(r'```gap\n(.*?)\n```',body,re.S)
 if codes!=raw_code:raise ValueError('Appendix code changed or disappeared in AST')
 options=[readeropt,'--standalone','--to=latex','--include-in-header=qed.tex']
 for v in p['render']['variables']:options+=['--variable',v]
 template=run('template',[pandoc,'--print-default-template=latex']);(out/'default-template.tex').write_text(template.stdout)
 run('latex',[pandoc,'replacement.md',*options,'--output=replacement.tex'])
 # Direct passes expose all LaTeX warnings; successful Pandoc PDF creation alone
 # does not expose overfull boxes or first-pass table-width diagnostics.
 pass_warnings=[]
 for n in [1,2]:
  run(f'xelatex-pass{n}',[programs['xelatex']['path'],'-interaction=nonstopmode','-halt-on-error','-recorder','replacement.tex'])
  log=(out/'replacement.log').read_text();(out/f'xelatex-pass{n}.log').write_text(log)
  pass_warnings.append([line for line in log.splitlines() if re.search(r'Warning:|Overfull \\[hv]box|Underfull \\[hv]box|Missing character:|Missing glyph',line,re.I)])
 if pass_warnings[-1]:raise RuntimeError('Final LaTeX diagnostics require review: '+json.dumps(pass_warnings[-1]))
 reader=pypdf.PdfReader(out/'replacement.pdf');rendered,pages,warnings=extract(reader);(out/'replacement_extraction.txt').write_text(rendered)
 if warnings:raise RuntimeError('Replacement extraction warnings: '+str(warnings))
 if rendered.count('■')!=ai['qed_marks']:raise ValueError('Proof-end mark loss')
 # Code token spelling and sequence must survive extraction (only whitespace ignored).
 appendix=rendered[rendered.index('ids :='):];end=appendix.index('Assert(0,counts=[64,4,16,8]);')+len('Assert(0,counts=[64,4,16,8]);');pdf_code=appendix[:end]
 if re.sub(r'\s+','',pdf_code)!=re.sub(r'\s+','',codes[0]):raise ValueError('Census code token loss in PDF extraction')
 rendered_metrics={f:m.metrics(rendered,f) for f in p['forms']};baseline=p['expected_rendering'];checks={'pages':len(pages)==baseline['pages'],'extraction_hash':sha(rendered.encode())==baseline['extraction_sha256'],'metrics':rendered_metrics==baseline['metrics'],'all_qed_marks':True,'complete_appendix_code_tokens':True,'final_latex_diagnostics_empty':True,'source_extractions_exact':True}
 if not all(checks.values()) and not args.allow_toolchain_drift:raise ValueError('Rendered baseline changed: '+str(checks))
 if args.rasterize:
  r=run('rasterize',[programs['gs']['path'],'-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r130','-sOutputFile=page-%02d.png','replacement.pdf'])
  if re.search(r'Error|Warning|repair',r.stdout+'\n'+r.stderr,re.I):raise RuntimeError('Rasterizer diagnostic requires review')
 sums={f:{k:sum(docs[d]['metrics'][f][k] for d in p['source_keys']) for k in p['metric_keys']} for f in p['forms']};ratios={f:{k:{'numerator':sums[f][k],'denominator':rendered_metrics[f][k],'factor':sums[f][k]/rendered_metrics[f][k]} for k in p['metric_keys']} for f in p['forms']}
 fonts=set()
 for page in reader.pages:
  for ref in page['/Resources'].get_object().get('/Font',{}).get_object().values():
   font=ref.get_object();fonts.add(str(font.get('/BaseFont')))
 tex_inputs={}
 for line in (out/'replacement.fls').read_text().splitlines():
  if line.startswith('INPUT '):
   q=Path(line[6:]);q=q if q.is_absolute() else out/q
   if q.is_file() and out not in q.resolve().parents:tex_inputs[str(q.resolve())]=sha(q.read_bytes())
 report={'schema':'six_source_full_unified_conservative_lower_bound_v1','status':'reproducible_author_measurement_pending_independent_review','protocol_sha256':PROTOCOL_SHA256,'runner_sha256':sha(Path(__file__).read_bytes()),'output_directory':str(out),'environment':{'python':sys.version,'python_executable':sys.executable,'platform':platform.platform(),'unicode_database':unicodedata.unidata_version,'pypdf_version':pypdf.__version__,'pypdf_module_sha256':sha(Path(pypdf.__file__).read_bytes()),'programs':programs,'toolchain_drift':drift},'contract':p['contract'],'contract_bindings':p['contract_bindings'],'source_documents':docs,'source_body_sums':sums,'replacement':{'input':s,'raw_markdown_metrics':{f:m.metrics(body,f) for f in p['forms']},'rendered_metrics':rendered_metrics,'rendered_extraction_sha256':sha(rendered.encode()),'pages':len(pages),'entire_Appendix_A_included':True},'conservative_lower_bounds_under_declared_convention':ratios,'N001_credit':0,'exact_seven_source_factor':None,'rendering':{'ast':ai,'commands':cmds,'xelatex_pass_diagnostics':pass_warnings,'embedded_font_names':sorted(fonts),'tex_input_hashes':tex_inputs,'checks':checks,'rasterized_all_pages':args.rasterize,'visual_review_automated':False},'external_costs':p['external_costs'],'counting_convention':p['counting_convention'],'source_text_exported':False,'source_pdf_exported':False,'whole_document_equivalence_claim':False,'mathematical_proof_check_performed_by_this_runner':False}
 write_json(out/'report.json',report);write_json(out/'manifest.json',{'files':{f.name:sha(f.read_bytes()) for f in sorted(out.iterdir()) if f.is_file()},'source_text_or_pdf_included':False})
 print(json.dumps({'status':report['status'],'report_sha256':sha((out/'report.json').read_bytes()),'NFC':ratios['NFC'],'NFKC':ratios['NFKC'],'checks':checks},indent=2))
if __name__=='__main__':main()
