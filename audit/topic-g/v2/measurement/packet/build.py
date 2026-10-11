#!/usr/bin/env python3
"""Whole-topic and conditional geometry costs from independently accepted inputs."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import subprocess

PINS = {
    'inputs': 'c46e1742d44138d9a63af86ae2ee9dd9d1498d0b4ca0d75cf1fd19a022af978d',
    'input_review': '4bd02d9322aa41b6f6ea09ec68c10428b07bf079288048ef416f1d7e7f737d80',
    'input_adoption': '26fefb9a3b596a7ed8ceb0792a99afe0e39f01e3cb1483225ce04d8e69d8fbbb',
}
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
FORMS = ['NFC', 'NFKC']
RAW_KEYS = ['complete_programs', 'complete_operational_drivers', 'complete_formal_files']
PAIRS = [('L009', 'G1'), ('L092', 'G2')]


def need(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')


def bind(root, pin):
    need(digest(root/'manifest.json') == pin, 'Accepted manifest changed')
    for r in read(root/'manifest.json')['exports']:
        p = root/r['path']
        need(p.stat().st_size == r['bytes'] and digest(p) == r['sha256'], 'Changed export '+str(p))


def fraction(n, d):
    value = Fraction(n, d)
    return dict(numerator=n, denominator=d, reduced_numerator=value.numerator,
                reduced_denominator=value.denominator, decimal=format(float(value), '.12f'))


def calculate(roots):
    for k,pin in PINS.items():
        bind(roots[k],pin)
    counts=read(roots['inputs']/'author_counts.json')
    independent=read(roots['input_review']/'recount.json')
    adoption=read(roots['input_adoption']/'review.json')
    review=read(roots['input_review']/'review.json')
    policy=read(roots['inputs']/'policy.json')
    need(review['status']=='ACCEPTED_INDEPENDENT_TOPIC_G_MEASUREMENT_INPUTS_V2' and
         adoption['status']=='ROOT_ACCEPTED_TOPIC_G_INPUTS_V2_WITH_EXPLICIT_EXTRACTION_BOUNDARY', 'Inputs not accepted')
    need(counts['documents']==independent['documents'] and counts['ratios'] is None, 'Independent full PDF counts')
    need(policy['units']==UNITS and policy['variants']==VARIANTS and policy['normalizations']==FORMS, 'Fixed measurement coordinates')
    need(not policy['comparison_policy']['cross_topic_deduplication'] and policy['source_intake_closed'], 'Full common cost, closed intake')
    for k in RAW_KEYS:
        need(counts[k]==independent['raw_files'][k], 'Independent full raw counts '+k)
    need([len(counts[k]) for k in RAW_KEYS]==[13,3,6], 'Complete raw files')
    expected_roles={'required mathematical computation':4,'required witness verification':1,'required certificate bridge':1,'validation':7}
    need({role:sum(r['role']==role for r in counts['complete_programs'].values()) for role in expected_roles}==expected_roles, 'Program roles')
    rows=[];cover_rows=[]
    for variant in VARIANTS:
        for form in FORMS:
            for unit in UNITS:
                c={k:r['variants'][variant][form][unit] for k,r in counts['documents'].items()}
                raw={k:sum(r['metrics'][form][unit] for r in counts[k].values()) for k in RAW_KEYS}
                role_costs={role:sum(r['metrics'][form][unit] for r in counts['complete_programs'].values() if r['role']==role)
                            for role in expected_roles}
                need(sum(role_costs.values())==raw['complete_programs'], 'All program roles paid')
                source=c['L009']+c['L092'];written=c['U_G']+c['G1']+c['G2']
                cmp=dict(written=fraction(source,written),
                         including_printed_programs=fraction(source,written+c['CODE']),
                         including_raw_programs=fraction(source,written+raw['complete_programs']))
                conditional={s:dict(application=a,comparison=fraction(c[s],c[a])) for s,a in PAIRS}
                rows.append(dict(variant=variant,normalization=form,unit=unit,document_costs=c,raw_costs=raw,
                                 program_costs_by_role=role_costs,source_sum=source,written_denominator=written,
                                 combined=cmp,conditional=conditional,
                                 acquired_common=c['U_G'],acquired_printed_programs=c['CODE'],
                                 acquired_raw_programs_alternative=raw['complete_programs']))
                article=counts['identification_cover_sensitivity']['article_only'][variant][form][unit]
                source2=article+c['L092']
                cover_rows.append(dict(variant=variant,normalization=form,unit=unit,L009_article_only=article,
                                       source_sum=source2,written=fraction(source2,written),
                                       including_printed_programs=fraction(source2,written+c['CODE']),
                                       including_raw_programs=fraction(source2,written+raw['complete_programs']),
                                       L009_conditional=fraction(article,c['G1']),L092_conditional_unchanged=True))
    primary=next(r for r in rows if (r['variant'],r['normalization'],r['unit'])==
                 ('calibrated_selected','NFC','characters_without_whitespace'))
    return dict(status='AUTHOR_NUMERICAL_CANDIDATE_PENDING_INDEPENDENT_REVIEW',input_manifests=PINS,
                source_ids=['L009','L092'],source_records=79,principal_contracts=2,
                coordinates=rows,coordinate_count=30,exact_fraction_count=150,
                combined_fractions=90,conditional_fractions=60,primary=primary,
                cover_sensitivity=dict(primary_includes_cover=True,article_only_coordinates=cover_rows,
                                       additional_exact_fractions=120,method='Directly counted accepted article-only strings, not subtraction of token totals.',
                                       full_visible_cover_logo_cost=None),
                boundary=dict(whole_common_once_within_topic=True,whole_source_and_applications=True,
                              cross_topic_discount=False,required_finite_programs=4,witness_certificate_bridges=2,validation_programs=7,
                              complete_programs=13,program_representations='Whole printed appendix or thirteen full raw files, alternatives never both.',
                              conditional='After acquisition of whole U_G and all thirteen complete programs, including validation; roles remain distinct.',
                              operational_drivers_separate=3,Lean_files_separate=6,prior_partial_Lean_declarations=40,
                              retained_BDL_full_proof_cost=None,retained_Kantor_full_proof_cost=None,other_external_proof_cost=None,
                              historical_program_cost=None,graphics_and_formula_layout_cost=None,
                              source_qualifications='The accepted corrected principal contracts and all recorded exclusions apply. Full source length does not claim recovery of every printed auxiliary assertion.',
                              mathematical_complexity_claim=False,sawtooth_claim=False,
                              interpretation='Available complete text lengths in the fixed representation, not total research effort or minimum proof length.'),
                new_source_credit=0,new_question_credit=0,new_formal_credit=0,primary_text_fonts_images_exported=False)


def plot(result,out):
    os.environ['MPLCONFIGDIR']=str(out/'.matplotlib');os.environ['XDG_CACHE_HOME']=str(out/'.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'topic-g-complete-documents'})
    p=result['primary'];c=p['document_costs'];fig,axes=plt.subplots(1,2,figsize=(10,4.0),layout='constrained')
    left,right=axes
    left.bar(0,p['source_sum'],color='#686868',label='Both sources')
    left.bar(1,c['U_G'],color='#426b9a',label='Whole common theory')
    left.bar(1,c['G1']+c['G2'],bottom=c['U_G'],color='#70a59a',label='Both applications')
    left.set_xticks([0,1],['Sources','Our written papers']);left.set_ylabel('NFC characters without whitespace')
    top=max(p['source_sum'],p['written_denominator']);left.set_ylim(0,top*1.2)
    for x,y in [(0,p['source_sum']),(1,p['written_denominator'])]:left.text(x,y+top*.02,f'{y:,}',ha='center')
    left.legend(loc='upper center',bbox_to_anchor=(.5,-.16),frameon=False,fontsize=8);left.set_title('Whole written comparison')
    keys=['U_G','L009','G1','L092','G2','CODE'];colors=['#426b9a','#686868','#70a59a','#686868','#70a59a','#bd874e']
    bars=right.bar(range(6),[c[k] for k in keys],color=colors);right.set_xticks(range(6),['Common','L009','G1','L092','G2','Code']);right.tick_params(axis='x',labelsize=8)
    top=max(c[k] for k in keys);right.set_ylim(0,top*1.22)
    for bar,k in zip(bars,keys):right.text(bar.get_x()+bar.get_width()/2,c[k]+top*.025,f'{c[k]:,}',ha='center',fontsize=8)
    right.set_title('Complete components')
    for ax in axes:ax.spines[['right','top']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
    fig.savefig(out/'complete_costs.pdf',metadata={'CreationDate':None,'ModDate':None});fig.savefig(out/'complete_costs.svg',metadata={'Date':None});plt.close(fig)


def reader(result,out):
    p=result['primary'];c=p['document_costs'];raw=p['raw_costs'];shown=lambda f:format(float(f['decimal']),'.3f')
    cover=next(r for r in result['cover_sensitivity']['article_only_coordinates'] if
               (r['variant'],r['normalization'],r['unit'])==('calibrated_selected','NFC','characters_without_whitespace'))
    rows=[]
    labels=['Whitespace words','Alphanumeric units','Nonspace characters','Characters, collapsed spaces','UTF-8 bytes, collapsed spaces']
    for unit,label in zip(UNITS,labels):
        row=next(r for r in result['coordinates'] if r['variant']=='calibrated_selected' and r['normalization']=='NFC' and r['unit']==unit)
        rows.append(label+' & '+' & '.join(shown(f) for f in [row['combined']['written'],row['conditional']['L009']['comparison'],row['conditional']['L092']['comparison']])+r' \\')
    text=r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.85in]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Flag relations and incidence residues:\\complete manuscript costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The two fixed sources are Delaby--Leemans--Tranchida, \emph{Geometries with
trialities arising from linear spaces}, Algebraic Combinatorics 9 (2026),
379--402 (L009), and Leemans, \emph{A generalization of a construction due
to Van Nypelseer}, Beitr\"age Algebra Geom.\ 46 (2005), 561--574 (L092).
Their complete PDFs have 25 and 14 physical pages; L009 includes its
publisher identification cover. The accepted principal contracts contain
79 source records, with explicit corrections and exclusions. They do not
assert recovery of every printed auxiliary claim.

\paragraph{The common theory and the two applications.}
The primary convention counts calibrated NFC characters without whitespace.
Only exact running furniture is removed. Titles, abstracts, proofs,
references and extractable table and diagram labels remain charged.
\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Source L009 & 25 & @L009@\\
Source L092 & 14 & @L092@\\
Whole common theory $U_G$ & 12 & @U_G@\\
Triangle application G1 & 8 & @G1@\\
Steiner application G2 & 22 & @G2@\\
Whole program appendix & 20 & @CODE@\\\bottomrule
\end{tabular}\end{center}
The combined written comparison pays for the whole common theory once:
\[
 R_{\rm written}=\frac{@L009@+@L092@}{@U_G@+@G1@+@G2@}
 =\frac{@SOURCE@}{@WRITTEN@}=@RW@.
\]
After acquiring the whole common paper and all thirteen complete programs,
the two source/application comparisons are
\[
 r_1\mid(U_G,P_G)=\frac{@L009@}{@G1@}=@R1@,\qquad
 r_2\mid(U_G,P_G)=\frac{@L092@}{@G2@}=@R2@.
\]
The complete written replacement is longer than the two sources in this
measure. G1 is shorter than L009; G2 is longer than L092 even after the
common theory is acquired. Other topics pay their own common theories in
full, even where they overlap.

\paragraph{Programs, formal evidence and retained inputs.}
Four programs supply finite mathematical inputs, two verify witnesses or
bridge them to certificates, and seven validate separately proved arguments.
All thirteen are retained in full. The printed appendix gives
$@SOURCE@/(@WRITTEN@+@CODE@)=@RP@$. The thirteen raw files instead cost
@RAWCODE@, giving $@SOURCE@/@WITHRAW@=@RR@$. These are alternative costs,
never simultaneous charges. Three drivers cost @DRIVERS@ separately; six
Lean files cost @LEAN@ separately and contain forty previously checked
component declarations. They do not formalize the entire source contracts.
BDL, Kantor and other classical inputs remain attributed and their full
proof costs unknown, as do historical programs, graphics and formula layout.
\newpage
\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
The left panel compares complete written totals. The right panel displays
all common, source, application and printed-program costs separately.
These lengths do not establish a recurring sawtooth pattern or minimum
mathematical proof complexity.

\paragraph{Sensitivity.}
For calibrated selected text with NFC normalization:
\begin{center}\begin{tabular}{lrrr}\toprule
Unit & Combined written & L009/G1 & L092/G2\\\midrule
@ROWS@
\bottomrule\end{tabular}\end{center}
All five units are retained under NFC and NFKC for three extraction policies:
untrimmed raw, selected raw and calibrated selected. The thirty coordinates
supply 150 exact fractions: ninety combined and sixty conditional.
Removing only L009's identification cover gives the separately counted
article cost @ARTICLE@. This changes the combined written factor to @RCOVER@
and the L009/G1 factor to @R1COVER@; L092/G2 is unchanged. The additional
120 exact fractions retain the printed and raw program alternatives too.
The primary comparison continues to include that cover.

\paragraph{Source qualifications and extraction.}
L009 retains the determinant correction and its circle-list, polarity and
ancillary-example limits. L092 retains the corrected deleted-line and
subline cases, path convention and Figure~2 qualifications; named-geometry
identifications and the claim without partial linearity remain excluded.
The full source texts are counted with these declared principal-result
contracts, not with an assertion that every historical statement is true.

The independent input audit checked all 101 physical pages, 180 PDF metric
cells and 220 separate raw-file cells. It aligned 75,909 source characters
with actual PDF text bytes and inspected the embedded glyph evidence.
The corrected cache identifies actual font dictionaries and effective
encodings: 701 occurrences had previously been mislabeled in the audit,
but none of the metric cells changed. The 509 visible-glyph calibrations
and all raw sensitivities remain explicit. The retained parsers are
pypdf 6.13.0 and fontTools 4.63.0; extraction does not price complete visual
information. Independent numerical review is required before publication.
\end{document}
'''
    values={**c,'SOURCE':p['source_sum'],'WRITTEN':p['written_denominator'],
            'RW':shown(p['combined']['written']),'R1':shown(p['conditional']['L009']['comparison']),
            'R2':shown(p['conditional']['L092']['comparison']),'RP':shown(p['combined']['including_printed_programs']),
            'RR':shown(p['combined']['including_raw_programs']),'RAWCODE':raw['complete_programs'],
            'WITHRAW':p['written_denominator']+raw['complete_programs'],'DRIVERS':raw['complete_operational_drivers'],
            'LEAN':raw['complete_formal_files'],'ROWS':'\n'.join(rows),'ARTICLE':cover['L009_article_only'],
            'RCOVER':shown(cover['written']),'R1COVER':shown(cover['L009_conditional'])}
    for k,v in values.items():text=text.replace('@'+k+'@',str(v))
    need('@' not in text,'unfilled reader value');(out/'measurement.tex').write_text(text)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in PINS:ap.add_argument('--'+key.replace('_','-'),type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True);ap.add_argument('--xelatex',default='/opt/homebrew/bin/xelatex');a=ap.parse_args()
    need(not a.out.exists(),'fresh output');roots={k:getattr(a,k).resolve() for k in PINS};result=calculate(roots)
    a.out.mkdir(parents=True);write(a.out/'measurement.json',result);plot(result,a.out);reader(result,a.out)
    for n in [1,2]:
        r=subprocess.run([a.xelatex,'-no-shell-escape','-interaction=nonstopmode','-halt-on-error','measurement.tex'],cwd=a.out,capture_output=True,text=True,timeout=180)
        (a.out/f'render{n}.log').write_text(r.stdout+r.stderr);need(r.returncode==0,'XeLaTeX failed')
    log=(a.out/'measurement.log').read_text();bad=[s for s in log.splitlines() if 'Overfull' in s or 'Missing character:' in s or 'LaTeX Warning:' in s];need(not bad,'Render diagnostics '+repr(bad))
    from pypdf import PdfReader
    pages=[p.extract_text() or '' for p in PdfReader(a.out/'measurement.pdf').pages];need(len(pages)==2,'Two-page reader')
    replay=dict(status='PASS_AUTHOR_CALCULATION_AND_RENDER',coordinate_count=30,main_exact_fractions=150,
                additional_cover_sensitivity_fractions=120,reader_pages=len(pages),render_diagnostics=[],
                page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in pages],input_manifests=PINS,
                visual_review='Separate, not implied by rendering.')
    write(a.out/'replay.json',replay);print(json.dumps(replay))


if __name__=='__main__':main()
