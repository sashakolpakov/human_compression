Need:=function(ok) if not ok then Error("L059 cutoff probe invalid"); fi; end;;
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


D:=P177Graph("144_057",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 74], [1, 91], [1, 92], [2, 73], [2, 74], [2, 85], [2, 86], [3, 79], [3, 80], [3, 85], [3, 86], [4, 79], [4, 80], [4, 91], [4, 92], [5, 97], [5, 98], [5, 115], [5, 116], [6, 97], [6, 98], [6, 109], [6, 110], [7, 103], [7, 104], [7, 109], [7, 110], [8, 103], [8, 104], [8, 115], [8, 116], [9, 121], [9, 122], [9, 139], [9, 140], [10, 121], [10, 122], [10, 133], [10, 134], [11, 127], [11, 128], [11, 133], [11, 134], [12, 127], [12, 128], [12, 139], [12, 140], [13, 76], [13, 77], [13, 94], [13, 95], [14, 76], [14, 77], [14, 88], [14, 89], [15, 82], [15, 83], [15, 88], [15, 89], [16, 82], [16, 83], [16, 94], [16, 95], [17, 100], [17, 101], [17, 118], [17, 119], [18, 100], [18, 101], [18, 112], [18, 113], [19, 106], [19, 107], [19, 112], [19, 113], [20, 106], [20, 107], [20, 118], [20, 119], [21, 124], [21, 125], [21, 142], [21, 143], [22, 124], [22, 125], [22, 136], [22, 137], [23, 130], [23, 131], [23, 136], [23, 137], [24, 130], [24, 131], [24, 142], [24, 143], [25, 98], [25, 99], [25, 143], [25, 144], [26, 98], [26, 99], [26, 137], [26, 138], [27, 104], [27, 105], [27, 137], [27, 138], [28, 104], [28, 105], [28, 143], [28, 144], [29, 74], [29, 75], [29, 128], [29, 129], [30, 74], [30, 75], [30, 122], [30, 123], [31, 80], [31, 81], [31, 122], [31, 123], [32, 80], [32, 81], [32, 128], [32, 129], [33, 89], [33, 90], [33, 116], [33, 117], [34, 89], [34, 90], [34, 110], [34, 111], [35, 95], [35, 96], [35, 110], [35, 111], [36, 95], [36, 96], [36, 116], [36, 117], [37, 101], [37, 102], [37, 140], [37, 141], [38, 101], [38, 102], [38, 134], [38, 135], [39, 107], [39, 108], [39, 134], [39, 135], [40, 107], [40, 108], [40, 140], [40, 141], [41, 77], [41, 78], [41, 131], [41, 132], [42, 77], [42, 78], [42, 125], [42, 126], [43, 83], [43, 84], [43, 125], [43, 126], [44, 83], [44, 84], [44, 131], [44, 132], [45, 86], [45, 87], [45, 119], [45, 120], [46, 86], [46, 87], [46, 113], [46, 114], [47, 92], [47, 93], [47, 113], [47, 114], [48, 92], [48, 93], [48, 119], [48, 120], [49, 114], [49, 115], [49, 129], [49, 130], [50, 114], [50, 115], [50, 123], [50, 124], [51, 109], [51, 120], [51, 123], [51, 124], [52, 109], [52, 120], [52, 129], [52, 130], [53, 90], [53, 91], [53, 133], [53, 144], [54, 90], [54, 91], [54, 138], [54, 139], [55, 85], [55, 96], [55, 138], [55, 139], [56, 85], [56, 96], [56, 133], [56, 144], [57, 75], [57, 76], [57, 97], [57, 108], [58, 75], [58, 76], [58, 102], [58, 103], [59, 81], [59, 82], [59, 102], [59, 103], [60, 81], [60, 82], [60, 97], [60, 108], [61, 111], [61, 112], [61, 121], [61, 132], [62, 111], [62, 112], [62, 126], [62, 127], [63, 117], [63, 118], [63, 126], [63, 127], [64, 117], [64, 118], [64, 121], [64, 132], [65, 87], [65, 88], [65, 141], [65, 142], [66, 87], [66, 88], [66, 135], [66, 136], [67, 93], [67, 94], [67, 135], [67, 136], [68, 93], [68, 94], [68, 141], [68, 142], [69, 78], [69, 79], [69, 105], [69, 106], [70, 78], [70, 79], [70, 99], [70, 100], [71, 73], [71, 84], [71, 99], [71, 100], [72, 73], [72, 84], [72, 105], [72, 106]]);;
R:=P177Census(D);;
Need(Size(R.F)=9216);;
PrintTo("quartic_cutoff_probe/144_057.g","L059Result := ",R,";\n");
Print("L059_CUTOFF_COMPLETE 144_057 ",Length(R.witnesses),"\n");
QUIT;
