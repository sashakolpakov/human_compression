# Exact finite structural witnesses, using accepted literal images.
SetAssertionLevel(1);;
AtomSize:=function(a)
 if a[1]="cyclic" then return a[2];
 elif a[1]="elementary" then return a[2]^a[3];
 elif a[1]="special" then return a[2]^(a[3]+a[4]);
 elif a[1]="S" then return Factorial(a[2]);
 elif a[1]="A" then return Factorial(a[2])/2;
 elif a[1]="PSL" then return Size(PSL(a[2],a[3]));
 elif a[1]="PSU" then return Size(PSU(a[2],a[3]));
 elif a[1]="Q8" then return 8;
 fi;Error("unknown atom");
end;;
ShapeSize:=function(s)
 if s[1]="atom" then return AtomSize(s[2]);fi;
 return ShapeSize(s[2])*ShapeSize(s[3]);
end;;
AtomProof:=function(G,a) local z,d,f,iso,T,w;
 if Size(G)<>AtomSize(a) then return fail;fi;
 w:=rec(kind:="atom",order:=Size(G),description:=a,generators:=GeneratorsOfGroup(G));
 if a[1]="cyclic" then if not IsCyclic(G) then return fail;fi;w.exponent:=Exponent(G);
 elif a[1]="elementary" then if not IsElementaryAbelian(G) then return fail;fi;w.exponent:=Exponent(G);
 elif a[1]="special" then
  z:=Centre(G);d:=DerivedSubgroup(G);f:=FrattiniSubgroup(G);
  if not (z=d and d=f and Size(z)=a[2]^a[3] and IsElementaryAbelian(z) and IsElementaryAbelian(FactorGroup(G,z))) then return fail;fi;
  w.centre_generators:=GeneratorsOfGroup(z);w.derived_generators:=GeneratorsOfGroup(d);w.frattini_generators:=GeneratorsOfGroup(f);w.exponent:=Exponent(G);w.centre_order:=Size(z);w.central_quotient_order:=Index(G,z);
 elif a[1]="Q8" then
  if IsAbelian(G) or Number(Elements(G),x->Order(x)=2)<>1 then return fail;fi;w.element_order_histogram:=Collected(List(Elements(G),Order));
 else
  if a[1]="S" then T:=SymmetricGroup(a[2]);
  elif a[1]="A" then T:=AlternatingGroup(a[2]);
  elif a[1]="PSL" then T:=PSL(a[2],a[3]);
  elif a[1]="PSU" then T:=PSU(a[2],a[3]);
  else Error("unknown atom");fi;
  iso:=IsomorphismGroups(G,T);if iso=fail or not IsBijective(iso) then return fail;fi;
  w.target_generators:=GeneratorsOfGroup(T);w.isomorphism_images:=List(GeneratorsOfGroup(G),g->Image(iso,g));w.isomorphism_inverse_images:=List(GeneratorsOfGroup(T),g->PreImagesRepresentative(iso,g));
 fi;
 return w;
end;;
# If a target quotient has derived length at most d, its kernel contains G^(d).
DerivedBound:=function(s) local a,b;
 if s[1]="atom" then
  a:=s[2];if a[1] in ["cyclic","elementary"] then return 1;
  elif a[1] in ["special","Q8"] then return 2;
  elif a[1]="S" and a[2]<=4 then return a[2]-1;
  elif a[1]="A" and a[2]<=4 then return Maximum(1,a[2]-2);
  else return fail;fi;
 fi;
 a:=DerivedBound(s[2]);b:=DerivedBound(s[3]);if a=fail or b=fail then return fail;fi;
 if s[1]="direct" then return Maximum(a,b);else return a+b;fi;
end;;
TrivialRadicalShape:=function(s) local a;
 if s[1]="atom" then
  a:=s[2];return (a[1] in ["S","A"] and a[2]>=5) or (a[1]="PSL" and a[2]=2 and a[3]>=4) or (a[1]="PSU" and a[2]=3 and a[3]>=3);
 fi;
 return s[1]="direct" and TrivialRadicalShape(s[2]) and TrivialRadicalShape(s[3]);
end;;
NormalCandidates:=function(G,s) local b,D,j,f,Q,target,pp;
 target:=ShapeSize(s[2]);b:=DerivedBound(s[3]);pp:=PrimeDivisors(target);
 if Length(pp)=1 then
  D:=PCore(G,pp[1]);if Size(D)<target then return [];fi;
  if Size(D)=target then return [D];fi;
  return Filtered(NormalSubgroups(D),N->Size(N)=target and IsNormal(G,N));
 fi;
 if TrivialRadicalShape(s[3]) then
  D:=SolvableRadical(G);
  if Size(D)>1 then
   if target mod Size(D)<>0 then return [];fi;
   if Size(D)=target then return [D];fi;
   f:=NaturalHomomorphismByNormalSubgroup(G,D);Q:=Image(f);
   return List(Filtered(NormalSubgroups(Q),N->Size(N)*Size(D)=target),N->PreImage(f,N));
  fi;
 fi;
 if b<>fail then
  D:=G;for j in [1..b] do D:=DerivedSubgroup(D);od;
  if Size(D)>1 then
   if target mod Size(D)<>0 then return [];fi;
   f:=NaturalHomomorphismByNormalSubgroup(G,D);Q:=Image(f);
   return List(Filtered(NormalSubgroups(Q),N->Size(N)*Size(D)=target),N->PreImage(f,N));
  fi;
 fi;
 return Filtered(NormalSubgroups(G),N->Size(N)=target);
end;;
# Exact bounded complement searches for the only nonsolvable-kernel quotients used here.
SmallQuotientComplements:=function(G,N,s) local P,x,classes,y,T,H;
 if Index(G,N)=2 then
  P:=SylowSubgroup(G,2);x:=First(Elements(P),x->Order(x)=2 and not x in N);
  if x=fail then return [];else return [Subgroup(G,[x])];fi;
 fi;
 if s=["atom",["S",3]] then
  P:=SylowSubgroup(G,3);classes:=ConjugacyClasses(P);
  for y in List(classes,Representative) do
   if Order(y)=3 and not y in N then
    T:=Normalizer(G,Subgroup(G,[y]));P:=SylowSubgroup(T,2);
    x:=First(Elements(P),x->Order(x)=2 and y^x=y^-1 and not x in N);
    if x<>fail then H:=Subgroup(G,[x,y]);Assert(0,Size(H)=6);return [H];fi;
   fi;
  od;
  return [];
 fi;
 return ComplementClassesRepresentatives(G,N);
end;;
# Every success is a checked normal extension. Search failure is just a bounded candidate outcome until its hypotheses are separately read.
FindShape:=function(G,s) local normals,N,f,Q,l,r,cs,C,check,Z;
 if Size(G)<>ShapeSize(s) then return fail;fi;
 if s[1]="atom" then
  return AtomProof(G,s[2]);
 fi;
 normals:=NormalCandidates(G,s);
 for N in normals do
  Assert(0,IsNormal(G,N));f:=NaturalHomomorphismByNormalSubgroup(G,N);Q:=Image(f);Assert(0,Kernel(f)=N and Size(Q)*Size(N)=Size(G));
  r:=FindShape(Q,s[3]);
  if r<>fail then
   l:=FindShape(N,s[2]);
   if l<>fail then
    if s[1]="dot" then
     return rec(kind:="dot",order:=Size(G),kernel_generators:=GeneratorsOfGroup(N),quotient_images:=List(GeneratorsOfGroup(G),g->Image(f,g)),kernel:=l,quotient:=r);
    fi;
    if s[1]="direct" then
     C:=Centralizer(G,N);Z:=Centre(N);
     if Size(C)*Size(N)<>Size(G)*Size(Z) then cs:=[];
     elif Size(Z)=1 then cs:=[C];
     else cs:=ComplementClassesRepresentatives(C,Z);fi;
    else cs:=SmallQuotientComplements(G,N,s[3]);fi;
    for C in cs do
     if s[1]="colon" or (IsNormal(G,C) and ForAll(GeneratorsOfGroup(C),c->ForAll(GeneratorsOfGroup(N),n->c*n=n*c))) then
      Assert(0,Size(Intersection(N,C))=1 and Size(N)*Size(C)=Size(G));
      Assert(0,Size(ClosureGroup(N,C))=Size(G));
      return rec(kind:=s[1],order:=Size(G),kernel_generators:=GeneratorsOfGroup(N),complement_generators:=GeneratorsOfGroup(C),quotient_images:=List(GeneratorsOfGroup(G),g->Image(f,g)),intersection_order:=Size(Intersection(N,C)),kernel:=l,quotient:=r);
     fi;
    od;
   fi;
  fi;
 od;
 return fail;
end;;
