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
D:=P177Graph("100_002",100,[1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43, 45, 47, 49, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100],[[1, 2], [1, 50], [1, 51], [1, 87], [2, 3], [2, 52], [2, 88], [3, 4], [3, 53], [3, 89], [4, 5], [4, 54], [4, 90], [5, 6], [5, 55], [5, 91], [6, 7], [6, 56], [6, 92], [7, 8], [7, 57], [7, 93], [8, 9], [8, 58], [8, 94], [9, 10], [9, 59], [9, 95], [10, 11], [10, 60], [10, 96], [11, 12], [11, 61], [11, 97], [12, 13], [12, 62], [12, 98], [13, 14], [13, 63], [13, 99], [14, 15], [14, 64], [14, 100], [15, 16], [15, 51], [15, 65], [16, 17], [16, 52], [16, 66], [17, 18], [17, 53], [17, 67], [18, 19], [18, 54], [18, 68], [19, 20], [19, 55], [19, 69], [20, 21], [20, 56], [20, 70], [21, 22], [21, 57], [21, 71], [22, 23], [22, 58], [22, 72], [23, 24], [23, 59], [23, 73], [24, 25], [24, 60], [24, 74], [25, 26], [25, 61], [25, 75], [26, 27], [26, 62], [26, 76], [27, 28], [27, 63], [27, 77], [28, 29], [28, 64], [28, 78], [29, 30], [29, 65], [29, 79], [30, 31], [30, 66], [30, 80], [31, 32], [31, 67], [31, 81], [32, 33], [32, 68], [32, 82], [33, 34], [33, 69], [33, 83], [34, 35], [34, 70], [34, 84], [35, 36], [35, 71], [35, 85], [36, 37], [36, 72], [36, 86], [37, 38], [37, 73], [37, 87], [38, 39], [38, 74], [38, 88], [39, 40], [39, 75], [39, 89], [40, 41], [40, 76], [40, 90], [41, 42], [41, 77], [41, 91], [42, 43], [42, 78], [42, 92], [43, 44], [43, 79], [43, 93], [44, 45], [44, 80], [44, 94], [45, 46], [45, 81], [45, 95], [46, 47], [46, 82], [46, 96], [47, 48], [47, 83], [47, 97], [48, 49], [48, 84], [48, 98], [49, 50], [49, 85], [49, 99], [50, 86], [50, 100], [51, 52], [51, 100], [52, 53], [53, 54], [54, 55], [55, 56], [56, 57], [57, 58], [58, 59], [59, 60], [60, 61], [61, 62], [62, 63], [63, 64], [64, 65], [65, 66], [66, 67], [67, 68], [68, 69], [69, 70], [70, 71], [71, 72], [72, 73], [73, 74], [74, 75], [75, 76], [76, 77], [77, 78], [78, 79], [79, 80], [80, 81], [81, 82], [82, 83], [83, 84], [84, 85], [85, 86], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100]]);;
R:=P177Census(D);;Need(Size(R.F)=400);;
PrintTo("current_c4_descent/100_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 100_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
