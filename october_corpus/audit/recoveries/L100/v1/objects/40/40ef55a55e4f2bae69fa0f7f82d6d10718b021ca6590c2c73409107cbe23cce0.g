# Same object/marker construction as accepted R188Pair, using adjacency lists.
LiteralPaletteGraph:=function(d)
 local n,r,adj,t,a,aug;
 n:=d.n;r:=d.rank;adj:=List(d.adjacency,ShallowCopy);
 if Length(adj)<>n or Length(d.types)<>n or Set(d.types)<>[1..r] then Error("literal palette domain");fi;
 for a in [1..n] do
  if adj[a]<>Set(adj[a]) or a in adj[a] or not ForAll(adj[a],b->b in [1..n]and a in adj[b]and d.types[b]<>d.types[a])then Error("simple typed incidence graph");fi;
  AddSet(adj[a],n+d.types[a]);
 od;
 for t in [1..r] do Add(adj,Filtered([1..n],a->d.types[a]=t));od;
 aug:=Graph(Group(()),[1..n+r],OnPoints,function(a,b)return b in adj[a];end,true);
 return rec(graph:=aug,colourClasses:=[[1..n],[n+1..n+r]],adjacency:=adj,n:=n,rank:=r,types:=d.types);
end;
CheckPaletteMap:=function(d,e,p)
 local n,r,a;
 n:=d.n;r:=d.rank;
 return n=e.n and r=e.rank and IsPerm(p) and OnSets([1..n],p)=[1..n]and OnSets([n+1..n+r],p)=[n+1..n+r]
  and ForAll([1..n+r],a->OnSets(d.adjacency[a],p)=e.adjacency[a^p]);
end;
LiteralPaletteGroups:=function(d)
 local a,C,K,act,kernel,x,objectAction,typedAction;
 a:=LiteralPaletteGraph(d);C:=AutGroupGraph(a.graph,a.colourClasses);
 for x in GeneratorsOfGroup(C)do if not CheckPaletteMap(a,a,x)then Error("literal full correlation generator");fi;od;
 act:=ActionHomomorphism(C,[d.n+1..d.n+d.rank],OnPoints);kernel:=Kernel(act);
 K:=Stabilizer(C,[d.n+1..d.n+d.rank],OnTuples);
 if K<>kernel then Error("typed marker kernel mismatch");fi;
 objectAction:=ActionHomomorphism(C,[1..d.n],OnPoints);
 if Size(Kernel(objectAction))<>1 then Error("marker extension not faithful");fi;
 typedAction:=RestrictedMapping(objectAction,K);
 return rec(palette:=a,correlations:=C,typed:=K,object_correlations:=Image(objectAction),object_typed:=Image(typedAction),type_action:=Image(act));
end;
