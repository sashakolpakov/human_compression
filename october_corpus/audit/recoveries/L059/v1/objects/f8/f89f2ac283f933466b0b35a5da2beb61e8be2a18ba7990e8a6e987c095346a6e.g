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
D:=P177Graph("144_062",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 96], [1, 98], [1, 102], [1, 136], [2, 86], [2, 88], [2, 97], [2, 120], [3, 79], [3, 85], [3, 108], [3, 135], [4, 87], [4, 90], [4, 106], [4, 112], [5, 83], [5, 89], [5, 107], [5, 141], [6, 84], [6, 95], [6, 111], [6, 114], [7, 77], [7, 80], [7, 138], [7, 142], [8, 78], [8, 100], [8, 101], [8, 113], [9, 99], [9, 105], [9, 119], [9, 137], [10, 77], [10, 94], [10, 112], [10, 130], [11, 89], [11, 91], [11, 100], [11, 128], [12, 81], [12, 84], [12, 110], [12, 137], [13, 92], [13, 98], [13, 134], [13, 138], [14, 78], [14, 86], [14, 109], [14, 115], [15, 99], [15, 126], [15, 129], [15, 135], [16, 82], [16, 90], [16, 116], [16, 136], [17, 83], [17, 93], [17, 97], [17, 125], [18, 85], [18, 111], [18, 127], [18, 133], [19, 104], [19, 110], [19, 128], [19, 143], [20, 81], [20, 121], [20, 130], [20, 132], [21, 74], [21, 91], [21, 94], [21, 123], [22, 109], [22, 117], [22, 124], [22, 126], [23, 129], [23, 134], [23, 139], [23, 144], [24, 75], [24, 92], [24, 115], [24, 122], [25, 76], [25, 125], [25, 127], [25, 131], [26, 73], [26, 82], [26, 118], [26, 133], [27, 93], [27, 103], [27, 116], [27, 140], [28, 75], [28, 107], [28, 118], [28, 119], [29, 80], [29, 95], [29, 117], [29, 140], [30, 76], [30, 87], [30, 101], [30, 139], [31, 103], [31, 108], [31, 113], [31, 132], [32, 74], [32, 96], [32, 105], [32, 131], [33, 73], [33, 88], [33, 104], [33, 142], [34, 114], [34, 120], [34, 123], [34, 144], [35, 79], [35, 106], [35, 122], [35, 143], [36, 102], [36, 121], [36, 124], [36, 141], [37, 95], [37, 97], [37, 101], [37, 135], [38, 85], [38, 87], [38, 98], [38, 119], [39, 80], [39, 86], [39, 107], [39, 136], [40, 88], [40, 89], [40, 105], [40, 111], [41, 84], [41, 90], [41, 108], [41, 142], [42, 83], [42, 96], [42, 112], [42, 113], [43, 78], [43, 79], [43, 137], [43, 141], [44, 77], [44, 99], [44, 102], [44, 114], [45, 100], [45, 106], [45, 120], [45, 138], [46, 78], [46, 93], [46, 111], [46, 129], [47, 90], [47, 92], [47, 99], [47, 127], [48, 82], [48, 83], [48, 109], [48, 138], [49, 91], [49, 97], [49, 133], [49, 137], [50, 77], [50, 85], [50, 110], [50, 116], [51, 100], [51, 125], [51, 130], [51, 136], [52, 81], [52, 89], [52, 115], [52, 135], [53, 84], [53, 94], [53, 98], [53, 126], [54, 86], [54, 112], [54, 128], [54, 134], [55, 103], [55, 109], [55, 127], [55, 144], [56, 82], [56, 122], [56, 129], [56, 131], [57, 73], [57, 92], [57, 93], [57, 124], [58, 110], [58, 118], [58, 123], [58, 125], [59, 130], [59, 133], [59, 140], [59, 143], [60, 76], [60, 91], [60, 116], [60, 121], [61, 75], [61, 126], [61, 128], [61, 132], [62, 74], [62, 81], [62, 117], [62, 134], [63, 94], [63, 104], [63, 115], [63, 139], [64, 76], [64, 108], [64, 117], [64, 120], [65, 79], [65, 96], [65, 118], [65, 139], [66, 75], [66, 88], [66, 102], [66, 140], [67, 104], [67, 107], [67, 114], [67, 131], [68, 73], [68, 95], [68, 106], [68, 132], [69, 74], [69, 87], [69, 103], [69, 141], [70, 113], [70, 119], [70, 124], [70, 143], [71, 80], [71, 105], [71, 121], [71, 144], [72, 101], [72, 122], [72, 123], [72, 142]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_062.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_062 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
