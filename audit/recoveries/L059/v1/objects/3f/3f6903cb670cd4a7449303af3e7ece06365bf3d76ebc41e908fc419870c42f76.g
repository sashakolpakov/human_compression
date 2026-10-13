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
D:=P177Graph("066_002",66,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65],[[1, 2], [1, 24], [1, 44], [1, 66], [2, 3], [2, 25], [2, 45], [3, 4], [3, 26], [3, 46], [4, 5], [4, 27], [4, 47], [5, 6], [5, 28], [5, 48], [6, 7], [6, 29], [6, 49], [7, 8], [7, 30], [7, 50], [8, 9], [8, 31], [8, 51], [9, 10], [9, 32], [9, 52], [10, 11], [10, 33], [10, 53], [11, 12], [11, 34], [11, 54], [12, 13], [12, 35], [12, 55], [13, 14], [13, 36], [13, 56], [14, 15], [14, 37], [14, 57], [15, 16], [15, 38], [15, 58], [16, 17], [16, 39], [16, 59], [17, 18], [17, 40], [17, 60], [18, 19], [18, 41], [18, 61], [19, 20], [19, 42], [19, 62], [20, 21], [20, 43], [20, 63], [21, 22], [21, 44], [21, 64], [22, 23], [22, 45], [22, 65], [23, 24], [23, 46], [23, 66], [24, 25], [24, 47], [25, 26], [25, 48], [26, 27], [26, 49], [27, 28], [27, 50], [28, 29], [28, 51], [29, 30], [29, 52], [30, 31], [30, 53], [31, 32], [31, 54], [32, 33], [32, 55], [33, 34], [33, 56], [34, 35], [34, 57], [35, 36], [35, 58], [36, 37], [36, 59], [37, 38], [37, 60], [38, 39], [38, 61], [39, 40], [39, 62], [40, 41], [40, 63], [41, 42], [41, 64], [42, 43], [42, 65], [43, 44], [43, 66], [44, 45], [45, 46], [46, 47], [47, 48], [48, 49], [49, 50], [50, 51], [51, 52], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66]]);;
R:=P177Census(D);;Need(Size(R.F)=264);;
PrintTo("current_c4_descent/066_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 066_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
