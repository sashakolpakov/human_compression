TestFusionWitnesses:=function()
 local groups,G,A,subs,families,p,q,w,oracle,old,tests,positive,negative,rank,H,model,corrupt,phi;
 groups:=[SymmetricGroup(3),Group((1,2),(3,4)),Group((1,2,3),(4,5,6)),Group((1,2,3,4),(2,4)),Group((1,2),(3,4),(5,6))];
 tests:=0;positive:=0;negative:=0;
 for G in groups do
  A:=AutomorphismGroup(G);
  subs:=Concatenation(List(ConjugacyClassesSubgroups(G),Elements));
  subs:=Filtered(subs,H->Size(H)>1 and H<>G);
  families:=Combinations(subs,2);
  if Length(families)>14 then families:=families{[1..14]};fi;
  if Length(subs)>=3 then Append(families,Combinations(subs,3){[1..Minimum(4,Binomial(Length(subs),3))]});fi;
  for p in families do for q in families do
   if Length(p)<>Length(q) then continue;fi;
   oracle:=ForAny(Elements(A),a->ForAny(Elements(SymmetricGroup(Length(p))),perm->List(p,H->Image(a,H))=Permuted(q,perm)));
   old:=EquivalentFamilies(A,p,q);w:=FindFamilyWitness(G,A,p,q);
   if old<>oracle or (w<>fail)<>oracle then Error("literal full-Aut/type oracle mismatch");fi;
   if w<>fail then
    if not CheckFamilyWitness(G,p,q,w) then Error("positive map invalid");fi;
    positive:=positive+1;
   else negative:=negative+1;fi;
   tests:=tests+1;
  od;od;
 od;
 G:=Group((1,2),(3,4));A:=AutomorphismGroup(G);p:=[Subgroup(G,[(1,2)]),Subgroup(G,[(3,4)])];
 w:=FindFamilyWitness(G,A,p,Reversed(p));
 if w=fail or not CheckFamilyWitness(G,p,Reversed(p),w) then Error("type exchange control");fi;
 corrupt:=rec(type_permutation:=w.type_permutation,generator_images:=[(),()]);
 if CheckFamilyWitness(G,p,Reversed(p),corrupt) then Error("damaged generator images accepted");fi;
 corrupt:=rec(type_permutation:=(1,2,3),generator_images:=w.generator_images);
 if CheckFamilyWitness(G,p,Reversed(p),corrupt) then Error("wrong palette permutation accepted");fi;
 # A second literal action is compared only after an explicit conjugating map.
 model:=(1,7)(2,8)(3,9)(4,10);H:=G^model;
 if H=G then Error("relabel fixture unchanged");fi;
 phi:=ConjugatorIsomorphism(G,model);
 if not IsBijective(phi) or List(p,P->Image(phi,P))<>List(p,P->P^model) then Error("explicit model transport");fi;
 if ForAll(GeneratorsOfGroup(H),x->x in G) then Error("untransported model not detected");fi;
 Print("PASS_FUSION_WITNESSES tests=",tests," positive=",positive," negative=",negative," damaged=2 relabel=1\n");
end;
TestFusionWitnesses();;
