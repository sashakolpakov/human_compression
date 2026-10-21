LoadPackage("grape");;LoadPackage("json");;SizeScreen([100000,24]);;
Read(Concatenation(CODE_DIR,"/cosets.g"));;
Read(Concatenation(CODE_DIR,"/palette.g"));;
RunSmallPaletteControls:=function(out)
 local n,partition,colors,allowed,es,adj,e,d,got,blocks,C,K,p,modelCount,isoCount,ee,objectPerm,typePerm,q,g2,found,
       g,a,b,c,models,par,E,degree,records,i,r;
 modelCount:=0;isoCount:=0;
 for n in [1..4]do
  for partition in PartitionsSet([1..n])do
   colors:=List([1..n],v->PositionProperty(partition,c->v in c));
   allowed:=Filtered(Combinations([1..n],2),e->colors[e[1]]<>colors[e[2]]);
   for es in Combinations(allowed)do
    adj:=List([1..n],v->[]);for e in es do AddSet(adj[e[1]],e[2]);AddSet(adj[e[2]],e[1]);od;
    d:=rec(n:=n,rank:=Length(partition),types:=colors,adjacency:=adj);got:=LiteralPaletteGroups(d);
    blocks:=Set(partition);C:=Filtered(Elements(SymmetricGroup(n)),p->Set(List(partition,b->OnSets(b,p)))=blocks and ForAll([1..n],v->OnSets(adj[v],p)=adj[v^p]));
    K:=Filtered(C,p->ForAll([1..n],v->colors[v^p]=colors[v]));
    if Set(Elements(got.object_correlations))<>Set(C)or Set(Elements(got.object_typed))<>Set(K)then Error("literal all-permutation palette groups");fi;
    objectPerm:=PermList(Reversed([1..n]));typePerm:=PermList(Reversed([1..d.rank]));
    ee:=List([1..n],v->[]);e:=List([1..n],v->0);
    for i in [1..n]do ee[i^objectPerm]:=OnSets(adj[i],objectPerm);e[i^objectPerm]:=colors[i]^typePerm;od;
    g2:=LiteralPaletteGraph(rec(n:=n,rank:=d.rank,types:=e,adjacency:=ee));
    q:=PermList(Concatenation(List([1..n],v->v^objectPerm),List([1..d.rank],t->n+t^typePerm)));
    if not CheckPaletteMap(got.palette,g2,q)then Error("explicit positive palette relabelling");fi;
    found:=GraphIsomorphism(rec(graph:=got.palette.graph,colourClasses:=got.palette.colourClasses),rec(graph:=g2.graph,colourClasses:=g2.colourClasses));
    if found=fail or not CheckPaletteMap(got.palette,g2,found)then Error("exact palette isomorphism");fi;
    modelCount:=modelCount+1;isoCount:=isoCount+1;
   od;
  od;
 od;
 # Same uncoloured empty graph, inequivalent equal-rank type partitions.
 d:=LiteralPaletteGraph(rec(n:=4,rank:=2,types:=[1,1,2,2],adjacency:=[[],[],[],[]]));
 e:=LiteralPaletteGraph(rec(n:=4,rank:=2,types:=[1,2,2,2],adjacency:=[[],[],[],[]]));
 if GraphIsomorphism(rec(graph:=d.graph,colourClasses:=d.colourClasses),rec(graph:=e.graph,colourClasses:=e.colourClasses))<>fail then Error("wrong type partitions accepted");fi;
 models:=[];
 g:=Group((1,2),(3,4));Add(models,[g,[Group((1,2)),Group((3,4))]]);
 g:=SymmetricGroup(3);Add(models,[g,[Group((1,2)),Group((1,2,3))]]);
 g:=Group((1,2,3),(4,5),(6,7));a:=Group((1,2,3));b:=Group((4,5));c:=Group((6,7));Add(models,[g,[ClosureGroup(b,c),ClosureGroup(a,c),ClosureGroup(a,b)]]);
 records:=[];
 for i in [1..Length(models)]do
  g:=models[i][1];par:=models[i][2];E:=Elements(g);d:=LiteralCosetGeometry(g,par,E);got:=LiteralPaletteGroups(d);degree:=LargestMovedPoint(g);
  r:=rec(group_generators:=List(GeneratorsOfGroup(g),p->ListPerm(p,degree)),group_elements:=List(E,p->ListPerm(p,degree)),parabolics:=List(par,H->List(Elements(H),x->Position(E,x))),
   n:=d.n,rank:=d.rank,types:=d.types,coset_positions:=d.coset_positions,adjacency:=d.adjacency,group_action:=List(d.group_action,p->ListPerm(p,d.n)),
   correlation_order:=Size(got.object_correlations),typed_order:=Size(got.object_typed));Add(records,r);
 od;
 PrintTo(Concatenation(out,"/coset_models.json"),GapToJsonString(records));
 Print("PASS_LITERAL_PALETTE_CONTROLS graphs=",modelCount," positive_isomorphisms=",isoCount," coset_models=",Length(records),"\n");
end;
RunSmallPaletteControls(OUTPUT_DIR);;
QUIT_GAP(0);
