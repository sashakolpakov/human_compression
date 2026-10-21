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
D:=P177Graph("144_024",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 81], [1, 85], [1, 104], [1, 117], [2, 81], [2, 104], [2, 125], [2, 129], [3, 87], [3, 105], [3, 126], [3, 131], [4, 84], [4, 87], [4, 105], [4, 111], [5, 95], [5, 97], [5, 106], [5, 113], [6, 96], [6, 118], [6, 121], [6, 132], [7, 80], [7, 83], [7, 106], [7, 139], [8, 84], [8, 95], [8, 111], [8, 113], [9, 121], [9, 124], [9, 132], [9, 134], [10, 83], [10, 128], [10, 137], [10, 139], [11, 86], [11, 98], [11, 112], [11, 135], [12, 101], [12, 131], [12, 143], [12, 144], [13, 119], [13, 122], [13, 127], [13, 130], [14, 86], [14, 93], [14, 94], [14, 110], [15, 101], [15, 102], [15, 108], [15, 114], [16, 88], [16, 119], [16, 134], [16, 141], [17, 98], [17, 124], [17, 134], [17, 135], [18, 101], [18, 128], [18, 137], [18, 144], [19, 122], [19, 125], [19, 129], [19, 130], [20, 93], [20, 102], [20, 110], [20, 141], [21, 83], [21, 102], [21, 107], [21, 108], [22, 99], [22, 134], [22, 141], [22, 142], [23, 75], [23, 96], [23, 133], [23, 140], [24, 85], [24, 94], [24, 118], [24, 136], [25, 82], [25, 99], [25, 115], [25, 116], [26, 74], [26, 103], [26, 135], [26, 144], [27, 120], [27, 123], [27, 128], [27, 133], [28, 77], [28, 78], [28, 113], [28, 124], [29, 84], [29, 127], [29, 136], [29, 137], [30, 102], [30, 133], [30, 140], [30, 141], [31, 83], [31, 86], [31, 107], [31, 112], [32, 94], [32, 99], [32, 118], [32, 142], [33, 82], [33, 85], [33, 116], [33, 117], [34, 74], [34, 103], [34, 132], [34, 139], [35, 100], [35, 110], [35, 120], [35, 128], [36, 76], [36, 78], [36, 105], [36, 124], [37, 79], [37, 84], [37, 115], [37, 137], [38, 73], [38, 82], [38, 114], [38, 138], [39, 75], [39, 79], [39, 112], [39, 125], [40, 80], [40, 88], [40, 117], [40, 126], [41, 92], [41, 95], [41, 109], [41, 140], [42, 73], [42, 90], [42, 98], [42, 111], [43, 89], [43, 91], [43, 107], [43, 122], [44, 97], [44, 129], [44, 142], [44, 143], [45, 82], [45, 132], [45, 138], [45, 139], [46, 96], [46, 101], [46, 114], [46, 118], [47, 97], [47, 100], [47, 106], [47, 110], [48, 75], [48, 76], [48, 96], [48, 105], [49, 75], [49, 88], [49, 112], [49, 119], [50, 79], [50, 80], [50, 115], [50, 126], [51, 123], [51, 126], [51, 131], [51, 133], [52, 87], [52, 92], [52, 93], [52, 109], [53, 89], [53, 90], [53, 111], [53, 121], [54, 99], [54, 103], [54, 109], [54, 115], [55, 81], [55, 89], [55, 92], [55, 107], [56, 90], [56, 120], [56, 129], [56, 142], [57, 77], [57, 91], [57, 116], [57, 123], [58, 76], [58, 100], [58, 130], [58, 138], [59, 91], [59, 122], [59, 135], [59, 144], [60, 87], [60, 91], [60, 93], [60, 116], [61, 77], [61, 86], [61, 94], [61, 113], [62, 89], [62, 121], [62, 131], [62, 143], [63, 103], [63, 109], [63, 119], [63, 127], [64, 73], [64, 81], [64, 92], [64, 114], [65, 97], [65, 127], [65, 136], [65, 143], [66, 73], [66, 80], [66, 98], [66, 106], [67, 88], [67, 90], [67, 117], [67, 120], [68, 74], [68, 76], [68, 100], [68, 104], [69, 78], [69, 79], [69, 108], [69, 125], [70, 95], [70, 130], [70, 138], [70, 140], [71, 74], [71, 77], [71, 104], [71, 123], [72, 78], [72, 85], [72, 108], [72, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=576);;
PrintTo("current_c4_descent/144_024.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_024 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
