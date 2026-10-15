Read("/Users/sasha/medusa/research/leemans/topic_D_L096_HS_extension/archive_data/inputs.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/clean_run01/result.g");;
Read("/Users/sasha/medusa/research/leemans/reboot_20261013/L091_work/pair_witnesses.g");;
RunCosetOracle:=function()
 local G,cache,i,r,A,B,H,j,rt,hom,base,P,N,a,M,c,w,phi,p,q,target;
 G:=Group(Concatenation(L096Inputs[1].parabolic_generators));cache:=[];
 for i in [1..Length(HSRankTwoResult.pairs)] do
  r:=HSRankTwoResult.pairs[i];A:=Subgroup(G,r.A);B:=Subgroup(G,r.B);H:=Subgroup(G,r.H);
  if Intersection(A,B)<>H or [Size(A),Size(B),Size(H)]<>r.orders then Error("Actual subgroup mismatch");fi;
  j:=PositionProperty(cache,x->x.A=A);
  if j=fail then
   rt:=RightTransversal(G,A);hom:=ActionHomomorphism(G,rt,OnRight);base:=Position(rt,One(G));
   Add(cache,rec(A:=A,hom:=hom,base:=base));j:=Length(cache);
  fi;
  hom:=cache[j].hom;base:=cache[j].base;P:=Image(hom,B);N:=Set(Orbit(P,base));
  if Length(N)<>r.degrees[2] or not IsTransitive(Stabilizer(P,base),Difference(N,[base])) then Error("Independent local action mismatch");fi;
  a:=First(RightTransversal(A,H),x->not x in H);M:=OnSets(N,Image(hom,a));
  c:=Length(Intersection(N,M));
  if c<>r.common or (c=1 or Length(N)=Index(G,A))<>r.IP2 then Error("Independent incidence mismatch");fi;
  Print("ORACLE_PAIR ",i," COSSET_DEGREE ",Index(G,A)," NEIGHBOURS ",Length(N)," COMMON ",c,"\n");
 od;
 for w in HSRankTwoWitnesses do
  phi:=GroupHomomorphismByImages(G,G,GeneratorsOfGroup(G),w.generator_images);
  if phi=fail or not IsBijective(phi) then Error("Recorded map is not an automorphism");fi;
  r:=HSRankTwoResult.pairs[w.source_pair];p:=List([r.A,r.B],x->Subgroup(G,x));
  r:=HSRankTwoResult.pairs[w.target_pair];q:=List([r.A,r.B],x->Subgroup(G,x));target:=Permuted(q,w.type_permutation);
  if List(p,H->Image(phi,H))<>target then Error("Recorded automorphism does not identify both parabolics");fi;
  Print("ORACLE_WITNESS ",w.source_pair," ",w.target_pair,"\n");
 od;
 Print("PASS_COSET_ORACLE ",Length(HSRankTwoResult.pairs)," ",Length(HSRankTwoWitnesses),"\n");
end;;
RunCosetOracle();
QUIT;
