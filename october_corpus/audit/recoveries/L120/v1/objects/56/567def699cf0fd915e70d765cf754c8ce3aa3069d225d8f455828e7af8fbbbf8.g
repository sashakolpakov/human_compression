SizeScreen([1000000,1000000]);;
Read(intervalFile);;
Read(positiveFile);;
Need:=function(b,s)if not b then Error(s);fi;end;;
AllSubsetStringIP:=function(t)
 local r,a,b,sets,gs,G;
 r:=Length(t);
 if r=0 or not ForAll(t,x->IsPerm(x) and Order(x)=2) then return false;fi;
 for a in [1..r] do for b in [a+2..r] do
  if Comm(t[a],t[b])<>() then return false;fi;
 od;od;
 G:=Group(t);sets:=Combinations([1..r]);gs:=List(sets,z->Subgroup(G,t{z}));
 for a in [1..Length(sets)] do for b in [1..Length(sets)] do
  if Intersection(gs[a],gs[b])<>Subgroup(G,t{Intersection(sets[a],sets[b])}) then return false;fi;
 od;od;
 return true;
end;;
ivs:=Filtered(Elements(SymmetricGroup(4)),g->Order(g)=2);;
Need(Length(ivs)=9,"nine literal S4 involutions");;
for r in [1..4] do
 count:=0;good:=0;
 for t in Tuples(ivs,r) do
  actual:=IntervalStringIP(t);truth:=AllSubsetStringIP(t);
  Need(actual.ok=truth,"complete S4 comparison against arbitrary subsets");
  count:=count+1;if truth then good:=good+1;fi;
 od;
 Print("SMALL|",r,"|",count,"|",good,"\n");
od;
for t in [[],[()],[(1,2,3)],[(1,2),(1,2)],[(1,2),(3,4),(2,3)]] do
 Need(not IntervalStringIP(t).ok,"explicit malformed or invalid marking");
od;
n:=0;;
for row in positiveRows do
 n:=row[1];count:=0;checks:=0;
 for arrays in row[2] do
  Need(ForAll(arrays,a->Length(a)=n and Set(a)=[1..n]),"literal permutations");
  t:=List(arrays,PermList);ans:=IntervalStringIP(t);
  Need(ans.ok,"accepted positive marking passes all intervals");
  Need(Size(Group(t))=Factorial(n),"actual symmetric target");
  Need(ans.checks=(Length(t)-1)*(Length(t)-2)/2,"every interval tested");
  count:=count+1;checks:=checks+ans.checks;
 od;
 Print("POSITIVE|",n,"|",count,"|",checks,"\n");
od;
Print("EXPLICIT_NEGATIVES|5\nCOMPLETE_INTERVAL_CONTROLS\n");
QUIT;
