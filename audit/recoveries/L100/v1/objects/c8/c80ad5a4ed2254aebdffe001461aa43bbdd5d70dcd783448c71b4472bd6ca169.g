# Fixed-model and exact complete Aut/type result are loaded by the pinned driver.
RunLiteralPaletteCatalogue:=function(G,input,out)
 local E,gs,degree,graphs,models,classes,members,records,i,j,c,d,g,hit,p,colors,record,summary,r,counts,completed;
 gs:=GeneratorsOfGroup(G);
 if input.group_generators<>gs then Error("fixed fusion group generators");fi;
 E:=Elements(G);degree:=LargestMovedPoint(G);
 PrintTo(Concatenation(out,"/group_elements.json"),GapToJsonString(rec(
  generators:=List(gs,p->ListPerm(p,degree)),elements:=List(E,p->ListPerm(p,degree)))));
 graphs:=[];models:=[];classes:=[];members:=[];records:=[];completed:=[];
 for i in [1..Length(input.representatives)]do
  c:=input.representatives[i];Print("PALETTE_BEGIN ",i," source=",[c.borel_id,c.source_index],"\n");
  d:=LiteralCosetGeometry(G,c.parabolics,E);g:=LiteralPaletteGroups(d);
  if not ForAll(d.group_action,p->p in g.object_typed)then Error("specified right action outside full typed group");fi;
  PrintTo(Concatenation(out,"/model",String(i),".json"),GapToJsonString(rec(
   source:=[c.borel_id,c.source_index],n:=d.n,rank:=d.rank,types:=d.types,type_sizes:=d.type_sizes,
   parabolics:=List(c.parabolics,H->List(Elements(H),x->Position(E,x))),coset_positions:=d.coset_positions,
   adjacency:=d.adjacency,group_action:=List(d.group_action,p->ListPerm(p,d.n)))));
  hit:=fail;p:=fail;
  for j in classes do
   if d.rank=models[j].rank and SortedList(d.type_sizes)=SortedList(models[j].type_sizes)then
    p:=GraphIsomorphism(rec(graph:=graphs[j].graph,colourClasses:=graphs[j].colourClasses),rec(graph:=g.palette.graph,colourClasses:=g.palette.colourClasses));
    if p<>fail then
     if not CheckPaletteMap(graphs[j],g.palette,p)then Error("literal geometry isomorphism");fi;
     hit:=j;break;
    fi;
   fi;
  od;
  if hit=fail then Add(classes,i);hit:=i;p:=();fi;
  record:=rec(index:=i,source:=[c.borel_id,c.source_index],rank:=d.rank,type_sizes:=d.type_sizes,
   correlations_order:=Size(g.correlations),typed_order:=Size(g.typed),type_action_order:=Size(g.type_action),
   correlations_generators:=List(GeneratorsOfGroup(g.correlations),p->ListPerm(p,d.n+d.rank)),
   typed_generators:=List(GeneratorsOfGroup(g.typed),p->ListPerm(p,d.n+d.rank)),
   bare_representative:=hit,bare_map:=ListPerm(p,d.n+d.rank));
  PrintTo(Concatenation(out,"/groups",String(i),".json"),GapToJsonString(record));
  Add(graphs,g.palette);Add(models,d);Add(records,record);Add(members,[hit,i]);Add(completed,i);
  summary:=rec(status:="COMPLETE_LEADING_REPRESENTATIVES_ONLY",completed:=completed,classes:=classes,members:=members,records:=records);
  PrintTo(Concatenation(out,"/checkpoint.json"),GapToJsonString(summary));
  Print("PALETTE_DONE ",i," rank=",d.rank," types=",d.type_sizes," Cor=",Size(g.correlations)," Aut=",Size(g.typed)," class=",hit,"\n");
 od;
 counts:=[];
 for r in Set(List(input.representatives,c->Length(c.parabolics)))do
  Add(counts,[r,Number(input.representatives,c->Length(c.parabolics)=r),Number(classes,i->models[i].rank=r)]);
 od;
 summary:=rec(status:="COMPLETE_LITERAL_INCIDENCE_AND_PALETTE_CATALOGUE",counts:=counts,classes:=classes,members:=members,records:=records,completed:=completed,
  scope:="Full incidence isomorphism, correlation and type-preserving groups for precisely the acquired representatives; group names, diagrams and source joins separate");
 PrintTo(Concatenation(out,"/result.json"),GapToJsonString(summary));
 Print("PASS_COMPLETE_LITERAL_PALETTE representatives=",Length(models)," counts=",counts,"\n");
end;
RunLiteralPaletteCatalogue(G,L100CompleteAutFusion,OUTPUT_DIR);;
QUIT_GAP(0);
