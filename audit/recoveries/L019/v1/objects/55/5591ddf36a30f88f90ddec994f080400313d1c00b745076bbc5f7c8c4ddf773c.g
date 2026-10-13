S:=SymmetricGroup(6);;T:=Stabilizer(S,1);;iv:=Filtered(Elements(T),g->Order(g)=2);;
IP:=function(t)
local subs,I,J,r; r:=Length(t);subs:=List(Combinations([1..r]),I->Group(t{I},()));
for I in [1..Length(subs)] do for J in [1..I] do
if Intersection(subs[I],subs[J])<>Group(t{Intersection(Combinations([1..r])[I],Combinations([1..r])[J])},()) then return false;fi;
od;od;return true;end;;
GoodCut:=function(t,j)
local O,A,B,L,R,q,cross,a,b,fa,fb;
O:=Orbits(Group(t{Difference([1..4],[j])}),[1..6]);if Length(O)<>2 then return false;fi;
L:=Group(t{[1..j-1]});R:=Group(t{[j+1..4]});
for A in O do B:=Difference([1..6],A);
if not (IsTransitive(L,A) and IsTransitive(R,B) and ForAll(GeneratorsOfGroup(L),h->ForAll(B,x->x^h=x)) and ForAll(GeneratorsOfGroup(R),h->ForAll(A,x->x^h=x))) then continue;fi;
q:=t[j];cross:=Filtered(A,x->not x^q in A);if Length(cross)<>1 then continue;fi;
a:=cross[1];b:=a^q;fa:=ForAll(Difference(A,[a]),x->x^q=x);fb:=ForAll(Difference(B,[b]),x->x^q=x);
if fa and ForAny(t{[1..j-1]},h->SignPerm(h)=-1) and ForAny(t{[j..4]},h->SignPerm(h)=-1) then return true;fi;
if fb and ForAny(t{[1..j]},h->SignPerm(h)=-1) and ForAny(t{[j+1..4]},h->SignPerm(h)=-1) then return true;fi;
od;return false;end;;
count:=0;;bad:=[];;fractured:=0;;t:=[];;
for a in [(1,2),(1,2)(3,4),(1,2)(3,4)(5,6)] do
for b in iv do if a*b=b*a then continue;fi;
for c in iv do if a*c<>c*a or b*c=c*b or not IP([a,b,c]) then continue;fi;
for d in iv do if a*d<>d*a or b*d<>d*b or c*d=d*c then continue;fi;
t:=[a,b,c,d];if Size(Group(t))<>720 or not IP(t) then continue;fi;count:=count+1;
if ForAny([1..4],j->IsTransitive(Group(t{Difference([1..4],[j])}),[1..6])) then continue;fi;
fractured:=fractured+1;
if not ForAny([2,3],j->GoodCut(t,j)) then Add(bad,t);Print("BAD ",t,"\n");fi;
od;od;od;od;
Print("SUMMARY all=",count," fractured=",fractured," bad=",Length(bad),"\n");QUIT;
