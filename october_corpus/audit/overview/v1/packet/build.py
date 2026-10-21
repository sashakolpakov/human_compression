#!/usr/bin/env python3
"""Consolidate pinned, accepted primary comparisons; never extract source text."""
from __future__ import annotations
import argparse, csv, hashlib, json
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise ValueError(message)

def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def ratio(n, d):
    need(type(n) is int and type(d) is int and n >= 0 and d > 0, 'invalid ratio')
    f = Fraction(n, d)
    with localcontext() as ctx:
        ctx.prec = 50
        dec = f'{Decimal(n)/Decimal(d):.12f}'
    return dict(numerator=n, denominator=d, exact_fraction=str(f), decimal=dec)

def check_old_ratio(old, n, d):
    need(old['numerator'] == n and old['denominator'] == d, 'changed admitted fraction')
    v = old.get('factor', old.get('decimal'))
    if v is not None:
        need(abs(Decimal(str(v)) - Decimal(n)/Decimal(d)) < Decimal('0.000000000002'), 'changed admitted decimal')

def load_inputs(spec, public, study, locations=None):
    result = {}
    for key, rec in spec['bindings'].items():
        path = Path(locations[key]) if locations and key in locations else (public if rec['anchor']=='public' else study)/rec['path']
        raw = path.read_bytes()
        need(len(raw)==rec['bytes'] and hashlib.sha256(raw).hexdigest()==rec['sha256'], 'input binding: '+key)
        result[key] = json.loads(raw)
    return result

def pair(source, application, s, a, original_id=None):
    return dict(source=source, application=application, original_application_id=original_id or application,
                source_cost=s, application_cost=a, conditional=ratio(s,a))

def topic(key, title, common, pairs, printed, raw, roles, representation='calibrated_selected_pdf', optional=None):
    sources=sum(r['source_cost'] for r in pairs); apps=sum(r['application_cost'] for r in pairs)
    return dict(topic=key,title=title,source_count=len(pairs),source_ids=[r['source'] for r in pairs],
        representation=representation,normalization='NFC',unit='characters_without_whitespace',
        source_sum=sources,common_theory=common,applications_sum=apps,written_denominator=common+apps,
        written=ratio(sources,common+apps),printed_program_cost=printed,raw_program_alternative=raw,
        including_printed_programs=ratio(sources,common+apps+printed),
        including_raw_programs=None if raw is None else ratio(sources,common+apps+raw),
        optional_validation_printed=optional,
        including_optional_validation=None if optional is None else ratio(sources,common+apps+printed+optional),
        program_roles=roles,conditional_prepaid=dict(full_common=common,full_declared_printed_programs=printed,total=common+printed),
        pairs=pairs,external_proof_cost=None,historical_software_cost=None,complete_graphic_cost=None,
        full_formalization_cost=None)

def make(data):
    rows=[]
    a=data['a_admission']['primary']; pairs=[]
    for q in a['conditional_applications']:
        pairs.append(pair(q['source_id'],q['application_id'],q['factor']['numerator'],q['factor']['denominator']))
    x=topic('A','Supported kernels and group presentations',a['costs']['full_umbrella'],pairs,
        a['costs']['complete_printed_program_appendix'],a['costs']['complete_raw_program_files'],
        'Four complete files in the admitted code/data/runner appendix; the finite census is a proof dependency.')
    check_old_ratio(a['written_topic'],x['source_sum'],x['written_denominator'])
    check_old_ratio(a['program_inclusive_topic'],x['source_sum'],x['written_denominator']+x['printed_program_cost'])
    rows.append(x)
    for key,title in [('B','Forest coordinates and primitive geometries'),('C','Chamber operations and binary translations')]:
        p=data['bc_results']['primary'][key]
        need(p['PDF_variant']=='raw_untrimmed', 'B/C boundary changed')
        pairs=[pair(q['source'],q['application'],q['source_cost'],q['application_cost']) for q in p['individual']]
        x=topic(key,title,p['common_theory'],pairs,p['printed_program_cost'],p['raw_program_alternative'],
            'No required mathematical program in this complete written contract.' if key=='B' else 'Two complete required GAP programs; diagnostics and operational/formal files remain separate.',
            'literal_rendered_source_plus_raw_untrimmed_pdfs')
        check_old_ratio(p['whole']['written'],x['source_sum'],x['written_denominator'])
        rows.append(x)
    p=data['d_admission']['primary']
    pairs=[pair(q['source'],q['application'],q['source_cost'],q['application_cost']) for q in p['per_result']]
    x=topic('D','Orbit counts and incidence geometries',p['common_theory'],pairs,p['printed_program_cost'],p['raw_program_cost'],
        'Eight complete programs: five required and three diagnostics. Two operational drivers are separate.')
    check_old_ratio(p['comparisons']['written_papers'],x['source_sum'],x['written_denominator']);rows.append(x)
    p=data['e_summary']; pairs=[]
    for j,q in enumerate(p['per_result_contract'],1):
        pairs.append(pair(q['source'],f'E{j}',q['full_source_length'],q['complete_application_length'],q['application']))
    x=topic('E','Projective string markings',p['common_theory'],pairs,p['required_program'],None,
        'One complete required GAP program; one optional validation program is a separate sensitivity.',optional=p['optional_validation_program'])
    need(x['written_denominator']==p['complete_written_denominator'] and x['source_sum']==p['historical_manuscripts'],'E admitted costs')
    need(abs(float(x['written']['decimal'])-p['overall_written_factor'])<2e-12,'E admitted factor');rows.append(x)
    p=data['f_admission']['primary']; c=p['costs']
    x=topic('F','Cyclotomic groups and tight hypertopes',c['U_F'],[pair('L014','F1',c['L014'],c['F1'])],c['CODE'],p['raw_costs']['complete_validation_programs'],
        'Three complete validation programs; zero uniform mathematical proof programs. Two drivers are separate.')
    check_old_ratio(p['comparisons']['written'],x['source_sum'],x['written_denominator']);rows.append(x)
    p=data['g_admission']['primary'];c=p['document_costs']
    pairs=[pair(s,q['application'],c[s],c[q['application']]) for s,q in p['conditional'].items()]
    x=topic('G','Flag relations and incidence residues',c['U_G'],pairs,c['CODE'],p['raw_costs']['complete_programs'],
        'Thirteen complete programs: four required finite computations, two witness/certificate bridges, seven validations. Three drivers are separate.')
    check_old_ratio(p['combined']['written'],x['source_sum'],x['written_denominator']);rows.append(x)
    p=data['affine_admission']['primary'];c=p['document_costs']
    x=topic('Affine','Affine groups and lattice quotients',c['U_Affine'],[pair('L012','AF1',c['L012'],c['AF1'])],c['CODE'],p['raw_program_cost'],
        'Six complete required mathematical programs; two drivers and one diagnostic are separate.')
    check_old_ratio(p['comparisons']['written_papers'],x['source_sum'],x['written_denominator']);rows.append(x)
    p=data['representation_admission']['primary'];c=p['document_costs']
    x=topic('Representation','Finite groups and incidence geometries',c['U_R'],[pair('F010','R1',c['F010'],c['R1'])],c['CODE'],p['raw_costs']['complete_validation_programs'],
        'Two complete validation programs; zero uniform finite proof premises. Two drivers are separate.')
    check_old_ratio(p['comparisons']['written_papers'],x['source_sum'],x['written_denominator']);rows.append(x)
    p=data['h_results']['primary'];c=p['documents']
    pairs=[pair(s,q['application'],c[s],c[q['application']]) for s,q in p['conditional'].items()]
    x=topic('Chamber','Chamber orbits and regular covers',c['U_H'],pairs,c['CODE'],p['raw_costs']['complete_mathematical_programs'],
        'One complete required GAP program and one diagnostic Python program. Three drivers are separate.')
    check_old_ratio(p['combined']['written'],x['source_sum'],x['written_denominator']);rows.append(x)
    # Existing immutable PDF coordinates stay unknown; the explicit new representation is distinct.
    need(data['b_admission']['primary']['overall_factor'] is None and data['c_admission']['primary']['overall_factor'] is None,'old PDF nulls changed')
    need(data['h_review']['numerical_manifest_sha256']=='89c751241470fc1595c26077b6862acd39e5566f961af98f62267aceada87931','Chamber distinct acceptance')
    result=dict(schema='programme.primary_summary.v1',status='AUTHOR_CANDIDATE_PENDING_DISTINCT_REVIEW',
        coordinate='NFC characters without whitespace, with the representation declared separately for every topic',
        topic_count=10,original_manuscript_count=27,registry_manuscripts=161,
        all_registry_manuscripts_completed=False,later_scientific_contracts_not_measured_here=['F015','L028'],pooled_factor=None,cross_topic_deduplication=False,
        new_source_credit=0,new_question_credit=0,new_formal_credit=0,
        full_source_main_result_contract=True,every_ancillary_source_assertion_recovered=False,
        unknown_costs=['retained external full proofs','historical software','full graphics and layout','end-to-end formalization'],
        topics=rows,
        notes=[
          'Every topic pays its full common paper independently, including overlap with other topics.',
          'Conditional ratios prepay the entire common paper and the complete declared printed program bundle; they do not charge only the fragment used by that application.',
          'B/C use literal complete renderings for N001/L108 and raw untrimmed PDF extraction for every other document. Their original PDF costs remain null in prior packets.',
          'All other rows use their accepted full selected PDF text and glyph calibration; recorded page furniture is excluded.',
          'G retains the L009 publisher cover in its primary numerator; its article-only sensitivity is separate.',
          'Representation reverses across units: the accepted calibrated UTF-8 written factor is about 0.970886. The character factor is not a unit-independent claim.',
          'E alone separates optional validation from its required program cost; its raw alternative was not an admitted headline and is not invented here.',
          'All source qualifications, corrected statements and excluded ancillary clauses remain in the existing scientific admissions. No mathematical status changes here.',
          'The count is 27 distinct original manuscripts in these ten measured blocks, not 27 clauses and not completion of the 161-item registry. Later accepted F015 and L028 contracts await measurement and are not silently included.'
        ])
    validate(result)
    return result

def validate(result):
    need(result['topic_count']==10 and len(result['topics'])==10,'topic count')
    need(result['pooled_factor'] is None and not result['cross_topic_deduplication'],'invalid pooled comparison')
    need(not result['all_registry_manuscripts_completed'],'registry overclaim')
    allids=[]
    for t in result['topics']:
        need(t['source_count']==len(t['pairs']),'source count')
        need(t['source_ids']==[q['source'] for q in t['pairs']],'source identity')
        allids.extend(t['source_ids'])
        need(sum(q['source_cost'] for q in t['pairs'])==t['source_sum'],'full sources not paid')
        need(sum(q['application_cost'] for q in t['pairs'])==t['applications_sum'],'full applications not paid')
        need(t['written_denominator']==t['common_theory']+t['applications_sum'],'common theory not paid')
        need(t['written']==ratio(t['source_sum'],t['written_denominator']),'written ratio')
        need(t['including_printed_programs']==ratio(t['source_sum'],t['written_denominator']+t['printed_program_cost']),'printed program charge')
        raw=t['raw_program_alternative']
        need(t['including_raw_programs']==(None if raw is None else ratio(t['source_sum'],t['written_denominator']+raw)),'raw must replace, not supplement, printed code')
        need(t['conditional_prepaid']==dict(full_common=t['common_theory'],full_declared_printed_programs=t['printed_program_cost'],total=t['common_theory']+t['printed_program_cost']),'conditional prepayment')
        need(t['representation']==('literal_rendered_source_plus_raw_untrimmed_pdfs' if t['topic'] in ['B','C'] else 'calibrated_selected_pdf'),'representation mismatch')
        for q in t['pairs']:
            need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'conditional ratio')
        for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:
            need(t[k] is None,'unknown cost as zero')
    need(len(allids)==len(set(allids))==result['original_manuscript_count']==27,'duplicate or missing original')

def write_csv(out,result):
    cols=['topic','originals','representation','sources','common','applications','written','written_factor','printed_programs','printed_factor','raw_programs','raw_factor']
    with (out/'topics.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(cols)
        for t in result['topics']:
            w.writerow([t['topic'],t['source_count'],t['representation'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['decimal'],t['printed_program_cost'],t['including_printed_programs']['decimal'],t['raw_program_alternative'],None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal']])
    with (out/'applications.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['topic','source','application','source_cost','application_cost','conditional_factor','full_common_prepaid','full_program_prepaid'])
        for t in result['topics']:
            for q in t['pairs']:
                w.writerow([t['topic'],q['source'],q['application'],q['source_cost'],q['application_cost'],q['conditional']['decimal'],t['common_theory'],t['printed_program_cost']])

def svg_graph(result, conditional=False):
    # Literal rectangle geometry is exposed and checked independently of its labels.
    from html import escape
    rows=[(t,q) for t in result['topics'] for q in t['pairs']] if conditional else [(t,None) for t in result['topics']]
    width=1000; left=170; top=60; step=36 if conditional else 57
    maxcost=max(max(q['source_cost'],q['application_cost']) if q else max(t['source_sum'],t['written_denominator']) for t,q in rows)
    scale=720/maxcost; height=top+len(rows)*step+65
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
       '<rect width="100%" height="100%" fill="white"/>',
       '<style>text{font-family:Arial,sans-serif;font-size:18px;fill:#172333} .small{font-size:16px}</style>',
       f'<text x="20" y="23">{"Each full source and its complete application (common theory already acquired)" if conditional else "Full source manuscripts and full common theory plus applications"}</text>',
       '<rect x="20" y="35" width="13" height="10" fill="#333d4c"/><text class="small" x="39" y="45">Sources</text>',
       '<rect x="130" y="35" width="13" height="10" fill="#236b8e"/><text class="small" x="150" y="45">Common theory</text>' if not conditional else '',
       '<rect x="350" y="35" width="13" height="10" fill="#71b3ab"/><text class="small" x="369" y="45">Applications</text>']
    for i,(t,q) in enumerate(rows):
        y=top+i*step
        name=f"{'R' if t['topic']=='Representation' else t['topic']} {q['source']}" if q else t['topic']+('*' if t['topic'] in ['B','C'] else '')
        s.append(f'<text x="10" y="{y+18}">{escape(name)}</text>')
        vals=[('source',q['source_cost'] if q else t['source_sum'],left,y,'#333d4c')]
        if q: vals.append(('application',q['application_cost'],left,y+13,'#71b3ab'))
        else: vals.extend([('common',t['common_theory'],left,y+17,'#236b8e'),('applications',t['applications_sum'],left+t['common_theory']*scale,y+17,'#71b3ab')])
        for kind,v,x,yy,col in vals:
            rid=f"{t['topic']}-{q['source']+'-' if q else ''}{kind}"
            s.append(f'<rect id="bar-{rid}" data-cost="{v}" x="{x:.8f}" y="{yy}" width="{v*scale:.8f}" height="10" fill="{col}"/>')
        fac=q['conditional']['decimal'] if q else t['written']['decimal']
        s.append(f'<text class="small" x="915" y="{y+17}">{float(fac):.3f}</text>')
    s.extend([f'<text class="small" x="170" y="{height-30}">Bar length: NFC characters without whitespace; factors at right.</text>',
       f'<text class="small" x="20" y="{height-10}">{"All conditional factors prepay the full topic common theory and declared programs." if conditional else "* B/C use literal rendered sources plus untrimmed PDFs. No pooled factor is formed."}</text>','</svg>'])
    return '\n'.join(s)+'\n'

def tex(result):
    def n(v): return f'{v:,}'
    def fac(r): return f"{float(r['decimal']):.3f}"
    def name(t): return 'Represent.' if t=='Representation' else t
    trows=[];prows=[];arows=[]
    for t in result['topics']:
        k=name(t['topic'])+('$^*$' if t['topic'] in ['B','C'] else '')
        trows.append(' & '.join([k,str(t['source_count']),n(t['source_sum']),n(t['common_theory']),n(t['applications_sum']),n(t['written_denominator']),fac(t['written'])])+r' \\')
        prows.append(' & '.join([k,n(t['printed_program_cost']),fac(t['including_printed_programs']), '--' if t['raw_program_alternative'] is None else n(t['raw_program_alternative']), '--' if t['including_raw_programs'] is None else fac(t['including_raw_programs']),n(t['conditional_prepaid']['total'])])+r' \\')
        for q in t['pairs']:
            arows.append(' & '.join([k,q['source'],q['application'],n(q['source_cost']),n(q['application_cost']),fac(q['conditional'])])+r' \\')
    head=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=22mm]{geometry}
\usepackage{fontspec}\setmainfont{STIXGeneral}
\usepackage{amsmath,booktabs,array,graphicx,xcolor,hyperref}
\hypersetup{colorlinks=true,linkcolor=blue,urlcolor=blue}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\smalltable}{\small\setlength{\tabcolsep}{5pt}\renewcommand{\arraystretch}{1.13}}
\begin{document}
\begin{center}\Large\textbf{Ten topics: complete papers and conditional applications}\end{center}
This report brings together the accepted measurements for \textbf{27 distinct original manuscripts} in ten canonical topics. It does not complete the 161-item registry. The later accepted F015 and L028 contracts are not yet measured and are outside this fixed numerical baseline. The task is to derive the specified main results from complete common theories and applications, with corrections, retained outside theorems and exclusions recorded in each scientific admission. No new mathematical result or source credit is asserted here.

For topic $T$, write $S_T=\sum_i c(L_i)$ for the full original manuscripts, $U_T=c(U)$ for the entire common paper, and $A_T=\sum_i c(A_i)$ for all complete applications. The two headline comparisons are
\[
 R_T=\frac{S_T}{U_T+A_T},\qquad
 r_{T,i}=\frac{c(L_i)}{c(A_i)}\quad
 \text{after acquiring all of $U$ and the declared programs.}
\]
Every topic pays its own whole common theory even when another topic contains overlapping mathematics. A factor above one means fewer measured characters in the replacement; a factor below one means more. The conditional factors do not describe a complete replacement obtained at the cost of the application alone.

\textbf{Complete written papers.} Costs below are NFC characters without whitespace, at each topic's accepted primary representation. They include introductions, definitions, proof text and references as prescribed by the fixed input boundaries.
\begin{center}\smalltable
\begin{tabular}{lrrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Ours & Factor\\\midrule
'''
    body='\n'.join(trows)+r'''
\bottomrule\end{tabular}\end{center}
\textbf{Representation matters.} Unstarred rows use the accepted full selected PDF text with calibrated glyphs and recorded page furniture excluded. In B and C, N001 and L108 are complete literal text renderings; every other source and every replacement PDF in those two comparisons is counted \emph{untrimmed}. No speculative symbol repair is made to the rendered bodies. Their original PDF costs remain unknown in the earlier PDF records. These two representations are not pooled into a programme-wide factor.

The full-source numerator concerns the agreed principal results, not every ancillary assertion. Retained external proofs, unknown historical software, full image/layout information and end-to-end formalization have no invented zero cost. The tables measure documents under the admitted boundaries, not an absolute minimum proof complexity.
\newpage
\textbf{Whole-topic written costs.} Each dark bar is the complete source sum. The paired bar pays the entire common theory (blue) and all complete applications (green). Both bars use the same scale. The separate representations for B and C remain explicit.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The displayed factors retain cases that do not shorten the written record: Affine, G and Chamber are longer overall in this coordinate. Small factors above one also require the stated unit: for Representation, the admitted calibrated UTF-8 comparison is approximately $0.970886$, rather than above one. Other units and boundary sensitivities remain available in the underlying packets; this report does not select a different favourable coordinate for each row.

G includes the L009 publisher cover in its primary numerator; its article-only alternative is separate. E uses its current readable edition, with the added motivation and clarifications charged in full. No earlier, shorter language edition is substituted.
\newpage
\textbf{Complete programs and prior acquisition.} The following alternatives add the entire declared printed program appendix to the written denominator, or replace that appendix by the cost of its whole raw files. Printed and raw versions are never both charged. These costs include different roles, made explicit below; validations are not silently described as mathematical premises.
\begin{center}\smalltable
\begin{tabular}{lrrrrr}\toprule
Topic & Printed code & With printed & Raw alternative & With raw & $U+$printed\\\midrule
'''+ '\n'.join(prows)+r'''
\bottomrule\end{tabular}\end{center}
The final column is the full prepaid amount for every conditional row on the next page. B has no required mathematical program in its complete written contract. E's optional validation file adds a further 5,173 characters; including it gives factor $1.372$. E's raw alternative is not introduced here because it was not an admitted headline coordinate.

\begin{itemize}\setlength\itemsep{1pt}
\item A: four complete files in the admitted code, data and runner appendix; C: two required GAP programs; Affine: six required mathematical programs.
\item D: five required programs and three diagnostics. G: four required finite computations, two programs for witnesses and certificates, and seven validations. Chamber: one required GAP program and one diagnostic.
\item E: one required GAP program, with one optional validation program shown separately. F: three validation programs and no uniform finite proof premise. Representation: two validation programs and no uniform finite proof premise.
\end{itemize}
Other operational drivers and partial Lean evidence remain separately inventoried in the underlying admissions. Their absence from a written-paper denominator is explicit, not a claim that execution, verification or full formalization is free. The programme comparison is conditioned on the named retained mathematical inputs; their full proof costs remain unknown. No claim about a historical software cost follows from its absence from a supplied manuscript.

\textbf{Mathematical interpretation.} Each common paper is charged once within its topic. Every application retains its complete local proof obligations. A short application can therefore express a substantial consequence after common theory has been established; it does not establish historical novelty of that common theory. Attribution and corrected source claims remain governed by the accepted source maps.
\newpage
\textbf{Every original and its complete application.} These are conditional comparisons after the full acquisition shown on the previous page. E1--E3 are display names for the admitted files New\_A1--New\_A3. No application or original is omitted because its factor is below one.
\begin{center}\smalltable
\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Original cost & Application cost & Conditional\\\midrule
'''+ '\n'.join(arows)+r'''
\bottomrule\end{tabular}\end{center}
The original identifiers are unique across these ten topics. The machine-readable companion supplies exact fractions, all input hashes and the full source/application lists. The existing topic packets preserve all measured units and sensitivities. This consolidation changes no proof, source boundary, conjecture status or existing numerical input.
\newpage
\textbf{Application costs after common theory acquisition.} Dark bars show complete originals; green bars show complete applications. The full common theory and declared programs have already been acquired independently for each topic. The bars measure text cost, not theorem counts.
\begin{center}\includegraphics[width=\linewidth,height=0.82\textheight,keepaspectratio]{conditional_applications.pdf}\end{center}
\end{document}
'''
    return head+body

def render_graphs(out):
    # Render the exact SVG rectangle/text geometry without a second cost calculation.
    import xml.etree.ElementTree as ET
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle
    for stem in ['whole_topics','conditional_applications']:
        root=ET.parse(out/(stem+'.svg')).getroot();w,h=float(root.attrib['width']),float(root.attrib['height'])
        fig=plt.figure(figsize=(w/72,h/72));ax=fig.add_axes([0,0,1,1]);ax.set_xlim(0,w);ax.set_ylim(h,0);ax.axis('off')
        for el in root:
            tag=el.tag.rsplit('}',1)[-1]
            if tag=='rect' and el.get('id','').startswith('bar-'):
                ax.add_patch(Rectangle((float(el.get('x')),float(el.get('y'))),float(el.get('width')),float(el.get('height')),color=el.get('fill'),linewidth=0))
            elif tag=='rect' and el.get('width')!='100%':
                ax.add_patch(Rectangle((float(el.get('x')),float(el.get('y'))),float(el.get('width')),float(el.get('height')),color=el.get('fill'),linewidth=0))
            elif tag=='text':
                ax.text(float(el.get('x')),float(el.get('y')),el.text or '',fontsize=16 if el.get('class')=='small' else 18,color='#172333',fontfamily='DejaVu Sans',va='baseline')
        fig.savefig(out/(stem+'.pdf'),metadata={'Creator':'programme_measurement_summary_v1','CreationDate':None,'ModDate':None});plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--public-root',type=Path,default=Path('/Users/sasha/medusa/math_compression'));p.add_argument('--study-root',type=Path,default=Path('/Users/sasha/medusa/research/leemans'));p.add_argument('--locations',type=Path);p.add_argument('--out',type=Path,required=True);p.add_argument('--pdf-graphs',action='store_true');args=p.parse_args()
    spec=json.loads((HERE/'inputs.json').read_text());data=load_inputs(spec,args.public_root,args.study_root,None if args.locations is None else json.loads(args.locations.read_text()))
    result=make(data);args.out.mkdir(parents=True,exist_ok=True)
    dump(args.out/'results.json',result);write_csv(args.out,result)
    (args.out/'whole_topics.svg').write_text(svg_graph(result));(args.out/'conditional_applications.svg').write_text(svg_graph(result,True));(args.out/'summary.tex').write_text(tex(result))
    if args.pdf_graphs:render_graphs(args.out)
    print('PASS: 10 topics, 27 distinct originals, complete common/application/program costs; no pooled factor')

if __name__=='__main__': main()
