# Complete diagnostics for the written uniform theorems; no finite-premise claim.
SetInfoLevel(InfoWarning,0);;
Need:=function(b,s) if not b then Error(s); fi; end;;
OnSubset:=function(marks,S) local x;x:=List(S,i->marks[i]);if IsEmpty(x) then return Group(());fi;return Group(x);end;;
AllIP:=function(marks) local subs,gs,i,j,k;subs:=Combinations([1..Length(marks)]);gs:=List(subs,S->OnSubset(marks,S));for i in [1..Length(subs)] do for j in [i..Length(subs)] do k:=Position(subs,Intersection(subs[i],subs[j]));if Intersection(gs[i],gs[j])<>gs[k] then return false;fi;od;od;return true;end;;
Components:=function(n,edges) local cs,e,a,b;cs:=List([1..n],x->[x]);for e in edges do a:=PositionProperty(cs,c->e[1] in c);b:=PositionProperty(cs,c->e[2] in c);if a<>b then cs[a]:=Union(cs[a],cs[b]);Remove(cs,b);fi;od;return cs;end;;
Marks:=function(n,edges,Removed) local out,e,g;out:=[];for e in edges do g:=(e[1],e[2]);if Intersection(e,Removed)=[] then g:=g*(n+e[1],n+e[2]);fi;Add(out,g);od;return out;end;;
SymSupport:=function(S) if Length(S)<2 then return Group(());fi;return SymmetricGroup(S);end;;
Predicted:=function(n,edges,Removed) local cs,C,gs,D,ed,other,I,x,g;
 cs:=Components(n,edges);gs:=[];
 for C in cs do
  if Intersection(C,Removed)=[] then
   for g in GeneratorsOfGroup(SymSupport(C)) do Add(gs,g*PermList(Concatenation([1..n],List([1..n],x->n+x^g))));od;
  else
   Append(gs,GeneratorsOfGroup(SymSupport(C)));
   ed:=Filtered(edges,e->IsSubset(C,e) and Intersection(e,Removed)=[]);
   for D in Components(n,ed) do if IsSubset(Difference(C,Removed),D) then Append(gs,GeneratorsOfGroup(SymSupport(List(D,x->x+n))));fi;od;
  fi;
 od;
 if IsEmpty(gs) then return Group(());fi;return Group(gs);
end;;
trees:=[rec(n:=1,edges:=[]),rec(n:=2,edges:=[[1,2]]),rec(n:=4,edges:=[[1,2],[2,3],[3,4]]),rec(n:=4,edges:=[[1,2],[1,3],[1,4]]),rec(n:=5,edges:=[[1,2],[2,3],[3,4],[4,5]]),rec(n:=5,edges:=[[1,2],[2,3],[2,4],[4,5]])];;
cases:=0;;fibers:=0;;wreaths:=0;;
for T in trees do
 for Removed in Combinations([1..T.n]) do
  if Removed<>[] then
   ZE:=Filtered(T.edges,e->IsSubset(Removed,e));
   comps:=Components(T.n,ZE);
   if Removed in comps then
    m:=Marks(T.n,T.edges,Removed);Need(AllIP(m),"deleted tree C");
    for I in Combinations([1..Length(T.edges)]) do
     Need(OnSubset(m,I)=Predicted(T.n,T.edges{I},Removed),"exact selected subgroup formula");fibers:=fibers+1;
    od;
    cases:=cases+1;
   fi;
  fi;
 od;
 for z in [1..T.n] do
  m:=Marks(T.n,T.edges,[z]);s:=Product([1..T.n],i->(i,T.n+i));
  Need(AllIP(Concatenation(m,[s])),"tree wreath C");
  Need(Size(Group(Concatenation(m,[s])))=2*Factorial(T.n)^2,"full wreath order");
  wreaths:=wreaths+1;
 od;
od;
# Disconnected deleted set is the source's p9 unequal-start counterexample.
bad:=Marks(4,[[1,2],[2,3],[3,4]],[1,4]);;
Need(not AllIP(bad),"disconnected deletion must fail");
Need((6,7) in Intersection(Group(bad{[1,2]}),Group(bad{[2,3]})) and not (6,7) in Group(bad{[2]}),"literal defect pure second transposition");
# A cycle instead of a tree already fails in one row.
Need(not AllIP(Marks(3,[[1,2],[2,3],[1,3]],[1,2,3])),"cycle must fail");
# Exact marked identification, not just abstract group order, for the source r3 row.
source:=[(1,2)(5,6),(2,3),(1,5)(2,6)(3,4)];;
Need(AllIP(source) and Size(Group(source))=72,"literal source rank3 marking");
Print("PASS deleted cases ",cases," exact selected subgroups ",fibers," wreath cases ",wreaths," 2 weakening controls and literal rank3 source model\n");


# The individual-flip theorem is tested on all roots of the same trees.
binaries:=0;; binaryfibers:=0;;
for T in trees do
 for z in [1..T.n] do
  m:=Marks(T.n,T.edges,[]);f:=(z,T.n+z);
  Need(AllIP(Concatenation(m,[f])),"binary paired-tree C");
  Need(Size(Group(Concatenation(m,[f])))=2^T.n*Factorial(T.n),"binary full order");
  for I in Combinations([1..Length(T.edges)]) do
   cs:=Components(T.n,T.edges{I});D:=First(cs,C->z in C);
   predicted:=Group(Concatenation(m{I},List(D,x->(x,T.n+x))));
   Need(OnSubset(Concatenation(m,[f]),Concatenation(I,[Length(m)+1]))=predicted,"binary exact fiber");
   binaryfibers:=binaryfibers+1;
  od;
  binaries:=binaries+1;
 od;
od;
# Every selected group containing both new marks has the stated product formula.
tailfibers:=0;;
for n in [1..5] do
 edges:=List([1..n-1],i->[i,i+1]);m:=Marks(n,edges,[n]);s:=Product([1..n],i->(i,n+i));t:=(2*n,2*n+1);
 marks:=Concatenation(m,[s,t]);Need(AllIP(marks),"terminal-tail C");Need(Size(Group(marks))=Factorial(2*n+1),"terminal-tail full group");
 for I in Combinations([1..Length(edges)]) do
  cs:=Components(n,edges{I});D:=First(cs,C->n in C);R:=Concatenation(D,List(D,x->n+x),[2*n+1]);
  gs:=ShallowCopy(GeneratorsOfGroup(SymSupport(R)));
  for C in cs do if C<>D then
   for g in GeneratorsOfGroup(SymSupport(C)) do Add(gs,g*PermList(Concatenation([1..n],List([1..n],x->n+x^g))));od;
  fi;od;
  if Difference([1..n],D)<>[] then Add(gs,Product(Difference([1..n],D),x->(x,n+x)));fi;
  Need(Group(gs)=OnSubset(marks,Concatenation(I,[n,n+1])),"tail exact double-mark formula");tailfibers:=tailfibers+1;
 od;
od;
# Rooted-tree tail weakening: explicit element, not merely a failed black-box IP test.
m:=[(1,2),(1,3),(1,4)(2,5)(3,6),(4,7)];;
Need((3,6) in Group(m{[1,3,4]}) and (3,6) in Group(m{[2,3,4]}) and not (3,6) in Group(m{[3,4]}),"branching tail obstruction");
Print("PASS binary cases ",binaries," exact binary fibers ",binaryfibers," exact tail fibers ",tailfibers," and branching-tail control\n");
QUIT;
