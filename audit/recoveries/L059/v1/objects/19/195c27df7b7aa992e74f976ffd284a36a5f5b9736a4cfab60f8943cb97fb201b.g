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
D:=P177Graph("144_063",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 79], [1, 98], [1, 103], [1, 113], [2, 74], [2, 87], [2, 98], [2, 119], [3, 74], [3, 109], [3, 112], [3, 137], [4, 79], [4, 112], [4, 122], [4, 127], [5, 78], [5, 119], [5, 127], [5, 140], [6, 109], [6, 139], [6, 140], [6, 141], [7, 122], [7, 128], [7, 139], [7, 144], [8, 75], [8, 78], [8, 80], [8, 144], [9, 75], [9, 83], [9, 115], [9, 141], [10, 83], [10, 103], [10, 105], [10, 128], [11, 80], [11, 87], [11, 105], [11, 123], [12, 113], [12, 115], [12, 123], [12, 137], [13, 79], [13, 107], [13, 110], [13, 142], [14, 87], [14, 99], [14, 114], [14, 142], [15, 85], [15, 99], [15, 109], [15, 138], [16, 79], [16, 85], [16, 108], [16, 125], [17, 78], [17, 84], [17, 114], [17, 125], [18, 84], [18, 95], [18, 100], [18, 109], [19, 95], [19, 96], [19, 108], [19, 128], [20, 78], [20, 96], [20, 111], [20, 129], [21, 100], [21, 111], [21, 115], [21, 126], [22, 102], [22, 110], [22, 126], [22, 128], [23, 87], [23, 97], [23, 102], [23, 129], [24, 97], [24, 107], [24, 115], [24, 138], [25, 86], [25, 110], [25, 121], [25, 135], [26, 81], [26, 82], [26, 114], [26, 121], [27, 77], [27, 82], [27, 92], [27, 138], [28, 77], [28, 93], [28, 108], [28, 135], [29, 89], [29, 91], [29, 93], [29, 114], [30, 88], [30, 91], [30, 92], [30, 100], [31, 73], [31, 88], [31, 108], [31, 136], [32, 89], [32, 129], [32, 130], [32, 136], [33, 100], [33, 101], [33, 120], [33, 130], [34, 73], [34, 106], [34, 110], [34, 120], [35, 81], [35, 106], [35, 129], [35, 133], [36, 86], [36, 101], [36, 133], [36, 138], [37, 94], [37, 113], [37, 135], [37, 144], [38, 74], [38, 81], [38, 131], [38, 144], [39, 74], [39, 83], [39, 92], [39, 117], [40, 83], [40, 104], [40, 127], [40, 135], [41, 89], [41, 123], [41, 127], [41, 131], [42, 92], [42, 116], [42, 123], [42, 139], [43, 73], [43, 98], [43, 104], [43, 139], [44, 75], [44, 89], [44, 90], [44, 98], [45, 75], [45, 101], [45, 112], [45, 116], [46, 73], [46, 94], [46, 105], [46, 112], [47, 81], [47, 90], [47, 105], [47, 140], [48, 101], [48, 113], [48, 117], [48, 140], [49, 94], [49, 95], [49, 132], [49, 142], [50, 76], [50, 111], [50, 131], [50, 142], [51, 85], [51, 111], [51, 117], [51, 143], [52, 85], [52, 102], [52, 104], [52, 132], [53, 84], [53, 102], [53, 118], [53, 131], [54, 84], [54, 107], [54, 116], [54, 143], [55, 96], [55, 104], [55, 107], [55, 124], [56, 90], [56, 96], [56, 99], [56, 118], [57, 99], [57, 116], [57, 126], [57, 134], [58, 94], [58, 124], [58, 125], [58, 126], [59, 76], [59, 90], [59, 97], [59, 125], [60, 95], [60, 97], [60, 117], [60, 134], [61, 86], [61, 122], [61, 132], [61, 136], [62, 76], [62, 80], [62, 82], [62, 136], [63, 82], [63, 120], [63, 141], [63, 143], [64, 93], [64, 103], [64, 120], [64, 132], [65, 80], [65, 93], [65, 118], [65, 133], [66, 88], [66, 133], [66, 137], [66, 143], [67, 88], [67, 103], [67, 121], [67, 124], [68, 118], [68, 119], [68, 121], [68, 130], [69, 77], [69, 130], [69, 134], [69, 137], [70, 77], [70, 106], [70, 122], [70, 124], [71, 76], [71, 91], [71, 106], [71, 119], [72, 86], [72, 91], [72, 134], [72, 141]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_063.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_063 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
