"""Compare all six printed rows with the completed connected censuses."""
from pathlib import Path
import hashlib
import json
import re
from pypdf import PdfReader

S = Path('/Users/sasha/medusa/research/leemans')
W = S / 'reboot_20261013'
out = W / 'F006_source_table01'
out.mkdir(exist_ok=False)
paths = [Path(__file__), S / 'sources/coxeter_ranks2025.pdf']
pdf = PdfReader(paths[1])
assert len(pdf.pages) == 13
page = pdf.pages[11].extract_text()
(out / 'source_page12.txt').write_text(page)
source = {}
for name in ['H3', 'H4', 'F4', 'E6', 'E7', 'E8']:
    lines = re.findall(r'^' + name + r' ([^\n]+)$', page, re.M)
    assert len(lines) == 1, name
    cells = lines[0].split()
    assert len(cells) == 7
    pairs = []
    for cell in cells:
        m = re.fullmatch(r'(\d+)(?:\((\d+)\))?', cell)
        assert m is not None
        pairs.append([int(m[1]), int(m[2] or 0)])
    source[name] = pairs

pattern = (r'RANK\s+(\d+)\s+ordered\s+(\d+)\s+self\s+(\d+)\s+dual_classes\s+(\d+)'
           r'\s+connected_ordered\s+(\d+)\s+connected_self\s+(\d+)\s+connected_dual\s+(\d+)')
computed = {}
literal = {}
raw_rows = {}
for name, run, limit in [('F4','F006_F4_restored01',10),
                         ('H4','F006_H4_restored01',13),
                         ('E6','F006_E6_restored01',15),
                         ('E7','F006_E7_inner_restart01',21),
                         ('E8','central_marks_E8_01',29)]:
    run = W / run
    paths.extend([run/'report.json', run/'stdout.log', run/'stderr.log'])
    receipt = json.loads((run/'report.json').read_text())
    assert receipt['status']=='EXITED' and receipt['returncode']==0
    assert receipt['complete_marker'] and receipt['unchanged']
    assert (run/'stderr.log').read_bytes()==b''
    raw = (run/'stdout.log').read_text()
    assert raw.count('COMPLETE_EXHAUSTION')==1
    rows = [list(map(int,x)) for x in re.findall(pattern,raw)]
    assert [r[0] for r in rows]==list(range(1,limit+1))
    assert all(2*r[3]==r[1]+r[2] and 2*r[6]==r[4]+r[5] for r in rows)
    assert all(r[1]==0 for r in rows if r[0]<3)
    connected = {r[0]:[r[6],r[5]] for r in rows}
    unrestricted = {r[0]:[r[3],r[2]] for r in rows}
    def table(d):
        return [[sum(v[i] for v in d.values()) for i in range(2)]] + \
               [d.get(r,[0,0]) for r in range(3,8)] + \
               [[sum(v[i] for r,v in d.items() if r>=8) for i in range(2)]]
    computed[name] = table(connected)
    literal[name] = table(unrestricted)
    raw_rows[name] = rows

h3 = S / 'corpus106_F006_small_coxeter_v1/census/report.json'
paths.append(h3)
data = json.loads(h3.read_text())
assert data['status']=='COMPLETE_FINITE_CENSUS_EXECUTION'
assert [r['rank'] for r in data['rows']]==list(range(1,7))
h3_connected = {}
h3_literal = {}
for row in data['rows']:
    reps = row['representatives']
    assert len(reps)==row['count']
    assert sum(x['self_dual'] for x in reps)==row['self_dual']
    assert sum(x['connected'] for x in reps)==row['connected']
    h3_literal[row['rank']]=[row['count'],row['self_dual']]
    h3_connected[row['rank']]=[row['connected'],sum(x['self_dual'] and x['connected'] for x in reps)]
computed['H3']=table(h3_connected)
literal['H3']=table(h3_literal)
assert computed==source, (computed,source)
discrepancies={name:dict(printed=source[name],unrestricted=literal[name])
               for name in source if literal[name]!=source[name]}
assert set(discrepancies)=={'H3','E7'}
pins=[]
for p in paths:
    b=p.read_bytes()
    pins.append(dict(path=str(p.relative_to(S)),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
report=dict(status='ALL_SIX_CONNECTED_SOURCE_ROWS_MATCH',source_physical_page=12,
    printed_cells=42,columns=['total','rank3','rank4','rank5','rank6','rank7','rank>=8'],
    source=source,computed_connected=computed,computed_unrestricted=literal,
    literal_definition_discrepancies=discrepancies,complete_enumeration_rows=raw_rows,
    pins=pins,whole_original_credit=0,distinct_review_pending=True,
    limitation='Comparison of completed enumerations, not an independent completeness proof or whole-source acceptance.')
(out/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(dict(status=report['status'],printed_cells=42,discrepancies=list(discrepancies))))
