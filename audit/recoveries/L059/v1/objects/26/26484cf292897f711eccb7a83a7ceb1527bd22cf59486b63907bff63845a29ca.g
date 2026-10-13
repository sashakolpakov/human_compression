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
D:=P177Graph("144_022",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 94], [1, 107], [1, 119], [1, 124], [2, 94], [2, 107], [2, 132], [2, 143], [3, 86], [3, 114], [3, 122], [3, 126], [4, 86], [4, 114], [4, 129], [4, 131], [5, 99], [5, 119], [5, 124], [5, 131], [6, 81], [6, 90], [6, 92], [6, 118], [7, 78], [7, 92], [7, 99], [7, 118], [8, 103], [8, 110], [8, 121], [8, 125], [9, 79], [9, 97], [9, 102], [9, 113], [10, 103], [10, 110], [10, 135], [10, 140], [11, 80], [11, 97], [11, 102], [11, 132], [12, 81], [12, 122], [12, 132], [12, 143], [13, 88], [13, 122], [13, 126], [13, 135], [14, 77], [14, 95], [14, 96], [14, 112], [15, 84], [15, 98], [15, 100], [15, 109], [16, 74], [16, 77], [16, 88], [16, 95], [17, 73], [17, 84], [17, 109], [17, 143], [18, 82], [18, 101], [18, 105], [18, 111], [19, 93], [19, 104], [19, 117], [19, 120], [20, 98], [20, 100], [20, 136], [20, 138], [21, 105], [21, 111], [21, 134], [21, 142], [22, 93], [22, 104], [22, 127], [22, 136], [23, 87], [23, 124], [23, 136], [23, 138], [24, 112], [24, 121], [24, 129], [24, 131], [25, 79], [25, 99], [25, 100], [25, 131], [26, 74], [26, 81], [26, 90], [26, 140], [27, 78], [27, 96], [27, 99], [27, 125], [28, 121], [28, 125], [28, 128], [28, 134], [29, 79], [29, 113], [29, 127], [29, 144], [30, 83], [30, 89], [30, 91], [30, 115], [31, 76], [31, 85], [31, 108], [31, 123], [32, 75], [32, 87], [32, 106], [32, 116], [33, 83], [33, 89], [33, 128], [33, 137], [34, 85], [34, 108], [34, 138], [34, 144], [35, 116], [35, 119], [35, 127], [35, 144], [36, 78], [36, 87], [36, 116], [36, 129], [37, 117], [37, 120], [37, 130], [37, 141], [38, 73], [38, 75], [38, 80], [38, 106], [39, 82], [39, 101], [39, 130], [39, 133], [40, 84], [40, 102], [40, 130], [40, 141], [41, 73], [41, 80], [41, 90], [41, 126], [42, 75], [42, 88], [42, 94], [42, 135], [43, 101], [43, 115], [43, 135], [43, 140], [44, 76], [44, 80], [44, 117], [44, 132], [45, 81], [45, 98], [45, 113], [45, 122], [46, 96], [46, 112], [46, 137], [46, 142], [47, 74], [47, 82], [47, 88], [47, 91], [48, 73], [48, 120], [48, 123], [48, 143], [49, 76], [49, 123], [49, 133], [49, 139], [50, 91], [50, 115], [50, 139], [50, 141], [51, 97], [51, 109], [51, 133], [51, 139], [52, 74], [52, 106], [52, 107], [52, 140], [53, 104], [53, 108], [53, 134], [53, 142], [54, 86], [54, 118], [54, 128], [54, 134], [55, 78], [55, 98], [55, 113], [55, 129], [56, 75], [56, 94], [56, 96], [56, 125], [57, 83], [57, 111], [57, 127], [57, 136], [58, 76], [58, 87], [58, 117], [58, 124], [59, 106], [59, 107], [59, 112], [59, 121], [60, 79], [60, 90], [60, 100], [60, 126], [61, 85], [61, 93], [61, 128], [61, 137], [62, 89], [62, 105], [62, 138], [62, 144], [63, 116], [63, 119], [63, 120], [63, 123], [64, 92], [64, 114], [64, 137], [64, 142], [65, 77], [65, 103], [65, 130], [65, 133], [66, 92], [66, 101], [66, 114], [66, 115], [67, 82], [67, 86], [67, 91], [67, 118], [68, 84], [68, 89], [68, 102], [68, 105], [69, 95], [69, 110], [69, 139], [69, 141], [70, 83], [70, 97], [70, 109], [70, 111], [71, 95], [71, 104], [71, 108], [71, 110], [72, 77], [72, 85], [72, 93], [72, 103]]);;
R:=P177Census(D);;Need(Size(R.F)=4608);;
PrintTo("current_c4_descent/144_022.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_022 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
