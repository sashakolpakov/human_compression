# Complete small-group exclusion, modulo actual automorphisms of each group.
Need:=function(b,m)if not b then Error(m);fi;end;
Run:=function()
 local n,G,au,els,inv,reps,a,b,c,rr,H,K,st,bs,pairs,triples,poly,rev,nonchiral,images,perms,r,ts;
 for n in [5,6] do
  G:=AlternatingGroup(n);au:=AutomorphismGroup(G);els:=Elements(G);inv:=Filtered(els,x->Order(x)=2);
  reps:=List(Orbits(au,els),x->x[1]);pairs:=0;triples:=0;poly:=0;nonchiral:=0;
  for a in Filtered(reps,x->Order(x)>2) do
   st:=Stabilizer(au,a);bs:=Filtered(els,b->Order(b)>2 and Order(a*b)=2 and Size(Intersection(Group(a),Group(b)))=1);
   for b in List(Orbits(st,bs),x->x[1]) do
    H:=Group(a,b);if H=G then continue;fi;pairs:=pairs+1;r:=a*b;
    for ts in inv do
     c:=r*ts;
     if Order(c)<=2 or Order(b*c)<>2 then continue;fi;
     K:=Group(b,c);if K=G or Size(Intersection(Group(b),Group(c)))<>1 then continue;fi;
     if Group(a,b,c)<>G then continue;fi;triples:=triples+1;
     if Intersection(H,K)<>Group(b) then continue;fi;poly:=poly+1;
     rev:=GroupHomomorphismByImages(G,G,[a,b,c],[a^-1,a^2*b,c]);
     Need(rev<>fail and IsBijective(rev) and ForAll([a,b,c],x->Image(rev,Image(rev,x))=x),"every small polytopal triple has actual reversal");nonchiral:=nonchiral+1;
    od;
   od;
  od;
  Need(nonchiral=poly,"complete exclusion");
  Print("SMALL_ROTATIONS ",Size(G)," AUT ",Size(au)," PAIRS ",pairs," GENERATING_TRIPLES ",triples," POLYTOPAL ",poly," CHIRAL0\n");
 od;
 Print("SMALL_ROTATION_EXCLUSIONS_PASS\n");
end;
Run();QUIT;
