#!/usr/bin/env python3
"""Portable exact L084 replay. No historical g.txt or primary text is executable input."""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time
from pathlib import Path
import accounting
ROOT=Path(__file__).resolve().parent

def need(value,message):
    if not value:raise ValueError(message)
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')
def binding(path):return {'bytes':path.stat().st_size,'sha256':sha(path)}
def checked_file(base,row):
    rel=Path(row['path']);need(not rel.is_absolute() and '..'not in rel.parts,'relative file binding')
    p=base/rel;need(p.is_file(),'missing '+str(p));need(binding(p)=={k:row[k]for k in ['bytes','sha256']},'changed '+str(p));return p

def metadata_checks():
    scope=json.loads((ROOT/'scope.json').read_text())
    expected={'ambient_order':600415200,'all_subgroup_classes':1262,'all_element_classes':180,'forbidden_classes':47,'survivors':137,'containment_edges':349,'literal_maximal_words':30,'surviving_literal_anchors':26,'deletion_witnesses':8,'section_regular':66,'same_local_types':65,'mixed_facets':71}
    need(scope['census']==expected and scope['formal_declarations']==0 and scope['historical_g_txt_used'] is False,'exact census and formal boundary')
    need(scope['primary_text_exported'] is False and scope['unseen_journal_table_identity_claimed'] is False,'source edition boundary')
    ledger=json.loads((ROOT/'source_ledger.json').read_text())
    need(len(ledger['rows'])==18 and len({r['id']for r in ledger['rows']})==18,'complete distinct clause ledger')
    need({x['id']for x in ledger['retained']}=={'R.Universal','R.Quotient','R.Local','R.Computation'},'all retained premises explicit')
    proof=json.loads((ROOT/'proof_map.json').read_text())
    for row in proof['spans']:
        lines=(ROOT/row['path']).read_text().splitlines()
        text='\n'.join(lines[row['start_line']-1:row['end_line']])+'\n'
        need(hashlib.sha256(text.encode()).hexdigest()==row['sha256'],'exact written proof span '+row['id'])
    return {'source_rows':len(ledger['rows']),'written_contexts':len(proof['spans']),'retained_inputs':4}

def execute(command,cwd,stem,timeout=900,input=None):
    start=time.monotonic();p=subprocess.run(command,cwd=cwd,input=input,text=True,capture_output=True,timeout=timeout)
    (cwd/(stem+'.stdout')).write_text(p.stdout);(cwd/(stem+'.stderr')).write_text(p.stderr)
    need(p.returncode==0,'nonzero command '+stem)
    need(not any(s in p.stdout+p.stderr for s in ['Error,','Syntax error','Syntax warning','Missing character:','Emergency stop','Fatal error']),'diagnostic '+stem)
    return p.stdout,time.monotonic()-start

def computational_inputs(gap,out):
    script='LoadPackage("tomlib");; Print("GAP_VERSION|",GAPInfo.Version,"\\nTOMLIB_VERSION|",PackageInfo("tomlib")[1].Version,"\\n");; for p in GAPInfo.RootPaths do Print("GAP_ROOT|",p,"\\n"); od; Print("TOMLIB_ROOT|",Filename(DirectoriesPackageLibrary("tomlib","")[1],""),"\\n");; QUIT;\n'
    text,elapsed=execute([gap,'-q','-b','-A','-r'],out,'runtime',input=script)
    vals={};roots=[]
    for line in text.splitlines():
        if '|'in line:
            k,v=line.split('|',1)
            if k=='GAP_ROOT':roots.append(Path(v))
            else:vals[k]=v
    spec=json.loads((ROOT/'computational_inputs.json').read_text())
    need(vals.get('GAP_VERSION')==spec['GAP'] and vals.get('TOMLIB_VERSION')==spec['TomLib'],'pinned GAP/TomLib versions')
    import networkx
    need(networkx.__version__==spec['NetworkX'],'pinned NetworkX version')
    files=[]
    for row in spec['file_pins']:
        candidates=roots if row['root']=='gap_root'else [Path(vals['TOMLIB_ROOT'])]
        ps=[p/row['path'] for p in candidates if (p/row['path']).is_file()]
        need(any(binding(p)=={k:row[k]for k in ['bytes','sha256']} for p in ps),'runtime/data binding '+row['path'])
        files.append(row)
    return {'versions':{'GAP':vals['GAP_VERSION'],'TomLib':vals['TOMLIB_VERSION'],'NetworkX':networkx.__version__},'files':files,'trust':spec['trust']}

def render(out,xelatex):
    from pypdf import PdfReader
    target=out/'render';target.mkdir()
    shutil.copytree(ROOT/'programs',target/'programs')
    shutil.copy2(ROOT/'accounting.py',target/'accounting.py')
    result=[]
    for name in ['semisparse-quotient-census','required-programs','corrected-census']:
        shutil.copy2(ROOT/(name+'.tex'),target/(name+'.tex'))
        for run in [1,2]:execute([xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error',name+'.tex'],target,name+'-'+str(run),timeout=120)
        log=(target/(name+'.log')).read_text(errors='replace')
        diagnostics=[x for x in log.splitlines()if any(y in x for y in ['Overfull','Missing character','undefined references','LaTeX Warning:','Package unicode-math Warning:'])]
        need(not diagnostics,'render diagnostics '+name+': '+repr(diagnostics))
        pages=[p.extract_text()or''for p in PdfReader(target/(name+'.pdf')).pages]
        need(all(not any(ord(c)<32 and c not in '\n\t\r'for c in t) and '\ufffd'not in t for t in pages),'render glyph scan')
        existing=ROOT/(name+'.pdf')
        if existing.exists():need(pages==[p.extract_text()or''for p in PdfReader(existing).pages],'render page text changed '+name)
        result.append({'document':name,'pages':len(pages),'page_text_sha256':[hashlib.sha256(t.encode()).hexdigest()for t in pages],'diagnostics':diagnostics})
    return result

def printed_table_check(census,reconciliation):
    text=(ROOT/'corrected-census.tex').read_text()
    blocks=text.split(r'\midrule\endhead'+'\n')[1:]
    need(len(blocks)==2,'two complete computed table blocks')
    actual=[[line for line in b.split(r'\bottomrule')[0].splitlines()if line]for b in blocks]
    mapping={int(k):v for k,v in reconciliation['historical_to_computed'].items()};reverse={v:k for k,v in mapping.items()}
    counts={x[0]:x for x in census['survivors']};types={i:(g,q)for i,g,q in census['survivor_types']}
    expected=[[],[]]
    for lab,i in sorted(mapping.items()):
        _,o,d,h=counts[i];children=sorted(reverse[b]for a,b in census['maximal_edges']if a==i)
        expected[0].append(f'{lab}&{o}&{d}&{h}&'+(', '.join(map(str,children))or'--')+r'\\')
        g,q=types[i];expected[1].append(str(lab)+'&'+g+'&'+q+r'\\')
    need(actual==expected,'every printed census and structure/normalizer row')
    return {'facet_containment_rows':137,'structure_normalizer_rows':137,'edges':349}

def complete_code_check(pdf):
    from pypdf import PdfReader
    import unicodedata
    texts=[]
    for i,page in enumerate(PdfReader(pdf).pages,1):
        t=page.extract_text()or''
        t=re.sub(r'\n'+str(i)+r'\s*$', '', t)
        texts.append(t)
    compact=lambda t:''.join(c for c in unicodedata.normalize('NFKC',t)if not c.isspace())
    extracted=compact('\n'.join(texts));rows=[]
    for rel in ['programs/ambient_marking.g','programs/source_maximals.g','programs/quotient_census.g','accounting.py']:
        p=ROOT/rel;needle=compact(p.read_text())
        need(needle in extracted,'complete normalized code inclusion '+rel)
        rows.append({'path':rel,**binding(p),'comparison':'Complete file occurs in the PDF after NFKC/whitespace normalization and exact page-footer removal; raw source bytes are independently bound.'})
    return rows

def replay_witnesses(gap,out):
    text='Read("programs/ambient_marking.g");;\nproduct:=Set(Concatenation(List(Elements(H0),a->List(Elements(H3),b->a*b))));;\n'
    test='q in W and x in h and x^q=b and b in product and not b in [One(W),om]'
    text+='WitnessValid:=function(h,x,q,b) return '+test+';end;;\n'
    for i in sorted(accounting.DELETED):
        text+=f'Read("witness_{i}.g");; CheckL084(WitnessValid(Group(rejectedGenerators),violatingElement,conjugator,endProductElement),"literal witness {i}");; CheckL084(not WitnessValid(Group(rejectedGenerators),One(W),conjugator,endProductElement),"reject zeroed witness {i}");; CheckL084(not WitnessValid(Group(rejectedGenerators),violatingElement,conjugator,One(W)),"reject permitted target {i}");;\n'
    text+='Print("L084_WITNESSES_PASS 8 real 16 rejected mutations\\n");; QUIT;\n'
    (out/'check_witnesses.g').write_text(text)
    log,elapsed=execute([gap,'-q','-b','-A','-r','check_witnesses.g'],out,'witness_replay')
    need('L084_WITNESSES_PASS 8 real 16 rejected mutations'in log,'witness sentinel')
    return {'actual_witnesses':8,'mutations_rejected':16,'seconds':elapsed}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True,type=Path);ap.add_argument('--study-root',type=Path);ap.add_argument('--gap',default=shutil.which('gap'));ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default=shutil.which('xelatex'));args=ap.parse_args()
    need(args.gap is not None,'GAP executable required');need(not args.out.exists(),'fresh output directory required');args.out.mkdir(parents=True)
    start=time.monotonic();checked=[]
    mf=ROOT/'manifest.json'
    if mf.exists():
        manifest=json.loads(mf.read_text())
        for row in manifest['exports']:checked_file(ROOT,row);checked.append(row['path'])
    sources=[]
    if args.study_root:
        for key,row in json.loads((ROOT/'source_bindings.json').read_text()).items():checked_file(args.study_root,row);sources.append(key)
    metadata=metadata_checks()
    runtime=computational_inputs(args.gap,args.out)
    shutil.copytree(ROOT/'programs',args.out/'programs')
    text,elapsed=execute([args.gap,'-q','-b','-A','-r','programs/quotient_census.g'],args.out,'census')
    need('L084_CENSUS_PASS classes=1262 survivors=137 maximal=26 section_regular=66 same_local=65 mixed=71'in text,'complete census sentinel')
    census=json.loads((args.out/'census.json').read_text());rows=json.loads((ROOT/'source_tables.json').read_text())
    reconciliation=accounting.reconcile(census,rows);controls=accounting.controls(census,rows)
    write(args.out/'reconciliation.json',reconciliation)
    table_check=printed_table_check(census,reconciliation)
    need((args.out/'computed_subgroups.g').stat().st_size>1000000,'complete subgroup representative evidence')
    witnesses=replay_witnesses(args.gap,args.out)
    pdfs=render(args.out,args.xelatex)if args.render else []
    code_inclusion=complete_code_check(args.out/'render/required-programs.pdf')if args.render else complete_code_check(ROOT/'required-programs.pdf')
    report={'status':'PASS','manifest_exports_checked':len(checked),'sources_verified':sources,'metadata':metadata,'runtime':runtime,'census_seconds':elapsed,'reconciliation':reconciliation,'semantic_controls_rejected':controls,'witness_replay':witnesses,'printed_tables':table_check,'complete_code_inclusion':code_inclusion,'renders':pdfs,'evidence':{p.name:binding(p)for p in sorted(args.out.iterdir())if p.is_file()and p.suffix in ['.json','.g']},'wall_seconds':time.monotonic()-start,'formal_scope':'No Lean declaration; exact GAP/Python runtime and retained mathematical premises remain explicit.'}
    write(args.out/'report.json',report);print(json.dumps({'status':'PASS','classes':1262,'survivors':137,'edges':349,'controls':len(controls)+16,'seconds':report['wall_seconds']}))
if __name__=='__main__':main()
