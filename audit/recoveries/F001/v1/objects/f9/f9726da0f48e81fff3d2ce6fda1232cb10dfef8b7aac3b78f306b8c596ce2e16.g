FullIP:=function(t)
 local r,sets,groups,i,j,k;
 r:=Length(t);sets:=Combinations([1..r]);
 groups:=List(sets,s->Group(Concatenation([One(t[1])],t{s})));
 for i in [1..Length(sets)] do for j in [1..Length(sets)] do
  k:=Position(sets,Intersection(sets[i],sets[j]));
  if Intersection(groups[i],groups[j])<>groups[k] then return false;fi;
 od;od;return true;
end;;
AbstractEquivalent:=function(t,u)
 local h;
 h:=GroupHomomorphismByImages(Group(t),Group(u),t,u);
 return h<>fail and IsBijective(h);
end;;
