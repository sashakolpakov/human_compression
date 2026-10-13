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
D:=P177Graph("144_066",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 101], [1, 115], [1, 127], [1, 139], [2, 84], [2, 88], [2, 128], [2, 136], [3, 92], [3, 95], [3, 108], [3, 141], [4, 87], [4, 100], [4, 131], [4, 132], [5, 75], [5, 85], [5, 109], [5, 113], [6, 77], [6, 78], [6, 86], [6, 103], [7, 96], [7, 97], [7, 123], [7, 140], [8, 114], [8, 116], [8, 122], [8, 144], [9, 93], [9, 102], [9, 121], [9, 133], [10, 74], [10, 76], [10, 100], [10, 123], [11, 81], [11, 85], [11, 122], [11, 126], [12, 89], [12, 103], [12, 105], [12, 121], [13, 97], [13, 119], [13, 129], [13, 139], [14, 73], [14, 80], [14, 88], [14, 144], [15, 83], [15, 92], [15, 133], [15, 135], [16, 79], [16, 101], [16, 131], [16, 138], [17, 98], [17, 106], [17, 113], [17, 136], [18, 82], [18, 86], [18, 99], [18, 141], [19, 89], [19, 94], [19, 117], [19, 126], [20, 74], [20, 105], [20, 125], [20, 143], [21, 76], [21, 81], [21, 104], [21, 107], [22, 80], [22, 124], [22, 130], [22, 135], [23, 83], [23, 110], [23, 129], [23, 134], [24, 73], [24, 91], [24, 119], [24, 142], [25, 90], [25, 99], [25, 106], [25, 111], [26, 82], [26, 112], [26, 118], [26, 138], [27, 79], [27, 98], [27, 120], [27, 137], [28, 91], [28, 115], [28, 118], [28, 127], [29, 84], [29, 124], [29, 128], [29, 137], [30, 90], [30, 95], [30, 108], [30, 134], [31, 87], [31, 120], [31, 132], [31, 143], [32, 75], [32, 104], [32, 109], [32, 111], [33, 77], [33, 78], [33, 94], [33, 112], [34, 96], [34, 107], [34, 110], [34, 140], [35, 114], [35, 116], [35, 117], [35, 142], [36, 93], [36, 102], [36, 125], [36, 130], [37, 75], [37, 100], [37, 102], [37, 123], [38, 77], [38, 85], [38, 122], [38, 140], [39, 103], [39, 116], [39, 121], [39, 132], [40, 97], [40, 108], [40, 114], [40, 139], [41, 88], [41, 93], [41, 127], [41, 144], [42, 92], [42, 96], [42, 128], [42, 133], [43, 78], [43, 84], [43, 101], [43, 131], [44, 87], [44, 95], [44, 113], [44, 136], [45, 86], [45, 109], [45, 115], [45, 141], [46, 89], [46, 101], [46, 126], [46, 139], [47, 74], [47, 88], [47, 105], [47, 136], [48, 76], [48, 81], [48, 92], [48, 141], [49, 80], [49, 100], [49, 131], [49, 135], [50, 83], [50, 85], [50, 113], [50, 129], [51, 73], [51, 86], [51, 103], [51, 119], [52, 97], [52, 99], [52, 106], [52, 123], [53, 82], [53, 122], [53, 138], [53, 144], [54, 79], [54, 98], [54, 121], [54, 133], [55, 74], [55, 76], [55, 91], [55, 118], [56, 81], [56, 124], [56, 126], [56, 137], [57, 89], [57, 90], [57, 105], [57, 134], [58, 119], [58, 120], [58, 129], [58, 143], [59, 73], [59, 80], [59, 104], [59, 111], [60, 83], [60, 94], [60, 112], [60, 135], [61, 79], [61, 107], [61, 110], [61, 138], [62, 98], [62, 106], [62, 117], [62, 142], [63, 82], [63, 99], [63, 125], [63, 130], [64, 75], [64, 94], [64, 102], [64, 117], [65, 77], [65, 125], [65, 140], [65, 143], [66, 104], [66, 107], [66, 116], [66, 132], [67, 108], [67, 114], [67, 124], [67, 130], [68, 93], [68, 110], [68, 127], [68, 134], [69, 91], [69, 96], [69, 128], [69, 142], [70, 78], [70, 84], [70, 90], [70, 111], [71, 87], [71, 95], [71, 112], [71, 118], [72, 109], [72, 115], [72, 120], [72, 137]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_066.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_066 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
