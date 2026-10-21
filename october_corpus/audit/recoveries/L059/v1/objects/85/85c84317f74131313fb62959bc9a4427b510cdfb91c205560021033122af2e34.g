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
D:=P177Graph("136_013",136,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68],[[1, 69], [1, 70], [1, 121], [1, 122], [2, 69], [2, 70], [2, 85], [2, 86], [3, 85], [3, 86], [3, 101], [3, 102], [4, 101], [4, 102], [4, 117], [4, 118], [5, 117], [5, 118], [5, 133], [5, 134], [6, 81], [6, 82], [6, 133], [6, 134], [7, 81], [7, 82], [7, 97], [7, 98], [8, 97], [8, 98], [8, 113], [8, 114], [9, 113], [9, 114], [9, 129], [9, 130], [10, 77], [10, 78], [10, 129], [10, 130], [11, 77], [11, 78], [11, 93], [11, 94], [12, 93], [12, 94], [12, 109], [12, 110], [13, 109], [13, 110], [13, 125], [13, 126], [14, 73], [14, 74], [14, 125], [14, 126], [15, 73], [15, 74], [15, 89], [15, 90], [16, 89], [16, 90], [16, 105], [16, 106], [17, 105], [17, 106], [17, 121], [17, 122], [18, 70], [18, 71], [18, 134], [18, 135], [19, 70], [19, 71], [19, 74], [19, 75], [20, 74], [20, 75], [20, 78], [20, 79], [21, 78], [21, 79], [21, 82], [21, 83], [22, 82], [22, 83], [22, 86], [22, 87], [23, 86], [23, 87], [23, 90], [23, 91], [24, 90], [24, 91], [24, 94], [24, 95], [25, 94], [25, 95], [25, 98], [25, 99], [26, 98], [26, 99], [26, 102], [26, 103], [27, 102], [27, 103], [27, 106], [27, 107], [28, 106], [28, 107], [28, 110], [28, 111], [29, 110], [29, 111], [29, 114], [29, 115], [30, 114], [30, 115], [30, 118], [30, 119], [31, 118], [31, 119], [31, 122], [31, 123], [32, 122], [32, 123], [32, 126], [32, 127], [33, 126], [33, 127], [33, 130], [33, 131], [34, 130], [34, 131], [34, 134], [34, 135], [35, 71], [35, 72], [35, 123], [35, 124], [36, 71], [36, 72], [36, 87], [36, 88], [37, 87], [37, 88], [37, 103], [37, 104], [38, 103], [38, 104], [38, 119], [38, 120], [39, 119], [39, 120], [39, 135], [39, 136], [40, 83], [40, 84], [40, 135], [40, 136], [41, 83], [41, 84], [41, 99], [41, 100], [42, 99], [42, 100], [42, 115], [42, 116], [43, 115], [43, 116], [43, 131], [43, 132], [44, 79], [44, 80], [44, 131], [44, 132], [45, 79], [45, 80], [45, 95], [45, 96], [46, 95], [46, 96], [46, 111], [46, 112], [47, 111], [47, 112], [47, 127], [47, 128], [48, 75], [48, 76], [48, 127], [48, 128], [49, 75], [49, 76], [49, 91], [49, 92], [50, 91], [50, 92], [50, 107], [50, 108], [51, 107], [51, 108], [51, 123], [51, 124], [52, 69], [52, 72], [52, 133], [52, 136], [53, 69], [53, 72], [53, 73], [53, 76], [54, 73], [54, 76], [54, 77], [54, 80], [55, 77], [55, 80], [55, 81], [55, 84], [56, 81], [56, 84], [56, 85], [56, 88], [57, 85], [57, 88], [57, 89], [57, 92], [58, 89], [58, 92], [58, 93], [58, 96], [59, 93], [59, 96], [59, 97], [59, 100], [60, 97], [60, 100], [60, 101], [60, 104], [61, 101], [61, 104], [61, 105], [61, 108], [62, 105], [62, 108], [62, 109], [62, 112], [63, 109], [63, 112], [63, 113], [63, 116], [64, 113], [64, 116], [64, 117], [64, 120], [65, 117], [65, 120], [65, 121], [65, 124], [66, 121], [66, 124], [66, 125], [66, 128], [67, 125], [67, 128], [67, 129], [67, 132], [68, 129], [68, 132], [68, 133], [68, 136]]);;
R:=P177Census(D);;Need(Size(R.F)=272);;
PrintTo("current_c4_descent/136_013.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_013 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
