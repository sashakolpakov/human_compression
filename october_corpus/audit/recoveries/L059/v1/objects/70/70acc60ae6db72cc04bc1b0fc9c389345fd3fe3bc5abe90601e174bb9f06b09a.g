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
D:=P177Graph("144_044",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 91], [1, 110], [1, 112], [1, 113], [2, 91], [2, 110], [2, 139], [2, 140], [3, 97], [3, 109], [3, 117], [3, 120], [4, 83], [4, 87], [4, 96], [4, 130], [5, 75], [5, 97], [5, 102], [5, 117], [6, 83], [6, 93], [6, 96], [6, 98], [7, 78], [7, 79], [7, 128], [7, 134], [8, 73], [8, 95], [8, 111], [8, 142], [9, 105], [9, 125], [9, 129], [9, 142], [10, 94], [10, 105], [10, 120], [10, 137], [11, 77], [11, 100], [11, 106], [11, 132], [12, 74], [12, 82], [12, 108], [12, 133], [13, 76], [13, 81], [13, 98], [13, 107], [14, 76], [14, 99], [14, 103], [14, 118], [15, 75], [15, 79], [15, 102], [15, 134], [16, 73], [16, 85], [16, 90], [16, 142], [17, 82], [17, 105], [17, 125], [17, 127], [18, 78], [18, 94], [18, 95], [18, 105], [19, 77], [19, 93], [19, 98], [19, 132], [20, 74], [20, 116], [20, 131], [20, 133], [21, 81], [21, 98], [21, 122], [21, 138], [22, 99], [22, 118], [22, 136], [22, 138], [23, 92], [23, 127], [23, 137], [23, 144], [24, 101], [24, 103], [24, 116], [24, 124], [25, 75], [25, 90], [25, 107], [25, 124], [26, 88], [26, 113], [26, 131], [26, 141], [27, 85], [27, 88], [27, 102], [27, 104], [28, 80], [28, 94], [28, 100], [28, 117], [29, 96], [29, 112], [29, 113], [29, 119], [30, 88], [30, 92], [30, 108], [30, 113], [31, 115], [31, 119], [31, 121], [31, 129], [32, 79], [32, 80], [32, 94], [32, 130], [33, 80], [33, 125], [33, 132], [33, 133], [34, 87], [34, 123], [34, 134], [34, 135], [35, 74], [35, 77], [35, 114], [35, 123], [36, 101], [36, 116], [36, 126], [36, 136], [37, 132], [37, 133], [37, 136], [37, 138], [38, 126], [38, 129], [38, 136], [38, 142], [39, 85], [39, 90], [39, 92], [39, 127], [40, 82], [40, 103], [40, 124], [40, 127], [41, 78], [41, 95], [41, 107], [41, 124], [42, 88], [42, 104], [42, 111], [42, 128], [43, 96], [43, 114], [43, 119], [43, 123], [44, 92], [44, 108], [44, 114], [44, 143], [45, 115], [45, 116], [45, 119], [45, 131], [46, 79], [46, 122], [46, 130], [46, 138], [47, 87], [47, 89], [47, 134], [47, 139], [48, 74], [48, 77], [48, 139], [48, 140], [49, 99], [49, 100], [49, 106], [49, 110], [50, 73], [50, 114], [50, 121], [50, 143], [51, 109], [51, 135], [51, 143], [51, 144], [52, 73], [52, 86], [52, 121], [52, 140], [53, 75], [53, 90], [53, 122], [53, 126], [54, 86], [54, 131], [54, 140], [54, 141], [55, 84], [55, 89], [55, 93], [55, 139], [56, 86], [56, 89], [56, 109], [56, 144], [57, 85], [57, 86], [57, 89], [57, 102], [58, 80], [58, 83], [58, 115], [58, 125], [59, 81], [59, 84], [59, 109], [59, 120], [60, 87], [60, 99], [60, 110], [60, 130], [61, 84], [61, 93], [61, 104], [61, 112], [62, 76], [62, 83], [62, 103], [62, 115], [63, 97], [63, 106], [63, 123], [63, 135], [64, 76], [64, 100], [64, 107], [64, 117], [65, 111], [65, 128], [65, 135], [65, 143], [66, 120], [66, 122], [66, 126], [66, 137], [67, 101], [67, 137], [67, 141], [67, 144], [68, 78], [68, 81], [68, 84], [68, 128], [69, 97], [69, 104], [69, 106], [69, 112], [70, 91], [70, 118], [70, 121], [70, 129], [71, 82], [71, 91], [71, 108], [71, 118], [72, 95], [72, 101], [72, 111], [72, 141]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_044.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_044 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
