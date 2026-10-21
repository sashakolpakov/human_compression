CheckString:=function(t)
 local m;
 m:=Length(t);if m<=2 then return true;fi;
 return CheckString(t{[1..m-1]}) and CheckString(t{[2..m]}) and
 Intersection(Group(t{[1..m-1]}),Group(t{[2..m]}))=Group(t{[2..m-1]});
end;;
PartialC:=function(t,selected,H)
 local blocks,b,i;
 blocks:=[];b:=[];
 for i in selected do
  if Length(b)>0 and i<>b[Length(b)]+1 then Add(blocks,b);b:=[];fi;
  Add(b,i);
 od;
 if Length(b)>0 then Add(blocks,b);fi;
 for b in blocks do
  if not CheckString(t{b}) then return false;fi;
 od;
 return Product(blocks,b->Size(Group(t{b})))=Size(H);
end;;
