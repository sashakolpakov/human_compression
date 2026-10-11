#!/usr/bin/env python3
"""Complete-topic comparisons, with all conditional applications separately shown."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess
from compute import need

COLORS = {'source': '#626c76', 'common': '#426b9a',
          'application': '#70a59a', 'program': '#bd874e'}


def plot(result, out):
    os.environ['MPLCONFIGDIR'] = str(out / '.mpl')
    os.environ['XDG_CACHE_HOME'] = str(out / '.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'AC-whole-topic-additions-v1'})
    fig, axes = plt.subplots(1, 2, figsize=(8.0, 3.3), layout='constrained', sharey=True)
    maximum = max(max(r['source_sum'], r['written_denominator'] + r['printed_program_cost'])
                  for r in result['primary'].values())
    data = []
    for ax, (topic, row) in zip(axes, result['primary'].items()):
        s, common, app, code = [row[k] for k in
                               ['source_sum', 'common_theory', 'applications', 'printed_program_cost']]
        pieces = [('source', 0, s, 0), ('common-written', 1, common, 0),
                  ('application-written', 1, app, common), ('common-printed', 2, common, 0),
                  ('application-printed', 2, app, common), ('program', 2, code, common + app)]
        for name, x, cost, bottom in pieces:
            role = name.split('-')[0]
            gid = 'bar-' + topic + '-' + name
            ax.bar(x, cost, bottom=bottom, color=COLORS[role], width=.58)[0].set_gid(gid)
            data.append(dict(id=gid, topic=topic, role=role, cost=cost, bottom=bottom))
        for x, y in [(0, s), (1, common + app), (2, common + app + code)]:
            ax.text(x, y + maximum * .024, f'{y:,}', ha='center', fontsize=8)
        ax.set_xticks([0, 1, 2], ['Originals', 'Our written\npapers', 'Our papers\n+ printed code'])
        ax.set_ylim(0, maximum * 1.16)
        ax.set_title('Topic A: seven originals' if topic == 'A' else 'Topic C: five originals')
        ax.spines[['right', 'top']].set_visible(False)
        ax.grid(axis='y', alpha=.2)
        ax.set_axisbelow(True)
    axes[0].set_ylabel('NFC characters without whitespace')
    fig.legend([Patch(color=COLORS[x]) for x in COLORS],
               ['Complete originals', 'Whole common theory', 'All applications', 'Whole program appendices'],
               loc='outside lower center', ncol=2, frameon=False, fontsize=8)
    fig.savefig(out / 'whole_costs.svg', metadata={'Date': None})
    fig.savefig(out / 'whole_costs.pdf', metadata={'CreationDate': None, 'ModDate': None})
    plt.close(fig)
    (out / 'plot_data.json').write_text(json.dumps(dict(primary_only=True, bars=data,
        actual_rectangles=12, shared_y_limit=maximum * 1.16,
        representation={'A': 'calibrated_selected', 'C': 'literal L108 and raw_untrimmed PDFs'}), indent=2) + '\n')


def reader(result, out):
    fmt = lambda q: f"{float(q['decimal']):.3f}"
    totals, applications = [], []
    for topic, row in result['primary'].items():
        totals.append(topic + ' & ' + ' & '.join(f'{row[k]:,}' for k in
            ['source_sum', 'common_theory', 'applications']) + ' & ' +
            ' & '.join(fmt(row['whole'][k]) for k in ['written', 'including_printed_programs',
                                                     'including_raw_programs']) + r' \\')
        for x in row['individual']:
            applications.append(' & '.join([topic, x['source'], x['application'],
                f"{x['source_cost']:,}", f"{x['application_cost']:,}", fmt(x['conditional'])]) + r' \\')
    unit_rows = []
    for label, unit in [('Whitespace tokens', 'whitespace_tokens'),
                        ('Alphanumeric runs', 'alphanumeric_units'),
                        ('Nonspace characters', 'characters_without_whitespace'),
                        ('Collapsed characters', 'characters_with_collapsed_whitespace'),
                        ('Collapsed UTF-8 bytes', 'utf8_bytes_with_collapsed_whitespace')]:
        vals = []
        for topic, variant in [('A', 'calibrated_selected'), ('C', 'raw_untrimmed')]:
            row = next(x for x in result['rows'] if (x['topic'], x['variant'], x['normalization'], x['unit'])
                       == (topic, variant, 'NFC', unit))
            vals.extend(fmt(row['whole'][k]) for k in ['written', 'including_printed_programs'])
        unit_rows.append(label + ' & ' + ' & '.join(vals) + r' \\')
    a, c = result['primary']['A'], result['primary']['C']
    text = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=23mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\title{Complete comparisons after adding two applications}
\author{Human Compression Project}\date{11 October 2026}
\begin{document}\maketitle
This edition extends two existing topics. Topic A now contains seven original manuscripts: L032, L034, F016, F013, L035, N009 and L128. Topic C contains five: L088, N013, L108, F014 and L068. The additions are Leemans--Spiga--Tranchida's \emph{Hypertopes with prescribed diagram symmetries} and Hartley--Hubard--Leemans's \emph{Regular 4-polytopes from the Livingstone graph of Janko's first group}. Twelve originals are compared; detailed theorem rows are not counted as manuscripts.

\paragraph{Complete topics.}
For each topic let $U$ contain every common paper, $A_i$ every complete application, and $P$ the whole declared program bundle. The comparison is
\[
R_{\rm written}=\frac{\sum_i c(L_i)}{c(U)+\sum_i c(A_i)}.
\]
The entire earlier Topic A common paper, six applications and four programs remain. Topic C retains its entire earlier common paper, four applications and two programs; the complete two-page incidence note is added to $U_C$. Each topic pays its full theory independently. No overlap deduction has been made.
\begin{center}\small\begin{tabular}{lrrr|rrr}\toprule
 & Originals & Common & Applications & Written & Printed code & Raw code\\\midrule
@TOTALS@
\bottomrule\end{tabular}\end{center}
The first three columns are primary NFC nonspace characters; the last three are source/denominator factors. The code columns add either the complete printed bundle or the complete raw files to the written denominator, never both. A factor below one means a longer replacement.

\paragraph{Complete applications after acquisition.}
Each row below gives $r_i\mid(U,P)=c(L_i)/c(A_i)$, conditional on \emph{the entire enlarged common theory and every whole declared program already being acquired}. These are not whole-topic savings.
\begin{center}\small\begin{tabular}{lllrrr}\toprule
Topic & Original & Application & Original cost & Application cost & Conditional\\\midrule
@APPLICATIONS@
\bottomrule\end{tabular}\end{center}
The whole printed bundles cost @A_PRINTED@ and @C_PRINTED@; the raw alternatives cost @A_RAW@ and @C_RAW@. Topic A pays five complete programs. Topic C pays three: its unchanged construction program is byte-identical in the new location and is charged once, while its earlier exhaustive census remains paid in full.
\newpage
\begin{center}\includegraphics[width=\textwidth]{whole_costs.pdf}\end{center}
Topic A retains its calibrated-selected primary representation. Topic C retains the complete literal rendering of L108 and raw untrimmed PDF extraction for every other source and replacement, including both new common and application documents. The bars use these declared representations; their costs are not pooled into a cross-topic factor.

\begin{center}\small\begin{tabular}{lrrrr}\toprule
 & \multicolumn{2}{c}{Topic A} & \multicolumn{2}{c}{Topic C}\\
NFC unit & Written & With printed code & Written & With printed code\\\midrule
@UNITS@
\bottomrule\end{tabular}\end{center}
Exact data preserve raw untrimmed, raw selected and calibrated selected text under NFC and NFKC, in all five units: sixty coordinates and 540 fractions. The twelve application comparisons use the same full acquisition in every coordinate. They do not measure a minimum proof length or establish a mathematical sawtooth pattern by themselves.

\paragraph{Scientific scope and limitations.}
The accepted source contracts and their corrections remain unchanged. L128 retains the qualification that its final proper-quotient claim preserves the same diagram. Frucht's theorem, the small-group classification and exact GAP algorithms are stated outside inputs. L068 includes the corrected construction with its additional incidence condition, the literal counterexample and the qualification of Proposition 3.3; it does not claim that every printed assertion is true. Complete source documents form the numerators because the specified main results have been recovered with these visible qualifications.

The independently accepted additions include all forty-eight pages and all new whole files. Seven delimiter components decoded as whitespace remain visible; the one envelope decoded as seven characters is calibrated as one glyph. Literal line-wrap hooks, extracted graph components and the L108 rendering retain their stated limitations. Full graphics, external proofs, historical software and a complete formalization have unknown costs, not zero.

The three new operational drivers and two Lean files remain separate inventories. The nine added formal declarations verify specific interfaces, not the complete source theorems. Earlier driver and formal inventories are unchanged. No scientific or conjecture credit is added by this numerical update. Previous measurements remain immutable; these new arithmetic, plots and reader require distinct review before admission.
\end{document}
'''
    replacements = {'TOTALS': '\n'.join(totals), 'APPLICATIONS': '\n'.join(applications),
                    'UNITS': '\n'.join(unit_rows), 'A_PRINTED': f"{a['printed_program_cost']:,}",
                    'C_PRINTED': f"{c['printed_program_cost']:,}",
                    'A_RAW': f"{a['raw_program_alternative']:,}",
                    'C_RAW': f"{c['raw_program_alternative']:,}"}
    for k, v in replacements.items():
        text = text.replace('@' + k + '@', v)
    need('@' not in text, 'reader fields resolved')
    (out / 'measurement.tex').write_text(text)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--results', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--xelatex', default='/opt/homebrew/bin/xelatex')
    a = ap.parse_args()
    need(not a.out.exists(), 'fresh render')
    a.out.mkdir(parents=True)
    result = json.loads(a.results.read_text())
    plot(result, a.out)
    reader(result, a.out)
    for i in range(2):
        proc = subprocess.run([a.xelatex, '-no-shell-escape', '-halt-on-error',
            '-interaction=nonstopmode', 'measurement.tex'], cwd=a.out, capture_output=True,
            text=True, timeout=180)
        (a.out / f'render{i}.log').write_text(proc.stdout + proc.stderr)
        need(proc.returncode == 0, 'clean TeX render')
    log = (a.out / 'measurement.log').read_text()
    bad = [s for s in log.splitlines() if any(t in s for t in
           ['Overfull', 'Missing character:', 'LaTeX Warning:'])]
    need(not bad, 'render diagnostics ' + repr(bad))
    from pypdf import PdfReader
    pages = [p.extract_text() or '' for p in PdfReader(a.out / 'measurement.pdf').pages]
    need(len(pages) == 2, 'two complete reader pages')
    report = dict(status='PASS', reader_pages=len(pages), diagnostics=[],
                  page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in pages])
    (a.out / 'render_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
