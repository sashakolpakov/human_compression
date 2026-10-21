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
D:=P177Graph("128_054",128,[1, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 117], [2, 118], [2, 125], [3, 119], [3, 120], [3, 126], [4, 121], [4, 123], [4, 128], [5, 122], [5, 124], [5, 127], [6, 50], [6, 54], [6, 66], [6, 67], [7, 51], [7, 55], [7, 72], [7, 73], [8, 59], [8, 60], [8, 69], [8, 73], [9, 62], [9, 65], [9, 70], [9, 72], [10, 58], [10, 63], [10, 66], [10, 68], [11, 52], [11, 57], [11, 69], [11, 70], [12, 53], [12, 56], [12, 68], [12, 71], [13, 61], [13, 64], [13, 67], [13, 71], [14, 30], [14, 34], [14, 42], [14, 50], [15, 31], [15, 35], [15, 43], [15, 54], [16, 33], [16, 39], [16, 43], [16, 51], [17, 31], [17, 40], [17, 44], [17, 60], [18, 30], [18, 41], [18, 44], [18, 64], [19, 33], [19, 34], [19, 48], [19, 62], [20, 31], [20, 38], [20, 48], [20, 63], [21, 32], [21, 37], [21, 49], [21, 65], [22, 30], [22, 39], [22, 49], [22, 58], [23, 32], [23, 40], [23, 42], [23, 55], [24, 33], [24, 41], [24, 45], [24, 57], [25, 32], [25, 38], [25, 45], [25, 53], [26, 30], [26, 36], [26, 46], [26, 56], [27, 33], [27, 36], [27, 47], [27, 59], [28, 32], [28, 35], [28, 47], [28, 61], [29, 31], [29, 37], [29, 46], [29, 52], [34, 96], [34, 107], [35, 97], [35, 104], [36, 95], [36, 103], [37, 98], [37, 108], [38, 93], [38, 106], [39, 99], [39, 105], [40, 100], [40, 102], [41, 94], [41, 101], [42, 83], [42, 88], [43, 83], [43, 85], [44, 82], [44, 92], [45, 84], [45, 86], [46, 84], [46, 87], [47, 82], [47, 91], [48, 81], [48, 90], [49, 81], [49, 89], [50, 93], [50, 109], [51, 98], [51, 109], [52, 96], [52, 110], [53, 99], [53, 110], [54, 94], [54, 111], [55, 95], [55, 111], [56, 97], [56, 112], [57, 100], [57, 112], [58, 104], [58, 116], [59, 108], [59, 115], [60, 105], [60, 113], [61, 107], [61, 113], [62, 102], [62, 116], [63, 103], [63, 114], [64, 106], [64, 115], [65, 101], [65, 114], [66, 87], [66, 92], [67, 86], [67, 90], [68, 85], [68, 91], [69, 85], [69, 90], [70, 88], [70, 92], [71, 88], [71, 89], [72, 86], [72, 91], [73, 87], [73, 89], [74, 95], [74, 96], [74, 101], [74, 105], [75, 97], [75, 98], [75, 102], [75, 106], [76, 93], [76, 100], [76, 104], [76, 108], [77, 94], [77, 99], [77, 103], [77, 107], [78, 109], [78, 112], [78, 115], [78, 116], [79, 110], [79, 111], [79, 113], [79, 114], [80, 81], [80, 82], [80, 83], [80, 84], [81, 125], [82, 126], [83, 127], [84, 128], [85, 121], [86, 122], [87, 124], [88, 123], [89, 120], [90, 119], [91, 118], [92, 117], [93, 121], [94, 123], [95, 121], [96, 122], [97, 122], [98, 123], [99, 124], [100, 124], [101, 119], [102, 120], [103, 120], [104, 119], [105, 118], [106, 118], [107, 117], [108, 117], [109, 125], [110, 125], [111, 126], [112, 126], [113, 127], [114, 128], [115, 128], [116, 127]]);;
R:=P177Census(D);;Need(Size(R.F)=512);;
PrintTo("current_c4_descent/128_054.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_054 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
