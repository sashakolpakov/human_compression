"""Small graph/design controls only; never run the M11 target."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
import importlib.util,json
H=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('graphs',H/'compute.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
c6=[[3,5],[3,4],[4,5],[0,1],[1,2],[0,2]]
a=m.metrics(c6,3);m.need((a['point_diameter'],a['gonality'],a['line_diameter'])==(3,3,3),'C6')
d=m.designs(c6,3,0);m.need(d['uniform_counts']==[{'t':1,'lambda_value':2,'subsets_checked':3},{'t':2,'lambda_value':1,'subsets_checked':3}] and d['distinct_blocks']==3,'triangle design')
k23=[[2,3,4],[2,3,4],[0,1],[0,1],[0,1]]
a=m.metrics(k23,2);m.need((a['point_diameter'],a['gonality'],a['line_diameter'])==(2,2,2),'K2,3')
d=m.designs(k23,2,0);m.need(d['complete_incidence'] and d['constant_lambda']==3 and d['distinct_blocks']==1,'repeated full blocks')
c8=[[4,7],[4,5],[5,6],[6,7],[0,1],[1,2],[2,3],[0,3]]
a=m.metrics(c8,4);m.need(a['girth']==8,'C8 girth');d=m.designs(c8,4,0);m.need(d['first_failure']['t']==2 and sorted(d['first_failure']['counts'])==[0,1],'nonuniform two-subsets')
bad=[row[:] for row in c6];bad[0].pop()
try:m.metrics(bad,3)
except ValueError as e:m.need('undirected' in str(e),'correct bad edge guard')
else:raise ValueError('asymmetric adjacency accepted')
print(json.dumps({'status':'PASS_L036_M11_SMALL_GRAPH_CONTROLS','graphs':['C6','K2,3','C8'],'checks':['all-root girth','type eccentricities','all design subsets','full repeated blocks','explicit non-design pair','asymmetric-edge rejection'],'M11_target_executed':False}))
