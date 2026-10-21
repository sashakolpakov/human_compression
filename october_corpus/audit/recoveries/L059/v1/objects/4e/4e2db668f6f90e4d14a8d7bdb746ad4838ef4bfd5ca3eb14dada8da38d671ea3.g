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
D:=P177Graph("144_054",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 85], [1, 86], [1, 109], [1, 110], [2, 79], [2, 80], [2, 109], [2, 110], [3, 79], [3, 80], [3, 121], [3, 122], [4, 73], [4, 74], [4, 121], [4, 122], [5, 73], [5, 74], [5, 115], [5, 116], [6, 85], [6, 86], [6, 115], [6, 116], [7, 86], [7, 87], [7, 127], [7, 128], [8, 80], [8, 81], [8, 127], [8, 128], [9, 80], [9, 81], [9, 139], [9, 140], [10, 74], [10, 75], [10, 139], [10, 140], [11, 74], [11, 75], [11, 133], [11, 134], [12, 86], [12, 87], [12, 133], [12, 134], [13, 87], [13, 88], [13, 91], [13, 92], [14, 81], [14, 82], [14, 91], [14, 92], [15, 81], [15, 82], [15, 103], [15, 104], [16, 75], [16, 76], [16, 103], [16, 104], [17, 75], [17, 76], [17, 97], [17, 98], [18, 87], [18, 88], [18, 97], [18, 98], [19, 88], [19, 89], [19, 112], [19, 113], [20, 82], [20, 83], [20, 112], [20, 113], [21, 82], [21, 83], [21, 124], [21, 125], [22, 76], [22, 77], [22, 124], [22, 125], [23, 76], [23, 77], [23, 118], [23, 119], [24, 88], [24, 89], [24, 118], [24, 119], [25, 89], [25, 90], [25, 130], [25, 131], [26, 83], [26, 84], [26, 130], [26, 131], [27, 83], [27, 84], [27, 142], [27, 143], [28, 77], [28, 78], [28, 142], [28, 143], [29, 77], [29, 78], [29, 136], [29, 137], [30, 89], [30, 90], [30, 136], [30, 137], [31, 85], [31, 90], [31, 94], [31, 95], [32, 79], [32, 84], [32, 94], [32, 95], [33, 79], [33, 84], [33, 106], [33, 107], [34, 73], [34, 78], [34, 106], [34, 107], [35, 73], [35, 78], [35, 100], [35, 101], [36, 85], [36, 90], [36, 100], [36, 101], [37, 105], [37, 106], [37, 128], [37, 129], [38, 99], [38, 100], [38, 128], [38, 129], [39, 99], [39, 100], [39, 140], [39, 141], [40, 93], [40, 94], [40, 140], [40, 141], [41, 93], [41, 94], [41, 134], [41, 135], [42, 105], [42, 106], [42, 134], [42, 135], [43, 104], [43, 105], [43, 110], [43, 111], [44, 98], [44, 99], [44, 110], [44, 111], [45, 98], [45, 99], [45, 122], [45, 123], [46, 92], [46, 93], [46, 122], [46, 123], [47, 92], [47, 93], [47, 116], [47, 117], [48, 104], [48, 105], [48, 116], [48, 117], [49, 123], [49, 124], [49, 127], [49, 132], [50, 117], [50, 118], [50, 127], [50, 132], [51, 117], [51, 118], [51, 139], [51, 144], [52, 111], [52, 112], [52, 139], [52, 144], [53, 111], [53, 112], [53, 133], [53, 138], [54, 123], [54, 124], [54, 133], [54, 138], [55, 103], [55, 108], [55, 131], [55, 132], [56, 97], [56, 102], [56, 131], [56, 132], [57, 97], [57, 102], [57, 143], [57, 144], [58, 91], [58, 96], [58, 143], [58, 144], [59, 91], [59, 96], [59, 137], [59, 138], [60, 103], [60, 108], [60, 137], [60, 138], [61, 107], [61, 108], [61, 113], [61, 114], [62, 101], [62, 102], [62, 113], [62, 114], [63, 101], [63, 102], [63, 125], [63, 126], [64, 95], [64, 96], [64, 125], [64, 126], [65, 95], [65, 96], [65, 119], [65, 120], [66, 107], [66, 108], [66, 119], [66, 120], [67, 121], [67, 126], [67, 129], [67, 130], [68, 115], [68, 120], [68, 129], [68, 130], [69, 115], [69, 120], [69, 141], [69, 142], [70, 109], [70, 114], [70, 141], [70, 142], [71, 109], [71, 114], [71, 135], [71, 136], [72, 121], [72, 126], [72, 135], [72, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_054.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_054 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
