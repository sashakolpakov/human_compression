LogTo("research/leemans/chiral_fiber_check.log");
LeftSetCoset:=function(H,g) return Set(Elements(H),h->g*h);end;
ChamberImage:=function(C,g)return List(C,S->Set(S,x->g*x));end;
IsChamber:=function(C)
 local i,j;
 for i in [1..Length(C)] do for j in [i+1..Length(C)] do
  if IsEmpty(Intersection(C[i],C[j])) then return false;fi;
 od;od;
 return true;
end;
CheckFiber:=function(name,alph)
 local G,r,I,subsets,P,H,S,T,C,D,i,j,g,cosets,chambers,orbit0,orbit1,
       panel,basepanels,k,products,fiber,autos,inverter;
 G:=Group(alph);alph:=Concatenation([One(G)],alph);r:=Length(alph);I:=[1..r];
 subsets:=Combinations(I);
 P:=function(S)
  if Length(S)<2 then return TrivialSubgroup(G);fi;
  return Subgroup(G,Concatenation(List(S,i->List(S,j->alph[i]^-1*alph[j]))));
 end;
 for S in subsets do for T in subsets do
  if Intersection(P(S),P(T))<>P(Intersection(S,T)) then Error("C+ IP failed");fi;
 od;od;
 H:=List(I,i->P(Difference(I,[i])));C:=List(H,Elements);
 D:=[];
 for i in I do
  j:=First(I,j->j<>i);S:=ShallowCopy(C);S[i]:=LeftSetCoset(H[i],alph[i]^-1*alph[j]);
  if not IsChamber(S) or S=C then Error("Canonical neighbor failed");fi;
  Add(D,S);
 od;
 for i in I do for j in I do
  if ChamberImage(D[i],alph[j]^-1*alph[i])<>D[j] then Error("Neighbor transport failed");fi;
 od;od;
 cosets:=List(H,H->Set(Elements(G),g->LeftSetCoset(H,g)));
 chambers:=Filtered(Cartesian(cosets),IsChamber);
 orbit0:=Set(Elements(G),g->ChamberImage(C,g));
 orbit1:=Set(Elements(G),g->ChamberImage(D[1],g));
 if not IsEmpty(Intersection(orbit0,orbit1)) or Union(orbit0,orbit1)<>Set(chambers)
 then Error("Two orbit prediction failed");fi;
 for k in I do
  basepanels:=Set(Elements(G),g->List(Difference(I,[k]),i->ChamberImage(C,g)[i]));
  for T in chambers do
   panel:=List(Difference(I,[k]),i->T[i]);
   if not panel in basepanels then Error("Proper flag orbit failed");fi;
   if Number(chambers,S->List(Difference(I,[k]),i->S[i])=panel)<>2
   then Error("Thinness failed");fi;
  od;
  products:=List(Difference(I,[k]),j->Set(Concatenation(List(Elements(H[j]),
                   x->List(Elements(H[k]),y->x*y)))));
  fiber:=Intersection(products);
  if Length(fiber)<>2*Size(H[k]) then Error("Fiber count failed");fi;
 od;
 autos:=AutomorphismGroup(G);
 inverter:=ForAny(Elements(autos),f->ForAll(alph,a->Image(f,a)=a^-1));
 Print(name," grouporder=",Size(G)," rank=",r," chambers=",Length(chambers),
       " orbit_sizes=",[Length(orbit0),Length(orbit1)]," inversion=",inverter," PASS\n");
end;

# Rotations of the regular rank-four simplex.
rho:=[(1,2),(2,3),(3,4),(4,5)];
CheckFiber("simplex_A5",List([2..4],i->rho[1]*rho[i]));
# The chiral square toroid associated to the index-five lattice (1,2).
# Affine maps of F5: x -> 2x and x -> 1-x, with point x represented by x+1.
a:=PermList(List([0..4],x->(2*x mod 5)+1));
b:=PermList(List([0..4],x->((1-x) mod 5)+1));
CheckFiber("affine_F20",[a,b]);
LogTo();
QUIT;
