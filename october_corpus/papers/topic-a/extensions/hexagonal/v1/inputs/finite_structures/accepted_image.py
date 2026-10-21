"""Exact group reconstruction from the whole accepted per-row receipt."""
from pathlib import Path
HERE=Path(__file__).resolve().parent
PRIOR=HERE
def group_code(i):
 s=(PRIOR/'accepted_certificates'/(i+'.log')).read_text();gens=s.split('ROTATION_GENERATORS ',1)[1].split('\nLITERAL_RELATORS ',1)[0].strip()
 code='SetAssertionLevel(1);;SizeScreen([100000,100000]);;gg:='+gens+';;G:=Group(gg);;\n'
 if 'CHIRALITY_WITNESS_RELATOR' not in s:
  code+='aut:=GroupHomomorphismByImages(G,G,gg,List(gg,Inverse));;Assert(0,aut<>fail and IsBijective(aut));;d:=LargestMovedPoint(G);;diag:=g->PermList(Concatenation(List([1..d],i->i^g),List([1..d],i->d+i^Image(aut,g))));;t:=PermList(Concatenation([d+1..2*d],[1..d]));;G:=Group(Concatenation([t],List(gg,diag)));;\n'
 return code
