# Independent labelled anchored degree6 census: no prefix-orbit reduction,
# no index bound, no incremental end criterion, no candidate cache.
SizeScreen([100000,100000]);;
n:=6;; S:=SymmetricGroup(n);; F:=Stabilizer(S,1);;
I:=Filtered(Elements(S),g->Order(g)=2 and 1^g<>1);;
T:=Filtered(Elements(F),g->Order(g)=2);;
IP:=function(t)
 local subsets,groups,i,j,k;
 subsets:=Combinations([1..Length(t)]);
 groups:=List(subsets,A->Group(t{A},()));
 for i in [1..Length(groups)] do for j in [1..i] do
  k:=Position(subsets,Intersection(subsets[i],subsets[j]));
  if Intersection(groups[i],groups[j])<>groups[k] then return false;fi;
 od;od;return true;
end;;
count:=0;; transitive:=0;; outputs:=[];; t:=[];;
for a in I do for b in T do for c in T do
 if a*c<>c*a then continue;fi;
 count:=count+1;t:=[a,b,c];H:=Group(t);
 if not IsTransitive(H,[1..n]) then continue;fi;transitive:=transitive+1;
 if ForAny([1..3],j->IsTransitive(Group(t{Difference([1..3],[j])},()),[1..n])) then continue;fi;
 if not IP(t) then continue;fi;
 good:=true;old:=Group(());
 for j in [1..3] do
  J:=Group(t{[1..j]});anchorOrbit:=Orbit(old,1);
  if not IsSubgroup(old,Intersection(J,SymmetricGroup(anchorOrbit))) then good:=false;break;fi;
  old:=J;
 od;
 if good then Add(outputs,t);Print("LABELLED|",List(t,g->List([1..n],i->i^g)),"\n");fi;
od;od;od;
Print("COMPLETE_LABELLED|",count,"|",transitive,"|",Length(outputs),"\n");QUIT;
