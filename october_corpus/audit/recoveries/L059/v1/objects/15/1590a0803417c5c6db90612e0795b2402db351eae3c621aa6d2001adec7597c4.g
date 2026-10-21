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
D:=P177Graph("144_052",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 75], [1, 77], [1, 80], [2, 73], [2, 74], [2, 78], [2, 82], [3, 75], [3, 79], [3, 83], [3, 86], [4, 74], [4, 76], [4, 84], [4, 89], [5, 78], [5, 85], [5, 90], [5, 95], [6, 79], [6, 82], [6, 91], [6, 96], [7, 76], [7, 80], [7, 92], [7, 99], [8, 77], [8, 81], [8, 93], [8, 100], [9, 84], [9, 94], [9, 101], [9, 108], [10, 85], [10, 89], [10, 102], [10, 109], [11, 73], [11, 82], [11, 103], [11, 110], [12, 81], [12, 86], [12, 104], [12, 114], [13, 79], [13, 82], [13, 87], [13, 105], [14, 83], [14, 88], [14, 106], [14, 115], [15, 92], [15, 100], [15, 116], [15, 126], [16, 93], [16, 101], [16, 107], [16, 117], [17, 94], [17, 99], [17, 118], [17, 127], [18, 74], [18, 81], [18, 89], [18, 114], [19, 73], [19, 75], [19, 119], [19, 128], [20, 87], [20, 95], [20, 120], [20, 132], [21, 88], [21, 96], [21, 121], [21, 133], [22, 85], [22, 89], [22, 97], [22, 122], [23, 90], [23, 96], [23, 121], [23, 134], [24, 91], [24, 98], [24, 123], [24, 135], [25, 95], [25, 104], [25, 115], [25, 120], [26, 105], [26, 116], [26, 124], [26, 136], [27, 106], [27, 117], [27, 125], [27, 137], [28, 77], [28, 88], [28, 100], [28, 133], [29, 107], [29, 114], [29, 131], [29, 141], [30, 76], [30, 87], [30, 99], [30, 132], [31, 74], [31, 78], [31, 106], [31, 125], [32, 75], [32, 79], [32, 129], [32, 142], [33, 97], [33, 108], [33, 123], [33, 137], [34, 91], [34, 96], [34, 109], [34, 130], [35, 98], [35, 110], [35, 122], [35, 138], [36, 94], [36, 99], [36, 110], [36, 138], [37, 92], [37, 100], [37, 111], [37, 139], [38, 101], [38, 109], [38, 117], [38, 130], [39, 102], [39, 103], [39, 112], [39, 144], [40, 103], [40, 112], [40, 113], [40, 140], [41, 108], [41, 120], [41, 134], [41, 137], [42, 76], [42, 84], [42, 121], [42, 135], [43, 83], [43, 98], [43, 115], [43, 122], [44, 121], [44, 135], [44, 136], [44, 143], [45, 113], [45, 124], [45, 132], [45, 140], [46, 124], [46, 125], [46, 132], [46, 133], [47, 77], [47, 80], [47, 97], [47, 123], [48, 78], [48, 85], [48, 111], [48, 139], [49, 103], [49, 110], [49, 126], [49, 143], [50, 101], [50, 108], [50, 111], [50, 140], [51, 102], [51, 109], [51, 119], [51, 127], [52, 81], [52, 93], [52, 112], [52, 138], [53, 113], [53, 118], [53, 128], [53, 139], [54, 107], [54, 114], [54, 118], [54, 128], [55, 104], [55, 115], [55, 130], [55, 144], [56, 116], [56, 119], [56, 127], [56, 136], [57, 117], [57, 126], [57, 137], [57, 143], [58, 80], [58, 92], [58, 130], [58, 144], [59, 90], [59, 112], [59, 134], [59, 138], [60, 91], [60, 113], [60, 135], [60, 139], [61, 98], [61, 123], [61, 131], [61, 141], [62, 83], [62, 86], [62, 111], [62, 140], [63, 84], [63, 94], [63, 129], [63, 142], [64, 119], [64, 120], [64, 128], [64, 134], [65, 116], [65, 126], [65, 129], [65, 141], [66, 88], [66, 106], [66, 118], [66, 127], [67, 87], [67, 93], [67, 105], [67, 107], [68, 125], [68, 131], [68, 133], [68, 142], [69, 102], [69, 131], [69, 142], [69, 144], [70, 90], [70, 95], [70, 129], [70, 141], [71, 86], [71, 104], [71, 136], [71, 143], [72, 97], [72, 105], [72, 122], [72, 124]]);;
R:=P177Census(D);;Need(Size(R.F)=288);;
PrintTo("current_c4_descent/144_052.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_052 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
