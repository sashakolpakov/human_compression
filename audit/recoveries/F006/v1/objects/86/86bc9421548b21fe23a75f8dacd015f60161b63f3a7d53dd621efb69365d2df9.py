"""Check the exact Coxeter presentations of the five retained models."""
from pathlib import Path
import hashlib
import json
import subprocess

S = Path('/Users/sasha/medusa/research/leemans')
M = S / 'corpus106_F006_exceptional_work'
W = S / 'reboot_20261013/F006_model_identification01'
W.mkdir(exist_ok=False)


def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=hashlib.sha256(b).hexdigest())


models = [('F4', 4, 1152), ('H4', 4, 14400), ('E6', 6, 51840),
          ('E7', 7, 2903040), ('E8', 8, 696729600)]
code = 't:=[];;matrix:=[];;\n'
pins = [pin(Path(__file__))]
for name, n, order in models:
    p = M / (name + '_model.g')
    pins.append(pin(p))
    matrix = [[1 if i == j else 2 for j in range(n)] for i in range(n)]
    edges = ([(0, 1, 3), (1, 2, 4), (2, 3, 3)] if name == 'F4' else
             [(0, 1, 5), (1, 2, 3), (2, 3, 3)] if name == 'H4' else
             [(i, i+1, 3) for i in range(n-2)] + [(2, n-1, 3)])
    for i, j, k in edges:
        matrix[i][j] = matrix[j][i] = k
    code += 'Read(' + json.dumps(str(p)) + ');;\n'
    code += 't:=List(modelPerms,PermList);;\n'
    code += 'matrix:=' + json.dumps(matrix) + ';;\n'
    code += f'if Length(t)<>{n} or Size(G)<>{order} then Error("order or degree");fi;\n'
    code += ('if not ForAll(t,x->Order(x)=2) then Error("reflection order");fi;\n'
             'for i in [1..Length(t)] do for j in [1..Length(t)] do\n'
             ' if Order(t[i]*t[j])<>matrix[i][j] then Error("Coxeter relation");fi;\n'
             'od;od;\n')
    code += f'Print("VERIFIED_COXETER_MODEL {name} ORDER ",Size(G),"\\n");\n'
code += 'Print("COMPLETE_FIVE_MODEL_IDENTIFICATIONS\\n");QUIT;\n'
(W / 'check.g').write_text(code)
pins.append(pin(W / 'check.g'))
with (W / 'stdout.log').open('wb') as so, (W / 'stderr.log').open('wb') as se:
    result = subprocess.run(['/opt/homebrew/bin/gap', '-q', '-b', 'check.g'],
                            cwd=W, stdout=so, stderr=se, timeout=120)
complete = (W / 'stdout.log').read_text().count('COMPLETE_FIVE_MODEL_IDENTIFICATIONS') == 1
unchanged = all(pin(Path(p['path'])) == p for p in pins)
ok = result.returncode == 0 and complete and unchanged and not (W / 'stderr.log').read_bytes()
report = dict(status='PASS' if ok else 'FAILED_NO_CERTIFICATE', returncode=result.returncode,
              complete_marker=complete, unchanged=unchanged, pins=pins,
              retained_classical_input='Finite Coxeter presentations and their exact classical orders.',
              whole_original_credit=0)
(W / 'report.json').write_text(json.dumps(report, indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='pins'}))
raise SystemExit(0 if ok else 1)
