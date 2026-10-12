#!/usr/bin/env python3
"""Optional two-backend validation, not a premise of the elementary proof."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--gap', default='/opt/homebrew/bin/gap')
p.add_argument('--out', type=Path, required=True)
a = p.parse_args()
data_path = Path(__file__).with_name('graph.json')
data = json.loads(data_path.read_bytes())
script = '''
if LoadPackage("grape")=fail or LoadPackage("digraphs")=fail then Error("packages");fi;
adj:=%s;;gens:=%s;;
B:=Graph(Group(()),[1..Length(adj)],OnPoints,function(u,v)return v in adj[u];end,true);;
A:=AutGroupGraph(B);;
D:=Digraph(adj);;C:=BlissAutomorphismGroup(D);;
P:=Group(List(gens,PermList));;
if A<>C or A<>P or Size(A)<>5376 then Error("full group discrepancy");fi;
part:=Filtered([1..896],v->Distance(B,1,v) mod 2=0);;
K:=Stabilizer(A,Set(part),OnSets);;
edges:=Set(Concatenation(List([1..896],u->List(Filtered(adj[u],v->v>u),v->[u,v]))));;
if Size(K)<>2688 or Length(Orbits(K,edges,OnSets))<>1 then Error("part action");fi;
distribution:=Collected(List(Filtered(Elements(A),g->not g in K),Order));;
if distribution<>[[4,1024],[12,896],[28,768]] then Error("coset distribution");fi;
Print("GAP ",GAPInfo.Version," grape ",PackageInfo("grape")[1].Version,
 " digraphs ",PackageInfo("digraphs")[1].Version,"\\n");
Print("L126_TWO_BACKEND_PASS full=5376 kernel=2688 orders=",distribution,"\\n");
QUIT;
''' % (repr(data['adjacency']), repr(data['generators']))
r = subprocess.run([a.gap, '-q', '-b'], input=script, text=True,
                   capture_output=True, timeout=120)
if r.returncode != 0 or 'L126_TWO_BACKEND_PASS' not in r.stdout or 'Error,' in r.stdout + r.stderr:
    raise SystemExit('GAP diagnostic failed\n' + r.stdout + r.stderr)
result = {'status': 'PASS', 'role': 'optional validation only',
          'data_sha256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
          'diagnostic_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          'stdout': r.stdout, 'stderr': r.stderr}
a.out.parent.mkdir(parents=True, exist_ok=True)
a.out.write_text(json.dumps(result, indent=2) + '\n')
print(r.stdout.strip())
