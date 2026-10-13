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
D:=P177Graph("144_021",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 94], [1, 107], [1, 119], [1, 124], [2, 73], [2, 84], [2, 94], [2, 107], [3, 86], [3, 114], [3, 122], [3, 126], [4, 78], [4, 86], [4, 95], [4, 114], [5, 95], [5, 119], [5, 124], [5, 131], [6, 80], [6, 88], [6, 89], [6, 117], [7, 103], [7, 112], [7, 121], [7, 125], [8, 79], [8, 98], [8, 101], [8, 109], [9, 88], [9, 117], [9, 130], [9, 131], [10, 74], [10, 93], [10, 103], [10, 112], [11, 84], [11, 98], [11, 101], [11, 133], [12, 73], [12, 84], [12, 89], [12, 126], [13, 93], [13, 122], [13, 126], [13, 135], [14, 76], [14, 97], [14, 99], [14, 113], [15, 83], [15, 96], [15, 100], [15, 108], [16, 82], [16, 102], [16, 106], [16, 111], [17, 90], [17, 104], [17, 116], [17, 120], [18, 79], [18, 109], [18, 136], [18, 138], [19, 76], [19, 99], [19, 135], [19, 140], [20, 73], [20, 83], [20, 108], [20, 143], [21, 106], [21, 111], [21, 128], [21, 137], [22, 90], [22, 104], [22, 127], [22, 136], [23, 92], [23, 124], [23, 136], [23, 138], [24, 78], [24, 95], [24, 97], [24, 125], [25, 79], [25, 95], [25, 100], [25, 131], [26, 74], [26, 80], [26, 89], [26, 140], [27, 121], [27, 125], [27, 128], [27, 132], [28, 81], [28, 87], [28, 91], [28, 118], [29, 77], [29, 85], [29, 110], [29, 123], [30, 96], [30, 100], [30, 127], [30, 144], [31, 75], [31, 92], [31, 105], [31, 115], [32, 116], [32, 120], [32, 134], [32, 139], [33, 81], [33, 87], [33, 132], [33, 142], [34, 85], [34, 110], [34, 138], [34, 144], [35, 115], [35, 119], [35, 127], [35, 144], [36, 78], [36, 92], [36, 115], [36, 130], [37, 82], [37, 102], [37, 129], [37, 134], [38, 98], [38, 108], [38, 134], [38, 139], [39, 75], [39, 93], [39, 94], [39, 135], [40, 113], [40, 121], [40, 130], [40, 131], [41, 74], [41, 82], [41, 91], [41, 93], [42, 77], [42, 84], [42, 116], [42, 133], [43, 79], [43, 89], [43, 100], [43, 126], [44, 97], [44, 113], [44, 137], [44, 142], [45, 77], [45, 123], [45, 129], [45, 141], [46, 75], [46, 105], [46, 133], [46, 143], [47, 91], [47, 118], [47, 139], [47, 141], [48, 83], [48, 101], [48, 129], [48, 141], [49, 80], [49, 122], [49, 133], [49, 143], [50, 74], [50, 105], [50, 107], [50, 140], [51, 85], [51, 90], [51, 128], [51, 137], [52, 86], [52, 117], [52, 128], [52, 132], [53, 75], [53, 94], [53, 97], [53, 125], [54, 102], [54, 118], [54, 135], [54, 140], [55, 73], [55, 120], [55, 123], [55, 143], [56, 81], [56, 111], [56, 127], [56, 136], [57, 77], [57, 92], [57, 116], [57, 124], [58, 104], [58, 110], [58, 132], [58, 142], [59, 88], [59, 114], [59, 137], [59, 142], [60, 78], [60, 96], [60, 109], [60, 130], [61, 105], [61, 107], [61, 113], [61, 121], [62, 76], [62, 103], [62, 129], [62, 134], [63, 82], [63, 86], [63, 91], [63, 117], [64, 87], [64, 106], [64, 138], [64, 144], [65, 115], [65, 119], [65, 120], [65, 123], [66, 81], [66, 98], [66, 108], [66, 111], [67, 99], [67, 112], [67, 139], [67, 141], [68, 88], [68, 102], [68, 114], [68, 118], [69, 80], [69, 96], [69, 109], [69, 122], [70, 76], [70, 85], [70, 90], [70, 103], [71, 83], [71, 87], [71, 101], [71, 106], [72, 99], [72, 104], [72, 110], [72, 112]]);;
R:=P177Census(D);;Need(Size(R.F)=4608);;
PrintTo("current_c4_descent/144_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
