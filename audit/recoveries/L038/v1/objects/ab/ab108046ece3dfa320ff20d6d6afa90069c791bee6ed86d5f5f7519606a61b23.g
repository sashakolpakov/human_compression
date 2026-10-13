Read("a12_witnesses.g");
Check:=function(t)
 local r,i,j,sets,sub,k,c;
 r:=Length(t);
 if not ForAll(t,x->Order(x)=2 and SignPerm(x)=1) then Error("even involutions");fi;
 for i in [1..r] do if i+2<=r then for j in [i+2..r] do
  if t[i]*t[j]<>t[j]*t[i] then Error("string");fi;
 od;fi;od;
 if Size(Group(t))<>Factorial(12)/2 then Error("A12 generation");fi;
 sets:=Combinations([1..r]);sub:=List(sets,I->Group(Concatenation([()],t{I})));c:=0;
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  k:=Position(sets,Union(sets[i],sets[j]));
  if Intersection(sub[i],sub[j])<>sub[k] then Error("subset intersection");fi;c:=c+1;
 od;od;
 Print("A12_RANK ",r," ORDER ",Size(Group(t))," SUBSET_PAIRS ",c," TYPE ",List([1..r-1],i->Order(t[i]*t[i+1])),"\n");
end;
for t in a12Tuples do Check(t);od;
Print("TWO_RETAINED_A12_WITNESSES_PASS\n");QUIT;
