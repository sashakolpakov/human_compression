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
D:=P177Graph("128_038",128,[1, 3, 4, 6, 10, 11, 13, 16, 18, 19, 20, 22, 26, 28, 30, 32, 33, 34, 36, 38, 40, 45, 46, 48, 51, 56, 58, 59, 61, 62, 63, 65, 66, 67, 69, 70, 71, 72, 73, 76, 77, 84, 90, 91, 94, 95, 96, 97, 98, 99, 101, 102, 103, 104, 105, 108, 115, 121, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 5], [1, 112], [1, 117], [2, 6], [2, 13], [2, 48], [3, 7], [3, 14], [3, 106], [3, 120], [4, 8], [4, 15], [4, 100], [4, 119], [5, 16], [5, 30], [5, 48], [6, 17], [6, 31], [6, 47], [7, 18], [7, 28], [7, 32], [8, 19], [8, 26], [8, 33], [9, 20], [9, 34], [9, 121], [9, 128], [10, 21], [10, 35], [10, 113], [10, 116], [11, 21], [11, 35], [11, 110], [11, 114], [12, 22], [12, 36], [12, 115], [12, 126], [13, 37], [13, 47], [13, 49], [14, 20], [14, 28], [14, 34], [15, 26], [15, 38], [15, 46], [16, 24], [16, 39], [16, 50], [17, 40], [17, 51], [17, 56], [18, 23], [18, 41], [18, 52], [19, 29], [19, 42], [19, 53], [20, 43], [20, 54], [21, 22], [21, 36], [22, 44], [22, 55], [23, 32], [23, 123], [23, 127], [24, 30], [24, 121], [24, 128], [25, 45], [25, 56], [25, 124], [25, 125], [26, 111], [26, 122], [27, 38], [27, 46], [27, 124], [27, 125], [28, 93], [28, 107], [29, 33], [29, 115], [29, 126], [30, 57], [30, 64], [31, 56], [31, 58], [31, 66], [32, 44], [32, 55], [33, 37], [33, 49], [34, 42], [34, 53], [35, 45], [35, 56], [36, 57], [36, 64], [37, 59], [37, 67], [38, 39], [38, 50], [39, 40], [39, 51], [40, 60], [40, 68], [41, 46], [41, 61], [41, 69], [42, 62], [42, 70], [43, 45], [43, 63], [43, 71], [44, 65], [44, 72], [45, 54], [46, 52], [47, 123], [47, 127], [48, 109], [48, 118], [49, 73], [49, 76], [50, 62], [50, 70], [51, 74], [51, 82], [52, 73], [52, 76], [53, 65], [53, 72], [54, 61], [54, 69], [55, 58], [55, 66], [57, 59], [57, 67], [58, 75], [58, 83], [59, 60], [59, 68], [60, 77], [60, 84], [61, 78], [61, 85], [62, 79], [62, 86], [63, 64], [63, 80], [63, 87], [64, 71], [65, 81], [65, 88], [66, 89], [66, 92], [67, 81], [67, 88], [68, 90], [68, 98], [69, 74], [69, 82], [70, 80], [70, 87], [71, 89], [71, 92], [72, 78], [72, 85], [73, 75], [73, 83], [74, 91], [74, 99], [75, 77], [75, 84], [76, 79], [76, 86], [77, 93], [77, 100], [78, 94], [78, 101], [79, 95], [79, 102], [80, 96], [80, 103], [81, 97], [81, 104], [82, 105], [82, 108], [83, 94], [83, 101], [84, 106], [84, 113], [85, 96], [85, 103], [86, 105], [86, 108], [87, 90], [87, 98], [88, 95], [88, 102], [89, 91], [89, 99], [90, 107], [90, 114], [91, 93], [91, 100], [92, 97], [92, 104], [93, 115], [94, 109], [94, 116], [95, 110], [95, 117], [96, 111], [96, 118], [97, 112], [97, 119], [98, 120], [98, 122], [99, 111], [99, 118], [100, 121], [101, 112], [101, 119], [102, 106], [102, 113], [103, 110], [103, 117], [104, 120], [104, 122], [105, 107], [105, 114], [106, 125], [107, 115], [108, 109], [108, 116], [109, 126], [110, 127], [111, 123], [112, 124], [113, 128], [114, 127], [116, 128], [117, 124], [118, 126], [119, 121], [120, 125], [122, 123]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_038.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_038 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
