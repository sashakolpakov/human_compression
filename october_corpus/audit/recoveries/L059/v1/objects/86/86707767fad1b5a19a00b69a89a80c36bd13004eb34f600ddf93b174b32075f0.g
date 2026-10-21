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
D:=P177Graph("136_012",136,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68],[[1, 96], [1, 108], [1, 121], [1, 129], [2, 82], [2, 96], [2, 112], [2, 121], [3, 74], [3, 104], [3, 110], [3, 127], [4, 69], [4, 74], [4, 83], [4, 104], [5, 74], [5, 108], [5, 122], [5, 129], [6, 70], [6, 92], [6, 122], [6, 136], [7, 98], [7, 107], [7, 115], [7, 130], [8, 80], [8, 87], [8, 112], [8, 126], [9, 92], [9, 122], [9, 128], [9, 133], [10, 71], [10, 98], [10, 107], [10, 117], [11, 87], [11, 112], [11, 124], [11, 125], [12, 74], [12, 82], [12, 112], [12, 122], [13, 96], [13, 107], [13, 110], [13, 127], [14, 82], [14, 91], [14, 111], [14, 113], [15, 71], [15, 73], [15, 78], [15, 94], [16, 81], [16, 88], [16, 118], [16, 128], [17, 76], [17, 85], [17, 106], [17, 132], [18, 80], [18, 126], [18, 129], [18, 132], [19, 69], [19, 72], [19, 123], [19, 125], [20, 79], [20, 82], [20, 88], [20, 111], [21, 78], [21, 94], [21, 130], [21, 135], [22, 70], [22, 81], [22, 88], [22, 116], [23, 85], [23, 99], [23, 105], [23, 132], [24, 124], [24, 125], [24, 129], [24, 132], [25, 69], [25, 72], [25, 78], [25, 126], [26, 69], [26, 83], [26, 96], [26, 107], [27, 70], [27, 94], [27, 121], [27, 136], [28, 81], [28, 104], [28, 115], [28, 130], [29, 84], [29, 91], [29, 108], [29, 113], [30, 79], [30, 83], [30, 109], [30, 119], [31, 84], [31, 90], [31, 99], [31, 131], [32, 76], [32, 87], [32, 106], [32, 109], [33, 97], [33, 103], [33, 105], [33, 134], [34, 123], [34, 125], [34, 127], [34, 134], [35, 86], [35, 95], [35, 124], [35, 133], [36, 79], [36, 84], [36, 88], [36, 108], [37, 83], [37, 109], [37, 113], [37, 120], [38, 76], [38, 84], [38, 89], [38, 131], [39, 87], [39, 99], [39, 105], [39, 109], [40, 75], [40, 103], [40, 106], [40, 134], [41, 78], [41, 126], [41, 127], [41, 134], [42, 94], [42, 121], [42, 128], [42, 133], [43, 91], [43, 98], [43, 118], [43, 128], [44, 71], [44, 73], [44, 92], [44, 123], [45, 95], [45, 124], [45, 131], [45, 136], [46, 71], [46, 81], [46, 104], [46, 117], [47, 79], [47, 85], [47, 110], [47, 119], [48, 100], [48, 114], [48, 117], [48, 120], [49, 86], [49, 90], [49, 99], [49, 111], [50, 72], [50, 97], [50, 100], [50, 105], [51, 77], [51, 89], [51, 101], [51, 116], [52, 75], [52, 93], [52, 102], [52, 135], [53, 80], [53, 86], [53, 93], [53, 133], [54, 85], [54, 110], [54, 113], [54, 120], [55, 77], [55, 100], [55, 117], [55, 119], [56, 76], [56, 86], [56, 89], [56, 111], [57, 72], [57, 75], [57, 100], [57, 106], [58, 92], [58, 123], [58, 130], [58, 135], [59, 90], [59, 101], [59, 114], [59, 116], [60, 95], [60, 97], [60, 102], [60, 135], [61, 73], [61, 75], [61, 93], [61, 101], [62, 70], [62, 91], [62, 98], [62, 116], [63, 80], [63, 93], [63, 131], [63, 136], [64, 103], [64, 114], [64, 115], [64, 120], [65, 77], [65, 89], [65, 102], [65, 118], [66, 77], [66, 103], [66, 115], [66, 119], [67, 90], [67, 102], [67, 114], [67, 118], [68, 73], [68, 95], [68, 97], [68, 101]]);;
R:=P177Census(D);;Need(Size(R.F)=272);;
PrintTo("current_c4_descent/136_012.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_012 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
