"""Find one small witness; its separate literal reader uses no graph library."""
from pathlib import Path
import itertools,json,networkx as nx,time
P=Path(__file__).resolve().parent
duads=list(itertools.combinations(range(1,7),2))
def matchings(xs):
 if not xs:
  yield ();return
 a=xs[0]
 for b in xs[1:]:
  for rest in matchings([x for x in xs[1:] if x!=b]):yield ((a,b),)+rest
synthemes=sorted(matchings(list(range(1,7))))
edges=sorted((duads.index(d),15+j)for j,t in enumerate(synthemes)for d in t)
G=nx.Graph();G.add_nodes_from((i,{'side':i//15})for i in range(30));G.add_edges_from(edges)
started=time.monotonic()
f=next(nx.algorithms.isomorphism.GraphMatcher(G,G,node_match=lambda a,b:a['side']!=b['side']).isomorphisms_iter())
data={'duads':duads,'synthemes':synthemes,'duality':[f[i]for i in range(30)],'indexing':'zero-based:15lexicographic duads,then15lexicographic synthemes','finder_seconds':time.monotonic()-started}
out=P/'duality.json';assert not out.exists();out.write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps({'status':'ONE_DUALITY_FOUND','permutation':data['duality'],'seconds':data['finder_seconds']}))
