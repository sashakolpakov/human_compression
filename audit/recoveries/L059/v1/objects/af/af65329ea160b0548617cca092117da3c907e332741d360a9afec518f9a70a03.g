Need:=function(ok) if not ok then Error("L059 cubic census invalid"); fi; end;;
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
D:=P177Graph("VT3_112_37",112,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 103, 104, 105, 106, 107, 108, 112],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 30], [15, 37], [16, 31], [16, 38], [17, 25], [17, 32], [18, 33], [18, 34], [19, 34], [19, 39], [20, 28], [20, 40], [21, 31], [21, 35], [22, 23], [22, 36], [23, 47], [24, 41], [24, 48], [25, 42], [26, 43], [26, 44], [27, 44], [27, 49], [28, 50], [29, 41], [29, 45], [30, 46], [31, 60], [32, 51], [32, 61], [33, 52], [33, 62], [34, 53], [35, 54], [35, 56], [36, 55], [36, 57], [37, 56], [37, 63], [38, 57], [38, 64], [39, 51], [39, 58], [40, 52], [40, 59], [41, 74], [42, 65], [42, 75], [43, 66], [43, 76], [44, 67], [45, 68], [45, 70], [46, 69], [46, 71], [47, 70], [47, 77], [48, 71], [48, 78], [49, 65], [49, 72], [50, 66], [50, 73], [51, 87], [52, 88], [53, 79], [53, 80], [54, 75], [54, 86], [55, 72], [55, 80], [56, 81], [57, 82], [58, 69], [58, 83], [59, 78], [59, 84], [60, 84], [60, 85], [61, 68], [61, 85], [62, 77], [62, 83], [63, 76], [63, 79], [64, 73], [64, 86], [65, 97], [66, 98], [67, 89], [67, 90], [68, 96], [69, 90], [70, 91], [71, 92], [72, 93], [73, 94], [74, 94], [74, 95], [75, 95], [76, 93], [77, 89], [78, 96], [79, 101], [80, 102], [81, 92], [81, 100], [82, 91], [82, 99], [83, 96], [84, 100], [85, 99], [86, 93], [87, 97], [87, 102], [88, 98], [88, 101], [89, 105], [90, 106], [91, 104], [92, 103], [94, 104], [95, 103], [97, 106], [98, 105], [99, 107], [100, 108], [101, 108], [102, 107], [103, 109], [104, 110], [105, 110], [106, 109], [107, 111], [108, 111], [109, 112], [110, 112], [111, 112]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_112_37.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_112_37 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
