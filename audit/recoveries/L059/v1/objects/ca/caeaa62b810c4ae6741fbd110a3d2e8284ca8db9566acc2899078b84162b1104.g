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
D:=P177Graph("144_064",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 98], [1, 101], [1, 114], [1, 125], [2, 75], [2, 81], [2, 101], [2, 116], [3, 75], [3, 113], [3, 118], [3, 131], [4, 93], [4, 113], [4, 124], [4, 125], [5, 116], [5, 124], [5, 134], [5, 137], [6, 118], [6, 132], [6, 136], [6, 137], [7, 92], [7, 93], [7, 136], [7, 144], [8, 76], [8, 79], [8, 134], [8, 144], [9, 77], [9, 79], [9, 84], [9, 132], [10, 84], [10, 92], [10, 98], [10, 109], [11, 76], [11, 81], [11, 109], [11, 121], [12, 77], [12, 114], [12, 121], [12, 131], [13, 98], [13, 111], [13, 115], [13, 142], [14, 90], [14, 102], [14, 116], [14, 142], [15, 86], [15, 102], [15, 117], [15, 131], [16, 86], [16, 93], [16, 115], [16, 122], [17, 74], [17, 85], [17, 116], [17, 122], [18, 85], [18, 96], [18, 117], [18, 132], [19, 93], [19, 96], [19, 99], [19, 133], [20, 74], [20, 76], [20, 99], [20, 112], [21, 78], [21, 112], [21, 123], [21, 132], [22, 98], [22, 107], [22, 123], [22, 133], [23, 76], [23, 90], [23, 100], [23, 107], [24, 78], [24, 100], [24, 111], [24, 131], [25, 88], [25, 115], [25, 120], [25, 143], [26, 82], [26, 90], [26, 97], [26, 120], [27, 80], [27, 82], [27, 106], [27, 117], [28, 80], [28, 95], [28, 104], [28, 115], [29, 74], [29, 94], [29, 95], [29, 97], [30, 87], [30, 91], [30, 94], [30, 117], [31, 91], [31, 104], [31, 133], [31, 135], [32, 74], [32, 127], [32, 135], [32, 141], [33, 78], [33, 87], [33, 119], [33, 127], [34, 110], [34, 119], [34, 133], [34, 143], [35, 90], [35, 110], [35, 130], [35, 141], [36, 78], [36, 88], [36, 106], [36, 130], [37, 114], [37, 129], [37, 143], [37, 144], [38, 75], [38, 89], [38, 97], [38, 144], [39, 75], [39, 84], [39, 103], [39, 106], [40, 84], [40, 104], [40, 124], [40, 129], [41, 97], [41, 121], [41, 124], [41, 140], [42, 87], [42, 103], [42, 121], [42, 136], [43, 101], [43, 104], [43, 136], [43, 138], [44, 79], [44, 101], [44, 140], [44, 141], [45, 79], [45, 87], [45, 113], [45, 139], [46, 109], [46, 113], [46, 138], [46, 143], [47, 89], [47, 109], [47, 137], [47, 141], [48, 106], [48, 114], [48, 137], [48, 139], [49, 96], [49, 105], [49, 129], [49, 142], [50, 89], [50, 112], [50, 128], [50, 142], [51, 86], [51, 103], [51, 108], [51, 112], [52, 83], [52, 86], [52, 107], [52, 129], [53, 85], [53, 107], [53, 128], [53, 140], [54, 85], [54, 103], [54, 111], [54, 126], [55, 83], [55, 99], [55, 111], [55, 138], [56, 73], [56, 99], [56, 102], [56, 140], [57, 102], [57, 123], [57, 126], [57, 139], [58, 105], [58, 122], [58, 123], [58, 138], [59, 73], [59, 89], [59, 100], [59, 122], [60, 96], [60, 100], [60, 108], [60, 139], [61, 88], [61, 92], [61, 105], [61, 135], [62, 82], [62, 128], [62, 134], [62, 135], [63, 77], [63, 82], [63, 108], [63, 119], [64, 83], [64, 92], [64, 95], [64, 119], [65, 81], [65, 95], [65, 128], [65, 130], [66, 77], [66, 91], [66, 126], [66, 130], [67, 83], [67, 91], [67, 120], [67, 125], [68, 73], [68, 81], [68, 120], [68, 127], [69, 80], [69, 118], [69, 126], [69, 127], [70, 80], [70, 105], [70, 110], [70, 125], [71, 73], [71, 94], [71, 110], [71, 134], [72, 88], [72, 94], [72, 108], [72, 118]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_064.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_064 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
