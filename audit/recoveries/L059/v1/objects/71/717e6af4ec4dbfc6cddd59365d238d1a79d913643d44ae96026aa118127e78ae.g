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
D:=P177Graph("144_053",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 88], [1, 89], [1, 109], [1, 110], [2, 76], [2, 77], [2, 109], [2, 110], [3, 76], [3, 77], [3, 115], [3, 116], [4, 82], [4, 83], [4, 115], [4, 116], [5, 82], [5, 83], [5, 121], [5, 122], [6, 88], [6, 89], [6, 121], [6, 122], [7, 79], [7, 80], [7, 112], [7, 113], [8, 73], [8, 74], [8, 112], [8, 113], [9, 73], [9, 74], [9, 124], [9, 125], [10, 85], [10, 86], [10, 124], [10, 125], [11, 85], [11, 86], [11, 118], [11, 119], [12, 79], [12, 80], [12, 118], [12, 119], [13, 89], [13, 90], [13, 127], [13, 128], [14, 77], [14, 78], [14, 127], [14, 128], [15, 77], [15, 78], [15, 133], [15, 134], [16, 83], [16, 84], [16, 133], [16, 134], [17, 83], [17, 84], [17, 139], [17, 140], [18, 89], [18, 90], [18, 139], [18, 140], [19, 80], [19, 81], [19, 130], [19, 131], [20, 74], [20, 75], [20, 130], [20, 131], [21, 74], [21, 75], [21, 142], [21, 143], [22, 86], [22, 87], [22, 142], [22, 143], [23, 86], [23, 87], [23, 136], [23, 137], [24, 80], [24, 81], [24, 136], [24, 137], [25, 88], [25, 90], [25, 91], [25, 92], [26, 76], [26, 78], [26, 91], [26, 92], [27, 76], [27, 78], [27, 97], [27, 98], [28, 82], [28, 84], [28, 97], [28, 98], [29, 82], [29, 84], [29, 103], [29, 104], [30, 88], [30, 90], [30, 103], [30, 104], [31, 79], [31, 81], [31, 94], [31, 95], [32, 73], [32, 75], [32, 94], [32, 95], [33, 73], [33, 75], [33, 106], [33, 107], [34, 85], [34, 87], [34, 106], [34, 107], [35, 85], [35, 87], [35, 100], [35, 101], [36, 79], [36, 81], [36, 100], [36, 101], [37, 107], [37, 108], [37, 128], [37, 129], [38, 95], [38, 96], [38, 128], [38, 129], [39, 95], [39, 96], [39, 134], [39, 135], [40, 101], [40, 102], [40, 134], [40, 135], [41, 101], [41, 102], [41, 140], [41, 141], [42, 107], [42, 108], [42, 140], [42, 141], [43, 98], [43, 99], [43, 131], [43, 132], [44, 92], [44, 93], [44, 131], [44, 132], [45, 92], [45, 93], [45, 143], [45, 144], [46, 104], [46, 105], [46, 143], [46, 144], [47, 104], [47, 105], [47, 137], [47, 138], [48, 98], [48, 99], [48, 137], [48, 138], [49, 106], [49, 108], [49, 110], [49, 111], [50, 94], [50, 96], [50, 110], [50, 111], [51, 94], [51, 96], [51, 116], [51, 117], [52, 100], [52, 102], [52, 116], [52, 117], [53, 100], [53, 102], [53, 122], [53, 123], [54, 106], [54, 108], [54, 122], [54, 123], [55, 97], [55, 99], [55, 113], [55, 114], [56, 91], [56, 93], [56, 113], [56, 114], [57, 91], [57, 93], [57, 125], [57, 126], [58, 103], [58, 105], [58, 125], [58, 126], [59, 103], [59, 105], [59, 119], [59, 120], [60, 97], [60, 99], [60, 119], [60, 120], [61, 124], [61, 126], [61, 127], [61, 129], [62, 112], [62, 114], [62, 127], [62, 129], [63, 112], [63, 114], [63, 133], [63, 135], [64, 118], [64, 120], [64, 133], [64, 135], [65, 118], [65, 120], [65, 139], [65, 141], [66, 124], [66, 126], [66, 139], [66, 141], [67, 115], [67, 117], [67, 130], [67, 132], [68, 109], [68, 111], [68, 130], [68, 132], [69, 109], [69, 111], [69, 142], [69, 144], [70, 121], [70, 123], [70, 142], [70, 144], [71, 121], [71, 123], [71, 136], [71, 138], [72, 115], [72, 117], [72, 136], [72, 138]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_053.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_053 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
