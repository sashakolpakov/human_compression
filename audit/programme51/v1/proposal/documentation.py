#!/usr/bin/env python3
"""Private proposed reader-facing updates; scientific source bytes are untouched."""
from pathlib import Path
import json,os
H=Path(__file__).resolve().parent
def put(path,text):
    p=H/'wrappers'/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
def link(label,target,base):return '`'+label+' <'+os.path.relpath(target,Path(base).parent)+'>`_'
def main():
    guide='papers/topic-a/v4/PUBLICATION.rst'
    def l(label,target):return link(label,target,guide)
    text='''Nine originals using the common theory of kernels and lattices
==============================================================

The current Topic A comparison contains nine originals. The entire accepted
23-page common paper and its eight existing applications are unchanged at v3.
L121 adds the complete eleven-page application of the same common theory.
There is no second copy of the common paper and no cross-topic discount.

'''+l('Read the common paper','papers/topic-a/v3/umbrella.pdf')+', '+l('the new application','papers/topic-a/extensions/locally-toroidal/v1/application.pdf')+', and '+l('the four-page numerical reader','audit/topic-a/v4/measurement/packet/reader.pdf')+'''.
The complete source map has 27 L121 dispositions, in addition to 102 prior
dispositions. These are nine manuscripts, not 129 original papers. The source
families and constructions retain their authorship. The corrected cubic
toroid identification, literal finite presentation claims and unrestricted
minimum-degree suggestion retain their exact accepted qualifications.

The primary written comparison is 273,937/(66,140+136,125) = 1.354347019999.
The prior eight-original comparison was 1.395289617239. The L121 conditional
comparison is 27,367/25,549 = 1.071157383851, after acquisition of the entire
common theory and required computational and retained mathematical premises.
All eight previous conditionals remain exact. The 30 coordinates and 300
fractions preserve the accepted unit and extraction sensitivities.

Programs are excluded symmetrically from the written scalar. The enlarged
topic requires twenty complete program/data files. Its three historical
printed appendices cover only the old eleven-file subset; they are not a
complete enlarged program representation. All 45 whole raw files remain
inventoried: twenty required, three inherited auxiliaries, six operational
runners, fifteen partial Lean modules and one dependency manifest. Historical
source software, full graphics and complete external proof costs remain
unknown. No software-inclusive, pooled or full-formalization factor is given.
The six added Lean declarations check specified finite relations and two
nonconsequences; they do not prove the uniform geometry or group orders.

The original frozen author records retain their contemporary candidate labels.
'''+l('The current admission','audit/topic-a/v4/admission.json')+''' binds the subsequent distinct
scientific, input and numerical acceptances. Root assembled the scientific
application; rewrite_termination reviewed that assembly and the new inputs,
then authored the numerical successor; enumeration_volume independently
reviewed the numerical derivation. Historical roles remain disclosed.

The canonical TeX builder now registers the nine existing v3 scientific rows
and the new L121 row while retaining historical editions. The former use
XeLaTeX; L121 uses pdfLaTeX with all five declared section files. Exact current
builds total 79 pages. Numerical replay does not run the scientific programs::

    python -B -O audit/topic-a/v4/measurement/packet/check.py --out /fresh/output --render

L022 is a separately reviewed editorial preface. It remains one of the 106
accessible originals, with no mathematical recovery or measurement factor.
It is not an application of this common theory and is not added to the A
numerator. The programme therefore records 51 measured originals, 54 originals
awaiting mathematical recovery, and one editorial; 55 unavailable originals
remain archived. No new question-answer or historical-priority claim follows.
'''
    put(guide,text)
    put('papers/topic-a/extensions/locally-toroidal/v1/PUBLICATION.rst','''Period lattices and locally toroidal hypertopes
==============================================

The unchanged application.tex/PDF is the accepted L121 assembly. Its full
source map contains 27 dispositions, including corrected literal source
claims and explicitly retained classical inputs. The original README/scope
candidate labels are preserved as historical author bytes; subsequent
scientific and numerical acceptances are bound by the current admission.

The complete common theory is the unchanged 23-page Topic A v3 paper.
This extension adds eight required mathematical programs and one data file;
four operational runners and two partial-formal files remain separate.
cubic_relation/check.py is an actual required coordinate calculation despite
its filename. The six Lean declarations cover finite relations and specified
nonconsequences only. Historical software cost is unknown, not zero.

`Current common paper <../../../v3/umbrella.pdf>`_
`Current topic guide <../../../v4/PUBLICATION.rst>`_
`Exact local admission <../../../../../audit/topic-a/extensions/locally-toroidal/v1/admission.json>`_
No scientific, numerical or source body was edited for publication.
''')
    old=(H/'baseline/README.rst').read_text();new=old;edits=[]
    def change(before,after):
        nonlocal new
        n=new.count(before)
        if not n:raise ValueError('missing README exact target '+before[:60])
        new=new.replace(before,after);edits.append(dict(before=before,after=after,occurrences=n))
    begin=new.index('Current LCD edition\n');end=new.index('Current LCD papers',begin)
    change(new[begin:end],'''Current programme and locally toroidal extension
-----------------------------------------------

The programme contains **51 recovered/measured originals, 54 awaiting mathematical recovery, and one editorial**, within the 106 accessible originals; 55 earlier indexed originals remain archived. L121 adds one complete application to the existing shared theory A. Its whole written factor is **1.354347**, down from the preceding eight-original factor **1.395290**; L121's conditional factor is **1.071157**, after acquisition of the entire common theory and required computational and retained mathematical premises. The `current A guide <papers/topic-a/v4/PUBLICATION.rst>`_ and `numerical reader <audit/topic-a/v4/measurement/packet/reader.pdf>`_ preserve all exact costs and qualifications.

L022 is a completely read editorial preface with no principal mathematical result to recover. Its `accepted disposition <audit/corpus/editorial/L022/v1/admission.json>`_ keeps it active, assigns no factor and adds no measured-original or question credit. The `current overview <audit/overview/v17/packet/reader.pdf>`_ keeps nineteen topics; all eighteen other topic factors and all fifty previous individual factors remain unchanged.

The preceding LCD addition
-------------------------

The `LCD edition <papers/topic-lcd/latest.json>`_ retains L050 and F017, its complete fourteen-page common paper and applications of fifteen and twelve pages. Its whole written factor remains **0.592382: expansion, not achieved whole-topic compression**. The conditional L050/F017 factors remain **0.659169** and **1.157126**. There is no software-inclusive or pooled factor.

''')
    change('nineteen whole-topic and fifty individual factors','nineteen whole-topic and fifty-one individual factors')
    change('**50 accessible originals have admitted principal-result recoveries;\n56 await complete recovery.** Nineteen whole-topic factors and fifty individual',
           '**51 accessible originals have admitted principal-result recoveries;\n54 await mathematical recovery, and one is editorial.** Nineteen whole-topic factors and fifty-one individual')
    change('audit/corpus/accessible106/updates/lcd-catalogue.json','audit/corpus/accessible106/updates/l121-editorial-catalogue.json')
    begin=new.index('The `consolidated comparison');end=new.index('There is no software-inclusive or pooled factor.',begin)
    change(new[begin:end],'''The `consolidated comparison <audit/overview/v17/packet/reader.pdf>`_ accounts
for nineteen topics and fifty-one measured originals. Topic A pays the whole
23-page common paper and all 56 application pages for its nine originals;
its written factor is **1.354**. The eighteen other topic records and all
fifty previous conditional records remain unchanged from v16. L022 is retained
separately as editorial material without a factor. All accepted listing
exclusions, retained premises and unknown source costs remain explicit.
''')
    change('`remaining twenty-five\n','`remaining individual comparisons\n')
    change('     - 8\n     - 1.395\n','     - 9\n     - 1.354\n')
    begin=new.index('The `current common paper <papers/topic-a/v3/umbrella.pdf>');end=new.index('Earlier Topic A editions (historical)',begin)
    block=new[begin:end]
    block=block.replace('all eight\noriginals','all nine\noriginals').replace('papers/topic-a/v3/PUBLICATION.rst','papers/topic-a/v4/PUBLICATION.rst').replace('audit/topic-a/v3/measurement/packet/reader.pdf','audit/topic-a/v4/measurement/packet/reader.pdf')
    block=block.replace('66,140 characters and all applications 110,576, against 246,570 source\ncharacters. All eleven required program/data files retain their proof roles;\nthe three printed appendices and full raw inventories remain separate.','66,140 characters and all applications 136,125, against 273,937 source\ncharacters. All twenty required program/data files retain their proof roles;\nthe three old printed appendices cover only the old eleven-file subset.\nThe complete enlarged raw inventory is separate; no enlarged printed-code\nor software-inclusive factor is claimed.')
    block+=''
    block=block.rstrip()+'''\n   * - L121
     - `locally toroidal hypertopes <papers/topic-a/extensions/locally-toroidal/v1/application.pdf>`_

'''
    change(new[begin:end],block)
    change('audit/overview/v16/','audit/overview/v17/')
    put('README.rst',new)
    oldcomp=(H/'baseline/audit/completion.rst').read_text()
    header='''Current programme51 proposal: 51 recovered/measured originals, 54 pending mathematical originals and one separately accepted editorial (L022), among106 active;55 archived. L121 adds one complete application to A, with entire U23 paid and all prior scientific bytes unchanged. No new question credit. Current nine-source A comparison: audit/topic-a/v4; consolidated overview17 is separately reviewed. Earlier chronological completion records below remain historical.\n\n'''
    pos=oldcomp.find('\n\n')+2;put('audit/completion.rst',oldcomp[:pos]+header+oldcomp[pos:])
    (H/'documentation_delta.json').write_text(json.dumps(dict(status='PRIVATE_PROPOSED_UPDATES_REQUIRING_JOINT_OVERVIEW17_INTEGRATION',readme_replacements=edits,
      scientific_TeX_changes=0,overview17_prepublication_gate=True,historical_text_preserved_in_baseline=True),indent=2)+'\n')
if __name__=='__main__':main()
