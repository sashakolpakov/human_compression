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
D:=P177Graph("144_067",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 91], [1, 98], [1, 101], [1, 119], [2, 87], [2, 89], [2, 97], [2, 98], [3, 89], [3, 92], [3, 119], [3, 124], [4, 97], [4, 104], [4, 117], [4, 134], [5, 82], [5, 92], [5, 93], [5, 104], [6, 91], [6, 93], [6, 117], [6, 126], [7, 82], [7, 106], [7, 124], [7, 128], [8, 101], [8, 106], [8, 126], [8, 133], [9, 87], [9, 128], [9, 133], [9, 134], [10, 105], [10, 106], [10, 117], [10, 138], [11, 104], [11, 116], [11, 133], [11, 136], [12, 75], [12, 93], [12, 102], [12, 128], [13, 90], [13, 98], [13, 116], [13, 128], [14, 78], [14, 89], [14, 102], [14, 106], [15, 105], [15, 119], [15, 130], [15, 133], [16, 75], [16, 78], [16, 104], [16, 119], [17, 93], [17, 98], [17, 130], [17, 138], [18, 89], [18, 90], [18, 117], [18, 136], [19, 81], [19, 102], [19, 111], [19, 136], [20, 73], [20, 75], [20, 105], [20, 112], [21, 74], [21, 76], [21, 116], [21, 138], [22, 76], [22, 102], [22, 130], [22, 131], [23, 90], [23, 105], [23, 111], [23, 127], [24, 73], [24, 77], [24, 78], [24, 116], [25, 77], [25, 112], [25, 130], [25, 136], [26, 74], [26, 75], [26, 90], [26, 131], [27, 78], [27, 81], [27, 127], [27, 138], [28, 77], [28, 79], [28, 107], [28, 131], [29, 118], [29, 127], [29, 131], [29, 143], [30, 77], [30, 83], [30, 120], [30, 127], [31, 79], [31, 81], [31, 96], [31, 112], [32, 74], [32, 95], [32, 112], [32, 143], [33, 74], [33, 81], [33, 114], [33, 120], [34, 76], [34, 96], [34, 107], [34, 111], [35, 73], [35, 95], [35, 111], [35, 118], [36, 73], [36, 76], [36, 83], [36, 114], [37, 83], [37, 94], [37, 99], [37, 143], [38, 88], [38, 99], [38, 107], [38, 120], [39, 79], [39, 88], [39, 94], [39, 118], [40, 86], [40, 95], [40, 120], [40, 122], [41, 79], [41, 113], [41, 114], [41, 122], [42, 86], [42, 96], [42, 113], [42, 143], [43, 100], [43, 114], [43, 118], [43, 132], [44, 83], [44, 96], [44, 109], [44, 132], [45, 95], [45, 100], [45, 107], [45, 109], [46, 80], [46, 86], [46, 108], [46, 132], [47, 109], [47, 122], [47, 123], [47, 135], [48, 100], [48, 113], [48, 125], [48, 144], [49, 99], [49, 100], [49, 121], [49, 123], [50, 88], [50, 115], [50, 132], [50, 144], [51, 80], [51, 85], [51, 94], [51, 109], [52, 94], [52, 115], [52, 122], [52, 125], [53, 85], [53, 99], [53, 108], [53, 113], [54, 86], [54, 88], [54, 121], [54, 135], [55, 129], [55, 135], [55, 142], [55, 144], [56, 80], [56, 84], [56, 125], [56, 140], [57, 108], [57, 123], [57, 137], [57, 139], [58, 85], [58, 110], [58, 137], [58, 144], [59, 80], [59, 103], [59, 121], [59, 142], [60, 84], [60, 115], [60, 123], [60, 141], [61, 85], [61, 135], [61, 140], [61, 141], [62, 110], [62, 121], [62, 125], [62, 139], [63, 103], [63, 108], [63, 115], [63, 129], [64, 87], [64, 92], [64, 110], [64, 141], [65, 91], [65, 103], [65, 110], [65, 124], [66, 97], [66, 101], [66, 103], [66, 141], [67, 92], [67, 126], [67, 129], [67, 140], [68, 91], [68, 134], [68, 139], [68, 140], [69, 82], [69, 97], [69, 129], [69, 139], [70, 87], [70, 126], [70, 137], [70, 142], [71, 84], [71, 124], [71, 134], [71, 142], [72, 82], [72, 84], [72, 101], [72, 137]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_067.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_067 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
