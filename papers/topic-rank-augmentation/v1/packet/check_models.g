# Exhaustive finite diagnostics within the explicitly bounded template space.
# These samples are not premises of any quantified written theorem.
SizeScreen([240,60]);;
Need:=function(x,m)if not x then Error(m);fi;end;;
Par:=function(xs,I)return Group(Concatenation([()],xs{I}));end;;
IsC:=function(xs)local ss,i,j;ss:=Combinations([1..Length(xs)]);
 for i in ss do for j in ss do
  if Intersection(Par(xs,i),Par(xs,j))<>Par(xs,Intersection(i,j)) then return false;fi;
 od;od;return true;end;;
TailList:=function(m,n)local tails,k,nxt,s,a,b,u,z;
 tails:=[[[],[],m]];
 for k in [1..n-m] do
  nxt:=[];
  for s in tails do a:=s[1];b:=s[2];u:=s[3];
   if u=n then Add(nxt,s);else
    Add(nxt,[a,b,u+1]);
    if u+2<=n then z:=(u+1,u+2);
     Add(nxt,[Concatenation(a,[z]),b,u+2]);
     Add(nxt,[a,Concatenation(b,[z]),u+2]);
     Add(nxt,[Concatenation(a,[z]),Concatenation(b,[z]),u+2]);
    fi;
    if u+3<=n then Add(nxt,[Concatenation(a,[(u+1,u+2)]),Concatenation(b,[(u+2,u+3)]),u+3]);fi;
   fi;
  od;tails:=Set(nxt);
 od;return Filtered(tails,s->s[3]=n);
end;;
templates:=[rec(m:=4,a:=(2,3),b:=(3,4),t:=(1,2),ends:=[1,2],u:=2),
 rec(m:=5,a:=(1,2)(3,4),b:=(4,5),t:=(2,3),ends:=[2,3],u:=3),
 rec(m:=6,a:=(2,3)(4,5),b:=(1,2)(5,6),t:=(3,4),ends:=[3,4],u:=4)];;
counts:=List([1..3],i->[0,0,0,0]);;R:=[];;
for d in [1..3] do e:=templates[d];
 for n in [Maximum(5,e.m)..8] do
  for tail in TailList(e.m,n) do
   a:=e.a*Product(tail[1],());;b:=e.b*Product(tail[2],());;t:=e.t;;
   central:=Intersection(Centralizer(SymmetricGroup(n),a),Stabilizer(SymmetricGroup(n),e.ends,OnTuples));;
   for c in Filtered(Elements(central),x->Order(x)=2) do
    counts[d][1]:=counts[d][1]+1;
    if not IsTransitive(Group([t,a,b,c]),[1..n]) then continue;fi;
    counts[d][2]:=counts[d][2]+1;
    Need(Length(Set([t,a,b,c]))=4,"distinct output involutions");
    B:=Group([a,b]);;H:=Group([t,a,b]);;K:=Group([a,b,c]);;
    Need(IsC([t,a,b]) and IsC([a,b,c]),"both actual C ends");
    full:=IsC([t,a,b,c]);;
    if e.m<6 then
     aout:=PermList(List([1..n],i->i));;bout:=aout;;
     aa:=List([1..n],i->i);;bb:=ShallowCopy(aa);;
     for i in [e.m+1..n] do aa[i]:=i^a;bb[i]:=i^b;od;
     Bout:=Group([PermList(aa),PermList(bb)]);;
     Need(H=Group(Concatenation(GeneratorsOfGroup(SymmetricGroup([1..e.m])),GeneratorsOfGroup(Bout))),"actual supported product");
     R:=Orbit(K,e.u);;triples:=Filtered(Orbits(B,[1..n]),o->Length(o)=3 and o[1] in R);;
     blockhyp:=Length(triples)=1 or not IsPrimitive(Action(K,R));;
     sufficient:=blockhyp and (e.m=4 or ForAll([a,b,c],x->SignPerm(x)=1));;
     if sufficient then Need(full,"four/five point positive theorem");counts[d][3]:=counts[d][3]+1;fi;
    else
     N:=Group([(3,4),(2,5),(1,6)]);;
     Need(Size(N)=8 and H=Group(Concatenation(GeneratorsOfGroup(N),[a,b])) and Size(Intersection(N,B))=1,"matching semidirect product");
     Need(full=(Size(Intersection(N,K))=1),"seven-test equivalence");
     if not 4 in Orbit(K,3) then Need(full,"separated-triple sufficient condition");counts[d][3]:=counts[d][3]+1;fi;
    fi;
    if full then counts[d][4]:=counts[d][4]+1;fi;
   od;
  od;
 od;
od;
Print("COUNTS [scanned,transitive,sufficient,C] ",counts,"\n");
Print("PASS bounded common-theorem diagnostics\n");
QUIT_GAP(0);
