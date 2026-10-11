#!/usr/bin/env python3
"""Consolidate admitted primary values; no source extraction or scientific replay."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse, copy, csv, hashlib, io, json, os, subprocess, textwrap

ROOT=Path(__file__).resolve().parent
TITLES={
 'A':'Supported kernels and finite two-groups',
 'B':'Forests and high-rank permutation groups',
 'C':'Chamber operations and binary translations',
 'D':'Stabilizer actions and geometry enumeration',
 'E':'Projective groups and string markings',
 'F':'Odd kernels and tight hypertopes',
 'G':'Linear spaces and incidence residues',
 'Affine':'Affine groups and lattice quotients',
 'Representation':'Realizing groups as geometry automorphisms',
 'Chamber':'Chamber systems and regular covers',
 'Matching':'Matching extensions of centrally symmetric polytopes',
 'ChiralEnumeration':'Complete enumeration of chiral polytopes',
 'Diagonal':'Orbit constructions: N007 edition'}
SHORT={'Representation':'Represent.','ChiralEnumeration':'Chiral','Diagonal':'Diagonal*'}

def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,x): p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ratio(n,d):
    need(type(n) is int and type(d) is int and n>0 and d>0,'invalid whole cost')
    f=Fraction(n,d)
    with localcontext() as c:
        c.prec=50; dec=f'{Decimal(n)/Decimal(d):.12f}'
    return {'numerator':n,'denominator':d,'exact_fraction':str(f),'decimal':dec}
def same_ratio(x,n,d):
    need(x['numerator']==n and x['denominator']==d,'changed admitted numerator/denominator')
    if 'exact_fraction' in x: need(Fraction(x['exact_fraction'])==Fraction(n,d),'admitted fraction')
    if 'reduced_numerator' in x: need(Fraction(x['reduced_numerator'],x['reduced_denominator'])==Fraction(n,d),'admitted reduction')
    if 'decimal' in x: need(abs(Decimal(x['decimal'])-Decimal(n)/Decimal(d))<Decimal('0.000000000002'),'admitted decimal')

def load_inputs(public=None):
    p=json.loads((ROOT/'protocol.json').read_text()); data={}
    for key,b in p['bindings'].items():
        raw=(ROOT/b['local']).read_bytes()
        need(len(raw)==b['bytes'] and sha(raw)==b['sha256'],'copied binding '+key)
        if public is not None:
            original=subprocess.check_output(['git','show',b['commit']+':'+b['path']],cwd=public)
            need(original==raw,'committed input '+key)
        data[key]=json.loads(raw)
    for k in ['old','ac','b5','additional','diagonal']:
        admission=data[k+'_admission']; rows=admission['artifacts']
        need(admission['status'].startswith('ROOT_ADMITTED'),'input not admitted')
        for suffix in ['results','manifest','review']:
            b=p['bindings'][k+'_'+suffix]
            need(any(x['path']==b['path'] and x['sha256']==b['sha256'] and x['bytes']==b['bytes'] for x in rows),'admission route '+k+suffix)
        mf=data[k+'_manifest']; b=p['bindings'][k+'_results']
        need(any(x['path']=='results.json' and x['sha256']==b['sha256'] and x['bytes']==b['bytes'] for x in mf['exports']),'results not author-bound')
    return p,data

def pair(q):
    r={'source':q['source'],'application':q['application'],'source_cost':q['source_cost'],
       'application_cost':q['application_cost'],'source_representation':q.get('source_representation','complete_PDF_calibrated_selected'),
       'conditional':ratio(q['source_cost'],q['application_cost'])}
    same_ratio(q['conditional'],r['source_cost'],r['application_cost']);return r

def recompute(t):
    t['title']=TITLES[t['topic']]
    t['source_count']=len(t['pairs']);t['source_ids']=[q['source'] for q in t['pairs']]
    t['source_sum']=sum(q['source_cost'] for q in t['pairs'])
    t['applications_sum']=sum(q['application_cost'] for q in t['pairs'])
    t['written_denominator']=t['common_theory']+t['applications_sum']
    t['written']=ratio(t['source_sum'],t['written_denominator'])
    t['including_printed_programs']=ratio(t['source_sum'],t['written_denominator']+t['printed_program_cost'])
    raw=t['raw_program_alternative']
    t['including_raw_programs']=None if raw is None else ratio(t['source_sum'],t['written_denominator']+raw)
    optional=t.get('optional_validation_printed')
    t['including_optional_validation']=None if optional is None else ratio(t['source_sum'],t['written_denominator']+t['printed_program_cost']+optional)
    t['conditional_prepaid']={'full_common':t['common_theory'],'full_declared_printed_programs':t['printed_program_cost'],
                              'total':t['common_theory']+t['printed_program_cost']}
    t['common_components']=t.get('common_components',{'whole_common_paper':t['common_theory']})
    t['normalization']='NFC';t['unit']='characters_without_whitespace'
    for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']: t[k]=None
    return t

def expanded(k,p):
    t=recompute({'topic':k,'common_theory':p['common_theory'],'common_components':p['common_components'],
                 'pairs':[pair(q) for q in p['individual']], 'printed_program_cost':p['printed_program_cost'],
                 'raw_program_alternative':p['raw_program_alternative'],
                 'printed_program_components':p['printed_program_components'],'raw_program_components':p['raw_program_components'],
                 'representation':'literal_rendered_source_plus_raw_untrimmed_pdfs' if k in ['B','C'] else 'calibrated_selected_pdf'})
    for key in ['written','including_printed_programs','including_raw_programs']:
        same_ratio(p['whole'][key],t[key]['numerator'],t[key]['denominator'])
    need(p['conditional_acquisition']['full_common']==t['common_theory'] and p['conditional_acquisition']['full_printed_programs']==t['printed_program_cost'],'expanded acquisition')
    return t

def single(k,p,app):
    c=p['document_costs']; raw=p['raw_costs'].get('complete_programs',p['raw_costs'].get('programs'))
    t=recompute({'topic':k,'common_theory':c['common'],'pairs':[pair({'source':p['source_id'],'application':app,'source_cost':c['source'],'application_cost':c['application'],'conditional':p['comparisons']['conditional_application']})],
                 'printed_program_cost':c['program'],'raw_program_alternative':raw,'representation':'calibrated_selected_pdf','separate_raw_inventory':p['raw_costs']})
    for key in ['written','including_printed_programs','including_raw_programs']:
        same_ratio(p['comparisons'][key],t[key]['numerator'],t[key]['denominator'])
    return t

def make(data,protocol):
    old=data['old_results']; rows={t['topic']:copy.deepcopy(t) for t in old['topics']}
    for k,t in rows.items():
        for q in t['pairs']: q.setdefault('source_representation','complete_PDF_calibrated_selected')
        t['source_admission']=protocol['bindings']['old_admission']['path']
        t['admitted_numeric_origin']='old_results/topics/'+k
        recompute(t)
    for k in ['A','C']:
        rows[k]=expanded(k,data['ac_results']['primary'][k]);rows[k]['source_admission']=protocol['bindings']['ac_admission']['path'];rows[k]['admitted_numeric_origin']='ac_results/primary/'+k
    rows['B']=expanded('B',data['b5_results']['primary']['B']);rows['B']['source_admission']=protocol['bindings']['b5_admission']['path'];rows['B']['admitted_numeric_origin']='b5_results/primary/B'
    for k,app in [('Matching','M1'),('ChiralEnumeration','CE1')]:
        rows[k]=single(k,data['additional_results']['primary'][k],app);rows[k]['source_admission']=protocol['bindings']['additional_admission']['path'];rows[k]['admitted_numeric_origin']='additional_results/primary/'+k
    rows['Diagonal']=single('Diagonal',data['diagonal_results']['primary']['Diagonal'],'DG1')
    rows['Diagonal'].update({'source_admission':protocol['bindings']['diagonal_admission']['path'],'admitted_numeric_origin':'diagonal_results/primary/Diagonal','measured_edition_scope':'earlier N007-only common paper and application; not the enlarged N006+N007 theory'})
    roles={
      'A':'Five full files: the earlier complete four-file census/data/runner bundle and the new rank-three minimum GAP program.',
      'B':'Four full files: one primitive-group finite premise, two validations and one auxiliary n=8 example; two new drivers separate.',
      'C':'Three full GAP programs: earlier construction and exhaustive census plus Livingstone check. The identical shared construction is charged once within C.',
      'Matching':'One complete required exceptional-orbit census; driver and scoped Lean source separate.',
      'ChiralEnumeration':'Three whole files: reference enumeration, formula evaluation and involution validation; the uniform written proof is separate.',
      'Diagonal':'One whole validation program; no uniform finite proof premise. Two drivers and scoped Lean file separate.'}
    for k,v in roles.items(): rows[k]['program_roles']=v
    result={'schema':'programme.primary_summary.v2','status':'AUTHOR_CANDIDATE_PENDING_DISTINCT_REVIEW',
      'measurement_baseline_commit':protocol['measurement_baseline_commit'],'scope_update_commit':protocol['unmeasured_scope_update_commit'],
      'coordinate':'NFC characters without whitespace, at each declared admitted representation',
      'topic_count':13,'original_manuscript_count':33,'registry_manuscripts':161,'accessible_originals':104,
      'currently_admitted_originals':34,'accessible_pending_complete_recovery':70,'pending_source_retrieval':57,
      'all_registry_manuscripts_completed':False,'pooled_factor':None,'cross_topic_deduplication':False,
      'new_source_credit':0,'new_question_credit':0,'new_formal_credit':0,
      'topics':[rows[k] for k in TITLES],
      'unmeasured':[{'source':'N006','topic':'Diagonal','scientific_admission':protocol['bindings']['n006_admission']['path'],
       'status':'admitted; measurement of enlarged N006+N007 topic pending','source_cost':None,'common_theory':None,
       'application_cost':None,'program_cost':None,'whole_factor':None,'conditional_factor':None,
       'prior_N007_factor_not_transferred':True}],
      'scope':'Complete source documents matched to admitted specified principal-result recoveries, with all recorded corrections, retained inputs and excluded ancillary clauses preserved.',
      'notes':['All complete common papers are paid within each topic. B pays both common papers; C pays its added incidence note.',
       'Each conditional factor prepays the full enlarged common theory and all complete declared programs; it is not a standalone application saving.',
       'Printed and raw code are alternative representations, never additive. E optional validation remains a separate admitted sensitivity.',
       'B and C use complete authored N001/L108 renderings and raw untrimmed PDFs. Their older unavailable-PDF coordinates stay null.',
       'Every other row retains its accepted selected calibrated PDF coordinate. No pooled factor or cross-topic common discount is formed.',
       'Unknown external proof, historical software, complete graphic and full formalization costs are null, not zero.',
       'All introductions, references and local context covered by each fixed whole-document boundary remain charged.',
       'N006 is unmeasured. The displayed Diagonal row is the earlier N007-only edition; its factor does not describe the enlarged current topic.',
       'The 33 measured originals are a subset of the 161-item programme, not a stopping boundary. The old 27-original overview remains immutable.']}
    ids=sorted(q['source'] for t in result['topics'] for q in t['pairs'])
    need(ids==sorted(data['corpus_baseline']['measured_original_ids'])==sorted(data['corpus_current']['measured_original_ids']),'corpus measured ID equality')
    need(data['corpus_current']['measurement_pending_original_ids']==['N006'],'pending source identity')
    need(data['n006_admission']['compression_factor'] is None and data['n006_admission']['measurement_status']=='pending','N006 measured without adoption')
    validate(result);return result

def validate(r):
    need(r['topic_count']==len(r['topics'])==13,'13 topics')
    need(r['pooled_factor'] is None and r['cross_topic_deduplication'] is False,'no pooled factor/discount')
    need(r['all_registry_manuscripts_completed'] is False and r['registry_manuscripts']==161,'whole corpus overclaim')
    need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'new credit')
    ids=[]
    for t in r['topics']:
        need(t['title']==TITLES[t['topic']],'descriptive title changed')
        need(sum(t['common_components'].values())==t['common_theory'],'complete common components')
        need(sum(q['source_cost'] for q in t['pairs'])==t['source_sum'],'full sources')
        need(sum(q['application_cost'] for q in t['pairs'])==t['applications_sum'],'full applications')
        need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'source list')
        need(t['written_denominator']==t['common_theory']+t['applications_sum'],'written denominator')
        for key,d in [('written',t['written_denominator']),('including_printed_programs',t['written_denominator']+t['printed_program_cost'])]: need(t[key]==ratio(t['source_sum'],d),'whole ratio')
        raw=t['raw_program_alternative']
        need(t['including_raw_programs']==(None if raw is None else ratio(t['source_sum'],t['written_denominator']+raw)),'raw replaces printed')
        need(t['conditional_prepaid']=={'full_common':t['common_theory'],'full_declared_printed_programs':t['printed_program_cost'],'total':t['common_theory']+t['printed_program_cost']},'whole acquisition')
        for q in t['pairs']: need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'conditional ratio');ids.append(q['source'])
        need(t['representation']==('literal_rendered_source_plus_raw_untrimmed_pdfs' if t['topic'] in ['B','C'] else 'calibrated_selected_pdf'),'representation')
        for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k] is None,'unknown cost')
    need(len(ids)==len(set(ids))==r['original_manuscript_count']==33,'33 distinct originals')
    u=r['unmeasured'];need(len(u)==1 and u[0]['source']=='N006' and u[0]['prior_N007_factor_not_transferred'] is True,'N006 scope')
    for k in ['source_cost','common_theory','application_cost','program_cost','whole_factor','conditional_factor']:need(u[0][k] is None,'unmeasured N006 assigned number')
    e=next(t for t in r['topics'] if t['topic']=='E')
    need(e['raw_program_alternative'] is None and e['optional_validation_printed']==5173,'E extra alternative invented/pruned')
    need(e['including_optional_validation']==ratio(e['source_sum'],e['written_denominator']+e['printed_program_cost']+5173),'E optional ratio')

def csv_text(r):
    ans={}; f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n')
    w.writerow(['topic','title','originals','representation','sources','common','applications','written','written_factor','printed_programs','printed_factor','raw_programs','raw_factor'])
    for t in r['topics']:w.writerow([t['topic'],t['title'],t['source_count'],t['representation'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['decimal'],t['printed_program_cost'],t['including_printed_programs']['decimal'],t['raw_program_alternative'],None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal']])
    ans['topics.csv']=f.getvalue();f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n')
    w.writerow(['topic','title','source','application','source_cost','application_cost','conditional_exact','conditional_factor','full_common_prepaid','full_program_prepaid','source_representation'])
    for t in r['topics']:
        for q in t['pairs']: w.writerow([t['topic'],t['title'],q['source'],q['application'],q['source_cost'],q['application_cost'],q['conditional']['exact_fraction'],q['conditional']['decimal'],t['common_theory'],t['printed_program_cost'],q['source_representation']])
    ans['applications.csv']=f.getvalue();return ans

def plot_spec(r,kind):
    rows=[]
    if kind=='whole_topics':
        for t in r['topics']:
            segments=[{'id':'common-'+k,'cost':v,'role':'common'} for k,v in t['common_components'].items()]
            segments += [{'id':q['application'],'cost':q['application_cost'],'role':'application'} for q in t['pairs']]
            rows.append({'id':t['topic'],'label':SHORT.get(t['topic'],t['topic'])+': '+t['title'],'source':t['source_sum'],'segments':segments,'factor':t['written']['decimal']})
    else:
        pairs=[(t,q) for t in r['topics'] for q in t['pairs']]
        if kind=='conditional_1':pairs=pairs[:17]
        elif kind=='conditional_2':pairs=pairs[17:]
        for t,q in pairs:rows.append({'id':t['topic']+'-'+q['source'],'label':q['source']+' / '+q['application'],'topic':t['topic'],'title':t['title'],'source':q['source_cost'],'segments':[{'id':q['application'],'cost':q['application_cost'],'role':'application'}],'factor':q['conditional']['decimal']})
    return {'kind':kind,'rows':rows,'unit':'NFC characters without whitespace','bar_scale':'one common linear scale per chart; identical for source and replacement','pending_N006':'no bar, no zero placeholder'}

def draw(spec,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'overview33-fixed','pdf.fonttype':42})
    rows=spec['rows'];whole=spec['kind']=='whole_topics';fig,ax=plt.subplots(figsize=(10.2,8.0 if whole else 8.6))
    fig.subplots_adjust(left=.37 if whole else .34,right=.91,top=.94,bottom=.08)
    ymax=max(max(q['source'],sum(x['cost'] for x in q['segments'])) for q in rows); ax.set_xlim(0,ymax*1.13)
    for i,row in enumerate(rows):
        b=ax.barh(i-.16,row['source'],height=.25,color='#344354');b[0].set_gid('bar-'+row['id']+'-source')
        start=0
        for j,s in enumerate(row['segments']):
            color='#286e99' if s['role']=='common' else ['#81bdb0','#61a294'][j%2]
            b=ax.barh(i+.16,s['cost'],left=start,height=.25,color=color,edgecolor='white',linewidth=.4);b[0].set_gid('bar-'+row['id']+'-'+s['id']);start+=s['cost']
        ax.text(ymax*1.14,i,f"{float(row['factor']):.3f}×",va='center',fontsize=10,clip_on=False)
    labels=['\n'.join(textwrap.wrap(q['label'] if whole else SHORT.get(q['topic'],q['topic'])+' · '+q['label'],35 if whole else 30)) for q in rows]
    ax.set_yticks(range(len(rows)),labels);ax.invert_yaxis();ax.tick_params(axis='y',length=0,pad=9)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x,pos:f'{int(x):,}'));ax.grid(axis='x',alpha=.22);ax.set_axisbelow(True)
    for spine in ['top','right','left']:ax.spines[spine].set_visible(False)
    ax.set_xlabel('NFC characters without whitespace')
    from matplotlib.patches import Patch
    handles=[Patch(color='#344354',label='Full original(s)')]
    if whole:handles.append(Patch(color='#286e99',label='Full common theory'))
    handles.append(Patch(color='#81bdb0',label='Complete application(s)'))
    fig.legend(handles=handles,loc='upper center',ncol=len(handles),frameon=False,fontsize=10)
    meta={'Creator':'Human Compression admitted-value overview','CreationDate':None,'ModDate':None}
    fig.savefig(out/(spec['kind']+'.pdf'),metadata=meta);fig.savefig(out/(spec['kind']+'.svg'),metadata={'Date':None});plt.close(fig)

def tex(r):
    n=lambda x:f'{x:,}'; f=lambda q:f"{float(q['decimal']):.3f}"; short=lambda t:SHORT.get(t,t)
    heads=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\tabsetup}{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.12}}
\begin{document}
\begin{center}\Large\textbf{Complete papers and shared theories}\\[4pt]
\normalsize Thirteen measured sets, thirty-three original manuscripts\end{center}
This additive overview brings together admitted values. It preserves the earlier 27-original report, adds Matching, Chiral enumeration and the N007 comparison, and uses the enlarged A, B and C editions. The numerical baseline is commit \texttt{c6b1b13}. The subsequent N006 admission is shown separately as \emph{unmeasured}; the old N007 factor does not describe the enlarged orbit-construction topic.

For each topic, $S=\sum_i c(L_i)$ counts the complete originals, $U$ every complete common paper, and $A=\sum_i c(A_i)$ every complete application. The two headline comparisons are
\[
 R=\frac{S}{U+A},\qquad r_i=\frac{c(L_i)}{c(A_i)}
 \quad\text{after acquiring all common theory and declared programs.}
\]
Every topic pays its common theory independently, even when proofs overlap other topics. A factor above one means a shorter replacement in the stated coordinate; a factor below one means a longer replacement. Conditional factors are not standalone application savings.

\textbf{Complete written costs.} All values below are NFC characters excluding whitespace. The fixed whole-document boundaries include their introductions, proofs, local context and references.
\begin{center}\tabsetup\begin{tabular}{lrrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Written & Factor\\\midrule
'''
    rows=[]
    for t in r['topics']: rows.append(' & '.join([short(t['topic']),str(t['source_count']),n(t['source_sum']),n(t['common_theory']),n(t['applications_sum']),n(t['written_denominator']),f(t['written'])])+r' \\')
    s=heads+'\n'.join(rows)+r'''
\bottomrule\end{tabular}\end{center}
\textbf{Representations remain distinct.} B and C use complete authored text renderings for N001 and L108; all other source and replacement PDFs in those two topics are counted raw and untrimmed. Their older original-PDF coordinates remain unknown. The other rows use accepted calibrated, selected PDF text with exact repeated furniture removed. No pooled factor across these representations is formed.

\textbf{Scope.} These are 33 measured originals within the fixed 161-item programme. The current scientific register has 34 admitted recoveries among 104 accessible originals, with N006 awaiting measurement; 70 accessible originals await complete recovery and 57 remain retrieval targets. Complete numerators match the declared principal-result contracts, with corrections, retained facts and ancillary exclusions preserved. This report changes no scientific, question or formal credit.
\newpage
\textbf{Full common theories and applications.}
Each row has one scale for its original sum and replacement. Blue segments are whole common papers; green segments are individual complete applications. B pays both common papers (14,124 and 28,423). C pays its original common paper (27,142) and the entire incidence note (3,295). All segments remain charged.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The Diagonal row concerns only the earlier N007 edition. There is no bar or numerical placeholder for N006, and no measured whole-topic factor for the expanded N006+N007 edition. Text length is not a minimum proof complexity or a measure of mathematical originality.
\newpage
\textbf{Complete programs and prior acquisition.}
The written comparison remains first. These separate alternatives add the entire declared printed appendix, or its entire raw program files, to the written denominator. Printed and raw code are never added together.
\begin{center}\tabsetup\begin{tabular}{lrrrrr}\toprule
Topic & Printed code & With printed & Raw code & With raw & $U+$printed\\\midrule
'''
    for t in r['topics']:
        s+=' & '.join([short(t['topic']),n(t['printed_program_cost']),f(t['including_printed_programs']),'--' if t['raw_program_alternative'] is None else n(t['raw_program_alternative']),'--' if t['including_raw_programs'] is None else f(t['including_raw_programs']),n(t['conditional_prepaid']['total'])])+r' \\'+'\n'
    s+=r'''\bottomrule\end{tabular}\end{center}
The final column is prepaid in every conditional row for that topic. E preserves its admitted convention: its optional validation program costs another 5,173 characters and gives a separate program-inclusive factor of 1.372. An unadmitted raw-code alternative for E is not invented here.

\textbf{Program roles.} A includes all five files. B includes one finite proof premise, two validations and an auxiliary example. C includes its three complete GAP files; the identical shared construction is charged once, and its exhaustive census remains paid. D includes five required and three diagnostic programs. E separates one required program from optional validation. F's three programs and Representation's two are validations, not uniform proof premises. G retains four finite computations, two certificate bridges and seven validations. Affine retains all six mathematical programs. Chamber retains one required GAP program and one diagnostic. Matching's census is a finite premise. Chiral enumeration retains all three enumeration/formula/validation programs. The N007 edition includes its whole validation program. Separate operational drivers and partial Lean inventories stay separate, as in the admitted packets.

\textbf{Limits.} Retained full external proofs, unprovided historical software, complete graphic information and end-to-end formalization have unknown costs, not zero. Units matter: Representation's written factor is about 0.971 in its admitted UTF-8 coordinate, and Chiral enumeration is about 1.003 in whitespace tokens but 0.925 in nonspace characters. All underlying multi-unit sensitivities remain available; this table consistently uses the declared primary character coordinate.
\newpage
\textbf{Every complete application after full acquisition.}
All common papers and all declared programs in the preceding table have already been paid. The source and application are complete documents under the same topic boundary; no smaller theorem closure replaces either side.
\begin{center}\tabsetup\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Source cost & Application cost & Conditional\\\midrule
'''
    for t in r['topics']:
        for q in t['pairs']:s+=' & '.join([short(t['topic']),q['source'],q['application'],n(q['source_cost']),n(q['application_cost']),f(q['conditional'])])+r' \\'+'\n'
    s+=r'''\bottomrule\end{tabular}\end{center}
The asterisk on Diagonal identifies the earlier N007-only acquisition. These individual factors cannot be transferred to a new common edition without a newly fixed measurement. No node-count factor is used.
\newpage
\textbf{Individual source and application costs: first seventeen originals.}
Dark bars show complete originals; green bars show their complete applications. Factors at right assume full prior acquisition, including the enlarged B and C common theory and all declared programs. A shared scale is used within this chart.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
Source IDs are stable catalogue labels. Their exact definitions, source editions and proof contracts remain in the linked admitted measurements; they are not additional mathematical claims of this overview.
\newpage
\textbf{Individual source and application costs: remaining sixteen originals.}
The same conventions apply; the scale is shared by every source/application pair in this chart. No cost for N006 is inferred from the last row.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\textbf{Exact data and provenance.} The accompanying \texttt{results.json}, \texttt{topics.csv} and \texttt{applications.csv} retain exact integer costs and rational factors. \texttt{protocol.json} pins the old admitted overview, four admitted numerical updates, their independent records and the unmeasured N006 admission. No primary text was copied or extracted in this consolidation. Graph bars use these same costs; they do not depict theorem counts or claims of optimality. The new consolidation requires distinct review before publication.
\end{document}
'''
    return s

def build(out,public=None,render=False,xelatex='xelatex'):
    need(not out.exists() and not out.is_symlink(),'output must be fresh');out.mkdir(parents=True)
    protocol,data=load_inputs(public);r=make(data,protocol);dump(out/'results.json',r)
    for name,s in csv_text(r).items():(out/name).write_text(s)
    specs={k:plot_spec(r,k) for k in ['whole_topics','conditional_1','conditional_2']};dump(out/'plot_data.json',specs)
    os.environ.setdefault('MPLCONFIGDIR',str(out/'mpl-cache'));os.environ.setdefault('XDG_CACHE_HOME',str(out/'cache'))
    for spec in specs.values():draw(spec,out)
    (out/'summary.tex').write_text(tex(r));diagnostics=[]
    if render:
        for i in range(2):
            p=subprocess.run([xelatex,'-interaction=nonstopmode','-halt-on-error','summary.tex'],cwd=out,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
            (out/f'xelatex-{i+1}.log').write_bytes(p.stdout);need(p.returncode==0,'TeX build failed')
        s=(out/'summary.log').read_text(errors='replace')
        diagnostics=[line for line in s.splitlines() if any(x in line for x in ['Overfull','Missing character','Font Warning','LaTeX Warning'])]
        need(not diagnostics,'TeX diagnostics: '+str(diagnostics))
    dump(out/'build_report.json',{'status':'PASS','input_bindings':len(protocol['bindings']),'topics':13,'originals':33,'exact_primary_comparisons':72,'diagnostics':diagnostics,'rendered':render})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--public-root',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='xelatex');o=a.parse_args()
    build(o.out,o.public_root,o.render,o.xelatex)
