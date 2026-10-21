# Original bounded diagnostics for the fixed-excess support theorem.
# Finite examples only; the uniform proof does not depend on these checks.
if LoadPackage("nq")=fail then Error("NQ required");fi;
SizeScreen([100000,24]);;

CheckExample16:=function(d,triples,edges)
 local F,f,rel,i,j,G,r,sets,groups,K,k,J,I,H,expected,meets,a,e,b,
       Ni,D,prodset,overlap,coreorder,components,iso;
 F:=FreeGroup(d);f:=GeneratorsOfGroup(F);
 rel:=List(f,x->x^2);
 for i in [1..d] do for j in [i+1..d] do
  if j-i>1 then Add(rel,Comm(f[i],f[j]));fi;
 od;od;
 for i in [1..d-1] do
  if not i in edges then Add(rel,(f[i]*f[i+1])^4);fi;
 od;
 for i in [1..d-2] do
  if not i in triples then Add(rel,Comm(Comm(f[i],f[i+1]),f[i+2]));fi;
 od;
 G:=NilpotentQuotient(F/rel,3);r:=GeneratorsOfGroup(G){[1..d]};
 iso:=IsomorphismPcGroup(G);r:=List(r,x->Image(iso,x));G:=Image(iso);
 K:=CommutatorSubgroup(DerivedSubgroup(G),G);k:=LogInt(Size(K),2);
 expected:=2^(2*d-1+Length(triples)+Length(edges));
 if Size(G)<>expected or Size(K)<>2^(Length(triples)+Length(edges)) then
  Error("Unexpected example size");fi;
 sets:=Combinations([1..d]);groups:=List(sets,A->Subgroup(G,r{A}));
 meets:=0;
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  if Intersection(groups[i],groups[j])<>groups[Position(sets,Intersection(sets[i],sets[j]))] then
   Error("Actual IP");fi;
  meets:=meets+1;
 od;od;
 J:=[1..d];
 for i in [1..Length(sets)] do
  if IsSubgroup(groups[i],K) then J:=Intersection(J,sets[i]);fi;
  if Intersection(K,groups[i])<>CommutatorSubgroup(DerivedSubgroup(groups[i]),groups[i]) then
   Error("Canonical kernel restriction");fi;
 od;
 I:=Filtered([1..d],v->ForAny(J,w->AbsInt(v-w)<=1));
 H:=Subgroup(G,r{I});
 components:=Number(J,v->not v-1 in J);
 if Length(J)>3*k or components>k or Length(I)>5*k then Error("Support bound");fi;
 if k>0 and Size(H)>2^(11*k-1) then Error("Core order bound");fi;
 if CommutatorSubgroup(DerivedSubgroup(H),H)<>K then Error("Core kernel");fi;
 D:=List([1..d-1],v->Subgroup(G,[(r[v]*r[v+1])^4]));
 a:=List(D,L->LogInt(Size(L),2));
 Ni:=List([1..d-2],v->CommutatorSubgroup(DerivedSubgroup(Subgroup(G,r{[v..v+2]})),Subgroup(G,r{[v..v+2]})));
 e:=List(Ni,L->LogInt(Size(L),2));
 b:=List([1..d-2],v->e[v]-a[v]-a[v+1]);
 if ForAny(b,v->v<0) or Sum(a)+Sum(b)>k then Error("Local budget");fi;
 prodset:=[One(G)];
 for i in [1..Length(Ni)] do
  prodset:=Set(Concatenation(List(prodset,x->List(Elements(Ni[i]),y->x*y))));
 od;
 if Length(prodset)<>2^(Sum(a)+Sum(b)) then Error("Exact product cardinality");fi;
 Print("PASS rank=",d," order=",Size(G)," k=",k," triple_seeds=",triples," edge_seeds=",edges,
  " support=",J," components=",components," neighborhood=",I," core_order=",Size(H),
  " edge_excess=",a," intrinsic_triple_excess=",b," local_product_order=",Length(prodset),
  " full_subset_meets=",meets," kernel_restrictions=",Length(sets),"\n");
 return meets;
end;;
Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");;
total:=0;;
for case16 in [[3,[1],[]],[5,[2],[]],[6,[1,4],[]],[7,[1,5],[]],[5,[],[3]],[5,[],[]]] do
 total:=total+CallFuncList(CheckExample16,case16);
od;
Print("PASS total_full_subset_meets=",total,"; six exact examples only.\n");
QUIT;
