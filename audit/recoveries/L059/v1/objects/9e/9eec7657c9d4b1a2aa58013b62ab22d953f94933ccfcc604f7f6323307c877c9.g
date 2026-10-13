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
D:=P177Graph("128_055",128,[1, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128],[[1, 2], [1, 3], [1, 4], [1, 5], [2, 117], [2, 118], [2, 119], [3, 120], [3, 121], [3, 122], [4, 123], [4, 126], [4, 127], [5, 124], [5, 125], [5, 128], [6, 36], [6, 48], [6, 50], [6, 76], [7, 39], [7, 48], [7, 53], [7, 77], [8, 38], [8, 49], [8, 52], [8, 77], [9, 37], [9, 49], [9, 51], [9, 76], [10, 40], [10, 45], [10, 51], [10, 75], [11, 43], [11, 46], [11, 52], [11, 72], [12, 41], [12, 47], [12, 53], [12, 74], [13, 42], [13, 44], [13, 50], [13, 73], [14, 36], [14, 41], [14, 55], [14, 72], [15, 38], [15, 40], [15, 54], [15, 73], [16, 37], [16, 43], [16, 57], [16, 74], [17, 39], [17, 42], [17, 56], [17, 75], [18, 33], [18, 45], [18, 64], [18, 71], [19, 32], [19, 44], [19, 63], [19, 71], [20, 35], [20, 47], [20, 65], [20, 70], [21, 34], [21, 46], [21, 62], [21, 70], [22, 30], [22, 34], [22, 58], [22, 69], [23, 30], [23, 33], [23, 59], [23, 68], [24, 31], [24, 35], [24, 61], [24, 68], [25, 31], [25, 32], [25, 60], [25, 69], [26, 54], [26, 58], [26, 64], [26, 66], [27, 57], [27, 59], [27, 62], [27, 67], [28, 56], [28, 61], [28, 63], [28, 66], [29, 55], [29, 60], [29, 65], [29, 67], [30, 82], [30, 84], [31, 81], [31, 83], [32, 94], [32, 100], [33, 96], [33, 99], [34, 95], [34, 98], [35, 93], [35, 97], [36, 83], [36, 102], [37, 84], [37, 104], [38, 83], [38, 103], [39, 84], [39, 101], [40, 91], [40, 98], [41, 90], [41, 99], [42, 92], [42, 97], [43, 89], [43, 100], [44, 85], [44, 90], [45, 87], [45, 89], [46, 88], [46, 92], [47, 86], [47, 91], [48, 94], [48, 95], [49, 93], [49, 96], [50, 82], [50, 87], [51, 81], [51, 85], [52, 82], [52, 86], [53, 81], [53, 88], [54, 100], [54, 101], [55, 98], [55, 104], [56, 99], [56, 103], [57, 97], [57, 102], [58, 90], [58, 93], [59, 91], [59, 94], [60, 92], [60, 96], [61, 89], [61, 95], [62, 85], [62, 103], [63, 86], [63, 104], [64, 88], [64, 102], [65, 87], [65, 101], [66, 105], [66, 116], [67, 105], [67, 115], [68, 106], [68, 109], [69, 107], [69, 108], [70, 113], [70, 114], [71, 112], [71, 114], [72, 106], [72, 110], [73, 109], [73, 111], [74, 108], [74, 111], [75, 107], [75, 110], [76, 113], [76, 116], [77, 112], [77, 115], [78, 105], [78, 110], [78, 111], [78, 114], [79, 106], [79, 108], [79, 112], [79, 116], [80, 107], [80, 109], [80, 113], [80, 115], [81, 117], [82, 117], [83, 120], [84, 120], [85, 123], [86, 126], [87, 125], [88, 124], [89, 122], [90, 122], [91, 121], [92, 121], [93, 128], [94, 128], [95, 127], [96, 127], [97, 119], [98, 119], [99, 118], [100, 118], [101, 123], [102, 126], [103, 125], [104, 124], [105, 117], [106, 123], [107, 126], [108, 125], [109, 124], [110, 128], [111, 127], [112, 119], [113, 118], [114, 120], [115, 122], [116, 121]]);;
R:=P177Census(D);;Need(Size(R.F)=1536);;
PrintTo("current_c4_descent/128_055.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_055 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
