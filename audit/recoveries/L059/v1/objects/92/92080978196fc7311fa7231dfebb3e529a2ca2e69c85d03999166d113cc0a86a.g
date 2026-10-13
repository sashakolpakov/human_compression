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
D:=P177Graph("CSS_110_1",110,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 51, 53, 55, 57, 59, 61, 63, 65, 67, 69, 71, 73, 75, 77, 79, 81, 83, 85, 87, 89, 91, 93, 95, 97, 99, 101, 103, 105, 107, 109],[[1, 2], [1, 32], [1, 110], [2, 3], [2, 81], [3, 4], [3, 104], [4, 5], [4, 13], [5, 6], [5, 46], [6, 7], [6, 75], [7, 8], [7, 58], [8, 9], [8, 67], [9, 10], [9, 100], [10, 11], [10, 29], [11, 12], [11, 42], [12, 13], [12, 91], [13, 14], [14, 15], [14, 23], [15, 16], [15, 56], [16, 17], [16, 85], [17, 18], [17, 68], [18, 19], [18, 77], [19, 20], [19, 110], [20, 21], [20, 39], [21, 22], [21, 52], [22, 23], [22, 101], [23, 24], [24, 25], [24, 33], [25, 26], [25, 66], [26, 27], [26, 95], [27, 28], [27, 78], [28, 29], [28, 87], [29, 30], [30, 31], [30, 49], [31, 32], [31, 62], [32, 33], [33, 34], [34, 35], [34, 43], [35, 36], [35, 76], [36, 37], [36, 105], [37, 38], [37, 88], [38, 39], [38, 97], [39, 40], [40, 41], [40, 59], [41, 42], [41, 72], [42, 43], [43, 44], [44, 45], [44, 53], [45, 46], [45, 86], [46, 47], [47, 48], [47, 98], [48, 49], [48, 107], [49, 50], [50, 51], [50, 69], [51, 52], [51, 82], [52, 53], [53, 54], [54, 55], [54, 63], [55, 56], [55, 96], [56, 57], [57, 58], [57, 108], [58, 59], [59, 60], [60, 61], [60, 79], [61, 62], [61, 92], [62, 63], [63, 64], [64, 65], [64, 73], [65, 66], [65, 106], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [70, 89], [71, 72], [71, 102], [72, 73], [73, 74], [74, 75], [74, 83], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [80, 99], [81, 82], [82, 83], [83, 84], [84, 85], [84, 93], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [90, 109], [91, 92], [92, 93], [93, 94], [94, 95], [94, 103], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100], [100, 101], [101, 102], [102, 103], [103, 104], [104, 105], [105, 106], [106, 107], [107, 108], [108, 109], [109, 110]]);;
R:=P177Census(D);;
Need(Size(R.F)=Size(R.A));;
PrintTo("cubic_markings/CSS_110_1.g","L059Result := ",R,";\n");
Print("L059_CUBIC_COMPLETE CSS_110_1 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
