#!/usr/bin/env python3
"""Calculate the fixed Topic F comparisons from accepted complete input counts."""
import argparse
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import subprocess

PINS = {
    'inputs': '0dfc2fce16d8c532a1cdd9b8f61c1d9391c15099091e795cbba56bde30501620',
    'input_review': '91ac8430736283e6719bcb3cb4e1245cb2576a38608283b4fd207c1009a0247b',
    'input_adoption': 'f5a71b94d9fe202cd6dfdff92c7ec7002cf490092a31d3d78080e390d2e3053d',
}
UNITS = ['whitespace_tokens', 'alphanumeric_units', 'characters_without_whitespace',
         'characters_with_collapsed_whitespace', 'utf8_bytes_with_collapsed_whitespace']
VARIANTS = ['raw_untrimmed', 'raw_selected', 'calibrated_selected']
NORMALIZATIONS = ['NFC', 'NFKC']


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path):
    return json.loads(path.read_text())


def bind_packet(root, pin):
    need(digest(root/'manifest.json') == pin, 'wrong input manifest')
    manifest = load(root/'manifest.json')
    for row in manifest['exports']:
        path = root/row['path']
        need(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
             'changed accepted input: '+str(path))


def fraction(numerator, denominator):
    value = Fraction(numerator, denominator)
    return {'numerator': numerator, 'denominator': denominator,
            'reduced_numerator': value.numerator, 'reduced_denominator': value.denominator,
            'decimal': format(float(value), '.12f')}


def calculate(roots):
    for key, pin in PINS.items():
        bind_packet(roots[key], pin)
    counts = load(roots['inputs']/'author_counts.json')
    independent = load(roots['input_review']/'recount.json')
    review = load(roots['input_review']/'review.json')
    adoption = load(roots['input_adoption']/'review.json')
    policy = load(roots['inputs']/'policy.json')
    need(review['status'] == 'ACCEPTED_INPUT_BOUNDARY_NO_FACTORS' and
         adoption['status'] == 'ROOT_ACCEPTED_TOPIC_F_INPUTS_WITH_EXPLICIT_EXTRACTION_BOUNDARY',
         'input boundary has not been accepted')
    need(counts['documents'] == independent['documents'] and counts['ratios'] is None,
         'independent PDF input agreement')
    need(policy['units'] == UNITS and policy['variants'] == VARIANTS and
         policy['normalizations'] == NORMALIZATIONS, 'measurement coordinates changed')
    raw_keys = ['complete_validation_programs', 'complete_operational_drivers', 'complete_formal_files']
    for key in raw_keys:
        need(counts[key] == independent['raw_files'][key], 'independent raw input agreement')
    need([len(counts[k]) for k in raw_keys] == [3, 2, 1], 'whole raw file inventory')
    need(not policy['comparison_policy']['cross_topic_deduplication'] and
         all(r['uniform_written_proof_premise'] is False for r in policy['program_roster']),
         'validation role or common cost changed')
    rows = []
    for variant in VARIANTS:
        for normalization in NORMALIZATIONS:
            for unit in UNITS:
                costs = {key: value['variants'][variant][normalization][unit]
                         for key, value in counts['documents'].items()}
                raw = {key: sum(v['metrics'][normalization][unit] for v in counts[key].values())
                       for key in raw_keys}
                source, common, application, printed = [costs[k] for k in ['L014', 'U_F', 'F1', 'CODE']]
                written = common+application
                rows.append({'variant': variant, 'normalization': normalization, 'unit': unit,
                             'costs': costs, 'raw_costs': raw,
                             'comparisons': {
                                 'written': fraction(source, written),
                                 'including_printed_validation': fraction(source, written+printed),
                                 'including_raw_validation': fraction(source, written+raw['complete_validation_programs']),
                                 'conditional_application': fraction(source, application)},
                             'acquired_common': common,
                             'acquired_printed_validation': printed,
                             'acquired_raw_validation_alternative': raw['complete_validation_programs']})
    primary = next(r for r in rows if (r['variant'], r['normalization'], r['unit']) ==
                   ('calibrated_selected', 'NFC', 'characters_without_whitespace'))
    return {
        'status': 'AUTHOR_NUMERICAL_CANDIDATE_PENDING_INDEPENDENT_REVIEW',
        'input_manifests': PINS, 'source_ids': ['L014'], 'source_records': 25,
        'documents': ['L014', 'U_F', 'F1', 'CODE'], 'physical_pages': [12, 4, 5, 4],
        'coordinates': rows, 'coordinate_count': 30, 'exact_fraction_count': 120,
        'combined_fractions': 90, 'conditional_fractions': 30, 'primary': primary,
        'boundary': {
            'whole_source_and_applications': True, 'whole_common_once': True,
            'cross_topic_discount': False, 'required_uniform_proof_programs': 0,
            'complete_validation_programs': 3,
            'program_representations': 'Whole printed appendix or three complete raw files; alternatives, never both.',
            'conditional': 'After acquiring the whole common paper and complete declared validation package; validation is not a mathematical premise.',
            'separate_operational_drivers': 2, 'separate_Lean_files': 1, 'scoped_Lean_declarations': 5,
            'retained_CP_fulltext_cost': None, 'retained_external_cost': None,
            'source_graphics_layout_cost': None, 'historical_program_cost': None,
            'source_contract_qualification': 'Declared corrected principal results; not recovery of every printed auxiliary assertion.',
            'mathematical_complexity_claim': False, 'sawtooth_claim': False,
            'interpretation': 'Available complete text lengths in the fixed representation; not total effort or minimum proof complexity.'},
        'new_source_credit': 0, 'new_question_credit': 0, 'new_formal_credit': 0,
        'primary_material_exported': False}


def figure(result, out):
    os.environ['MPLCONFIGDIR'] = str(out/'.matplotlib')
    os.environ['XDG_CACHE_HOME'] = str(out/'.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    primary = result['primary']
    c = primary['costs']
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10,
                         'svg.hashsalt': 'topic-f-complete-documents'})
    fig, axes = plt.subplots(1, 2, figsize=(10.1, 4.2), layout='constrained')
    ax = axes[0]
    ax.bar(0, c['L014'], color='#666666', label='Complete source')
    ax.bar(1, c['U_F'], color='#426b9a', label='Whole common theory')
    ax.bar(1, c['F1'], bottom=c['U_F'], color='#70a59a', label='Complete application')
    ax.set_xticks([0, 1], ['L014', 'Our written papers'])
    ax.set_ylabel('NFC characters without whitespace')
    ax.set_ylim(0, max(c['L014'], c['U_F']+c['F1'])*1.15)
    for x, value in [(0, c['L014']), (1, c['U_F']+c['F1'])]:
        ax.text(x, value+450, f'{value:,}', ha='center')
    ax.set_title('Whole written comparison')
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.17), frameon=False, fontsize=8)
    ax = axes[1]
    values = [c['U_F'], c['F1'], c['CODE']]
    bars = ax.bar([0, 1, 2], values, color=['#426b9a', '#70a59a', '#bd874e'])
    ax.set_xticks([0, 1, 2], ['Common theory', 'Application', 'Validation appendix'])
    ax.tick_params(axis='x', labelsize=8)
    ax.set_ylim(0, max(values)*1.18)
    for bar, value in zip(bars, values):
        ax.text(bar.get_x()+bar.get_width()/2, value+220, f'{value:,}', ha='center')
    ax.set_title('Complete components, priced separately')
    for ax in axes:
        ax.spines[['right', 'top']].set_visible(False)
        ax.grid(axis='y', alpha=0.2)
        ax.set_axisbelow(True)
    fig.savefig(out/'complete_costs.pdf', metadata={'CreationDate': None, 'ModDate': None})
    fig.savefig(out/'complete_costs.svg', metadata={'Date': None})
    plt.close(fig)


def reader(result, out):
    p = result['primary']; c = p['costs']; raw = p['raw_costs']; ratios = p['comparisons']
    shown = lambda name: format(float(ratios[name]['decimal']), '.3f')
    source, common, app, code = [c[k] for k in ['L014', 'U_F', 'F1', 'CODE']]
    metric_rows = []
    labels = ['Whitespace words', 'Alphanumeric units', 'Nonspace characters',
              'Characters, collapsed spaces', 'UTF-8 bytes, collapsed spaces']
    for unit, label in zip(UNITS, labels):
        row = next(r for r in result['coordinates'] if r['variant']=='calibrated_selected' and
                   r['normalization']=='NFC' and r['unit']==unit)
        v = row['comparisons']
        metric_rows.append(label+' & '+' & '.join(format(float(v[k]['decimal']), '.3f') for k in
                           ['written', 'including_printed_validation', 'conditional_application'])+r' \\')
    text = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=0.9in]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}
\title{Odd kernels and cyclotomic polyhedra:\\complete manuscript costs}
\author{Human Compression project}\date{}
\begin{document}\maketitle
The fixed source is Hou--Feng--Leemans--Qu, \emph{String C-groups of order
$4p^m$}, arXiv:2407.10388v1, 15 July 2024. Its twelve pages are compared with
our complete four-page common theory and five-page application. The declared
corrected principal contract has 25 source records; it excludes the
introductory numerical census and general Hughes classification. Full source
length does not mean that every printed auxiliary assertion was recovered.

\paragraph{The whole topic and the conditional application.}
The primary coordinate counts NFC characters without whitespace after the
accepted visible-glyph calibration and removal of exact running furniture.
Titles, abstracts, proofs, tables' extractable text, references and contacts
remain counted. The entire common paper is paid once within this topic.
\[
 R_{\rm written}=\frac{@SOURCE@}{@COMMON@+@APP@}
 =\frac{@SOURCE@}{@WRITTEN@}=@RW@,\qquad
 r\mid(U_F,V_F)=\frac{@SOURCE@}{@APP@}=@RC@.
\]
The conditional figure assumes acquisition of the whole common paper and
the declared complete validation package $V_F$. Its programs check the
uniform written proofs; none supplies a finite premise of those proofs.
Overlap with other topics gives no discount on the common paper.

\begin{center}\begin{tabular}{lrr}\toprule
Complete document & Pages & Characters\\\midrule
Source L014 & 12 & @SOURCE@\\
Common theory $U_F$ & 4 & @COMMON@\\
Application F1 & 5 & @APP@\\
Validation appendix & 4 & @CODE@\\\bottomrule
\end{tabular}\end{center}

\paragraph{The complete validation cost.}
The four-page appendix prints all three programs, including comments and
printed continuation marks. It gives the separate comparison
\[
 R_{\rm validation}=\frac{@SOURCE@}{@WRITTEN@+@CODE@}
 =\frac{@SOURCE@}{@WITHCODE@}=@RV@.
\]
Using the three complete raw files instead costs @RAWCODE@ characters,
giving $@SOURCE@/@WITHRAW@=@RR@$. The appendix and raw files are alternative
representations; they are never charged together. The two operational
drivers cost @DRIVERS@ characters separately. The reused Lean file costs
@LEAN@ separately and proves five scoped declarations, not the entire
source contract. No fresh mathematical or formal result is asserted here.

\paragraph{Retained inputs and unknown costs.}
The tightness converse retains Cunningham--Pellicer's classification, with
its exact odd/even hypotheses and uniqueness conclusion. Its full proof
cost, other external proof costs, historical software and source graphics
remain unknown. The 43 one-pixel source images and two-dimensional formula
layout are inventoried but not priced by extracted-text metrics. These are
comparisons of available texts, not total research effort or minimum proof
complexity.\newpage

\begin{center}\includegraphics[width=\textwidth]{complete_costs.pdf}\end{center}
The left panel compares the whole source with both complete written papers.
The right panel exposes each complete cost, including validation. There is
only one application in this topic; these bars establish no recurring
sawtooth pattern. A later dependency graph may locate reuse within the
proofs without changing this full-document accounting.

\paragraph{Sensitivity to the unit of length.}
For calibrated selected text with NFC normalization, the three displayed
comparisons are as follows. Different units answer different questions;
the primary nonspace-character convention was fixed before these factors
were evaluated.
\begin{center}\begin{tabular}{lrrr}\toprule
Unit & Whole written & With validation & Conditional\\\midrule
@METRICROWS@
\bottomrule\end{tabular}\end{center}

The machine-readable calculation retains all five units under NFC and
NFKC, for untrimmed raw extraction, selected raw extraction and calibrated
selected extraction: thirty coordinates and 120 exact fractions. Whole raw
programs, drivers and formal files retain their separate input counts.
Rounded figures here are readers for the exact integer fractions, not
substitutes for them.

\paragraph{Extraction and verification.}
The accepted input audit independently recounted all 120 PDF and 60 raw-file
metric cells. It inspected all 25 physical pages and aligned all 25,574
nonspace source characters with their original PDF text bytes. Ninety-five
occurrences repair visible glyph identity: sixteen mathematical alphabet
glyphs, 78 pieces of tall square brackets and one normality sign. These
repairs neither fix the source's mathematical marking nor rearrange formulas.
Raw extraction remains available as a sensitivity. The pinned parsers are
pypdf 6.13.0 and fontTools 4.63.0; their implementation and Unicode semantics
are declared computational dependencies.

The numerical builder reads the accepted input records, checks their frozen
manifests and independently reviewed counts, and forms the displayed complete
denominators. The original input policy and mathematical admissions remain
unchanged. Independent numerical review is required before publication.
\end{document}
'''
    replacements = {'SOURCE': source, 'COMMON': common, 'APP': app, 'CODE': code,
                    'WRITTEN': common+app, 'WITHCODE': common+app+code,
                    'RAWCODE': raw['complete_validation_programs'],
                    'WITHRAW': common+app+raw['complete_validation_programs'],
                    'DRIVERS': raw['complete_operational_drivers'], 'LEAN': raw['complete_formal_files'],
                    'RW': shown('written'), 'RC': shown('conditional_application'),
                    'RV': shown('including_printed_validation'), 'RR': shown('including_raw_validation'),
                    'METRICROWS': '\n'.join(metric_rows)}
    for key, value in replacements.items():
        text = text.replace('@'+key+'@', str(value))
    need('@' not in text, 'unfilled reader value')
    (out/'measurement.tex').write_text(text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in PINS:
        parser.add_argument('--'+key.replace('_', '-'), type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--xelatex', default='/opt/homebrew/bin/xelatex')
    args = parser.parse_args()
    need(not args.out.exists(), 'fresh output directory required')
    roots = {key: getattr(args, key).resolve() for key in PINS}
    result = calculate(roots)
    args.out.mkdir(parents=True)
    (args.out/'measurement.json').write_text(json.dumps(result, indent=2)+'\n')
    figure(result, args.out)
    reader(result, args.out)
    for turn in [1, 2]:
        proc = subprocess.run([args.xelatex, '-no-shell-escape', '-interaction=nonstopmode',
                               '-halt-on-error', 'measurement.tex'], cwd=args.out,
                              capture_output=True, text=True, timeout=180)
        (args.out/f'render{turn}.log').write_text(proc.stdout+proc.stderr)
        need(proc.returncode == 0, 'reader compilation failed')
    log = (args.out/'measurement.log').read_text()
    need(not any(s in log for s in ['Overfull', 'Missing character:', 'LaTeX Warning:']),
         'reader rendering diagnostic')
    from pypdf import PdfReader
    pages = [p.extract_text() or '' for p in PdfReader(args.out/'measurement.pdf').pages]
    need(len(pages) == 2, 'reader should occupy two pages')
    report = {'status': 'PASS_AUTHOR_CALCULATION_AND_RENDER', 'coordinates': 30,
              'exact_fractions': 120, 'reader_pages': len(pages), 'diagnostics': [],
              'reader_text_sha256': hashlib.sha256('\n'.join(pages).encode()).hexdigest(),
              'input_manifests': PINS, 'visual_review': 'Separate; not inferred from this build.'}
    (args.out/'replay.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
