#!/usr/bin/env python3
"""Consolidate admitted primary values; no source extraction or scientific replay."""
from pathlib import Path
from fractions import Fraction
from decimal import Decimal, localcontext
import argparse, copy, csv, hashlib, io, json, os, subprocess, textwrap

ROOT=Path(__file__).resolve().parent
TITLES={
 'A':'Supported kernels and finite two-groups',
 'B':'Coset geometries and symmetric group markings',
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
 'Diagonal':'Orbit and semidirect constructions',
 'Gluing':'Common point gluing and synchronized trees'}
SHORT={'Representation':'Represent.','ChiralEnumeration':'Chiral','Diagonal':'Diagonal'}

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
    p=json.loads((ROOT/'protocol.json').read_text());data={}
    for key,b in p['bindings'].items():
        raw=(ROOT/b['local']).read_bytes();need(len(raw)==b['bytes'] and sha(raw)==b['sha256'],'exact copied binding '+key)
        if b['kind']=='committed_admitted':
            need(b['commit']==p['admitted_baseline_commit'],'exact unchanged public baseline')
            if public is not None:need(subprocess.check_output(['git','show',b['commit']+':'+b['path']],cwd=public)==raw,'committed record '+key)
        else:need(b['kind'] in ['frozen_root_accepted_unpublished','frozen_distinct_root_numerical_acceptance'] and b['commit'] is None,'new accepted packet has no invented commit')
        data[key]=json.loads(raw)
    old=data['previous_admission'];need(old['status'].startswith('ROOT_ADMITTED'),'previous numerical acceptance')
    for key in ['previous_results','previous_manifest','previous_review']:
        b=p['bindings'][key];need(any(z['path']==b['path'] and z['sha256']==b['sha256'] and z['bytes']==b['bytes'] for z in old['artifacts']),'exact prior admission binding')
    for key in ['previous','Gluing']:
        b=p['bindings'][key+'_results'];need(any(z['path']=='results.json' and z['sha256']==b['sha256'] and z['bytes']==b['bytes'] for z in data[key+'_manifest']['exports']),'manifest-bound arithmetic result')
    need(data['Gluing_results']['status']=='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_ROOT_REVIEW','new numerical role boundary')
    accepted_inputs(p,data)
    return p,data

def accepted_inputs(p,data):
    need(p['status']=='AUTHOR_BOUNDARY_USING_DISTINCTLY_ACCEPTED_NUMERICAL_PACKETS','overview preparation must await acceptance')
    m=data['Gluing_root_manifest'];r=data['Gluing_root_review'];b=p['bindings']['Gluing_root_review']
    need(any(z['path']=='review.json' and z['sha256']==b['sha256'] and z['bytes']==b['bytes'] for z in m['exports']),'manifest-bound distinct acceptance')
    need(r['status']==p['numerical_acceptance_status'] and r['status'].startswith('ROOT_ACCEPTED'),'distinct root numerical acceptance')
    need(r['author_manifest_sha256']==p['bindings']['Gluing_manifest']['sha256'],'acceptance names exact numerical edition')
    need(p['public_overview_path'] is not None and p['bindings']['Gluing_results']['public_path'] is not None,'root-provided publication routing')

def new_pair(source,application,sc,ac,representation):
    return dict(source=source,application=application,source_cost=sc,application_cost=ac,source_representation=representation,conditional=ratio(sc,ac))

def gluing_topic(p):
    c=p['costs'];raw=p['raw_costs'];common=c['U1']+c['U2'];q=new_pair('L010','GL1',c['L010'],c['A1'],'complete_PDF_calibrated_selected')
    t=dict(topic='Gluing',title=TITLES['Gluing'],source_count=1,source_ids=['L010'],pairs=[q],common_theory=common,common_components={'U1_common_point':c['U1'],'U2_synchronized_trees':c['U2']},application_components={'GL1':{'complete_application':c['A1']}},source_sum=c['L010'],applications_sum=c['A1'],written_denominator=common+c['A1'],printed_program_cost=c['CODE'],raw_program_alternative=raw['programs'],representation='calibrated_selected_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_overview_publication',numeric_origin='Gluing_results/primary')
    for name,d in [('written',t['written_denominator']),('including_printed_programs',t['written_denominator']+c['CODE']),('including_raw_programs',t['written_denominator']+raw['programs'])]:
        t[name]=ratio(c['L010'],d);same_ratio(p['comparisons'][name],c['L010'],d)
    same_ratio(p['comparisons']['conditional_application'],q['source_cost'],q['application_cost'])
    t['including_optional_validation']=None
    t['conditional_prepaid']=dict(full_common=common,full_declared_printed_programs=c['CODE'],total=common+c['CODE'])
    for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
    t.update(separate_raw_inventory=raw,program_roles='Three whole validation programs; no finite premise. Three operational drivers and two partial Lean files separate.',source_admission='Distinct numerical root acceptance bound; current overview integration pending.',scientific_boundary='One L010 original and 23 accepted source dispositions; historical numerical sequence and unused preliminaries are not newly recovered.',entire_source_pages=15,entire_common_pages=[5,6],entire_application_pages=5,entire_program_pages=4)
    return t

def make(data,protocol):
    old=data['previous_results'];r=copy.deepcopy(old)
    for key in ['accessible_originals','currently_admitted_originals','accessible_pending_complete_recovery','pending_source_retrieval','candidate_result_bindings','distinct_numerical_acceptances','unmeasured']:r.pop(key,None)
    r.update(schema='programme.primary_summary.v4',status='AUTHOR_OVERVIEW_CANDIDATE_FROM_ACCEPTED_NUMERICAL_PACKETS',admitted_baseline_commit=protocol['admitted_baseline_commit'],topic_count=14,original_manuscript_count=35,currently_published_measured_originals=34,proposed_measured_originals=35,pending_numerical_acceptance=[],pending_overview_review=True,recovery_status_not_derived_from_measurement=True)
    r['topics']=copy.deepcopy(old['topics'])+[gluing_topic(data['Gluing_results']['primary'])]
    r['notes']=['All thirteen admitted topic objects and their exact costs, representations and qualifications are preserved from the committed 34-original overview.','Only Gluing is added: both complete common papers, the full application and all three whole validation programs.','Gluing has a written factor below one; its conditional factor assumes acquisition of both whole common papers and every declared program.','Thirty-five measured originals are a subset of the 161-item programme. This numerical count is not the number of scientifically recovered or accessible originals.','No pooled factor, cross-topic discount, new credit or zero valuation of unknown outside costs is introduced.']
    r['candidate_result_bindings']={'Gluing':protocol['bindings']['Gluing_results']};r['distinct_numerical_acceptances']={'Gluing':protocol['bindings']['Gluing_root_manifest']};r['old_overviews_preserved']=True
    need(r['topics'][:-1]==old['topics'],'all thirteen admitted topic rows exactly preserved')
    need(sorted(q['source']for t in r['topics']for q in t['pairs'])==sorted([q['source']for t in old['topics']for q in t['pairs']]+['L010']),'exact one added measured original')
    validate(r);return r

def validate(r):
    need(r['topic_count']==len(r['topics'])==14 and r['original_manuscript_count']==35,'fourteen topics and thirty-five original texts')
    need(not any(k in r for k in ['accessible_originals','currently_admitted_originals','accessible_pending_complete_recovery','pending_source_retrieval']),'recovery and accessibility are not derived from measured counts')
    need(r['pending_numerical_acceptance']==[] and r['pending_overview_review'] is True and r['currently_published_measured_originals']==34 and r['proposed_measured_originals']==35,'candidate does not self-admit')
    need(r['pooled_factor'] is None and not r['cross_topic_deduplication'] and not r['all_registry_manuscripts_completed'] and r['registry_manuscripts']==161,'no pooled factor or whole-corpus overclaim')
    need(all(r[k]==0 for k in ['new_source_credit','new_question_credit','new_formal_credit']),'no new mathematical credit')
    ids=[]
    for t in r['topics']:
        need(sum(t['common_components'].values())==t['common_theory'],'complete common components')
        need(sum(q['source_cost'] for q in t['pairs'])==t['source_sum'] and sum(q['application_cost'] for q in t['pairs'])==t['applications_sum'],'complete sources and applications')
        need(t['source_ids']==[q['source'] for q in t['pairs']] and t['source_count']==len(t['pairs']),'exact topic source roster')
        need(t['written_denominator']==t['common_theory']+t['applications_sum'] and t['written']==ratio(t['source_sum'],t['written_denominator']),'full written denominator')
        for name,cost in [('including_printed_programs',t['printed_program_cost']),('including_raw_programs',t['raw_program_alternative'])]:need(t[name]==(None if cost is None else ratio(t['source_sum'],t['written_denominator']+cost)),'program alternative '+name)
        if t['printed_program_cost'] is not None:need(t['conditional_prepaid']=={'full_common':t['common_theory'],'full_declared_printed_programs':t['printed_program_cost'],'total':t['common_theory']+t['printed_program_cost']},'whole printed acquisition')
        for q in t['pairs']:
            need(q['conditional']==ratio(q['source_cost'],q['application_cost']),'whole conditional application');ids.append(q['source'])
            if 'application_components' in t:need(sum(t['application_components'][q['application']].values())==q['application_cost'],'all companion paper costs')
        for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:need(t[k] is None,'unknown cost null')
    need(len(ids)==len(set(ids))==35 and r['recovery_status_not_derived_from_measurement'] is True,'all thirty-five measured rows, separate recovery status')
    gl=next(t for t in r['topics'] if t['topic']=='Gluing');need(gl['common_components']=={'U1_common_point':12299,'U2_synchronized_trees':16117} and gl['source_ids']==['L010'] and gl['program_roles'].startswith('Three whole validation'),'both complete Gluing common papers and exact source/software roles')
    d=next(t for t in r['topics'] if t['topic']=='Diagonal');b=next(t for t in r['topics'] if t['topic']=='B');e=next(t for t in r['topics'] if t['topic']=='E')
    need(d['source_ids']==['N007','N006'] and d['printed_program_cost'] is None and d['including_printed_programs'] is None and d['no_complete_printed_route'],'complete enlarged Diagonal, no invented printed route')
    need(sum(d['raw_program_components'].values())==d['raw_program_alternative'] and d['raw_program_components']['both_required_decoders']==11015 and d['raw_program_components']['nineteen_full_files']==383279,'all nineteen files and two required decoders')
    need(d['conditional_prepaid']==dict(full_common=d['common_theory'],full_declared_raw_software=d['raw_program_alternative'],total=d['common_theory']+d['raw_program_alternative'],required_external_data_already_acquired=True,external_bytes_separate=True),'Diagonal complete acquisition including data')
    need(d['external_bytes']==dict(required_representation_files=4,required_representation_bytes=21960689,listed_installed_files=16,listed_installed_bytes=2516249),'external bytes separate and complete')
    need(b['common_components']=={'whole_current_common':44905} and b['common_theory']==44905 and b['representation']=='literal_rendered_source_plus_raw_untrimmed_pdfs','whole new B common and unchanged source representations')
    need(e['raw_program_alternative'] is None and e['optional_validation_printed']==5173 and e['including_optional_validation']==ratio(e['source_sum'],e['written_denominator']+e['printed_program_cost']+5173),'unchanged E optional sensitivity')

def csv_text(r):
    ans={};f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','title','originals','representation','sources','common','applications','written','written_factor','printed_programs','printed_factor','raw_programs','raw_factor','numerical_status'])
    for t in r['topics']:w.writerow([t['topic'],t['title'],t['source_count'],t['representation'],t['source_sum'],t['common_theory'],t['applications_sum'],t['written_denominator'],t['written']['decimal'],t['printed_program_cost'],None if t['including_printed_programs'] is None else t['including_printed_programs']['decimal'],t['raw_program_alternative'],None if t['including_raw_programs'] is None else t['including_raw_programs']['decimal'],t.get('numerical_status','unchanged_admitted')])
    ans['topics.csv']=f.getvalue();f=io.StringIO(newline='');w=csv.writer(f,lineterminator='\n');w.writerow(['topic','title','source','application','source_cost','application_cost','conditional_exact','conditional_factor','full_common_prepaid','full_program_or_software_prepaid','acquisition_representation','source_representation'])
    for t in r['topics']:
        for q in t['pairs']:w.writerow([t['topic'],t['title'],q['source'],q['application'],q['source_cost'],q['application_cost'],q['conditional']['exact_fraction'],q['conditional']['decimal'],t['common_theory'],t['raw_program_alternative'] if t['topic']=='Diagonal' else t['printed_program_cost'],'whole_raw_software_and_external_data' if t['topic']=='Diagonal' else 'whole_printed_programs',q['source_representation']])
    ans['applications.csv']=f.getvalue();return ans

def plot_spec(r,kind):
    rows=[]
    if kind=='whole_topics':
        for t in r['topics']:
            segments=[{'id':'common-'+k,'cost':v,'role':'common'} for k,v in t['common_components'].items()]
            segments += [{'id':q['application']+'-'+name,'cost':cost,'role':'application'} for q in t['pairs'] for name,cost in t.get('application_components',{}).get(q['application'],{q['application']:q['application_cost']}).items()]
            rows.append({'id':t['topic'],'label':SHORT.get(t['topic'],t['topic'])+': '+t['title'],'source':t['source_sum'],'segments':segments,'factor':t['written']['decimal']})
    else:
        pairs=[(t,q) for t in r['topics'] for q in t['pairs']]
        if kind=='conditional_1':pairs=pairs[:17]
        elif kind=='conditional_2':pairs=pairs[17:]
        for t,q in pairs:rows.append({'id':t['topic']+'-'+q['source'],'label':q['source']+' / '+q['application'],'topic':t['topic'],'title':t['title'],'source':q['source_cost'],'segments':[{'id':q['application']+'-'+name,'cost':cost,'role':'application'} for name,cost in t.get('application_components',{}).get(q['application'],{q['application']:q['application_cost']}).items()],'factor':q['conditional']['decimal']})
    return {'kind':kind,'rows':rows,'unit':'NFC characters without whitespace','bar_scale':'one common linear scale per chart; identical for source and replacement','candidate_scope':'All 35 originals; all numerical inputs accepted, consolidated overview awaits separate review'}

def draw(spec,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'overview35-fixed','pdf.fonttype':42})
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
    meta={'Creator':'Human Compression numerical candidate overview','CreationDate':None,'ModDate':None}
    fig.savefig(out/(spec['kind']+'.pdf'),metadata=meta);fig.savefig(out/(spec['kind']+'.svg'),metadata={'Date':None});plt.close(fig)

def tex(r):
    n=lambda x:'--' if x is None else f'{x:,}';f=lambda q:'--' if q is None else f"{float(q['decimal']):.3f}";short=lambda t:SHORT.get(t,t)
    s=r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,array,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\setlength{\parindent}{0pt}\setlength{\parskip}{5pt}
\newcommand{\tabsetup}{\small\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.10}}
\begin{document}
\begin{center}\Large\textbf{Complete papers and shared theories}\\[4pt]
\normalsize Fourteen topics, thirty-five original texts\end{center}
This candidate preserves all thirteen topic rows from the admitted thirty-four-original overview and adds the Gluing topic, L010. The new numerical packet has distinct frozen root acceptance; this consolidation still awaits separate review. Its exact result and review hashes are bound directly. The unchanged baseline is committed \texttt{acad9c3}; no future commit is invented. Earlier overviews remain preserved.

For each topic, $S=\sum_i c(L_i)$ counts its complete original texts, $U$ every complete common paper, and $A=\sum_i c(A_i)$ every complete application. The comparisons are
\[
 R=\frac{S}{U+A},\qquad r_i=\frac{c(L_i)}{c(A_i)}
 \quad\text{after acquiring the whole theory and declared software/data.}
\]
Each topic pays its common theory independently, even when proofs overlap another topic. A factor above one means a shorter replacement in that coordinate; a factor below one means a longer one. Conditional factors do not include acquisition a second time, and are not standalone application savings.

\textbf{Complete written costs.} All rows use NFC characters without whitespace at their stated representations. Full-document boundaries include introductions, context, proofs and references.
\begin{center}\tabsetup\begin{tabular}{lrrrrrr}\toprule
Topic & Originals & Sources & Common & Applications & Written & Factor\\\midrule
"""
    for t in r['topics']:s+=' & '.join([short(t['topic']),str(t['source_count']),n(t['source_sum']),n(t['common_theory']),n(t['applications_sum']),n(t['written_denominator']),f(t['written'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
\textbf{Representations remain distinct.} B and C use complete authored-text renderings for N001 and L108, with raw untrimmed PDFs for their other documents. Those originals' unavailable-PDF costs remain unknown. Other rows use their accepted selected, calibrated PDF coordinate. Diagonal's encoded-event graphical proxies retain raw and text-only sensitivities. No pooled factor is formed.

\textbf{Scope.} These are 35 measured originals in 14 topics within the 161-item programme. This is not the number of recovered or accessible originals, nor completion of the programme. Recovery and retrieval progress are reported separately. All corrections, retained premises and ancillary exclusions remain. Gluing's written factor is below one: its complete replacement is longer in this coordinate. No scientific, source, question or formal credit changes.
\newpage
\textbf{Complete common theories and applications.}
Dark bars are whole original sums. Blue segments are whole common papers; green segments are all complete applications. Unified B pays its entire current common paper once. C still pays its complete additional incidence note. The N006 application is displayed as all three companion-paper segments.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
Diagonal retains both N007 and N006 and all three companion papers. Gluing adds both complete common papers and the full application; its 0.677 written factor is not replaced by its 2.342 conditional factor. Text length is not minimum proof complexity or originality.
\newpage
\textbf{Complete programs and prior acquisition.}
The written comparison remains first. These separate alternatives add the entire declared program representation to the written denominator. Raw and printed forms are never added together.
\begin{center}\tabsetup\begin{tabular}{lrrrrr}\toprule
Topic & Printed code & With printed & Raw software & With raw & $U+$programs\\\midrule
"""
    for t in r['topics']:s+=' & '.join([short(t['topic']),n(t['printed_program_cost']),f(t['including_printed_programs']),n(t['raw_program_alternative']),f(t['including_raw_programs']),n(t['conditional_prepaid']['total'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
The final column uses the complete printed form when available. For Diagonal it uses all nineteen raw program/witness files plus both required decoding drivers. Its complete printed route is unavailable: the old two-page appendix covers only one validation file. Diagonal conditionals also assume acquisition of all required external data, separately inventoried as 21,960,689 representation bytes and 2,516,249 listed installed bytes. Byte storage is not added to character units. Large witnesses are not discounted.

E retains its separate optional-validation sensitivity: another 5,173 characters gives a program-inclusive factor of 1.372. No unadmitted raw-code alternative is invented for E.

\textbf{Roles.} A includes five full files. B includes a finite premise, two validations and an auxiliary example. C includes its three complete GAP files, counting the identical shared construction once within C and retaining its exhaustive census. D includes five required and three diagnostic programs. E separates its required program from optional validation. F's three programs and Representation's two are validations. G retains four finite computations, two certificate bridges and seven validations. Affine retains six mathematical programs; Chamber one required and one diagnostic program; Matching its census; Chiral enumeration all three files. Diagonal includes sixteen finite proof/witness files, three validations and both required decoders. Gluing pays all three complete validation programs, with three drivers and two partial Lean files separate. Other operational drivers and partial Lean inventories stay separate.

\textbf{Limits.} Complete external proofs, unprovided historical software, full graphics and end-to-end formalization have unknown costs, not zero. Every topic retains its underlying multi-unit and source-cover sensitivities. B's source costs are unchanged from the prior edition. This table does not compare a theorem closure with a complete original or use a node-count ratio.
\newpage
\textbf{Every complete application after full acquisition.}
All common papers and all declared software/data have already been acquired. The whole application is charged, including local context and references. DG2 includes every N006 companion paper.
\begin{center}\tabsetup\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Source cost & Application cost & Conditional\\\midrule
"""
    for t in r['topics']:
        for q in t['pairs']:s+=' & '.join([short(t['topic']),q['source'],q['application'],n(q['source_cost']),n(q['application_cost']),f(q['conditional'])])+r' \\'+'\n'
    s+=r"""\bottomrule\end{tabular}\end{center}
Gluing uses its exact newly accepted numerical packet. All thirteen previous topic rows remain unchanged from the committed admitted overview. This consolidation does not equate 35 measured originals with all recoveries or add scientific credit.
\newpage
\textbf{Individual source and application costs: first seventeen originals.}
Dark bars show complete original texts; green bars show complete applications. Factors at right assume full prior acquisition. The source and replacement bars share the same scale within each chart.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
Source IDs are stable catalogue cross-references. Descriptive topic titles, exact editions and current source-contract qualifications remain in the bound records; they are not new claims of this overview.
\newpage
\textbf{Individual source and application costs: remaining eighteen originals.}
The same conventions apply. The N006 bar retains all three companion papers. The final L010 bar is the complete Gluing application, conditional on both entire common papers and all declared diagnostic programs.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\textbf{Data and provenance.} Exact integers and rational comparisons are in \texttt{results.json}, \texttt{topics.csv} and \texttt{applications.csv}. The protocol pins committed unchanged numerical/admission records and the new Gluing numerical packet and its distinct acceptance record directly. No primary text is copied or extracted. Bar segments use complete document costs, not theorem counts. Distinct review is required before this overview becomes the public current edition.
\end{document}
"""
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
    dump(out/'build_report.json',{'status':'PASS','input_bindings':len(protocol['bindings']),'topics':14,'originals':35,'exact_primary_comparisons':76,'diagnostics':diagnostics,'rendered':render})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--public-root',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='xelatex');o=a.parse_args()
    build(o.out,o.public_root,o.render,o.xelatex)
