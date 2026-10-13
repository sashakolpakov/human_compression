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
D:=P177Graph("128_025",128,[1, 3, 9, 10, 12, 13, 14, 17, 18, 20, 23, 32, 34, 35, 36, 37, 38, 39, 41, 42, 43, 47, 48, 49, 51, 52, 54, 59, 60, 62, 65, 66, 69, 71, 74, 77, 82, 83, 85, 87, 88, 90, 91, 92, 94, 96, 97, 98, 99, 100, 103, 108, 111, 112, 113, 114, 115, 117, 119, 120, 121, 122, 127, 128],[[1, 70], [1, 86], [1, 101], [1, 106], [2, 3], [2, 41], [2, 51], [2, 62], [3, 8], [3, 15], [3, 70], [4, 32], [4, 34], [4, 39], [4, 117], [5, 20], [5, 34], [5, 43], [5, 114], [6, 14], [6, 37], [6, 48], [6, 127], [7, 60], [7, 100], [7, 112], [7, 113], [8, 92], [8, 98], [8, 111], [9, 19], [9, 31], [9, 50], [9, 57], [10, 30], [10, 44], [10, 81], [10, 118], [11, 52], [11, 65], [11, 91], [11, 100], [12, 50], [12, 55], [12, 61], [12, 72], [13, 27], [13, 57], [13, 84], [13, 95], [14, 63], [14, 109], [14, 125], [15, 32], [15, 66], [15, 90], [16, 48], [16, 85], [16, 87], [16, 113], [17, 22], [17, 46], [17, 72], [17, 76], [18, 24], [18, 40], [18, 95], [18, 118], [19, 60], [19, 65], [19, 115], [20, 72], [20, 79], [20, 110], [21, 49], [21, 99], [21, 108], [21, 120], [22, 35], [22, 88], [22, 114], [23, 33], [23, 75], [23, 101], [23, 126], [24, 41], [24, 90], [24, 120], [25, 35], [25, 43], [25, 85], [25, 112], [26, 36], [26, 91], [26, 111], [26, 128], [27, 41], [27, 49], [27, 59], [28, 34], [28, 38], [28, 83], [28, 121], [29, 51], [29, 52], [29, 54], [29, 92], [30, 35], [30, 52], [30, 128], [31, 71], [31, 77], [31, 120], [32, 93], [32, 101], [33, 38], [33, 48], [33, 97], [34, 126], [35, 67], [36, 64], [36, 68], [36, 81], [37, 61], [37, 78], [37, 124], [38, 89], [38, 93], [39, 84], [39, 118], [39, 123], [40, 52], [40, 71], [40, 88], [41, 123], [42, 56], [42, 89], [42, 106], [42, 124], [43, 44], [43, 45], [44, 103], [44, 117], [45, 60], [45, 87], [45, 119], [46, 87], [46, 103], [46, 122], [47, 56], [47, 78], [47, 104], [47, 116], [48, 86], [49, 80], [49, 104], [50, 99], [50, 119], [51, 58], [51, 116], [53, 59], [53, 66], [53, 74], [53, 111], [54, 68], [54, 78], [54, 109], [55, 71], [55, 100], [55, 108], [56, 97], [56, 113], [57, 82], [57, 94], [58, 74], [58, 96], [58, 128], [59, 63], [59, 116], [60, 110], [61, 87], [61, 115], [62, 104], [62, 107], [62, 109], [63, 82], [63, 97], [64, 88], [64, 92], [64, 103], [65, 81], [65, 95], [66, 84], [66, 107], [67, 92], [67, 96], [67, 122], [68, 71], [68, 115], [69, 76], [69, 79], [69, 101], [69, 102], [70, 96], [70, 121], [72, 112], [73, 85], [73, 98], [73, 103], [73, 128], [74, 93], [74, 123], [75, 82], [75, 99], [75, 127], [76, 117], [76, 119], [77, 81], [77, 84], [77, 105], [78, 100], [79, 83], [79, 99], [80, 83], [80, 94], [80, 97], [82, 107], [83, 106], [85, 89], [86, 98], [86, 122], [88, 105], [89, 96], [90, 102], [90, 105], [91, 116], [91, 125], [93, 98], [94, 110], [94, 126], [95, 108], [102, 114], [102, 121], [104, 127], [105, 117], [106, 127], [107, 120], [108, 110], [109, 111], [112, 124], [113, 125], [114, 118], [115, 125], [119, 126], [121, 123], [122, 124]]);;
R:=P177Census(D);;Need(Size(R.F)=1024);;
PrintTo("current_c4_descent/128_025.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 128_025 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
