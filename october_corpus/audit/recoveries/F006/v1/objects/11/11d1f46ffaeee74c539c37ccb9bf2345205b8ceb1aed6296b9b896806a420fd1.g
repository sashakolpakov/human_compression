# Exact finite catalogue input for the written primitive-rank bound.
# This uses the GAP primitive-groups catalogue and complete maximal-subgroup
# algorithms. It does NOT search for C-group markings.
SetInfoLevel(InfoWarning,0);;
Need:=function(b,s) if not b then Error(s); fi; end;;
PrimeLength:=n->Length(FactorsInt(n));;
PrimitiveExceptions:=[];; total:=0;;
for n in [9..25] do
 for k in [1..NrPrimitiveGroups(n)] do
  g:=PrimitiveGroup(n,k);; total:=total+1;;
  if Size(g)<Factorial(n)/2 and PrimeLength(Size(g))>n-4 then
   Add(PrimitiveExceptions,[n,k,Size(g),PrimeLength(Size(g))]);
  fi;
 od;
od;
expected:=[[9,5,144,6],[9,6,216,6],[9,7,432,7],[9,8,504,6],
[9,9,1512,7],[10,4,720,7],[10,5,720,7],[10,6,720,7],
[10,7,1440,8],[11,6,7920,8],[12,2,95040,11],[16,11,322560,14]];;
Need(PrimitiveExceptions=expected,"primitive exception list changed");;
Print("PRIMITIVE_CATALOGUE ",total," ",PrimitiveExceptions,"\n");
for k in [5,6,7] do
 g:=PrimitiveGroup(9,k);; v:=Socle(g);;
 Need(Size(v)=9 and IsElementaryAbelian(v),"affine9 socle");
 q:=FactorGroup(g,v);;
 if k=7 then
  f:=FrattiniSubgroup(q);;
  Need(Size(f)=2,"GL2(3) Frattini order");
  Need(IsomorphismGroups(FactorGroup(q,f),SymmetricGroup(4))<>fail,"Frattini quotient S4");
  bound:=4; # mu(q)=mu(S4)<=3, then translation contribution1
 else bound:=PrimeLength(Size(q))+1; fi;
 Need(bound<=5,"affine9 bound");
 Print("AFFINE9 ",k," quotient=",Size(q)," bound=",bound,"\n");
od;
g:=PrimitiveGroup(9,9);; inv:=Filtered(AsList(g),x->Order(x)=2);;
Need(Size(Group(inv))=504,"odd extension involutions");;
Print("ODD_EXTENSION_INVOLUTION_SUBGROUP 504\n");
for k in [4,6,7] do
 g:=PrimitiveGroup(10,k);; s:=Socle(g);;
 Need(IsomorphismGroups(s,AlternatingGroup(6))<>fail,"degree10 A6 socle");
 Need(Index(g,s) in [2,4],"degree10 quotient");
 Print("DEGREE10 ",k," A6 quotient=",Index(g,s)," bound=",4+PrimeLength(Index(g,s)),"\n");
od;
Need(IsomorphismGroups(PrimitiveGroup(10,5),SymmetricGroup(6))<>fail,"degree10 S6");;
g:=PrimitiveGroup(16,11);; v:=Socle(g);;
Need(Size(v)=16 and IsElementaryAbelian(v),"affine16 socle");;
Need(IsomorphismGroups(FactorGroup(g,v),AlternatingGroup(8))<>fail,"affine16 A8");;
Print("AFFINE16_BOUND 7\n");
for nk in [[9,8],[11,6],[12,2]] do
 g:=PrimitiveGroup(nk[1],nk[2]);; maxs:=MaximalSubgroupClassReps(g);;
 if nk=[9,8] then
  Need(ForAll(maxs,h->PrimeLength(Size(h))<=4),"PSL2(8) maximal bound");
  Print("PSL28_MAXIMAL_ORDERS ",SortedList(List(maxs,Size))," bound=5\n");
 elif nk=[11,6] then
  for h in maxs do
   inv:=Filtered(AsList(h),x->Order(x)=2);;
   j:=Group(inv);;
   Need(PrimeLength(Size(j))<=6,"M11 involution generated maximal bound");
  od;
  Print("M11_MAXIMAL_ORDERS ",SortedList(List(maxs,Size))," bound=7\n");
 else
  for h in maxs do
   if Size(h)=7920 then
    Need(IsomorphismGroups(h,PrimitiveGroup(11,6))<>fail,"M12 M11 maximal");
   elif Size(h)=1440 then
    s:=Socle(h);;
    Need(IsomorphismGroups(s,AlternatingGroup(6))<>fail and Index(h,s)=4,"M12 A6 quotient maximal");
   else Need(PrimeLength(Size(h))<=7,"M12 remaining maximal bound");fi;
  od;
  Print("M12_MAXIMAL_ORDERS ",SortedList(List(maxs,Size))," bound=8\n");
 fi;
od;
# The finite numerical part of the Maroti envelope, before the analytic
# power-of-two argument valid from degree64 onwards.
for n in [26..63] do
 k:=LogInt(n,2);; b:=n*Product([0..k-1],i->n-2^i);;
 Need(b<2^(n-3),"integer primitive chain envelope");
od;
Print("MAROTI_INTEGER_ENVELOPE 26..63 PASS\n");
Print("PASS exact finite primitive inputs; no marking enumeration\n");
# The stronger independent-family input needed for primitive block stabilizers.
# The single exception to mu'(L)<=degree-3 is the natural degree6 copy of S5.
independentExceptions:=[];;
for n in [5..25] do
 for k in [1..NrPrimitiveGroups(n)] do
  g:=PrimitiveGroup(n,k);;
  if Size(g)<Factorial(n)/2 and PrimeLength(Size(g))>n-3 then
   Add(independentExceptions,[n,k,Size(g)]);
  fi;
 od;
od;
Need(independentExceptions=[[5,3,20],[6,1,60],[6,2,120],[7,5,168],
[8,3,1344],[8,5,336],[9,7,432],[9,9,1512],[10,7,1440],
[12,2,95040],[16,11,322560]],"independent primitive exception list");;
Print("INDEPENDENT_PRIMITIVE_EXCEPTIONS ",independentExceptions,"\n");
g:=PrimitiveGroup(5,3);;v:=Socle(g);;
Need(Size(v)=5 and IsCyclic(FactorGroup(g,v)),"F20 cyclic quotient");;
Need(IsomorphismGroups(PrimitiveGroup(6,1),AlternatingGroup(5))<>fail,"degree6 A5");;
Need(IsomorphismGroups(PrimitiveGroup(6,2),SymmetricGroup(5))<>fail,"degree6 S5");;
g:=PrimitiveGroup(7,5);;
for h in MaximalSubgroupClassReps(g) do
 Need(PrimeLength(Size(h))<=2 or IsomorphismGroups(h,SymmetricGroup(4))<>fail,"PSL32 maximal bound");
od;
g:=PrimitiveGroup(8,3);;v:=Socle(g);;
Need(Size(v)=8 and IsElementaryAbelian(v),"AGL32 translation");;
Need(IsomorphismGroups(FactorGroup(g,v),PrimitiveGroup(7,5))<>fail,"AGL32 linear quotient");;
g:=PrimitiveGroup(8,5);;s:=Socle(g);;
Need(Index(g,s)=2 and IsomorphismGroups(s,PrimitiveGroup(7,5))<>fail,"PGL27 socle");;
g:=PrimitiveGroup(9,7);;q:=FactorGroup(g,Socle(g));;
Need(ForAll(MaximalSubgroupClassReps(q),h->PrimeLength(Size(h))<=4),"GL23 proper subgroup bound");;
g:=PrimitiveGroup(9,9);;s:=Socle(g);;
Need(Index(g,s)=3 and IsomorphismGroups(s,PrimitiveGroup(9,8))<>fail,"PGL28 field extension");;
g:=PrimitiveGroup(12,2);;
Need(ForAll(MaximalSubgroupClassReps(g),h->PrimeLength(Size(h))<=8),"M12 independent bound9");;
Print("PASS primitive block-stabilizer identifications and independent bounds\n");

QUIT;
