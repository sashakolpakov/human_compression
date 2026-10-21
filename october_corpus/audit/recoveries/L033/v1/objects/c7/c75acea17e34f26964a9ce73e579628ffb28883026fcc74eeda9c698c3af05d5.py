"""Complete through3840 application of the acquired normal quotient method."""
import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
sys.dont_write_bytecode=True
import argparse, importlib.util, json
from pathlib import Path
P=Path(__file__).resolve().parent
S=P.parents[2]
METHOD=S/'corpus106_L033_coxeter_lins_methods_v1'
CORE=S/'corpus106_L033_hyperbolic_core_v1'
OLD=S/'reboot_20261013/L033_work/hyperbolic_recovery_work/3535_composed_accepted01'
M=[[1,3,2,5],[3,1,5,2],[2,5,1,3],[5,2,3,1]]

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

shared=module('divisor_validation',P.parent/'divisor_v1/check.py')
need,read,save,pin,exact,call,load,gap_driver=(getattr(shared,x)for x in ['need','read','save','pin','exact','call','load','gap_driver'])
GAP=['/opt/homebrew/bin/gap','-q','-b']

def frozen():
    if not(P/'manifest.json').exists():return None
    m=read(P/'manifest.json')
    for row in m['exports']:
        actual=pin(P/row['path'])
        need(all(actual[k]==row[k] for k in ['bytes','sha256']),'frozen export '+row['path'])
    return m

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--render',action='store_true')
    args=parser.parse_args();out=args.out.resolve()
    need(not out.exists(),'fresh output')
    before=frozen();deps=read(P/'dependencies.json')
    for row in deps:exact(row)
    old=(METHOD/'enumerate_changed.g').read_text()
    need(old.count('if result.ok then')==1,'one record filter')
    changed=old.replace('if result.ok then','if true then # Retain every tested quotient, including failures.').replace('ACCEPTED','RECORDED')
    need(changed==(P/'enumerate_all.g').read_text(),'exact record-only change; unchanged search')
    out.mkdir()
    paths=[METHOD/'coxeter_seeds.g',METHOD/'composed_pmodules.g',P/'enumerate_all.g']
    runtime=[Path('/opt/homebrew/bin/gap'),Path('/opt/homebrew/Cellar/gap/4.15.1/bin/gap')]
    script=gap_driver(out,'census','LoadPackage("LINS");;\n'+''.join(load(p)for p in paths)+'RunHyperbolic('+json.dumps(M)+',[120,120,120,120],3840,'+json.dumps(str(out/'census/records.g'))+');;')
    text=call(out,'census',GAP+[str(script)],paths+runtime+[script],60)
    # The shared runner's generic scope is validation; this exact search scope
    # is explicit here and in the component report, never inferred from it.
    save(out/'census/scope.json',dict(target_census=True,all_indices_through=3840,normal_kernels=25,retained_marked_quotients=23,changed_search=False))
    need('COMPLETE_HYPERBOLIC_BOUND 3840 NORMALS 25 RECORDED 23' in text,'complete bounded census')
    marker='INDEX_MULTIPLICITIES '
    lines=[s[len(marker):]for s in text.splitlines()if s.startswith(marker)]
    need(len(lines)==1 and json.loads(lines[0])==[[1,1],[2,1],[60,1],[120,1],[660,1],[960,1],[1320,1],[1920,7],[3840,11]],'normal index multiplicities')
    compare=load(METHOD/'compare_markings.g')+load(out/'census/records.g')+'fresh:=hyperbolic_records;;\n'+load(OLD/'records.g')+'''
positive:=Filtered(fresh,r->r.checks.ok);;
if OrderedMarkingBijection(positive,hyperbolic_records)=fail then Error("same acquired positive kernel");fi;
if Length(fresh)<>23 or Length(positive)<>1 then Error("complete marked roster");fi;
'''
    if (P/'records.g').exists():
        compare+=load(P/'records.g')+'if OrderedMarkingBijection(fresh,hyperbolic_records)=fail then Error("same entire marked inventory");fi;\n'
    compare+='Print("LITERAL_QUOTIENTS ",List(fresh,r->[r.node,r.order,r.permutations,r.checks.ok]),"\\n");;\nPrint("COMPLETE_BOUND_MARKED_COMPARISON\\n");;'
    bridge_script=gap_driver(out,'bridge',compare)
    inputs=[METHOD/'compare_markings.g',out/'census/records.g',OLD/'records.g',bridge_script]+runtime
    if (P/'records.g').exists():inputs.append(P/'records.g')
    bridge=call(out,'bridge',GAP+[str(bridge_script)],inputs,60)
    values=[s.removeprefix('LITERAL_QUOTIENTS ')for s in bridge.splitlines()if s.startswith('LITERAL_QUOTIENTS ')]
    need(len(values)==1 and 'COMPLETE_BOUND_MARKED_COMPARISON' in bridge,'complete literal bridge')
    values=json.loads(values[0]);need(len(values)==23,'23 literal tuples')
    literal=module('independent_literal',CORE/'literal.py')
    rows=[];reports=[]
    for n,order,perms,ok in values:
        row=dict(type='3535',node=n,order=order,permutations=perms,matrix=M,expected_reject=not ok)
        result=literal.validate(row,M)
        need(bool(result['intersection_failures']or result['flag_failures'])==row['expected_reject'],'literal verdict agrees')
        rows.append(row);reports.append(result)
    positive=[r for r in reports if not(r['intersection_failures']or r['flag_failures'])]
    need(len(positive)==1 and positive[0]['order']==1920 and positive[0]['local_orders']==[60]*4,'unique positive and actual local orders')
    lower=[r for r in reports if r['order']==960]
    need(len(lower)==1 and not lower[0]['intersection_failures'] and lower[0]['flag_failures'],'960 requires incidence test')
    excluded=[r for r in reports if r['order']==3840]
    need(len(excluded)==11 and all(r['intersection_failures']for r in excluded),'all eleven3840 kernels fail intersection')
    need(sum(bool(r['intersection_failures'])for r in reports)==21,'all21 intersection rejections')
    save(out/'quotients.json',rows);save(out/'literal.json',reports)
    pages=None
    if args.render:
        native=out/'native';native.mkdir()
        for i in [1,2]:
            call(out,'tex'+str(i),['/opt/homebrew/bin/pdflatex','-halt-on-error','-interaction=nonstopmode','-output-directory',str(native),str(P/'square.tex')],[P/'square.tex'],30)
        need(not any(x in(native/'square.log').read_text()for x in ['Warning','Overfull','Underfull']),'clean native layout')
        from pypdf import PdfReader
        pdf=PdfReader(native/'square.pdf');pages=len(pdf.pages)
        if(P/'square.pdf').exists():need([p.extract_text()for p in pdf.pages]==[p.extract_text()for p in PdfReader(P/'square.pdf').pages],'unchanged proof text')
        call(out,'raster',['/opt/homebrew/bin/gs','-q','-dSAFER','-dBATCH','-dNOPAUSE','-sDEVICE=png16m','-r110','-sOutputFile='+str(native/'page-%02d.png'),str(native/'square.pdf')],[native/'square.pdf'],30)
    for row in deps:exact(row)
    need(frozen()==before,'stable frozen component')
    report=dict(status='PASS_COMPLETE_SQUARE3535_THROUGH3840',all_indices_through=3840,normal_kernels=25,marked_quotients=23,positive=1,
                intersection_rejections=21,incidence_rejections=1,broad_minimum=1920,universal_minimum='greater than3840; existence beyond bound not asserted',
                excluded_exact_order3840=11,native_pages=pages,search_delta='Retain negatives only; search unchanged',classification_premises_retained=True,
                whole_original_credit=0,new_question_credit=0,new_Lean=0,measurement=None)
    save(out/'report.json',report);print(json.dumps(report))

if __name__=='__main__':main()
