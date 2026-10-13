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
D:=P177Graph("100_003",100,[1, 3, 5, 7, 9, 12, 14, 16, 18, 20, 21, 23, 25, 27, 29, 32, 34, 36, 38, 40, 41, 43, 45, 47, 49, 52, 54, 56, 58, 60, 61, 63, 65, 67, 69, 72, 74, 76, 78, 80, 81, 83, 85, 87, 89, 92, 94, 96, 98, 100],[[1, 2], [1, 10], [1, 11], [1, 91], [2, 3], [2, 12], [2, 92], [3, 4], [3, 13], [3, 93], [4, 5], [4, 14], [4, 94], [5, 6], [5, 15], [5, 95], [6, 7], [6, 16], [6, 96], [7, 8], [7, 17], [7, 97], [8, 9], [8, 18], [8, 98], [9, 10], [9, 19], [9, 99], [10, 20], [10, 100], [11, 12], [11, 20], [11, 21], [12, 13], [12, 22], [13, 14], [13, 23], [14, 15], [14, 24], [15, 16], [15, 25], [16, 17], [16, 26], [17, 18], [17, 27], [18, 19], [18, 28], [19, 20], [19, 29], [20, 30], [21, 22], [21, 30], [21, 31], [22, 23], [22, 32], [23, 24], [23, 33], [24, 25], [24, 34], [25, 26], [25, 35], [26, 27], [26, 36], [27, 28], [27, 37], [28, 29], [28, 38], [29, 30], [29, 39], [30, 40], [31, 32], [31, 40], [31, 41], [32, 33], [32, 42], [33, 34], [33, 43], [34, 35], [34, 44], [35, 36], [35, 45], [36, 37], [36, 46], [37, 38], [37, 47], [38, 39], [38, 48], [39, 40], [39, 49], [40, 50], [41, 42], [41, 50], [41, 51], [42, 43], [42, 52], [43, 44], [43, 53], [44, 45], [44, 54], [45, 46], [45, 55], [46, 47], [46, 56], [47, 48], [47, 57], [48, 49], [48, 58], [49, 50], [49, 59], [50, 60], [51, 52], [51, 60], [51, 61], [52, 53], [52, 62], [53, 54], [53, 63], [54, 55], [54, 64], [55, 56], [55, 65], [56, 57], [56, 66], [57, 58], [57, 67], [58, 59], [58, 68], [59, 60], [59, 69], [60, 70], [61, 62], [61, 70], [61, 71], [62, 63], [62, 72], [63, 64], [63, 73], [64, 65], [64, 74], [65, 66], [65, 75], [66, 67], [66, 76], [67, 68], [67, 77], [68, 69], [68, 78], [69, 70], [69, 79], [70, 80], [71, 72], [71, 80], [71, 81], [72, 73], [72, 82], [73, 74], [73, 83], [74, 75], [74, 84], [75, 76], [75, 85], [76, 77], [76, 86], [77, 78], [77, 87], [78, 79], [78, 88], [79, 80], [79, 89], [80, 90], [81, 82], [81, 90], [81, 91], [82, 83], [82, 92], [83, 84], [83, 93], [84, 85], [84, 94], [85, 86], [85, 95], [86, 87], [86, 96], [87, 88], [87, 97], [88, 89], [88, 98], [89, 90], [89, 99], [90, 100], [91, 92], [91, 100], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98], [98, 99], [99, 100]]);;
R:=P177Census(D);;Need(Size(R.F)=800);;
PrintTo("current_c4_descent/100_003.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 100_003 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
