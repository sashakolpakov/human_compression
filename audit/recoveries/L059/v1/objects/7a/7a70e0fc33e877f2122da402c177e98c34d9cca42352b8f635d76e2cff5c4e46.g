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
D:=P177Graph("144_045",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 82], [1, 111], [1, 116], [1, 117], [2, 89], [2, 105], [2, 111], [2, 117], [3, 91], [3, 107], [3, 128], [3, 140], [4, 92], [4, 99], [4, 139], [4, 141], [5, 83], [5, 107], [5, 113], [5, 128], [6, 73], [6, 92], [6, 99], [6, 103], [7, 84], [7, 126], [7, 139], [7, 143], [8, 95], [8, 130], [8, 139], [8, 143], [9, 89], [9, 97], [9, 115], [9, 122], [10, 87], [10, 91], [10, 98], [10, 115], [11, 76], [11, 91], [11, 102], [11, 115], [12, 76], [12, 97], [12, 106], [12, 124], [13, 93], [13, 95], [13, 134], [13, 135], [14, 84], [14, 126], [14, 132], [14, 144], [15, 95], [15, 103], [15, 106], [15, 130], [16, 82], [16, 115], [16, 121], [16, 122], [17, 87], [17, 98], [17, 100], [17, 118], [18, 76], [18, 83], [18, 88], [18, 102], [19, 86], [19, 97], [19, 124], [19, 143], [20, 78], [20, 81], [20, 134], [20, 135], [21, 75], [21, 91], [21, 93], [21, 140], [22, 81], [22, 85], [22, 103], [22, 106], [23, 75], [23, 93], [23, 100], [23, 125], [24, 105], [24, 119], [24, 141], [24, 142], [25, 90], [25, 116], [25, 141], [25, 142], [26, 90], [26, 92], [26, 113], [26, 134], [27, 73], [27, 101], [27, 105], [27, 119], [28, 77], [28, 127], [28, 139], [28, 141], [29, 90], [29, 116], [29, 136], [29, 137], [30, 89], [30, 105], [30, 129], [30, 138], [31, 77], [31, 119], [31, 123], [31, 125], [32, 96], [32, 101], [32, 102], [32, 117], [33, 123], [33, 124], [33, 126], [33, 128], [34, 74], [34, 114], [34, 122], [34, 130], [35, 80], [35, 86], [35, 100], [35, 118], [36, 81], [36, 85], [36, 132], [36, 144], [37, 78], [37, 96], [37, 100], [37, 125], [38, 90], [38, 131], [38, 134], [38, 140], [39, 77], [39, 127], [39, 132], [39, 136], [40, 79], [40, 110], [40, 136], [40, 137], [41, 110], [41, 120], [41, 129], [41, 138], [42, 119], [42, 123], [42, 131], [42, 140], [43, 75], [43, 101], [43, 102], [43, 133], [44, 78], [44, 81], [44, 123], [44, 124], [45, 84], [45, 114], [45, 122], [45, 129], [46, 80], [46, 83], [46, 86], [46, 88], [47, 74], [47, 82], [47, 116], [47, 133], [48, 89], [48, 97], [48, 112], [48, 118], [49, 78], [49, 83], [49, 96], [49, 113], [50, 74], [50, 110], [50, 120], [50, 133], [51, 108], [51, 112], [51, 118], [51, 120], [52, 87], [52, 121], [52, 135], [52, 144], [53, 86], [53, 121], [53, 135], [53, 143], [54, 82], [54, 88], [54, 104], [54, 121], [55, 76], [55, 106], [55, 108], [55, 109], [56, 93], [56, 94], [56, 95], [56, 109], [57, 73], [57, 103], [57, 114], [57, 131], [58, 88], [58, 104], [58, 108], [58, 120], [59, 85], [59, 111], [59, 112], [59, 127], [60, 85], [60, 99], [60, 104], [60, 111], [61, 80], [61, 107], [61, 138], [61, 142], [62, 75], [62, 80], [62, 133], [62, 142], [63, 114], [63, 131], [63, 132], [63, 136], [64, 73], [64, 79], [64, 101], [64, 110], [65, 87], [65, 108], [65, 109], [65, 144], [66, 94], [66, 109], [66, 126], [66, 128], [67, 74], [67, 112], [67, 127], [67, 130], [68, 84], [68, 99], [68, 104], [68, 129], [69, 79], [69, 92], [69, 94], [69, 113], [70, 77], [70, 79], [70, 94], [70, 125], [71, 96], [71, 98], [71, 117], [71, 137], [72, 98], [72, 107], [72, 137], [72, 138]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_045.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_045 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
