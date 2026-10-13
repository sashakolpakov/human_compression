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
D:=P177Graph("144_055",144,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72],[[1, 73], [1, 74], [1, 118], [1, 119], [2, 73], [2, 74], [2, 109], [2, 110], [3, 82], [3, 83], [3, 109], [3, 110], [4, 82], [4, 83], [4, 118], [4, 119], [5, 74], [5, 75], [5, 136], [5, 137], [6, 74], [6, 75], [6, 127], [6, 128], [7, 83], [7, 84], [7, 127], [7, 128], [8, 83], [8, 84], [8, 136], [8, 137], [9, 75], [9, 76], [9, 100], [9, 101], [10, 75], [10, 76], [10, 91], [10, 92], [11, 84], [11, 85], [11, 91], [11, 92], [12, 84], [12, 85], [12, 100], [12, 101], [13, 76], [13, 77], [13, 121], [13, 122], [14, 76], [14, 77], [14, 112], [14, 113], [15, 85], [15, 86], [15, 112], [15, 113], [16, 85], [16, 86], [16, 121], [16, 122], [17, 77], [17, 78], [17, 142], [17, 143], [18, 77], [18, 78], [18, 133], [18, 134], [19, 86], [19, 87], [19, 133], [19, 134], [20, 86], [20, 87], [20, 142], [20, 143], [21, 78], [21, 79], [21, 106], [21, 107], [22, 78], [22, 79], [22, 97], [22, 98], [23, 87], [23, 88], [23, 97], [23, 98], [24, 87], [24, 88], [24, 106], [24, 107], [25, 79], [25, 80], [25, 124], [25, 125], [26, 79], [26, 80], [26, 115], [26, 116], [27, 88], [27, 89], [27, 115], [27, 116], [28, 88], [28, 89], [28, 124], [28, 125], [29, 80], [29, 81], [29, 139], [29, 140], [30, 80], [30, 81], [30, 130], [30, 131], [31, 89], [31, 90], [31, 130], [31, 131], [32, 89], [32, 90], [32, 139], [32, 140], [33, 73], [33, 81], [33, 103], [33, 104], [34, 73], [34, 81], [34, 94], [34, 95], [35, 82], [35, 90], [35, 94], [35, 95], [36, 82], [36, 90], [36, 103], [36, 104], [37, 93], [37, 94], [37, 137], [37, 138], [38, 93], [38, 94], [38, 128], [38, 129], [39, 102], [39, 103], [39, 128], [39, 129], [40, 102], [40, 103], [40, 137], [40, 138], [41, 92], [41, 93], [41, 119], [41, 120], [42, 92], [42, 93], [42, 110], [42, 111], [43, 101], [43, 102], [43, 110], [43, 111], [44, 101], [44, 102], [44, 119], [44, 120], [45, 111], [45, 112], [45, 136], [45, 144], [46, 111], [46, 112], [46, 127], [46, 135], [47, 120], [47, 121], [47, 127], [47, 135], [48, 120], [48, 121], [48, 136], [48, 144], [49, 91], [49, 99], [49, 143], [49, 144], [50, 91], [50, 99], [50, 134], [50, 135], [51, 100], [51, 108], [51, 134], [51, 135], [52, 100], [52, 108], [52, 143], [52, 144], [53, 98], [53, 99], [53, 122], [53, 123], [54, 98], [54, 99], [54, 113], [54, 114], [55, 107], [55, 108], [55, 113], [55, 114], [56, 107], [56, 108], [56, 122], [56, 123], [57, 114], [57, 115], [57, 141], [57, 142], [58, 114], [58, 115], [58, 132], [58, 133], [59, 123], [59, 124], [59, 132], [59, 133], [60, 123], [60, 124], [60, 141], [60, 142], [61, 96], [61, 97], [61, 140], [61, 141], [62, 96], [62, 97], [62, 131], [62, 132], [63, 105], [63, 106], [63, 131], [63, 132], [64, 105], [64, 106], [64, 140], [64, 141], [65, 95], [65, 96], [65, 125], [65, 126], [66, 95], [66, 96], [66, 116], [66, 117], [67, 104], [67, 105], [67, 116], [67, 117], [68, 104], [68, 105], [68, 125], [68, 126], [69, 109], [69, 117], [69, 138], [69, 139], [70, 109], [70, 117], [70, 129], [70, 130], [71, 118], [71, 126], [71, 129], [71, 130], [72, 118], [72, 126], [72, 138], [72, 139]]);;
R:=P177Census(D);;Need(Size(R.F)=1152);;
PrintTo("current_c4_descent/144_055.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 144_055 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
