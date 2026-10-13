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
D:=P177Graph("120_043",120,[1, 3, 4, 6, 9, 11, 12, 14, 17, 19, 20, 22, 25, 28, 29, 31, 34, 36, 37, 40, 43, 45, 46, 50, 52, 53, 54, 55, 57, 59, 61, 62, 64, 68, 69, 71, 72, 76, 77, 79, 80, 81, 82, 83, 85, 86, 88, 90, 94, 96, 100, 103, 106, 108, 110, 114, 116, 117, 118, 119],[[1, 2], [1, 5], [1, 65], [1, 74], [2, 6], [2, 11], [2, 96], [3, 7], [3, 15], [3, 70], [3, 115], [4, 8], [4, 16], [4, 27], [4, 67], [5, 17], [5, 34], [5, 83], [6, 18], [6, 35], [6, 99], [7, 19], [7, 36], [7, 119], [8, 20], [8, 37], [8, 118], [9, 21], [9, 26], [9, 47], [9, 75], [10, 22], [10, 28], [10, 55], [10, 80], [11, 23], [11, 48], [11, 93], [12, 24], [12, 26], [12, 49], [12, 92], [13, 25], [13, 50], [13, 72], [13, 76], [14, 26], [14, 51], [14, 66], [14, 73], [15, 25], [15, 52], [15, 85], [16, 53], [16, 86], [16, 114], [17, 18], [17, 48], [17, 87], [18, 54], [18, 88], [19, 30], [19, 33], [19, 44], [20, 32], [20, 58], [20, 89], [21, 55], [21, 90], [21, 108], [22, 56], [22, 74], [22, 120], [23, 46], [23, 54], [23, 100], [24, 45], [24, 55], [24, 82], [25, 39], [25, 47], [26, 50], [27, 57], [27, 62], [27, 71], [28, 58], [28, 67], [28, 97], [29, 44], [29, 70], [29, 84], [29, 98], [30, 57], [30, 59], [30, 103], [31, 51], [31, 60], [31, 75], [31, 102], [32, 53], [32, 61], [32, 76], [33, 52], [33, 62], [33, 77], [34, 63], [34, 99], [34, 101], [35, 64], [35, 100], [35, 114], [36, 56], [36, 65], [36, 101], [37, 38], [37, 66], [37, 102], [38, 71], [38, 103], [38, 110], [39, 46], [39, 61], [39, 116], [40, 41], [40, 67], [40, 104], [40, 111], [41, 55], [41, 68], [41, 106], [42, 43], [42, 54], [42, 64], [42, 69], [43, 70], [43, 78], [43, 112], [44, 71], [44, 85], [45, 67], [45, 91], [45, 109], [46, 70], [46, 105], [47, 82], [47, 106], [48, 68], [48, 81], [49, 69], [49, 80], [49, 108], [50, 63], [50, 107], [51, 103], [51, 108], [52, 101], [52, 107], [53, 102], [53, 113], [54, 84], [56, 79], [56, 83], [57, 95], [57, 102], [58, 79], [58, 86], [59, 60], [59, 65], [59, 120], [60, 90], [60, 96], [61, 112], [61, 115], [62, 109], [62, 111], [63, 88], [63, 94], [64, 91], [64, 92], [65, 77], [66, 76], [66, 94], [68, 74], [68, 97], [69, 73], [69, 98], [71, 104], [72, 89], [72, 101], [72, 115], [73, 88], [73, 110], [74, 90], [75, 76], [75, 116], [77, 95], [77, 99], [78, 79], [78, 80], [78, 119], [79, 115], [80, 91], [81, 84], [81, 104], [81, 105], [82, 107], [82, 111], [83, 89], [83, 97], [84, 110], [85, 105], [85, 111], [86, 91], [86, 112], [87, 94], [87, 110], [87, 118], [88, 92], [89, 94], [90, 93], [92, 117], [93, 106], [93, 116], [95, 96], [95, 114], [96, 113], [97, 118], [98, 103], [98, 119], [99, 117], [100, 112], [100, 113], [104, 118], [105, 106], [107, 117], [108, 120], [109, 114], [109, 117], [113, 116], [119, 120]]);;
R:=P177Census(D);;Need(Size(R.F)=1440);;
PrintTo("current_c4_descent/120_043.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 120_043 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
