Read("positive_inputs.g");;
SizeScreen([100000,100000]);;
AllIP:=function(t)
 local subsets,groups,i,j,k;
 subsets:=Combinations([1..Length(t)]);groups:=List(subsets,A->Group(t{A},()));
 for i in [1..Length(groups)] do for j in [1..i] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));
  if Intersection(groups[i],groups[j])<>groups[k] then return false;fi;
 od;od;return true;
end;;
IntervalsIP:=function(t)
 local r,len,i,j,A,B,C;
 r:=Length(t);
 for i in [1..r] do
  if Order(t[i])<>2 then return false;fi;
  for j in [i+2..r] do if t[i]*t[j]<>t[j]*t[i] then return false;fi;od;
 od;
 for len in [2..r] do for i in [1..r-len+1] do
  j:=i+len-1;A:=Group(t{[i..j-1]},());B:=Group(t{[i+1..j]},());C:=Group(t{[i+1..j-1]},());
  if Intersection(A,B)<>C then return false;fi;
 od;od;return true;
end;;
wingOrders:=[];;fullOrders:=[];;
for arr in wingArrays do
 n:=Length(arr[1]);t:=List(arr,PermList);r:=Length(t);H:=Group(t);
 if not IsTransitive(H,[1..n]) or not AllIP(t) then Error("wing IP/transitivity");fi;
 if 1^t[1]=1 or ForAny(t{[2..r]},g->1^g<>1) then Error("wing anchor");fi;
 for j in [1..r] do
  if IsTransitive(Group(t{Difference([1..r],[j])},()),[1..n]) then Error("wing fracture");fi;
  A:=Group(t{[1..j-1]},());B:=Group(t{[1..j]},());O:=Orbit(A,1);
  if not IsSubgroup(A,Intersection(B,SymmetricGroup(O))) then Error("wing leaf");fi;
 od;
 Add(wingOrders,Size(H));
od;
for arr in fullArrays do
 n:=Length(arr[1]);t:=List(arr,PermList);H:=Group(t);
 if Size(H)<>Factorial(n) or not IntervalsIP(t) then Error("full gluing group or IP");fi;
 Add(fullOrders,Size(H));
od;
Print("COMPLETE_POSITIVE_CHECKS|",Length(wingOrders),"|",Length(fullOrders),"|",Collected(wingOrders),"|",Collected(fullOrders),"\n");QUIT;
