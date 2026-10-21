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
D:=P177Graph("144_069",144,[1, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 136], [2, 137], [2, 141], [3, 133], [3, 140], [3, 144], [4, 134], [4, 139], [4, 142], [5, 135], [5, 138], [5, 143], [6, 75], [6, 79], [6, 83], [6, 87], [7, 76], [7, 80], [7, 84], [7, 89], [8, 77], [8, 82], [8, 85], [8, 90], [9, 78], [9, 81], [9, 86], [9, 88], [10, 38], [10, 59], [10, 63], [10, 85], [11, 38], [11, 60], [11, 64], [11, 86], [12, 38], [12, 62], [12, 66], [12, 84], [13, 38], [13, 61], [13, 65], [13, 83], [14, 40], [14, 47], [14, 50], [14, 76], [15, 42], [15, 48], [15, 50], [15, 78], [16, 41], [16, 48], [16, 49], [16, 75], [17, 39], [17, 47], [17, 49], [17, 77], [18, 39], [18, 51], [18, 53], [18, 55], [19, 40], [19, 51], [19, 54], [19, 58], [20, 42], [20, 52], [20, 54], [20, 56], [21, 41], [21, 52], [21, 53], [21, 57], [22, 44], [22, 62], [22, 68], [22, 91], [23, 43], [23, 59], [23, 70], [23, 94], [24, 44], [24, 60], [24, 69], [24, 93], [25, 43], [25, 61], [25, 67], [25, 92], [26, 46], [26, 58], [26, 64], [26, 82], [27, 46], [27, 55], [27, 65], [27, 80], [28, 45], [28, 56], [28, 66], [28, 79], [29, 45], [29, 57], [29, 63], [29, 81], [30, 42], [30, 44], [30, 71], [30, 87], [31, 39], [31, 43], [31, 72], [31, 89], [32, 40], [32, 44], [32, 72], [32, 90], [33, 41], [33, 43], [33, 71], [33, 88], [34, 41], [34, 46], [34, 68], [34, 73], [35, 39], [35, 45], [35, 69], [35, 73], [36, 42], [36, 46], [36, 70], [36, 74], [37, 40], [37, 45], [37, 67], [37, 74], [47, 97], [47, 99], [48, 98], [48, 100], [49, 129], [49, 132], [50, 130], [50, 131], [51, 109], [51, 111], [52, 110], [52, 112], [53, 105], [53, 106], [54, 107], [54, 108], [55, 113], [55, 130], [56, 114], [56, 129], [57, 116], [57, 131], [58, 115], [58, 132], [59, 117], [59, 129], [60, 118], [60, 130], [61, 120], [61, 132], [62, 119], [62, 131], [63, 121], [63, 126], [64, 124], [64, 125], [65, 122], [65, 127], [66, 123], [66, 128], [67, 110], [67, 113], [68, 109], [68, 114], [69, 112], [69, 115], [70, 111], [70, 116], [71, 125], [71, 127], [72, 126], [72, 128], [73, 101], [73, 102], [74, 103], [74, 104], [75, 107], [75, 126], [76, 106], [76, 125], [77, 108], [77, 127], [78, 105], [78, 128], [79, 106], [79, 118], [80, 107], [80, 117], [81, 108], [81, 120], [82, 105], [82, 119], [83, 104], [83, 109], [84, 101], [84, 110], [85, 103], [85, 112], [86, 102], [86, 111], [87, 97], [87, 101], [88, 99], [88, 103], [89, 98], [89, 104], [90, 100], [90, 102], [91, 98], [91, 113], [91, 121], [92, 97], [92, 114], [92, 124], [93, 99], [93, 116], [93, 122], [94, 100], [94, 115], [94, 123], [95, 121], [95, 122], [95, 123], [95, 124], [96, 117], [96, 118], [96, 119], [96, 120], [97, 140], [98, 139], [99, 137], [100, 138], [101, 141], [102, 142], [103, 144], [104, 143], [105, 141], [106, 142], [107, 144], [108, 143], [109, 137], [110, 138], [111, 140], [112, 139], [113, 133], [114, 134], [115, 136], [116, 135], [117, 137], [118, 138], [119, 140], [120, 139], [121, 141], [122, 142], [123, 144], [124, 143], [125, 133], [126, 134], [127, 136], [128, 135], [129, 133], [130, 134], [131, 136], [132, 135]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_069.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_069 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
