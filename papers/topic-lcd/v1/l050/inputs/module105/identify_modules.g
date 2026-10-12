# Exact group identification and all19-factor maps into the permutation module.
F:=GF(3);;
pgens:=List(coordinate_generators,PermList);;G:=Group(pgens);;
if Size(G)<>241920 then Error("group order");fi;
N:=PerfectResiduum(G);;
if Size(N)<>20160 or not IsNormal(G,N) or IsomorphismGroups(N,PSL(3,4))=fail then Error("simple normal subgroup");fi;
outer:=List(complement_generators,PermList);;Q:=Group(outer);;
if not IsSubgroup(G,Q) or Size(Q)<>12 or Size(Intersection(N,Q))<>1 or
 IsomorphismGroups(Q,DihedralGroup(12))=fail or ClosureGroup(N,Q)<>G then Error("outer semidirect complement");fi;
index2:=ClosureGroup(N,Group(outer{[1,2]}));;
if Size(index2)<>120960 or not IsNormal(G,index2) then Error("nontrivial linear character kernel");fi;
if not IsTransitive(G,[1..105]) or Length(Orbits(Stabilizer(G,1),[1..105]))<>4 then Error("source rank4 action");fi;
M:=List(pgens,g->PermutationMat(g,105,F));;
D:=D_basis*One(F);;
HomImages:=function(S)
 local d,n,eqs,z,inv,i,j,k,r,solutions,X,solution;
 d:=19;n:=105;eqs:=[];
 for z in [1..Length(pgens)] do
  inv:=pgens[z]^-1;
  for i in [1..d] do for j in [1..n] do
   r:=ListWithIdenticalEntries(d*n,Zero(F));
   r[(i-1)*n+j^inv]:=One(F);
   for k in [1..d] do r[(k-1)*n+j]:=r[(k-1)*n+j]-S[z][i][k];od;
   ConvertToVectorRep(r,3);Add(eqs,r);
  od;od;
 od;
 solutions:=NullspaceMat(TransposedMat(eqs));;
 if Length(solutions)<>d*n-RankMat(eqs) then Error("complete Hom nullspace");fi;
 for solution in solutions do
  X:=List([1..d],i->solution{[(i-1)*n+1..i*n]});
  if not ForAll([1..Length(pgens)],z->X*M[z]=S[z]*X) then Error("Hom equations");fi;
  if RankMat(Concatenation(D,X))<>19 then Error("19dimensional image outside D");fi;
 od;
 return Length(solutions);
end;;
homs:=List(nineteen_factors,S->HomImages(List(S,T->T*One(F))));;
Print("HOM dimensions ",homs,"\n");
if homs<>[0,1,1] then Error("unexpected Hom dimensions");fi;
s:=OutputTextFile("module_identification.json",false);;SetPrintFormattingStatus(s,false);;
PrintTo(s,"{\"status\":\"PASS\",\"group_order\":241920,\"normal_simple_group\":\"PSL(3,4)\",\"normal_order\":20160,\"complement\":\"D12\",\"complement_order\":12,\"rank\":4,\"index2_normal_order\":120960,\"all19factor_Hom_dimensions\":",homs,",\"all19factor_images_in_D\":true}\n");
CloseStream(s);;
Print("LCD105_MODULES_PASS\n");
