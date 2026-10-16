"""Exact source assembly audit; mathematical completeness needs distinct review."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,subprocess,sys,time
if not __debug__:raise SystemExit('optimization is not an admitted execution mode')
C=Path(__file__).resolve().parent

def need(test,message):
    if not test:raise ValueError(message)

def load(p):return json.loads(p.read_text())

def binding(p,base=None):
    b=p.read_bytes()
    return dict(path=str(p.relative_to(base) if base else p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())

def verify(r,base=None):
    p=Path(r['path']) if base is None else base/r['path']
    need(binding(p,base)==r,'binding changed: '+str(p))

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
            if key in dx:need(dx[key].get_data()==dy[key].get_data(),'glyph program changed')

def ledger_check(d):
    sid=d['source_id'];need(sid in ['L063','L064'],'source id')
    size,count=(24,122) if sid=='L063' else (21,28)
    need(d['source_pages']==size,'source edition')
    rows=d['claims'];need(len(rows)==count and len({r['label'] for r in rows})==count,'missing or repeated source claim')
    proofs=set(load(C/'proof_routes.json'))|{'completion','partI'}
    for r in rows:
        need(r['physical_pages'] and all(type(p)==int and 1<=p<=size for p in r['physical_pages']),'invalid physical page')
        need(all(r[k] for k in ['status','proof','qualification','attribution']),'incomplete disposition')
        need(set(r['proof'])<=proofs,'unknown proof route')
    by={r['label']:r for r in rows}
    if sid=='L063':
        expected={(t,r) for t,n in enumerate([18,7,9,5,2,3],1) for r in range(1,n+1)}
        table=[r for r in rows if 'table' in r]
        need(len(table)==44 and {(r['table'],r['row']) for r in table}==expected,'source table coverage')
        arcs={(r['table'],r['row']):r['local_arc_length'] for r in load(C/'source_arc_rows.json')['rows']}
        need(all(r['local_arc_length']==arcs[r['table'],r['row']] for r in table),'arc column changed')
        for n in [12,13,14,18]:need(by[f'Table1 row{n}']['status']=='EMPTY_PARAMETER_BRANCH','empty branch promoted')
        for n in [6,7]:need(by[f'Table2 row{n}']['status']=='INNER_COUNT_CORRECTED','unordered correction lost')
        need(by['Proposition4.6 complete representation list']['status']=='CORRECTED_AND_REPROVED','missing S4 actions concealed')
        need(by['Table8 maximal subgroups in odd characteristic']['status']=='CLASSICAL_PREMISE_WITH_INDEX_CORRECTION','index correction lost')
        for p in [17,31,47,79]:need(by[f'Section6 S4/S4 full graph group q={p}']['status']=='FULL_GRAPH_GROUP_CORRECTED','full group correction lost')
        cross=[r for r in rows if 'source_table_rows' in r]
        need(len(cross)==9,'Table9 crossreferences missing')
        need(all((x['table'],x['row']) in expected for r in cross for x in r['source_table_rows']),'unknown Table9 target')
    else:
        need(by['Lemma21']['status']=='RECOVERED_WITH_COMPLETE_AFFINE_INTERPRETATION','appendix/published statement conflated')
        need(by['Proposition22 general even affine subcase']['status']=='PRINCIPAL_STATEMENT_ALREADY_REFUTED','principal disposition changed')
        need(by['Lemma24 item2 PGL exclusion']['status']=='AUXILIARY_ASSERTION_REFUTED','false auxiliary premise retained')
        for p in [19,20,21]:need(by[f'Proposition30 page{p} transporter denominator']['status']=='TRANSCRIPTION_CORRECTED','transcription correction lost')
    need(d['principal_disposition']=='principal_statement_refuted','principal disposition')
    for k in ['ordinary_recovery_credit','new_principal_refutation_credit','new_original_credit','new_named_open_questions_solved','new_Lean_declarations','new_measurements','new_scientific_acquisitions_in_assembly']:
        need(d[k]==0,'unearned credit '+k)
    need(d['public_registration_performed'] is False and d['principal_acquisition_repeated'] is False,'scope changed')
    need(d['remaining_fixed_paper_asserted_mathematical_claims']==[],'unresolved original claim')
    need(len(d['borrowed_premises'])==5 and len(d['uncertified_extensions'])==5,'attribution or limits missing')
    need(d['source_scope_conventions']['unordered_parabolics'] is True,'unordered source convention lost')

def imports_check(rows):
    need(len(rows)==20,'exact proof import count')
    for r in rows:
        verify(r['source']);verify(r['destination'],C)
        need(r['mode']=='EXACT','unrecorded proof change')
        need(Path(r['source']['path']).read_bytes()==(C/r['destination']['path']).read_bytes(),'proof bytes changed')

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--render',action='store_true');args=p.parse_args()
    out=args.out.resolve();need(not out.exists() and not out.is_relative_to(C),'fresh separate output required')
    need(shutil.disk_usage(C).free>=4*1024**3,'hold below4GiB reserve')
    started=time.monotonic();deps=load(C/'dependencies.json')
    for r in deps:verify(r)
    for r in load(C/'manifest.json')['exports']:verify(r,C)
    gates=load(C/'gates.json');need(len(gates)==11,'exact gate count')
    for g in gates:
        verify(g['manifest']);need(load(Path(g['manifest']['path']))['status']==g['status'],'acceptance changed')
    ledgers=[load(C/(sid+'_claims.json')) for sid in ['L063','L064']]
    for d in ledgers:ledger_check(d)
    imports=load(C/'imports.json');imports_check(imports)
    controls=[]
    for name,index,change in [
        ('missing_table',0,lambda d:d['claims'].pop()),
        ('ordered_convention',0,lambda d:d['source_scope_conventions'].update(unordered_parabolics=False)),
        ('new_principal_credit',1,lambda d:d.update(new_principal_refutation_credit=1)),
        ('ordinary_recovery_credit',0,lambda d:d.update(ordinary_recovery_credit=1)),
        ('missing_auxiliary_correction',1,lambda d:next(r for r in d['claims'] if r['label']=='Lemma24 item2 PGL exclusion').update(status='RECOVERED'))]:
        bad=copy.deepcopy(ledgers[index]);change(bad)
        try:ledger_check(bad)
        except ValueError:controls.append(name)
        else:raise ValueError('damaged ledger accepted '+name)
    bad=copy.deepcopy(imports);bad[0]['mode']='EDITED'
    try:imports_check(bad)
    except ValueError:controls.append('edited_proof_rejected')
    else:raise ValueError('edited proof accepted')
    from pypdf import PdfReader
    parts=load(C/'parts.json');need(len(parts)==11,'part count')
    whole=PdfReader(C/'complete.pdf');need(len(whole.pages)==1+sum(r['pages'] for r in parts),'volume length')
    offset=1
    for r in parts:
        part=PdfReader(C/r['path']);need(r['first_page']==offset+1 and len(part.pages)==r['pages'],'part order')
        for i,page in enumerate(part.pages):embedded_page_check(page,whole.pages[offset+i])
        offset+=len(part.pages)
    for flag in ['-O','-OO']:
        r=subprocess.run([sys.executable,flag,str(C/'check.py')],capture_output=True,timeout=10)
        need(r.returncode!=0 and b'optimization is not an admitted execution mode' in r.stderr,'optimization guard')
        controls.append(flag+'_rejected')
    out.mkdir(parents=True);runs=[]
    if args.render:
        native=out/'native';(native/'proofs').mkdir(parents=True)
        for f in list(C.glob('*.tex'))+list((C/'proofs').glob('*.tex'))+list((C/'proofs').glob('*.pdf')):shutil.copyfile(f,native/f.relative_to(C))
        for stem in ['completion','complete']:
            for n in (1,2):
                r=subprocess.run(['/opt/homebrew/bin/pdflatex','-recorder','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],cwd=native,capture_output=True,timeout=30)
                (native/f'{stem}-pass{n}.stdout').write_bytes(r.stdout);(native/f'{stem}-pass{n}.stderr').write_bytes(r.stderr)
                need(r.returncode==0,'native TeX failed');runs.append({'stem':stem,'pass':n,'returncode':r.returncode})
            need('Overfull' not in (native/(stem+'.log')).read_text(),'native layout warning')
            original=PdfReader(C/(stem+'.pdf'));rebuilt=PdfReader(native/(stem+'.pdf'))
            need([p.extract_text() for p in original.pages]==[p.extract_text() for p in rebuilt.pages],'native mathematical text changed')
        r=subprocess.run(['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r105','-sOutputFile='+str(out/'complete-%02d.png'),str(native/'complete.pdf')],capture_output=True,timeout=45)
        (out/'render.stdout').write_bytes(r.stdout);(out/'render.stderr').write_bytes(r.stderr)
        need(r.returncode==0 and len(list(out.glob('complete-*.png')))==len(whole.pages),'native rendering failed')
    for r in deps:verify(r)
    report=dict(status='PASS_L063_L064_COMPLETE_SOURCE_ASSEMBLY',dependencies=len(deps),accepted_gates=len(gates),source_claims={d['source_id']:len(d['claims']) for d in ledgers},volume_pages=len(whole.pages),exact_proof_imports=len(imports),embedded_page_streams_and_glyph_programs_match=True,controls=controls,runs=runs,seconds=time.monotonic()-started,new_acquisitions=0,public_mutations=0,new_Lean=0,measurements=None,general_proofs='REQUIRE_DISTINCT_MATHEMATICAL_REVIEW')
    report['outputs']=[binding(f,out) for f in sorted(out.rglob('*')) if f.is_file()]
    (out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['status','dependencies','source_claims','volume_pages','controls','seconds']}))

if __name__=='__main__':main()
