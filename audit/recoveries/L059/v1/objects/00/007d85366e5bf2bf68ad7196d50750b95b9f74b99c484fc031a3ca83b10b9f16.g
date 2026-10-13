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
D:=P177Graph("104_006",104,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78],[[1, 27], [1, 52], [1, 81], [1, 102], [2, 27], [2, 28], [2, 82], [2, 103], [3, 28], [3, 29], [3, 83], [3, 104], [4, 29], [4, 30], [4, 79], [4, 84], [5, 30], [5, 31], [5, 80], [5, 85], [6, 31], [6, 32], [6, 81], [6, 86], [7, 32], [7, 33], [7, 82], [7, 87], [8, 33], [8, 34], [8, 83], [8, 88], [9, 34], [9, 35], [9, 84], [9, 89], [10, 35], [10, 36], [10, 85], [10, 90], [11, 36], [11, 37], [11, 86], [11, 91], [12, 37], [12, 38], [12, 87], [12, 92], [13, 38], [13, 39], [13, 88], [13, 93], [14, 39], [14, 40], [14, 89], [14, 94], [15, 40], [15, 41], [15, 90], [15, 95], [16, 41], [16, 42], [16, 91], [16, 96], [17, 42], [17, 43], [17, 92], [17, 97], [18, 43], [18, 44], [18, 93], [18, 98], [19, 44], [19, 45], [19, 94], [19, 99], [20, 45], [20, 46], [20, 95], [20, 100], [21, 46], [21, 47], [21, 96], [21, 101], [22, 47], [22, 48], [22, 97], [22, 102], [23, 48], [23, 49], [23, 98], [23, 103], [24, 49], [24, 50], [24, 99], [24, 104], [25, 50], [25, 51], [25, 79], [25, 100], [26, 51], [26, 52], [26, 80], [26, 101], [27, 56], [27, 77], [28, 57], [28, 78], [29, 53], [29, 58], [30, 54], [30, 59], [31, 55], [31, 60], [32, 56], [32, 61], [33, 57], [33, 62], [34, 58], [34, 63], [35, 59], [35, 64], [36, 60], [36, 65], [37, 61], [37, 66], [38, 62], [38, 67], [39, 63], [39, 68], [40, 64], [40, 69], [41, 65], [41, 70], [42, 66], [42, 71], [43, 67], [43, 72], [44, 68], [44, 73], [45, 69], [45, 74], [46, 70], [46, 75], [47, 71], [47, 76], [48, 72], [48, 77], [49, 73], [49, 78], [50, 53], [50, 74], [51, 54], [51, 75], [52, 55], [52, 76], [53, 91], [53, 92], [54, 92], [54, 93], [55, 93], [55, 94], [56, 94], [56, 95], [57, 95], [57, 96], [58, 96], [58, 97], [59, 97], [59, 98], [60, 98], [60, 99], [61, 99], [61, 100], [62, 100], [62, 101], [63, 101], [63, 102], [64, 102], [64, 103], [65, 103], [65, 104], [66, 79], [66, 104], [67, 79], [67, 80], [68, 80], [68, 81], [69, 81], [69, 82], [70, 82], [70, 83], [71, 83], [71, 84], [72, 84], [72, 85], [73, 85], [73, 86], [74, 86], [74, 87], [75, 87], [75, 88], [76, 88], [76, 89], [77, 89], [77, 90], [78, 90], [78, 91]]);;
R:=P177Census(D);;Need(Size(R.F)=416);;
PrintTo("current_c4_descent/104_006.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 104_006 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
