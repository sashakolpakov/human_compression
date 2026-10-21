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
D:=P177Graph("144_068",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 75], [1, 90], [1, 115], [1, 133], [2, 73], [2, 116], [2, 117], [2, 122], [3, 101], [3, 110], [3, 126], [3, 139], [4, 76], [4, 82], [4, 110], [4, 133], [5, 73], [5, 74], [5, 75], [5, 106], [6, 103], [6, 122], [6, 136], [6, 139], [7, 82], [7, 115], [7, 117], [7, 136], [8, 74], [8, 76], [8, 116], [8, 126], [9, 90], [9, 101], [9, 103], [9, 106], [10, 104], [10, 115], [10, 127], [10, 133], [11, 73], [11, 85], [11, 104], [11, 116], [12, 85], [12, 101], [12, 127], [12, 139], [13, 82], [13, 113], [13, 133], [13, 140], [14, 73], [14, 74], [14, 78], [14, 140], [15, 78], [15, 103], [15, 113], [15, 139], [16, 82], [16, 86], [16, 115], [16, 120], [17, 74], [17, 86], [17, 116], [17, 123], [18, 101], [18, 103], [18, 120], [18, 123], [19, 84], [19, 104], [19, 121], [19, 127], [20, 85], [20, 104], [20, 108], [20, 142], [21, 80], [21, 85], [21, 127], [21, 135], [22, 113], [22, 132], [22, 140], [22, 142], [23, 78], [23, 83], [23, 135], [23, 140], [24, 78], [24, 113], [24, 121], [24, 141], [25, 80], [25, 83], [25, 86], [25, 120], [26, 84], [26, 86], [26, 123], [26, 141], [27, 108], [27, 120], [27, 123], [27, 132], [28, 84], [28, 118], [28, 121], [28, 125], [29, 94], [29, 98], [29, 108], [29, 142], [30, 80], [30, 100], [30, 135], [30, 138], [31, 95], [31, 100], [31, 132], [31, 142], [32, 83], [32, 111], [32, 125], [32, 135], [33, 93], [33, 98], [33, 121], [33, 141], [34, 80], [34, 83], [34, 93], [34, 94], [35, 84], [35, 95], [35, 138], [35, 141], [36, 108], [36, 111], [36, 118], [36, 132], [37, 118], [37, 125], [37, 129], [37, 144], [38, 79], [38, 87], [38, 94], [38, 98], [39, 100], [39, 102], [39, 107], [39, 138], [40, 95], [40, 97], [40, 100], [40, 129], [41, 79], [41, 111], [41, 125], [41, 128], [42, 93], [42, 98], [42, 107], [42, 130], [43, 93], [43, 94], [43, 97], [43, 144], [44, 87], [44, 95], [44, 128], [44, 138], [45, 102], [45, 111], [45, 118], [45, 130], [46, 92], [46, 119], [46, 129], [46, 144], [47, 79], [47, 87], [47, 119], [47, 134], [48, 92], [48, 102], [48, 107], [48, 134], [49, 81], [49, 89], [49, 97], [49, 129], [50, 79], [50, 81], [50, 114], [50, 128], [51, 89], [51, 107], [51, 114], [51, 130], [52, 97], [52, 109], [52, 124], [52, 144], [53, 87], [53, 112], [53, 124], [53, 128], [54, 102], [54, 109], [54, 112], [54, 130], [55, 91], [55, 92], [55, 105], [55, 119], [56, 96], [56, 99], [56, 119], [56, 134], [57, 77], [57, 92], [57, 134], [57, 137], [58, 81], [58, 89], [58, 99], [58, 143], [59, 77], [59, 81], [59, 88], [59, 114], [60, 89], [60, 105], [60, 114], [60, 131], [61, 88], [61, 109], [61, 124], [61, 137], [62, 91], [62, 112], [62, 124], [62, 131], [63, 96], [63, 109], [63, 112], [63, 143], [64, 75], [64, 90], [64, 91], [64, 105], [65, 96], [65, 99], [65, 117], [65, 122], [66, 77], [66, 110], [66, 126], [66, 137], [67, 76], [67, 99], [67, 110], [67, 143], [68, 75], [68, 77], [68, 88], [68, 106], [69, 105], [69, 122], [69, 131], [69, 136], [70, 88], [70, 117], [70, 136], [70, 137], [71, 76], [71, 91], [71, 126], [71, 131], [72, 90], [72, 96], [72, 106], [72, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_068.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_068 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
