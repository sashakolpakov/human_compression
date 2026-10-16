# Independent finite checks, not premises of the general proofs.
L115Controls:=function()
 local F,els,pairs,q,theta,perms,a,b,P,Z,H,B,t,maxes,got,expected,
       m,d,k,A,C,G,normal,classes,X,K,orders,count,p,alpha;
 F:=GF(8);els:=AsList(F);q:=8;theta:=4;pairs:=Cartesian(els,els);
 perms:=[];
 for a in els do for b in els do
  Add(perms,PermList(List(pairs,x->Position(pairs,[x[1]+a,x[2]+b+x[1]*a^theta]))));
 od;od;
 P:=Group(perms);Z:=Centre(P);t:=PrimitiveElement(F);
 H:=Group(PermList(List(pairs,x->Position(pairs,[t^theta*x[1],t^(theta+2)*x[2]]))));
 B:=ClosureGroup(P,H);
 if Size(P)<>64 or Size(Z)<>8 or Size(B)<>448 then Error("actual affine groups");fi;
 if Set(List(Elements(P),x->x^2))<>Set(Elements(Z)) then Error("squares are exactly Z");fi;
 if FrattiniSubgroup(P)<>Z then Error("actual Frattini subgroup");fi;
 maxes:=MaximalSubgroupClassReps(B);got:=SortedList(List(maxes,Size));
 if got<>[56,64] or not ForAll(maxes,M->IsSubgroup(M,Z)) then Error("point stabilizer maximal classes");fi;
 Print("POINT_STABILIZER_Q8 MAXIMAL_ORDERS ",got," CENTER_AND_FRATTINI 8\n");
 # Permutation realizations of every unit action admitted by these small cases.
 # x -> x+1 generates the odd cyclic normal subgroup.  x -> k*x acts
 # on it; a disjoint d-cycle retains the full complement even if k has
 # smaller order.
 count:=0;
 for m in [1,3,5,9,13,15] do for d in [2,4] do
  for k in [0..m-1] do
   if Gcd(k,m)=1 and (k^d mod m)= (1 mod m) then
    A:=Group(PermList(Concatenation(List([0..m-1],x->((x+1)mod m)+1),[m+1..m+d])));
    alpha:=PermList(Concatenation(List([0..m-1],x->((k*x)mod m)+1),List([0..d-1],x->m+((x+1)mod d)+1)));
    G:=ClosureGroup(A,Group(alpha));
    if Size(G)<>m*d or not IsNormal(G,A) then Error("cyclic semidirect realization");fi;
    classes:=MaximalSubgroupClassReps(G);
    expected:=[m*d/2];
    for p in Set(FactorsInt(m)) do Add(expected,m*d/p);od;
    if SortedList(List(classes,Size))<>SortedList(expected) then Print("FAILED_PARAMETERS ",m," ",d," ",k," GOT ",SortedList(List(classes,Size))," EXPECTED ",SortedList(expected)," FACTORS ",FactorsInt(m),"\n");Error("maximal cyclic classes");fi;
    for X in classes do
     K:=Intersection(X,A);
     if not IsSubgroup(X,A) and not IsPrimeInt(Index(A,K)) then Error("prime cyclic quotient");fi;
    od;
    count:=count+1;
   fi;
  od;
 od;od;
 Print("PASS_L115_PRELIMINARY_CONTROLS CYCLIC_ACTIONS ",count,"\n");
end;;
L115Controls();;QUIT;
