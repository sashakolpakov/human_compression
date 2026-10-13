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
D:=P177Graph("144_020",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 74], [1, 91], [1, 92], [2, 73], [2, 74], [2, 133], [2, 134], [3, 127], [3, 128], [3, 133], [3, 134], [4, 109], [4, 110], [4, 127], [4, 128], [5, 103], [5, 104], [5, 109], [5, 110], [6, 85], [6, 86], [6, 103], [6, 104], [7, 79], [7, 80], [7, 85], [7, 86], [8, 79], [8, 80], [8, 139], [8, 140], [9, 121], [9, 122], [9, 139], [9, 140], [10, 115], [10, 116], [10, 121], [10, 122], [11, 97], [11, 98], [11, 115], [11, 116], [12, 91], [12, 92], [12, 97], [12, 98], [13, 74], [13, 75], [13, 140], [13, 141], [14, 74], [14, 75], [14, 86], [14, 87], [15, 86], [15, 87], [15, 98], [15, 99], [16, 98], [16, 99], [16, 110], [16, 111], [17, 110], [17, 111], [17, 122], [17, 123], [18, 122], [18, 123], [18, 134], [18, 135], [19, 80], [19, 81], [19, 134], [19, 135], [20, 80], [20, 81], [20, 92], [20, 93], [21, 92], [21, 93], [21, 104], [21, 105], [22, 104], [22, 105], [22, 116], [22, 117], [23, 116], [23, 117], [23, 128], [23, 129], [24, 128], [24, 129], [24, 140], [24, 141], [25, 75], [25, 76], [25, 93], [25, 94], [26, 75], [26, 76], [26, 135], [26, 136], [27, 129], [27, 130], [27, 135], [27, 136], [28, 111], [28, 112], [28, 129], [28, 130], [29, 105], [29, 106], [29, 111], [29, 112], [30, 87], [30, 88], [30, 105], [30, 106], [31, 81], [31, 82], [31, 87], [31, 88], [32, 81], [32, 82], [32, 141], [32, 142], [33, 123], [33, 124], [33, 141], [33, 142], [34, 117], [34, 118], [34, 123], [34, 124], [35, 99], [35, 100], [35, 117], [35, 118], [36, 93], [36, 94], [36, 99], [36, 100], [37, 76], [37, 77], [37, 142], [37, 143], [38, 76], [38, 77], [38, 88], [38, 89], [39, 88], [39, 89], [39, 100], [39, 101], [40, 100], [40, 101], [40, 112], [40, 113], [41, 112], [41, 113], [41, 124], [41, 125], [42, 124], [42, 125], [42, 136], [42, 137], [43, 82], [43, 83], [43, 136], [43, 137], [44, 82], [44, 83], [44, 94], [44, 95], [45, 94], [45, 95], [45, 106], [45, 107], [46, 106], [46, 107], [46, 118], [46, 119], [47, 118], [47, 119], [47, 130], [47, 131], [48, 130], [48, 131], [48, 142], [48, 143], [49, 77], [49, 78], [49, 95], [49, 96], [50, 77], [50, 78], [50, 137], [50, 138], [51, 131], [51, 132], [51, 137], [51, 138], [52, 113], [52, 114], [52, 131], [52, 132], [53, 107], [53, 108], [53, 113], [53, 114], [54, 89], [54, 90], [54, 107], [54, 108], [55, 83], [55, 84], [55, 89], [55, 90], [56, 83], [56, 84], [56, 143], [56, 144], [57, 125], [57, 126], [57, 143], [57, 144], [58, 119], [58, 120], [58, 125], [58, 126], [59, 101], [59, 102], [59, 119], [59, 120], [60, 95], [60, 96], [60, 101], [60, 102], [61, 73], [61, 84], [61, 138], [61, 139], [62, 73], [62, 84], [62, 85], [62, 96], [63, 85], [63, 96], [63, 97], [63, 108], [64, 97], [64, 108], [64, 109], [64, 120], [65, 109], [65, 120], [65, 121], [65, 132], [66, 121], [66, 132], [66, 133], [66, 144], [67, 78], [67, 79], [67, 133], [67, 144], [68, 78], [68, 79], [68, 90], [68, 91], [69, 90], [69, 91], [69, 102], [69, 103], [70, 102], [70, 103], [70, 114], [70, 115], [71, 114], [71, 115], [71, 126], [71, 127], [72, 126], [72, 127], [72, 138], [72, 139]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_020.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_020 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
