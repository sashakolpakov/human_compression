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
D:=P177Graph("128_056",128,[1, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 119], [2, 121], [2, 126], [3, 118], [3, 122], [3, 127], [4, 120], [4, 123], [4, 125], [5, 117], [5, 124], [5, 128], [6, 37], [6, 47], [6, 53], [6, 73], [7, 40], [7, 50], [7, 55], [7, 74], [8, 39], [8, 49], [8, 56], [8, 74], [9, 38], [9, 48], [9, 54], [9, 73], [10, 44], [10, 52], [10, 66], [10, 71], [11, 41], [11, 51], [11, 68], [11, 72], [12, 42], [12, 52], [12, 67], [12, 72], [13, 43], [13, 51], [13, 65], [13, 71], [14, 32], [14, 38], [14, 50], [14, 69], [15, 34], [15, 39], [15, 47], [15, 70], [16, 33], [16, 40], [16, 48], [16, 70], [17, 31], [17, 37], [17, 49], [17, 69], [18, 31], [18, 46], [18, 62], [18, 66], [19, 32], [19, 46], [19, 63], [19, 67], [20, 34], [20, 45], [20, 64], [20, 65], [21, 33], [21, 45], [21, 61], [21, 68], [22, 31], [22, 35], [22, 58], [22, 61], [23, 32], [23, 35], [23, 57], [23, 64], [24, 34], [24, 36], [24, 59], [24, 63], [25, 33], [25, 36], [25, 60], [25, 62], [26, 30], [26, 41], [26, 54], [26, 59], [27, 30], [27, 42], [27, 55], [27, 58], [28, 30], [28, 44], [28, 56], [28, 57], [29, 30], [29, 43], [29, 53], [29, 60], [31, 113], [32, 116], [33, 115], [34, 114], [35, 89], [35, 91], [36, 90], [36, 92], [37, 92], [37, 95], [38, 90], [38, 96], [39, 89], [39, 93], [40, 91], [40, 94], [41, 94], [41, 103], [42, 96], [42, 104], [43, 93], [43, 102], [44, 95], [44, 101], [45, 101], [45, 104], [46, 102], [46, 103], [47, 99], [47, 116], [48, 98], [48, 113], [49, 97], [49, 115], [50, 100], [50, 114], [51, 113], [51, 116], [52, 114], [52, 115], [53, 100], [53, 108], [54, 97], [54, 105], [55, 99], [55, 106], [56, 98], [56, 107], [57, 82], [57, 109], [58, 83], [58, 112], [59, 84], [59, 111], [60, 81], [60, 110], [61, 88], [61, 111], [62, 86], [62, 109], [63, 85], [63, 112], [64, 87], [64, 110], [65, 86], [65, 105], [66, 87], [66, 106], [67, 88], [67, 107], [68, 85], [68, 108], [69, 81], [69, 84], [70, 82], [70, 83], [71, 83], [71, 84], [72, 81], [72, 82], [73, 87], [73, 88], [74, 85], [74, 86], [75, 93], [75, 94], [75, 95], [75, 96], [76, 89], [76, 92], [76, 103], [76, 104], [77, 90], [77, 91], [77, 101], [77, 102], [78, 97], [78, 100], [78, 109], [78, 112], [79, 98], [79, 99], [79, 110], [79, 111], [80, 105], [80, 106], [80, 107], [80, 108], [81, 121], [82, 122], [83, 124], [84, 123], [85, 128], [86, 127], [87, 126], [88, 125], [89, 121], [90, 124], [91, 123], [92, 122], [93, 125], [94, 126], [95, 128], [96, 127], [97, 118], [98, 120], [99, 119], [100, 117], [101, 118], [102, 119], [103, 120], [104, 117], [105, 121], [106, 122], [107, 124], [108, 123], [109, 125], [110, 128], [111, 127], [112, 126], [113, 117], [114, 120], [115, 119], [116, 118]]);;
R:=P177Census(D);;Need(Size(R.F)=256);;
PrintTo("current_c4_descent/128_056.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_056 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
