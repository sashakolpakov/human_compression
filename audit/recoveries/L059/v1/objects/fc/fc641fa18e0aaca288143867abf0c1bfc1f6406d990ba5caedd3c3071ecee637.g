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
D:=P177Graph("140_008",140,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70],[[1, 71], [1, 72], [1, 113], [1, 114], [2, 71], [2, 72], [2, 99], [2, 100], [3, 99], [3, 100], [3, 127], [3, 128], [4, 85], [4, 86], [4, 127], [4, 128], [5, 85], [5, 86], [5, 113], [5, 114], [6, 72], [6, 73], [6, 128], [6, 129], [7, 72], [7, 73], [7, 86], [7, 87], [8, 86], [8, 87], [8, 100], [8, 101], [9, 100], [9, 101], [9, 114], [9, 115], [10, 114], [10, 115], [10, 128], [10, 129], [11, 73], [11, 74], [11, 115], [11, 116], [12, 73], [12, 74], [12, 101], [12, 102], [13, 101], [13, 102], [13, 129], [13, 130], [14, 87], [14, 88], [14, 129], [14, 130], [15, 87], [15, 88], [15, 115], [15, 116], [16, 74], [16, 75], [16, 130], [16, 131], [17, 74], [17, 75], [17, 88], [17, 89], [18, 88], [18, 89], [18, 102], [18, 103], [19, 102], [19, 103], [19, 116], [19, 117], [20, 116], [20, 117], [20, 130], [20, 131], [21, 75], [21, 76], [21, 117], [21, 118], [22, 75], [22, 76], [22, 103], [22, 104], [23, 103], [23, 104], [23, 131], [23, 132], [24, 89], [24, 90], [24, 131], [24, 132], [25, 89], [25, 90], [25, 117], [25, 118], [26, 76], [26, 77], [26, 132], [26, 133], [27, 76], [27, 77], [27, 90], [27, 91], [28, 90], [28, 91], [28, 104], [28, 105], [29, 104], [29, 105], [29, 118], [29, 119], [30, 118], [30, 119], [30, 132], [30, 133], [31, 77], [31, 78], [31, 119], [31, 120], [32, 77], [32, 78], [32, 105], [32, 106], [33, 105], [33, 106], [33, 133], [33, 134], [34, 91], [34, 92], [34, 133], [34, 134], [35, 91], [35, 92], [35, 119], [35, 120], [36, 78], [36, 79], [36, 134], [36, 135], [37, 78], [37, 79], [37, 92], [37, 93], [38, 92], [38, 93], [38, 106], [38, 107], [39, 106], [39, 107], [39, 120], [39, 121], [40, 120], [40, 121], [40, 134], [40, 135], [41, 79], [41, 80], [41, 121], [41, 122], [42, 79], [42, 80], [42, 107], [42, 108], [43, 107], [43, 108], [43, 135], [43, 136], [44, 93], [44, 94], [44, 135], [44, 136], [45, 93], [45, 94], [45, 121], [45, 122], [46, 80], [46, 81], [46, 136], [46, 137], [47, 80], [47, 81], [47, 94], [47, 95], [48, 94], [48, 95], [48, 108], [48, 109], [49, 108], [49, 109], [49, 122], [49, 123], [50, 122], [50, 123], [50, 136], [50, 137], [51, 81], [51, 82], [51, 123], [51, 124], [52, 81], [52, 82], [52, 109], [52, 110], [53, 109], [53, 110], [53, 137], [53, 138], [54, 95], [54, 96], [54, 137], [54, 138], [55, 95], [55, 96], [55, 123], [55, 124], [56, 82], [56, 83], [56, 138], [56, 139], [57, 82], [57, 83], [57, 96], [57, 97], [58, 96], [58, 97], [58, 110], [58, 111], [59, 110], [59, 111], [59, 124], [59, 125], [60, 124], [60, 125], [60, 138], [60, 139], [61, 83], [61, 84], [61, 125], [61, 126], [62, 83], [62, 84], [62, 111], [62, 112], [63, 111], [63, 112], [63, 139], [63, 140], [64, 97], [64, 98], [64, 139], [64, 140], [65, 97], [65, 98], [65, 125], [65, 126], [66, 71], [66, 84], [66, 127], [66, 140], [67, 71], [67, 84], [67, 85], [67, 98], [68, 85], [68, 98], [68, 99], [68, 112], [69, 99], [69, 112], [69, 113], [69, 126], [70, 113], [70, 126], [70, 127], [70, 140]]);;
R:=P177Census(D);;Need(Size(R.F)=280);;
PrintTo("current_c4_descent/140_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 140_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
