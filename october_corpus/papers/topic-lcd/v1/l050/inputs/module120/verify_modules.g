# Exact certificate; read constructed.g first. MeatAxe was discovery only.
F:=GF(3);;
pgens:=List(group_generators,PermList);;
G:=Group(pgens);;A:=Group(List(full_generators,PermList));;
if Size(A)<>80640 or Size(G)<>20160 or DerivedSubgroup(A)<>G then Error("group orders");fi;
if IsomorphismGroups(G,PSL(3,4))=fail then Error("specified simple group");fi;
if not IsPrimitive(G,[1..120]) or not IsTransitive(G,[1..120]) or Size(Stabilizer(G,1))<>168 or IsomorphismGroups(Stabilizer(G,1),PSL(3,2))=fail then Error("source coset action");fi;
complement:=Group(List(outer_complement,PermList));;
if Size(complement)<>4 or not IsElementaryAbelian(complement) or Size(Intersection(G,complement))<>1 or Group(Concatenation(pgens,GeneratorsOfGroup(complement)))<>A then Error("outer complement");fi;
K:=K_basis*One(F);;N:=N_basis*One(F);;
if RankMat(K)<>15 or RankMat(N)<>16 then Error("code ranks");fi;
if not IsZero(K*TransposedMat(K)) or not IsZero(N*TransposedMat(N)) then Error("orthogonality");fi;
for g in GeneratorsOfGroup(A) do
 if RankMat(Concatenation(K,List(K,v->Permuted(v,g))))<>15 or RankMat(Concatenation(N,List(N,v->Permuted(v,g))))<>16 then Error("full group invariance");fi;
od;
# Triangularity and full matrix algebras certify the supplied composition series.
basis_matrix:=filtration_basis*One(F);;
if Length(basis_matrix)<>120 or RankMat(basis_matrix)<>120 then Error("filtration basis");fi;
cuts:=filtration_cuts;;
if cuts<>[0,15,34,49,64,65,84,99,100,119,120] then Error("filtration dimensions");fi;
if RankMat(Concatenation(basis_matrix{[1..15]},K))<>15 then Error("first simple submodule is not K");fi;
mats:=List(pgens,g->PermutationMat(g,120,F));;
changed:=List(mats,g->basis_matrix*g*basis_matrix^-1);;
for c in cuts{[2..Length(cuts)-1]} do for T in changed do
 if not ForAll([1..c],i->ForAll([c+1..120],j->IsZero(T[i][j]))) then Error("noninvariant filtration");fi;
od;od;
# Solve X P_g = D_g X. Every simple-factor homomorphism has image in N.
HomCertificate:=function(D)
 local d,n,eqs,z,inv,i,j,k,r,solutions,sol,X;
 d:=Length(D[1]);n:=120;eqs:=[];
 for z in [1..Length(pgens)] do
  inv:=pgens[z]^-1;
  for i in [1..d] do for j in [1..n] do
   r:=ListWithIdenticalEntries(d*n,Zero(F));
   r[(i-1)*n+j^inv]:=One(F);
   for k in [1..d] do r[(k-1)*n+j]:=r[(k-1)*n+j]-D[z][i][k];od;
   ConvertToVectorRep(r,3);Add(eqs,r);
  od;od;
 od;
 solutions:=NullspaceMat(TransposedMat(eqs));
 if Length(solutions)<>d*n-RankMat(eqs) then Error("complete Hom basis");fi;
 for sol in solutions do
  X:=List([1..d],i->sol{[(i-1)*n+1..i*n]});
  if not ForAll([1..Length(pgens)],z->X*mats[z]=D[z]*X) then Error("intertwiner equation");fi;
  if RankMat(Concatenation(N,X))<>16 then Error("simple image outside N");fi;
 od;
 return Length(solutions);
end;;
factor_dimensions:=[];;hom_dimensions:=[];;algebra_dimensions:=[];;inds:=[];;
for i in [1..Length(cuts)-1] do
 inds:=[cuts[i]+1..cuts[i+1]];;d:=Length(inds);;
 D:=List(changed,T->List(inds,j->T[j]{inds}));;
 algdim:=Dimension(AlgebraWithOne(F,D));;
 if algdim<>d^2 then Error("factor not certified absolutely irreducible");fi;
 hd:=HomCertificate(D);;
 Add(factor_dimensions,d);Add(hom_dimensions,hd);Add(algebra_dimensions,algdim);
 Print("factor ",i," dimension ",d," algebra ",algdim," Hom-to-M ",hd,"\n");
od;
seed:=minimum_seed;;
if Number(seed,x->x<>0)<>48 or RankMat(Concatenation(K,[seed*One(F)]))<>15 then Error("minimum seed");fi;
minimum_orbit:=Orbit(G,seed,Permuted);;
supports:=Set(List(minimum_orbit,v->PositionsProperty(v,x->x<>0)));;
if Length(minimum_orbit)<>1260 or Length(supports)<>630 then Error("minimum orbit");fi;
if not ForAll(minimum_orbit,v->Number(v,x->x<>0)=48) then Error("orbit weight");fi;
output_stream:=OutputTextFile("support_data.json",false);;SetPrintFormattingStatus(output_stream,false);;
PrintTo(output_stream,"{\"supports\":",supports,",\"coordinate_generators\":",full_generators,"}\n");
CloseStream(output_stream);;
output_stream:=OutputTextFile("module_report.json",false);;SetPrintFormattingStatus(output_stream,false);;
PrintTo(output_stream,"{\"status\":\"PASS\",\"group_order\":20160,\"coset_stabilizer_order\":168,\"full_code_subgroup_order\":80640,\"K_dimension\":15,\"N_dimension\":16,\"factor_dimensions\":",factor_dimensions,",\"factor_algebra_dimensions\":",algebra_dimensions,",\"Hom_dimensions\":",hom_dimensions,",\"all_simple_images_in_N\":true,\"minimum_orbit\":1260,\"minimum_supports\":630}\n");
CloseStream(output_stream);;
Print("LCD120_MODULE_CERTIFICATE_PASS\n");
