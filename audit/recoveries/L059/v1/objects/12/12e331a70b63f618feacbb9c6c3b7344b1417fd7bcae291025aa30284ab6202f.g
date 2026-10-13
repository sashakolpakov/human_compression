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
D:=P177Graph("144_004",144,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109, 111, 113, 115, 117, 119, 121, 123, 125, 127, 129, 131, 133, 135, 137, 139, 141, 143],[[1, 50], [1, 96], [1, 98], [1, 144], [2, 49], [2, 51], [2, 97], [2, 99], [3, 50], [3, 52], [3, 98], [3, 100], [4, 51], [4, 53], [4, 99], [4, 101], [5, 52], [5, 54], [5, 100], [5, 102], [6, 53], [6, 55], [6, 101], [6, 103], [7, 54], [7, 56], [7, 102], [7, 104], [8, 55], [8, 57], [8, 103], [8, 105], [9, 56], [9, 58], [9, 104], [9, 106], [10, 57], [10, 59], [10, 105], [10, 107], [11, 58], [11, 60], [11, 106], [11, 108], [12, 59], [12, 61], [12, 107], [12, 109], [13, 60], [13, 62], [13, 108], [13, 110], [14, 61], [14, 63], [14, 109], [14, 111], [15, 62], [15, 64], [15, 110], [15, 112], [16, 63], [16, 65], [16, 111], [16, 113], [17, 64], [17, 66], [17, 112], [17, 114], [18, 65], [18, 67], [18, 113], [18, 115], [19, 66], [19, 68], [19, 114], [19, 116], [20, 67], [20, 69], [20, 115], [20, 117], [21, 68], [21, 70], [21, 116], [21, 118], [22, 69], [22, 71], [22, 117], [22, 119], [23, 70], [23, 72], [23, 118], [23, 120], [24, 71], [24, 73], [24, 119], [24, 121], [25, 72], [25, 74], [25, 120], [25, 122], [26, 73], [26, 75], [26, 121], [26, 123], [27, 74], [27, 76], [27, 122], [27, 124], [28, 75], [28, 77], [28, 123], [28, 125], [29, 76], [29, 78], [29, 124], [29, 126], [30, 77], [30, 79], [30, 125], [30, 127], [31, 78], [31, 80], [31, 126], [31, 128], [32, 79], [32, 81], [32, 127], [32, 129], [33, 80], [33, 82], [33, 128], [33, 130], [34, 81], [34, 83], [34, 129], [34, 131], [35, 82], [35, 84], [35, 130], [35, 132], [36, 83], [36, 85], [36, 131], [36, 133], [37, 84], [37, 86], [37, 132], [37, 134], [38, 85], [38, 87], [38, 133], [38, 135], [39, 86], [39, 88], [39, 134], [39, 136], [40, 87], [40, 89], [40, 135], [40, 137], [41, 88], [41, 90], [41, 136], [41, 138], [42, 89], [42, 91], [42, 137], [42, 139], [43, 90], [43, 92], [43, 138], [43, 140], [44, 91], [44, 93], [44, 139], [44, 141], [45, 92], [45, 94], [45, 140], [45, 142], [46, 93], [46, 95], [46, 141], [46, 143], [47, 94], [47, 96], [47, 142], [47, 144], [48, 49], [48, 95], [48, 97], [48, 143], [49, 98], [49, 144], [50, 97], [50, 99], [51, 98], [51, 100], [52, 99], [52, 101], [53, 100], [53, 102], [54, 101], [54, 103], [55, 102], [55, 104], [56, 103], [56, 105], [57, 104], [57, 106], [58, 105], [58, 107], [59, 106], [59, 108], [60, 107], [60, 109], [61, 108], [61, 110], [62, 109], [62, 111], [63, 110], [63, 112], [64, 111], [64, 113], [65, 112], [65, 114], [66, 113], [66, 115], [67, 114], [67, 116], [68, 115], [68, 117], [69, 116], [69, 118], [70, 117], [70, 119], [71, 118], [71, 120], [72, 119], [72, 121], [73, 120], [73, 122], [74, 121], [74, 123], [75, 122], [75, 124], [76, 123], [76, 125], [77, 124], [77, 126], [78, 125], [78, 127], [79, 126], [79, 128], [80, 127], [80, 129], [81, 128], [81, 130], [82, 129], [82, 131], [83, 130], [83, 132], [84, 131], [84, 133], [85, 132], [85, 134], [86, 133], [86, 135], [87, 134], [87, 136], [88, 135], [88, 137], [89, 136], [89, 138], [90, 137], [90, 139], [91, 138], [91, 140], [92, 139], [92, 141], [93, 140], [93, 142], [94, 141], [94, 143], [95, 142], [95, 144], [96, 97], [96, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_004.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_004 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
