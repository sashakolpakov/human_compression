#!/usr/bin/env python3
"""Check frozen Topic C bindings and optionally render or recompile scoped proofs.

This is a reproducibility check, not independent mathematical review. The full
Janko census has its own explicit --census option and is never inferred from
checking a saved execution record.
"""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess
ROOT=Path(__file__).resolve().parent
NAMES=['umbrella','janko-geometries','halving-generalized-cubes','petrials-and-faithful-actions','equal-adjacent-parameters','required-programs']

def need(ok,message):
    if not ok:raise RuntimeError(message)

def digest(data):return hashlib.sha256(data).hexdigest()

def binding(root,row):
    p=root/row['path'];need(p.is_file(),'Missing '+str(p));b=p.read_bytes()
    need(len(b)==row['bytes'] and digest(b)==row['sha256'],'Changed '+str(p))

def check_scope(root,scope):
    expected={*[f'J{i}' for i in range(1,12)],*[f'N{i}' for i in range(1,17)],*[f'P{i}' for i in range(1,9)],*[f'F{i}' for i in range(1,6)]}
    rows=scope['source_result_rows'];need(len(rows)==40 and {r['id'] for r in rows}==expected,'Incorrect clause boundary')
    byid={r['id']:r for r in rows}
    for key in ['N14','N15']:need(byid[key]['coverage']=='excluded_auxiliary','Lost explicit exclusion')
    for key in ['J10','N13','P4','P7','P8']:need(byid[key]['coverage']=='corrected_or_qualified_assertion','Lost correction/qualification')
    need(byid['J9']['required_programs']==['program.construction','program.census'],'Census dependency omitted')
    need(all(not r['required_programs'] for r in rows if r['source']!='L088'),'Invented uniform-proof program premise')
    sources={s['id']:s for s in scope['sources']}
    need(set(sources)=={'L088','N013','L108','F014'},'Source boundary changed')
    need(sources['L108']['source_pdf_available'] is False and sources['L108']['full_source_pdf_cost'] is None,'Unavailable source cost replaced')
    need(scope['cost_boundary']['ratio'] is None and scope['new_source_credit']==scope['new_question_credit']==0,'Unreviewed credit or measurement')
    count=0
    for record in list(scope['proof_regions'].values())+[n['binding'] for n in scope['proof_statements_and_context'].values()]:
        text=(root/record['file']).read_text();a,b=record['start_char'],record['end_char'];need(0<=a<b<=len(text),'Invalid proof span')
        raw=text[a:b].encode();need(len(raw)==record['bytes'] and digest(raw)==record['sha256'],'Changed proof span')
        need(text[:a].count('\n')+1==record['start_line'] and text[:b].count('\n')+1==record['end_line'],'Changed proof line locator');count+=1
    nodes=set(scope['proof_statements_and_context'])
    for row in rows:
        need(set(row.get('current_proof_ids',row.get('current_common_proof_ids',[])))<=nodes,'Missing proof reference')
    for row in scope['complete_proof_files']:binding(root,row)
    programs=scope['required_programs'];need(len(programs)==3,'Program inventory changed')
    need({p['id'] for p in programs if p['required_mathematics']}=={'program.construction','program.census'},'Required code not fully charged')
    for row in programs:binding(root,row['file'])
    formal=json.loads((root/'formal/scope.json').read_text());need(formal==scope['formal_scope'],'Formal scope changed')
    for row in formal['modules']:
        raw=(root/'formal'/row['file']).read_bytes();need(len(raw)==row['bytes'] and digest(raw)==row['sha256'],'Changed Lean source')
    need(sum(len(r['declarations']) for r in formal['modules'])==16,'Wrong scoped declaration inventory')
    return count

def pdf_text(path):
    from pypdf import PdfReader
    return [p.extract_text() or '' for p in PdfReader(path).pages]

def code_inclusion(root):
    pages=pdf_text(root/'required-programs.pdf');parts=[]
    for number,page in enumerate(pages,1):
        lines=page.splitlines()
        if lines and lines[-1].strip()==str(number):lines.pop()
        parts.append(''.join(lines))
    text=re.sub(r'\s+','',''.join(parts)).replace('↪','');result=[]
    for name in ['phase40_compress_operations_check.g','phase40_compress_operations_exhaustive.g']:
        raw=(root/'programs'/name).read_text();need('↪' not in raw,'Wrap marker occurs in program');target=re.sub(r'\s+','',raw)
        need(target in text,'Complete program not found in appendix PDF: '+name)
        result.append({'program':name,'nonspace_characters':len(target),'complete_contiguous_inclusion_after_page_footer_and_display_wrap_marker_removal':True})
    return result

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);p.add_argument('--study-root',type=Path);p.add_argument('--public-root',type=Path);p.add_argument('--render',action='store_true');p.add_argument('--xelatex',default='xelatex');p.add_argument('--formal',action='store_true');p.add_argument('--census',action='store_true');a=p.parse_args()
    need(not a.out.exists() and not a.out.is_symlink(),'Use a fresh output path');out=a.out.resolve();out.mkdir(parents=True)
    manifest=json.loads((ROOT/'manifest.json').read_text())
    for row in manifest['exports']:binding(ROOT,row)
    scope=json.loads((ROOT/'scope.json').read_text());count=check_scope(ROOT,scope)
    source_count=0;prior_count=0
    if a.study_root:
        for row in scope['sources']:binding(a.study_root,row['primary']);source_count+=1
        for row in scope['prior_admissions_and_contracts']:
            if row['path'].startswith('public:'):continue
            binding(a.study_root,row);prior_count+=1
    if a.public_root:
        for row in scope['prior_admissions_and_contracts']:
            if not row['path'].startswith('public:'):continue
            binding(a.public_root,{**row,'path':row['path'][7:]});prior_count+=1
    included=code_inclusion(ROOT);renders=[]
    if a.render:
        temp=out/'render';temp.mkdir()
        for row in manifest['exports']:
            rel=Path(row['path'])
            if rel.suffix not in ['.tex','.g']:continue
            dest=temp/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
        for name in NAMES:
            for i in range(2):
                run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error',name+'.tex'],cwd=temp,capture_output=True,text=True,timeout=180)
                (out/(name+f'.pass{i+1}.log')).write_text(run.stdout+run.stderr);need(run.returncode==0,'Render failed: '+name)
            log=(temp/(name+'.log')).read_text();need(not any(x in log for x in ['Overfull','Missing character','undefined','LaTeX Warning']),'TeX diagnostic: '+name)
            before=pdf_text(ROOT/(name+'.pdf'));after=pdf_text(temp/(name+'.pdf'));need(before==after,'Rendered page text differs: '+name)
            need(not any(ord(c)<32 and c not in '\n\r\t' for page in after for c in page),'Control glyph')
            renders.append({'document':name,'pages':len(after),'per_page_text_identical':True})
        code_inclusion(temp)
    if a.formal:
        subprocess.run([__import__('sys').executable,'-B','-O',ROOT/'formal/check.py','--out',out/'formal'],check=True)
    if a.census:
        subprocess.run([__import__('sys').executable,'-B','-O',ROOT/'programs/phase150_module_C_run.py','--output-dir',out/'census'],check=True)
    result={'status':'PASS','bound_exports':len(manifest['exports']),'clause_rows':40,'proof_spans':count,'primary_bindings_checked':source_count,'prior_contract_bindings_checked':prior_count,'full_code_appendix':included,'fresh_renders':renders,'fresh_scoped_formal':a.formal,'fresh_Janko_census':a.census,'independent_math_review':False,'source_credit_increment':0,'question_credit_increment':0,'ratio':None}
    (out/'report.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
