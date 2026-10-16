"""Audit L114 source assembly; mathematical completeness needs distinct review."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys,time
if not __debug__:raise SystemExit('optimization is not an admitted execution mode')
C=Path(__file__).resolve().parent
def need(test,message):
    if not test: raise ValueError(message)

def load(path): return json.loads(path.read_text())

def binding(path,base=None):
    b=path.read_bytes()
    return dict(path=str(path.relative_to(base) if base else path),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def verify(row,base=None):
    path=Path(row['path']) if base is None else base/row['path']
    need(binding(path,base)==row,'binding changed: '+str(path))

def normalized(page): return ''.join(page.extract_text().split())

def compare_pdfs(first,second):
    from pypdf import PdfReader
    a,b=PdfReader(first),PdfReader(second)
    need(len(a.pages)==len(b.pages),'native page count changed')
    for i,(x,y) in enumerate(zip(a.pages,b.pages)):
        need(normalized(x)==normalized(y),'native text changed: '+str(first)+' page '+str(i+1))

def embedded_page_check(source,container):
    forms=[x.get_object() for x in container['/Resources']['/XObject'].values()]
    need(len(forms)==1,'one imported form required')
    form=forms[0]
    need(form.get_data()==source.get_contents().get_data(),'imported drawing stream changed')
    a,b=source['/Resources']['/Font'],form['/Resources']['/Font']
    need(set(a)==set(b),'page font resources changed')
    for name in a:
        x,y=a[name].get_object(),b[name].get_object()
        need(x['/Subtype']==y['/Subtype'],'font type changed')
        dx,dy=x['/FontDescriptor'].get_object(),y['/FontDescriptor'].get_object()
        for key in ['/FontFile','/FontFile2','/FontFile3']:
            need((key in dx)==(key in dy),'font program presence changed')
            if key in dx: need(dx[key].get_data()==dy[key].get_data(),'glyph program changed')

def ledger_check(d):
 need(d['source_id']=='L114','source id')
 rows=d['claims'];need(len(rows)==61 and len({r['label'] for r in rows})==61,'missing or repeated claim')
 for r in rows:
  need(r['physical_pages'] and all(1<=x<=21 for x in r['physical_pages']),'source page')
  need(all(r[k] for k in ['status','proof','qualification','attribution']),'incomplete claim record')
 by={r['label']:r for r in rows}
 expected={'Theorem 5.5 exhaustive list':'PRINCIPAL_STATEMENT_ALREADY_REFUTED','Theorem 5.4':'REPROVED_FULL_RANK_RANGE','Theorem 6.1: q8 thinness':'REFUTED_LITERAL_ALGEBRAIC_LOCAL_VERSION','Theorem 6.1: prime-q−1>7 thinness':'REFUTED_LITERAL_ALGEBRAIC_LOCAL_VERSION','Introduction and Theorem 6.1: universal local rank bound':'REFUTED_BY_UNBOUNDED_PREGEOMETRY_FAMILY','Introduction and Theorem 6.1: rank3 only for prime q−1':'REFUTED_BY_RANK3_GEOMETRY','Theorem 5.1: dihedral catalogue and diagrams':'EXPLICIT_CITED_PREMISE','Table 4 row 16':'CORRECTED_CENTRAL_FAMILY'}
 for label,status in expected.items():need(by[label]['status']==status,'source correction hidden: '+label)
 for p in range(1,11):
  status='INTERSECTIONS_IMPOSSIBLE' if p in [1,2,3,5] else ('INTERSECTIONS_EXIST_RWPRI_IMPOSSIBLE' if p==9 else 'UNIFORM_RWPRI_EXISTENCE')
  need(by['Theorem 5.5 pattern '+str(p)+' realization']['status']==status,'pattern disposition')
 need(d['principal_disposition']=='principal_statement_refuted','principal disposition')
 for key in ['ordinary_recovery_credit','new_principal_refutation_credit','new_original_credit','new_named_open_questions_solved','new_Lean_declarations','new_measurements','new_scientific_acquisitions_in_assembly']:need(d[key]==0,'unearned credit '+key)
 for key in ['public_registration_performed','principal_acquisition_repeated']:need(d[key] is False,'unauthorized scope '+key)
 need(d['remaining_fixed_paper_mathematical_claims']==[],'unresolved source claim')
 need(len(d['borrowed_premises'])==4 and len(d['uncertified_extensions'])==4,'premises/limits missing')
 need('higher-rank' in ' '.join(d['uncertified_extensions']).lower(),'higher-rank scope promoted')

def imports_check(rows):
 need(len(rows)==28,'exact proof imports')
 for r in rows:
  verify(r['source']);verify(r['destination'],C)
  need(r['mode']=='EXACT','unrecorded proof edition')
  need(Path(r['source']['path']).read_bytes()==(C/r['destination']['path']).read_bytes(),'proof changed')

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--render',action='store_true');args=p.parse_args()
 out=Path(args.out).resolve();need(not out.exists() and not out.is_relative_to(C),'fresh separate output required')
 need(shutil.disk_usage(C).free>=4*1024**3,'hold below4GiB reserve')
 start=time.monotonic();deps=load(C/'dependencies.json')
 for r in deps:verify(r)
 if (C/'manifest.json').exists():
  for r in load(C/'manifest.json')['exports']:verify(r,C)
 gates=load(C/'gates.json');need(len(gates)==13,'accepted gate count')
 for g in gates:
  verify(g['manifest']);need(load(Path(g['manifest']['path']))['status']==g['status'],'gate changed')
 need(any('UNBOUNDED' in g['status'] or 'LOCAL_RANK' in g['status'] for g in gates),'local rank gate missing')
 ledger=load(C/'claims.json');ledger_check(ledger)
 imports=load(C/'imports.json');imports_check(imports)
 editions=load(C/'edition_deltas.json');need(editions['accepted_proofs_modified'] is False,'unrecorded accepted edition')
 for r in editions['realizations_old_inputs']:verify(r)
 controls=[]
 def remove_bound(x):
  row=next(r for r in x['claims'] if r['label']=='Introduction and Theorem 6.1: universal local rank bound');row['status']='UNPROVED'
 for name,change in [('missing_claim',lambda x:x['claims'].pop()),('second_principal_credit',lambda x:x.update(new_principal_refutation_credit=1)),('ordinary_recovery_credit',lambda x:x.update(ordinary_recovery_credit=1)),('rank_bound_hidden',remove_bound),('stronger_variant_promoted',lambda x:x.update(uncertified_extensions=[]))]:
  bad=copy.deepcopy(ledger);change(bad)
  try:ledger_check(bad)
  except ValueError:controls.append(name)
  else:raise ValueError('damaged ledger accepted '+name)
 bad=copy.deepcopy(imports);bad[0]['mode']='EDITED'
 try:imports_check(bad)
 except ValueError:controls.append('edited_proof_rejected')
 else:raise ValueError('edited proof accepted')
 from pypdf import PdfReader
 parts=load(C/'parts.json');need(len(parts)==16,'part count')
 whole=PdfReader(C/'complete.pdf');need(len(whole.pages)==68,'volume length')
 offset=1
 for r in parts:
  part=PdfReader(C/r['path']);need(r['first_page']==offset+1 and len(part.pages)==r['pages'],'part order/length')
  for i,page in enumerate(part.pages):embedded_page_check(page,whole.pages[offset+i])
  offset+=len(part.pages)
 need(offset==len(whole.pages),'unaccounted pages')
 for flag in ['-O','-OO']:
  run=subprocess.run([sys.executable,flag,str(C/'check.py')],capture_output=True,timeout=10)
  need(run.returncode!=0 and b'optimization is not an admitted execution mode' in run.stderr,'optimization guard')
  controls.append(flag+'_rejected')
 out.mkdir(parents=True);runs=[]
 if args.render:
  native=out/'native';(native/'proofs').mkdir(parents=True)
  for f in sorted(C.glob('*.tex'))+sorted((C/'proofs').glob('*.tex')):shutil.copyfile(f,native/f.relative_to(C))
  # Rebuild every exact TeX input, then the assembly. PDF metadata can differ;
  # page text, drawing streams and glyph programs are checked separately.
  rels=[r['path'][:-4] for r in parts]+['complete']
  for rel in rels:
   stem=native/rel
   for n in [1,2]:
    cmd=['/opt/homebrew/bin/pdflatex','-interaction=nonstopmode','-halt-on-error',stem.name+'.tex'];t=time.monotonic();run=subprocess.run(cmd,cwd=stem.parent,capture_output=True,timeout=30)
    stem.with_name(stem.name+'-pass'+str(n)+'.stdout').write_bytes(run.stdout);stem.with_name(stem.name+'-pass'+str(n)+'.stderr').write_bytes(run.stderr)
    need(run.returncode==0,'native TeX failed '+rel);runs.append(dict(stem=rel,pass_number=n,seconds=time.monotonic()-t,returncode=run.returncode))
   if rel in ['completion','realizations','complete']:
    log=stem.with_suffix('.log').read_text();need('Overfull' not in log and 'undefined' not in log,'new document warning '+rel)
   compare_pdfs(C/(rel+'.pdf'),stem.with_suffix('.pdf'))
  cmd=['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile='+str(out/'complete-%02d.png'),str(native/'complete.pdf')]
  run=subprocess.run(cmd,capture_output=True,timeout=45);(out/'render.stdout').write_bytes(run.stdout);(out/'render.stderr').write_bytes(run.stderr)
  need(run.returncode==0 and len(list(out.glob('complete-*.png')))==68,'native render')
 for r in deps:verify(r)
 report=dict(status='PASS_L114_COMPLETE_SOURCE_ASSEMBLY',dependencies=len(deps),accepted_gates=len(gates),source_claims=61,volume_pages=68,exact_proof_imports=28,embedded_page_streams_and_glyph_programs_match=True,controls=controls,runs=runs,seconds=time.monotonic()-start,new_acquisitions=0,public_mutations=0,new_Lean=0,measurements=None,general_proofs='REQUIRE_DISTINCT_MATHEMATICAL_REVIEW',outputs=[binding(f,out) for f in sorted(out.rglob('*')) if f.is_file()])
 (out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:report[k] for k in ['status','dependencies','source_claims','volume_pages','controls','seconds']}))
if __name__=='__main__':main()
