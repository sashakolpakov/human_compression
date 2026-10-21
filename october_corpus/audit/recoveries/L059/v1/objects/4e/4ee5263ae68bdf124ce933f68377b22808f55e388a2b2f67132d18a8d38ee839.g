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
D:=P177Graph("096_038",96,[1, 4, 5, 6, 8, 12, 15, 17, 18, 19, 22, 23, 25, 26, 31, 33, 36, 40, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 59, 68, 70, 71, 72, 73, 74, 75, 76, 78, 79, 80, 81, 90, 91, 92, 93, 96],[[1, 2], [1, 3], [1, 20], [1, 30], [2, 4], [2, 5], [2, 45], [3, 6], [3, 8], [3, 48], [4, 7], [4, 9], [4, 58], [5, 10], [5, 13], [5, 61], [6, 11], [6, 14], [6, 62], [7, 12], [7, 15], [7, 71], [8, 16], [8, 21], [8, 55], [9, 17], [9, 22], [9, 72], [10, 18], [10, 23], [10, 73], [11, 19], [11, 22], [11, 78], [12, 20], [12, 24], [12, 83], [13, 25], [13, 31], [13, 68], [14, 15], [14, 26], [14, 81], [15, 27], [15, 32], [16, 25], [16, 33], [16, 75], [17, 28], [17, 34], [17, 84], [18, 21], [18, 29], [18, 32], [19, 30], [19, 35], [19, 85], [20, 36], [20, 46], [21, 46], [21, 80], [22, 37], [22, 39], [23, 24], [23, 38], [23, 89], [24, 40], [24, 47], [25, 37], [25, 43], [26, 38], [26, 41], [26, 86], [27, 42], [27, 48], [27, 90], [28, 31], [28, 44], [28, 47], [29, 45], [29, 49], [29, 91], [30, 31], [30, 50], [31, 88], [32, 51], [32, 53], [33, 34], [33, 35], [33, 87], [34, 36], [34, 52], [35, 40], [35, 59], [36, 54], [36, 60], [37, 51], [37, 56], [38, 50], [38, 52], [39, 42], [39, 45], [39, 93], [40, 55], [40, 61], [41, 44], [41, 46], [41, 59], [42, 57], [42, 60], [43, 48], [43, 49], [43, 92], [44, 58], [44, 62], [45, 63], [46, 82], [47, 64], [47, 66], [48, 65], [49, 54], [49, 67], [50, 57], [50, 67], [51, 64], [51, 69], [52, 63], [52, 65], [53, 55], [53, 58], [53, 95], [54, 68], [54, 72], [55, 70], [56, 61], [56, 62], [56, 94], [57, 71], [57, 73], [58, 74], [59, 69], [59, 77], [60, 75], [60, 78], [61, 76], [62, 79], [63, 70], [63, 79], [64, 75], [64, 81], [65, 74], [65, 76], [66, 68], [66, 71], [66, 96], [67, 80], [67, 81], [68, 82], [69, 72], [69, 73], [70, 83], [70, 84], [71, 85], [72, 86], [73, 87], [74, 82], [74, 87], [75, 89], [76, 85], [76, 86], [77, 78], [77, 80], [77, 96], [78, 83], [79, 88], [79, 89], [80, 88], [81, 84], [82, 90], [83, 91], [84, 92], [85, 92], [86, 91], [87, 93], [88, 93], [89, 90], [90, 94], [91, 94], [92, 95], [93, 95], [94, 96], [95, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_038.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_038 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
