import sys
if sys.flags.optimize:
    raise SystemExit('normal Python required')
from pathlib import Path
import hashlib,json,shutil

H=Path(__file__).resolve().parent
S=H.parents[2]
P=H/'named_stage03'
D=S/'corpus106_L033_hyperbolic_names_v1'

def need(ok,msg):
    if not ok: raise ValueError(msg)
def load(p): return json.loads(p.read_text())
def dump(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def pin(p,base=None):
    b=p.read_bytes()
    return {'path':str(p.relative_to(base)) if base else str(p.resolve()),
            'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

need(not D.exists(),'immutable destination must be new')
report=load(H/'named_author03/report.json')
need(report['status']=='PASS_L033_TWENTY_TWO_GROUP_CERTIFICATES' and report['native_pages']==3 and report['positive_certificates']==22 and report['LINS_runs']==0,'complete bounded author replay')
receipt=load(H/'named_author03_receipt/receipt.json')
need(receipt['status']=='TERMINAL_PASS' and receipt['returncode']==0,'clean author receipt')
for row in load(P/'manifest.json')['exports']:
    need(all(pin(P/row['path'])[k]==row[k] for k in ['bytes','sha256']),'unchanged stage export')

shutil.copytree(P,D)
(D/'manifest.json').unlink()
shutil.copytree(H/'named_author03',D/'author_replay')
shutil.copytree(H/'named_author03_receipt',D/'author_receipt')
shutil.copy2(P/'manifest.json',D/'author_replay/input_stage_manifest.json')
shutil.copy2(H/'named_author03/native/names.pdf',D/'names.pdf')
shutil.copy2(H/'named_author03/native/names.log',D/'names.log')
shutil.copy2(Path(__file__),D/'freeze_names.py')
shutil.copy2(P/'README.rst',D/'history/stage03_README.rst')
(D/'README.rst').write_text('''Twenty-two named groups in the hyperbolic table
================================================

Read names.tex or names.pdf (three complete pages), followed by source_map.json.
This companion certifies the displayed group descriptions of 22 selected
literal marked groups from the accepted eight-diagram L033 core. Every selected
record has the universal local orders listed in selected_tuples.json; its
intersection property, actual flag transitivity and full automorphism-group
interpretation are acquired from that core, its distinct review and root
adoption. They are not inferred from a group order or structural string.

Replay, using normal Python and a new output whose parent exists:

  /Users/sasha/.venvs/global/bin/python check.py --study /Users/sasha/medusa/research/leemans --out NEW_ABSOLUTE_DIRECTORY --render

The replay takes about 20 seconds on the author environment. It verifies exact
dependencies, all 22 group certificates, five specifically damaged certificates,
three damaged source joins, two optimization guards and the three-page native
manuscript. It does not call LINS, regenerate a kernel census or search for new
tuples. Each GAP child is capped at 60 seconds; commands, outputs and failures
are retained. Software and constructor premises are explicit in the manuscript
and software_interfaces.json. Source Table 3 is physical page 14 of the exact
16-page catalogue_L033.pdf, pinned as a documentary source input.

Unspecified extension actions mean the literal certified actions; this is not a
classification of all abstract groups with the same structural string. The two
source-order exclusions 336 and 2160 remain acquired core results. The ninth
square (3,5,3,5), its printed orders 3840 and 9720, and all remaining whole-source
obligations are outside this component. No priority, new census, measurement,
question, Lean or whole-original credit is claimed.

The root supplied the original normal-quotient probe. The publication agent
authored the group certificates, verifier and companion proof. Acquired review
roles are unchanged. Earlier provider searches supply positive witnesses only.
The failed stage02 native-tool invocation and all earlier verifier corrections
are retained in history. Stage03 replaced an unavailable PDF-text utility by
pinned pypdf and Ghostscript; no GAP certificate or mathematical text changed.
All three final author-native pages were directly viewed before this freeze.
''')
dump(D/'scope.json',{
    'status':'AUTHOR_FROZEN_L033_TWENTY_TWO_NAMED_GROUP_CERTIFICATES',
    'source':'sources/catalogue_L033.pdf','physical_page':14,
    'positive_named_rows':22,'source_table_rows':26,
    'selected_tuples_from_accepted_core':22,'accepted_core_positive_tuples':59,
    'all_selected_local_orders_universal':True,
    'source_map':'source_map.json','proof':'names.tex',
    'acquired_core_excluded_orders':[336,2160],
    'ninth_square_3535':{'status':'OUTSIDE_THIS_COMPONENT','printed_orders':[3840,9720]},
    'structural_notation':'actual certified extensions; no uniqueness assertion from an unspecified action',
    'new_LINS_runs':0,'new_census_runs':0,'whole_original_credit':0,
    'new_questions':0,'new_measurements':0,'new_Lean':0})
dump(D/'visual_review.json',{
    'reviewer_role':'author','native_pages_directly_viewed':[1,2,3],
    'source_Table3_physical_page_directly_viewed':14,
    'native_route':'author_replay/native','clean_two_pass_build':True,
    'complete_text_and_table':True,
    'rendered_pages':[pin(D/'author_replay/native'/f'page-{i:02d}.png',D) for i in [1,2,3]]})
dump(D/'provenance.json',{
    'root':'original normal-quotient probe provider; no authorship of the new named-group certificate argument',
    'publication_recovery':'literal certificates, verifier, source join, complete proof, bounded wrapper and native review',
    'distinct_review':'not yet requested for these frozen bytes',
    'acquired_reviews':'unchanged roles as recorded in the accepted eight-diagram core',
    'earlier_searches':'candidate providers only; not completeness premises for the new positive certificates',
    'preserved_native_failure':'history/failed_author02_receipt/receipt.json',
    'native_repair':'history/native_repair.diff'})

deps=load(P/'dependencies.json')
seen={(r.get('namespace'),r['path'],r['sha256']) for r in deps}
for folder in [P,H/'named_author03',H/'named_author03_receipt']:
    for q in sorted(folder.rglob('*')):
        if q.is_file() and '__pycache__' not in q.parts:
            r=pin(q);key=(None,r['path'],r['sha256'])
            if key not in seen: deps.append(r);seen.add(key)
deps.append(pin(Path(__file__)))
dump(D/'dependencies.json',deps)
exports=[pin(q,D) for q in sorted(D.rglob('*')) if q.is_file()]
dump(D/'manifest.json',{
    'status':'AUTHOR_FROZEN_L033_TWENTY_TWO_NAMED_GROUP_CERTIFICATES',
    'scope':'22 positive named-group rows from the accepted 59 marked tuples; no ninth diagram or whole original',
    'exports':exports,'dependencies':len(deps),'native_pages':3,
    'new_LINS_runs':0,'new_census_runs':0,'whole_original_credit':0})
print(json.dumps({'packet':str(D),'manifest':pin(D/'manifest.json'),'exports':len(exports),'dependencies':len(deps)}))
