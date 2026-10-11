#!/usr/bin/env python3
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from compute import need
COLORS={'source':'#626c76','common':'#426b9a','application':'#70a59a','program':'#bd874e'}

def plot(result, out):
    os.environ['MPLCONFIGDIR'] = str(out / '.mpl')
    os.environ['XDG_CACHE_HOME'] = str(out / '.cache')
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 9,
                         'svg.fonttype': 'none', 'svg.hashsalt': 'B5-whole-topic-addition-v1'})
    fig, ax = plt.subplots(1, 1, figsize=(8.0, 3.0), layout='constrained')
    axes = [ax]
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
        ax.set_title('Topic B: five complete originals')
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
        actual_rectangles=6, shared_y_limit=maximum * 1.16,
        representation={'B': 'literal N001 and raw_untrimmed PDFs, including L040 cover'}), indent=2) + '\n')


def reader(result, out):
    row = result['primary']['B']
    fmt = lambda q: f"{float(q['decimal']):.3f}"
    applications = [' & '.join([x['source'], x['application'], f"{x['source_cost']:,}",
                    f"{x['application_cost']:,}", fmt(x['conditional'])]) + r' \\'
                    for x in row['individual']]
    unit_rows = []
    for label, unit in [('Whitespace tokens', 'whitespace_tokens'), ('Alphanumeric runs', 'alphanumeric_units'),
                        ('Nonspace characters', 'characters_without_whitespace'),
                        ('Collapsed characters', 'characters_with_collapsed_whitespace'),
                        ('Collapsed UTF-8 bytes', 'utf8_bytes_with_collapsed_whitespace')]:
        r = next(x for x in result['rows'] if (x['variant'], x['normalization'], x['unit']) ==
                 ('raw_untrimmed', 'NFC', unit))
        unit_rows.append(label + ' & ' + ' & '.join(fmt(r['whole'][k]) for k in
                         ['written', 'including_printed_programs', 'including_raw_programs']) + r' \\')
    body = row['article_only_sensitivity']
    text = r'''\documentclass[11pt,a4paper]{article}
\usepackage[margin=24mm]{geometry}
\usepackage{fontspec,unicode-math,booktabs,graphicx,hyperref}
\setmainfont{STIXGeneral}\setmathfont{STIX Two Math}\hypersetup{hidelinks}
\title{A complete comparison for five Topic B manuscripts}
\author{Human Compression Project}\date{11 October 2026}
\begin{document}\maketitle
Topic B now compares N001, N003, N008, L030 and L040. The new original is Fernandes--Leemans, \emph{C-groups of high rank for the symmetric groups}: the accepted institutional manuscript contains twenty authored pages and one publisher cover. The comparison uses that exact edition, not the earlier arXiv PDF. Five originals are counted; the thirty-five new detailed clauses are not thirty-five papers.

\paragraph{The full topic.}
Every earlier source and complete application remains. The existing five-page common paper is retained in full, as is the new ten-page common paper. The new application has eleven pages and its four whole programs fill a seven-page appendix. No overlap between the common papers is deducted before a revised unified proof is reviewed.
\begin{center}\begin{tabular}{lr}\toprule
Complete component & NFC nonspace characters\\\midrule
All five originals & @SOURCES@\\
Earlier common paper & @OLD_COMMON@\\
New common paper & @NEW_COMMON@\\
All five applications & @APPS@\\
Full printed program appendix & @PRINTED_CODE@\\
Full raw programs, alternative representation & @RAW_CODE@\\\bottomrule
\end{tabular}\end{center}
Writing $U$ for \emph{both entire common papers}, $A_i$ for each complete application and $P$ for the full program bundle gives
\[
R_{\rm written}=\frac{\sum_i c(L_i)}{c(U)+\sum_i c(A_i)}=@WRITTEN@.
\]
Including all printed programs gives @PRINTED@; using all raw programs instead gives @RAW@. Printed and raw code are alternatives, never a duplicate charge. The primary written replacement is slightly shorter overall, but the complete replacement including either program representation is longer.

\paragraph{Applications after acquisition.}
Each conditional factor below is $r_i\mid(U,P)=c(L_i)/c(A_i)$. It assumes that \emph{both entire common papers and all four complete programs have already been acquired}. It is not a whole-topic saving.
\begin{center}\begin{tabular}{lllrr}\toprule
Original & Application & Original cost & Application cost & Conditional\\\midrule
@APPLICATIONS@
\bottomrule\end{tabular}\end{center}
One program supplies required finite primitive-group inputs, two validate written uniform calculations, and one supports the auxiliary degree-eight example and validates branching. All four are included in the code columns above. Two operational drivers (10,902 and 7,708) and the partial Lean source (4,668) are separately inventoried. Eight new declarations do not formalize the complete classification.
\newpage
\begin{center}\includegraphics[width=\textwidth]{whole_costs.pdf}\end{center}
The primary representation is unchanged: complete literal authored text for N001 and raw untrimmed PDF extraction for every other original and replacement. Page furniture and the L040 cover remain. Full graphics, historical software, retained outside proofs, primitive-catalogue construction and complete formalization have unknown costs, not zero.

\begin{center}\small\begin{tabular}{lrrr}\toprule
NFC unit & Written & With printed code & With raw code\\\midrule
@UNITS@
\bottomrule\end{tabular}\end{center}
In the NFC UTF-8 coordinate, even the written factor is below one. All five units, NFC and NFKC, and three variants---raw untrimmed, raw selected and calibrated selected---remain in the exact data. Thirty coordinates give 240 main fractions. A separate cover-only sensitivity uses all twenty directly extracted authored L040 pages, never token subtraction, and changes no replacement cost. Its primary whole written factor is @BODY_WRITTEN@; with printed code it is @BODY_PRINTED@ and with raw code @BODY_RAW@. The L040 conditional becomes @BODY_CONDITIONAL@. The other four conditional values are unchanged. This sensitivity has 120 additional fractions.

\paragraph{Scope and representation limits.}
The accepted contract recovers the rank $n-1$ classification for $n\geq7$, rank $n-2$ for $n\geq9$, all allowed branching, complete intersection and flag arguments, and corrected general marking presentations. A printed branching clause has a literal counterexample and is not claimed as recovered without correction. The ancillary exact primitive-rank census and the ambiguous leaf-count convention remain outside the stated contract. The source's Whiston, Cameron--Cara and Mar\'oti inputs retain their exact hypotheses and attributions; unavailable full texts and outside computations are not silently free measured proofs.

The distinct input review inspected all forty-nine pages in the input packet and the actual exceptional glyphs. Twenty-four curved diagram classes remain literal extracted names rather than guessed arc symbols. Straight strokes and script letters use only observed outline corrections in the calibrated sensitivity; full graph structure and watermark artwork are not encoded by these text counts. The raw primary is unchanged. No new scientific or conjecture credit follows from this numerical update, and no sawtooth or minimum proof complexity conclusion is inferred from a length ratio. Earlier numerical reports remain immutable. Distinct review of arithmetic and the actual plots is required before admission.
\end{document}
'''
    replacements = {'SOURCES': f"{row['source_sum']:,}", 'OLD_COMMON': f"{row['common_components']['U_B_previous']:,}",
                    'NEW_COMMON': f"{row['common_components']['U_B_high_rank']:,}", 'APPS': f"{row['applications']:,}",
                    'PRINTED_CODE': f"{row['printed_program_cost']:,}", 'RAW_CODE': f"{row['raw_program_alternative']:,}",
                    'WRITTEN': fmt(row['whole']['written']), 'PRINTED': fmt(row['whole']['including_printed_programs']),
                    'RAW': fmt(row['whole']['including_raw_programs']), 'APPLICATIONS': '\n'.join(applications),
                    'UNITS': '\n'.join(unit_rows), 'BODY_WRITTEN': fmt(body['whole']['written']),
                    'BODY_PRINTED': fmt(body['whole']['including_printed_programs']),
                    'BODY_RAW': fmt(body['whole']['including_raw_programs']), 'BODY_CONDITIONAL': fmt(body['L040_conditional'])}
    for k, v in replacements.items():
        text = text.replace('@' + k + '@', v)
    need('@' not in text, 'resolved reader fields')
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
        p = subprocess.run([a.xelatex, '-no-shell-escape', '-halt-on-error', '-interaction=nonstopmode',
                            'measurement.tex'], cwd=a.out, capture_output=True, text=True, timeout=180)
        (a.out / f'render{i}.log').write_text(p.stdout + p.stderr)
        need(p.returncode == 0, 'clean TeX build')
    bad = [x for x in (a.out / 'measurement.log').read_text().splitlines()
           if any(k in x for k in ['Overfull', 'Missing character:', 'LaTeX Warning:'])]
    need(not bad, 'render diagnostics ' + repr(bad))
    from pypdf import PdfReader
    pages = [p.extract_text() or '' for p in PdfReader(a.out / 'measurement.pdf').pages]
    need(len(pages) == 2, 'two complete reader pages')
    report = dict(status='PASS', reader_pages=2, diagnostics=[],
                  page_text_sha256=[hashlib.sha256(t.encode()).hexdigest() for t in pages])
    (a.out / 'render_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()

