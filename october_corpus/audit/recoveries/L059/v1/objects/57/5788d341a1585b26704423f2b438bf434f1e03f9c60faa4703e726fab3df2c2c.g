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
D:=P177Graph("VT3_120_101",120,[1, 5, 6, 7, 8, 9, 10, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 113, 114, 115, 116, 117, 118, 119, 120],[[1, 2], [1, 3], [1, 4], [2, 5], [2, 6], [3, 7], [3, 9], [4, 8], [4, 10], [5, 11], [5, 13], [6, 12], [6, 14], [7, 15], [7, 19], [8, 16], [8, 20], [9, 17], [9, 21], [10, 18], [10, 22], [11, 23], [11, 27], [12, 24], [12, 28], [13, 25], [13, 29], [14, 26], [14, 30], [15, 30], [15, 38], [16, 31], [16, 39], [17, 32], [17, 40], [18, 33], [18, 41], [19, 34], [19, 42], [20, 35], [20, 43], [21, 31], [21, 36], [22, 23], [22, 37], [23, 51], [24, 44], [24, 52], [25, 45], [25, 53], [26, 46], [26, 54], [27, 47], [27, 55], [28, 48], [28, 56], [29, 44], [29, 49], [30, 50], [31, 66], [32, 57], [32, 61], [33, 46], [33, 58], [34, 59], [34, 64], [35, 48], [35, 60], [36, 52], [36, 67], [37, 61], [37, 68], [38, 62], [38, 65], [39, 49], [39, 63], [40, 53], [40, 69], [41, 64], [41, 70], [42, 55], [42, 57], [43, 58], [43, 65], [44, 80], [45, 71], [45, 75], [46, 72], [47, 73], [47, 78], [48, 74], [49, 81], [50, 75], [50, 82], [51, 76], [51, 79], [52, 77], [53, 83], [54, 78], [54, 84], [55, 71], [56, 72], [56, 79], [57, 91], [58, 92], [59, 85], [59, 89], [60, 76], [60, 81], [61, 86], [62, 74], [62, 87], [63, 83], [63, 88], [64, 78], [65, 85], [66, 89], [66, 90], [67, 74], [67, 93], [68, 83], [68, 94], [69, 77], [69, 82], [70, 86], [70, 90], [71, 101], [72, 102], [73, 95], [73, 99], [75, 96], [76, 97], [77, 98], [79, 95], [80, 99], [80, 100], [81, 103], [82, 104], [84, 96], [84, 100], [85, 112], [86, 107], [87, 104], [87, 108], [88, 105], [88, 109], [89, 106], [90, 105], [91, 108], [91, 110], [92, 109], [92, 111], [93, 106], [93, 110], [94, 97], [94, 111], [95, 120], [96, 115], [97, 116], [98, 113], [98, 117], [99, 114], [100, 113], [101, 116], [101, 118], [102, 117], [102, 119], [103, 114], [103, 118], [104, 119], [105, 113], [106, 114], [107, 117], [107, 120], [108, 116], [109, 115], [110, 120], [111, 119], [112, 115], [112, 118]]);;
R:=P177Census(D);;
Need(Size(R.F)=2*Size(R.A));;
PrintTo("cubic_markings/VT3_120_101.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE VT3_120_101 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
