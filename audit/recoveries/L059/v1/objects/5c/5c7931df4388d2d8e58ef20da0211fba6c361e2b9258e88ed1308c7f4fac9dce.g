Need:=function(ok) if not ok then Error("L059 descent invalid"); fi; end;;
Read("maximal_descent.g");;

# Exact rank-two marked-geometry census for explicitly constructed graphs.
# This is a new bounded census, not a replay of the unrecovered historical lists.
LoadPackage("grape");;
SetAssertionLevel(1);;

P177Graph := function(label, n, black, edges)
  local E, graph, white;
  E := Set(List(edges, Set));
  white := Difference([1..n], black);
  Need( ForAll(E,e->Length(e)=2 and Length(Intersection(e,black))=1));
  graph := Graph(Group(()), [1..n], OnPoints, function(a,b) return Set([a,b]) in E; end, true);
  Need( IsConnectedGraph(graph));
  return rec(label:=label,n:=n,black:=Set(black),white:=white,edges:=E,graph:=graph);
end;;

P177Max := function(upper,lower)
  local degree, action;
  degree := Index(upper,lower);
  Need(degree>1);
  action := Action(upper,RightCosets(upper,lower),OnRight);
  if Transitivity(action,[1..degree])>=2 then return "2T"; fi;
  if IsPrimitive(action,[1..degree]) then return "M"; fi;
  return "X";
end;;

P177Census := function(data)
  local A, F, classes, edge, b, w, witnesses, H, H0, H1, B, D, duals,
        row, cls, maxcode, normcode, maxorder, dualorder, suborders;
  A := AutGroupGraph(data.graph,[data.black,data.white]);
  F := AutGroupGraph(data.graph);
  Need(IsTransitive(A,data.edges,OnSets));
  edge := data.edges[1];
  b := Intersection(edge,data.black)[1]; w := Intersection(edge,data.white)[1];
  classes := L059Descent(A,data.edges);
  witnesses := [];
  for cls in classes do
    H := Representative(cls);
    if IsTransitive(H,data.edges,OnSets) then
      H0 := Stabilizer(H,b); H1 := Stabilizer(H,w); B := Intersection(H0,H1);
      Need(Size(ClosureGroup(H0,H1))=Size(H));
      Need(Size(Core(H,B))=1);
      Need(Index(H,B)=Length(data.edges));
      maxcode := List([[H0,B],[H1,B],[H,H0],[H,H1]],p->P177Max(p[1],p[2]));
      normcode := List([H,H0,H1,B],K->IsNormal(A,K));
      D := Stabilizer(Normalizer(F,H),edge,OnSets);
      duals := Filtered(Elements(D),g->b^g=w);
      if IsEmpty(duals) then dualorder:=0; else dualorder:=Minimum(List(duals,Order)); fi;
      maxorder := Maximum(List(ConjugacyClasses(H),c->Order(Representative(c))));
      row := rec(H:=H,H0:=H0,H1:=H1,B:=B,maxcode:=maxcode,normcode:=normcode,
                 dualorder:=dualorder,maxorder:=maxorder,
                 group_order:=Size(H),subgroup_orders:=List([H0,H1,B],Size),
                 structure:=List([H,H0,H1,B],StructureDescription));
      Add(witnesses,row);
    fi;
  od;
  Print(data.label," vertices=",data.n," edges=",Length(data.edges)," Aut+=",Size(A),
        " Aut=",Size(F)," subgroup_classes=",Length(classes)," geometries=",Length(witnesses),"\n");
  Print("MAX ",Collected(List(witnesses,r->r.maxcode)),"\n");
  Print("NORM ",Collected(List(witnesses,r->r.normcode)),"\n");
  return rec(label:=data.label,n:=data.n,black:=data.black,white:=data.white,edges:=data.edges,
             A:=A,F:=F,base_edge:=edge,b:=b,w:=w,retained_edge_transitive_classes:=Length(classes),search:=L059Search,witnesses:=witnesses);
end;;


t:=Runtime();;
D:=P177Graph("064_006",64,[1, 2, 3, 4, 5, 6, 7, 8, 17, 18, 19, 20, 21, 22, 23, 24, 33, 34, 35, 36, 37, 38, 39, 40, 49, 50, 51, 52, 53, 54, 55, 56],[[1, 9], [1, 16], [1, 58], [1, 63], [2, 9], [2, 10], [2, 59], [2, 64], [3, 10], [3, 11], [3, 57], [3, 60], [4, 11], [4, 12], [4, 58], [4, 61], [5, 12], [5, 13], [5, 59], [5, 62], [6, 13], [6, 14], [6, 60], [6, 63], [7, 14], [7, 15], [7, 61], [7, 64], [8, 15], [8, 16], [8, 57], [8, 62], [9, 19], [9, 24], [10, 17], [10, 20], [11, 18], [11, 21], [12, 19], [12, 22], [13, 20], [13, 23], [14, 21], [14, 24], [15, 17], [15, 22], [16, 18], [16, 23], [17, 28], [17, 29], [18, 29], [18, 30], [19, 30], [19, 31], [20, 31], [20, 32], [21, 25], [21, 32], [22, 25], [22, 26], [23, 26], [23, 27], [24, 27], [24, 28], [25, 36], [25, 39], [26, 37], [26, 40], [27, 33], [27, 38], [28, 34], [28, 39], [29, 35], [29, 40], [30, 33], [30, 36], [31, 34], [31, 37], [32, 35], [32, 38], [33, 41], [33, 48], [34, 41], [34, 42], [35, 42], [35, 43], [36, 43], [36, 44], [37, 44], [37, 45], [38, 45], [38, 46], [39, 46], [39, 47], [40, 47], [40, 48], [41, 51], [41, 56], [42, 49], [42, 52], [43, 50], [43, 53], [44, 51], [44, 54], [45, 52], [45, 55], [46, 53], [46, 56], [47, 49], [47, 54], [48, 50], [48, 55], [49, 60], [49, 61], [50, 61], [50, 62], [51, 62], [51, 63], [52, 63], [52, 64], [53, 57], [53, 64], [54, 57], [54, 58], [55, 58], [55, 59], [56, 59], [56, 60]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/064_006.g","L059Result := ",R,";\n");
Read("current_c4_census/064_006.g");;
Need(Length(R.witnesses)=Length(L059Result.witnesses));;
for x in R.witnesses do y:=First(L059Result.witnesses,y->IsConjugate(R.A,x.H,y.H)); Need(y<>fail); Need(x.maxcode=y.maxcode and x.normcode=y.normcode and x.dualorder=y.dualorder and x.maxorder=y.maxorder); od;
Print("OLD_COMPLETE_CENSUS_MATCH\n");
Print("L059_DESCENT_COMPLETE 064_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
