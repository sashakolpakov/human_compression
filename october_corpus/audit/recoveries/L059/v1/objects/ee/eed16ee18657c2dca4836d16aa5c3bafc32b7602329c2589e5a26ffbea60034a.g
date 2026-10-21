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
D:=P177Graph("136_009",136,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102],[[1, 35], [1, 68], [1, 109], [1, 130], [2, 35], [2, 36], [2, 110], [2, 131], [3, 36], [3, 37], [3, 111], [3, 132], [4, 37], [4, 38], [4, 112], [4, 133], [5, 38], [5, 39], [5, 113], [5, 134], [6, 39], [6, 40], [6, 114], [6, 135], [7, 40], [7, 41], [7, 115], [7, 136], [8, 41], [8, 42], [8, 103], [8, 116], [9, 42], [9, 43], [9, 104], [9, 117], [10, 43], [10, 44], [10, 105], [10, 118], [11, 44], [11, 45], [11, 106], [11, 119], [12, 45], [12, 46], [12, 107], [12, 120], [13, 46], [13, 47], [13, 108], [13, 121], [14, 47], [14, 48], [14, 109], [14, 122], [15, 48], [15, 49], [15, 110], [15, 123], [16, 49], [16, 50], [16, 111], [16, 124], [17, 50], [17, 51], [17, 112], [17, 125], [18, 51], [18, 52], [18, 113], [18, 126], [19, 52], [19, 53], [19, 114], [19, 127], [20, 53], [20, 54], [20, 115], [20, 128], [21, 54], [21, 55], [21, 116], [21, 129], [22, 55], [22, 56], [22, 117], [22, 130], [23, 56], [23, 57], [23, 118], [23, 131], [24, 57], [24, 58], [24, 119], [24, 132], [25, 58], [25, 59], [25, 120], [25, 133], [26, 59], [26, 60], [26, 121], [26, 134], [27, 60], [27, 61], [27, 122], [27, 135], [28, 61], [28, 62], [28, 123], [28, 136], [29, 62], [29, 63], [29, 103], [29, 124], [30, 63], [30, 64], [30, 104], [30, 125], [31, 64], [31, 65], [31, 105], [31, 126], [32, 65], [32, 66], [32, 106], [32, 127], [33, 66], [33, 67], [33, 107], [33, 128], [34, 67], [34, 68], [34, 108], [34, 129], [35, 76], [35, 97], [36, 77], [36, 98], [37, 78], [37, 99], [38, 79], [38, 100], [39, 80], [39, 101], [40, 81], [40, 102], [41, 69], [41, 82], [42, 70], [42, 83], [43, 71], [43, 84], [44, 72], [44, 85], [45, 73], [45, 86], [46, 74], [46, 87], [47, 75], [47, 88], [48, 76], [48, 89], [49, 77], [49, 90], [50, 78], [50, 91], [51, 79], [51, 92], [52, 80], [52, 93], [53, 81], [53, 94], [54, 82], [54, 95], [55, 83], [55, 96], [56, 84], [56, 97], [57, 85], [57, 98], [58, 86], [58, 99], [59, 87], [59, 100], [60, 88], [60, 101], [61, 89], [61, 102], [62, 69], [62, 90], [63, 70], [63, 91], [64, 71], [64, 92], [65, 72], [65, 93], [66, 73], [66, 94], [67, 74], [67, 95], [68, 75], [68, 96], [69, 119], [69, 120], [70, 120], [70, 121], [71, 121], [71, 122], [72, 122], [72, 123], [73, 123], [73, 124], [74, 124], [74, 125], [75, 125], [75, 126], [76, 126], [76, 127], [77, 127], [77, 128], [78, 128], [78, 129], [79, 129], [79, 130], [80, 130], [80, 131], [81, 131], [81, 132], [82, 132], [82, 133], [83, 133], [83, 134], [84, 134], [84, 135], [85, 135], [85, 136], [86, 103], [86, 136], [87, 103], [87, 104], [88, 104], [88, 105], [89, 105], [89, 106], [90, 106], [90, 107], [91, 107], [91, 108], [92, 108], [92, 109], [93, 109], [93, 110], [94, 110], [94, 111], [95, 111], [95, 112], [96, 112], [96, 113], [97, 113], [97, 114], [98, 114], [98, 115], [99, 115], [99, 116], [100, 116], [100, 117], [101, 117], [101, 118], [102, 118], [102, 119]]);;
R:=P177Census(D);;Need(Size(R.F)=544);;
PrintTo("current_c4_descent/136_009.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 136_009 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
