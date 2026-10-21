# Private exact shadow-property pilot. The supplied parabolic permutations
# are primary mathematical data, parsed separately without executing Magma.
SizeScreen([100000,100000]);;
Read("ambient.g");;Read("sz8_rows.g");;
L096Rows:=List(L096Sz8Triples,t->[L096Sz8Involutions{t{[2,3]}},L096Sz8Involutions{t{[1,3]}},L096Sz8Involutions{t{[1,2]}}]);;
L096ActCache:=[];;

L096ShadowTest:=function(row,number)
 local G,H,n,sets,HG,acts,base,sh,i,T,C,phi,pt,expected,proofs,
 j,K,dc,h,inter,a,sx,sf,inc,U,q,good,allgood,witness,flagcount,
 tested,failures,geomok,allrank,record,ci,transport;
 G:=Group(Concatenation(row));n:=Length(row);
 if Size(G)<>29120 or not IsSimpleGroup(G) then Error("incorrect Sz8 input group");fi;
 H:=List(row,gens->Subgroup(G,gens));
 sets:=Combinations([1..n]);
 HG:=List(sets,T->Intersection(Concatenation([G],H{T})));
 acts:=[];base:=[];sh:=[];
 for i in [1..n] do
  ci:=1;transport:=fail;
  while ci<=Length(L096ActCache) do
   if Size(H[i])=Size(L096ActCache[ci].H) then
    transport:=RepresentativeAction(G,L096ActCache[ci].H,H[i]);
    if transport<>fail then break;fi;
   fi;
   ci:=ci+1;
  od;
  if transport=fail then
   C:=RightCosets(G,H[i]);phi:=ActionHomomorphism(G,C,OnRight);
   pt:=Position(C,RightCoset(H[i],One(G)));
   Add(L096ActCache,rec(H:=H[i],phi:=phi,pt:=pt));
  else
   phi:=L096ActCache[ci].phi;
   pt:=L096ActCache[ci].pt^Image(phi,transport);
   if Stabilizer(G,pt,function(x,g) return x^Image(phi,g);end)<>H[i] then Error("wrong cached stabilizer");fi;
  fi;
  Add(acts,phi);Add(base,pt);
  Add(sh,List(HG,A->Set(Orbit(Image(phi,A),pt))));
 od;
 # Full flag transitivity is checked from actual shadow intersections.
 # The induction starts at the empty flag. At each type extension, the
 # entire eligible coset set must be the chamber-stabilizer orbit.
 geomok:=true;flagcount:=0;
 for i in [1..n] do
  for T in [1..Length(sets)] do
   if not i in sets[T] then
    expected:=[1..Index(G,H[i])];
    for j in sets[T] do
     expected:=Intersection(expected,sh[i][Position(sets,[j])]);
    od;
    if expected<>sh[i][T] then geomok:=false;fi;
    flagcount:=flagcount+1;
   fi;
  od;
 od;
 if not geomok then Error("flag transitivity fails for source input");fi;
 allgood:=[];tested:=0;failures:=[];
 for i in [1..n] do
  good:=true;
  for j in Difference([1..n],[i]) do
   K:=Intersection(H[i],H[j]);sx:=sh[i][Position(sets,[j])];
   for T in [1..Length(sets)] do
    if Length(sets[T])=0 or i in sets[T] then continue;fi;
    for dc in DoubleCosets(H[i],Intersection(H[i],HG[T]),K) do
     h:=Representative(dc);sf:=OnSets(sh[i][T],Image(acts[i],h));
     inter:=Intersection(sx,sf);a:=Length(inter);tested:=tested+1;
     if a<=1 then continue;fi;
     inc:=base[j] in OnSets(sh[j][T],Image(acts[j],h));
     if a=Minimum(Length(sx),Length(sf)) and inc then continue;fi;
     witness:=false;
     for U in [1..Length(sets)] do
      if i in sets[U] or Length(sh[i][U])<>a then continue;fi;
      for q in RightTransversal(K,Intersection(K,HG[U])) do
       if OnSets(sh[i][U],Image(acts[i],q))<>inter then continue;fi;
       if ForAll(sets[U],u->base[u]^Image(acts[u],q) in
                    OnSets(sh[u][T],Image(acts[u],h))) then
        witness:=true;break;
       fi;
      od;
      if witness then break;fi;
     od;
     if not witness then
      good:=false;Add(failures,[i,j,sets[T],a]);break;
     fi;
    od;
    if not good then break;fi;
   od;
   if not good then break;fi;
  od;
  Add(allgood,good);
 od;
 record:=rec(row:=number,order:=Size(G),parabolics:=List(H,Size),
  full_flag_extensions:=flagcount,IP3:=ForAll(allgood,x->x),
  WIP3:=ForAny(allgood,x->x),type_results:=allgood,orbit_tests:=tested,
  negative_witnesses:=failures);
 Print("GEOMETRY|",record,"\n");return record;
end;;
L096Results:=List([1..Length(L096Rows)],i->L096ShadowTest(L096Rows[i],i));;
L096Counts:=[Number(L096Results,r->r.IP3),Number(L096Results,r->r.WIP3 and not r.IP3),Number(L096Results,r->not r.WIP3)];;
Print("AGGREGATE|",L096Counts,"\n");
if L096Counts<>[27,48,72] then Error("aggregate differs from source Section5 Sz8");fi;
PrintTo("sz8_shadow_results.g","L096Sz8ShadowResults:=",L096Results,";;\n");
Print("PASS_SZ8_RANK3_SHADOWS\n");QUIT;
