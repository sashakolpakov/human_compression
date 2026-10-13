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
D:=P177Graph("098_002",98,[1, 3, 5, 7, 9, 11, 13, 16, 18, 20, 22, 24, 26, 28, 29, 31, 33, 35, 37, 39, 41, 44, 46, 48, 50, 52, 54, 56, 57, 59, 61, 63, 65, 67, 69, 72, 74, 76, 78, 80, 82, 84, 85, 87, 89, 91, 93, 95, 97],[[1, 2], [1, 14], [1, 15], [1, 92], [2, 3], [2, 16], [2, 93], [3, 4], [3, 17], [3, 94], [4, 5], [4, 18], [4, 95], [5, 6], [5, 19], [5, 96], [6, 7], [6, 20], [6, 97], [7, 8], [7, 21], [7, 98], [8, 9], [8, 22], [8, 85], [9, 10], [9, 23], [9, 86], [10, 11], [10, 24], [10, 87], [11, 12], [11, 25], [11, 88], [12, 13], [12, 26], [12, 89], [13, 14], [13, 27], [13, 90], [14, 28], [14, 91], [15, 16], [15, 28], [15, 29], [16, 17], [16, 30], [17, 18], [17, 31], [18, 19], [18, 32], [19, 20], [19, 33], [20, 21], [20, 34], [21, 22], [21, 35], [22, 23], [22, 36], [23, 24], [23, 37], [24, 25], [24, 38], [25, 26], [25, 39], [26, 27], [26, 40], [27, 28], [27, 41], [28, 42], [29, 30], [29, 42], [29, 43], [30, 31], [30, 44], [31, 32], [31, 45], [32, 33], [32, 46], [33, 34], [33, 47], [34, 35], [34, 48], [35, 36], [35, 49], [36, 37], [36, 50], [37, 38], [37, 51], [38, 39], [38, 52], [39, 40], [39, 53], [40, 41], [40, 54], [41, 42], [41, 55], [42, 56], [43, 44], [43, 56], [43, 57], [44, 45], [44, 58], [45, 46], [45, 59], [46, 47], [46, 60], [47, 48], [47, 61], [48, 49], [48, 62], [49, 50], [49, 63], [50, 51], [50, 64], [51, 52], [51, 65], [52, 53], [52, 66], [53, 54], [53, 67], [54, 55], [54, 68], [55, 56], [55, 69], [56, 70], [57, 58], [57, 70], [57, 71], [58, 59], [58, 72], [59, 60], [59, 73], [60, 61], [60, 74], [61, 62], [61, 75], [62, 63], [62, 76], [63, 64], [63, 77], [64, 65], [64, 78], [65, 66], [65, 79], [66, 67], [66, 80], [67, 68], [67, 81], [68, 69], [68, 82], [69, 70], [69, 83], [70, 84], [71, 72], [71, 84], [71, 85], [72, 73], [72, 86], [73, 74], [73, 87], [74, 75], [74, 88], [75, 76], [75, 89], [76, 77], [76, 90], [77, 78], [77, 91], [78, 79], [78, 92], [79, 80], [79, 93], [80, 81], [80, 94], [81, 82], [81, 95], [82, 83], [82, 96], [83, 84], [83, 97], [84, 98], [85, 86], [85, 98], [86, 87], [87, 88], [88, 89], [89, 90], [90, 91], [91, 92], [92, 93], [93, 94], [94, 95], [95, 96], [96, 97], [97, 98]]);;
R:=P177Census(D);;Need(Size(R.F)=784);;
PrintTo("current_c4_descent/098_002.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 098_002 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
