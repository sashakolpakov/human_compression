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
D:=P177Graph("144_065",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 94], [1, 99], [1, 101], [1, 142], [2, 81], [2, 88], [2, 119], [2, 140], [3, 78], [3, 114], [3, 135], [3, 144], [4, 75], [4, 89], [4, 92], [4, 139], [5, 91], [5, 93], [5, 95], [5, 134], [6, 85], [6, 122], [6, 128], [6, 143], [7, 107], [7, 113], [7, 120], [7, 124], [8, 77], [8, 82], [8, 123], [8, 130], [9, 84], [9, 103], [9, 127], [9, 138], [10, 92], [10, 102], [10, 111], [10, 113], [11, 82], [11, 83], [11, 95], [11, 98], [12, 96], [12, 103], [12, 110], [12, 122], [13, 79], [13, 99], [13, 124], [13, 136], [14, 88], [14, 116], [14, 130], [14, 131], [15, 76], [15, 84], [15, 129], [15, 135], [16, 74], [16, 97], [16, 139], [16, 142], [17, 81], [17, 91], [17, 104], [17, 105], [18, 90], [18, 114], [18, 126], [18, 143], [19, 83], [19, 86], [19, 96], [19, 115], [20, 80], [20, 110], [20, 111], [20, 133], [21, 98], [21, 102], [21, 125], [21, 137], [22, 100], [22, 116], [22, 117], [22, 129], [23, 76], [23, 106], [23, 121], [23, 136], [24, 79], [24, 87], [24, 109], [24, 131], [25, 104], [25, 118], [25, 126], [25, 141], [26, 73], [26, 90], [26, 97], [26, 112], [27, 74], [27, 105], [27, 108], [27, 132], [28, 73], [28, 87], [28, 140], [28, 144], [29, 78], [29, 94], [29, 100], [29, 108], [30, 101], [30, 118], [30, 119], [30, 121], [31, 85], [31, 93], [31, 132], [31, 133], [32, 89], [32, 125], [32, 128], [32, 141], [33, 75], [33, 86], [33, 112], [33, 134], [34, 77], [34, 106], [34, 127], [34, 137], [35, 107], [35, 109], [35, 115], [35, 138], [36, 80], [36, 117], [36, 120], [36, 123], [37, 84], [37, 89], [37, 91], [37, 120], [38, 77], [38, 124], [38, 134], [38, 143], [39, 85], [39, 130], [39, 138], [39, 139], [40, 82], [40, 101], [40, 107], [40, 114], [41, 103], [41, 123], [41, 140], [41, 142], [42, 78], [42, 81], [42, 113], [42, 127], [43, 75], [43, 88], [43, 94], [43, 122], [44, 92], [44, 93], [44, 119], [44, 135], [45, 95], [45, 99], [45, 128], [45, 144], [46, 74], [46, 82], [46, 122], [46, 136], [47, 92], [47, 103], [47, 104], [47, 131], [48, 90], [48, 95], [48, 113], [48, 129], [49, 84], [49, 88], [49, 97], [49, 102], [50, 83], [50, 105], [50, 124], [50, 135], [51, 99], [51, 110], [51, 126], [51, 130], [52, 79], [52, 91], [52, 111], [52, 114], [53, 98], [53, 116], [53, 142], [53, 143], [54, 76], [54, 81], [54, 96], [54, 139], [55, 90], [55, 131], [55, 133], [55, 137], [56, 74], [56, 115], [56, 125], [56, 129], [57, 80], [57, 86], [57, 104], [57, 136], [58, 87], [58, 105], [58, 106], [58, 110], [59, 100], [59, 102], [59, 109], [59, 126], [60, 83], [60, 97], [60, 117], [60, 121], [61, 73], [61, 76], [61, 98], [61, 132], [62, 79], [62, 96], [62, 108], [62, 141], [63, 111], [63, 112], [63, 116], [63, 118], [64, 117], [64, 134], [64, 138], [64, 141], [65, 85], [65, 106], [65, 112], [65, 120], [66, 77], [66, 89], [66, 109], [66, 132], [67, 78], [67, 115], [67, 118], [67, 123], [68, 73], [68, 80], [68, 101], [68, 127], [69, 107], [69, 108], [69, 137], [69, 140], [70, 86], [70, 100], [70, 119], [70, 128], [71, 75], [71, 121], [71, 133], [71, 144], [72, 87], [72, 93], [72, 94], [72, 125]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_065.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_065 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
