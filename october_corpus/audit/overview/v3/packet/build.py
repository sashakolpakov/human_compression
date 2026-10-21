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
 'Diagonal':'Orbit and semidirect constructions'}
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
    for key in ['previous','B','Diagonal']:
        b=p['bindings'][key+'_results'];need(any(z['path']=='results.json' and z['sha256']==b['sha256'] and z['bytes']==b['bytes'] for z in data[key+'_manifest']['exports']),'manifest-bound arithmetic result')
    for key in ['B','Diagonal']:need(data[key+'_results']['status']=='AUTHOR_NUMERICAL_CANDIDATE_PENDING_DISTINCT_REVIEW','new numerical role boundary')
    accepted_inputs(p,data)
    return p,data

def accepted_inputs(p,data):
    for key,status in [('B','ROOT_ACCEPTED_COMPLETE_UNIFIED_B_NUMBERS'),('Diagonal','ROOT_ACCEPTED_COMPLETE_DIAGONAL_V2_NUMBERS')]:
        m=data[key+'_root_manifest'];r=data[key+'_root_review'];b=p['bindings'][key+'_root_review']
        need(m['status']=='FROZEN_ROOT_NUMERICAL_ACCEPTANCE','frozen distinct root review')
        need(any(z['path']=='review.json' and z['sha256']==b['sha256'] and z['bytes']==b['bytes'] for z in m['exports']),'manifest-bound distinct acceptance')
        need(r['status']==status and r['author_manifest_sha256']==p['bindings'][key+'_manifest']['sha256'],'acceptance names exact numerical edition')

def new_pair(source,application,sc,ac,representation):
    return dict(source=source,application=application,source_cost=sc,application_cost=ac,source_representation=representation,conditional=ratio(sc,ac))

def replacement(topic,p):
    if topic=='B':
        pairs=[new_pair(k,'B'+str(i+1),p['source_costs'][k],p['applications'][k],p['source_representations'][k]) for i,k in enumerate(['N001','N003','N008','L030','L040'])]
        printed=p['printed_program_cost'];raw=p['raw_program_cost'];expected=p['whole'];parts={q['application']:{q['application']:q['application_cost']} for q in pairs}
    else:
        pairs=[new_pair(k,'DG'+str(i+1),p['original_costs'][k],p['application_costs'][k],'complete_PDF_calibrated_selected_encoded_event_proxies') for i,k in enumerate(['N007','N006'])]
        printed=None;raw=p['whole_software_cost'];expected={'written':p['whole']['written'],'including_raw_programs':p['whole']['including_whole_raw_software']};parts={'DG1':{'N007_complete':p['document_costs']['A1']},'DG2':{k:p['document_costs'][k] for k in ['A2','A2nine','A2HN']}}
    t=dict(topic=topic,title=TITLES[topic],source_count=len(pairs),source_ids=[q['source'] for q in pairs],pairs=pairs,common_theory=p['common_theory'],common_components={'whole_current_common':p['common_theory']},application_components=parts,source_sum=sum(q['source_cost'] for q in pairs),applications_sum=sum(q['application_cost'] for q in pairs),printed_program_cost=printed,raw_program_alternative=raw,representation='literal_rendered_source_plus_raw_untrimmed_pdfs' if topic=='B' else 'calibrated_selected_pdf',normalization='NFC',unit='characters_without_whitespace',numerical_status='distinctly_root_accepted_pending_publication',numeric_origin=topic+'_results/primary')
    t['written_denominator']=t['common_theory']+t['applications_sum'];t['written']=ratio(t['source_sum'],t['written_denominator']);t['including_printed_programs']=None if printed is None else ratio(t['source_sum'],t['written_denominator']+printed);t['including_raw_programs']=ratio(t['source_sum'],t['written_denominator']+raw);t['including_optional_validation']=None
    t['conditional_prepaid']=dict(full_common=t['common_theory'],full_declared_printed_programs=printed,total=t['common_theory']+printed) if printed is not None else dict(full_common=t['common_theory'],full_declared_raw_software=raw,total=t['common_theory']+raw,required_external_data_already_acquired=True,external_bytes_separate=True)
    for name,f in expected.items():same_ratio(f,t[name]['numerator'],t[name]['denominator'])
    for q in pairs:same_ratio(p['conditional'][q['source']],q['source_cost'],q['application_cost'])
    for k in ['external_proof_cost','historical_software_cost','complete_graphic_cost','full_formalization_cost']:t[k]=None
    t['separate_raw_inventory']=p['raw_file_costs'];t['source_admission']='distinct numerical root acceptance bound; public integration pending'
    if topic=='B':t.update(program_roles='Four whole programs: one finite premise, two validations, one auxiliary example. Two operational drivers and two partial Lean files separate.',cover_sensitivity_retained=True)
    else:t.update(program_roles='Nineteen whole files: sixteen finite proof/witness files and three validations, plus both complete required decoding drivers. Four other drivers and three partial Lean files separate.',raw_program_components={'nineteen_full_files':p['whole_program_cost'],'both_required_decoders':p['required_decoder_cost']},old_single_validation_printed_alternative=p['old_single_printed_validation_cost'],no_complete_printed_route=True,external_bytes={'required_representation_files':4,'required_representation_bytes':21960689,'listed_installed_files':16,'listed_installed_bytes':2516249},graphic_proxy_sensitivities_required=True)
    return t

def make(data,protocol):
    old=data['previous_results'];r=copy.deepcopy(old)
    r.update(schema='programme.primary_summary.v3',status='AUTHOR_OVERVIEW_CANDIDATE_FROM_ACCEPTED_NUMERICAL_PACKETS',admitted_baseline_commit=protocol['admitted_baseline_commit'],original_manuscript_count=34,currently_published_measured_originals=33,proposed_measured_originals=34,pending_numerical_acceptance=[],pending_overview_review=True,unmeasured=[],pending_source_retrieval=57,accessible_pending_complete_recovery=70)
    r.pop('measurement_baseline_commit',None);r.pop('scope_update_commit',None)
    r['topics']=[replacement(t['topic'],data[t['topic']+'_results']['primary']) if t['topic'] in ['B','Diagonal'] else copy.deepcopy(t) for t in old['topics']]
    r['notes']=['Complete-topic and conditional figures are separate. Every topic pays its entire common theory independently.','B uses the entire new unified U and all five applications. Its original source costs and representations are unchanged.','Diagonal now includes N007 and N006, the entire current U and all three N006 companions. Raw software includes all nineteen files and both required decoding drivers. Its complete printed alternative is null.','B and enlarged Diagonal values have distinct frozen root numerical acceptance; the other eleven topic rows are unchanged from the committed admitted overview. This consolidation still requires separate review.','The 34 original texts are a subset of the 161-item programme. Scientific corrections, retained inputs and exclusions remain in each source contract.','No pooled factor, cross-topic discount, new credit or zero valuation of unknown outside costs is introduced.']
    r['candidate_result_bindings']={k:protocol['bindings'][k+'_results'] for k in ['B','Diagonal']};r['old_overviews_preserved']=True;r['distinct_numerical_acceptances']={k:protocol['bindings'][k+'_root_manifest'] for k in ['B','Diagonal']}
    need(sorted(q['source'] for t in r['topics'] for q in t['pairs'])==sorted([q['source'] for t in old['topics'] for q in t['pairs']]+['N006']),'exact one added numerical original')
    for before,after in zip(old['topics'],r['topics']):
        if before['topic'] not in ['B','Diagonal']:need(before==after,'unchanged admitted topic '+before['topic'])
    validate(r);return r

def validate(r):
    need(r['topic_count']==len(r['topics'])==13 and r['original_manuscript_count']==34,'thirteen topics and thirty-four original texts')
    need(r['pending_numerical_acceptance']==[] and r['pending_overview_review'] is True and r['currently_published_measured_originals']==33 and r['proposed_measured_originals']==34,'candidate does not self-admit')
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
    need(len(ids)==len(set(ids))==34 and r['unmeasured']==[],'all thirty-four candidate rows, no stale unmeasured N006 row')
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
    return {'kind':kind,'rows':rows,'unit':'NFC characters without whitespace','bar_scale':'one common linear scale per chart; identical for source and replacement','candidate_scope':'All 34 originals; all numerical inputs accepted, consolidated overview awaits separate review'}

def draw(spec,out):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'overview34-fixed','pdf.fonttype':42})
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
\normalsize Thirteen topics, thirty-four original texts\end{center}
This candidate overview combines eleven unchanged admitted topic rows with the new unified B edition and the enlarged N007--N006 orbit-construction edition. Both new numerical packets have distinct frozen root acceptance; this consolidated overview still awaits its separate review. Their exact result hashes are bound directly; no future public commit is invented. The unchanged baseline is committed \texttt{ea98753}; both earlier overviews remain preserved.

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

\textbf{Scope.} This is a proposed numerical account of 34 original texts within the 161-item programme, not completion of that programme. The committed scientific snapshot has 34 recoveries among 104 accessible originals, with 70 awaiting complete recovery and 57 retrieval targets. All corrections, retained premises and ancillary exclusions remain. No scientific, source, question or formal credit changes.
\newpage
\textbf{Complete common theories and applications.}
Dark bars are whole original sums. Blue segments are whole common papers; green segments are all complete applications. Unified B pays its entire current common paper once. C still pays its complete additional incidence note. The N006 application is displayed as all three companion-paper segments.
\begin{center}\includegraphics[width=\linewidth]{whole_topics.pdf}\end{center}
The enlarged Diagonal row now contains both N007 and N006 and the whole current eight-page theory. It uses the new frozen two-original measurement; no factor or common cost is borrowed from the old N007-only edition. Text length is not a minimum proof complexity or a measure of originality.
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

\textbf{Roles.} A includes five full files. B includes a finite premise, two validations and an auxiliary example. C includes its three complete GAP files, counting the identical shared construction once within C and retaining its exhaustive census. D includes five required and three diagnostic programs. E separates its required program from optional validation. F's three programs and Representation's two are validations. G retains four finite computations, two certificate bridges and seven validations. Affine retains six mathematical programs; Chamber one required and one diagnostic program; Matching its census; Chiral enumeration all three files. Diagonal includes sixteen finite proof/witness files, three validations and both required decoders. Other operational drivers and partial Lean inventories stay separate.

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
The B and Diagonal rows use their exact newly accepted numerical packets. Other rows remain unchanged from the committed admitted overview. This consolidation adds no scientific or numerical admission.
\newpage
\textbf{Individual source and application costs: first seventeen originals.}
Dark bars show complete original texts; green bars show complete applications. Factors at right assume full prior acquisition. The source and replacement bars share the same scale within each chart.
\begin{center}\includegraphics[width=\linewidth]{conditional_1.pdf}\end{center}
Source IDs are stable catalogue cross-references. Descriptive topic titles, exact editions and current source-contract qualifications remain in the bound records; they are not new claims of this overview.
\newpage
\textbf{Individual source and application costs: remaining seventeen originals.}
The same conventions apply. The final N006 bar includes its general application, nine-case certificate paper and Harada--Norton companion, with all references retained.
\begin{center}\includegraphics[width=\linewidth]{conditional_2.pdf}\end{center}
\textbf{Data and provenance.} Exact integers and rational comparisons are in \texttt{results.json}, \texttt{topics.csv} and \texttt{applications.csv}. The protocol pins committed unchanged numerical/admission records and the two new numerical packets and their distinct acceptance records directly. No primary text is copied or extracted. Bar segments use complete document costs, not theorem counts. Distinct review is required before this overview becomes the public current edition.
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
    dump(out/'build_report.json',{'status':'PASS','input_bindings':len(protocol['bindings']),'topics':13,'originals':34,'exact_primary_comparisons':72,'diagnostics':diagnostics,'rendered':render})

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,required=True);a.add_argument('--public-root',type=Path);a.add_argument('--render',action='store_true');a.add_argument('--xelatex',default='xelatex');o=a.parse_args()
    build(o.out,o.public_root,o.render,o.xelatex)
