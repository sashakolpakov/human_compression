import hashlib
import json
import shutil
from pathlib import Path

W = Path(__file__).resolve().parent
P = Path('/Users/sasha/medusa/research/leemans/corpus106_N010_principal_v1')
if P.exists():
    raise RuntimeError('Refuse to overwrite a frozen author edition')
P.mkdir()
files = ['principal.tex', 'principal.pdf', 'principal_expected.txt',
         'principal_and_components.pdf', 'context_table.tex', 'question_table.tex',
         'secondary_table.tex', 'claim_register.json', 'scope.json', 'provenance.json',
         'acquired_manuscripts.json', 'acquired_packets.json', 'dependencies.json',
         'prepare_synthesis_tables.py', 'prepare_principal.py', 'freeze_principal.py',
         'principal.log', 'synthesis_build04.stdout', 'synthesis_build04.stderr',
         'synthesis_build05.stdout', 'synthesis_build05.stderr',
         'metadata02.stdout', 'metadata02.stderr']
for name in files:
    shutil.copyfile(W / name, P / name)
shutil.copyfile(W / 'check_principal.py', P / 'check.py')
(P / 'README.rst').write_text('''Chambers, universal constructions, and realization cones
========================================================

Author edition awaiting distinct review of the entire survey assembly.
Read principal.pdf (11 pages), then the four complete components in
principal_and_components.pdf (22 immediate pages in total). Older acquired
group/chamber/classification proofs remain additional dependencies; this
page count is not a compression measurement or the total cost of all inputs.

The fixed source has34 numbered problems and14 secondary records,16contexts,
51 established/contextual clauses and66 bibliography entries. All are routed.
The source-only17/441 aggregates are explicitly not independently reproduced;
the acquired137-family census does not determine a corrected global total.
Retained classifications, source reports, acquired old answers and new proofs
of established statements have different dispositions. No new conjecture,
current open-status survey, Lean declaration or numerical factor is claimed.

The checksum/source-join checker does not verify mathematical proofs.
Run with normal Python and pypdf, using a fresh external output directory::

  python check.py --study STUDY --repo REPOSITORY --out FRESH --render

The three literal TeX inputs context_table.tex,question_table.tex and
secondary_table.tex must remain adjacent to principal.tex. All private
component editions and published complete transports are acquired at exact
hashes; no historical group census is repeated by this wrapper.

The metadata preparation retained three pypdf warnings about annotation
sizes while merging inherited PDFs. The final wrapper compares every page's
text with the unabridged component PDFs; no mathematical page is omitted.
The TeX synthesis itself builds without layout or reference warnings.
''')
exports = []
for p in sorted(P.iterdir()):
    b = p.read_bytes()
    exports.append(dict(path=p.name, bytes=len(b), sha256=hashlib.sha256(b).hexdigest()))
(P / 'manifest.json').write_text(json.dumps(dict(original='N010',
    status='AUTHOR_FROZEN_COMPLETE_SURVEY_DISPOSITION_AWAITS_DISTINCT_REVIEW',
    exports=exports), indent=2) + '\n')
b = (P / 'manifest.json').read_bytes()
print(json.dumps(dict(path=str(P / 'manifest.json'), bytes=len(b),
                      sha256=hashlib.sha256(b).hexdigest(), exports=len(exports))))
