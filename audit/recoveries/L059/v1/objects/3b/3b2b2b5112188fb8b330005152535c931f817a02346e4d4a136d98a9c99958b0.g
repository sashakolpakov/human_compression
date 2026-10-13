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
D:=P177Graph("078_002",78,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77],[[1, 2], [1, 26], [1, 54], [1, 78], [2, 3], [2, 27], [2, 55], [3, 4], [3, 28], [3, 56], [4, 5], [4, 29], [4, 57], [5, 6], [5, 30], [5, 58], [6, 7], [6, 31], [6, 59], [7, 8], [7, 32], [7, 60], [8, 9], [8, 33], [8, 61], [9, 10], [9, 34], [9, 62], [10, 11], [10, 35], [10, 63], [11, 12], [11, 36], [11, 64], [12, 13], [12, 37], [12, 65], [13, 14], [13, 38], [13, 66], [14, 15], [14, 39], [14, 67], [15, 16], [15, 40], [15, 68], [16, 17], [16, 41], [16, 69], [17, 18], [17, 42], [17, 70], [18, 19], [18, 43], [18, 71], [19, 20], [19, 44], [19, 72], [20, 21], [20, 45], [20, 73], [21, 22], [21, 46], [21, 74], [22, 23], [22, 47], [22, 75], [23, 24], [23, 48], [23, 76], [24, 25], [24, 49], [24, 77], [25, 26], [25, 50], [25, 78], [26, 27], [26, 51], [27, 28], [27, 52], [28, 29], [28, 53], [29, 30], [29, 54], [30, 31], [30, 55], [31, 32], [31, 56], [32, 33], [32, 57], [33, 34], [33, 58], [34, 35], [34, 59], [35, 36], [35, 60], [36, 37], [36, 61], [37, 38], [37, 62], [38, 39], [38, 63], [39, 40], [39, 64], [40, 41], [40, 65], [41, 42], [41, 66], [42, 43], [42, 67], [43, 44], [43, 68], [44, 45], [44, 69], [45, 46], [45, 70], [46, 47], [46, 71], [47, 48], [47, 72], [48, 49], [48, 73], [49, 50], [49, 74], [50, 51], [50, 75], [51, 52], [51, 76], [52, 53], [52, 77], [53, 54], [53, 78], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78]]);;
R:=P177Census(D);;Need(Size(R.F)=312);;
PrintTo("current_c4_descent/078_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 078_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
