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
D:=P177Graph("096_021",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 60], [1, 66], [1, 67], [2, 60], [2, 67], [2, 72], [2, 74], [3, 55], [3, 62], [3, 71], [3, 77], [4, 55], [4, 60], [4, 93], [4, 95], [5, 55], [5, 57], [5, 62], [5, 65], [6, 55], [6, 63], [6, 81], [6, 95], [7, 54], [7, 59], [7, 61], [7, 64], [8, 68], [8, 71], [8, 73], [8, 77], [9, 49], [9, 61], [9, 78], [9, 94], [10, 64], [10, 67], [10, 83], [10, 85], [11, 60], [11, 68], [11, 87], [11, 93], [12, 56], [12, 84], [12, 94], [12, 95], [13, 59], [13, 64], [13, 70], [13, 76], [14, 57], [14, 65], [14, 68], [14, 73], [15, 61], [15, 72], [15, 89], [15, 94], [16, 58], [16, 64], [16, 83], [16, 90], [17, 63], [17, 68], [17, 81], [17, 87], [18, 83], [18, 84], [18, 87], [18, 94], [19, 54], [19, 61], [19, 69], [19, 75], [20, 69], [20, 70], [20, 75], [20, 76], [21, 51], [21, 69], [21, 77], [21, 88], [22, 49], [22, 58], [22, 63], [22, 66], [23, 49], [23, 53], [23, 76], [23, 78], [24, 66], [24, 71], [24, 80], [24, 91], [25, 52], [25, 79], [25, 88], [25, 93], [26, 56], [26, 67], [26, 75], [26, 85], [27, 62], [27, 70], [27, 92], [27, 96], [28, 53], [28, 56], [28, 91], [28, 95], [29, 53], [29, 83], [29, 87], [29, 91], [30, 52], [30, 57], [30, 74], [30, 84], [31, 51], [31, 59], [31, 77], [31, 86], [32, 58], [32, 63], [32, 72], [32, 74], [33, 53], [33, 72], [33, 76], [33, 89], [34, 52], [34, 71], [34, 74], [34, 91], [35, 65], [35, 69], [35, 82], [35, 88], [36, 52], [36, 81], [36, 88], [36, 96], [37, 56], [37, 58], [37, 75], [37, 90], [38, 50], [38, 70], [38, 73], [38, 96], [39, 59], [39, 65], [39, 82], [39, 86], [40, 50], [40, 54], [40, 73], [40, 79], [41, 78], [41, 82], [41, 90], [41, 92], [42, 57], [42, 66], [42, 80], [42, 84], [43, 79], [43, 80], [43, 86], [43, 93], [44, 50], [44, 51], [44, 85], [44, 89], [45, 54], [45, 62], [45, 79], [45, 92], [46, 80], [46, 81], [46, 86], [46, 96], [47, 51], [47, 78], [47, 85], [47, 92], [48, 50], [48, 82], [48, 89], [48, 90]]);;
R:=P177Census(D);;Need(Size(R.F)=192);;
PrintTo("current_c4_descent/096_021.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_021 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
