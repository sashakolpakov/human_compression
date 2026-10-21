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
D:=P177Graph("100_008",100,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75],[[1, 31], [1, 46], [1, 90], [1, 92], [2, 32], [2, 47], [2, 86], [2, 93], [3, 33], [3, 48], [3, 87], [3, 94], [4, 34], [4, 49], [4, 88], [4, 95], [5, 35], [5, 50], [5, 89], [5, 91], [6, 26], [6, 36], [6, 95], [6, 97], [7, 27], [7, 37], [7, 91], [7, 98], [8, 28], [8, 38], [8, 92], [8, 99], [9, 29], [9, 39], [9, 93], [9, 100], [10, 30], [10, 40], [10, 94], [10, 96], [11, 31], [11, 41], [11, 77], [11, 100], [12, 32], [12, 42], [12, 78], [12, 96], [13, 33], [13, 43], [13, 79], [13, 97], [14, 34], [14, 44], [14, 80], [14, 98], [15, 35], [15, 45], [15, 76], [15, 99], [16, 36], [16, 46], [16, 80], [16, 82], [17, 37], [17, 47], [17, 76], [17, 83], [18, 38], [18, 48], [18, 77], [18, 84], [19, 39], [19, 49], [19, 78], [19, 85], [20, 40], [20, 50], [20, 79], [20, 81], [21, 26], [21, 41], [21, 85], [21, 87], [22, 27], [22, 42], [22, 81], [22, 88], [23, 28], [23, 43], [23, 82], [23, 89], [24, 29], [24, 44], [24, 83], [24, 90], [25, 30], [25, 45], [25, 84], [25, 86], [26, 58], [26, 74], [27, 59], [27, 75], [28, 60], [28, 71], [29, 56], [29, 72], [30, 57], [30, 73], [31, 54], [31, 63], [32, 55], [32, 64], [33, 51], [33, 65], [34, 52], [34, 61], [35, 53], [35, 62], [36, 59], [36, 68], [37, 60], [37, 69], [38, 56], [38, 70], [39, 57], [39, 66], [40, 58], [40, 67], [41, 64], [41, 73], [42, 65], [42, 74], [43, 61], [43, 75], [44, 62], [44, 71], [45, 63], [45, 72], [46, 53], [46, 69], [47, 54], [47, 70], [48, 55], [48, 66], [49, 51], [49, 67], [50, 52], [50, 68], [51, 86], [51, 91], [52, 87], [52, 92], [53, 88], [53, 93], [54, 89], [54, 94], [55, 90], [55, 95], [56, 91], [56, 96], [57, 92], [57, 97], [58, 93], [58, 98], [59, 94], [59, 99], [60, 95], [60, 100], [61, 76], [61, 96], [62, 77], [62, 97], [63, 78], [63, 98], [64, 79], [64, 99], [65, 80], [65, 100], [66, 76], [66, 81], [67, 77], [67, 82], [68, 78], [68, 83], [69, 79], [69, 84], [70, 80], [70, 85], [71, 81], [71, 86], [72, 82], [72, 87], [73, 83], [73, 88], [74, 84], [74, 89], [75, 85], [75, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=800);;
PrintTo("current_c4_descent/100_008.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 100_008 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
