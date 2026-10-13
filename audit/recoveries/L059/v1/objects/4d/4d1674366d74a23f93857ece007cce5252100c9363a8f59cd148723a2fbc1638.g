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
D:=P177Graph("096_029",96,[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],[[1, 49], [1, 54], [1, 63], [1, 78], [2, 54], [2, 61], [2, 63], [2, 93], [3, 51], [3, 54], [3, 66], [3, 74], [4, 51], [4, 57], [4, 66], [4, 94], [5, 49], [5, 57], [5, 68], [5, 78], [6, 54], [6, 70], [6, 73], [6, 74], [7, 63], [7, 86], [7, 90], [7, 96], [8, 51], [8, 56], [8, 64], [8, 75], [9, 49], [9, 62], [9, 77], [9, 90], [10, 57], [10, 70], [10, 73], [10, 94], [11, 68], [11, 82], [11, 86], [11, 90], [12, 56], [12, 64], [12, 70], [12, 91], [13, 61], [13, 62], [13, 67], [13, 90], [14, 57], [14, 61], [14, 68], [14, 93], [15, 59], [15, 63], [15, 80], [15, 96], [16, 51], [16, 72], [16, 75], [16, 79], [17, 49], [17, 58], [17, 77], [17, 80], [18, 66], [18, 85], [18, 93], [18, 95], [19, 50], [19, 66], [19, 78], [19, 95], [20, 65], [20, 83], [20, 86], [20, 87], [21, 56], [21, 60], [21, 69], [21, 87], [22, 60], [22, 62], [22, 65], [22, 88], [23, 59], [23, 68], [23, 80], [23, 82], [24, 70], [24, 72], [24, 79], [24, 91], [25, 58], [25, 61], [25, 67], [25, 80], [26, 52], [26, 73], [26, 85], [26, 93], [27, 59], [27, 81], [27, 83], [27, 87], [28, 60], [28, 69], [28, 72], [28, 89], [29, 58], [29, 60], [29, 81], [29, 88], [30, 50], [30, 52], [30, 73], [30, 78], [31, 55], [31, 65], [31, 86], [31, 89], [32, 56], [32, 71], [32, 76], [32, 87], [33, 62], [33, 65], [33, 71], [33, 92], [34, 64], [34, 82], [34, 83], [34, 94], [35, 64], [35, 74], [35, 83], [35, 96], [36, 67], [36, 84], [36, 85], [36, 88], [37, 69], [37, 75], [37, 84], [37, 95], [38, 55], [38, 59], [38, 81], [38, 89], [39, 71], [39, 72], [39, 76], [39, 89], [40, 58], [40, 71], [40, 81], [40, 92], [41, 55], [41, 79], [41, 82], [41, 94], [42, 50], [42, 77], [42, 84], [42, 88], [43, 52], [43, 69], [43, 84], [43, 91], [44, 55], [44, 74], [44, 79], [44, 96], [45, 53], [45, 67], [45, 85], [45, 92], [46, 53], [46, 75], [46, 76], [46, 95], [47, 50], [47, 53], [47, 77], [47, 92], [48, 52], [48, 53], [48, 76], [48, 91]]);;
R:=P177Census(D);;Need(Size(R.F)=3072);;
PrintTo("current_c4_descent/096_029.g","L059Result := ",R,";\n");
Print("L059_DESCENT_COMPLETE 096_029 ",Length(R.witnesses)," ",Runtime()-t,"\n");
QUIT;
