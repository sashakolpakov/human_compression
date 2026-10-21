# Same classification as subdivision_markings.g, using its actual coset actions.
Read("subdivision_markings.g");;
L059ActionMax:=function(G,domain,action)
  local image;
  image:=Action(G,domain,action);
  if Transitivity(image,[1..Length(domain)])>=2 then return "2T"; fi;
  if IsPrimitive(image,[1..Length(domain)]) then return "M"; fi;
  return "X";
end;;
L059SubdivisionRows:=function(F,edges,reps)
  local arcs,edge,u,v,vertices,neighbours,rows,H,P,Q,B,row;
  arcs:=Concatenation(List(edges,e->[e,Reversed(e)]));
  vertices:=Set(Concatenation(edges));
  edge:=edges[1];u:=edge[1];v:=edge[2];rows:=[];
  neighbours:=Set(Concatenation(Filtered(edges,e->u in e)));
  RemoveSet(neighbours,u);
  Need(Length(neighbours)=3 and IsTransitive(F,arcs,OnTuples));
  for H in reps do
    Need(IsSubgroup(F,H) and IsTransitive(H,arcs,OnTuples));
    P:=Stabilizer(H,u);Q:=Stabilizer(H,edge,OnSets);B:=Intersection(P,Q);
    Need(B=Stabilizer(P,v));
    Need(Size(Core(H,B))=1 and ClosureGroup(P,Q)=H);
    Need(Index(P,B)=3 and Index(Q,B)=2);
    Need(IsTransitive(P,neighbours) and IsTransitive(Q,edge));
    row:=rec(H:=H,H0:=P,H1:=Q,B:=B,
      maxcode:=[L059ActionMax(P,neighbours,OnPoints),
               L059ActionMax(Q,edge,OnPoints),
               L059ActionMax(H,vertices,OnPoints),
               L059ActionMax(H,edges,OnSets)],
      normcode:=List([H,P,Q,B],K->IsNormal(F,K)),dualorder:=0,
      maxorder:=Maximum(List(ConjugacyClasses(H),c->Order(Representative(c)))),
      group_order:=Size(H),subgroup_orders:=List([P,Q,B],Size));
    Add(rows,row);
  od;
  return rows;
end;;
