#!/usr/bin/env python3
"""Fresh complete M22 enumeration and source reconciliation, in a new directory."""
import argparse,hashlib,importlib.util,json,os,re,shutil,signal,subprocess,sys,time,unicodedata
from pathlib import Path
R=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise ValueError(msg)
def binding(p):return {'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return json.loads(p.read_text())
def write(p,x):p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def run(cmd,cwd,stem,marker,seconds=90):
    t=time.monotonic();p=subprocess.Popen(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
    try:so,se=p.communicate(timeout=seconds)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid,signal.SIGTERM)
        try:so,se=p.communicate(timeout=5)
        except subprocess.TimeoutExpired:os.killpg(p.pid,signal.SIGKILL);so,se=p.communicate()
        (cwd/(stem+'.stdout')).write_text(so);(cwd/(stem+'.stderr')).write_text(se);raise ValueError('bounded child timeout '+stem)
    (cwd/(stem+'.stdout')).write_text(so);(cwd/(stem+'.stderr')).write_text(se)
    need(p.returncode==0 and marker in so and not any(x in so+se for x in ['Error,','Syntax error','Fatal error','Emergency stop']),'stage '+stem)
    return {'stage':stem,'seconds':time.monotonic()-t,'stdout':binding(cwd/(stem+'.stdout')),'stderr':binding(cwd/(stem+'.stderr')),'syntax_warnings':[l for l in (so+se).splitlines() if 'Syntax warning' in l]}

def module(name,path):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
def metadata():
    scope=load(R/'scope.json');need(scope['source_id']=='L073' and scope['rank_two_classes']==81 and scope['rank_three_classes']==431 and scope['physical_source_rows']==431,'complete source contract')
    need(scope['formal_declarations']==0 and not scope['historical_geo_numbering_recovered'] and not scope['printed_labels_all_simultaneously_true'] and not scope['L095_special_group_theorem_used'],'exact proof limits')
    inv=load(R/'program_inventory.json')
    for row in inv['mathematical_programs']:need(binding(R/row['path'])=={k:row[k]for k in ['bytes','sha256']},'whole mathematical program '+row['path'])
    m=load(R/'proof_map.json');text=(R/'primitive-mathieu-geometries.tex').read_text()
    need(binding(R/'primitive-mathieu-geometries.tex')==m['text_hash'],'complete written proof binding')
    for row in m['spans']:need(hashlib.sha256(text[row['start']:row['end']].encode()).hexdigest()==row['sha256'],'complete proof span '+row['id'])
    need(len(m['spans'])==7 and len(load(R/'source_ledger.json')['clauses'])==14,'complete named theorem/source map')
    if (R/'manifest.json').exists():
        rows=load(R/'manifest.json')['exports'];need(len({r['path']for r in rows})==len(rows),'unique manifest exports')
        for row in rows:
            q=Path(row['path']);need(not q.is_absolute() and '..'not in q.parts,'safe relative export')
            need(binding(R/q)=={k:row[k]for k in ['bytes','sha256']},'export '+str(q))
        return len(rows)
    return None

def source(study):
    if study is None:return {'checked':False,'scope':'Portable replay does not redistribute or require primary PDFs.'}
    from pypdf import PdfReader
    for r in load(R/'source_bindings.json')['primary']:
        p=study/r['path'];need(binding(p)=={k:r[k]for k in ['bytes','sha256']},'private primary '+r['path']);need(len(PdfReader(p).pages)==r['pages'],'full source extent')
    inherited=load(R/'inherited_bindings.json')
    for r in inherited:need(binding(study/r['path'])=={k:r[k]for k in ['bytes','sha256']},'historical provenance '+r['path'])
    pdf=PdfReader(study/'sources/catalogue_L073.pdf');rows=[]
    for i,p in enumerate(pdf.pages,1):
        for line in p.extract_text(extraction_mode='layout').splitlines():
            matches=list(re.finditer(r'(M\d{3}\([^)]*\))\s+(\d+)\s+(.+?)(?=\s+M\d{3}\(|$)',line))
            for m in matches:rows.append({'row':len(rows)+1,'page':i,'label_text':m[1],'source_number':int(m[2]),'Borel_text':m[3].strip()})
    compact=lambda t:''.join(t.split())
    bound=load(R/'data/phase164_L073_table_contract.json')['rows'];need(len(rows)==len(bound)==431,'all physical source rows')
    for a,b in zip(rows,bound):need(all(compact(str(a[k]))==compact(str(b[k]))for k in a),'literal complete source row '+str(b['row']))
    return {'checked':True,'source_pages':9,'rows':431,'old_source_pages':48,'old_source_reading_targeted_only':True,'historical_bindings_checked':len(inherited)}

def runtime(gap,out):
    cmd='SizeScreen([100000,24]);;Print("GAP|",GAPInfo.Version,"\\n");;for n in ["tomlib","smallgrp","design","grape"] do LoadPackage(n);;Print(n,"|",PackageInfo(n)[1].Version,"|",Filename(DirectoriesPackageLibrary(n,"")[1],""),"\\n");od;QUIT;'
    rec=run([gap,'-q','-b','-A','-r','-c',cmd],out,'runtime','grape|');spec=load(R/'computational_inputs.json');lines=(out/'runtime.stdout').read_text().splitlines();versions={};roots={}
    for l in lines:
        a=l.strip().split('|')
        if len(a)>=2:versions[a[0]]=a[1]
        if len(a)==3:roots[a[0]]=Path(a[2])
    need(versions.get('GAP')==spec['GAP'],'GAP version')
    for k,v in spec['packages'].items():need(versions.get(k)==v,'package version '+k)
    for r in spec['file_pins']:need(binding(roots[r['package']]/r['path'])=={k:r[k]for k in ['bytes','sha256']},'retained external data/code '+r['path'])
    return {'versions':versions,'pins':spec['file_pins'],'execution':rec,'exact_algorithms_trusted':True}

def render(out,xe):
    from pypdf import PdfReader
    q=out/'render';q.mkdir();shutil.copytree(R/'programs',q/'programs');result=[]
    text=lambda p:[x.extract_text()or'' for x in PdfReader(p).pages]
    for n in ['primitive-mathieu-geometries','class-tables','source-rows','required-programs']:
        shutil.copy2(R/(n+'.tex'),q/(n+'.tex'))
        for i in range(2):run([xe,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',n+'.tex'],q,n+'-'+str(i),'Output written on',120)
        diag=[l for l in (q/(n+'.log')).read_text().splitlines() if any(x in l for x in ['Overfull','Missing character','Warning:'])];need(not diag,'render diagnostics '+n+str(diag))
        ts=text(q/(n+'.pdf'));need(ts==text(R/(n+'.pdf')),'exact fresh page text '+n)
        need(all(not any(ord(c)<32 and c not in '\n\r\t' for c in t) and '\ufffd'not in t for t in ts),'decoded glyphs '+n)
        result.append({'name':n,'pages':len(ts),'page_text_hashes':[hashlib.sha256(t.encode()).hexdigest()for t in ts],'diagnostics':diag})
    compact=lambda t:''.join(c for c in unicodedata.normalize('NFKC',t)if not c.isspace())
    pages=[re.sub(r'\n'+str(i)+r'\s*$','',s)for i,s in enumerate(text(q/'required-programs.pdf'),1)];whole=compact('\n'.join(pages))
    inclusion=[]
    for r in load(R/'program_inventory.json')['mathematical_programs']:
        literal=compact((R/r['path']).read_text());pos=whole.find(literal)
        need(pos>=0,'full printed code '+r['path'])
        inclusion.append({'path':r['path'],'source':binding(R/r['path']),'normalized_character_count':len(literal),'normalized_start':pos,'normalized_end':pos+len(literal)})
    write(out/'printed_code_inclusion.json',{'scope':'Full-file inclusion after NFKC and whitespace removal; this is not a measurement rule. Only exact trailing page numbers are removed from PDF text. No other printable glyph is deleted.','pdf':binding(R/'required-programs.pdf'),'files':inclusion})
    return result

def main():
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--gap',default='gap');a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='xelatex');a.add_argument('--study-root',type=Path);x=a.parse_args();out=x.out.absolute();need(not out.exists() and not out.is_symlink(),'fresh output');out.mkdir(parents=True)
    exports=metadata();private=source(x.study_root);environment=runtime(x.gap,out)
    pins={str(p.relative_to(R)):binding(p) for d in ['programs','data'] for p in (R/d).iterdir() if p.is_file()}
    stages=[]
    def gap(stem,name,assign,marker):
        code=''.join(k+':='+json.dumps(str(v))+';;' for k,v in assign.items())+'Read('+json.dumps(str(R/'programs'/name))+');'
        stages.append(run([x.gap,'-q','-b','-T','-m','64m','-o','1g','-c',code],out,stem,marker))
    gap('census','phase164_m22_census.g',{},'M22_EXHAUSTIVE_FINISHED')
    witness=out/'phase164_m22_witnesses.g'
    need(binding(witness)['sha256']=='ec5ac0724e8dff8a1f1842347ba28efd03ff0a9bb81cdc1b139540ae06ff45cb','same exhaustive witnesses as independently accepted core')
    gap('validate','phase164_m22_validate.g',{},'M22_WITNESSES_VALIDATED')
    gap('coordinates','orbit_coordinates.g',{'WITNESS_FILE':witness},'L073_COMPLETE_COORDINATES 81 431')
    stages.append(run([sys.executable,'-B','-O',str(R/'programs/phase180_code_completions.py'),'--source',str(R/'data/phase180_source_notation.json'),'--target-shadows',str(out/'canonical_triples.json'),'--output-dir',str(out/'codes')],out,'completions','"completions": 4'))
    gap('literal_configurations','phase180_mog_check.g',{'INPUT_FILE':out/'codes/code_inputs.g','WITNESS_FILE':witness,'OUTPUT_FILE':out/'codes/mog_check.json'},'PHASE180_ALL_SOURCE_COMPLETIONS_CHECKED 4')
    argv=[sys.executable,'-B','-O',str(R/'programs/reconcile.py'),'--data',str(R/'data'),'--work',str(out)]
    stages.append(run(argv,out,'prepare','L073_RECONCILIATION_PREPARED'))
    gap('borels','phase180_borel_check.g',{'INPUT_FILE':out/'Borel_inputs.g','WITNESS_FILE':witness,'OUTPUT_FILE':out/'Borel_check.json'},'PHASE180_BOREL_SHAPES_COMPLETE')
    stages.append(run(argv+['--finish'],out,'reconcile','explicit_pair_objects'))
    for name,pin in pins.items():need(binding(R/name)==pin,'unchanged input '+name)
    data=load(out/'reconciliation.json');checks=module('l073_controls',R/'controls.py').check(out);module('l073_tables',R/'build_tables.py').build(out/'reconciliation.json',out/'tables')
    expected=R/'evidence'
    for name in ['canonical_pairs.json','source_pairs.json','canonical_triples.json','source_triples.json','Borel_check.json','reconciliation.json']:
        if (expected/name).exists():need(load(out/name)==load(expected/name),'fresh complete evidence equality '+name)
    for name in ['class-tables.tex','source-rows.tex','required-programs.tex']:need((out/'tables'/name).read_bytes()==(R/name).read_bytes(),'exact full table/code source '+name)
    graphics=render(out,x.xelatex) if x.render else []
    report={'status':'PASS_AUTHOR_COMPLETE_CORRECTED_L073_CANDIDATE','exports_checked':exports,'private_source':private,'runtime':environment,'controls':checks,'render':graphics,'inputs':pins,'stages':stages,'summaries':data['summaries'],'census_input_uses_source_rows':False,'Lean_declarations':0,'historical_numbering_recovered':False}
    write(out/'report.json',report);print(json.dumps({'status':report['status'],'out':str(out),'summaries':data['summaries']},sort_keys=True))
if __name__=='__main__':main()
