# Independent local diagnostics for the class-four support proof.
# This is not the author checker and does not assert an all-rank conclusion
# from these finite cases. GAP with the NQ package is required.
if LoadPackage("nq") = fail then Error("NQ is required"); fi;
SizeScreen([240,24]);;

AuditPath := function(rank)
 local F, fr, relations, i, j, G, r, c, z, t, p, s, q, h,
       gamma2, gamma3, gamma4, one, expected, comparisons, value;
 F := FreeGroup(rank);
 fr := GeneratorsOfGroup(F);
 relations := List(fr, x -> x^2);
 for i in [1..rank] do
  for j in [i+1..rank] do
   if j-i > 1 then Add(relations, Comm(fr[i],fr[j])); fi;
  od;
 od;
 G := NilpotentQuotient(F / relations, 4);
 r := GeneratorsOfGroup(G){[1..rank]};
 one := One(G);
 c := List([1..rank-1], i -> Comm(r[i],r[i+1]));
 z := List(c, x -> x^2);
 t := List([1..rank-2], i -> Comm(c[i],r[i+2]));
 p := List(c, x -> x^4);
 s := List(t, x -> x^2);
 q := List([1..rank-2], i -> Comm(c[i],c[i+1]));
 h := List([1..rank-3], i -> Comm(t[i],r[i+3]));
 gamma2 := DerivedSubgroup(G);
 gamma3 := CommutatorSubgroup(gamma2,G);
 gamma4 := CommutatorSubgroup(gamma3,G);
 if not IsAbelian(gamma3) then Error("gamma3 abelian"); fi;
 if not IsElementaryAbelian(gamma4) then Error("gamma4 elementary abelian"); fi;
 if Subgroup(G,Concatenation(p,s,q,h)) <> gamma4 then Error("gamma4 generation"); fi;
 if ClosureGroup(Subgroup(G,Concatenation(z,t)),gamma4) <> gamma3 then
  Error("gamma3 generation");
 fi;
 comparisons := 0;
 for i in [1..Length(z)] do
  for j in [1..rank] do
   expected := one;
   if j = i-1 then expected := s[i-1]; fi;
   if j = i or j = i+1 then expected := p[i]; fi;
   if j = i+2 then expected := s[i]; fi;
   if Comm(z[i],r[j]) <> expected then Error("z collection"); fi;
   comparisons := comparisons+1;
  od;
 od;
 for i in [1..Length(t)] do
  for j in [1..rank] do
   expected := one;
   if j = i-1 then expected := h[i-1]; fi;
   if j = i or j = i+2 then expected := s[i]; fi;
   if j = i+1 then expected := q[i]*s[i]; fi;
   if j = i+3 then expected := h[i]; fi;
   if Comm(t[i],r[j]) <> expected then Error("t collection"); fi;
   comparisons := comparisons+1;
  od;
 od;
 for i in [1..rank-2] do
  # The direct triple derivation used in the prose, including its sign.
  value := Comm(c[i]^-1,r[i+2]*c[i+1]^-1);
  if value <> q[i]*t[i]^-1 or t[i]^r[i+1] <> value then
   Error("middle-conjugation identity");
  fi;
  comparisons := comparisons+1;
 od;
 for i in [2..rank-2] do
  # The four-vertex Jacobi swap whose sign vanishes in gamma4.
  if Comm(t[i],r[i-1]) <> Comm(Comm(c[i-1],r[i+1]),r[i+2]) then
   Error("left four-vertex identity");
  fi;
  comparisons := comparisons+1;
 od;
 Print("rank=",rank," order=",Size(G)," gamma3_order=",Size(gamma3),
       " gamma4_order=",Size(gamma4)," exact_comparisons=",comparisons," PASS\n");
 return comparisons;
end;

Print("GAP=",GAPInfo.Version," NQ=",PackageInfo("nq")[1].Version,"\n");
total := Sum(List([2..6],AuditPath));;
Print("total_exact_comparisons=",total,"\n");
Print("PASS: bounded independent local diagnostics only; uniform proof reviewed separately.\n");
QUIT;
