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
D:=P177Graph("120_057",120,[1, 2, 4, 5, 13, 16, 20, 21, 22, 27, 29, 30, 31, 33, 34, 36, 38, 39, 43, 44, 45, 47, 51, 52, 57, 60, 61, 62, 63, 68, 69, 70, 72, 73, 75, 77, 81, 83, 84, 85, 87, 88, 90, 91, 94, 95, 98, 100, 101, 102, 106, 109, 110, 111, 113, 114, 115, 117, 118, 120],[[1, 10], [1, 67], [1, 80], [1, 107], [2, 3], [2, 6], [2, 59], [2, 93], [3, 5], [3, 85], [3, 113], [4, 12], [4, 14], [4, 78], [4, 116], [5, 10], [5, 41], [5, 89], [6, 33], [6, 81], [6, 91], [7, 61], [7, 72], [7, 87], [7, 113], [8, 22], [8, 68], [8, 69], [8, 83], [9, 27], [9, 36], [9, 52], [9, 91], [10, 77], [10, 101], [11, 16], [11, 44], [11, 87], [11, 115], [12, 90], [12, 102], [12, 114], [13, 65], [13, 66], [13, 67], [13, 96], [14, 101], [14, 110], [14, 117], [15, 60], [15, 73], [15, 81], [15, 102], [16, 42], [16, 96], [16, 119], [17, 27], [17, 63], [17, 69], [17, 95], [18, 29], [18, 36], [18, 69], [18, 88], [19, 38], [19, 77], [19, 106], [19, 113], [20, 37], [20, 55], [20, 71], [20, 86], [21, 96], [21, 97], [21, 103], [21, 116], [22, 41], [22, 56], [22, 80], [23, 30], [23, 88], [23, 91], [23, 95], [24, 36], [24, 68], [24, 70], [24, 117], [25, 33], [25, 51], [25, 95], [25, 109], [26, 34], [26, 43], [26, 70], [26, 100], [27, 46], [27, 71], [28, 57], [28, 62], [28, 111], [28, 114], [29, 32], [29, 41], [29, 78], [30, 32], [30, 76], [30, 97], [31, 37], [31, 50], [31, 56], [31, 108], [32, 52], [32, 63], [33, 53], [33, 58], [34, 48], [34, 49], [34, 79], [35, 36], [35, 45], [35, 84], [35, 100], [37, 90], [37, 95], [38, 48], [38, 64], [38, 107], [39, 42], [39, 66], [39, 79], [39, 86], [40, 47], [40, 62], [40, 63], [40, 90], [41, 117], [42, 47], [42, 73], [43, 53], [43, 55], [43, 82], [44, 86], [44, 99], [44, 104], [45, 49], [45, 64], [45, 74], [46, 73], [46, 87], [46, 100], [47, 71], [47, 103], [48, 111], [48, 118], [49, 68], [49, 114], [50, 98], [50, 109], [50, 110], [51, 55], [51, 93], [51, 99], [52, 74], [52, 112], [53, 90], [53, 110], [54, 61], [54, 62], [54, 68], [54, 118], [55, 98], [56, 118], [56, 120], [57, 64], [57, 112], [57, 116], [58, 84], [58, 101], [58, 102], [59, 60], [59, 101], [59, 106], [60, 66], [60, 107], [61, 64], [61, 92], [62, 108], [63, 116], [65, 94], [65, 109], [65, 120], [66, 111], [67, 98], [67, 118], [69, 108], [70, 89], [70, 99], [71, 115], [72, 97], [72, 112], [72, 119], [73, 105], [74, 87], [74, 106], [75, 76], [75, 93], [75, 104], [75, 119], [76, 81], [76, 109], [77, 78], [77, 112], [78, 94], [79, 85], [79, 98], [80, 94], [80, 110], [81, 96], [82, 84], [82, 114], [82, 117], [83, 89], [83, 92], [83, 104], [84, 105], [85, 99], [85, 107], [86, 100], [88, 89], [88, 93], [91, 105], [92, 115], [92, 120], [94, 97], [102, 103], [103, 111], [104, 113], [105, 106], [108, 115], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_057.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_057 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
