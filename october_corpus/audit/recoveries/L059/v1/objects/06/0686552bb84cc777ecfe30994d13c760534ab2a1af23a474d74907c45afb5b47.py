from pathlib import Path
import re, json, hashlib, sys
if sys.flags.optimize:
    raise RuntimeError('optimized Python is unsupported')
W = Path(__file__).resolve().parent
S = W.parent.parent
raw = (W/'c4_110_7_forms.html').read_text()
m = re.search(r'g:=Graph<110\|\{(.*?)\}\s*>;', raw, re.S)
if m is None:
    raise ValueError('expected one 110-vertex Magma graph')
es = [[int(a),int(b)] for a,b in re.findall(r'\{\s*(\d+)\s*,\s*(\d+)\s*\}',m[1])]
if len(es)!=220 or len(set(map(tuple,map(sorted,es))))!=220:
    raise ValueError('edge count or duplicate')
if not all(1<=a<=55<b<=110 for a,b in es):
    raise ValueError('bipartition')
if not all(sum(v in e for e in es)==4 for v in range(1,111)):
    raise ValueError('degree')
base=(S/'phase177_rank_two_graphs.g').read_text().split('P177Inputs :=')[0]
base=base.replace('Assert(1,','L059Need(')
guard='L059Need := function(ok) if not ok then Error("L059 exact check failed"); fi; end;;\n'
program=guard+base+'\nD:=P177Graph("C4_current_110_7",110,[1..55],'+str(es)+');;\nR:=P177Census(D);;\nPrintTo("exception_witnesses.g","L059Exception := ",R,";\\n");\nPrint("L059_EXCEPTION_COMPLETE\\n");\nQUIT;\n'
(W/'exception_census.g').write_text(program)
(W/'exception_edges.json').write_text(json.dumps({'n':110,'black':list(range(1,56)),'edges':es,'source':'c4_110_7_forms.html'},indent=2)+'\n')
print('prepared 110 vertices,220 edges; reuses full phase177 census algorithm')
