import importlib.util,json,sys
from pathlib import Path
if sys.flags.optimize:raise RuntimeError('unoptimized execution required')
w=Path(__file__).resolve().parent
v=importlib.util.spec_from_file_location('arrays',w/'verify_arrays.py');m=importlib.util.module_from_spec(v);v.loader.exec_module(m)
wings=[t for n in range(2,13,2) for t in m.load_run(w,n)]
r=json.loads((w/'arrays_report.json').read_text());full=[x['marks'] for rows in r['boundary_literal_classes'].values() for x in rows]
f=w/'positive_inputs.g'
f.write_text('wingArrays:='+repr([[[x+1 for x in g] for g in t] for t in wings])+';;\nfullArrays:='+repr([[[x+1 for x in g] for g in t] for t in full])+';;\n')
