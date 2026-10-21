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
D:=P177Graph("128_039",128,[1, 3, 5, 7, 9, 11, 13, 15, 16, 18, 20, 21, 23, 25, 27, 30, 32, 34, 36, 38, 39, 41, 43, 45, 46, 48, 50, 52, 54, 55, 56, 58, 60, 61, 63, 64, 67, 71, 76, 79, 81, 82, 84, 85, 86, 88, 89, 90, 91, 93, 94, 98, 102, 107, 110, 112, 113, 114, 115, 116, 117, 118, 120, 121],[[1, 2], [1, 4], [1, 80], [1, 95], [2, 5], [2, 9], [2, 110], [3, 6], [3, 10], [3, 96], [3, 99], [4, 11], [4, 18], [4, 121], [5, 12], [5, 19], [5, 122], [6, 13], [6, 20], [6, 118], [7, 8], [7, 14], [7, 97], [7, 106], [8, 15], [8, 21], [8, 112], [9, 22], [9, 31], [9, 128], [10, 23], [10, 32], [10, 112], [11, 24], [11, 33], [11, 127], [12, 25], [12, 34], [12, 36], [13, 26], [13, 35], [13, 123], [14, 27], [14, 36], [14, 118], [15, 28], [15, 37], [15, 126], [16, 17], [16, 29], [16, 109], [16, 111], [17, 30], [17, 38], [17, 121], [18, 28], [18, 35], [18, 124], [19, 32], [19, 39], [19, 48], [20, 24], [20, 40], [20, 126], [21, 33], [21, 49], [21, 123], [22, 27], [22, 41], [22, 50], [23, 31], [23, 51], [23, 119], [24, 25], [24, 52], [25, 42], [25, 53], [26, 43], [26, 54], [26, 56], [27, 44], [27, 125], [28, 45], [28, 55], [29, 46], [29, 56], [29, 110], [30, 47], [30, 57], [30, 128], [31, 43], [31, 55], [32, 47], [32, 125], [33, 48], [33, 58], [34, 49], [34, 59], [34, 68], [35, 50], [35, 61], [36, 57], [36, 119], [37, 41], [37, 56], [37, 60], [38, 44], [38, 51], [38, 122], [39, 40], [39, 62], [39, 69], [40, 46], [40, 63], [41, 42], [41, 70], [42, 64], [42, 71], [43, 65], [43, 72], [44, 45], [44, 54], [45, 66], [45, 73], [46, 49], [46, 124], [47, 52], [47, 67], [48, 66], [48, 72], [49, 67], [50, 68], [50, 74], [51, 60], [51, 61], [52, 74], [52, 75], [53, 61], [53, 76], [53, 84], [54, 62], [54, 77], [55, 69], [55, 78], [56, 127], [57, 58], [57, 63], [58, 77], [58, 78], [59, 60], [59, 79], [59, 85], [60, 75], [61, 83], [62, 64], [62, 86], [63, 65], [63, 73], [64, 80], [64, 87], [65, 81], [65, 88], [66, 82], [66, 89], [67, 70], [67, 83], [68, 81], [68, 89], [69, 84], [69, 90], [70, 90], [70, 91], [71, 78], [71, 92], [71, 99], [72, 85], [72, 94], [73, 79], [73, 93], [74, 93], [74, 94], [75, 82], [75, 88], [76, 77], [76, 95], [76, 100], [77, 91], [78, 98], [79, 80], [79, 101], [80, 102], [81, 96], [81, 103], [82, 97], [82, 104], [83, 86], [83, 98], [84, 97], [84, 103], [85, 99], [85, 105], [86, 105], [86, 106], [87, 94], [87, 107], [87, 112], [88, 95], [88, 108], [89, 100], [89, 109], [90, 108], [90, 109], [91, 96], [91, 104], [92, 93], [92, 110], [92, 113], [93, 106], [94, 111], [95, 114], [96, 115], [97, 116], [98, 101], [98, 111], [99, 116], [100, 112], [100, 117], [101, 117], [101, 118], [102, 109], [102, 119], [102, 123], [103, 113], [103, 121], [104, 110], [104, 120], [105, 120], [105, 121], [106, 115], [107, 108], [107, 122], [107, 124], [108, 118], [111, 114], [113, 123], [113, 125], [114, 125], [114, 126], [115, 122], [115, 127], [116, 124], [116, 128], [117, 127], [117, 128], [119, 120], [120, 126]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_039.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_039 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
