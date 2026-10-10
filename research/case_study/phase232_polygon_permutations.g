# Independent faithful permutation model on Omega x F2.
# No author diagnostic code or semidirect-product implementation is imported.
Point := function(i,e,n) return 2*(i mod n)+e+1; end;
Marking := function(n,bad)
  local r,j,i,e,k,t,images;
  r:=[];
  for j in [0..2] do
    images:=[];
    for i in [0..n-1] do
      for e in [0..1] do
        if j=1 then k:=(-i) mod n; else k:=(1-i) mod n; fi;
        t:=0;
        if j=2 then
          if bad then
            if k in [0,2] then t:=1; fi;
          elif k in [0,1] then t:=1;
          fi;
        fi;
        Add(images,Point(k,(e+t) mod 2,n));
      od;
    od;
    Add(r,PermList(images));
  od;
  return r;
end;
CheckMarking := function(n,r)
  local G,subsets,parabolics,I,J,k,T,duality;
  if not ForAll(r,g->Order(g)=2) then return false; fi;
  if Order(r[1]*r[2])<>n or Order(r[2]*r[3])<>n then return false; fi;
  if Order(r[1]*r[3])<>2 then return false; fi;
  G:=Group(r);
  if Size(G)<>n*2^n then return false; fi;
  subsets:=Combinations([1..3]);
  parabolics:=List(subsets,I->Group(Concatenation([()],r{I})));
  for I in [1..8] do
    for J in [1..8] do
      k:=Position(subsets,Intersection(subsets[I],subsets[J]));
      if Intersection(parabolics[I],parabolics[J])<>parabolics[k] then return false; fi;
    od;
  od;
  for k in [1..n-1] do
    if ((r[2]*r[3])^k*(r[1]*r[2])^k)^2<>() then return false; fi;
  od;
  duality:=(1,2);
  if r[1]^duality<>r[3] or r[2]^duality<>r[2] or r[3]^duality<>r[1] then return false; fi;
  Print("n=",n," order=",Size(G)," intersections=64 full_relators=",n-1," duality=PASS\n");
  return true;
end;
for n in [3,4,5,6,7,8,11,13] do
  if not CheckMarking(n,Marking(n,false)) then Error("marking failed at n=",n); fi;
od;
if CheckMarking(3,Marking(3,true)) then Error("altered marker was not rejected"); fi;
Print("altered_translation_rejected=PASS\n");
# The exceptional n=2 case uses three independent involutions.
r:=[(1,2),(3,4),(5,6)];;
G:=Group(r);;
if Size(G)<>8 or Order(r[1]*r[2])<>2 or Order(r[2]*r[3])<>2 then Error("n2 case"); fi;
subsets:=Combinations([1..3]);;
parabolics:=List(subsets,I->Group(Concatenation([()],r{I})));;
for I in [1..8] do
 for J in [1..8] do
  k:=Position(subsets,Intersection(subsets[I],subsets[J]));
  if Intersection(parabolics[I],parabolics[J])<>parabolics[k] then Error("n2 IP");fi;
 od;
od;
if r[1]^((1,5)(2,6))<>r[3] or r[2]^((1,5)(2,6))<>r[2] then Error("n2 duality");fi;
Print("exceptional_n2_order8_IP64_duality=PASS\n");
# Period relations alone do not imply displacement commutativity.
x:=(1,2,3,4);; y:=(1,2,4,3);;
t1:=y*x;; t2:=y^2*x^2;;
if x^4<> () or y^4<> () or t1*t2=t2*t1 then Error("bad weakening control"); fi;
Print("period_only_commutativity_weakening_refuted=PASS\n");
Print("PASS_INDEPENDENT_FINITE_DIAGNOSTICS_ONLY\n");
QUIT;
