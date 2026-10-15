# Exact right-coset incidence. No new subgroup or geometry enumeration.
LiteralCosetGeometry:=function(G,par,E)
 local r,n,types,parts,which,cosets,t,H,trans,x,c,i,j,k,a,b,adj,acts,g,images,target,domain,gs;
 r:=Length(par);n:=0;types:=[];parts:=[];which:=[];gs:=GeneratorsOfGroup(G);
 if E<>Elements(G) then Error("actual ordered group element domain");fi;
 for t in [1..r] do
  H:=par[t];if not IsSubgroup(G,H) or H=G then Error("proper literal parabolic");fi;
  trans:=RightTransversal(G,H);which[t]:=List(E,x->0);
  for x in trans do
   c:=Set(List(Elements(H),h->Position(E,h*x)));
   if Length(c)<>Size(H) then Error("literal right coset size");fi;
   n:=n+1;Add(types,t);Add(parts,c);
   for k in c do if which[t][k]<>0 then Error("coset partition overlap");fi;which[t][k]:=n;od;
  od;
  if ForAny(which[t],x->x=0) or Length(trans)*Size(H)<>Length(E) then Error("complete coset partition");fi;
 od;
 adj:=List([1..n],x->[]);
 for k in [1..Length(E)] do
  for i in [1..r] do for j in [i+1..r] do
   if j<=r then a:=which[i][k];b:=which[j][k];AddSet(adj[a],b);AddSet(adj[b],a);fi;
  od;od;
 od;
 acts:=[];
 for g in gs do
  images:=[];
  for a in [1..n] do
   t:=types[a];target:=which[t][Position(E,E[parts[a][1]]*g)];
   if not ForAll(parts[a],k->which[t][Position(E,E[k]*g)]=target) then Error("right action not well-defined on full coset");fi;
   images[a]:=target;
  od;
  x:=PermList(images);if x=fail or not ForAll([1..n],a->types[a^x]=types[a]and OnSets(adj[a],x)=adj[a^x])then Error("literal right action fails");fi;
  Add(acts,x);
 od;
 if Size(Group(acts))<>Size(G) then Error("nonfaithful specified group action");fi;
 return rec(n:=n,rank:=r,types:=types,coset_positions:=parts,adjacency:=adj,group_action:=acts,type_sizes:=List([1..r],t->Number(types,x->x=t)));
end;
