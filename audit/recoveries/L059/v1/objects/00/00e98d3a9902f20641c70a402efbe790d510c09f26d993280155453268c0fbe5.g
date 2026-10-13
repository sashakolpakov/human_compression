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
D:=P177Graph("064_011",64,[1, 3, 6, 8, 9, 11, 14, 16, 17, 19, 22, 24, 25, 27, 30, 32, 33, 35, 38, 40, 41, 43, 46, 48, 49, 51, 54, 56, 57, 59, 62, 64],[[1, 2], [1, 21], [1, 45], [1, 52], [2, 3], [2, 30], [2, 38], [3, 4], [3, 15], [3, 55], [4, 8], [4, 17], [4, 64], [5, 6], [5, 25], [5, 49], [5, 56], [6, 7], [6, 34], [6, 42], [7, 8], [7, 19], [7, 59], [8, 12], [8, 21], [9, 10], [9, 29], [9, 53], [9, 60], [10, 11], [10, 38], [10, 46], [11, 12], [11, 23], [11, 63], [12, 16], [12, 25], [13, 14], [13, 33], [13, 57], [13, 64], [14, 15], [14, 42], [14, 50], [15, 16], [15, 27], [16, 20], [16, 29], [17, 18], [17, 37], [17, 61], [18, 19], [18, 46], [18, 54], [19, 20], [19, 31], [20, 24], [20, 33], [21, 22], [21, 41], [22, 23], [22, 50], [22, 58], [23, 24], [23, 35], [24, 28], [24, 37], [25, 26], [25, 45], [26, 27], [26, 54], [26, 62], [27, 28], [27, 39], [28, 32], [28, 41], [29, 30], [29, 49], [30, 31], [30, 58], [31, 32], [31, 43], [32, 36], [32, 45], [33, 34], [33, 53], [34, 35], [34, 62], [35, 36], [35, 47], [36, 40], [36, 49], [37, 38], [37, 57], [38, 39], [39, 40], [39, 51], [40, 44], [40, 53], [41, 42], [41, 61], [42, 43], [43, 44], [43, 55], [44, 48], [44, 57], [45, 46], [46, 47], [47, 48], [47, 59], [48, 52], [48, 61], [49, 50], [50, 51], [51, 52], [51, 63], [52, 56], [53, 54], [54, 55], [55, 56], [56, 60], [57, 58], [58, 59], [59, 60], [60, 64], [61, 62], [62, 63], [63, 64]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/064_011.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 064_011 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
