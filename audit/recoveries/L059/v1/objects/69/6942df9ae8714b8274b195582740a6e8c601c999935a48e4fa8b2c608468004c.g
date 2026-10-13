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
D:=P177Graph("144_023",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 84], [1, 104], [1, 109], [2, 73], [2, 104], [2, 125], [2, 133], [3, 83], [3, 86], [3, 107], [3, 110], [4, 86], [4, 107], [4, 126], [4, 130], [5, 83], [5, 88], [5, 110], [5, 116], [6, 121], [6, 124], [6, 131], [6, 135], [7, 103], [7, 107], [7, 124], [7, 143], [8, 82], [8, 85], [8, 105], [8, 117], [9, 88], [9, 93], [9, 112], [9, 116], [10, 98], [10, 114], [10, 121], [10, 131], [11, 87], [11, 98], [11, 103], [11, 107], [12, 85], [12, 95], [12, 117], [12, 128], [13, 95], [13, 124], [13, 128], [13, 135], [14, 80], [14, 116], [14, 124], [14, 143], [15, 82], [15, 96], [15, 105], [15, 106], [16, 102], [16, 110], [16, 121], [16, 141], [17, 122], [17, 125], [17, 133], [17, 134], [18, 90], [18, 117], [18, 125], [18, 138], [19, 92], [19, 98], [19, 113], [19, 114], [20, 93], [20, 97], [20, 112], [20, 118], [21, 77], [21, 82], [21, 94], [21, 112], [22, 81], [22, 84], [22, 109], [22, 115], [23, 80], [23, 85], [23, 90], [23, 116], [24, 92], [24, 96], [24, 106], [24, 113], [25, 121], [25, 130], [25, 141], [25, 142], [26, 119], [26, 122], [26, 127], [26, 134], [27, 90], [27, 117], [27, 119], [27, 136], [28, 77], [28, 95], [28, 112], [28, 144], [29, 95], [29, 102], [29, 110], [29, 144], [30, 79], [30, 106], [30, 125], [30, 138], [31, 97], [31, 118], [31, 120], [31, 132], [32, 82], [32, 94], [32, 132], [32, 140], [33, 81], [33, 101], [33, 111], [33, 115], [34, 94], [34, 105], [34, 122], [34, 137], [35, 123], [35, 126], [35, 129], [35, 130], [36, 84], [36, 87], [36, 100], [36, 114], [37, 77], [37, 93], [37, 133], [37, 138], [38, 100], [38, 109], [38, 126], [38, 142], [39, 76], [39, 92], [39, 130], [39, 142], [40, 99], [40, 108], [40, 119], [40, 127], [41, 74], [41, 85], [41, 90], [41, 118], [42, 76], [42, 81], [42, 91], [42, 113], [43, 79], [43, 84], [43, 100], [43, 106], [44, 120], [44, 123], [44, 129], [44, 132], [45, 76], [45, 92], [45, 132], [45, 140], [46, 99], [46, 101], [46, 108], [46, 111], [47, 122], [47, 128], [47, 137], [47, 144], [48, 78], [48, 87], [48, 101], [48, 114], [49, 77], [49, 93], [49, 127], [49, 136], [50, 100], [50, 109], [50, 120], [50, 140], [51, 73], [51, 76], [51, 89], [51, 113], [52, 73], [52, 89], [52, 94], [52, 105], [53, 120], [53, 133], [53, 138], [53, 140], [54, 78], [54, 111], [54, 126], [54, 142], [55, 74], [55, 79], [55, 96], [55, 118], [56, 81], [56, 91], [56, 131], [56, 141], [57, 74], [57, 97], [57, 134], [57, 137], [58, 91], [58, 115], [58, 123], [58, 139], [59, 87], [59, 98], [59, 129], [59, 139], [60, 83], [60, 102], [60, 127], [60, 136], [61, 75], [61, 99], [61, 128], [61, 144], [62, 75], [62, 80], [62, 88], [62, 108], [63, 78], [63, 83], [63, 102], [63, 111], [64, 79], [64, 96], [64, 129], [64, 139], [65, 75], [65, 99], [65, 131], [65, 141], [66, 80], [66, 88], [66, 134], [66, 137], [67, 89], [67, 104], [67, 123], [67, 139], [68, 75], [68, 86], [68, 103], [68, 108], [69, 74], [69, 89], [69, 97], [69, 104], [70, 86], [70, 91], [70, 103], [70, 115], [71, 119], [71, 135], [71, 136], [71, 143], [72, 78], [72, 101], [72, 135], [72, 143]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_023.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_023 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
