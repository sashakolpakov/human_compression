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
D:=P177Graph("096_014",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80],[[1, 17], [1, 18], [1, 81], [1, 89], [2, 19], [2, 20], [2, 81], [2, 89], [3, 21], [3, 22], [3, 82], [3, 90], [4, 23], [4, 24], [4, 82], [4, 90], [5, 25], [5, 26], [5, 83], [5, 91], [6, 27], [6, 28], [6, 83], [6, 91], [7, 29], [7, 30], [7, 84], [7, 92], [8, 31], [8, 32], [8, 84], [8, 92], [9, 17], [9, 18], [9, 85], [9, 93], [10, 19], [10, 20], [10, 85], [10, 93], [11, 21], [11, 22], [11, 86], [11, 94], [12, 23], [12, 24], [12, 86], [12, 94], [13, 25], [13, 26], [13, 87], [13, 95], [14, 27], [14, 28], [14, 87], [14, 95], [15, 29], [15, 30], [15, 88], [15, 96], [16, 31], [16, 32], [16, 88], [16, 96], [17, 33], [17, 34], [18, 35], [18, 36], [19, 37], [19, 38], [20, 39], [20, 40], [21, 41], [21, 42], [22, 43], [22, 44], [23, 45], [23, 46], [24, 47], [24, 48], [25, 33], [25, 34], [26, 35], [26, 36], [27, 37], [27, 38], [28, 39], [28, 40], [29, 41], [29, 42], [30, 43], [30, 44], [31, 45], [31, 46], [32, 47], [32, 48], [33, 49], [33, 50], [34, 51], [34, 52], [35, 53], [35, 54], [36, 55], [36, 56], [37, 57], [37, 58], [38, 59], [38, 60], [39, 61], [39, 62], [40, 63], [40, 64], [41, 49], [41, 50], [42, 51], [42, 52], [43, 53], [43, 54], [44, 55], [44, 56], [45, 57], [45, 58], [46, 59], [46, 60], [47, 61], [47, 62], [48, 63], [48, 64], [49, 65], [49, 66], [50, 67], [50, 68], [51, 69], [51, 70], [52, 71], [52, 72], [53, 73], [53, 74], [54, 75], [54, 76], [55, 77], [55, 78], [56, 79], [56, 80], [57, 65], [57, 66], [58, 67], [58, 68], [59, 69], [59, 70], [60, 71], [60, 72], [61, 73], [61, 74], [62, 75], [62, 76], [63, 77], [63, 78], [64, 79], [64, 80], [65, 81], [65, 82], [66, 83], [66, 84], [67, 85], [67, 86], [68, 87], [68, 88], [69, 89], [69, 90], [70, 91], [70, 92], [71, 93], [71, 94], [72, 95], [72, 96], [73, 81], [73, 82], [74, 83], [74, 84], [75, 85], [75, 86], [76, 87], [76, 88], [77, 89], [77, 90], [78, 91], [78, 92], [79, 93], [79, 94], [80, 95], [80, 96]]);;
R:=P177Census(D);;Need(Size(R.F)=768);;
PrintTo("current_c4_descent/096_014.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_014 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
