#!/usr/bin/env python3
"""Portable calculation, CSV, complete-paper figures and isolated reader build."""
from pathlib import Path
from copy import deepcopy
import argparse,csv,json,subprocess,re
import calculate as C
import presentation as P

def controls(result,inputs,review_root):
    tests=[]
    def reject(name,fn):
        try:fn()
        except (ValueError,KeyError,IndexError) as e:
            tests.append(dict(name=name,rejected=True,reason=str(e)));return
        raise ValueError('control was accepted: '+name)
    def result_mutation(name,fn):
        r=deepcopy(result);fn(r);reject(name,lambda:C.validate_result(r))
    result_mutation('omit one coordinate',lambda r:r['coordinates'].pop())
    result_mutation('duplicate coordinate',lambda r:r['coordinates'].__setitem__(0,deepcopy(r['coordinates'][1])))
    result_mutation('omit second common paper from total',lambda r:r['coordinates'][0]['totals'].update(written=r['coordinates'][0]['totals']['written']-r['coordinates'][0]['costs']['U2']))
    result_mutation('double-charge code representations',lambda r:r['coordinates'][0]['totals'].update(with_printed_programs=r['coordinates'][0]['totals']['with_printed_programs']+r['coordinates'][0]['raw_costs']['programs']))
    result_mutation('discount a whole common paper',lambda r:r['coordinates'][0]['costs'].update(U1=0))
    result_mutation('wrong fraction numerator',lambda r:r['coordinates'][0]['comparisons']['written'].update(numerator=1))
    result_mutation('wrong reduced fraction',lambda r:r['coordinates'][0]['comparisons']['written'].update(reduced_denominator=1))
    result_mutation('wrong decimal',lambda r:r['coordinates'][0]['comparisons']['written'].update(decimal='1.000000000000'))
    result_mutation('conditional omits whole second common paper',lambda r:r['coordinates'][0]['conditional_acquisition'].update(whole_common_papers=['U1']))
    result_mutation('conditional omits complete code',lambda r:r['coordinates'][0]['conditional_acquisition'].update(printed_program_package=0))
    result_mutation('unknown retained proof becomes zero',lambda r:r['boundary']['unknown_costs'].update(retained_external_proofs=0))
    result_mutation('promote validation to finite premise',lambda r:r['boundary'].update(uniform_finite_program_premises=1))
    result_mutation('omit raw operational driver',lambda r:r['boundary'].update(separate_drivers=2))
    result_mutation('inflate Lean scope',lambda r:r['boundary'].update(partial_Lean_declarations=11))
    result_mutation('wrong count summary',lambda r:r.update(conditional_fractions=29))
    result_mutation('unreviewed source credit',lambda r:r.update(new_source_credit=1))
    p=C.read(inputs/'policy.json');a=C.read(inputs/'author_counts.json');i=C.read(review_root/'recount.json');v=C.read(review_root/'review.json')
    def input_mutation(name,fn):
        x=deepcopy(p);y=deepcopy(a);z=deepcopy(i);w=deepcopy(v);fn(x,y,z,w);reject(name,lambda:C.validate_inputs(x,y,z,w))
    input_mutation('wrong source page boundary',lambda p,a,i,v:a['documents']['L010'].update(pages=14))
    input_mutation('omit full third diagnostic',lambda p,a,i,v:p['programs'].pop())
    input_mutation('change raw file count against independent review',lambda p,a,i,v:next(iter(a['raw_files']['programs'].values()))['metrics']['NFC'].update(characters_without_whitespace=0))
    input_mutation('unaccepted input status',lambda p,a,i,v:v.update(status='PENDING'))
    return dict(status='PASS',rejected=len(tests),controls=tests)

def csvs(result,out):
    with (out/'costs.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['variant','normalization','unit','kind','component','cost'])
        for r in result['coordinates']:
            for kind,key in [('PDF','costs'),('raw_file_group','raw_costs')]:
                for k,v in r[key].items():w.writerow([r['variant'],r['normalization'],r['unit'],kind,k,v])
    with (out/'fractions.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['variant','normalization','unit','comparison','numerator','denominator','reduced_numerator','reduced_denominator','decimal'])
        for r in result['coordinates']:
            for k,v in r['comparisons'].items():w.writerow([r['variant'],r['normalization'],r['unit'],k]+list(v.values()))

def acquisition(r):
    p=r['primary'];c=p['costs'];raw=p['raw_costs'];routes=[]
    for kind,code in [('printed',c['CODE']),('raw',raw['programs'])]:
        steps=[];paid=0
        for k,amount in [('U1',c['U1']),('U2',c['U2']),('complete_validation_package',code),('A1',c['A1'])]:
            paid+=amount;steps.append(dict(acquired=k,increment=amount,total=paid))
        routes.append(dict(program_representation=kind,steps=steps,total=paid))
    return dict(scope='Whole-document acquisition with complete wrappers/references; no per-proof deduction or sharing discount.',routes=routes,conditional_application_cost=c['A1'],source_cost=c['L010'],external_proof_cost=None,graphics_cost=None)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--inputs',type=Path,required=True);ap.add_argument('--input-review',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--render',action='store_true');ap.add_argument('--xelatex',default='xelatex');a=ap.parse_args()
    C.need(not a.out.exists(),'fresh output directory');a.out.mkdir(parents=True)
    result=C.calculate(a.inputs,a.input_review);tests=controls(result,a.inputs,a.input_review)
    for name,value in [('results.json',result),('controls.json',tests),('acquisition.json',acquisition(result))]:
        (a.out/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
    csvs(result,a.out);P.figures(result,a.out);(a.out/'reader.tex').write_text(P.reader(result))
    report=dict(status='PASS_AUTHOR_NUMERICAL_REPLAY_PENDING_DISTINCT_REVIEW',input_manifests=C.PINS,coordinates=30,exact_fractions=120,combined_fractions=90,conditional_fractions=30,cost_csv_rows=240,fraction_csv_rows=120,controls_rejected=tests['rejected'],actual_cost_bars=9,graph_nodes=6,graph_edges=8,reader_pages=None,diagnostics=[],primary_material_exported=False,new_credits=0)
    if a.render:
        import pypdf
        for n in (1,2):
            run=subprocess.run([a.xelatex,'-interaction=nonstopmode','-halt-on-error','reader.tex'],cwd=a.out,capture_output=True,text=True)
            (a.out/f'render{n}.log').write_text(run.stdout+run.stderr);C.need(run.returncode==0,'XeLaTeX exit')
        log=(a.out/'reader.log').read_text();diagnostics=re.findall(r'(?:Overfull|Missing character|LaTeX Warning|Package .* Warning)[^\n]*',log)
        C.need(not diagnostics,'clean reader diagnostics')
        pages=[p.extract_text()or''for p in pypdf.PdfReader(a.out/'reader.pdf').pages];C.need(len(pages)==2,'complete two-page reader')
        report.update(reader_pages=2,reader_page_text_sha256=[__import__('hashlib').sha256(x.encode()).hexdigest()for x in pages])
    (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS30 coordinates/120 fractions/20 controls; numerical acceptance pending')
if __name__=='__main__':main()
