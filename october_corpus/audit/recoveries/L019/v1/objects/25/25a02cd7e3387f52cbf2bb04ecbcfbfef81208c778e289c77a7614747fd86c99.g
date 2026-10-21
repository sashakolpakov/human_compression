SizeScreen([100000,100000]);;
ambientGroup:=SymmetricGroup(10);;
AllIP:=function(gs)
 local groups,mask,other,common,inds,l;
 groups:=[];
 for mask in [0..2^Length(gs)-1] do
  inds:=Filtered([1..Length(gs)],l->QuoInt(mask,2^(l-1)) mod 2=1);
  Add(groups,Subgroup(ambientGroup,gs{inds}));
 od;
 for mask in [0..Length(groups)-1] do
  for other in [0..mask] do
   common:=Sum(Filtered([0..Length(gs)-1],l->QuoInt(mask,2^l) mod 2=1
                  and QuoInt(other,2^l) mod 2=1),l->2^l);
   if Intersection(groups[mask+1],groups[other+1])<>groups[common+1] then return false;fi;
  od;
 od;
 return true;
end;;
marks:=List([[2, 1, 3, 4, 5, 6, 7, 8, 9, 10], [1, 3, 2, 4, 5, 6, 7, 8, 9, 10], [1, 2, 4, 3, 5, 6, 7, 8, 9, 10], [1, 2, 3, 5, 4, 6, 7, 8, 9, 10], [1, 2, 3, 4, 6, 5, 8, 7, 10, 9], [1, 2, 3, 4, 5, 7, 6, 9, 8, 10]],PermList);;
if Size(Group(marks))<>Factorial(10) or not AllIP(marks) then Error("positive group/IP");fi;
if not ForAll(marks{[2..6]},x->1^x=1) or 1^marks[1]=1 or NrMovedPoints(marks[1])<>2 then Error("positive anchor/purity");fi;
for i in [1..6] do
 H:=Group(marks{Filtered([1..6],j->j<>i)});
 if IsTransitive(H,[1..10]) then Error("positive fracture");fi;
od;
for j in [2..6] do
 H:=Group(marks{[1..j-1]});J:=Group(marks{[1..j]});anchorOrbit:=Orbit(H,1);
 if Length(anchorOrbit)>=3 and not IsSubgroup(H,Intersection(J,AlternatingGroup(anchorOrbit))) then Error("positive even kernel");fi;
od;
Print("PASS_PURE_FIRST_POSITIVE|",Size(Group(marks)),"|6|2080_subset_pairs\n");
QUIT;
