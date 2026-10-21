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
D:=P177Graph("144_019",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 74], [1, 115], [1, 116], [2, 73], [2, 74], [2, 103], [2, 104], [3, 103], [3, 104], [3, 133], [3, 134], [4, 91], [4, 92], [4, 133], [4, 134], [5, 91], [5, 92], [5, 121], [5, 122], [6, 79], [6, 80], [6, 121], [6, 122], [7, 79], [7, 80], [7, 109], [7, 110], [8, 109], [8, 110], [8, 139], [8, 140], [9, 97], [9, 98], [9, 139], [9, 140], [10, 97], [10, 98], [10, 127], [10, 128], [11, 85], [11, 86], [11, 127], [11, 128], [12, 85], [12, 86], [12, 115], [12, 116], [13, 74], [13, 75], [13, 140], [13, 141], [14, 74], [14, 75], [14, 80], [14, 81], [15, 80], [15, 81], [15, 86], [15, 87], [16, 86], [16, 87], [16, 92], [16, 93], [17, 92], [17, 93], [17, 98], [17, 99], [18, 98], [18, 99], [18, 104], [18, 105], [19, 104], [19, 105], [19, 110], [19, 111], [20, 110], [20, 111], [20, 116], [20, 117], [21, 116], [21, 117], [21, 122], [21, 123], [22, 122], [22, 123], [22, 128], [22, 129], [23, 128], [23, 129], [23, 134], [23, 135], [24, 134], [24, 135], [24, 140], [24, 141], [25, 75], [25, 76], [25, 117], [25, 118], [26, 75], [26, 76], [26, 105], [26, 106], [27, 105], [27, 106], [27, 135], [27, 136], [28, 93], [28, 94], [28, 135], [28, 136], [29, 93], [29, 94], [29, 123], [29, 124], [30, 81], [30, 82], [30, 123], [30, 124], [31, 81], [31, 82], [31, 111], [31, 112], [32, 111], [32, 112], [32, 141], [32, 142], [33, 99], [33, 100], [33, 141], [33, 142], [34, 99], [34, 100], [34, 129], [34, 130], [35, 87], [35, 88], [35, 129], [35, 130], [36, 87], [36, 88], [36, 117], [36, 118], [37, 76], [37, 77], [37, 142], [37, 143], [38, 76], [38, 77], [38, 82], [38, 83], [39, 82], [39, 83], [39, 88], [39, 89], [40, 88], [40, 89], [40, 94], [40, 95], [41, 94], [41, 95], [41, 100], [41, 101], [42, 100], [42, 101], [42, 106], [42, 107], [43, 106], [43, 107], [43, 112], [43, 113], [44, 112], [44, 113], [44, 118], [44, 119], [45, 118], [45, 119], [45, 124], [45, 125], [46, 124], [46, 125], [46, 130], [46, 131], [47, 130], [47, 131], [47, 136], [47, 137], [48, 136], [48, 137], [48, 142], [48, 143], [49, 77], [49, 78], [49, 119], [49, 120], [50, 77], [50, 78], [50, 107], [50, 108], [51, 107], [51, 108], [51, 137], [51, 138], [52, 95], [52, 96], [52, 137], [52, 138], [53, 95], [53, 96], [53, 125], [53, 126], [54, 83], [54, 84], [54, 125], [54, 126], [55, 83], [55, 84], [55, 113], [55, 114], [56, 113], [56, 114], [56, 143], [56, 144], [57, 101], [57, 102], [57, 143], [57, 144], [58, 101], [58, 102], [58, 131], [58, 132], [59, 89], [59, 90], [59, 131], [59, 132], [60, 89], [60, 90], [60, 119], [60, 120], [61, 73], [61, 78], [61, 139], [61, 144], [62, 73], [62, 78], [62, 79], [62, 84], [63, 79], [63, 84], [63, 85], [63, 90], [64, 85], [64, 90], [64, 91], [64, 96], [65, 91], [65, 96], [65, 97], [65, 102], [66, 97], [66, 102], [66, 103], [66, 108], [67, 103], [67, 108], [67, 109], [67, 114], [68, 109], [68, 114], [68, 115], [68, 120], [69, 115], [69, 120], [69, 121], [69, 126], [70, 121], [70, 126], [70, 127], [70, 132], [71, 127], [71, 132], [71, 133], [71, 138], [72, 133], [72, 138], [72, 139], [72, 144]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_019.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_019 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
