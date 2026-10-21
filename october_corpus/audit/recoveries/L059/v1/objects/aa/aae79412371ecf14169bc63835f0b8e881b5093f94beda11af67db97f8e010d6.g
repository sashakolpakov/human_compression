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
D:=P177Graph("144_038",144,[1, 3, 4, 6, 9, 11, 12, 14, 17, 19, 20, 22, 25, 26, 27, 31, 32, 35, 37, 38, 40, 44, 49, 50, 54, 55, 56, 58, 59, 61, 63, 66, 68, 69, 70, 71, 73, 75, 76, 78, 80, 82, 83, 86, 88, 89, 90, 93, 96, 97, 99, 102, 105, 109, 110, 111, 113, 114, 115, 116, 117, 118, 119, 122, 123, 124, 125, 128, 130, 131, 137, 139],[[1, 2], [1, 5], [1, 91], [1, 108], [2, 6], [2, 14], [2, 80], [3, 7], [3, 15], [3, 47], [3, 60], [4, 8], [4, 16], [4, 62], [4, 107], [5, 17], [5, 35], [5, 37], [6, 18], [6, 36], [6, 94], [7, 19], [7, 37], [7, 113], [8, 20], [8, 38], [8, 117], [9, 21], [9, 39], [9, 41], [9, 51], [10, 22], [10, 40], [10, 86], [10, 93], [11, 23], [11, 33], [11, 41], [11, 92], [12, 18], [12, 24], [12, 42], [12, 87], [13, 25], [13, 31], [13, 69], [13, 137], [14, 43], [14, 74], [14, 81], [15, 44], [15, 75], [15, 82], [16, 26], [16, 76], [16, 83], [17, 45], [17, 48], [17, 77], [18, 78], [18, 105], [19, 21], [19, 46], [19, 79], [20, 47], [20, 64], [20, 98], [21, 66], [21, 80], [22, 48], [22, 81], [22, 126], [23, 49], [23, 71], [23, 82], [24, 50], [24, 83], [24, 130], [25, 51], [25, 84], [25, 127], [26, 51], [26, 52], [26, 95], [27, 43], [27, 45], [27, 53], [27, 85], [28, 40], [28, 49], [28, 54], [28, 110], [29, 31], [29, 55], [29, 86], [29, 116], [30, 56], [30, 69], [30, 88], [30, 125], [31, 60], [31, 112], [32, 43], [32, 46], [32, 57], [32, 72], [33, 58], [33, 69], [33, 124], [34, 40], [34, 59], [34, 70], [34, 122], [35, 74], [35, 87], [35, 100], [36, 88], [36, 115], [36, 119], [37, 120], [37, 126], [38, 41], [38, 121], [38, 127], [39, 44], [39, 55], [39, 122], [40, 72], [41, 123], [42, 61], [42, 124], [42, 128], [43, 89], [44, 48], [44, 94], [45, 59], [45, 125], [46, 109], [46, 119], [47, 58], [47, 110], [48, 90], [49, 52], [49, 91], [50, 53], [50, 92], [50, 112], [51, 93], [52, 113], [52, 114], [53, 115], [53, 117], [54, 94], [54, 100], [54, 140], [55, 84], [55, 126], [56, 95], [56, 127], [56, 143], [57, 96], [57, 118], [57, 128], [58, 84], [58, 103], [59, 81], [59, 129], [60, 76], [60, 97], [61, 85], [61, 95], [61, 98], [62, 88], [62, 89], [62, 99], [63, 79], [63, 91], [63, 100], [63, 132], [64, 66], [64, 86], [64, 139], [65, 68], [65, 69], [65, 78], [65, 96], [66, 101], [66, 121], [67, 70], [67, 88], [67, 90], [67, 102], [68, 98], [68, 103], [68, 142], [70, 79], [70, 87], [71, 98], [71, 104], [71, 141], [72, 75], [72, 105], [73, 77], [73, 79], [73, 106], [73, 120], [74, 115], [74, 130], [75, 101], [75, 120], [76, 103], [76, 121], [77, 96], [77, 130], [78, 134], [78, 136], [80, 138], [80, 140], [81, 109], [82, 84], [82, 140], [83, 141], [83, 143], [85, 102], [85, 137], [86, 108], [87, 131], [89, 106], [89, 142], [90, 136], [90, 138], [91, 97], [92, 99], [92, 139], [93, 104], [93, 132], [94, 118], [95, 116], [96, 107], [97, 126], [97, 133], [99, 127], [99, 134], [100, 105], [101, 109], [101, 110], [102, 129], [102, 143], [103, 111], [104, 110], [104, 116], [105, 129], [106, 119], [106, 131], [107, 111], [107, 131], [108, 109], [108, 123], [111, 112], [111, 144], [112, 114], [113, 121], [113, 132], [114, 133], [114, 141], [115, 134], [116, 135], [117, 135], [117, 142], [118, 120], [118, 136], [119, 138], [122, 132], [122, 138], [123, 133], [123, 140], [124, 134], [124, 141], [125, 136], [125, 144], [128, 129], [128, 142], [130, 144], [131, 143], [133, 139], [135, 137], [135, 139], [137, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_038.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_038 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
