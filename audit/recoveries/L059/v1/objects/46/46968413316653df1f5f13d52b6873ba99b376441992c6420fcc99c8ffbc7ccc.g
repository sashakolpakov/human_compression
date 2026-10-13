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
D:=P177Graph("120_032",120,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 85, 86, 87, 88, 89, 90, 91, 92, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 29], [1, 30], [1, 106], [1, 107], [2, 29], [2, 30], [2, 96], [2, 97], [3, 39], [3, 40], [3, 96], [3, 97], [4, 39], [4, 40], [4, 106], [4, 107], [5, 36], [5, 37], [5, 81], [5, 82], [6, 46], [6, 47], [6, 81], [6, 82], [7, 46], [7, 47], [7, 71], [7, 72], [8, 36], [8, 37], [8, 71], [8, 72], [9, 76], [9, 77], [9, 93], [9, 94], [10, 66], [10, 67], [10, 93], [10, 94], [11, 66], [11, 67], [11, 103], [11, 104], [12, 76], [12, 77], [12, 103], [12, 104], [13, 70], [13, 71], [13, 107], [13, 108], [14, 80], [14, 81], [14, 107], [14, 108], [15, 80], [15, 81], [15, 97], [15, 98], [16, 70], [16, 71], [16, 97], [16, 98], [17, 40], [17, 41], [17, 65], [17, 66], [18, 30], [18, 31], [18, 65], [18, 66], [19, 30], [19, 31], [19, 75], [19, 76], [20, 40], [20, 41], [20, 75], [20, 76], [21, 45], [21, 46], [21, 102], [21, 103], [22, 45], [22, 46], [22, 93], [22, 112], [23, 35], [23, 36], [23, 93], [23, 112], [24, 35], [24, 36], [24, 102], [24, 103], [25, 74], [25, 75], [25, 111], [25, 112], [26, 65], [26, 84], [26, 111], [26, 112], [27, 65], [27, 84], [27, 101], [27, 102], [28, 74], [28, 75], [28, 101], [28, 102], [29, 114], [29, 115], [31, 59], [31, 60], [32, 59], [32, 60], [32, 61], [32, 64], [33, 55], [33, 56], [33, 61], [33, 64], [34, 49], [34, 52], [34, 55], [34, 56], [35, 49], [35, 52], [37, 119], [37, 120], [38, 113], [38, 116], [38, 119], [38, 120], [39, 113], [39, 116], [41, 57], [41, 58], [42, 57], [42, 58], [42, 62], [42, 63], [43, 53], [43, 54], [43, 62], [43, 63], [44, 50], [44, 51], [44, 53], [44, 54], [45, 50], [45, 51], [47, 117], [47, 118], [48, 114], [48, 115], [48, 117], [48, 118], [49, 79], [49, 80], [50, 79], [50, 80], [51, 69], [51, 70], [52, 69], [52, 70], [53, 100], [53, 101], [54, 110], [54, 111], [55, 110], [55, 111], [56, 100], [56, 101], [57, 98], [57, 99], [58, 108], [58, 109], [59, 108], [59, 109], [60, 98], [60, 99], [61, 77], [61, 78], [62, 77], [62, 78], [63, 67], [63, 68], [64, 67], [64, 68], [68, 89], [68, 92], [69, 89], [69, 92], [72, 85], [72, 88], [73, 85], [73, 88], [73, 115], [73, 116], [74, 115], [74, 116], [78, 90], [78, 91], [79, 90], [79, 91], [82, 86], [82, 87], [83, 86], [83, 87], [83, 113], [83, 114], [84, 113], [84, 114], [85, 109], [85, 110], [86, 109], [86, 110], [87, 99], [87, 100], [88, 99], [88, 100], [89, 105], [89, 106], [90, 105], [90, 106], [91, 95], [91, 96], [92, 95], [92, 96], [94, 118], [94, 119], [95, 118], [95, 119], [104, 117], [104, 120], [105, 117], [105, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=480);;
PrintTo("current_c4_descent/120_032.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_032 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
